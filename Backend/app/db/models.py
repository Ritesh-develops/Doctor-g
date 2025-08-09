from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Boolean, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid

from app.db.session import Base


class User(Base):
    """User model for authentication"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    # Profile information
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)
    gender = Column(String(10), nullable=True)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    scans = relationship("Scan", back_populates="user", cascade="all, delete-orphan")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class RefreshToken(Base):
    """Refresh token model for JWT token management"""
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    token = Column(String(500), unique=True, index=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user = relationship("User", back_populates="refresh_tokens")

    def __repr__(self):
        return f"<RefreshToken(id={self.id}, user_id={self.user_id}, revoked={self.is_revoked})>"


class Conversation(Base):
    """Conversation model for chat history"""
    __tablename__ = "conversations"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), default="New Medical Consultation")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    # Conversation metadata - renamed to avoid conflict
    summary = Column(Text, nullable=True)
    patient_context = Column(JSON, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("ChatMessage", back_populates="conversation", cascade="all, delete-orphan")
    scans = relationship("Scan", back_populates="conversation")

    def __repr__(self):
        return f"<Conversation(id={self.id}, user_id={self.user_id}, title={self.title})>"


class ChatMessage(Base):
    """Chat message model"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default="text")  # 'text', 'image', 'analysis', 'system'
    # CHANGED: renamed 'metadata' to 'message_metadata' to avoid SQLAlchemy conflict
    message_metadata = Column(JSON, nullable=True)  # Store additional data like confidence scores, file info
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    # Message status
    is_edited = Column(Boolean, default=False)
    edited_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationship
    conversation = relationship("Conversation", back_populates="messages")

    def __repr__(self):
        return f"<ChatMessage(id={self.id}, conversation_id={self.conversation_id}, role={self.role})>"


class Scan(Base):
    """Medical scan model"""
    __tablename__ = "scans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=True)
    
    # File information
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)
    mime_type = Column(String(100), nullable=False)
    
    # Analysis results
    yolo_results = Column(JSON, nullable=True)  # Store YOLO detection results
    llm_analysis = Column(Text, nullable=True)  # Store LLM interpretation
    confidence_score = Column(Float, nullable=True)
    processing_status = Column(String(20), default="pending")  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Medical metadata - these are fine as they're specific to medical scans
    scan_type = Column(String(50), default="x-ray")
    body_part = Column(String(50), nullable=True)
    view_position = Column(String(50), nullable=True)  # PA, lateral, etc.
    
    # Relationships
    user = relationship("User", back_populates="scans")
    conversation = relationship("Conversation", back_populates="scans")

    def __repr__(self):
        return f"<Scan(id={self.id}, user_id={self.user_id}, filename={self.original_filename})>"