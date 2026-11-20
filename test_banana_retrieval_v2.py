
import json
import numpy as np
import onnxruntime as ort

from pathlib import Path
from tokenizers import Tokenizer

MODEL_DIR = Path("models/multilingual_minilm")

with open(
    "data/processed/banana_chunks_v2.json",
    encoding="utf-8"
) as f:
    chunks = json.load(f)

embeddings = np.load(
    "data/processed/banana_embeddings_v2.npy"
)

assert len(chunks) == len(embeddings)

tokenizer = Tokenizer.from_file(
    str(MODEL_DIR / "tokenizer.json")
)

tokenizer.enable_truncation(max_length=128)
tokenizer.enable_padding(
    pad_id=0,
    pad_token="[PAD]"
)

session = ort.InferenceSession(
    str(MODEL_DIR / "onnx/model_quint8_avx2.onnx"),
    providers=["CPUExecutionProvider"]
)


def embed_query(text):
    encoded = tokenizer.encode(text)

    ids = np.array([encoded.ids], dtype=np.int64)
    mask = np.array(
        [encoded.attention_mask], dtype=np.int64
    )

    feeds = {
        "input_ids": ids,
        "attention_mask": mask,
        "token_type_ids": np.zeros_like(ids)
    }

    token_vectors = session.run(None, feeds)[0]

    expanded_mask = mask[:, :, None].astype(np.float32)

    pooled = (
        (token_vectors * expanded_mask).sum(axis=1)
        / np.maximum(expanded_mask.sum(axis=1), 1e-9)
    )

    norm = np.linalg.norm(
        pooled, axis=1, keepdims=True
    )

    return (pooled / np.maximum(norm, 1e-12))[0]


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

passed = 0

for test in tests:
    query_vector = embed_query(test["question"])

    scores = embeddings @ query_vector
    ranked = np.argsort(scores)[::-1]

    top_id = chunks[ranked[0]]["chunk_id"]

    success = top_id == test["expected"]

    if success:
        passed += 1

    print("\n" + "=" * 65)
    print("Question:", test["question"])
    print("Expected:", test["expected"])
    print("Top-1 correct:", success)

    
        chunk = chunks[index]

        print(
            f"\nRank {rank} | "
            f"Score: {scores[index]:.4f}"
        )
        print("ID:", chunk["chunk_id"])
        print("Heading:", chunk["section_heading"])
        print("Text:", chunk["text"][:250])

print("\n" + "=" * 65)
print(f"TOP-1 ACCURACY: {passed}/{len(tests)}")
