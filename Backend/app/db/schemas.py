from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# Enums
class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    ANALYSIS = "analysis"
    SYSTEM = "system"


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# Base schemas
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength with better error messages"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        has_digit = any(char.isdigit() for char in v)
        has_upper = any(char.isupper() for char in v)
        has_lower = any(char.islower() for char in v)
        has_special = any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?" for char in v)
        
        missing = []
        if not has_digit:
            missing.append("at least one digit")
        if not has_upper:
            missing.append("at least one uppercase letter")
        if not has_lower:
            missing.append("at least one lowercase letter")
        
        if missing:
            error_msg = f"Password must contain {', '.join(missing)}"
            raise ValueError(error_msg)
        
        return v


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    gender: Optional[str] = None


class UserInDB(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    
    model_config = {"from_attributes": True}  # Updated for Pydantic v2


class User(UserInDB):
    pass


# Authentication schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None
    iat: Optional[int] = None
    type: Optional[str] = None  # "access" or "refresh"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


# Login schemas
class UserLogin(BaseModel):
    username: EmailStr  # FastAPI OAuth2PasswordRequestForm uses 'username'
    password: str


class LoginResponse(BaseModel):
    user: User
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


# Chat schemas
class ConversationBase(BaseModel):
    title: str = "New Medical Consultation"
    patient_context: Optional[Dict[str, Any]] = None


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    patient_context: Optional[Dict[str, Any]] = None
    summary: Optional[str] = None


class ConversationInDB(ConversationBase):
    id: str
    user_id: int
    created_at: datetime
    updated_at: datetime
    is_active: bool
    summary: Optional[str] = None
    
    model_config = {"from_attributes": True}  # Updated for Pydantic v2


class Conversation(ConversationInDB):
    message_count: int = 0


class ChatMessageBase(BaseModel):
    role: MessageRole
    content: str
    message_type: MessageType = MessageType.TEXT
    message_metadata: Optional[Dict[str, Any]] = None


class ChatMessageCreate(ChatMessageBase):
    conversation_id: str


class ChatMessageUpdate(BaseModel):
    content: Optional[str] = None
    message_metadata: Optional[Dict[str, Any]] = None


class ChatMessageInDB(ChatMessageBase):
    id: int
    conversation_id: str
    timestamp: datetime
    is_edited: bool = False
    edited_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}  # Updated for Pydantic v2


class ChatMessage(ChatMessageInDB):
    @property
    def metadata(self):
        """For backward compatibility with frontend"""
        return self.message_metadata


# Scan schemas
class ScanBase(BaseModel):
    scan_type: str = "x-ray"
    body_part: Optional[str] = None
    view_position: Optional[str] = None


class ScanCreate(ScanBase):
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str
    conversation_id: Optional[str] = None


class ScanUpdate(BaseModel):
    yolo_results: Optional[Dict[str, Any]] = None
    llm_analysis: Optional[str] = None
    confidence_score: Optional[float] = None
    processing_status: ProcessingStatus = ProcessingStatus.PENDING
    error_message: Optional[str] = None
    processed_at: Optional[datetime] = None
    body_part: Optional[str] = None
    view_position: Optional[str] = None


class ScanInDB(ScanBase):
    id: int
    user_id: int
    conversation_id: Optional[str] = None
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str
    yolo_results: Optional[Dict[str, Any]] = None
    llm_analysis: Optional[str] = None
    confidence_score: Optional[float] = None
    processing_status: ProcessingStatus = ProcessingStatus.PENDING
    error_message: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}  # Updated for Pydantic v2


class Scan(ScanInDB):
    pass


# API Response schemas
class APIResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    details: Optional[Any] = None


# File upload schema
class FileUploadResponse(BaseModel):
    filename: str
    file_path: str
    file_size: int
    mime_type: str
    upload_timestamp: datetime


# Analysis request/response schemas
class AnalysisRequest(BaseModel):
    conversation_id: str


class AnalysisResult(BaseModel):
    user_message: ChatMessage
    ai_analysis: Dict[str, Any]
    scan: Scan


# Message sending schema
class SendMessageRequest(BaseModel):
    message: str