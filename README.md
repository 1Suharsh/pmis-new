PMIS Internship AI Recommendation - Optimized for Render
======================================================

This repository contains a production-ready full-stack app for SIH:
- FastAPI backend (AI recommender using Sentence-BERT + FAISS)
- Prebuilt React frontend (professional UI & branding)
- Mock PM Internship dataset (120 entries)
- Optimized Dockerfile for Render (serves prebuilt frontend)
- render.yaml for one-click Render deployment

Steps to deploy:
1. Upload this repository to GitHub (branch main).
2. On Render, create a new Web Service, connect GitHub repo, choose Docker environment, deploy.
3. After the service is live, run `python scripts/build_index.py` in Render shell to build embeddings (optional but recommended).

Local testing:
- Build and run Docker locally:
  docker build -t pmis-optimized .
  docker run -p 8000:8000 pmis-optimized
- Open http://localhost:8000

