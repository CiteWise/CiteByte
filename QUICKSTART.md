# Quick Start Guide

## Prerequisites Check

Before running the system, ensure you have:

- [ ] Python 3.9 or higher installed
- [ ] Node.js 18 or higher installed
- [ ] pip and npm/yarn available

## Step-by-Step Setup

### 1. Backend Setup (5 minutes)

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Verify installation
python -c "import fastapi; import uvicorn; print('✅ Dependencies installed')"

# Run backend server
python main.py
```

Expected output:
```
✅ Database initialized
✅ Using mock APIs: True
✅ Using mock LLM: True
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Leave this terminal running**

### 2. Frontend Setup (5 minutes)

Open a **new terminal** window:

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Run development server
npm run dev
```

Expected output:
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
- Local:        http://localhost:3000
```

**Leave this terminal running**

### 3. Access the Application

Open your browser and go to: **http://localhost:3000**

## Example Usage

### Test Topic 1: Transformer Models

1. Enter topic: `Transformer models in natural language processing`
2. Select domain: `Artificial Intelligence`
3. Click **"1. Search & Rank Papers"**
   - View 20+ ranked papers
   - See BM25 scores
   - Top 5 papers highlighted
4. Return home and click **"2. Generate Full Survey"**
   - View structured survey
   - Click citations to see references
   - Export as text or JSON

### Test Topic 2: Cybersecurity

1. Enter topic: `Deep learning for intrusion detection systems`
2. Select domain: `Cybersecurity`
3. Generate survey
4. Verify all claims have citations

## Troubleshooting

### Backend Issues

**Error: Module not found**
```bash
pip install -r requirements.txt --force-reinstall
```

**Error: Database locked**
```bash
# Delete database and restart
rm literature_survey.db
python main.py
```

**Port 8000 already in use**
```bash
# Kill process on port 8000 (Windows)
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port
uvicorn main:app --port 8001
```

### Frontend Issues

**npm install fails**
```bash
# Clear cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Port 3000 already in use**
```bash
# Use different port
npm run dev -- -p 3001
```

**CORS errors**
- Ensure backend is running on port 8000
- Check browser console for error details
- Verify CORS middleware in backend/main.py

### Connection Issues

**Frontend can't reach backend**

1. Check backend is running: `http://localhost:8000`
2. Check backend health: `http://localhost:8000/api/health`
3. Verify CORS settings allow localhost:3000

## Verification Checklist

After setup, verify:

- [ ] Backend responds at http://localhost:8000
- [ ] Backend health check returns `{"status": "healthy"}`
- [ ] Frontend loads at http://localhost:3000
- [ ] Can enter topic and see form
- [ ] Search button triggers API call
- [ ] Papers page displays results
- [ ] Survey generation works
- [ ] Citations are clickable
- [ ] Can export survey

## Next Steps

Once running:

1. Try multiple research topics
2. Examine the generated surveys
3. Verify citation traceability
4. Review code structure
5. Prepare for viva/presentation

## Environment Variables (Optional)

The system works out-of-the-box with defaults. To customize:

1. Copy `.env.example` to `.env` (if needed)
2. Edit values in `.env`
3. Restart backend

Default: Mock mode (no API keys needed)

## Getting Help

- Check `README.md` in root folder
- Review `backend/README.md` for API details
- Review `frontend/README.md` for UI details
- Check browser console for frontend errors
- Check terminal output for backend errors
