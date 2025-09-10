from fastapi import APIRouter, HTTPException
from ..pm_client import fetch_internships, get_internship, apply_to_internship
from ..services.embeddings_recommender import EmbeddingsRecommender
router = APIRouter(prefix="/api/internships")
rec = EmbeddingsRecommender()
try:
    rec.load_index()
    print('Embeddings index loaded')
except Exception as e:
    print('No embeddings index on startup:', e)
@router.get('/')
def list_internships(q: str = None):
    try:
        return {'data': fetch_internships({'q':q} if q else {})}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@router.get('/{internship_id}')
def get_item(internship_id: str):
    try:
        return get_internship(internship_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
@router.post('/recommend')
def recommend(payload: dict):
    q = payload.get('query_text') or payload.get('skills') or ''
    if not q:
        return {'recommendations': []}
    try:
        results = rec.query(q, top_k=20)
        if results:
            return {'method':'embeddings','recommendations': results}
    except Exception as e:
        print('Embeddings failed:', e)
    # fallback: simple keyword match
    all_items = fetch_internships({})
    ql = q.lower()
    scored = []
    for it in all_items:
        txt = (it.get('title','')+' '+it.get('description','')+' '+it.get('required_skills','')).lower()
        score = 1.0 if all([w in txt for w in ql.split()]) else 0.0
        scored.append({**it,'score':score})
    scored.sort(key=lambda x: x['score'], reverse=True)
    return {'method':'fallback','recommendations': scored[:20]}
@router.post('/{internship_id}/apply')
def apply(internship_id: str, payload: dict):
    resp = apply_to_internship(internship_id, payload)
    return {'success': True, 'pmis': resp}
