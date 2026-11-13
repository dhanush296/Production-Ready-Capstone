# LaunchPad Internship Portal
A full-stack capstone starter: React + Vite frontend, FastAPI + SQLite backend, internship search/filter, saved listings, listing submission, health checks, request logging, tests, responsive UI and Docker.

## Run
Backend (Python 3.11+):
```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Frontend (Node 20+), new terminal:
```bash
cd frontend
npm install
npm run dev
```
Open http://localhost:5173. API docs: http://localhost:8000/docs. Health: http://localhost:8000/api/health.

## Tests
```bash
cd backend
pytest -q
```

## API contract
- GET `/api/health`
- GET `/api/internships?q=&location=&mode=`
- POST `/api/internships`

## Engineering decisions
- React/Vite: component UI and quick developer feedback.
- FastAPI/Pydantic: typed validation and automatic OpenAPI docs.
- SQLite: zero-configuration persistence for a student capstone; migrate to managed PostgreSQL for production.
- localStorage: saved roles work without account infrastructure; move to user-linked DB records when authentication exists.
- Environment-based API URL and CORS allowlist simplify deployment configuration.
- Request logs capture method, path, status and duration; health check verifies DB connectivity.
- Semantic controls, visible focus, responsive breakpoints and reduced-motion support improve accessibility.

## Docker
From root: `docker compose up --build`. Web at http://localhost:8080; API at http://localhost:8000.

## Deploy and submit
Deploy backend to a Python host and frontend to a static host. Set `CORS_ORIGINS` to the exact deployed frontend origin and `VITE_API_URL` to the deployed API. Use persistent managed PostgreSQL for real production. Verify HTTPS, health, search and listing creation.
Before submitting, add live app URL, GitHub URL, genuine test output, accessibility/performance/security evidence and optional two-minute walkthrough link. Do not claim deployment or audit results until completed.
