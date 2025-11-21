from fastapi import APIRouter, HTTPException, status
from api.models.ai import TranslateRequest, TranslateResponse
from api.services.sunbird import sunbird_service

router = APIRouter(
    prefix="/ai",
    tags=["AI Services"],
    responses={404: {"description": "Not found"}},
)

@router.post("/translate", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest):
    """
    Translate text using Sunbird AI.
    """
    try:
        result = await sunbird_service.translate(
            text=request.text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
        # Adapt response based on actual API return structure
        # Assuming result contains 'text' or similar
        translated_text = result.get("text") or result.get("translated_text")
        
        if not translated_text:
            # Fallback if structure is different
            translated_text = str(result)
            
        return TranslateResponse(
            translated_text=translated_text,
            source_lang=request.source_lang,
            target_lang=request.target_lang
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Translation failed: {str(e)}"
        )


