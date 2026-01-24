'use client';

import { useState } from 'react';

interface Citation {
    number: number;
    paper_id: string;
    formatted_reference: string;
}

interface CitationViewerProps {
    citations: Citation[];
}

export default function CitationViewer({ citations }: CitationViewerProps) {
    const [selectedCitation, setSelectedCitation] = useState<number | null>(null);

    return (
        <div className="academic-card">
            <h2 className="section-heading">References</h2>

            <div className="reference-list">
                {citations.map((citation) => (
                    <div
                        key={citation.number}
                        id={`ref-${citation.number}`}
                        className={`reference-item cursor-pointer ${selectedCitation === citation.number ? 'bg-yellow-100' : ''
                            }`}
                        onClick={() => setSelectedCitation(citation.number)}
                        onMouseEnter={() => setSelectedCitation(citation.number)}
                        onMouseLeave={() => setSelectedCitation(null)}
                    >
                        <div className="text-gray-800 font-serif">
                            {citation.formatted_reference}
                        </div>
                        {selectedCitation === citation.number && (
                            <div className="text-xs text-gray-500 mt-1">
                                Paper ID: {citation.paper_id}
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {citations.length === 0 && (
                <p className="text-gray-500 italic">No references found</p>
            )}
        </div>
    );
}
