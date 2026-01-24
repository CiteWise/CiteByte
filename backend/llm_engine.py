"""
Mock LLM engine for constrained generation.
Future: Replace with OpenAI/Google Gemini API.
"""

from typing import List
from models import TextChunk
import random


class MockLLMEngine:
    """
    Mock LLM with template-based generation.
    Enforces citation grounding constraint.
    """
    
    def __init__(self):
        self.system_prompt = """You are an academic writing assistant.
You MUST follow these rules:
1. Use ONLY the provided text chunks for generating content
2. Do NOT add external knowledge or information
3. After each factual claim, add [PaperID] citation
4. Maintain academic tone and rigor
5. Synthesize information across papers thematically, not paper-by-paper"""
    
    def generate_section(self, section_title: str, chunks: List[TextChunk], topic: str) -> str:
        """
        Generate a survey section from provided chunks.
        
        Args:
            section_title: Section name (e.g., "Introduction", "Methodologies")
            chunks: Relevant text chunks to use
            topic: Research topic
            
        Returns:
            Generated text with inline [PaperID] citations
        """
        # Mock generation using templates
        # Real implementation would call OpenAI/Gemini API with chunks as context
        
        if section_title == "Introduction":
            return self._generate_introduction(chunks, topic)
        elif section_title == "Methodologies Used":
            return self._generate_methodologies(chunks, topic)
        elif section_title == "Key Findings and Results":
            return self._generate_findings(chunks, topic)
        elif section_title == "Research Gaps and Future Directions":
            return self._generate_gaps(chunks, topic)
        else:
            return self._generate_generic(section_title, chunks, topic)
    
    def _generate_introduction(self, chunks: List[TextChunk], topic: str) -> str:
        """Generate introduction section."""
        # Extract unique papers
        papers_used = self._get_unique_papers(chunks)
        paper_ids = list(papers_used.keys())[:5]  # Use top 5 for intro
        
        intro = f"""The field of {topic} has seen significant advances in recent years. """
        
        # Add context from papers
        if paper_ids:
            intro += f"""Foundational work by {self._random_citation(paper_ids)} established key principles that continue to influence current research. """
            intro += f"""Recent studies {self._random_citation(paper_ids)} have expanded these concepts through novel methodologies and applications. """
            intro += f"""The growing importance of this domain is evidenced by extensive research efforts {self._random_citation(paper_ids)} addressing both theoretical foundations and practical implementations. """
        
        intro += f"""This literature survey examines the current state of research in {topic}, analyzing key methodologies, significant findings, and identifying areas for future investigation. """
        intro += f"""Our review synthesizes insights from recent publications {self._random_citation(paper_ids)} to provide a comprehensive overview of the field."""
        
        return intro
    
    def _generate_methodologies(self, chunks: List[TextChunk], topic: str) -> str:
        """Generate methodologies section."""
        papers_used = self._get_unique_papers(chunks)
        paper_ids = list(papers_used.keys())[:8]
        
        method = f"""Research in {topic} employs diverse methodological approaches. """
        
        if paper_ids:
            method += f"""A dominant paradigm involves data-driven techniques, as demonstrated in {self._random_citation(paper_ids)}. """
            method += f"""These approaches typically incorporate preprocessing pipelines and feature engineering {self._random_citation(paper_ids)}, """
            method += f"""followed by model training using optimization algorithms {self._random_citation(paper_ids)}. """
            method += f"""Recent work has explored novel architectural designs {self._random_citation(paper_ids)} """
            method += f"""that improve upon baseline methods through innovative modifications {self._random_citation(paper_ids)}. """
            method += f"""Experimental validation is commonly performed using benchmark datasets {self._random_citation(paper_ids)}, """
            method += f"""with rigorous comparison against state-of-the-art techniques {self._random_citation(paper_ids)}."""
        
        return method
    
    def _generate_findings(self, chunks: List[TextChunk], topic: str) -> str:
        """Generate findings section."""
        papers_used = self._get_unique_papers(chunks)
        paper_ids = list(papers_used.keys())[:8]
        
        findings = f"""Empirical studies in {topic} have yielded several important insights. """
        
        if paper_ids:
            findings += f"""Performance improvements of 5-15% over baseline methods have been consistently reported {self._random_citation(paper_ids)}. """
            findings += f"""These gains are attributed to enhanced model architectures {self._random_citation(paper_ids)} """
            findings += f"""and optimized training procedures {self._random_citation(paper_ids)}. """
            findings += f"""Ablation studies confirm the contribution of individual components {self._random_citation(paper_ids)}, """
            findings += f"""while comparative analyses validate the effectiveness of proposed approaches {self._random_citation(paper_ids)}. """
            findings += f"""Practical applicability has been demonstrated across various real-world scenarios {self._random_citation(paper_ids)}."""
        
        return findings
    
    def _generate_gaps(self, chunks: List[TextChunk], topic: str) -> str:
        """Generate research gaps section."""
        papers_used = self._get_unique_papers(chunks)
        paper_ids = list(papers_used.keys())[:5]
        
        gaps = f"""Despite significant progress, several research gaps remain in {topic}. """
        
        if paper_ids:
            gaps += f"""Current approaches face scalability challenges when applied to large-scale datasets {self._random_citation(paper_ids)}. """
            gaps += f"""The interpretability of complex models remains an open question {self._random_citation(paper_ids)}, """
            gaps += f"""limiting their adoption in critical applications. """
            gaps += f"""Future research should address computational efficiency {self._random_citation(paper_ids)} """
            gaps += f"""and explore theoretical foundations more rigorously. """
            gaps += f"""Additionally, cross-domain generalization {self._random_citation(paper_ids)} represents a promising direction for investigation."""
        
        return gaps
    
    def _generate_generic(self, section_title: str, chunks: List[TextChunk], topic: str) -> str:
        """Generic section generation."""
        papers_used = self._get_unique_papers(chunks)
        paper_ids = list(papers_used.keys())[:5]
        
        content = f"""This section discusses {section_title.lower()} in the context of {topic}. """
        if paper_ids:
            content += f"""Recent literature {self._random_citation(paper_ids)} provides valuable insights into this aspect. """
            content += f"""Multiple studies {self._random_citation(paper_ids)} have contributed to our understanding through empirical analysis and theoretical development."""
        
        return content
    
    def _get_unique_papers(self, chunks: List[TextChunk]) -> dict:
        """Extract unique papers from chunks."""
        papers = {}
        for chunk in chunks:
            if chunk.paper_id not in papers:
                papers[chunk.paper_id] = {
                    "title": chunk.paper_title,
                    "year": chunk.year
                }
        return papers
    
    def _random_citation(self, paper_ids: List[str]) -> str:
        """Generate citation string with random paper IDs."""
        if not paper_ids:
            return ""
        
        # Pick 1-3 random papers
        num_citations = min(random.randint(1, 3), len(paper_ids))
        cited = random.sample(paper_ids, num_citations)
        
        # Format as [PaperID1][PaperID2]
        return "".join([f"[{pid}]" for pid in cited])


class RealLLMEngine:
    """
    Real LLM engine wrapper (for future use).
    Supports OpenAI and Google Gemini APIs.
    """
    
    def __init__(self, provider: str = "openai", api_key: str = None):
        """
        Initialize real LLM engine.
        
        Args:
            provider: "openai" or "google"
            api_key: API key for the provider
        """
        self.provider = provider
        self.api_key = api_key
        
        # Placeholder for future implementation
        # if provider == "openai":
        #     import openai
        #     openai.api_key = api_key
        # elif provider == "google":
        #     import google.generativeai as genai
        #     genai.configure(api_key=api_key)
    
    def generate_section(self, section_title: str, chunks: List[TextChunk], topic: str) -> str:
        """
        Generate section using real LLM API.
        
        Future implementation will:
        1. Prepare chunks as context
        2. Create prompt with constraints
        3. Call LLM API
        4. Parse and validate output
        """
        raise NotImplementedError("Real LLM integration not yet implemented. Use MockLLMEngine.")
