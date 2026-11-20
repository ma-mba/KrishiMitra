
import json
import re
from pathlib import Path
from rank_bm25 import BM25Okapi

data_path = Path("data/processed/kau_crop_chunks.json")

with open(data_path, "r", encoding="utf-8") as f:
    documents = json.load(f)


STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were",
    "my", "me", "i", "you", "your", "why",
    "what", "when", "where", "how", "do",
    "does", "did", "of", "in", "on", "for",
    "to", "and", "or", "with", "it"
}

def tokenize(text):
    words = re.findall(r"[a-z0-9]+", text.lower())

    return [
        word for word in words
        if word not in STOPWORDS
    ]


def search(query, crop, top_k=5):
    # Restrict search to the selected crop
    selected = [
        doc for doc in documents
        if doc["crop"] == crop
    ]

    if not selected:
        print("No documents found for this crop.")
        return

    tokenized = [
        tokenize(doc["text"])
        for doc in selected
    ]

    bm25 = BM25Okapi(tokenized)
    scores = bm25.get_scores(tokenize(query))

    ranked = sorted(
        zip(selected, scores),
        key=lambda item: item[1],
        reverse=True
    )

    print(f"\nQUERY: {query}")
    print(f"CROP: {crop}")
    print("=" * 60)

    results = 0

    for doc, score in ranked:
        if score <= 0:
            continue

        print(f"\nRESULT {results + 1}")
        print("Score:", round(float(score), 3))
        print("PDF page:", doc["pdf_page"])
        print("Chunk:", doc["chunk_id"])
        print("Text:")
        print(doc["text"][:600])
        print("-" * 60)

        results += 1

        if results >= top_k:
            break

    if results == 0:
        print("No positive-scoring matches found.")

if __name__ == "__main__":
    crop = input("Select crop (rice/banana/coconut): ").strip().lower()
    query = input("Ask an agricultural question: ").strip()

    if crop not in {"rice", "banana", "coconut"}:
        print("Invalid crop selection.")
    elif not tokenize(query):
        print("Please enter a valid English query.")
    else:
        search(query, crop)
