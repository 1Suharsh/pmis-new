from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routes import router as api_router
import os
app = FastAPI(title='PMIS Hybrid Recommender')
app.include_router(api_router)
# mount frontend if exists
frontend = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build')
if os.path.exists(frontend):
    app.mount('/', StaticFiles(directory=frontend, html=True), name='frontend')
@app.get('/health')
def health():
    return {'status':'ok'}
