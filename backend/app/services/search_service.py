from tavily import TavilyClient
from app.core.config import settings
from typing import List, Dict

class SearchService:
    def __init__(self):
        self.api_key = settings.TAVILY_API_KEY
        if self.api_key:
            self.client = TavilyClient(api_key=self.api_key)
        else:
            self.client = None
            print("Search Service: Disabled (Missing TAVILY_API_KEY)")
    
    async def perform_research(self, query: str, max_results: int = 5) -> Dict:
        print(f"[DEBUG] SearchService.perform_research called with query: {query}")
        """
        Perform web research using Tavily API.
        
        Args:
            query: Search query
            max_results: Maximum number of results to return
        
        Returns:
            Dictionary containing search results and summary
        """
        if not self.client:
             return {
                 "query": query,
                 "answer": "Research functionality is currently disabled.",
                 "sources": [],
                 "summary": "Please configure the TAVILY_API_KEY in your backend .env file to enable live web research."
             }

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
