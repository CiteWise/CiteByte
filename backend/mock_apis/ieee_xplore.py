"""
Mock IEEE Xplore API client.
Provides secondary validation and metadata enrichment.
"""

from typing import Optional
from models import Paper


class MockIEEEXploreAPI:
    """Mock implementation of IEEE Xplore API."""
    
    def __init__(self, api_key: str = "mock_key"):
        self.api_key = api_key
    
    def validate_paper(self, doi: str) -> Optional[dict]:
        """
        Mock validation of paper metadata.
        In real implementation, would verify DOI and enrich metadata.
        """
        # For mock, always return success
        return {
            "validated": True,
            "source": "IEEE Xplore",
            "metadata_complete": True
        }
    
    def get_paper_metadata(self, paper_id: str) -> Optional[dict]:
        """
        Mock metadata retrieval.
        Returns placeholder enriched data.
        """
        return {
            "keywords": ["machine learning", "deep learning", "neural networks"],
            "ieee_terms": ["Artificial Intelligence", "Computer Science"],
            "pdf_available": False  # Mock mode doesn't provide PDFs
        }
