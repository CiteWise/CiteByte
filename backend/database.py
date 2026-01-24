"""
Database module using SQLAlchemy with SQLite.
Stores papers, text chunks, and generated surveys.
"""

from sqlalchemy import create_engine, Column, String, Integer, Text, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import settings

Base = declarative_base()


class PaperDB(Base):
    """Paper metadata storage."""
    __tablename__ = "papers"
    
    paper_id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    authors = Column(Text, nullable=False)  # JSON string
    year = Column(Integer)
    abstract = Column(Text)
    doi = Column(String)
    venue = Column(String)
    citation_count = Column(Integer, default=0)
    url = Column(String)
    created_at = Column(DateTime, default=datetime.now)


class TextChunkDB(Base):
    """Evidence chunks with traceability."""
    __tablename__ = "text_chunks"
    
    chunk_id = Column(String, primary_key=True)
    paper_id = Column(String, nullable=False)
    paper_title = Column(String)
    year = Column(Integer)
    section_name = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class SurveyDB(Base):
    """Generated surveys (for caching)."""
    __tablename__ = "surveys"
    
    survey_id = Column(String, primary_key=True)
    topic = Column(String, nullable=False)
    content = Column(Text, nullable=False)  # JSON string
    created_at = Column(DateTime, default=datetime.now)


# Database engine and session
engine = create_engine(settings.database_url, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency for FastAPI to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
