
import json
import re

with open(
    "data/processed/banana_token_chunks_test.json",
    encoding="utf-8"
) as f:
    chunks = json.load(f)


def normalize_text(text):
    # Repair a verified split heading
    text = text.replace(
        "Infectious chlorosis (Cucumber mosaic\nvirus disease)",
        "Infectious chlorosis (Cucumber mosaic virus disease)"
    )

    # Repair the verified line-break artifact
    text = text.replace(
        "cucurbi- taceous",
        "cucurbitaceous"
    )

    return re.sub(r"[ \t]+", " ", text).strip()


for chunk in chunks:
    if chunk["chunk_id"] in {
        "banana_section_002_part_1",
        "banana_section_002_part_3"
    }:
        print("\n" + "=" * 55)
        print("ID:", chunk["chunk_id"])
        print("\nBEFORE:")
        print(chunk["text"])
        print("\nAFTER:")
        print(normalize_text(chunk["text"]))
