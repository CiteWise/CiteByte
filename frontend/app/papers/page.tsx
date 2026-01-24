'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

interface PaperSearchData {
    topic: string;
    papers_found: number;
    ranked_papers: Array<{
        paper: {
            paper_id: string;
            title: string;
            authors: Array<{ name: string; affiliation?: string }>;
            year: number;
            abstract: string;
            venue?: string;
            citation_count?: number;
            doi?: string;
        };
        bm25_score: number;
        rank: number;
        used_for_full_text: boolean;
    }>;
}

export default function PapersPage() {
    const router = useRouter();
    const [data, setData] = useState<PaperSearchData | null>(null);

    useEffect(() => {
        const stored = sessionStorage.getItem('paperSearchData');
        if (stored) {
            setData(JSON.parse(stored));
        }
    }, []);

    if (!data) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <p className="text-gray-600 mb-4">No paper search data found</p>
                    <Link href="/" className="academic-button inline-block">
                        Return Home
                    </Link>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-academic-navy text-white py-8 shadow-lg">
                <div className="academic-container">
                    <Link href="/" className="text-sm text-gray-300 hover:text-white mb-2 inline-block">
                        ← Back to Home
                    </Link>
                    <h1 className="text-3xl font-bold">Paper Retrieval & Ranking</h1>
                    <p className="text-gray-300 mt-2">Topic: {data.topic}</p>
                </div>
            </header>

            <main className="academic-container">
                {/* Summary */}
                <div className="academic-card mb-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <h2 className="text-xl font-bold text-gray-800">
                                Found {data.papers_found} papers
                            </h2>
                            <p className="text-sm text-gray-600 mt-1">
                                Top {data.ranked_papers.filter(p => p.used_for_full_text).length} papers selected for full text analysis
                            </p>
                        </div>
                        <div className="bg-blue-50 px-6 py-3 rounded-lg">
                            <p className="text-sm font-semibold text-academic-blue">Ranked by BM25</p>
                        </div>
                    </div>
                </div>

                {/* Papers List */}
                <div className="space-y-4">
                    {data.ranked_papers.map((rankedPaper) => {
                        const { paper, bm25_score, rank, used_for_full_text } = rankedPaper;

                        return (
                            <div
                                key={paper.paper_id}
                                className={`paper-card ${used_for_full_text ? 'border-l-4 border-academic-blue bg-blue-50' : ''}`}
                            >
                                <div className="flex items-start gap-4">
                                    {/* Rank Badge */}
                                    <div className={`flex-shrink-0 w-12 h-12 rounded-full flex items-center justify-center font-bold ${used_for_full_text ? 'bg-academic-blue text-white' : 'bg-gray-200 text-gray-600'
                                        }`}>
                                        #{rank}
                                    </div>

                                    {/* Paper Details */}
                                    <div className="flex-1">
                                        <h3 className="text-lg font-semibold text-gray-900 mb-2">
                                            {paper.title}
                                        </h3>

                                        <div className="text-sm text-gray-600 mb-2">
                                            <span className="font-medium">
                                                {paper.authors.slice(0, 3).map(a => a.name).join(', ')}
                                                {paper.authors.length > 3 && ', et al.'}
                                            </span>
                                            {' • '}
                                            <span>{paper.year}</span>
                                            {paper.venue && (
                                                <>
                                                    {' • '}
                                                    <span className="italic">{paper.venue}</span>
                                                </>
                                            )}
                                        </div>

                                        <p className="text-sm text-gray-700 mb-3 line-clamp-3">
                                            {paper.abstract}
                                        </p>

                                        <div className="flex items-center gap-4 text-xs text-gray-500">
                                            <span className="bg-gray-100 px-3 py-1 rounded">
                                                BM25: {bm25_score.toFixed(2)}
                                            </span>
                                            {paper.citation_count && (
                                                <span>📊 {paper.citation_count.toLocaleString()} citations</span>
                                            )}
                                            {used_for_full_text && (
                                                <span className="bg-blue-100 text-academic-blue px-3 py-1 rounded font-semibold">
                                                    ⭐ Full Text Analyzed
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </main>
        </div>
    );
}
