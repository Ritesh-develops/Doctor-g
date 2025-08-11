from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc, and_
from datetime import datetime, timezone
import uuid
import os
import logging
from typing import List, Optional, Dict, Any
import aiofiles

from app.core.config import settings
from app.core.security import get_current_active_user
from app.db.session import get_session
from app.db.models import User, Conversation, ChatMessage, Scan
from app.db.schemas import (
    Conversation as ConversationSchema,
    ConversationCreate,
    ConversationUpdate,
    ChatMessage as ChatMessageSchema,
    SendMessageRequest,
    Scan as ScanSchema,
    ProcessingStatus
)
from app.services.yolo_service import yolo_service
from app.services.llm_service import llm_service

logger = logging.getLogger(__name__)

# Create router for chat endpoints
chat_router = APIRouter()


@chat_router.get("/conversations/", response_model=List[ConversationSchema])
async def get_conversations(
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    limit: int = 50,
    offset: int = 0
):
    """Get user's conversations with message count"""
    try:
        # Get conversations with message counts
        stmt = (
            select(
                Conversation,
                func.count(ChatMessage.id).label('message_count')
            )
            .outerjoin(ChatMessage, Conversation.id == ChatMessage.conversation_id)
            .where(
                and_(
                    Conversation.user_id == current_user.id,
                    Conversation.is_active == True
                )
            )
            .group_by(Conversation.id)
            .order_by(desc(Conversation.updated_at))
            .limit(limit)
            .offset(offset)
        )
        
        result = await db.execute(stmt)
        conversations_with_counts = result.all()
        
        # Format response
        conversations = []
        for conversation, message_count in conversations_with_counts:
            conv_data = ConversationSchema.model_validate(conversation)
            conv_data.message_count = message_count or 0
            conversations.append(conv_data)
        
        return conversations
        
    except Exception as e:
        logger.error(f"Error getting conversations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversations"
        )


@chat_router.post("/conversations/")
async def create_conversation(
    conversation_data: Optional[ConversationCreate] = None,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new conversation"""
    try:
        # Create conversation
        conversation = Conversation(
            id=str(uuid.uuid4()),
            user_id=current_user.id,
            title=conversation_data.title if conversation_data else "New Medical Consultation",
            patient_context=conversation_data.patient_context if conversation_data else None
        )
        
        db.add(conversation)
        await db.flush()  # Get the ID without committing
        
        # Create initial system message
        system_message = ChatMessage(
            conversation_id=conversation.id,
            role="system",
            content="Hello! I'm Dr. AI, your medical assistant. I can help analyze your X-ray images and answer questions about the results. Please upload an X-ray image to begin, or feel free to ask any medical questions you might have.",
            message_type="system"
        )
        
        db.add(system_message)
        await db.commit()
        await db.refresh(conversation)
        
        return {
            "conversation_id": conversation.id,
            "title": conversation.title,
            "created_at": conversation.created_at,
            "message": "Conversation created successfully"
        }
        
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating conversation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create conversation"
        )


@chat_router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific conversation"""
    try:
        stmt = select(Conversation).where(
            and_(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id,
                Conversation.is_active == True
            )
        )
        result = await db.execute(stmt)
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        return ConversationSchema.model_validate(conversation)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversation"
        )


@chat_router.put("/conversations/{conversation_id}")
async def update_conversation(
    conversation_id: str,
    conversation_update: ConversationUpdate,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Update a conversation"""
    try:
        stmt = select(Conversation).where(
            and_(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id,
                Conversation.is_active == True
            )
        )
        result = await db.execute(stmt)
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Update fields
        update_data = conversation_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(conversation, field, value)
        
        conversation.updated_at = datetime.now(timezone.utc)
        
        await db.commit()
        await db.refresh(conversation)
        
        return ConversationSchema.model_validate(conversation)
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating conversation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update conversation"
        )


@chat_router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Delete a conversation (soft delete)"""
    try:
        stmt = select(Conversation).where(
            and_(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id
            )
        )
        result = await db.execute(stmt)
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Soft delete
        conversation.is_active = False
        conversation.updated_at = datetime.now(timezone.utc)
        
        await db.commit()
        
        return {"message": "Conversation deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error deleting conversation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete conversation"
        )


@chat_router.get("/conversations/{conversation_id}/messages", response_model=List[ChatMessageSchema])
async def get_conversation_messages(
    conversation_id: str,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user),
    limit: int = 100,
    offset: int = 0
):
    """Get messages for a conversation"""
    try:
        # First verify conversation ownership
        conv_stmt = select(Conversation).where(
            and_(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id,
                Conversation.is_active == True
            )
        )
        conv_result = await db.execute(conv_stmt)
        conversation = conv_result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Get messages
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.conversation_id == conversation_id)
            .order_by(ChatMessage.timestamp)
            .limit(limit)
            .offset(offset)
        )
        
        result = await db.execute(stmt)
        messages = result.scalars().all()
        
        return [ChatMessageSchema.model_validate(msg) for msg in messages]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting messages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve messages"
        )


@chat_router.post("/conversations/{conversation_id}/messages")
async def send_message(
    conversation_id: str,
    message_request: SendMessageRequest,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Send a message in a conversation"""
    try:
        # Verify conversation ownership
        conv_stmt = select(Conversation).where(
            and_(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id,
                Conversation.is_active == True
            )
        )
        conv_result = await db.execute(conv_stmt)
        conversation = conv_result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Create user message
        user_message = ChatMessage(
            conversation_id=conversation_id,
            role="user",
            content=message_request.message,
            message_type="text"
        )
        
        db.add(user_message)
        await db.flush()
        
        # Get conversation history for context
        history_stmt = (
            select(ChatMessage)
            .where(ChatMessage.conversation_id == conversation_id)
            .order_by(desc(ChatMessage.timestamp))
            .limit(10)
        )
        history_result = await db.execute(history_stmt)
        recent_messages = history_result.scalars().all()
        
        # Prepare conversation history for LLM
        conversation_history = []
        for msg in reversed(recent_messages):  # Reverse to get chronological order
            if msg.role in ["user", "assistant"]:
                conversation_history.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Check if there are any recent X-ray analyses to reference
        scan_stmt = (
            select(Scan)
            .where(Scan.conversation_id == conversation_id)
            .order_by(desc(Scan.created_at))
            .limit(1)
        )
        scan_result = await db.execute(scan_stmt)
        latest_scan = scan_result.scalar_one_or_none()
        
        # Generate AI response
        try:
            if latest_scan and latest_scan.yolo_results:
                # Answer in context of X-ray analysis
                ai_response = await llm_service.answer_followup_question(
                    question=message_request.message,
                    yolo_results=latest_scan.yolo_results,
                    conversation_history=conversation_history
                )
            else:
                # General medical question - create a basic response
                ai_response = await llm_service.answer_followup_question(
                    question=message_request.message,
                    yolo_results={"detected_objects": [], "total_detections": 0, "confidence": 0.0, "summary": "No X-ray analysis available"},
                    conversation_history=conversation_history
                )
        except Exception as llm_error:
            logger.error(f"LLM error: {str(llm_error)}")
            ai_response = "I apologize, but I'm having trouble processing your question right now. Please try again, or consider uploading an X-ray image for analysis."
        
        # Create AI message
        ai_message = ChatMessage(
            conversation_id=conversation_id,
            role="assistant",
            content=ai_response,
            message_type="text"
        )
        
        db.add(ai_message)
        
        # Update conversation timestamp
        conversation.updated_at = datetime.now(timezone.utc)
        
        await db.commit()
        await db.refresh(user_message)
        await db.refresh(ai_message)
        
        return {
            "user_message": ChatMessageSchema.model_validate(user_message),
            "ai_response": ChatMessageSchema.model_validate(ai_message)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error sending message: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send message"
        )


@chat_router.post("/conversations/{conversation_id}/analyze")
async def analyze_xray(
    conversation_id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Analyze X-ray image and provide medical interpretation"""
    try:
        # Verify conversation ownership
        conv_stmt = select(Conversation).where(
            and_(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id,
                Conversation.is_active == True
            )
        )
        conv_result = await db.execute(conv_stmt)
        conversation = conv_result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Validate file
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File must be an image"
            )
        
        if file.size > settings.MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds maximum limit of {settings.MAX_UPLOAD_SIZE} bytes"
            )
        
        # Create upload directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Create scan record
        scan = Scan(
            user_id=current_user.id,
            conversation_id=conversation_id,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file.size,
            mime_type=file.content_type,
            processing_status=ProcessingStatus.PROCESSING
        )
        
        db.add(scan)
        await db.flush()
        
        # Create upload confirmation message
        upload_message = ChatMessage(
            conversation_id=conversation_id,
            role="user",
            content=f"X-ray image uploaded: {file.filename}",
            message_type="image",
            message_metadata={
                "filename": file.filename,
                "file_size": file.size,
                "scan_id": scan.id
            }
        )
        
        db.add(upload_message)
        await db.flush()
        
        try:
            # Run YOLO analysis
            yolo_results = await yolo_service.detect_nodules(file_path)
            
            # Update scan with YOLO results
            scan.yolo_results = yolo_results
            scan.confidence_score = yolo_results.get("confidence", 0.0)
            scan.processing_status = ProcessingStatus.PROCESSING
            
            # Generate LLM analysis
            llm_analysis = await llm_service.analyze_xray_results(
                yolo_results=yolo_results,
                patient_context=conversation.patient_context
            )
            
            # Update scan with LLM analysis
            scan.llm_analysis = llm_analysis
            scan.processing_status = ProcessingStatus.COMPLETED
            scan.processed_at = datetime.now(timezone.utc)
            
            # Create analysis result message
            analysis_message = ChatMessage(
                conversation_id=conversation_id,
                role="assistant",
                content=llm_analysis,
                message_type="analysis",
                message_metadata=yolo_results
            )
            
            db.add(analysis_message)
            
            # Update conversation
            conversation.updated_at = datetime.now(timezone.utc)
            
            await db.commit()
            await db.refresh(scan)
            await db.refresh(upload_message)
            await db.refresh(analysis_message)
            
            return {
                "user_message": ChatMessageSchema.model_validate(upload_message),
                "ai_analysis": {
                    "message": ChatMessageSchema.model_validate(analysis_message),
                    "yolo_results": yolo_results,
                    "confidence_score": scan.confidence_score
                },
                "scan": ScanSchema.model_validate(scan)
            }
            
        except Exception as analysis_error:
            # Update scan with error
            scan.processing_status = ProcessingStatus.FAILED
            scan.error_message = str(analysis_error)
            
            # Create error message
            error_message = ChatMessage(
                conversation_id=conversation_id,
                role="assistant",
                content="I apologize, but I encountered an error while analyzing your X-ray image. Please try uploading the image again, or contact support if the problem persists.",
                message_type="system"
            )
            
            db.add(error_message)
            await db.commit()
            
            logger.error(f"Analysis error: {str(analysis_error)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to analyze X-ray image"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.error(f"Error in X-ray analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process X-ray analysis"
        )


@chat_router.get("/conversations/{conversation_id}/scans", response_model=List[ScanSchema])
async def get_conversation_scans(
    conversation_id: str,
    db: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_active_user)
):
    """Get all scans for a conversation"""
    try:
        # Verify conversation ownership
        conv_stmt = select(Conversation).where(
            and_(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user.id,
                Conversation.is_active == True
            )
        )
        conv_result = await db.execute(conv_stmt)
        conversation = conv_result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Get scans
        stmt = (
            select(Scan)
            .where(Scan.conversation_id == conversation_id)
            .order_by(desc(Scan.created_at))
        )
        
        result = await db.execute(stmt)
        scans = result.scalars().all()
        
        return [ScanSchema.model_validate(scan) for scan in scans]
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation scans: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve scans"
        )


# Health check endpoints
@chat_router.get("/health")
async def health_check():
    """Health check for chat service"""
    try:
        yolo_status = await yolo_service.get_model_info()
        llm_status = await llm_service.get_service_status()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "services": {
                "yolo": yolo_status,
                "llm": llm_status
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }