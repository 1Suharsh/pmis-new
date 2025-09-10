# Build embeddings for internships using OpenAI and save to data/ (optional)
import os, json, numpy as np
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
MODEL = os.getenv('EMBEDDING_MODEL','text-embedding-3-small')
if not OPENAI_KEY:
    print('OPENAI_API_KEY not found. Exiting.')
    raise SystemExit(1)
import openai
openai.api_key = OPENAI_KEY
DATA = Path(__file__).resolve().parents[1] / 'sample_data' / 'internships.json'
OUT = Path(__file__).resolve().parents[1] / 'data'
OUT.mkdir(exist_ok=True)
with open(DATA,'r',encoding='utf-8') as f:
    items = json.load(f)
texts = []
for it in items:
    it['combined_text'] = f"{it.get('title','')} . {it.get('company','')} . {it.get('description','')} . skills: {it.get('required_skills','')}"
    texts.append(it['combined_text'])
all_embs = []
BATCH = 16
for i in range(0, len(texts), BATCH):
    chunk = texts[i:i+BATCH]
    resp = openai.Embedding.create(input=chunk, model=MODEL)
    for d in resp['data']:
        all_embs.append(d['embedding'])
arr = np.array(all_embs, dtype='float32')
np.save(OUT / 'embeddings.npy', arr)
with open(OUT / 'meta.json','w',encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False)
print('Embeddings saved to data/')
