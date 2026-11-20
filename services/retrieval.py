import json
import re
from pathlib import Path
import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

# Paths relative to project root
ROOT_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT_DIR / "models" / "multilingual_minilm"
DATA_PATH = ROOT_DIR / "data" / "processed" / "kau_crop_chunks.json"
EMBEDDINGS_PATH = ROOT_DIR / "data" / "processed" / "kau_embeddings.npy"
MODEL_PATH = MODEL_DIR / "onnx" / "model_quint8_avx2.onnx"

# Load data once at import time
with open(DATA_PATH, encoding="utf-8") as f:
    _documents = json.load(f)
_embeddings = np.load(EMBEDDINGS_PATH)

# Load tokenizer and ONNX model
_tokenizer = Tokenizer.from_file(str(MODEL_DIR / "tokenizer.json"))
_tokenizer.enable_truncation(max_length=128)
_tokenizer.enable_padding()

_session = ort.InferenceSession(str(MODEL_PATH), providers=["CPUExecutionProvider"])

# Broad agricultural crop dictionary
KNOWN_CROPS = {
    "apple": ["apple", "apples", "ആപ്പിൾ"],
    "banana": ["banana", "bananas", "വാഴ", "nendran", "robusta", "plantain", "musa", "poovan", "palayankodan"],
    "rice": ["rice", "paddy", "നെല്ല്", "pokkali", "kaipad", "uma", "jyothi", "kuttanad"],
    "coconut": ["coconut", "coconuts", "തെങ്ങ്", "palm", "copra", "neera", "keram"],
    "pepper": ["pepper", "black pepper", "കുരുമുളക്", "piper"],
    "tomato": ["tomato", "tomatoes", "തക്കാളി"],
    "potato": ["potato", "potatoes", "ഉരുളക്കിഴങ്ങ്"],
    "cardamom": ["cardamom", "ഏലം"],
    "rubber": ["rubber", "റബ്ബർ"],
    "mango": ["mango", "mangoes", "മാവ്", "മാങ്ങ"],
    "ginger": ["ginger", "ഇഞ്ചി"],
    "turmeric": ["turmeric", "മഞ്ഞൾ"],
    "cashew": ["cashew", "കശുവണ്ടി", "കശുമാവ്"],
    "coffee": ["coffee", "കാപ്പി"],
    "tea": ["tea", "തേയില"],
    "tapioca": ["tapioca", "cassava", "കപ്പ"]
}

def detect_crop_from_query(query: str, fallback_crop: str = "Paddy") -> str:
    """Detect crop entity from user question. If user asks about apple, returns apple, not fallback."""
    q_lower = query.lower()
    
    # Check known crops first
    for crop_name, keywords in KNOWN_CROPS.items():
        for kw in keywords:
            # Word boundary matching to avoid false substring triggers
            if re.search(r'\b' + re.escape(kw) + r'\b', q_lower):
                return crop_name
    
    # Check if fallback crop matches
    fb = fallback_crop.lower()
    for crop_name, keywords in KNOWN_CROPS.items():
        if crop_name in fb:
            return crop_name
        for kw in keywords:
            if kw in fb:
                return crop_name
                
    return fallback_crop.lower()

def _encode_query(query: str) -> np.ndarray:
    """Encode a query string to a normalized 384‑dim vector using the ONNX model."""
    encoding = _tokenizer.encode(query)
    inputs = {
        "input_ids": np.array([encoding.ids], dtype=np.int64),
        "attention_mask": np.array([encoding.attention_mask], dtype=np.int64),
        "token_type_ids": np.array([encoding.type_ids], dtype=np.int64),
    }
    token_embeddings = _session.run(None, inputs)[0]
    mask = inputs["attention_mask"][..., None]
    pooled = np.sum(token_embeddings * mask, axis=1) / np.maximum(np.sum(mask, axis=1), 1)
    norm = np.linalg.norm(pooled, axis=1, keepdims=True)
    norm = np.maximum(norm, 1e-12)
    pooled = pooled / norm
    return pooled[0].astype(np.float32)

def search(query: str, crop: str = "rice", top_k: int = 4):
    """Return the top‑k most similar chunks for *query*.
    Intelligently identifies crop from query and retrieves matching corpus.
    """
    effective_crop = detect_crop_from_query(query, fallback_crop=crop)
    query_vec = _encode_query(query)
    
    # Check if effective_crop has direct documents in KAU
    crop_indices = [i for i, doc in enumerate(_documents) if doc.get("crop", "").lower() == effective_crop]
    
    # If crop is not in KAU 3-crop sub-dataset (e.g. apple, tomato, pepper), search across entire KAU corpus for semantic matches (nutrition/soil/pest)
    is_external_crop = False
    if not crop_indices:
        crop_indices = list(range(len(_documents)))
        is_external_crop = True
        
    sims = _embeddings[crop_indices] @ query_vec
    top_idxs = np.argsort(sims)[::-1][:top_k]
    
    results = []
    for rank, idx in enumerate(top_idxs, start=1):
        doc_idx = crop_indices[idx]
        doc = _documents[doc_idx]
        results.append(
            {
                "rank": rank,
                "similarity": float(sims[idx]),
                "crop": doc.get("crop"),
                "pdf_page": doc.get("pdf_page"),
                "chunk_id": doc.get("chunk_id"),
                "text": doc.get("text", "").strip(),
                "is_external_crop": is_external_crop
            }
        )
    return results, effective_crop
