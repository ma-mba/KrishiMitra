
import json
from pathlib import Path

import numpy as np
import onnxruntime as ort
from tokenizers import Tokenizer

DATA_PATH = Path("data/processed/kau_crop_chunks.json")
MODEL_DIR = Path("models/multilingual_minilm")
MODEL_PATH = MODEL_DIR / "onnx" / "model_quint8_avx2.onnx"
TOKENIZER_PATH = MODEL_DIR / "tokenizer.json"
OUTPUT_PATH = Path("data/processed/kau_embeddings.npy")

# Load crop-specific knowledge base
with open(DATA_PATH, encoding="utf-8") as f:
    documents = json.load(f)

# Load tokenizer without importing PyTorch
tokenizer = Tokenizer.from_file(str(TOKENIZER_PATH))
tokenizer.enable_truncation(max_length=128)
tokenizer.enable_padding()

# Load the AVX2 ONNX model
session = ort.InferenceSession(
    str(MODEL_PATH),
    providers=["CPUExecutionProvider"]
)

print("Model loaded successfully.")
print("Documents:", len(documents))

def encode_batch(texts):
    encodings = tokenizer.encode_batch(texts)

    inputs = {
        "input_ids": np.asarray(
            [e.ids for e in encodings],
            dtype=np.int64
        ),
        "attention_mask": np.asarray(
            [e.attention_mask for e in encodings],
            dtype=np.int64
        ),
        "token_type_ids": np.asarray(
            [e.type_ids for e in encodings],
            dtype=np.int64
        )
    }

    outputs = session.run(None, inputs)
    token_embeddings = outputs[0]

    # Attention-mask-aware mean pooling
    mask = inputs["attention_mask"][..., None]

    summed = np.sum(
        token_embeddings * mask,
        axis=1
    )

    counts = np.maximum(
        np.sum(mask, axis=1),
        1
    )

    sentence_embeddings = summed / counts

    # L2 normalization for cosine similarity
    norms = np.linalg.norm(
        sentence_embeddings,
        axis=1,
        keepdims=True
    )

    return (
        sentence_embeddings / np.maximum(norms, 1e-12)
    ).astype(np.float32)


all_embeddings = []
batch_size = 4

for start in range(0, len(documents), batch_size):
    batch = documents[start:start + batch_size]
    texts = [doc["text"] for doc in batch]

    embeddings = encode_batch(texts)
    all_embeddings.append(embeddings)

    print(
        f"Processed {min(start + batch_size, len(documents))}"
        f"/{len(documents)}"
    )

all_embeddings = np.vstack(all_embeddings)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
np.save(OUTPUT_PATH, all_embeddings)

print("\nEmbedding generation complete!")
print("Shape:", all_embeddings.shape)
print("Saved to:", OUTPUT_PATH)
print("Contains NaN:", np.isnan(all_embeddings).any())
