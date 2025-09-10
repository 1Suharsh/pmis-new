import os, json, numpy as np
from pathlib import Path
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
OPENAI_KEY = os.getenv('OPENAI_API_KEY')
EMBED_MODEL = os.getenv('EMBEDDING_MODEL','text-embedding-3-small')
DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
DATA_DIR.mkdir(exist_ok=True)
EMB_FILE = DATA_DIR / 'embeddings.npy'
META_FILE = DATA_DIR / 'meta.json'
class Recommender:
    def __init__(self):
        self.method = 'tfidf'
        self.meta = []
        self.embs = None
        # try load cached embeddings
        if EMB_FILE.exists() and META_FILE.exists() and OPENAI_KEY:
            try:
                self.embs = np.load(str(EMB_FILE))
                with open(META_FILE,'r',encoding='utf-8') as f:
                    self.meta = json.load(f)
                self.method = 'openai_emb'
            except Exception as e:
                print('could not load embeddings:', e)
        if not self.meta:
            sample = Path(__file__).resolve().parents[1] / 'sample_data' / 'internships.json'
            with open(sample,'r',encoding='utf-8') as f:
                items = json.load(f)
            for it in items:
                it['combined_text'] = f"{it.get('title','')} . {it.get('company','')} . {it.get('description','')} . skills: {it.get('required_skills','')}"
            self.meta = items
    def recommend(self, query, top_k=10):
        # OpenAI embeddings path
        if self.method == 'openai_emb' and self.embs is not None and OPENAI_KEY:
            try:
                import openai
                openai.api_key = OPENAI_KEY
                resp = openai.Embedding.create(input=[query], model=EMBED_MODEL)
                q_emb = np.array(resp['data'][0]['embedding'], dtype='float32').reshape(1, -1)
                sims = cosine_similarity(q_emb, self.embs)[0]
                idxs = sims.argsort()[::-1][:top_k]
                results = []
                for idx in idxs:
                    item = dict(self.meta[int(idx)])
                    item['score'] = float(sims[int(idx)])
                    results.append(item)
                return results
            except Exception as e:
                print('openai failed, falling back to tfidf:', e)
        # TF-IDF fallback
        texts = [m.get('combined_text','') for m in self.meta]
        v = TfidfVectorizer(ngram_range=(1,2), max_features=2000)
        mat = v.fit_transform(texts + [query]).toarray()
        qv = mat[-1:]
        tv = mat[:-1]
        sims = cosine_similarity(qv, tv)[0]
        idxs = sims.argsort()[::-1][:top_k]
        res = []
        for idx in idxs:
            item = dict(self.meta[int(idx)])
            item['score'] = float(sims[int(idx)])
            res.append(item)
        return res
