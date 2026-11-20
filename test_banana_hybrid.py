
import json
import re
from pathlib import Path

import numpy as np
import onnxruntime as ort
from rank_bm25 import BM25Okapi
from tokenizers import Tokenizer


# ==========================================
# 1. FILE PATHS
# ==========================================

MODEL_DIR = Path("models/multilingual_minilm")

CHUNKS_PATH = Path(
    "data/processed/banana_chunks_v2.json"
)

EMBEDDINGS_PATH = Path(
    "data/processed/banana_embeddings_v2.npy"
)

ONNX_PATH = (
    MODEL_DIR / "onnx/model_quint8_avx2.onnx"
)


# ==========================================
# 2. LOAD CHUNKS AND EMBEDDINGS
# ==========================================

with open(CHUNKS_PATH, encoding="utf-8") as f:
    chunks = json.load(f)

embeddings = np.load(EMBEDDINGS_PATH)

assert len(chunks) == len(embeddings), (
    "Chunk count and embedding count do not match"
)

print("Loaded chunks:", len(chunks))
print("Embedding shape:", embeddings.shape)


# ==========================================
# 3. LOAD TOKENIZER AND ONNX MODEL
# ==========================================

tokenizer = Tokenizer.from_file(
    str(MODEL_DIR / "tokenizer.json")
)

tokenizer.enable_truncation(max_length=128)

tokenizer.enable_padding(
    pad_id=0,
    pad_token="[PAD]"
)

session = ort.InferenceSession(
    str(ONNX_PATH),
    sess_options=ort.SessionOptions(),
    providers=["CPUExecutionProvider"]
)

print("ONNX model loaded successfully")


# ==========================================
# 4. QUERY EMBEDDING FUNCTION
# ==========================================

def embed_query(text):
    encoded = tokenizer.encode(text)

    input_ids = np.array(
        [encoded.ids],
        dtype=np.int64
    )

    attention_mask = np.array(
        [encoded.attention_mask],
        dtype=np.int64
    )

    feeds = {
        "input_ids": input_ids,
        "attention_mask": attention_mask,
        "token_type_ids": np.zeros_like(input_ids)
    }

    token_embeddings = session.run(None, feeds)[0]

    # Mean pooling
    mask = attention_mask[:, :, None].astype(np.float32)

    pooled = (
        (token_embeddings * mask).sum(axis=1)
        / np.maximum(mask.sum(axis=1), 1e-9)
    )

    # L2 normalization
    norm = np.linalg.norm(
        pooled,
        axis=1,
        keepdims=True
    )

    normalized = pooled / np.maximum(norm, 1e-12)

    return normalized[0].astype(np.float32)


# ==========================================
# 5. BM25 TOKENIZATION
# ==========================================

def tokenize(text):
    return re.findall(
        r"\b\w+\b",
        text.lower()
    )


tokenized_documents = [
    tokenize(chunk["text"])
    for chunk in chunks
]

bm25 = BM25Okapi(tokenized_documents)


# ==========================================
# 6. HYBRID RETRIEVAL USING RRF
# ==========================================

def hybrid_search(query, k=60):

    # Semantic similarity
    query_vector = embed_query(query)

    semantic_scores = embeddings @ query_vector

    semantic_order = np.argsort(
        semantic_scores
    )[::-1]

    # BM25 keyword similarity
    bm25_scores = bm25.get_scores(
        tokenize(query)
    )

    bm25_order = np.argsort(
        bm25_scores
    )[::-1]

    # Reciprocal Rank Fusion
    combined_scores = np.zeros(
        len(chunks),
        dtype=np.float64
    )

    for rank, index in enumerate(
        semantic_order,
        start=1
    ):
        combined_scores[index] += 1 / (k + rank)

    for rank, index in enumerate(
        bm25_order,
        start=1
    ):
        combined_scores[index] += 1 / (k + rank)

    final_order = np.argsort(
        combined_scores
    )[::-1]

    return final_order, combined_scores


# ==========================================
# 7. TEST QUESTIONS
# ==========================================

tests = [
    {
        "question": (
            "My banana leaves have brown streaks "
            "and the youngest leaf is dying."
        ),
        "expected": "banana_section_003_part_2"
    },
    {
        "question": (
            "My banana leaves are losing colour "
            "in patches and look striped."
        ),
        "expected": "banana_section_002_part_2"
    },
    {
        "question": (
            "How does banana streak disease spread?"
        ),
        "expected": "banana_section_003_part_1"
    }
]


# ==========================================
# 8. EVALUATE RETRIEVAL
# ==========================================

passed = 0

for test in tests:

    question = test["question"]
    expected = test["expected"]

    ranked, scores = hybrid_search(question)

    top_id = chunks[int(ranked[0])]["chunk_id"]

    success = top_id == expected

    if success:
        passed += 1

    print("\n" + "=" * 65)
    print("Question:", question)
    print("Expected:", expected)
    print("Top-1 correct:", success)

    for rank, index in enumerate(
        ranked[:5],
        start=1
    ):
        index = int(index)
        chunk = chunks[index]

        print(
            f"\nRank {rank} | "
            f"RRF Score: {scores[index]:.6f}"
        )

        print("ID:", chunk["chunk_id"])
        print("Heading:", chunk["section_heading"])

    print("-" * 65)


# ==========================================
# 9. FINAL RESULTS
# ==========================================

print("\n" + "=" * 65)

print(
    f"HYBRID TOP-1 ACCURACY: "
    f"{passed}/{len(tests)}"
)

print(
    f"Accuracy percentage: "
    f"{passed / len(tests) * 100:.2f}%"
)

print("=" * 65)
