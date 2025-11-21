from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from .database import Base

# --- Pydantic Schemas ---

class UserBase(BaseModel):
    """Base user schema"""
    email: str = Field(..., description="User email")
    full_name: Optional[str] = Field(None, description="User full name")
    is_active: bool = Field(default=True, description="Is user active")

class UserCreate(UserBase):
    """User creation schema"""
    password: str = Field(..., min_length=8, description="User password")

class UserLogin(BaseModel):
    """User login schema"""
    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")

class User(UserBase):
    """User response schema"""
    id: int = Field(..., description="User ID")
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    """JWT token schema"""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """JWT token data schema"""
    email: Optional[str] = None

# --- SQLAlchemy Models ---

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    conversations = relationship("ConversationDB", back_populates="owner")
