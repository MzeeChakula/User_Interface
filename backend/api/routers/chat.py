import os
import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.models.chat import ChatRequest, ChatResponse, ChatMessage, ConversationDB, MessageDB
from api.models.user import UserDB
from api.models.database import get_db
from api.core.deps import get_current_user

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
    responses={404: {"description": "Not found"}},
)



from api.services.llm_service import llm_service

@router.post("/message", response_model=ChatResponse)
async def chat_message(
    request: ChatRequest,
    current_user: UserDB = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to the AI assistant.
    """
    try:
        # 1. Handle Conversation
        conversation_id = request.conversation_id
        if not conversation_id:
            # Create new conversation
            conversation_id = str(uuid.uuid4())
            new_conversation = ConversationDB(
                id=conversation_id,
                user_id=current_user.id,
                title=request.message[:30] + "..." # Simple title from first message
            )
            db.add(new_conversation)
            db.commit()
        else:
            # Verify conversation belongs to user
            conversation = db.query(ConversationDB).filter(
                ConversationDB.id == conversation_id,
                ConversationDB.user_id == current_user.id
            ).first()
            if not conversation:
                # If not found or not owned, create new one (or raise error)
                conversation_id = str(uuid.uuid4())
                new_conversation = ConversationDB(
                    id=conversation_id,
                    user_id=current_user.id,
                    title=request.message[:30] + "..."
                )
                db.add(new_conversation)
                db.commit()

        # 2. Save User Message
        user_msg = MessageDB(
            conversation_id=conversation_id,
            role="user",
            content=request.message
        )
        db.add(user_msg)
        db.commit()

        # 3. Construct messages for LLM
        messages = [
            {"role": "system", "content": "You are Mzee Chakula, a helpful nutritional assistant for elderly care in Uganda. You provide culturally relevant advice."}
        ]
        
        # Load history from DB if not provided in request, or trust request?
        # Better to load from DB for consistency, but for now let's use request history + current message
        # Actually, let's use the DB history for context if we want true persistence
        # For simplicity in this step, we'll stick to the request history but append the new message
        
        for msg in request.history:
            messages.append({"role": msg.role, "content": msg.content})
            
        messages.append({"role": "user", "content": request.message})
        
        # 4. Call Groq API via LLM Service
        response_content = llm_service.get_completion(messages)
        
        # 5. Save Assistant Response
        assistant_msg = MessageDB(
            conversation_id=conversation_id,
            role="assistant",
            content=response_content
        )
        db.add(assistant_msg)
        db.commit()
        
        return ChatResponse(
            response=response_content,
            conversation_id=conversation_id,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat service error: {str(e)}"
        )
