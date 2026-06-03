# Fraudar — Real-Time Scam & Fraud Detection Platform

Online scams cost Americans $12.5 billion in 2025. The victims are elderly people, international students, immigrants, and first-time internet users. There is no free, accessible, real-time tool that anyone can use to check if something is a scam before they engage.

Fraudar fixes that.

Paste any suspicious URL, email, job posting, or message. Get back a scam probability score, specific red flags explained in plain English, and exactly what to do next — in seconds.

## Live Demo
**API Docs:** `http://<your-ec2-ip>:8000/docs`

## How It Works

When you submit something suspicious, Fraudar runs it through four layers:

1. **VirusTotal** — checks the URL against 70+ antivirus engines
2. **Google Safe Browsing** — cross-references Google's malware and phishing database
3. **RAG Pipeline** — searches ChromaDB for similar patterns from real FTC and FBI IC3 scam reports
4. **Claude AI** — reads the content and generates a scam probability score, red flags, and plain-English explanation

Results are processed asynchronously via Redis queues and Celery workers, so the API never blocks under load.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Python 3.11 |
| AI / LLM | Anthropic Claude |
| Vector Database | ChromaDB + sentence-transformers |
| Queue System | Redis + Celery |
| Frontend | React, TypeScript |
| Browser Extension | Chrome Extension (Manifest V3) |
| Deployment | AWS EC2, Docker, GitHub Actions CI/CD |
| External APIs | VirusTotal, Google Safe Browsing |

## Running Locally

### 1. Clone and set up
```bash
git clone https://github.com/SaiTejaAppani16/fraudar.git
cd fraudar
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Add your API keys
Create a `.env` file in the root:
```
ANTHROPIC_API_KEY=your_key
VIRUSTOTAL_API_KEY=your_key
GOOGLE_SAFE_BROWSING_API_KEY=your_key
REDIS_URL=redis://localhost:6379
DATABASE_URL=postgresql://postgres:password@localhost:5432/fraudar
```

### 3. Start the backend
```bash
uvicorn backend.main:app --reload
```

### 4. Start the Celery worker
```bash
celery -A backend.workers.celery_app worker --loglevel=info --pool=solo
```

### 5. Start the frontend
```bash
cd frontend
npm install
npm start
```

### Or run everything with Docker
```bash
docker-compose up --build
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | /api/v1/health | Health check |
| POST | /api/v1/analyze/url | Synchronous URL analysis |
| POST | /api/v1/analyze/text | Synchronous text analysis |
| POST | /api/v1/jobs/analyze/url | Submit URL job to queue |
| POST | /api/v1/jobs/analyze/text | Submit text job to queue |
| GET | /api/v1/jobs/{job_id} | Poll job result |

## Chrome Extension

The extension checks every website you visit in real time and shows a color-coded badge — green for safe, orange for suspicious, red for dangerous.

To install:
1. Go to `chrome://extensions`
2. Enable Developer Mode
3. Click Load Unpacked and select the `extension/` folder
4. Visit any website and watch Fraudar work

## Data Sources

All free and legal:
- FTC Consumer Sentinel Network — public government scam reports
- FBI IC3 Annual Reports — public cybercrime data
- VirusTotal — free tier, 500 requests per day
- Google Safe Browsing API — free

## About

Built by Sai Teja Appani — MS CS student at the University of Florida.
This project was built to solve a real problem that affects people I know personally — international students, immigrants, and elderly family members who fall for scams every day.

[GitHub](https://github.com/SaiTejaAppani16) | [LinkedIn](https://linkedin.com/in/your-profile)
# CI/CD test
