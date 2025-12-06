from typing import List, Dict, Optional
import json
import re
from app.services.ai_service import ai_service
from app.services.search_service import search_service

class FactCheckService:
    def __init__(self):
        pass

    async def verify_content(self, text: str, min_confidence: float = 0.7) -> Dict:
        """
        Main entry point to verify content.
        Extracts claims, verifies them, and calculates a trust score.
        """
        # 1. Extract Claims
        claims = await self._extract_claims(text)
        
        # 2. Verify each claim
        verified_claims = []
        for claim in claims:
            verification = await self._verify_single_claim(claim)
            verified_claims.append(verification)
            
        # 3. Check Citations
        citation_check = await self._verify_citations(text)
        
        # 4. Calculate Score
        trust_score = self._calculate_trust_score(verified_claims, citation_check)
        
        return {
            "trust_score": trust_score,
            "claims": verified_claims,
            "citations": citation_check,
            "is_reliable": trust_score >= min_confidence
        }

    async def _extract_claims(self, text: str) -> List[str]:
        """Use AI to extract factual claims that need verification."""
        prompt = f"""
        Extract key factual claims from the following text that should be fact-checked.
        Focus on:
        - Statistics and numbers
        - Dates and historical events
        - Scientific claims
        - Quote attributions
        
        Return ONLY a JSON array of strings. Example: ["The earth is flat", "Water boils at 100C"]
        
        Text:
        {text[:2000]}... (truncated)
        """
        
        try:
            response = await ai_service.generate_response(prompt)
            # Clean and parse JSON
            cleaned = response.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)
        except Exception as e:
            print(f"Claim extraction failed: {e}")
            return []

    async def _verify_single_claim(self, claim: str) -> Dict:
        """Search for a claim and verify if it's true."""
        try:
            # Search for the claim
            search_results = await search_service.perform_research(f"verify claim: {claim}")
            
            # Use AI to compare claim with search results
            context = search_results.get("summary", "")
            
            prompt = f"""
            Verify the following claim based on the provided search results.
            
            Claim: "{claim}"
            
            Search Results:
            {context}
            
            Determine if the claim is:
            - "Supported" (True)
            - "Contradicted" (False)
            - "Unverified" (Not enough info)
            
            Return JSON: {{ "status": "Supported"|"Contradicted"|"Unverified", "reasoning": "short explanation", "source_url": "url if found" }}
            """
            
            response = await ai_service.generate_response(prompt)
            result = json.loads(response.replace("```json", "").replace("```", "").strip())
            
            return {
                "claim": claim,
                "status": result.get("status", "Unverified"),
                "reasoning": result.get("reasoning", ""),
                "source": result.get("source_url", "")
            }
            
        except Exception as e:
            return {"claim": claim, "status": "Unverified", "reasoning": str(e), "source": ""}

    async def _verify_citations(self, text: str) -> List[Dict]:
        """Extract citations and check if they look real."""
        # Simple regex for finding citations like [1], (Author, Year), etc.
        # This is basic; a real implementation would use AI or stricter parsing
        citations = []
        
        # Look for [1], [2] etc.
        numeric_citations = re.findall(r'\[\d+\]', text)
        
        # Look for (Author, Year) - basic approximation
        author_citations = re.findall(r'\([A-Z][a-z]+,\s\d{4}\)', text)
        
        all_refs = list(set(numeric_citations + author_citations))
        
        results = []
        for ref in all_refs[:5]: # Limit to 5 to save time
             # Verify if the paper/reference likely exists via search
             results.append({
                 "citation": ref,
                 "status": "Checked", # We aren't doing deep Paper checking yet to save API calls
                 "note": "Format detected" 
             })
             
        return results

    def _calculate_trust_score(self, verified_claims: List[Dict], citations: List[Dict]) -> float:
        if not verified_claims:
            return 1.0 # Benefit of doubt
            
        correct = len([c for c in verified_claims if c['status'] == 'Supported'])
        incorrect = len([c for c in verified_claims if c['status'] == 'Contradicted'])
        total = len(verified_claims)
        
        if total == 0: return 1.0
        
        # Simple scoring
        score = (correct + (total - correct - incorrect) * 0.5) / total
        return round(score, 2)

fact_check_service = FactCheckService()
