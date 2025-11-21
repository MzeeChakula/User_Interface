from fastapi import APIRouter, HTTPException, status
from api.models.ai import (
    TranslateRequest, TranslateResponse, 
    LanguageDetectRequest, LanguageDetectResponse,
    RAGQuery, RAGResponse
)
from api.services.sunbird import sunbird_service
from api.services.rag_service import get_rag_service

router = APIRouter(
    prefix="/ai",
    tags=["AI Services"],
    responses={404: {"description": "Not found"}},
)

@router.post("/detect-language", response_model=LanguageDetectResponse)
async def detect_language(request: LanguageDetectRequest):
    """
    Detect the language of the given text using Sunbird AI.
    Supports all Ugandan languages (Luganda, Runyankole, Acholi, Ateso, Lugbara).
    """
    try:
        result = await sunbird_service.detect_language(request.text)
        
        return LanguageDetectResponse(
            language=result["language"],
            language_name=result["language_name"],
            confidence=result["confidence"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Language detection failed: {str(e)}"
        )

@router.get("/languages")
async def get_supported_languages():
    """
    Get list of supported Ugandan languages.
    """
    try:
        languages = await sunbird_service.get_supported_languages()
        return {"languages": languages}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch languages: {str(e)}"
        )

@router.post("/translate", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest):
    """
    Translate text using Sunbird AI.
    Supports all Ugandan languages: Luganda, Runyankole, Acholi, Ateso, Lugbara.
    Auto-detects source language if not provided.
    """
    try:
        result = await sunbird_service.translate(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
        return TranslateResponse(
            translated_text=result["translated_text"],
            source_language=result["source_language"],
            target_language=result["target_language"],
            source_language_name=result.get("source_language_name"),
            target_language_name=result.get("target_language_name")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation failed: {str(e)}"
        )

@router.post("/rag", response_model=RAGResponse)
async def rag_query(query: RAGQuery):
    """
    Answer a query using RAG with ChromaDB and Tavily search.
    """
    try:
        # Get service instance
        rag_service = get_rag_service()

        result = await rag_service.answer_query(
            query=query.query,
            chat_history=query.chat_history,
            use_search=query.use_search
        )
        
        return RAGResponse(
            answer=result["answer"],
            sources=result["sources"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"RAG query failed: {str(e)}"
        )

