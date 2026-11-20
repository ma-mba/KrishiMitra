
import json
import random
from pathlib import Path

path = Path("data/processed/kau_english_chunks.json")

with open(path, "r", encoding="utf-8") as f:
    chunks = json.load(f)

print("TOTAL CHUNKS:", len(chunks))

# Search for the three crops in our project
keywords = {
    "PADDY / RICE": ["rice", "paddy"],
    "BANANA": ["banana"],
    "COCONUT": ["coconut"]
}

for crop, terms in keywords.items():
    matches = [
        chunk for chunk in chunks
        if any(
            term in chunk["text"].lower()
            for term in terms
        )
    ]

    print("\n" + "=" * 60)
    print("CROP:", crop)
    print("MATCHING CHUNKS:", len(matches))

    # Fixed seed makes results reproducible
    random.seed(42)

    samples = random.sample(
        matches,
        min(2, len(matches))
    )

    for chunk in samples:
        print("\nCHUNK ID:", chunk["chunk_id"])
        print("PDF PAGE:", chunk["page"])
        print("TEXT:")
        print(chunk["text"])
        print("-" * 40)

# Check chunk sizes
lengths = [len(chunk["text"]) for chunk in chunks]

print("\n" + "=" * 60)
print("CHUNK SIZE STATISTICS")
print("Smallest:", min(lengths))
print("Largest:", max(lengths))
print("Average:", round(sum(lengths) / len(lengths), 2))

short_chunks = sum(length < 100 for length in lengths)
print("Chunks shorter than 100 characters:", short_chunks)

