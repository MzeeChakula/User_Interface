"""
Voice/Speech Recognition API endpoints
"""
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from typing import Optional
from api.models.ai import (
    VoiceTranscriptionResponse,
    VoiceQueryResponse,
    LanguageDetectResponse
)
from api.services.voice_service import get_voice_service
from api.services.sunbird import sunbird_service

router = APIRouter(
    prefix="/voice",
    tags=["Voice Services"],
    responses={404: {"description": "Not found"}},
)


@router.post("/transcribe", response_model=VoiceTranscriptionResponse)
async def transcribe_audio(
    audio: UploadFile = File(..., description="Audio file (mp3, wav, m4a, ogg, webm, etc.)"),
    language: Optional[str] = Form(None, description="ISO-639-1 language code (e.g., 'en', 'lg', 'sw')"),
    temperature: float = Form(0.0, description="Sampling temperature (0-1). Lower is more deterministic.")
):
    """
    Transcribe audio to text using Groq Whisper API.

    Supported audio formats: mp3, mp4, mpeg, mpga, m4a, wav, webm, ogg

    The endpoint automatically detects the language if not specified.
    """
    try:
        # Read audio file
        audio_bytes = await audio.read()

        # Get voice service
        voice_service = get_voice_service()

        # Transcribe
        result = await voice_service.transcribe_audio(
            audio_file=audio_bytes,
            filename=audio.filename,
            language=language,
            temperature=temperature
        )

        return VoiceTranscriptionResponse(
            text=result["text"],
            language=result.get("language"),
            duration=result.get("duration")
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Transcription failed: {str(e)}"
        )


@router.post("/transcribe-and-translate", response_model=VoiceQueryResponse)
async def transcribe_and_translate(
    audio: UploadFile = File(..., description="Audio file"),
    translate_to: Optional[str] = Form(None, description="Target language code (e.g., 'eng', 'lug')"),
    detect_language: bool = Form(True, description="Detect the source language")
):
    """
    Transcribe audio and optionally translate to target language.

    Workflow:
    1. Transcribe audio to text using Whisper
    2. Detect language if requested
    3. Translate to target language if specified

    Useful for multilingual applications where you want both transcription and translation.
    """
    try:
        # Read audio file
        audio_bytes = await audio.read()

        # Get services
        voice_service = get_voice_service()

        # Transcribe
        transcription_result = await voice_service.transcribe_audio(
            audio_file=audio_bytes,
            filename=audio.filename
        )

        transcribed_text = transcription_result["text"]
        detected_language = transcription_result.get("language")

        response = VoiceQueryResponse(
            transcribed_text=transcribed_text,
            detected_language=detected_language
        )

        # Detect language if requested and not already detected
        if detect_language and transcribed_text:
            try:
                lang_result = await sunbird_service.detect_language(transcribed_text)
                response.detected_language = lang_result["language"]
                response.detected_language_name = lang_result["language_name"]
            except:
                # If detection fails, use Whisper's detected language
                pass

        # Translate if target language specified
        if translate_to and transcribed_text:
            try:
                translation_result = await sunbird_service.translate(
                    text=transcribed_text,
                    source_lang=detected_language,
                    target_lang=translate_to
                )
                response.translated_text = translation_result["translated_text"]
                response.translation_target = translate_to
            except Exception as e:
                # Log but don't fail the whole request
                print(f"Translation failed: {e}")

        return response

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Voice query failed: {str(e)}"
        )


@router.get("/supported-formats")
async def get_supported_formats():
    """
    Get list of supported audio formats for transcription.
    """
    voice_service = get_voice_service()
    return {
        "formats": list(voice_service.supported_formats),
        "recommended": ["mp3", "wav", "m4a", "ogg"]
    }
