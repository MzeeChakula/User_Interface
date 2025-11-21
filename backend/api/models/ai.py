from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class TranslateRequest(BaseModel):
    """Request schema for translation"""
    text: str = Field(..., description="Text to translate")
    source_lang: str = Field(..., description="Source language code (e.g., 'en', 'lg')")
    target_lang: str = Field(..., description="Target language code (e.g., 'lg', 'en')")

class TranslateResponse(BaseModel):
    """Response schema for translation"""
    translated_text: str = Field(..., description="Translated text")
    source_lang: str = Field(..., description="Source language code")
    target_lang: str = Field(..., description="Target language code")
    confidence: Optional[float] = Field(None, description="Translation confidence score")

class RAGQuery(BaseModel):
    """Request schema for RAG query"""
    query: str = Field(..., description="User query")
    context_filters: Optional[Dict[str, Any]] = Field(None, description="Filters for knowledge graph retrieval")

class RAGResponse(BaseModel):
    """Response schema for RAG query"""
    answer: str = Field(..., description="Generated answer")
    sources: List[str] = Field(default=[], description="List of sources used")
