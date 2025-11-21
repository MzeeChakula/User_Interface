import os
import httpx
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

class SunbirdService:
    """
    Service for interacting with Sunbird AI API for translation.
    """
    
    def __init__(self):
        self.api_key = os.getenv("SUNBIRD_API_KEY")
        self.base_url = "https://api.sunbird.ai/v1" # Verify exact URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
    async def translate(self, text: str, source_lang: str, target_lang: str) -> Dict[str, Any]:
        """
        Translate text using Sunbird AI.
        
        Args:
            text: Text to translate
            source_lang: Source language code (e.g., 'en', 'lg')
            target_lang: Target language code (e.g., 'lg', 'en')
            
        Returns:
            Dictionary containing translation result
        """
        if not self.api_key:
            logger.warning("SUNBIRD_API_KEY not set. Returning mock translation.")
            return {
                "text": f"[MOCK TRANSLATION to {target_lang}]: {text}",
                "source_language": source_lang,
                "target_language": target_lang
            }

        async with httpx.AsyncClient() as client:
            try:
                payload = {
                    "text": text,
                    "source_language": source_lang,
                    "target_language": target_lang
                }
                
                response = await client.post(
                    f"{self.base_url}/tasks/translate", # Endpoint might vary
                    json=payload,
                    headers=self.headers,
                    timeout=30.0
                )
                
                response.raise_for_status()
                return response.json()
                
            except httpx.HTTPStatusError as e:
                logger.error(f"Sunbird AI API error: {e.response.text}")
                raise Exception(f"Translation failed: {e.response.text}")
            except Exception as e:
                logger.error(f"Translation service error: {str(e)}")
                raise

# Singleton instance
sunbird_service = SunbirdService()
