from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
import logging
from .config import settings
from .search_service.search_manager import SearchManager
from .search_service.models.search import SearchResponse
from .llm_services.llm_manager import LLMManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Search API",
    description="Custom search engine with multiple LLM integration",
    version="1.0.0",
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize managers
search_manager = SearchManager()
llm_manager = LLMManager()

class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 10

@app.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    try:
        logger.info(f"Received search request: {request.query}")
        
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="Query parameter cannot be empty")
        
        # Perform search
        search_response = await search_manager.perform_search(
            query=request.query,
            max_results=request.max_results
        )

        # Get context from search results
        context = "\n".join([
            f"Title: {result.title}\nDescription: {result.description}\nContent: {result.content}\n"
            for result in search_response.results[:3]  # Use top 3 results for context
        ])

        # Get LLM responses
        logger.info("Getting LLM responses")
        try:
            llm_responses = await llm_manager.get_responses(request.query, context)
            search_response.llm_responses = llm_responses
        except Exception as llm_error:
            logger.error(f"LLM processing error: {str(llm_error)}")
            search_response.llm_responses = {
                "gemini": "Error generating response",
                "groq": "Error generating response"
            }
        
        logger.info(f"Search completed successfully for query: {request.query}")
        return search_response
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during search: {str(e)}"
        )

@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/api/llm-status")
async def llm_status():
    try:
        status = await llm_manager.check_availability()
        return status
    except Exception as e:
        logger.error(f"LLM status check error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error checking LLM status: {str(e)}"
        )

# Error handler for all exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global error handler caught: {str(exc)}", exc_info=True)
    return {
        "status_code": 500,
        "detail": f"Internal server error: {str(exc)}"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )