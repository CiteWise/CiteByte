"""
Survey generation module.
Orchestrates the RAG pipeline to generate structured literature survey.
"""

from typing import List
from sqlalchemy.orm import Session
from models import Paper, SurveySection, SurveyResponse, TextChunk
from evidence_store import EvidenceStore
from llm_engine import MockLLMEngine
from config import settings


class SurveyGenerator:
    """Generate citation-grounded literature survey using RAG pattern."""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.evidence_store = EvidenceStore(db_session)
        self.llm = MockLLMEngine()
    
    def generate_survey(self, topic: str, papers: List[Paper]) -> List[SurveySection]:
        """
        Generate structured survey sections.
        
        Args:
            topic: Research topic
            papers: List of papers to use
            
        Returns:
            List of SurveySection objects with inline citations
        """
        # Define survey structure
        section_titles = [
            "Introduction",
            "Methodologies Used",
            "Key Findings and Results",
            "Research Gaps and Future Directions"
        ]
        
        sections = []
        
        for section_title in section_titles:
            # Retrieve relevant chunks for this section
            section_query = self._create_section_query(topic, section_title)
            relevant_chunks = self.evidence_store.retrieve_relevant_chunks(
                query=section_query,
                top_k=15
            )
            
            # Generate section content using LLM
            content = self.llm.generate_section(
                section_title=section_title,
                chunks=relevant_chunks,
                topic=topic
            )
            
            # Create section object
            section = SurveySection(
                title=section_title,
                content=content
            )
            sections.append(section)
        
        return sections
    
    def _create_section_query(self, topic: str, section_title: str) -> str:
        """Create search query for section-specific chunks."""
        # Enhance query with section-specific keywords
        section_keywords = {
            "Introduction": f"{topic} overview background motivation",
            "Methodologies Used": f"{topic} method approach technique algorithm implementation",
            "Key Findings and Results": f"{topic} results performance evaluation experiments accuracy",
            "Research Gaps and Future Directions": f"{topic} limitations challenges future work directions"
        }
        
        return section_keywords.get(section_title, topic)
