'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import CitationViewer from '@/components/CitationViewer';

interface SurveySection {
    title: string;
    content: string;
}

interface Citation {
    number: number;
    paper_id: string;
    formatted_reference: string;
}

interface Paper {
    paper_id: string;
    title: string;
    authors: Array<{ name: string; affiliation?: string }>;
    year: number;
    abstract: string;
    venue?: string;
    citation_count?: number;
    doi?: string;
}

interface SurveyData {
    topic: string;
    sections: SurveySection[];
    references: Citation[];
    papers_used: Paper[];
    generated_at: string;
}

export default function SurveyPage() {
    const router = useRouter();
    const [data, setData] = useState<SurveyData | null>(null);
    const [highlightedCitation, setHighlightedCitation] = useState<number | null>(null);

    useEffect(() => {
        const stored = sessionStorage.getItem('surveyData');
        if (stored) {
            setData(JSON.parse(stored));
        }
    }, []);

    const handleCitationClick = (citationNum: number) => {
        // Scroll to reference
        const refElement = document.getElementById(`ref-${citationNum}`);
        if (refElement) {
            refElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
            setHighlightedCitation(citationNum);
            setTimeout(() => setHighlightedCitation(null), 2000);
        }
    };

    const renderContentWithCitations = (content: string) => {
        // Replace [1], [2], etc. with clickable citations
        const parts = content.split(/(\[\d+\])/g);

        return parts.map((part, idx) => {
            const match = part.match(/\[(\d+)\]/);
            if (match) {
                const citationNum = parseInt(match[1]);
                return (
                    <button
                        key={idx}
                        onClick={() => handleCitationClick(citationNum)}
                        className="citation-link"
                        title={`View reference [${citationNum}]`}
                    >
                        [{citationNum}]
                    </button>
                );
            }
            return <span key={idx}>{part}</span>;
        });
    };

    if (!data) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="text-center">
                    <p className="text-gray-600 mb-4">No survey data found</p>
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
                    <h1 className="text-3xl font-bold mb-2">Literature Survey</h1>
                    <p className="text-gray-300">Topic: {data.topic}</p>
                    <p className="text-sm text-gray-400 mt-1">
                        Generated on {new Date(data.generated_at).toLocaleString()} • {data.papers_used.length} papers • {data.references.length} references
                    </p>
                </div>
            </header>

            <main className="academic-container">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Survey Content (2/3 width) */}
                    <div className="lg:col-span-2 space-y-8">
                        {/* Abstract/Overview */}
                        <div className="academic-card">
                            <div className="bg-blue-50 border-l-4 border-academic-blue p-4 mb-4">
                                <p className="text-sm font-semibold text-academic-blue">
                                    📋 Citation-Grounded Survey
                                </p>
                                <p className="text-xs text-gray-700 mt-1">
                                    All claims are backed by references. Click citations to view source papers.
                                </p>
                            </div>

                            <div className="text-sm text-gray-600 space-y-2">
                                <p><strong>Topic:</strong> {data.topic}</p>
                                <p><strong>Papers Analyzed:</strong> {data.papers_used.length}</p>
                                <p><strong>Sections:</strong> {data.sections.length}</p>
                                <p><strong>Total References:</strong> {data.references.length}</p>
                            </div>
                        </div>

                        {/* Survey Sections */}
                        {data.sections.map((section, idx) => (
                            <div key={idx} className="academic-card">
                                <h2 className="section-heading">{section.title}</h2>
                                <div className="survey-content">
                                    <p>{renderContentWithCitations(section.content)}</p>
                                </div>
                            </div>
                        ))}

                        {/* Download Options */}
                        <div className="academic-card">
                            <h3 className="font-bold text-gray-800 mb-3">Export Survey</h3>
                            <div className="flex gap-3">
                                <button
                                    onClick={() => {
                                        const text = data.sections.map(s => `${s.title}\n\n${s.content}\n\n`).join('\n') +
                                            '\nReferences:\n' + data.references.map(r => r.formatted_reference).join('\n');
                                        const blob = new Blob([text], { type: 'text/plain' });
                                        const url = URL.createObjectURL(blob);
                                        const a = document.createElement('a');
                                        a.href = url;
                                        a.download = `survey_${data.topic.replace(/\s+/g, '_')}.txt`;
                                        a.click();
                                    }}
                                    className="academic-button text-sm py-2 px-4"
                                >
                                    📄 Download as Text
                                </button>
                                <button
                                    onClick={() => {
                                        const json = JSON.stringify(data, null, 2);
                                        const blob = new Blob([json], { type: 'application/json' });
                                        const url = URL.createObjectURL(blob);
                                        const a = document.createElement('a');
                                        a.href = url;
                                        a.download = `survey_${data.topic.replace(/\s+/g, '_')}.json`;
                                        a.click();
                                    }}
                                    className="academic-button text-sm py-2 px-4 bg-gray-700 hover:bg-gray-800"
                                >
                                    💾 Download as JSON
                                </button>
                            </div>
                        </div>
                    </div>

                    {/* References Sidebar (1/3 width) */}
                    <div className="lg:col-span-1">
                        <div className="sticky top-4">
                            <CitationViewer citations={data.references} />

                            {/* Papers Used */}
                            <div className="academic-card mt-4">
                                <h3 className="font-bold text-gray-800 mb-3">Papers Analyzed</h3>
                                <div className="space-y-2 max-h-96 overflow-y-auto">
                                    {data.papers_used.slice(0, 10).map((paper) => (
                                        <div key={paper.paper_id} className="text-xs border-b border-gray-100 pb-2">
                                            <p className="font-semibold text-gray-800">{paper.title}</p>
                                            <p className="text-gray-600">
                                                {paper.authors.slice(0, 2).map(a => a.name).join(', ')} ({paper.year})
                                            </p>
                                        </div>
                                    ))}
                                    {data.papers_used.length > 10 && (
                                        <p className="text-gray-500 italic">
                                            ...and {data.papers_used.length - 10} more papers
                                        </p>
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className="mt-16 py-8 border-t border-gray-200 bg-white">
                <div className="academic-container text-center text-sm text-gray-600">
                    <p className="font-semibold">Academic Positioning</p>
                    <p className="mt-2 max-w-3xl mx-auto">
                        "A citation-grounded AI-assisted literature survey system that improves trust and verifiability in academic writing."
                    </p>
                    <p className="mt-4 text-xs text-gray-500">
                        This is NOT a replacement for human researchers. It is an academic writing assistant focused on correctness and verifiability.
                    </p>
                </div>
            </footer>
        </div>
    );
}
