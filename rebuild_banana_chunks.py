
import json
import re
from pathlib import Path
from tokenizers import Tokenizer

INPUT = Path("data/processed/banana_sections_corrected.json")
OUTPUT = Path("data/processed/banana_chunks_v2.json")

tokenizer = Tokenizer.from_file(
    "models/multilingual_minilm/tokenizer.json"
)
tokenizer.no_truncation()
tokenizer.no_padding()

MAX_TOKENS = 128
TARGET_TOKENS = 110

with open(INPUT, encoding="utf-8") as f:
    sections = json.load(f)


def token_count(text):
    return len(tokenizer.encode(text).ids)


def clean_body(section):
    text = section["original_text"]

    # Verified PDF line-break artifact
    text = text.replace(
        "cucurbi-\ntaceous",
        "cucurbitaceous"
    )

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    heading = section["section_heading"]

    # Remove heading already present in source text
    if text.startswith(heading):
        text = text[len(heading):].strip()
    else:
        raise ValueError(
            f"Heading mismatch: {section['chunk_id']}"
        )

    return text


def split_section(section):
    heading = section["section_heading"]
    body = clean_body(section)

    sentences = re.split(r"(?<=[.!?])\s+", body)

    chunks = []
    current = []

    def make_text(parts):
        return heading + "\n" + " ".join(parts)

    for sentence in sentences:
        if not sentence:
            continue

        candidate = current + [sentence]

        if token_count(make_text(candidate)) <= TARGET_TOKENS:
            current = candidate
            continue

        if current:
            chunks.append(make_text(current))
            current = []

        if token_count(make_text([sentence])) <= TARGET_TOKENS:
            current = [sentence]
            continue

        # Split unusually long sentences by words
        words = sentence.split()
        partial = []

        for word in words:
            candidate = partial + [word]

            if token_count(make_text(candidate)) <= TARGET_TOKENS:
                partial = candidate
            else:
                if not partial:
                    raise ValueError(
                        f"Word exceeds token budget: {word}"
                    )

                chunks.append(make_text(partial))
                partial = [word]

        current = partial

    if current:
        chunks.append(make_text(current))

    return chunks


all_chunks = []

for section in sections:
    texts = split_section(section)

    for index, chunk_text in enumerate(texts, start=1):
        count = token_count(chunk_text)

        if count > MAX_TOKENS:
            raise ValueError(
                f"Chunk exceeds limit: {section['chunk_id']}"
            )

        all_chunks.append({
            "chunk_id": f"{section['chunk_id']}_part_{index}",
            "crop": section["crop"],
            "section_heading": section["section_heading"],
            "pdf_pages": section["pdf_pages"],
            "text": chunk_text,
            "token_count": count
        })

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(
        all_chunks,
        f,
        ensure_ascii=False,
        indent=2
    )

print("Original sections:", len(sections))
print("New chunks:", len(all_chunks))

for chunk in all_chunks:
    print(
        chunk["chunk_id"],
        "| Tokens:", chunk["token_count"],
        "| Heading:", chunk["section_heading"]
    )

print(
    "\nAll chunks within 128 tokens:",
    all(c["token_count"] <= MAX_TOKENS for c in all_chunks)
)

print("Saved to:", OUTPUT)
