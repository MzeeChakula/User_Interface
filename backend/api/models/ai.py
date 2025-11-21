"""
AI-related Pydantic schemas
"""
from typing import Optional, List, Dict
from pydantic import BaseModel

class TranslateRequest(BaseModel):
    text: str
    source_lang: str = "en"
    target_lang: str = "lg"  # Luganda

class TranslateResponse(BaseModel):
    translated_text: str
    source_lang: str
    target_lang: str

class RAGQuery(BaseModel):
    query: str
    use_search: bool = True
    chat_history: Optional[List[Dict[str, str]]] = None

class RAGResponse(BaseModel):
    answer: str
    sources: List[Dict]
