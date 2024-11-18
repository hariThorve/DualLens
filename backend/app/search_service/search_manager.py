from .engines.duckduckgo import DuckDuckGoEngine
from .models.search import SearchResponse, SearchResult
import time
import asyncio
import logging

logger = logging.getLogger(__name__)

class SearchManager:
    def __init__(self):
        self.engine = DuckDuckGoEngine()
    
    async def perform_search(self, query: str, max_results: int = 10) -> SearchResponse:
        try:
            start_time = time.time()
            
            # Get initial search results
            logger.info(f"Fetching search results for query: {query}")
            results = await self.engine.search(query, max_results)
            
            if not results:
                logger.warning(f"No results found for query: {query}")
                return SearchResponse(
                    query=query,
                    results=[],
                    total_results=0,
                    search_time=time.time() - start_time,
                    llm_responses=None  # Initialize as None
                )
            
            # Extract content for each result in parallel
            logger.info("Extracting content from search results")
            content_tasks = [
                self.engine.extract_content(result.url)
                for result in results
            ]
            
            contents = await asyncio.gather(*content_tasks, return_exceptions=True)
            
            # Update results with content
            processed_results = []
            for result, content in zip(results, contents):
                if isinstance(content, Exception):
                    logger.error(f"Content extraction failed for {result.url}: {str(content)}")
                    content = None
                result.content = content
                processed_results.append(result)
            
            search_time = time.time() - start_time
            
            logger.info(f"Search completed in {search_time:.2f} seconds")
            return SearchResponse(
                query=query,
                results=processed_results,
                total_results=len(processed_results),
                search_time=search_time,
                llm_responses=None  # Initialize as None
            )
            
        except Exception as e:
            logger.error(f"Search manager error: {str(e)}", exc_info=True)
            raise Exception(f"Search failed: {str(e)}")