from abc import ABC, abstractmethod
from ..models.search import SearchResult
from typing import List

class SearchEngine(ABC):
    @abstractmethod
    async def search(self, query: str, max_results: int = 10) -> List[SearchResult]:
        """
        Execute search and return results
        """
        pass

    @abstractmethod
    async def extract_content(self, url: str) -> str:
        """
        Extract main content from a webpage
        """
        pass