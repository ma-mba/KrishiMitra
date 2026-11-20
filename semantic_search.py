
import json
from pathlib import Path

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

MODEL_DIR = Path("models/multilingual_minilm")
MODEL_PATH = MODEL_DIR / "onnx" / "model_quint8_avx2.onnx"

DATA_PATH = Path("data/processed/kau_crop_chunks.json")
EMBEDDINGS_PATH = Path("data/processed/kau_embeddings.npy")

with open(DATA_PATH, encoding="utf-8") as f:
    documents = json.load(f)

embeddings = np.load(EMBEDDINGS_PATH)

assert embeddings.shape == (len(documents), 384), (
    "Embedding shape does not match the dataset."
)

tokenizer = Tokenizer.from_file(
    str(MODEL_DIR / "tokenizer.json")
)

tokenizer.enable_truncation(max_length=128)
tokenizer.enable_padding()

session = ort.InferenceSession(
    str(MODEL_PATH),
    providers=["CPUExecutionProvider"]
)

def encode_query(query):
    encoding = tokenizer.encode(query)

    inputs = {
        "input_ids": np.array(
            [encoding.ids], dtype=np.int64
        ),
        "attention_mask": np.array(
            [encoding.attention_mask], dtype=np.int64
        ),
        "token_type_ids": np.array(
            [encoding.type_ids], dtype=np.int64
        )
    }

    token_embeddings = session.run(None, inputs)[0]

    mask = inputs["attention_mask"][..., None]

    pooled = (
        np.sum(token_embeddings * mask, axis=1)
        / np.maximum(np.sum(mask, axis=1), 1)
    )

    pooled /= np.maximum(
        np.linalg.norm(pooled, axis=1, keepdims=True),
        1e-12
    )

    return pooled[0].astype(np.float32)


def search(query, crop, top_k=5):
    query_vector = encode_query(query)

    # Crop filtering
    indices = [
        i for i, doc in enumerate(documents)
        if doc["crop"] == crop
    ]

    if not indices:
        print("No documents found for this crop.")
        return

    # Cosine similarity because vectors are normalized
    similarities = embeddings[indices] @ query_vector

    ranked = np.argsort(similarities)[::-1][:top_k]

    print("\nQUESTION:", query)
    print("CROP:", crop)
    print("=" * 60)

    for rank, position in enumerate(ranked, start=1):
        doc = documents[indices[position]]

        print(f"\nRESULT {rank}")
        print("Similarity:", round(float(similarities[position]), 4))
        print("PDF page:", doc["pdf_page"])
        print("Chunk:", doc["chunk_id"])
        print("Text:")
        print(doc["text"][:700])
        print("-" * 60)


if __name__ == "__main__":
    crop = input(
        "Select crop (rice/banana/coconut): "
    ).strip().lower()

    if crop not in {"rice", "banana", "coconut"}:
        print("Invalid crop.")
    else:
        query = input(
            "Ask an agricultural question: "
        ).strip()

        if not query:
            print("Question cannot be empty.")
        else:
            search(query, crop)
r