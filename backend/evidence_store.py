"""
Evidence storage module.
Extracts and stores structured text chunks for citation traceability.
"""

from typing import List
import json
from sqlalchemy.orm import Session
from models import Paper, TextChunk
from database import TextChunkDB, PaperDB
import hashlib


class EvidenceStore:
    """Extract and store evidence chunks with traceability."""
    
    def __init__(self, db_session: Session):
        self.db = db_session
        self.chunk_size = 500  # ~500 tokens per chunk
    
    def store_papers(self, papers: List[Paper]) -> None:
        """Store paper metadata in database."""
        for paper in papers:
            # Check if already exists
            existing = self.db.query(PaperDB).filter_by(paper_id=paper.paper_id).first()
            if existing:
                continue
            
            # Store paper
            paper_db = PaperDB(
                paper_id=paper.paper_id,
                title=paper.title,
                authors=json.dumps([{"name": a.name, "affiliation": a.affiliation} for a in paper.authors]),
                year=paper.year,
                abstract=paper.abstract,
                doi=paper.doi,
                venue=paper.venue,
                citation_count=paper.citation_count,
                url=paper.url
            )
            self.db.add(paper_db)
        
        self.db.commit()
    
    def extract_and_store_chunks(self, papers: List[Paper], top_papers: List[Paper]) -> List[TextChunk]:
        """
        Extract text chunks from papers.
        - All papers: abstract
        - Top papers: methodology and results sections (mocked)
        
        Args:
            papers: All retrieved papers
            top_papers: Top-ranked papers for full text extraction
            
        Returns:
            List of TextChunk objects
        """
        all_chunks = []
        top_paper_ids = {p.paper_id for p in top_papers}
        
        for paper in papers:
            # Extract abstract chunks for all papers
            abstract_chunks = self._extract_section_chunks(
                paper=paper,
                section_name="Abstract",
                text=paper.abstract
            )
            all_chunks.extend(abstract_chunks)
            
            # Extract full sections for top papers
            if paper.paper_id in top_paper_ids:
                # Mock methodology and results sections
                methodology_chunks = self._extract_section_chunks(
                    paper=paper,
                    section_name="Methodology",
                    text=self._mock_methodology_section(paper)
                )
                all_chunks.extend(methodology_chunks)
                
                results_chunks = self._extract_section_chunks(
                    paper=paper,
                    section_name="Results",
                    text=self._mock_results_section(paper)
                )
                all_chunks.extend(results_chunks)
        
        # Store chunks in database
        self._store_chunks(all_chunks)
        
        return all_chunks
    
    def _extract_section_chunks(self, paper: Paper, section_name: str, text: str) -> List[TextChunk]:
        """Split section text into chunks."""
        chunks = []
        
        # Simple chunking by words (approximate tokens)
        words = text.split()
        chunk_texts = []
        
        current_chunk = []
        for word in words:
            current_chunk.append(word)
            if len(current_chunk) >= 400:  # ~500 tokens
                chunk_texts.append(" ".join(current_chunk))
                current_chunk = []
        
        # Add remaining words
        if current_chunk:
            chunk_texts.append(" ".join(current_chunk))
        
        # Create TextChunk objects
        for idx, chunk_text in enumerate(chunk_texts):
            chunk_id = self._generate_chunk_id(paper.paper_id, section_name, idx)
            chunk = TextChunk(
                chunk_id=chunk_id,
                paper_id=paper.paper_id,
                paper_title=paper.title,
                year=paper.year,
                section_name=section_name,
                text=chunk_text
            )
            chunks.append(chunk)
        
        return chunks
    
    def _store_chunks(self, chunks: List[TextChunk]) -> None:
        """Store chunks in database."""
        for chunk in chunks:
            # Check if already exists
            existing = self.db.query(TextChunkDB).filter_by(chunk_id=chunk.chunk_id).first()
            if existing:
                continue
            
            chunk_db = TextChunkDB(
                chunk_id=chunk.chunk_id,
                paper_id=chunk.paper_id,
                paper_title=chunk.paper_title,
                year=chunk.year,
                section_name=chunk.section_name,
                text=chunk.text
            )
            self.db.add(chunk_db)
        
        self.db.commit()
    
    def retrieve_relevant_chunks(self, query: str, top_k: int = 20) -> List[TextChunk]:
        """
        Retrieve most relevant chunks for a query.
        Simple keyword matching for now.
        """
        # Get all chunks
        chunks_db = self.db.query(TextChunkDB).all()
        
        # Score chunks by keyword overlap
        query_words = set(query.lower().split())
        scored_chunks = []
        
        for chunk_db in chunks_db:
            chunk_words = set(chunk_db.text.lower().split())
            overlap = len(query_words & chunk_words)
            
            if overlap > 0:
                chunk = TextChunk(
                    chunk_id=chunk_db.chunk_id,
                    paper_id=chunk_db.paper_id,
                    paper_title=chunk_db.paper_title,
                    year=chunk_db.year,
                    section_name=chunk_db.section_name,
                    text=chunk_db.text
                )
                scored_chunks.append((overlap, chunk))
        
        # Sort by score
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        return [chunk for _, chunk in scored_chunks[:top_k]]
    
    def _generate_chunk_id(self, paper_id: str, section: str, index: int) -> str:
        """Generate unique chunk ID."""
        content = f"{paper_id}_{section}_{index}"
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    def _mock_methodology_section(self, paper: Paper) -> str:
        """Generate mock methodology text for top papers."""
        return f"""We propose a novel approach for {paper.title}. Our methodology consists of three main components: 
        (1) Data preprocessing and feature extraction using standard techniques,
        (2) Model architecture design incorporating recent advances in the field,
        (3) Training procedure with carefully tuned hyperparameters.
        We implement our approach using Python and popular deep learning frameworks.
        The proposed method addresses key limitations of existing approaches while maintaining computational efficiency.
        Our implementation is optimized for both accuracy and runtime performance."""
    
    def _mock_results_section(self, paper: Paper) -> str:
        """Generate mock results text for top papers."""
        return f"""Experimental evaluation demonstrates the effectiveness of our approach.
        We conduct experiments on multiple benchmark datasets including standard test sets.
        Our method achieves state-of-the-art performance, outperforming baseline methods by 5-15%.
        Ablation studies confirm the contribution of each component.
        We analyze performance across different settings and data conditions.
        The results validate our theoretical analysis and demonstrate practical applicability.
        Statistical significance tests confirm the reliability of improvements."""
