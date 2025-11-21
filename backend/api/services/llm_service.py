import os
import openai
import logging
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class LLMService:
    """
    Service for interacting with LLM (Groq via OpenAI SDK).
    """
    
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.base_url = "https://api.groq.com/openai/v1"
        self.model = "llama3-70b-8192"
        self.client = None
        
        if self.api_key:
            try:
                self.client = openai.OpenAI(
                    base_url=self.base_url,
                    api_key=self.api_key
                )
                logger.info(f"Connected to Groq LLM ({self.model})")
            except Exception as e:
                logger.error(f"Failed to initialize LLM client: {e}")
        else:
            logger.warning("GROQ_API_KEY not set. LLM features disabled.")

    def get_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 1024
    ) -> str:
        """
        Get completion from LLM.
        """
        if not self.client:
            return "LLM service is not available."

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=1,
                stream=False,
                stop=None,
            )
            return completion.choices[0].message.content
        except Exception as e:
            logger.error(f"LLM completion failed: {e}")
            raise

# Singleton instance
llm_service = LLMService()
