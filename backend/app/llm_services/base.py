from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseLLM(ABC):
    @abstractmethod
    async def generate_response(self, query: str, context: str) -> str:
        """Generate response from LLM"""
        pass

    @abstractmethod
    async def is_available(self) -> bool:
        """Check if LLM service is available"""
        pass