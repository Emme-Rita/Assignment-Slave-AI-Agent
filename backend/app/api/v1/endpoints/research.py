from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.search_service import search_service

router = APIRouter()

class ResearchRequest(BaseModel):
    query: str
    max_results: int = 5

@router.post("/research")
async def perform_research(request: ResearchRequest):
    """
    Perform web research on a topic.
    
    Args:
        request: Research request with query and max_results
    
    Returns:
        Research results with sources and summary
    """
    try:
        results = await search_service.perform_research(
            query=request.query,
            max_results=request.max_results
        )
        
        return {
            "success": True,
            "data": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/research/{query}")
async def quick_research(query: str, max_results: int = 5):
    """
    Quick research endpoint using GET request.
    
    Args:
        query: Search query
        max_results: Maximum number of results
    
    Returns:
        Research results
    """
    try:
        results = await search_service.perform_research(
            query=query,
            max_results=max_results
        )
        
        return {
            "success": True,
            "data": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
