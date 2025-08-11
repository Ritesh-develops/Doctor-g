from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timezone
import logging

from app.core.security import get_current_active_user
from app.db.session import get_session
from app.db.models import User, Scan
from app.db.schemas import Scan as ScanSchema
from typing import List

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=List[ScanSchema])
async def get_user_scans(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    limit: int = 100,
    offset: int = 0
):
    """Get user's X-ray scans"""
    try:
        stmt = (
            select(Scan)
            .where(Scan.user_id == current_user.id)
            .order_by(Scan.created_at.desc())
            .limit(limit)
            .offset(offset)
        )
        
        result = await db.execute(stmt)
        scans = result.scalars().all()
        
        return [ScanSchema.model_validate(scan) for scan in scans]
        
    except Exception as e:
        logger.error(f"Error getting user scans: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve scans"
        )


@router.get("/count")
async def get_user_scans_count(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get count of user's X-ray scans"""
    try:
        stmt = (
            select(func.count(Scan.id))
            .where(Scan.user_id == current_user.id)
        )
        
        result = await db.execute(stmt)
        count = result.scalar()
        
        return {"count": count or 0}
        
    except Exception as e:
        logger.error(f"Error getting user scans count: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve scans count"
        )


@router.get("/stats")
async def get_user_scans_stats(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's scan statistics"""
    try:
        # Total scans count
        total_stmt = (
            select(func.count(Scan.id))
            .where(Scan.user_id == current_user.id)
        )
        total_result = await db.execute(total_stmt)
        total_count = total_result.scalar() or 0
        
        # This month scans count
        current_date = datetime.now(timezone.utc)
        month_start = current_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        month_stmt = (
            select(func.count(Scan.id))
            .where(
                Scan.user_id == current_user.id,
                Scan.created_at >= month_start
            )
        )
        month_result = await db.execute(month_stmt)
        month_count = month_result.scalar() or 0
        
        return {
            "total_scans": total_count,
            "month_scans": month_count
        }
        
    except Exception as e:
        logger.error(f"Error getting user scans stats: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve scans statistics"
        )


@router.get("/test")
async def test_scans():
    """Test scans endpoint"""
    return {
        "message": "Scans endpoint working",
        "status": "success",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }