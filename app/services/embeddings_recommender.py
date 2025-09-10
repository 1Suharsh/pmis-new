import os, json, numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
try:
    import faiss
    _HAS_FAISS = True
except Exception:
    _HAS_FAISS = False
    from sklearn.neighbors import NearestNeighbors
MODEL = os.getenv('EMBEDDING_MODEL','all-MiniLM-L6-v2')
INDEX_DIR = os.getenv('EMBEDDING_INDEX_DIR','/app/data/emb_index')
Path(INDEX_DIR).mkdir(parents=True, exist_ok=True)
class EmbeddingsRecommender:
    def __init__(self, model_name=MODEL, use_faiss=True):
        self.model = SentenceTransformer(model_name)
        self.use_faiss = use_faiss and _HAS_FAISS
        self.index = None
        self.meta = []
        self.embeddings = None
    def embed_texts(self, texts):
        embs = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        if embs.dtype != np.float32: embs = embs.astype('float32')
        return embs
    def build_index(self, items, text_key='combined_text'):
        texts = [item.get(text_key,'') for item in items]
        if not texts:
            self.meta = items; self.embeddings = np.zeros((0,self.model.get_sentence_embedding_dimension()),dtype='float32'); return
        embs = self.embed_texts(texts)
        self.embeddings = embs; self.meta = items
        dim = embs.shape[1]
        if self.use_faiss:
            index = faiss.IndexFlatIP(dim); faiss.normalize_L2(embs); index.add(embs); self.index=index
        else:
            self.index = NearestNeighbors(n_neighbors=min(10,len(embs)), metric='cosine'); self.index.fit(embs)
        self.save_index()
    def save_index(self):
        meta_path = Path(INDEX_DIR)/'meta.json'; emb_path = Path(INDEX_DIR)/'embeddings.npy'
        meta_path.write_text(json.dumps(self.meta, ensure_ascii=False))
        np.save(emb_path, self.embeddings)
        if self.use_faiss and hasattr(self,'index') and self.index is not None:
            faiss.write_index(self.index, str(Path(INDEX_DIR)/'faiss_index.idx'))
    def load_index(self):
        meta_path = Path(INDEX_DIR)/'meta.json'; emb_path = Path(INDEX_DIR)/'embeddings.npy'; faiss_path = Path(INDEX_DIR)/'faiss_index.idx'
        if not meta_path.exists() or not emb_path.exists():
            raise FileNotFoundError('Index not found')
        self.meta = json.loads(meta_path.read_text()); self.embeddings = np.load(emb_path)
        if self.use_faiss and faiss_path.exists():
            self.index = faiss.read_index(str(faiss_path))
        else:
            self.index = NearestNeighbors(n_neighbors=min(10,len(self.embeddings)), metric='cosine'); self.index.fit(self.embeddings)
    def query(self, query_text, top_k=10):
        q_emb = self.embed_texts([query_text])
        results = []
        if self.use_faiss and self.index is not None:
            faiss.normalize_L2(q_emb); D,I = self.index.search(q_emb, top_k)
            for score, idx in zip(D[0].tolist(), I[0].tolist()):
                if idx<0 or idx>=len(self.meta): continue
                item = dict(self.meta[idx]); item['score']=float(score); results.append(item)
            return results
        elif self.index is not None:
            distances, indices = self.index.kneighbors(q_emb, n_neighbors=top_k)
            for dist, idx in zip(distances[0].tolist(), indices[0].tolist()):
                sim = 1.0 - dist; item = dict(self.meta[idx]); item['score']=float(sim); results.append(item)
            return results
        else:
            return []
