'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export default function Home() {
    const router = useRouter();
    const [topic, setTopic] = useState('');
    const [domain, setDomain] = useState('Computer Science');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleGenerateSurvey = async () => {
        if (!topic.trim()) {
            setError('Please enter a research topic');
            return;
        }

        setError('');
        setLoading(true);

        try {
            // Call backend to generate survey
            const response = await axios.post(`${API_BASE}/api/generate-survey`, {
                topic: topic.trim(),
                domain,
                max_papers: 50,
            });

            // Store result in session storage
            sessionStorage.setItem('surveyData', JSON.stringify(response.data));

            // Navigate to survey page
            router.push('/survey');
        } catch (err: any) {
            console.error('Error generating survey:', err);
            setError(err.response?.data?.detail || 'Failed to generate survey. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleSearchPapers = async () => {
        if (!topic.trim()) {
            setError('Please enter a research topic');
            return;
        }

        setError('');
        setLoading(true);

        try {
            // Call backend to search papers
            const response = await axios.post(`${API_BASE}/api/search`, {
                topic: topic.trim(),
                domain,
                max_papers: 50,
            });

            // Store result in session storage
            sessionStorage.setItem('paperSearchData', JSON.stringify(response.data));

            // Navigate to papers page
            router.push('/papers');
        } catch (err: any) {
            console.error('Error searching papers:', err);
            setError(err.response?.data?.detail || 'Failed to search papers. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
            {/* Header */}
            <header className="bg-academic-navy text-white py-12 shadow-lg">
                <div className="academic-container">
                    <h1 className="text-4xl font-bold mb-3">Literature Survey System</h1>
                    <p className="text-lg text-gray-300">
                        Citation-grounded AI-assisted literature survey generation for engineering research
                    </p>
                </div>
            </header>

            {/* Main Content */}
            <main className="academic-container mt-12">
                <div className="max-w-3xl mx-auto">
                    {/* Info Card */}
                    <div className="academic-card mb-8">
                        <h2 className="text-2xl font-bold text-academic-navy mb-4">
                            Generate Academic Literature Survey
                        </h2>
                        <p className="text-gray-700 mb-4">
                            This system generates structured literature surveys with full citation traceability.
                            All claims are grounded in real academic papers with IEEE-style references.
                        </p>
                        <div className="bg-blue-50 border-l-4 border-academic-blue p-4 rounded">
                            <p className="text-sm text-gray-800">
                                <strong>Academic Constraints:</strong> Engineering domain only • Citation-grounded • No hallucination • Verifiable claims
                            </p>
                        </div>
                    </div>

                    {/* Input Form */}
                    <div className="academic-card">
                        <div className="mb-6">
                            <label htmlFor="topic" className="block text-sm font-semibold text-gray-700 mb-2">
                                Research Topic *
                            </label>
                            <input
                                id="topic"
                                type="text"
                                className="academic-input"
                                placeholder="e.g., Transformer models in natural language processing"
                                value={topic}
                                onChange={(e) => setTopic(e.target.value)}
                                disabled={loading}
                            />
                            <p className="text-xs text-gray-500 mt-1">
                                Enter a focused engineering research topic
                            </p>
                        </div>

                        <div className="mb-6">
                            <label htmlFor="domain" className="block text-sm font-semibold text-gray-700 mb-2">
                                Engineering Domain
                            </label>
                            <select
                                id="domain"
                                className="academic-input"
                                value={domain}
                                onChange={(e) => setDomain(e.target.value)}
                                disabled={loading}
                            >
                                <option value="Computer Science">Computer Science</option>
                                <option value="Artificial Intelligence">Artificial Intelligence</option>
                                <option value="Machine Learning">Machine Learning</option>
                                <option value="Cybersecurity">Cybersecurity</option>
                                <option value="Electronics">Electronics</option>
                                <option value="Software Engineering">Software Engineering</option>
                            </select>
                        </div>

                        {error && (
                            <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6">
                                <p className="text-sm text-red-800">{error}</p>
                            </div>
                        )}

                        <div className="flex gap-4">
                            <button
                                onClick={handleSearchPapers}
                                disabled={loading}
                                className="academic-button flex-1"
                            >
                                {loading ? 'Processing...' : '1. Search & Rank Papers'}
                            </button>

                            <button
                                onClick={handleGenerateSurvey}
                                disabled={loading}
                                className="academic-button flex-1 bg-green-700 hover:bg-green-800"
                            >
                                {loading ? 'Generating...' : '2. Generate Full Survey'}
                            </button>
                        </div>

                        <p className="text-xs text-gray-500 mt-4 text-center">
                            Step 1 shows paper retrieval and ranking. Step 2 generates the complete survey.
                        </p>
                    </div>

                    {/* Features */}
                    <div className="mt-8 grid grid-cols-3 gap-4">
                        <div className="text-center p-4">
                            <div className="text-3xl mb-2">📚</div>
                            <h3 className="font-semibold text-sm text-gray-800">Trusted Sources</h3>
                            <p className="text-xs text-gray-600">Semantic Scholar, IEEE Xplore</p>
                        </div>
                        <div className="text-center p-4">
                            <div className="text-3xl mb-2">🔍</div>
                            <h3 className="font-semibold text-sm text-gray-800">BM25 Ranking</h3>
                            <p className="text-xs text-gray-600">Relevance-based paper selection</p>
                        </div>
                        <div className="text-center p-4">
                            <div className="text-3xl mb-2">✅</div>
                            <h3 className="font-semibold text-sm text-gray-800">Citation Grounding</h3>
                            <p className="text-xs text-gray-600">Every claim is verifiable</p>
                        </div>
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className="mt-16 py-8 border-t border-gray-200 bg-white">
                <div className="academic-container text-center text-sm text-gray-600">
                    <p>University Engineering Mini-Project • Literature Survey System v1.0</p>
                    <p className="mt-2">Focus on academic rigor, citation correctness, and verifiability</p>
                </div>
            </footer>
        </div>
    );
}
