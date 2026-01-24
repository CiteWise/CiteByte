"""
Mock CrossRef API client.
Provides DOI resolution and citation formatting.
"""

from typing import Optional


class MockCrossRefAPI:
    """Mock implementation of CrossRef API."""
    
    def __init__(self, api_key: str = "mock_key"):
        self.api_key = api_key
    
    def resolve_doi(self, doi: str) -> Optional[dict]:
        """Mock DOI resolution."""
        # Mock successful resolution
        return {
            "doi": doi,
            "type": "journal-article",
            "publisher": "IEEE",
            "valid": True
        }
    
    def format_citation(self, doi: str, style: str = "ieee") -> str:
        """
        Mock citation formatting.
        In real implementation, would use CrossRef's formatting service.
        """
        # Placeholder IEEE citation
        return f"[DOI: {doi}] - IEEE Style Citation (Mock)"
