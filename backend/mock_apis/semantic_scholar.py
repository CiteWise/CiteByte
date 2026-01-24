"""
Mock Semantic Scholar API client.
Returns realistic placeholder data for engineering papers.
"""

from typing import List, Dict
import random
from models import Paper, Author


class MockSemanticScholarAPI:
    """Mock implementation of Semantic Scholar API."""
    
    # Engineering topics database (for realistic mock responses)
    MOCK_PAPERS = {
        "transformer": [
            {"title": "Attention Is All You Need", "year": 2017, "authors": ["Vaswani et al."], "venue": "NeurIPS", "citations": 85000},
            {"title": "BERT: Pre-training of Deep Bidirectional Transformers", "year": 2018, "authors": ["Devlin et al."], "venue": "NAACL", "citations": 65000},
            {"title": "GPT-3: Language Models are Few-Shot Learners", "year": 2020, "authors": ["Brown et al."], "venue": "NeurIPS", "citations": 15000},
            {"title": "Vision Transformer for Image Recognition", "year": 2020, "authors": ["Dosovitskiy et al."], "venue": "ICLR", "citations": 12000},
            {"title": "Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context", "year": 2019, "authors": ["Dai et al."], "venue": "ACL", "citations": 3500},
        ],
        "cybersecurity": [
            {"title": "Deep Learning for Intrusion Detection Systems", "year": 2020, "authors": ["Zhang et al."], "venue": "IEEE Transactions", "citations": 450},
            {"title": "Adversarial Machine Learning in Cybersecurity", "year": 2021, "authors": ["Kumar et al."], "venue": "ACM CCS", "citations": 320},
            {"title": "Blockchain-Based Security Framework for IoT", "year": 2019, "authors": ["Li et al."], "venue": "IEEE IoT", "citations": 680},
            {"title": "Zero Trust Architecture: A Survey", "year": 2022, "authors": ["Chen et al."], "venue": "IEEE Security", "citations": 150},
            {"title": "Federated Learning for Privacy-Preserving Systems", "year": 2021, "authors": ["Wang et al."], "venue": "ICML", "citations": 890},
        ],
        "deep learning": [
            {"title": "Deep Residual Learning for Image Recognition", "year": 2016, "authors": ["He et al."], "venue": "CVPR", "citations": 120000},
            {"title": "Generative Adversarial Networks", "year": 2014, "authors": ["Goodfellow et al."], "venue": "NeurIPS", "citations": 55000},
            {"title": "Adam: A Method for Stochastic Optimization", "year": 2014, "authors": ["Kingma et al."], "venue": "ICLR", "citations": 95000},
            {"title": "Batch Normalization: Accelerating Deep Network Training", "year": 2015, "authors": ["Ioffe et al."], "venue": "ICML", "citations": 42000},
            {"title": "Dropout: A Simple Way to Prevent Neural Networks from Overfitting", "year": 2014, "authors": ["Srivastava et al."], "venue": "JMLR", "citations": 38000},
        ],
        "machine learning": [
            {"title": "XGBoost: A Scalable Tree Boosting System", "year": 2016, "authors": ["Chen et al."], "venue": "KDD", "citations": 28000},
            {"title": "Random Forests for Classification and Regression", "year": 2001, "authors": ["Breiman"], "venue": "Machine Learning", "citations": 65000},
            {"title": "Support Vector Machines: A Practical Guide", "year": 2003, "authors": ["Hsu et al."], "venue": "Technical Report", "citations": 15000},
            {"title": "Neural Architecture Search: A Survey", "year": 2019, "authors": ["Elsken et al."], "venue": "JMLR", "citations": 2500},
            {"title": "AutoML: A Survey of the State-of-the-Art", "year": 2021, "authors": ["He et al."], "venue": "Knowledge-Based Systems", "citations": 1200},
        ],
    }
    
    def __init__(self, api_key: str = "mock_key"):
        self.api_key = api_key
    
    def search_papers(self, query: str, max_results: int = 50) -> List[Paper]:
        """
        Mock paper search based on query keywords.
        Returns realistic engineering papers.
        """
        query_lower = query.lower()
        papers = []
        
        # Find matching topic
        matched_papers = []
        for topic, topic_papers in self.MOCK_PAPERS.items():
            if topic in query_lower:
                matched_papers.extend(topic_papers)
        
        # If no match, use default ML papers
        if not matched_papers:
            matched_papers = self.MOCK_PAPERS["machine learning"]
        
        # Generate papers with realistic data
        for i, paper_data in enumerate(matched_papers[:max_results]):
            paper = self._generate_paper(paper_data, i)
            papers.append(paper)
        
        # Add some generic papers to reach target count
        while len(papers) < min(20, max_results):
            generic = self._generate_generic_paper(len(papers), query)
            papers.append(generic)
        
        return papers
    
    def _generate_paper(self, paper_data: Dict, index: int) -> Paper:
        """Generate realistic paper object."""
        paper_id = f"mock_{index:04d}"
        
        # Generate authors
        author_names = paper_data["authors"][0].split(" et al.")[0].split(", ")
        authors = [Author(name=name, affiliation=self._random_affiliation()) 
                  for name in author_names]
        
        # Generate abstract
        abstract = self._generate_abstract(paper_data["title"], paper_data.get("venue", "Conference"))
        
        return Paper(
            paper_id=paper_id,
            title=paper_data["title"],
            authors=authors,
            year=paper_data["year"],
            abstract=abstract,
            doi=f"10.1000/mock.{paper_id}",
            venue=paper_data.get("venue", "IEEE Conference"),
            citation_count=paper_data.get("citations", random.randint(50, 500)),
            url=f"https://semantic-scholar.org/paper/{paper_id}"
        )
    
    def _generate_generic_paper(self, index: int, topic: str) -> Paper:
        """Generate a generic paper when specific data not available."""
        paper_id = f"mock_{index:04d}"
        year = random.randint(2018, 2024)
        
        return Paper(
            paper_id=paper_id,
            title=f"A Survey on {topic.title()}: Methods and Applications",
            authors=[
                Author(name=f"Author {chr(65 + index % 26)}", affiliation=self._random_affiliation())
            ],
            year=year,
            abstract=self._generate_abstract(f"Survey on {topic}", "Survey Journal"),
            doi=f"10.1000/mock.{paper_id}",
            venue="International Journal of Engineering Research",
            citation_count=random.randint(50, 500),
            url=f"https://semantic-scholar.org/paper/{paper_id}"
        )
    
    def _generate_abstract(self, title: str, venue: str) -> str:
        """Generate realistic abstract text."""
        templates = [
            f"This paper presents a comprehensive study on {title}. We propose novel approaches that address key challenges in the field. Our experimental results demonstrate significant improvements over baseline methods. The proposed framework achieves state-of-the-art performance on multiple benchmark datasets. We discuss implications for future research and practical applications in engineering domains.",
            
            f"In this work, we investigate {title} and introduce innovative techniques for enhanced performance. We conduct extensive experiments across various settings and datasets. Our method outperforms existing approaches by a significant margin. We provide theoretical analysis and empirical validation of our contributions. Applications to real-world engineering problems are demonstrated.",
            
            f"We introduce a novel framework for {title}. The proposed approach leverages recent advances in machine learning and optimization. Through rigorous evaluation, we show improvements in accuracy, efficiency, and robustness. Our contributions include theoretical foundations and practical implementations. The work has implications for both academic research and industrial applications."
        ]
        return random.choice(templates)
    
    def _random_affiliation(self) -> str:
        """Return random university affiliation."""
        affiliations = [
            "MIT", "Stanford University", "Carnegie Mellon University",
            "UC Berkeley", "Georgia Tech", "University of Toronto",
            "ETH Zurich", "Oxford University", "Cambridge University",
            "IIT Delhi", "NUS Singapore", "Tsinghua University"
        ]
        return random.choice(affiliations)
