# Literature Survey System - Backend

Citation-grounded AI-assisted literature survey generation system for engineering research.

## Overview

The backend is built with **FastAPI** and uses **SQLite** for data storage. It implements a RAG (Retrieval-Augmented Generation) pipeline with strict academic constraints to ensure citation traceability.

## Architecture

```
Backend Modules:
├── main.py                 # FastAPI application & endpoints
├── config.py               # Environment configuration
├── models.py               # Pydantic data models
├── database.py             # SQLAlchemy database layer
├── retrieval.py            # Paper retrieval orchestrator
├── ranking.py              # BM25 ranking algorithm
├── evidence_store.py       # Evidence extraction & storage
├── llm_engine.py           # LLM generation (mock/real)
├── survey_generator.py     # Survey generation pipeline
├── citation_formatter.py   # IEEE citation formatting
└── mock_apis/              # Mock API clients
    ├── semantic_scholar.py
    ├── ieee_xplore.py
    └── crossref.py
```

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env` from project root or create one:

```bash
# Already created at project root
# Backend reads from ../env
```

### 3. Run Backend

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

## API Endpoints

### GET `/`
Root endpoint with system info.

### GET `/api/health`
Health check endpoint.

### POST `/api/search`
Search and rank papers for a topic.

**Request:**
```json
{
  "topic": "Transformer models in NLP",
  "domain": "Computer Science",
  "max_papers": 50
}
```

**Response:**
```json
{
  "topic": "Transformer models in NLP",
  "papers_found": 20,
  "ranked_papers": [...]
}
```

### POST `/api/generate-survey`
Generate complete literature survey.

**Request:**
```json
{
  "topic": "Deep learning for cybersecurity",
  "domain": "Computer Science"
}
```

**Response:**
```json
{
  "topic": "...",
  "sections": [...],
  "references": [...],
  "papers_used": [...],
  "generated_at": "2026-01-24T18:00:00"
}
```

### GET `/api/papers/{paper_id}`
Get details for a specific paper.

## Key Features

✅ **Mock APIs** - Realistic placeholder data for Semantic Scholar, IEEE, CrossRef  
✅ **BM25 Ranking** - Classical IR algorithm for paper relevance  
✅ **Evidence Storage** - Structured chunks with traceability  
✅ **RAG Pipeline** - Constrained generation using only stored chunks  
✅ **IEEE Citations** - Automatic conversion to numbered references  
✅ **SQLite Database** - Persistent storage for papers and chunks  

## Academic Constraints

The system enforces:
- **No hallucination**: LLM uses ONLY provided chunks
- **Citation grounding**: Every claim has paper reference
- **Engineering domain**: Filter for CS/AI/ML papers
- **Traceability**: Map citations back to source papers

## Mock Mode

Currently running in mock mode:
- `USE_MOCK_APIS=true` - No real API calls needed
- `USE_MOCK_LLM=true` - Template-based generation

To switch to real APIs:
1. Add API keys to `.env`
2. Set `USE_MOCK_APIS=false`
3. Implement real API clients (placeholders exist)

## Future Enhancements

- Real Semantic Scholar API integration
- OpenAI/Gemini LLM integration  
- PDF parsing for full text
- Advanced ranking (neural models)
- Caching and optimization
