from datetime import datetime, timedelta
from typing import Optional, Union, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_
import secrets
import logging

from app.core.config import settings
from app.db.session import get_session
from app.db.models import User, RefreshToken

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT Bearer
security = HTTPBearer()


class SecurityManager:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(
        data: Dict[str, Any], 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(
        data: Dict[str, Any], 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create JWT refresh token"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh",
            "jti": secrets.token_urlsafe(32)  # Unique token ID
        })
        
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(
                token, 
                settings.SECRET_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            
            # Verify token type
            if payload.get("type") != token_type:
                return None
            
            # Check expiration
            exp = payload.get("exp")
            if exp and datetime.utcnow().timestamp() > exp:
                return None
                
            return payload
            
        except JWTError as e:
            logger.warning(f"JWT Error: {str(e)}")
            return None
    
    @staticmethod
    async def store_refresh_token(
        db: AsyncSession, 
        user_id: int, 
        token: str
    ) -> RefreshToken:
        """Store refresh token in database"""
        # Decode token to get expiration
        payload = SecurityManager.verify_token(token, "refresh")
        if not payload:
            raise ValueError("Invalid refresh token")
        
        expires_at = datetime.fromtimestamp(payload.get("exp"))
        
        # Create refresh token record
        db_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
            is_revoked=False
        )
        
        db.add(db_token)
        await db.commit()
        await db.refresh(db_token)
        
        return db_token
    
    @staticmethod
    async def revoke_refresh_token(
        db: AsyncSession, 
        token: str
    ) -> bool:
        """Revoke refresh token"""
        try:
            stmt = (
                update(RefreshToken)
                .where(RefreshToken.token == token)
                .values(is_revoked=True)
            )
            result = await db.execute(stmt)
            await db.commit()
            
            return result.rowcount > 0
        except Exception as e:
            logger.error(f"Error revoking refresh token: {str(e)}")
            return False
    
    @staticmethod
    async def validate_refresh_token(
        db: AsyncSession, 
        token: str
    ) -> Optional[User]:
        """Validate refresh token and return associated user"""
        # First verify JWT token
        payload = SecurityManager.verify_token(token, "refresh")
        if not payload:
            return None
        
        # Check if token exists in database and is not revoked
        stmt = (
            select(RefreshToken, User)
            .join(User, RefreshToken.user_id == User.id)
            .where(
                and_(
                    RefreshToken.token == token,
                    RefreshToken.is_revoked == False,
                    RefreshToken.expires_at > datetime.utcnow(),
                    User.is_active == True
                )
            )
        )
        
        result = await db.execute(stmt)
        token_user = result.first()
        
        if not token_user:
            return None
            
        return token_user.User
    
    @staticmethod
    async def cleanup_expired_tokens(db: AsyncSession) -> int:
        """Remove expired refresh tokens"""
        try:
            stmt = select(RefreshToken).where(
                RefreshToken.expires_at < datetime.utcnow()
            )
            result = await db.execute(stmt)
            expired_tokens = result.scalars().all()
            
            for token in expired_tokens:
                await db.delete(token)
            
            await db.commit()
            
            logger.info(f"Cleaned up {len(expired_tokens)} expired refresh tokens")
            return len(expired_tokens)
            
        except Exception as e:
            logger.error(f"Error cleaning up expired tokens: {str(e)}")
            return 0


# Function to authenticate user
async def authenticate_user(
    db: AsyncSession, 
    email: str, 
    password: str
) -> Optional[User]:
    """Authenticate user with email and password"""
    try:
        stmt = select(User).where(
            and_(
                User.email == email, 
                User.is_active == True
            )
        )
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        # Verify password
        if not SecurityManager.verify_password(password, user.hashed_password):
            return None
        
        # Update last login
        user.last_login = datetime.utcnow()
        await db.commit()
        
        return user
        
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        return None


# Dependency to get current user from access token
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_session)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Verify token
    payload = SecurityManager.verify_token(credentials.credentials, "access")
    if payload is None:
        raise credentials_exception
    
    # Get user ID from token
    user_id: str = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    # Get user from database
    try:
        user_id_int = int(user_id)
        stmt = select(User).where(
            and_(
                User.id == user_id_int, 
                User.is_active == True
            )
        )
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if user is None:
            raise credentials_exception
            
        return user
        
    except (ValueError, Exception) as e:
        logger.error(f"Error getting current user: {str(e)}")
        raise credentials_exception


# Dependency to get current active user
async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    return current_user


# Optional dependency for optional authentication
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: AsyncSession = Depends(get_session)
) -> Optional[User]:
    """Get current user if authenticated, None otherwise"""
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None


# Password validation
def validate_password_strength(password: str) -> bool:
    """Validate password strength"""
    if len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    return all([has_upper, has_lower, has_digit, has_special])


# Email validation (additional to Pydantic)
def validate_email_format(email: str) -> bool:
    """Additional email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# Rate limiting helper (for future implementation)
class RateLimiter:
    """Simple rate limiter for authentication attempts"""
    
    def __init__(self):
        self.attempts = {}
    
    def is_allowed(self, identifier: str, max_attempts: int = 5, window_minutes: int = 15) -> bool:
        """Check if identifier is allowed based on rate limiting"""
        now = datetime.utcnow()
        window_start = now - timedelta(minutes=window_minutes)
        
        if identifier not in self.attempts:
            self.attempts[identifier] = []
        
        # Clean old attempts
        self.attempts[identifier] = [
            attempt_time for attempt_time in self.attempts[identifier]
            if attempt_time > window_start
        ]
        
        # Check if under limit
        return len(self.attempts[identifier]) < max_attempts
    
    def record_attempt(self, identifier: str):
        """Record an authentication attempt"""
        if identifier not in self.attempts:
            self.attempts[identifier] = []
        
        self.attempts[identifier].append(datetime.utcnow())


# Global rate limiter instance
rate_limiter = RateLimiter()