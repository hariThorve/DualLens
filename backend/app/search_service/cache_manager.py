from datetime import datetime, timedelta
from typing import Dict, Optional
import json
from .models.search import SearchResponse

class CacheManager:
    def __init__(self, cache_duration_minutes: int = 30):
        self._cache: Dict[str, Dict] = {}
        self._cache_duration = timedelta(minutes=cache_duration_minutes)

    def get(self, query: str) -> Optional[SearchResponse]:
        """Get cached response if it exists and is not expired"""
        if query in self._cache:
            cached_data = self._cache[query]
            cached_time = datetime.fromisoformat(cached_data['timestamp'])
            
            if datetime.now() - cached_time < self._cache_duration:
                return SearchResponse(**cached_data['response'])
                
            # Remove expired cache entry
            del self._cache[query]
        return None

    def set(self, query: str, response: SearchResponse):
        """Cache the search response"""
        self._cache[query] = {
            'timestamp': datetime.now().isoformat(),
            'response': response.model_dump()
        }

    def clear(self):
        """Clear all cached results"""
        self._cache.clear()