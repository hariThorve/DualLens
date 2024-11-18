from .base import BaseLLM
import google.generativeai as genai
from ..config import settings
import logging

class GeminiLLM(BaseLLM):
    def __init__(self):
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            logging.error(f"Failed to initialize Gemini: {str(e)}")
            raise

    async def generate_response(self, query: str, context: str) -> str:
        try:
            prompt = self._create_prompt(query, context)
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            logging.error(f"Gemini generation error: {str(e)}")
            return "Error generating response from Gemini."

    async def is_available(self) -> bool:
        try:
            response = await self.model.generate_content_async("Test connection")
            return True
        except:
            return False

    def _create_prompt(self, query: str, context: str) -> str:
        return f"""Based on the following context, answer the query: {query}

Context:
{context}

Please provide a comprehensive answer that:
1. Directly addresses the query
2. Uses information from the provided context
3. Cites sources when appropriate
4. Is concise and to the point
5. Keep it short and concise, don't use markdown formatting
"""