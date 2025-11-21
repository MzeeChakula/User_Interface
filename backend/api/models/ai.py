"""
AI-related Pydantic schemas
"""
from typing import Optional, List, Dict
from pydantic import BaseModel

class TranslateRequest(BaseModel):
    text: str
    source_lang: Optional[str] = None  # Auto-detect if not provided
    target_lang: str = "eng"  # Default to English

class TranslateResponse(BaseModel):
    translated_text: str
    source_language: str
    target_language: str
    source_language_name: Optional[str] = None
    target_language_name: Optional[str] = None

class LanguageDetectRequest(BaseModel):
    text: str

class LanguageDetectResponse(BaseModel):
    language: str
    language_name: str
    confidence: float

class RAGQuery(BaseModel):
    query: str
    use_search: bool = True
    chat_history: Optional[List[Dict[str, str]]] = None

class RAGResponse(BaseModel):
    answer: str
    sources: List[Dict]

