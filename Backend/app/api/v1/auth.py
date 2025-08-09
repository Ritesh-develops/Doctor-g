from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
import logging

from app.core.config import settings
from app.core.security import (
    SecurityManager, 
    authenticate_user, 
    get_current_active_user,
    rate_limiter
)
from app.db.session import get_session
from app.db.models import User, RefreshToken
from app.db.schemas import (
    UserCreate, 
    User as UserSchema, 
    Token, 
    RefreshTokenRequest
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", response_model=dict)
async def register_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_session)
):
    """Register a new user"""
    try:
        # Check if user already exists
        stmt = select(User).where(User.email == user_data.email)
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Create new user
        hashed_password = SecurityManager.get_password_hash(user_data.password)
        db_user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            phone=user_data.phone,
            date_of_birth=user_data.date_of_birth,
            gender=user_data.gender
        )
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        
        logger.info(f"New user registered: {user_data.email}")
        
        return {
            "message": "User registered successfully",
            "user_id": db_user.id,
            "email": db_user.email
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post("/login", response_model=Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_session)
):
    """Login user and return JWT tokens"""
    # Rate limiting
    if not rate_limiter.is_allowed(form_data.username):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many login attempts. Please try again later."
        )
    
    # Authenticate user
    user = await authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        rate_limiter.record_attempt(form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = SecurityManager.create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )
        
        # Create refresh token
        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_token = SecurityManager.create_refresh_token(
            data={"sub": str(user.id)},
            expires_delta=refresh_token_expires
        )
        
        # Store refresh token in database
        await SecurityManager.store_refresh_token(db, user.id, refresh_token)
        
        logger.info(f"User logged in: {user.email}")
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_session)
):
    """Refresh access token using refresh token"""
    user = await SecurityManager.validate_refresh_token(db, refresh_request.refresh_token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Create new access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = SecurityManager.create_access_token(
            data={"sub": str(user.id)},
            expires_delta=access_token_expires
        )
        
        # Create new refresh token
        refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        new_refresh_token = SecurityManager.create_refresh_token(
            data={"sub": str(user.id)},
            expires_delta=refresh_token_expires
        )
        
        # Revoke old refresh token and store new one
        await SecurityManager.revoke_refresh_token(db, refresh_request.refresh_token)
        await SecurityManager.store_refresh_token(db, user.id, new_refresh_token)
        
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/logout")
async def logout_user(
    refresh_request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Logout user by revoking refresh token"""
    try:
        await SecurityManager.revoke_refresh_token(db, refresh_request.refresh_token)
        
        logger.info(f"User logged out: {current_user.email}")
        
        return {"message": "Successfully logged out"}
        
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed"
        )


@router.get("/me", response_model=UserSchema)
async def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """Get current user information"""
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_user_profile(
    user_update: dict,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Update user profile"""
    try:
        # Update allowed fields
        allowed_fields = {'full_name', 'phone', 'date_of_birth', 'gender'}
        for field, value in user_update.items():
            if field in allowed_fields and hasattr(current_user, field):
                setattr(current_user, field, value)
        
        current_user.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(current_user)
        
        return current_user
        
    except Exception as e:
        logger.error(f"Profile update error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Profile update failed"
        )


@router.delete("/me")
async def delete_user_account(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Delete user account"""
    try:
        # Soft delete - just deactivate
        current_user.is_active = False
        current_user.updated_at = datetime.utcnow()
        
        # Revoke all refresh tokens
        stmt = select(RefreshToken).where(RefreshToken.user_id == current_user.id)
        result = await db.execute(stmt)
        tokens = result.scalars().all()
        
        for token in tokens:
            token.is_revoked = True
        
        await db.commit()
        
        logger.info(f"User account deleted: {current_user.email}")
        
        return {"message": "Account deleted successfully"}
        
    except Exception as e:
        logger.error(f"Account deletion error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Account deletion failed"
        )


# Test endpoint
@router.get("/test")
async def test_auth():
    """Test auth endpoint"""
    return {
        "message": "Auth endpoint working",
        "status": "success",
        "timestamp": datetime.utcnow()
    }