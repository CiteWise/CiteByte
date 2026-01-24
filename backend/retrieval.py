"""
Paper retrieval module.
Orchestrates multiple API sources and deduplicates results.
"""

from typing import List
from models import Paper
from mock_apis.semantic_scholar import MockSemanticScholarAPI
from mock_apis.ieee_xplore import MockIEEEXploreAPI
from config import settings


class PaperRetriever:
    """Retrieve papers from multiple academic sources."""
    
    def __init__(self):
        self.semantic_scholar = MockSemanticScholarAPI(settings.semantic_scholar_api_key)
        self.ieee = MockIEEEXploreAPI(settings.ieee_api_key)
    
    def retrieve_papers(self, topic: str, max_results: int = 50) -> List[Paper]:
        """
        Retrieve papers for a given research topic.
        
        Args:
            topic: Research topic query
            max_results: Maximum number of papers to retrieve
            
        Returns:
            List of Paper objects, deduplicated
        """
        # In mock mode, primarily use Semantic Scholar
        papers = self.semantic_scholar.search_papers(topic, max_results)
        
        # Validate engineering domain
        papers = self._filter_engineering_domain(papers)
        
        # Deduplicate by DOI and title
        papers = self._deduplicate(papers)
        
        return papers[:max_results]
    
    def _filter_engineering_domain(self, papers: List[Paper]) -> List[Paper]:
        """
        Filter to ensure papers are in engineering domain.
        For mock mode, this is lenient. Real implementation would check venues/keywords.
        """
        # In production, would check:
        # - Venue (IEEE, ACM, SpringerLink, etc.)
        # - Keywords (CS, AI, ML, Engineering terms)
        # - Author affiliations
        
        # Mock: accept all papers (already curated in mock data)
        return papers
    
    def _deduplicate(self, papers: List[Paper]) -> List[Paper]:
        """Remove duplicate papers based on DOI or title similarity."""
        seen_dois = set()
        seen_titles = set()
        unique_papers = []
        
        for paper in papers:
            # Check DOI
            if paper.doi and paper.doi in seen_dois:
                continue
            
            # Check title (normalized)
            title_normalized = paper.title.lower().strip()
            if title_normalized in seen_titles:
                continue
            
            # Add to unique set
            if paper.doi:
                seen_dois.add(paper.doi)
            seen_titles.add(title_normalized)
            unique_papers.append(paper)
        
        return unique_papers
