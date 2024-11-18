from .gemini_llm import GeminiLLM
from .groq_llm import GroqLLM
from typing import Dict
import asyncio
import logging

class LLMManager:
    def __init__(self):
        self.gemini = GeminiLLM()
        self.groq = GroqLLM()

    async def get_responses(self, query: str, context: str) -> Dict[str, str]:
        """Get responses from all available LLMs"""
        try:
            # Run LLMs in parallel
            responses = await asyncio.gather(
                self.gemini.generate_response(query, context),
                self.groq.generate_response(query, context),
                return_exceptions=True
            )

            return {
                "gemini": responses[0] if not isinstance(responses[0], Exception) else "Error generating Gemini response",
                "groq": responses[1] if not isinstance(responses[1], Exception) else "Error generating Groq response"
            }
        except Exception as e:
            logging.error(f"Error in LLM Manager: {str(e)}")
            return {
                "gemini": "Failed to generate response",
                "groq": "Failed to generate response"
            }

    async def check_availability(self) -> Dict[str, bool]:
        """Check which LLMs are available"""
        gemini_available = await self.gemini.is_available()
        groq_available = await self.groq.is_available()
        
        return {
            "gemini": gemini_available,
            "groq": groq_available
        }