from fastapi import APIRouter, HTTPException, Request
from .pm_client import fetch_internships, get_internship, apply_to_internship
from .recommender import Recommender
router = APIRouter()
rec = Recommender()
@router.get('/api/internships')
def list_internships(q: str = None):
    try:
        return {'data': fetch_internships({'q':q} if q else {})}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get('/api/internships/{internship_id}')
def get_item(internship_id: str):
    try:
        return get_internship(internship_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
@router.post('/api/internships/recommend')
async def recommend(request: Request):
    payload = await request.json()
    q = payload.get('query_text') or payload.get('skills') or ''
    if not q:
        return {'recommendations': []}
    try:
        results = rec.recommend(q, top_k=15)
        return {'method': rec.method, 'recommendations': results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.post('/api/internships/{internship_id}/apply')
def apply_route(internship_id: str, payload: dict):
    res = apply_to_internship(internship_id, payload)
    return {'success': True, 'pmis': res}
