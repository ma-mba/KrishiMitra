
import json
import re
from pathlib import Path
from tokenizers import Tokenizer

INPUT = Path("data/processed/banana_structured_sections.json")
OUTPUT = Path("data/processed/banana_token_chunks_test.json")

tokenizer = Tokenizer.from_file(
    "models/multilingual_minilm/tokenizer.json"
)
tokenizer.no_truncation()
tokenizer.no_padding()

MAX_TOKENS = 128
TARGET_TOKENS = 110

with open(INPUT, encoding="utf-8") as f:
    sections = json.load(f)


def count_tokens(text):
    return len(tokenizer.encode(text).ids)


def split_sentences(text):
    # Basic sentence splitting for this experiment
    text = re.sub(r"\s+", " ", text).strip()
    return re.split(r"(?<=[.!?])\s+", text)


def split_section(section):
    heading = section["section_heading"]

    # Avoid repeating the heading in the body
    body = section["text"]

    if body.startswith(heading):
        body = body[len(heading):].strip()

    sentences = split_sentences(body)

    chunks = []
    current = []

    def save_chunk():
        if current:
            chunks.append(
                heading + "\n" + " ".join(current)
            )

    for sentence in sentences:
        candidate = current + [sentence]
        candidate_text = heading + "\n" + " ".join(candidate)

        if count_tokens(candidate_text) <= TARGET_TOKENS:
            current = candidate
        else:
            if current:
                save_chunk()
                current = []

            # Handle sentences that are too long
            if count_tokens(heading + "\n" + sentence) > TARGET_TOKENS:
                words = sentence.split()
                partial = []

                for word in words:
                    test = heading + "\n" + " ".join(
                        partial + [word]
                    )

                    if count_tokens(test) <= TARGET_TOKENS:
                        partial.append(word)
                    else:
                        if partial:
                            chunks.append(
                                heading + "\n" + " ".join(partial)
                            )
                        partial = [word]

                current = [" ".join(partial)] if partial else []
            else:
                current = [sentence]

    save_chunk()

    return chunks


all_chunks = []

for section in sections:
    split_texts = split_section(section)

    for index, chunk_text in enumerate(split_texts, start=1):
        all_chunks.append({
            "chunk_id": (
                f"{section['chunk_id']}_part_{index}"
            ),
            "crop": section["crop"],
            "section_heading": section["section_heading"],
            "pdf_pages": section["pdf_pages"],
            "text": chunk_text,
            "token_count": count_tokens(chunk_text)
        })

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(
        all_chunks,
        f,
        ensure_ascii=False,
        indent=2
    )

print("Original sections:", len(sections))
print("New chunks:", len(all_chunks))

print("\nCHUNK DETAILS")

for chunk in all_chunks:
    print("\n" + "=" * 55)
    print("ID:", chunk["chunk_id"])
    print("Tokens:", chunk["token_count"])
    print("Pages:", chunk["pdf_pages"])
    print("Text:", chunk["text"])

print("\nAll chunks within 128 tokens:",
      all(c["token_count"] <= MAX_TOKENS for c in all_chunks))

print("\nSaved to:", OUTPUT)
