"""
Simple test script to verify backend functionality.
Run this to test the complete pipeline without starting the web server.
"""

import sys
sys.path.append('.')

from models import SurveyRequest
from retrieval import PaperRetriever
from ranking import PaperRanker
from evidence_store import EvidenceStore
from survey_generator import SurveyGenerator
from citation_formatter import CitationFormatter
from database import init_db, SessionLocal

def test_pipeline():
    """Test the complete literature survey pipeline."""
    print("=" * 60)
    print("LITERATURE SURVEY SYSTEM - PIPELINE TEST")
    print("=" * 60)
    
    # Initialize database
    print("\n[1/6] Initializing database...")
    init_db()
    db = SessionLocal()
    print("✅ Database initialized")
    
    # Test topic
    topic = "Transformer models in natural language processing"
    print(f"\n[2/6] Test topic: {topic}")
    
    # Retrieve papers
    print("\n[3/6] Retrieving papers...")
    retriever = PaperRetriever()
    papers = retriever.retrieve_papers(topic, max_results=20)
    print(f"✅ Retrieved {len(papers)} papers")
    for i, paper in enumerate(papers[:3]):
        print(f"   - {paper.title} ({paper.year})")
    
    # Rank papers
    print("\n[4/6] Ranking papers with BM25...")
    ranker = PaperRanker()
    ranked_papers = ranker.rank_papers(papers, topic)
    top_papers = ranker.get_top_papers(ranked_papers)
    print(f"✅ Ranked {len(ranked_papers)} papers")
    print(f"   Top paper: {ranked_papers[0].paper.title}")
    print(f"   BM25 score: {ranked_papers[0].bm25_score:.2f}")
    print(f"   Top {len(top_papers)} papers selected for full text")
    
    # Extract evidence
    print("\n[5/6] Extracting evidence chunks...")
    evidence_store = EvidenceStore(db)
    evidence_store.store_papers(papers)
    chunks = evidence_store.extract_and_store_chunks(papers, top_papers)
    print(f"✅ Extracted {len(chunks)} evidence chunks")
    print(f"   Chunk example: {chunks[0].text[:100]}...")
    
    # Generate survey
    print("\n[6/6] Generating literature survey...")
    generator = SurveyGenerator(db)
    sections = generator.generate_survey(topic, papers)
    print(f"✅ Generated {len(sections)} sections")
    
    # Format citations
    print("\n[7/7] Formatting citations...")
    formatter = CitationFormatter()
    processed_sections, citations = formatter.process_survey(sections, papers)
    print(f"✅ Created {len(citations)} references")
    
    # Display results
    print("\n" + "=" * 60)
    print("GENERATED SURVEY PREVIEW")
    print("=" * 60)
    
    for section in processed_sections[:2]:  # Show first 2 sections
        print(f"\n### {section.title}")
        print(section.content[:300] + "...")
    
    print(f"\n### References (showing first 3 of {len(citations)})")
    for citation in citations[:3]:
        print(f"{citation.formatted_reference}")
    
    print("\n" + "=" * 60)
    print("✅ PIPELINE TEST COMPLETED SUCCESSFULLY")
    print("=" * 60)
    
    # Cleanup
    db.close()

if __name__ == "__main__":
    try:
        test_pipeline()
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
