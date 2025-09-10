PMIS Internship Recommendation — Hybrid OpenAI + TF-IDF Backend
================================================================

This repository contains a FastAPI backend that serves a provided static UI and offers internship recommendations.

Features:
- Uses OpenAI Embeddings (text-embedding-3-small) if OPENAI_API_KEY is set and embeddings are built.
- Falls back to TF-IDF + cosine similarity if OpenAI key is not set or embeddings aren't built.
- Endpoints:
  - GET /api/internships
  - POST /api/internships/recommend  (JSON: {"query_text":"Python, ML"})
  - POST /api/internships/{id}/apply
  - GET /health

Quick start (local):
1. python -m venv venv && source venv/bin/activate
2. pip install -r requirements.txt
3. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Using OpenAI embeddings (optional, recommended for quality):
1. Set OPENAI_API_KEY in your environment.
2. python scripts/build_embeddings.py  # will call OpenAI to get embeddings for internships
3. Restart the server. /api/internships/recommend will now use OpenAI embeddings.

Deploy on Render:
1. Push this repo to GitHub.
2. Create a Web Service on Render, select Docker, connect repo and deploy.
3. In Render dashboard set environment variable OPENAI_API_KEY (do NOT commit it to GitHub).
4. (Optional) After deploy, use Render Shell to run: python scripts/build_embeddings.py

Notes:
- OpenAI usage consumes credits. The script batches embeddings to minimize requests.
- The TF-IDF fallback ensures the service works without OpenAI.
