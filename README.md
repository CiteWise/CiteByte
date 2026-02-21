# Literature Survey System

**v1.0.0** • University Engineering Mini-Project

A citation-grounded AI-assisted literature survey system that improves trust and verifiability in academic writing for engineering research domains.

## 🎯 Project Overview

This system generates structured literature surveys with full citation traceability, ensuring every claim is backed by real academic papers. Built for university-level engineering research, it prioritizes academic rigor over creativity.

### Academic Positioning

> **"A citation-grounded AI-assisted literature survey system that improves trust and verifiability in academic writing."**

This is:
- ✅ An academic writing assistant focused on correctness
- ✅ A tool for verifiable, citation-grounded surveys
- ✅ A proof-of-concept for engineering research

This is NOT:
- ❌ A replacement for human researchers
- ❌ A creative writing AI
- ❌ A general-purpose search engine

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Input (Topic)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Frontend (Next.js)                         │
│  • Topic Input Page                                          │
│  • Papers Ranking View                                       │
│  • Survey Display with Citations                             │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI)                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Paper Retrieval → BM25 Ranking → Evidence Storage   │   │
│  │       ↓                ↓                    ↓         │   │
│  │  Mock APIs       Top-K Papers       Text Chunks      │   │
│  │                                          ↓            │   │
│  │                              RAG Survey Generator     │   │
│  │                                          ↓            │   │
│  │                          Citation Formatter (IEEE)    │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              SQLite Database                                 │
│  • Papers metadata                                           │
│  • Text chunks (evidence)                                    │
│  • Generated surveys                                         │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- npm or yarn

### 1. Clone Repository

```bash
cd literature-survey-system
```

### 2. Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend runs on `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:3000`

### 4. Access Application

Open `http://localhost:3000` in your browser and enter a research topic!

## 📋 Features

### Core Features (Implemented)

✅ **Mock API Integration** - Semantic Scholar, IEEE Xplore, CrossRef  
✅ **BM25 Ranking** - Classical information retrieval algorithm  
✅ **Evidence Storage** - Structured chunks with paper traceability  
✅ **RAG Pipeline** - Retrieval-Augmented Generation with constraints  
✅ **IEEE Citations** - Automatic numbered reference formatting  
✅ **Citation Grounding** - Every claim linked to source papers  
✅ **Academic UI** - Clean, professional design  
✅ **Export Functionality** - Download surveys as text or JSON  

### Academic Constraints (Enforced)

🔒 **No Hallucination** - LLM uses ONLY provided text chunks  
🔒 **Engineering Domain Only** - Filters for CS/AI/ML/Cybersecurity papers  
🔒 **Citation Required** - Every factual claim has a reference  
🔒 **Verifiable Claims** - Users can trace claims to source papers  

## 📁 Project Structure

```
literature-survey-system/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Environment configuration
│   ├── models.py               # Pydantic data models
│   ├── database.py             # SQLAlchemy database
│   ├── retrieval.py            # Paper retrieval
│   ├── ranking.py              # BM25 ranking
│   ├── evidence_store.py       # Evidence extraction
│   ├── llm_engine.py           # LLM generation (mock/real)
│   ├── survey_generator.py     # Survey generation
│   ├── citation_formatter.py   # IEEE citation formatting
│   ├── mock_apis/              # Mock API clients
│   │   ├── semantic_scholar.py
│   │   ├── ieee_xplore.py
│   │   └── crossref.py
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   ├── app/
│   │   ├── page.tsx            # Home page
│   │   ├── papers/page.tsx     # Papers ranking view
│   │   ├── survey/page.tsx     # Survey display
│   │   ├── layout.tsx          # Root layout
│   │   └── globals.css         # Global styles
│   ├── components/
│   │   └── CitationViewer.tsx  # Citation component
│   ├── package.json
│   └── README.md
├── .env                        # Environment variables
├── .gitignore
└── README.md                   # This file
```

## 🔧 Configuration

### Environment Variables (`.env`)

```bash
# Mock mode (default - no real API keys needed)
USE_MOCK_APIS=true
USE_MOCK_LLM=true

# Optional: Real API keys (for future use)
SEMANTIC_SCHOLAR_API_KEY=your_key_here
IEEE_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

# Database
DATABASE_URL=sqlite:///./literature_survey.db

# Settings
MAX_PAPERS_RETRIEVE=50
TOP_PAPERS_FULL_TEXT=5
```

## 📖 Usage Example

### 1. Enter Research Topic

Example: "Transformer models in natural language processing"

### 2. View Ranked Papers

- System retrieves 20-50 papers
- Papers ranked by BM25 relevance
- Top 5 papers used for full text analysis

### 3. Generate Survey

Structured sections:
- **Introduction**: Context and motivation
- **Methodologies Used**: Technical approaches
- **Key Findings and Results**: Empirical insights
- **Research Gaps**: Future directions

### 4. Verify Citations

- Click any citation [1] to view reference
- Trace claims back to source papers
- Export survey with full bibliography

## 🎓 Academic Use Case

**Scenario**: Final year engineering student needs literature review for mini-project on "Deep Learning for Cybersecurity"

**Workflow**:
1. Enter topic: "Deep learning for intrusion detection"
2. System retrieves 25 relevant papers from mock database
3. BM25 ranks papers, top 5 selected for detailed analysis
4. Survey generated with 4 sections, 18 citations
5. Student reviews survey, verifies citations
6. Exports survey for inclusion in project report

**Outcome**: Citation-grounded review ready for professor evaluation

## 🔮 Future Enhancements

### Phase 2 (Future Work)

- Real Semantic Scholar API integration
- OpenAI/Google Gemini LLM integration
- PDF parsing for full paper text
- Advanced ranking (neural models)
- Multi-paper comparison views
- Export to LaTeX/PDF with formatting
- User accounts and survey history

### Out of Scope

- Training custom LLMs
- Web scraping random sources
- Non-engineering domains
- Real-time collaboration

## 🛡️ Limitations

**Current System**:
- Mock data (no real API calls)
- Template-based LLM (not real generation)
- Limited to engineering domains
- No user authentication
- Local-only deployment

**By Design**:
- Not for creative writing
- Requires internet for real APIs (future)
- English language only
- Academic sources only

## 📝 License & Academic Use

This is a university engineering mini-project for educational purposes.

**Defendable Claims for Viva**:
- ✅ "We use BM25, a proven classical IR algorithm"
- ✅ "Every citation is traceable to source papers"
- ✅ "RAG pattern ensures no hallucination"
- ✅ "System enforces academic constraints"

**NOT Defensible**:
- ❌ "We trained a custom LLM"
- ❌ "System works for all academic fields"
- ❌ "Replaces human literature review"

## 👥 Contributors

University Engineering Mini-Project Team

## 📞 Support

For more questions or issues:
Contact :
Neelam Joshi (Team Leader) - +91 7987130543
Cheryl Cardoza - +91 9892947915
Bipin P Kuruvilla - +91 9137406241

---

**Built with academic rigor. Focused on verifiability. Designed for trust.**
