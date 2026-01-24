"""
Ranking module using BM25 algorithm.
Ranks papers by relevance to the research topic.
"""

from typing import List, Tuple
from rank_bm25 import BM25Okapi
from models import Paper, RankedPaper
from config import settings


class PaperRanker:
    """Rank papers using BM25 algorithm."""
    
    def __init__(self):
        self.top_k = settings.top_papers_full_text
    
    def rank_papers(self, papers: List[Paper], query: str) -> List[RankedPaper]:
        """
        Rank papers using BM25 on abstracts.
        
        Args:
            papers: List of Paper objects
            query: Research topic query
            
        Returns:
            List of RankedPaper objects sorted by score (highest first)
        """
        if not papers:
            return []
        
        # Prepare documents (abstracts) for BM25
        documents = [self._prepare_document(paper) for paper in papers]
        tokenized_docs = [doc.split() for doc in documents]
        
        # Initialize BM25
        bm25 = BM25Okapi(tokenized_docs)
        
        # Tokenize query
        tokenized_query = query.lower().split()
        
        # Get BM25 scores
        scores = bm25.get_scores(tokenized_query)
        
        # Create ranked papers
        ranked_papers = []
        for idx, (paper, score) in enumerate(zip(papers, scores)):
            # Determine if this paper should be used for full text extraction
            # Top K papers get full text processing
            rank = idx + 1  # Will be updated after sorting
            
            ranked_paper = RankedPaper(
                paper=paper,
                bm25_score=float(score),
                rank=rank,
                used_for_full_text=False  # Updated after sorting
            )
            ranked_papers.append(ranked_paper)
        
        # Sort by score (descending)
        ranked_papers.sort(key=lambda x: x.bm25_score, reverse=True)
        
        # Update ranks and mark top K for full text
        for idx, ranked_paper in enumerate(ranked_papers):
            ranked_paper.rank = idx + 1
            ranked_paper.used_for_full_text = (idx < self.top_k)
        
        return ranked_papers
    
    def _prepare_document(self, paper: Paper) -> str:
        """
        Prepare paper text for BM25 indexing.
        Combines title and abstract.
        """
        # Combine title (weighted) and abstract
        # Title appears 3x for higher weight
        title_text = f"{paper.title} {paper.title} {paper.title}"
        abstract_text = paper.abstract
        
        combined = f"{title_text} {abstract_text}"
        return combined.lower()
    
    def get_top_papers(self, ranked_papers: List[RankedPaper]) -> List[Paper]:
        """Get top K papers for full text processing."""
        return [rp.paper for rp in ranked_papers[:self.top_k]]
