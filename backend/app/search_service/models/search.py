from pydantic import BaseModel
from typing import List, Optional, Dict

class SearchResult(BaseModel):
    title: str
    url: str
    description: Optional[str] = None
    content: Optional[str] = None
    timestamp: Optional[str] = None

class LLMResponse(BaseModel):
    gemini: str
    groq: str

class SearchResponse(BaseModel):
    query: str
    results: List[SearchResult]
    total_results: int
    search_time: float
    llm_responses: Optional[Dict[str, str]] = None  # Add this field