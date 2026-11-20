
import json
import re
from pathlib import Path

input_path = Path("data/processed/kau_english_pages.json")
output_path = Path("data/processed/kau_english_chunks.json")

with open(input_path, "r", encoding="utf-8") as f:
    pages = json.load(f)

def clean_text(text):
    # Normalize whitespace while keeping paragraph breaks
    text = text.replace("\r", "")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def split_text(text, chunk_size=800, overlap=150):
    chunks = []
    start = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))

        # Prefer breaking at whitespace
        if end < len(text):
            last_space = text.rfind(" ", start, end)
            if last_space > start + chunk_size // 2:
                end = last_space

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end == len(text):
            break

        start = max(start + 1, end - overlap)

    return chunks

records = []

for page in pages:
    cleaned = clean_text(page["text"])
    chunks = split_text(cleaned)

    for index, chunk in enumerate(chunks):
        records.append({
            "chunk_id": f"kau_{page['page']}_{index}",
            "document": page["document"],
            "source": page["source"],
            "language": page["language"],
            "publication_year": page["publication_year"],
            "page": page["page"],
            "text": chunk
        })

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)

print("Original page records:", len(pages))
print("Total chunks created:", len(records))
print("Saved to:", output_path)

if records:
    print("\nExample chunk:")
    print("Chunk ID:", records[0]["chunk_id"])
    print("Page:", records[0]["page"])
    print("Text:", records[0]["text"][:400])
