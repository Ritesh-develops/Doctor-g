from fastapi import APIRouter

from app.api.v1 import auth, scans  # Import directly from v1, not endpoints


api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    auth.router, 
    prefix="/auth", 
    tags=["authentication"]
)

api_router.include_router(
    scans.router, 
    prefix="/scans", 
    tags=["medical-scans"]
)


@api_router.get("/", tags=["root"])
async def api_root():
    """API v1 root endpoint"""
    return {
        "message": "Doctor-G API v1",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth",
            "scans": "/scans"
        }
    }