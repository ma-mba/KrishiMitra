
import json
import re
from pathlib import Path
from collections import defaultdict

SECTIONS_PATH = Path(
    "data/processed/banana_sections_corrected.json"
)
CHUNKS_PATH = Path(
    "data/processed/banana_chunks_v2.json"
)

with open(SECTIONS_PATH, encoding="utf-8") as f:
    sections = json.load(f)

with open(CHUNKS_PATH, encoding="utf-8") as f:
    chunks = json.load(f)


def normalize(text):
    text = text.replace(
        "cucurbi-\ntaceous",
        "cucurbitaceous"
    )
    return re.sub(r"\s+", " ", text).strip()


grouped = defaultdict(list)

for chunk in chunks:
    parent_id = chunk["chunk_id"].rsplit("_part_", 1)[0]
    grouped[parent_id].append(chunk)


all_passed = True

for section in sections:
    section_id = section["chunk_id"]
    heading = section["section_heading"]

    original = normalize(section["original_text"])

    if not original.startswith(heading):
        raise ValueError(
            f"Original heading mismatch: {section_id}"
        )

    original_body = original[len(heading):].strip()

    reconstructed_parts = []

    for chunk in grouped[section_id]:
        chunk_text = chunk["text"]

        if not chunk_text.startswith(heading + "\n"):
            raise ValueError(
                f"Chunk heading mismatch: {chunk['chunk_id']}"
            )

        body = chunk_text[len(heading):].strip()
        reconstructed_parts.append(body)

    reconstructed_body = normalize(
        " ".join(reconstructed_parts)
    )

    passed = original_body == reconstructed_body
    all_passed = all_passed and passed

    print("\n" + "=" * 55)
    print("Section:", section_id)
    print("Heading:", heading)
    print("Chunks:", len(grouped[section_id]))
    print("Content preserved:", passed)

    if not passed:
        print("\nOriginal body:")
        print(original_body)
        print("\nReconstructed body:")
        print(reconstructed_body)

print("\n" + "=" * 55)
print("ALL SECTIONS PRESERVED:", all_passed)
