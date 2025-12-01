from tavily import TavilyClient
from app.core.config import settings
from typing import List, Dict

class SearchService:
    def __init__(self):
        self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)
    
    async def perform_research(self, query: str, max_results: int = 5) -> Dict:
        """
        Perform web research using Tavily API.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
        
        Returns:
            Dictionary containing search results and summary
        """
        try:
            # Perform search
            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced"
            )
            
            # Extract relevant information
            results = {
                "query": query,
                "answer": response.get("answer", ""),
                "sources": [
                    {
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "content": result.get("content", ""),
                        "score": result.get("score", 0)
                    }
                    for result in response.get("results", [])
                ],
                "summary": self._create_summary(response)
            }
            
            return results
        
        except Exception as e:
            raise Exception(f"Search Service Error: {str(e)}")
    
    def _create_summary(self, response: Dict) -> str:
        """Create a text summary from search results."""
        summary_parts = []
        
        if response.get("answer"):
            summary_parts.append(f"Answer: {response['answer']}\n")
        
        if response.get("results"):
            summary_parts.append("Key Findings:")
            for i, result in enumerate(response["results"][:3], 1):
                summary_parts.append(f"{i}. {result.get('title', 'N/A')}")
                summary_parts.append(f"   {result.get('content', '')[:200]}...")
        
        return "\n".join(summary_parts)

search_service = SearchService()
