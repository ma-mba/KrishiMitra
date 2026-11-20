
import json
import re
from rank_bm25 import BM25Okapi

with open(
    "data/processed/banana_chunks_v2.json",
    encoding="utf-8"
) as f:
    chunks = json.load(f)


def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())


documents = [
    tokenize(chunk["text"])
    for chunk in chunks
]

bm25 = BM25Okapi(documents)

query = (
    "My banana leaves are losing colour "
    "in patches and look striped."
)

scores = bm25.get_scores(tokenize(query))

ranked = sorted(
    range(len(chunks)),
    key=lambda i: scores[i],
    reverse=True
)

print("QUESTION:", query)
print("\nBM25 RANKING")

for rank, index in enumerate(ranked, start=1):
    chunk = chunks[index]

    print("\n" + "=" * 55)
    print("Rank:", rank)
    print("Score:", round(float(scores[index]), 4))
    print("ID:", chunk["chunk_id"])
    print("Heading:", chunk["section_heading"])

expected = "banana_section_002_part_2"

expected_rank = next(
    rank
    for rank, index in enumerate(ranked, start=1)
    if chunks[index]["chunk_id"] == expected
)

print("\n" + "=" * 55)
print("Expected chunk rank:", expected_rank)
print("BM25 Top-1 correct:", expected_rank == 1)
