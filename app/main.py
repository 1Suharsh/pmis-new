from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import internships
from . import models
from .db import engine, Base
import os
Base.metadata.create_all(bind=engine)
app = FastAPI(title='PMIS AI Internship Engine (Optimized)')
app.include_router(internships.router)
# Serve frontend build if present
frontend_build = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build')
if os.path.exists(frontend_build):
    app.mount('/', StaticFiles(directory=frontend_build, html=True), name='frontend')
@app.get('/health')
def health():
    return {'status':'ok'}
