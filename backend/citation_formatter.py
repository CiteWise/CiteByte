"""
Citation formatting module.
Converts [PaperID] tags to IEEE-style numbered citations.
"""

from typing import List, Dict, Tuple
import re
from models import Paper, Citation, SurveySection


class CitationFormatter:
    """Format citations in IEEE style with traceability."""
    
    def __init__(self):
        self.citation_map = {}  # PaperID -> Citation number
        self.citations = []  # List of Citation objects
    
    def process_survey(self, sections: List[SurveySection], papers: List[Paper]) -> Tuple[List[SurveySection], List[Citation]]:
        """
        Process survey to convert [PaperID] to [1], [2], etc.
        Generate IEEE reference list.
        
        Args:
            sections: Survey sections with inline [PaperID] citations
            papers: All papers used in the survey
            
        Returns:
            Tuple of (processed_sections, citations_list)
        """
        # Build paper lookup
        paper_dict = {p.paper_id: p for p in papers}
        
        # Extract all paper IDs from sections
        cited_paper_ids = self._extract_cited_papers(sections)
        
        # Create citation mapping (order by first appearance or alphabetically)
        self._create_citation_mapping(cited_paper_ids, paper_dict)
        
        # Replace [PaperID] with [1], [2], etc. in sections
        processed_sections = self._replace_citations_in_sections(sections)
        
        return processed_sections, self.citations
    
    def _extract_cited_papers(self, sections: List[SurveySection]) -> List[str]:
        """Extract all cited paper IDs from sections."""
        cited_ids = []
        pattern = r'\[([^\]]+)\]'
        
        for section in sections:
            matches = re.findall(pattern, section.content)
            for match in matches:
                # Filter out non-paper-ID citations (e.g., numbers)
                if match.startswith('mock_'):
                    cited_ids.append(match)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_ids = []
        for pid in cited_ids:
            if pid not in seen:
                seen.add(pid)
                unique_ids.append(pid)
        
        return unique_ids
    
    def _create_citation_mapping(self, paper_ids: List[str], paper_dict: Dict[str, Paper]) -> None:
        """Create mapping from PaperID to citation number."""
        for idx, paper_id in enumerate(paper_ids):
            citation_num = idx + 1
            self.citation_map[paper_id] = citation_num
            
            # Get paper
            paper = paper_dict.get(paper_id)
            if not paper:
                continue
            
            # Create IEEE-style reference
            ieee_reference = self._format_ieee_reference(citation_num, paper)
            
            # Create Citation object
            citation = Citation(
                number=citation_num,
                paper_id=paper_id,
                formatted_reference=ieee_reference
            )
            self.citations.append(citation)
    
    def _format_ieee_reference(self, number: int, paper: Paper) -> str:
        """
        Format paper in IEEE style.
        IEEE format: [1] A. Author, "Title," Venue, Year.
        """
        # Extract author names
        author_names = []
        for author in paper.authors:
            # IEEE format: First Initial. Last Name
            name_parts = author.name.split()
            if len(name_parts) >= 2:
                formatted_name = f"{name_parts[0][0]}. {' '.join(name_parts[1:])}"
            else:
                formatted_name = author.name
            author_names.append(formatted_name)
        
        # Format authors (max 3, then "et al.")
        if len(author_names) > 3:
            authors_str = f"{', '.join(author_names[:3])}, et al."
        else:
            authors_str = ', '.join(author_names)
        
        # Build IEEE reference
        reference = f'[{number}] {authors_str}, "{paper.title}," '
        
        if paper.venue:
            reference += f"{paper.venue}, "
        
        reference += f"{paper.year}."
        
        # Add DOI if available
        if paper.doi:
            reference += f" DOI: {paper.doi}"
        
        return reference
    
    def _replace_citations_in_sections(self, sections: List[SurveySection]) -> List[SurveySection]:
        """Replace [PaperID] with [number] in all sections."""
        processed_sections = []
        
        for section in sections:
            processed_content = section.content
            
            # Replace each [PaperID] with [number]
            for paper_id, citation_num in self.citation_map.items():
                # Use word boundary to avoid partial matches
                pattern = r'\[' + re.escape(paper_id) + r'\]'
                replacement = f'[{citation_num}]'
                processed_content = re.sub(pattern, replacement, processed_content)
            
            processed_section = SurveySection(
                title=section.title,
                content=processed_content
            )
            processed_sections.append(processed_section)
        
        return processed_sections
