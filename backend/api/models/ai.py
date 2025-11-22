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

class VoiceTranscriptionResponse(BaseModel):
    text: str
    language: Optional[str] = None
    duration: Optional[float] = None

class VoiceQueryRequest(BaseModel):
    translate_to: Optional[str] = None  # Optional: translate transcribed text
    detect_language: bool = False  # Optional: detect language of transcribed text

class VoiceQueryResponse(BaseModel):
    transcribed_text: str
    detected_language: Optional[str] = None
    detected_language_name: Optional[str] = None
    translated_text: Optional[str] = None
    translation_target: Optional[str] = None
