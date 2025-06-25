from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from core.auth import get_current_user, User
from services.chat_service_v2 import ChatServiceV2

router = APIRouter(prefix="/chat", tags=["chat"])

# Request/Response models
class ChatMessage(BaseModel):
    message: str
    # selected_collections removed - not needed for PineScript trading assistant

class NewConversation(BaseModel):
    thread_name: Optional[str] = None

class UpdateThreadName(BaseModel):
    new_name: str

class ChatResponse(BaseModel):
    success: bool
    response: Optional[dict] = None
    conversation_id: Optional[str] = None
    thread_name: Optional[str] = None
    error: Optional[str] = None
    tokens: Optional[int] = None
    cost: Optional[float] = None

class ConversationListResponse(BaseModel):
    success: bool
    conversations: List[dict]
    total: int
    error: Optional[str] = None

# Create service instance
chat_service = ChatServiceV2()

# ========================
# CONVERSATION MANAGEMENT
# ========================

@router.post("/new")
async def create_conversation(
    data: NewConversation,
    user: User = Depends(get_current_user)
):
    """Create a new conversation thread"""
    result = chat_service.create_new_conversation(
        user_uuid=user.uuid,
        thread_name=data.thread_name
    )
    
    if result['success']:
        return {
            "success": True,
            "conversation_id": result['conversation_id'],
            "thread_name": result['thread_name'],
            "message": "New conversation created"
        }
    else:
        raise HTTPException(status_code=400, detail=result.get('error', 'Failed to create conversation'))

@router.get("/list")
async def list_conversations(
    user: User = Depends(get_current_user)
):
    """List all conversations for the current user"""
    result = chat_service.list_user_conversations(user.uuid)
    return ConversationListResponse(**result)

@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    user: User = Depends(get_current_user)
):
    """Get a specific conversation"""
    result = chat_service.get_conversation(user.uuid, conversation_id)
    
    if result['success']:
        return result['conversation']
    else:
        raise HTTPException(status_code=404, detail=result.get('error', 'Conversation not found'))

# ========================
# MESSAGE HANDLING
# ========================

@router.post("/{conversation_id}/message")
async def send_message(
    conversation_id: str,
    message: ChatMessage,
    user: User = Depends(get_current_user)
):
    """Send a message to an existing conversation"""
    result = chat_service.process_message(
        user_uuid=user.uuid,
        conversation_id=conversation_id,
        message=message.message
    )
    return ChatResponse(**result)

# ========================
# CONVERSATION MANAGEMENT
# ========================

@router.put("/{conversation_id}/name")
async def update_conversation_name(
    conversation_id: str,
    data: UpdateThreadName,
    user: User = Depends(get_current_user)
):
    """Update the name of a conversation thread"""
    result = chat_service.update_conversation_name(
        user_uuid=user.uuid,
        conversation_id=conversation_id,
        new_name=data.new_name
    )
    
    if result['success']:
        return {"message": result['message']}
    else:
        raise HTTPException(status_code=400, detail=result.get('error', 'Failed to update name'))

@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    user: User = Depends(get_current_user)
):
    """Delete a conversation"""
    result = chat_service.delete_conversation(user.uuid, conversation_id)
    
    if result['success']:
        return {"message": result['message']}
    else:
        raise HTTPException(status_code=400, detail=result.get('error', 'Failed to delete conversation'))

# ========================
# USER STATISTICS
# ========================

@router.get("/user/stats")
async def get_user_stats(
    user: User = Depends(get_current_user)
):
    """Get user statistics"""
    result = chat_service.get_user_stats(user.uuid)
    
    if result['success']:
        return result['stats']
    else:
        raise HTTPException(status_code=400, detail=result.get('error', 'Failed to get stats'))

# ========================
# BACKWARD COMPATIBILITY
# ========================

@router.post("/{conversation_id}")
async def send_message_legacy(
    conversation_id: str,
    message: ChatMessage,
    user: User = Depends(get_current_user)
):
    """Legacy endpoint - redirects to new message endpoint"""
    return await send_message(conversation_id, message, user)