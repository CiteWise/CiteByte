# Literature Survey System - Frontend

Modern academic interface for literature survey generation and display.

## Overview

Built with **Next.js 14** (App Router) and **TypeScript**. Features a clean, professional academic design focused on readability and usability.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS (academic theme)
- **HTTP Client**: Axios
- **State**: React hooks + sessionStorage

## Pages

### 1. Home (`/`)
- Research topic input form
- Engineering domain selection
- Two-phase workflow:
  - Search & rank papers
  - Generate complete survey

### 2. Papers (`/papers`)
- Displays BM25-ranked papers
- Shows metadata (authors, year, venue, citations)
- Highlights top papers used for full text analysis
- Visual ranking indicators

### 3. Survey (`/survey`)
- Structured survey sections
- Interactive citation links
- Reference list sidebar
- Export functionality (TXT, JSON)
- Citation traceability

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Run Development Server

```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### 3. Build for Production

```bash
npm run build
npm start
```

## Features

✅ **Academic Design** - Clean, professional, scholarly appearance  
✅ **Interactive Citations** - Click citations to view references  
✅ **Citation Traceability** - Map claims to source papers  
✅ **Responsive Layout** - Works on desktop and tablet  
✅ **Export Options** - Download survey as text or JSON  

## Design Principles

- **No Fancy Animations**: Focus on clarity and speed
- **Academic Typography**: Serif fonts for content, high contrast
- **Information Hierarchy**: Clear section organization
- **Professional Color Scheme**: Navy blue and gray palette
- **Accessibility**: Keyboard navigation, readable fonts

## API Integration

Frontend connects to backend at `http://localhost:8000`:

```typescript
POST /api/search          // Search and rank papers
POST /api/generate-survey // Generate full survey
GET  /api/papers/:id      // Get paper details
```

## Components

### `CitationViewer`
Interactive reference list with hover effects and click-to-highlight.

**Props:**
- `citations`: Array of Citation objects

## Future Enhancements

- PDF export with proper formatting
- Bookmarking and session management
- Advanced filtering and sorting
- Citation graph visualization
- Dark mode toggle
