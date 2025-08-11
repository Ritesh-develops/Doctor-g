from fastapi import APIRouter

from app.api.v1 import auth, scans, endpoints  # Import endpoints


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

# Include chat endpoints
api_router.include_router(
    endpoints.chat_router,
    prefix="/chats",
    tags=["chat"]
)


@api_router.get("/", tags=["root"])
async def api_root():
    """API v1 root endpoint"""
    return {
        "message": "Doctor-G API v1",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/auth",
            "scans": "/scans",
            "chats": "/chats"
        },
        "available_routes": {
            "authentication": [
                "POST /auth/register",
                "POST /auth/login",
                "POST /auth/refresh",
                "POST /auth/logout",
                "GET /auth/me",
                "PUT /auth/me",
                "DELETE /auth/me"
            ],
            "chat": [
                "GET /chats/conversations/",
                "POST /chats/conversations/",
                "GET /chats/conversations/{conversation_id}",
                "PUT /chats/conversations/{conversation_id}",
                "DELETE /chats/conversations/{conversation_id}",
                "GET /chats/conversations/{conversation_id}/messages",
                "POST /chats/conversations/{conversation_id}/messages",
                "POST /chats/conversations/{conversation_id}/analyze",
                "GET /chats/conversations/{conversation_id}/scans",
                "GET /chats/health"
            ],
            "scans": [
                "GET /scans/",
                "GET /scans/test"
            ]
        }
    }