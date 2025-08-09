from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import logging

from app.core.security import get_current_active_user
from app.db.session import get_session
from app.db.models import User

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
async def get_scans(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's scans"""
    return {
        "message": "Scans endpoint working",
        "user_id": current_user.id,
        "scans": []  # TODO: Implement actual scan retrieval
    }


@router.get("/test")
async def test_scans():
    """Test scans endpoint"""
    return {
        "message": "Scans endpoint working",
        "status": "success",
        "timestamp": datetime.utcnow()
    }