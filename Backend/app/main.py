from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
import time
import logging
import os

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.session import sessionmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application lifespan events"""
    
    # Startup
    logger.info("🚀 Starting Doctor-G Backend API...")
    logger.info(f"📊 Version: {settings.VERSION}")
    logger.info(f"🐛 Debug Mode: {settings.DEBUG}")
    logger.info(f"🔒 CORS Origins: {settings.BACKEND_CORS_ORIGINS}")
    
    # Initialize database connection pool
    sessionmanager.init(settings.DATABASE_URL)
    logger.info("✅ Database connection initialized")
    
    # Verify YOLO model exists
    if os.path.exists(settings.YOLO_MODEL_PATH):
        logger.info("✅ YOLO model found")
    else:
        logger.warning("⚠️ YOLO model not found - X-ray analysis will not work")
    
    # Verify Groq API key
    if settings.GROQ_API_KEY:
        logger.info("✅ Groq API key configured")
    else:
        logger.warning("⚠️ Groq API key not configured - LLM analysis will not work")
    
    # Create upload directory if it doesn't exist
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    logger.info(f"✅ Upload directory ready: {settings.UPLOAD_DIR}")
    
    logger.info("🎉 Doctor-G Backend API started successfully!")
    
    # Application is running
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down Doctor-G Backend API...")
    
    # Close database connections
    await sessionmanager.close()
    logger.info("✅ Database connections closed")
    
    logger.info("👋 Doctor-G Backend API shutdown complete")


def create_application() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.VERSION,
        description="AI-powered medical imaging analysis platform with YOLO detection and LLM interpretation",
        openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.DEBUG else None,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
        lifespan=lifespan,  # Use lifespan instead of on_event
    )
    
    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Add trusted host middleware for security
    if not settings.DEBUG:
        app.add_middleware(
            TrustedHostMiddleware, 
            allowed_hosts=settings.BACKEND_CORS_ORIGINS
        )
    
    # Add custom middleware for request timing and logging
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        # Log request details (only in debug mode to avoid spam)
        if settings.DEBUG:
            logger.info(
                f"{request.method} {request.url.path} - "
                f"Status: {response.status_code} - "
                f"Time: {process_time:.4f}s"
            )
        return response
    
    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    return app


# Create FastAPI app
app = create_application()


# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "status_code": exc.status_code,
            "timestamp": time.time(),
            "path": request.url.path
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors"""
    logger.error(f"Validation error on {request.url.path}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "error": True,
            "message": "Validation Error",
            "details": exc.errors(),
            "status_code": 422,
            "timestamp": time.time(),
            "path": request.url.path
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unexpected error on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error" if not settings.DEBUG else str(exc),
            "status_code": 500,
            "timestamp": time.time(),
            "path": request.url.path
        }
    )


# Health check endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Doctor-G API",
        "version": settings.VERSION,
        "status": "healthy",
        "timestamp": time.time(),
        "docs": "/docs" if settings.DEBUG else None
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "timestamp": time.time(),
        "services": {
            "database": "connected",
            "yolo_model": "loaded" if os.path.exists(settings.YOLO_MODEL_PATH) else "missing",
            "groq_api": "configured" if settings.GROQ_API_KEY else "missing",
            "upload_directory": "ready" if os.path.exists(settings.UPLOAD_DIR) else "missing"
        }
    }


@app.get("/info")
async def api_info():
    """API information endpoint"""
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "description": "AI-powered medical imaging analysis platform",
        "features": [
            "OAuth2 JWT Authentication",
            "X-ray Image Analysis",
            "YOLO Object Detection",
            "LLM Medical Interpretation",
            "Conversation Management",
            "Medical History Tracking",
            "Refresh Token Management"
        ],
        "endpoints": {
            "auth": f"{settings.API_V1_STR}/auth",
            "chats": f"{settings.API_V1_STR}/chats", 
            "scans": f"{settings.API_V1_STR}/scans"
        },
        "authentication": {
            "type": "Bearer JWT",
            "access_token_expire_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
            "refresh_token_expire_minutes": settings.REFRESH_TOKEN_EXPIRE_MINUTES
        },
        "timestamp": time.time()
    }


# Development endpoint to check configuration
@app.get("/config")
async def config_info():
    """Configuration information (debug only)"""
    if not settings.DEBUG:
        return {"message": "Configuration info only available in debug mode"}
    
    return {
        "debug": settings.DEBUG,
        "database_configured": bool(settings.DATABASE_URL),
        "groq_configured": bool(settings.GROQ_API_KEY),
        "cors_origins": settings.BACKEND_CORS_ORIGINS,
        "upload_dir": settings.UPLOAD_DIR,
        "max_upload_size": settings.MAX_UPLOAD_SIZE,
        "allowed_extensions": list(settings.ALLOWED_EXTENSIONS),
        "yolo_model_path": settings.YOLO_MODEL_PATH
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info" if settings.DEBUG else "warning"
    )