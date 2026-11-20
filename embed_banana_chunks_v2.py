
import json
import numpy as np
import onnxruntime as ort

from pathlib import Path
from tokenizers import Tokenizer

MODEL_DIR = Path("models/multilingual_minilm")
INPUT = Path("data/processed/banana_chunks_v2.json")
OUTPUT = Path("data/processed/banana_embeddings_v2.npy")

MODEL_PATH = MODEL_DIR / "onnx/model_quint8_avx2.onnx"

with open(INPUT, encoding="utf-8") as f:
    chunks = json.load(f)

tokenizer = Tokenizer.from_file(
    str(MODEL_DIR / "tokenizer.json")
)

tokenizer.enable_truncation(max_length=128)
tokenizer.enable_padding(
    pad_id=0,
    pad_token="[PAD]"
)

session = ort.InferenceSession(
    str(MODEL_PATH),
    providers=["CPUExecutionProvider"]
)

input_names = {item.name for item in session.get_inputs()}

print("Model inputs:", sorted(input_names))


def embed(text):
    encoded = tokenizer.encode(text)

    ids = np.array(
        [encoded.ids], dtype=np.int64
    )

    mask = np.array(
        [encoded.attention_mask], dtype=np.int64
    )

    feeds = {
        "input_ids": ids,
        "attention_mask": mask
    }

    if "token_type_ids" in input_names:
        feeds["token_type_ids"] = np.zeros_like(ids)

    feeds = {
        key: value
        for key, value in feeds.items()
        if key in input_names
    }

    outputs = session.run(None, feeds)

    # Token-level embeddings
    token_embeddings = outputs[0]

    # Mean pooling over non-padding tokens
    expanded_mask = mask[:, :, None].astype(np.float32)

    pooled = (
        (token_embeddings * expanded_mask).sum(axis=1)
        / np.maximum(expanded_mask.sum(axis=1), 1e-9)
    )

    # L2 normalization
    norm = np.linalg.norm(
        pooled, axis=1, keepdims=True
    )

    normalized = pooled / np.maximum(norm, 1e-12)

    return normalized[0].astype(np.float32)


embeddings = []

for i, chunk in enumerate(chunks, start=1):
    vector = embed(chunk["text"])
    embeddings.append(vector)

    print(
        f"Embedded {i}/{len(chunks)}:",
        chunk["chunk_id"]
    )

embeddings = np.stack(embeddings)

assert embeddings.shape == (len(chunks), 384)
assert np.isfinite(embeddings).all()

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
np.save(OUTPUT, embeddings)

print("\nEmbedding shape:", embeddings.shape)
print("NaN values:", np.isnan(embeddings).sum())
print("Saved to:", OUTPUT)
