"""
LLM Service using LangChain with Groq
"""
import os
from typing import List, Dict, Optional
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


class LLMService:

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self._llm = None

    @property
    def llm(self):
        """Lazy load the LLM client"""
        if self._llm is None:
            if not self.api_key:
                raise ValueError("GROQ_API_KEY not found in environment variables")
            self._llm = ChatGroq(
                api_key=self.api_key,
                model_name="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1024,
            )
        return self._llm
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:

        langchain_messages = []
        
        if system_prompt:
            langchain_messages.append(SystemMessage(content=system_prompt))
        
        for msg in messages:
            role = msg.get("role")
            content = msg.get("content", "")
            
            if role == "user":
                langchain_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))
            elif role == "system":
                langchain_messages.append(SystemMessage(content=content))
        
        # Create LLM with optional overrides
        llm = self.llm
        if temperature is not None or max_tokens is not None:
            llm = ChatGroq(
                api_key=self.api_key,
                model_name="llama-3.3-70b-versatile",
                temperature=temperature if temperature is not None else 0.7,
                max_tokens=max_tokens if max_tokens is not None else 1024,
            )

        # Generate response
        response = await llm.ainvoke(langchain_messages)
        return response.content


# Singleton pattern with lazy loading
_llm_service_instance = None

def get_llm_service() -> LLMService:
    """Get or create the LLM service singleton instance"""
    global _llm_service_instance
    if _llm_service_instance is None:
        _llm_service_instance = LLMService()
    return _llm_service_instance
