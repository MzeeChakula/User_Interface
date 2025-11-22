"""
Voice/Speech Recognition Service using Groq Whisper API
"""
import os
from typing import Optional, Dict
from groq import Groq
import tempfile


class VoiceService:
    """
    Service for speech-to-text using Groq's Whisper API.
    Supports multiple audio formats: mp3, mp4, mpeg, mpga, m4a, wav, webm
    """

    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        self.client = Groq(api_key=self.groq_api_key)

        # Supported audio formats by Groq Whisper
        self.supported_formats = {
            'mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm', 'ogg'
        }

    async def transcribe_audio(
        self,
        audio_file: bytes,
        filename: str,
        language: Optional[str] = None,
        prompt: Optional[str] = None,
        temperature: float = 0.0
    ) -> Dict:
        """
        Transcribe audio to text using Groq Whisper API.

        Args:
            audio_file: Audio file bytes
            filename: Original filename (used to determine format)
            language: Optional ISO-639-1 language code (e.g., 'en', 'lg', 'sw')
            prompt: Optional text to guide the model's style
            temperature: Sampling temperature (0-1). Lower is more deterministic.

        Returns:
            Dict with transcription text and metadata

        Raises:
            ValueError: If audio format is not supported
            Exception: If transcription fails
        """
        # Validate file format
        file_extension = filename.split('.')[-1].lower()
        if file_extension not in self.supported_formats:
            raise ValueError(
                f"Unsupported audio format: {file_extension}. "
                f"Supported formats: {', '.join(self.supported_formats)}"
            )

        try:
            # Create a temporary file to save the audio
            # Groq API requires a file-like object
            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=f".{file_extension}"
            ) as temp_audio:
                temp_audio.write(audio_file)
                temp_audio_path = temp_audio.name

            # Open and transcribe
            with open(temp_audio_path, "rb") as audio:
                transcription = self.client.audio.transcriptions.create(
                    file=(filename, audio.read()),
                    model="whisper-large-v3-turbo",
                    language=language,
                    prompt=prompt,
                    temperature=temperature,
                    response_format="verbose_json"  # Get detailed response with metadata
                )

            # Clean up temp file
            os.unlink(temp_audio_path)

            # Extract results
            result = {
                "text": transcription.text,
                "language": getattr(transcription, 'language', language),
                "duration": getattr(transcription, 'duration', None),
            }

            return result

        except Exception as e:
            # Clean up temp file if it exists
            if 'temp_audio_path' in locals():
                try:
                    os.unlink(temp_audio_path)
                except:
                    pass
            raise Exception(f"Transcription failed: {str(e)}")

    async def transcribe_with_translation(
        self,
        audio_file: bytes,
        filename: str,
        target_language: str = "eng",
        detect_language: bool = True
    ) -> Dict:
        """
        Transcribe audio and optionally translate to target language.

        Args:
            audio_file: Audio file bytes
            filename: Original filename
            target_language: Target language for translation
            detect_language: Whether to detect the source language

        Returns:
            Dict with transcription, detected language, and optional translation
        """
        # First transcribe
        transcription = await self.transcribe_audio(
            audio_file=audio_file,
            filename=filename
        )

        result = {
            "transcribed_text": transcription["text"],
            "detected_language": transcription.get("language"),
            "duration": transcription.get("duration")
        }

        return result


# Singleton pattern
_voice_service_instance = None

def get_voice_service() -> VoiceService:
    """Get or create the voice service singleton instance"""
    global _voice_service_instance
    if _voice_service_instance is None:
        _voice_service_instance = VoiceService()
    return _voice_service_instance
