"""
Sunbird AI Service for translation and language detection.
Supports 200+ African languages via Sunflower model.
"""
import os
import httpx
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

class SunbirdService:

    # Ugandan languages supported by Sunbird AI
    UGANDAN_LANGUAGES = {
        "eng": "English",
        "lug": "Luganda",
        "nyn": "Runyankole",
        "ach": "Acholi",
        "teo": "Ateso",
        "lgg": "Lugbara"
    }
    
    LANGUAGE_CODES = {
        # Ugandan Languages (Primary)
        "English": "eng",
        "Luganda": "lug",
        "Runyankole": "nyn",
        "Acholi": "ach",
        "Ateso": "teo",
        "Lugbara": "lgg",
        
        # East African Languages
        "Swahili": "swh",
        "Kinyarwanda": "kin",
        "Kikuyu": "kik",
        "Luo": "luo",
        "Gikuyu": "kik",
        "Kamba": "kam",
        "Somali": "som",
        
        # West African Languages
        "Yoruba": "yor",
        "Igbo": "ibo",
        "Hausa": "hau",
        "Fon": "fon",
        "Twi": "twi",
        "Akan": "aka",
        "Ewe": "ewe",
        "Wolof": "wol",
        "Bambara": "bam",
        "Fulfulde": "fuv",
        
        # Southern African Languages
        "Zulu": "zul",
        "Xhosa": "xho",
        "Shona": "sna",
        "Sesotho": "sot",
        "Setswana": "tsn",
        "Chichewa": "nya",
        "Lingala": "lin",
        
        # North African Languages
        "Arabic": "ara",
        "Amharic": "amh",
        "Tigrinya": "tir",
        "Oromo": "orm",
        
        # Central African Languages
        "Kirundi": "run",
        "Kongo": "kon",
        "Luba": "lub",
        "Swati": "ssw",
        
        # Other Major Languages
        "French": "fra",
        "Portuguese": "por",
        "Afrikaans": "afr",
    }
    
    def __init__(self):
        self.api_key = os.getenv("SUNBIRD_API_KEY")
        self.base_url = "https://api.sunbird.ai"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of the given text.
        
        Args:
            text: Text to detect language for
            
        Returns:
            Dictionary with detected language info
        """
        if not self.api_key:
            logger.warning("SUNBIRD_API_KEY not set. Returning mock detection.")
            return {
                "language": "eng",
                "language_name": "English",
                "confidence": 0.95
            }
        
        async with httpx.AsyncClient() as client:
            try:
                payload = {"text": text}
                
                response = await client.post(
                    f"{self.base_url}/tasks/language_id",
                    json=payload,
                    headers=self.headers,
                    timeout=30.0
                )
                
                response.raise_for_status()
                result = response.json()
                
                # Parse response and add language name
                detected_code = result.get("language", "eng")
                return {
                    "language": detected_code,
                    "language_name": self.UGANDAN_LANGUAGES.get(detected_code, "Unknown"),
                    "confidence": result.get("confidence", 0.0)
                }
                
            except httpx.HTTPStatusError as e:
                logger.error(f"Sunbird AI language detection error: {e.response.text}")
                # Fallback to English
                return {"language": "eng", "language_name": "English", "confidence": 0.0}
            except Exception as e:
                logger.error(f"Language detection error: {str(e)}")
                return {"language": "eng", "language_name": "English", "confidence": 0.0}
    
    async def translate(
        self, 
        text: str, 
        source_lang: Optional[str] = None, 
        target_lang: str = "eng"
    ) -> Dict[str, Any]:
 
        if not self.api_key:
            logger.warning("SUNBIRD_API_KEY not set. Returning mock translation.")
            return {
                "translated_text": f"[MOCK TRANSLATION to {target_lang}]: {text}",
                "source_language": source_lang or "auto",
                "target_language": target_lang
            }
        
        # Auto-detect source language if not provided
        if not source_lang:
            detection = await self.detect_language(text)
            source_lang = detection["language"]
            logger.info(f"Auto-detected language: {detection['language_name']} ({source_lang})")
        
        async with httpx.AsyncClient() as client:
            try:
                payload = {
                    "source_language": source_lang,
                    "target_language": target_lang,
                    "text": text
                }
                
                response = await client.post(
                    f"{self.base_url}/tasks/nllb_translate",
                    json=payload,
                    headers=self.headers,
                    timeout=30.0
                )
                
                response.raise_for_status()
                result = response.json()

                # Parse response - Sunbird can return {"output": "..."} or {"text": "..."}
                translated = result.get("output") or result.get("text") or text

                return {
                    "translated_text": translated,
                    "source_language": source_lang,
                    "target_language": target_lang,
                    "source_language_name": self.UGANDAN_LANGUAGES.get(source_lang, "Unknown"),
                    "target_language_name": self.UGANDAN_LANGUAGES.get(target_lang, "Unknown")
                }
                
            except httpx.HTTPStatusError as e:
                logger.error(f"Sunbird AI translation error: {e.response.text}")
                raise Exception(f"Translation failed: {e.response.text}")
            except Exception as e:
                logger.error(f"Translation service error: {str(e)}")
                raise
    
    async def get_supported_languages(self) -> List[Dict[str, str]]:
     
        return [
            {"code": code, "name": name}
            for code, name in self.UGANDAN_LANGUAGES.items()
        ]

# Singleton instance
sunbird_service = SunbirdService()
