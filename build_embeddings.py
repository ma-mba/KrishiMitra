
import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

data_path = Path("data/processed/kau_crop_chunks.json")
output_path = Path("data/processed/kau_embeddings.npy")

with open(data_path, "r", encoding="utf-8") as f:
    documents = json.load(f)

print("Loading multilingual embedding model...")

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    device="cpu"
)

texts = [doc["text"] for doc in documents]

print("Generating embeddings for", len(texts), "chunks...")

embeddings = model.encode(
    texts,
    batch_size=8,
    show_progress_bar=True,
    normalize_embeddings=True,
    convert_to_numpy=True
)

np.save(output_path, embeddings)

print("\nEmbeddings generated successfully!")
print("Shape:", embeddings.shape)
print("Saved to:", output_path)
