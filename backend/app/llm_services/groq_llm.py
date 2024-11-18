from .base import BaseLLM
from groq import AsyncGroq
from ..config import settings
import logging

class GroqLLM(BaseLLM):
    def __init__(self):
        try:
            self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
            self.model = "mixtral-8x7b-32768"
        except Exception as e:
            logging.error(f"Failed to initialize Groq: {str(e)}")
            raise

    async def generate_response(self, query: str, context: str) -> str:
        try:
            prompt = self._create_prompt(query, context)
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that provides comprehensive answers based on given sources."},
                    {"role": "user", "content": prompt}
                ]
            )
            return completion.choices[0].message.content
        except Exception as e:
            logging.error(f"Groq generation error: {str(e)}")
            return "Error generating response from Groq."

    async def is_available(self) -> bool:
        try:
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Test connection"}]
            )
            return True
        except:
            return False

    def _create_prompt(self, query: str, context: str) -> str:
        return f"""Based on the following context, answer the query: {query}

Context:
{context}

Requirements:

1. Use information only from the provided context
2. Include relevant citations
3. Structure the response clearly
4. Is concise and to the point
5. Keep it short and concise, don't use markdown formatting
6. Give detailed answers whenever asked, for example, if asked for expalining a concept, give a detailed explanation
"""
