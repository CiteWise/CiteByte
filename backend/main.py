"""
FastAPI main application.
Provides REST API endpoints for literature survey system.
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from database import init_db, get_db
from models import (
    SurveyRequest, SurveyResponse, PaperSearchResponse,
    RankedPaper, Paper, SurveySection, Citation
)
from retrieval import PaperRetriever
from ranking import PaperRanker
from evidence_store import EvidenceStore
from survey_generator import SurveyGenerator
from citation_formatter import CitationFormatter
from config import settings

# Initialize FastAPI app
app = FastAPI(
    title="Literature Survey System",
    description="Citation-grounded AI-assisted literature survey generation",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    """Initialize database tables."""
    init_db()
    print("✅ Database initialized")
    print(f"✅ Using mock APIs: {settings.use_mock_apis}")
    print(f"✅ Using mock LLM: {settings.use_mock_llm}")


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Literature Survey System API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "mock_mode": settings.use_mock_apis
    }


@app.post("/api/search", response_model=PaperSearchResponse)
def search_papers(request: SurveyRequest, db: Session = Depends(get_db)):
    """
    Search and rank papers for a research topic.
    
    Args:
        request: SurveyRequest with topic and parameters
        db: Database session
        
    Returns:
        PaperSearchResponse with ranked papers
    """
    try:
        # Retrieve papers
        retriever = PaperRetriever()
        papers = retriever.retrieve_papers(
            topic=request.topic,
            max_results=request.max_papers or settings.max_papers_retrieve
        )
        
        if not papers:
            raise HTTPException(status_code=404, detail="No papers found for this topic")
        
        # Rank papers
        ranker = PaperRanker()
        ranked_papers = ranker.rank_papers(papers, request.topic)
        
        # Store papers in database
        evidence_store = EvidenceStore(db)
        evidence_store.store_papers(papers)
        
        return PaperSearchResponse(
            topic=request.topic,
            papers_found=len(ranked_papers),
            ranked_papers=ranked_papers
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.post("/api/generate-survey", response_model=SurveyResponse)
def generate_survey(request: SurveyRequest, db: Session = Depends(get_db)):
    """
    Generate complete literature survey with citations.
    
    This endpoint:
    1. Retrieves and ranks papers
    2. Extracts evidence chunks
    3 Generates survey sections using RAG
    4. Formats citations in IEEE style
    
    Args:
        request: SurveyRequest with topic
        db: Database session
        
    Returns:
        SurveyResponse with structured survey and references
    """
    try:
        # Step 1: Retrieve papers
        retriever = PaperRetriever()
        papers = retriever.retrieve_papers(
            topic=request.topic,
            max_results=request.max_papers or settings.max_papers_retrieve
        )
        
        if not papers:
            raise HTTPException(status_code=404, detail="No papers found for this topic")
        
        # Step 2: Rank papers
        ranker = PaperRanker()
        ranked_papers = ranker.rank_papers(papers, request.topic)
        top_papers = ranker.get_top_papers(ranked_papers)
        
        # Step 3: Store papers and extract chunks
        evidence_store = EvidenceStore(db)
        evidence_store.store_papers(papers)
        chunks = evidence_store.extract_and_store_chunks(papers, top_papers)
        
        print(f"📄 Retrieved {len(papers)} papers")
        print(f"⭐ Top {len(top_papers)} papers selected for full text")
        print(f"📝 Extracted {len(chunks)} evidence chunks")
        
        # Step 4: Generate survey sections
        generator = SurveyGenerator(db)
        sections = generator.generate_survey(request.topic, papers)
        
        print(f"📖 Generated {len(sections)} survey sections")
        
        # Step 5: Format citations
        formatter = CitationFormatter()
        processed_sections, citations = formatter.process_survey(sections, papers)
        
        print(f"🔗 Created {len(citations)} citations")
        
        # Create response
        response = SurveyResponse(
            topic=request.topic,
            sections=processed_sections,
            references=citations,
            papers_used=papers,
            generated_at=datetime.now()
        )
        
        return response
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Survey generation failed: {str(e)}")


@app.get("/api/papers/{paper_id}", response_model=Paper)
def get_paper(paper_id: str, db: Session = Depends(get_db)):
    """
    Get details for a specific paper.
    
    Args:
        paper_id: Paper ID
        db: Database session
        
    Returns:
        Paper object
    """
    from database import PaperDB
    import json
    from models import Author
    
    paper_db = db.query(PaperDB).filter_by(paper_id=paper_id).first()
    
    if not paper_db:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Convert database model to Pydantic model
    authors_data = json.loads(paper_db.authors)
    authors = [Author(**author) for author in authors_data]
    
    paper = Paper(
        paper_id=paper_db.paper_id,
        title=paper_db.title,
        authors=authors,
        year=paper_db.year,
        abstract=paper_db.abstract,
        doi=paper_db.doi,
        venue=paper_db.venue,
        citation_count=paper_db.citation_count,
        url=paper_db.url
    )
    
    return paper


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
