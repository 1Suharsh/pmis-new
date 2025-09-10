import json
from pathlib import Path
SAMPLE = Path(__file__).resolve().parents[1] / 'sample_data' / 'internships.json'

def fetch_internships(params=None):
    params = params or {}
    with open(SAMPLE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    q = params.get('q')
    if q:
        ql = q.lower()
        data = [d for d in data if ql in (d.get('title','')+' '+d.get('description','')+' '+d.get('required_skills','')).lower()]
    return data

def get_internship(internship_id):
    with open(SAMPLE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for d in data:
        if str(d.get('id')) == str(internship_id):
            return d
    raise Exception('Not found')

def apply_to_internship(internship_id, payload):
    return {'internship_id': internship_id, 'status': 'applied', 'applicant': payload}
