"""
Data models for Literature Survey System.
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime


class Author(BaseModel):
    """Author information."""
    name: str
    affiliation: Optional[str] = None


class Paper(BaseModel):
    """Research paper metadata."""
    paper_id: str = Field(..., description="Unique identifier for the paper")
    title: str
    authors: List[Author]
    year: int
    abstract: str
    doi: Optional[str] = None
    venue: Optional[str] = None  # Conference or journal name
    citation_count: Optional[int] = 0
    url: Optional[str] = None
    

class TextChunk(BaseModel):
    """Structured text chunk for evidence storage."""
    chunk_id: str
    paper_id: str
    paper_title: str
    year: int
    section_name: str = Field(..., description="e.g., 'Abstract', 'Methodology', 'Results'")
    text: str
    

class RankedPaper(BaseModel):
    """Paper with ranking score."""
    paper: Paper
    bm25_score: float
    rank: int
    used_for_full_text: bool = Field(default=False, description="Whether full sections extracted")


class SurveyRequest(BaseModel):
    """Request to generate literature survey."""
    topic: str = Field(..., description="Research topic in engineering domain")
    domain: Optional[str] = Field(default="Computer Science", description="Engineering subdomain")
    max_papers: Optional[int] = 50
    

class SurveySection(BaseModel):
    """Individual section of the survey."""
    title: str
    content: str  # Contains inline [PaperID] citations
    

class Citation(BaseModel):
    """IEEE-style citation."""
    number: int  # Citation number [1], [2], etc.
    paper_id: str
    formatted_reference: str  # IEEE format: [1] Authors, "Title," Venue, Year.
    

class SurveyResponse(BaseModel):
    """Generated literature survey with citations."""
    topic: str
    sections: List[SurveySection]
    references: List[Citation]
    papers_used: List[Paper]
    generated_at: datetime = Field(default_factory=datetime.now)
    

class PaperSearchResponse(BaseModel):
    """Response from paper search endpoint."""
    topic: str
    papers_found: int
    ranked_papers: List[RankedPaper]
