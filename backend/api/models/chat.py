from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from .database import Base

# --- Pydantic Schemas ---

class ChatMessage(BaseModel):
    """Chat message schema"""
    role: str = Field(..., description="Message role (user/assistant)")
    content: str = Field(..., description="Message content")
    timestamp: Optional[str] = Field(None, description="Message timestamp")

class ChatRequest(BaseModel):
    """Chat request schema"""
    message: str = Field(..., description="User message")
    history: List[ChatMessage] = Field(default=[], description="Conversation history")
    conversation_id: Optional[str] = Field(None, description="Conversation ID")

class ChatResponse(BaseModel):
    """Chat response schema"""
    response: str = Field(..., description="Assistant response")
    conversation_id: str = Field(..., description="Conversation ID")
    timestamp: str = Field(..., description="Response timestamp")

# --- SQLAlchemy Models ---

class ConversationDB(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, index=True) # UUID
    title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("UserDB", back_populates="conversations")
    messages = relationship("MessageDB", back_populates="conversation")

class MessageDB(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, ForeignKey("conversations.id"))
    role = Column(String) # user/assistant
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("ConversationDB", back_populates="messages")
