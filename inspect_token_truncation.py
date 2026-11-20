
import json
from tokenizers import Tokenizer

with open(
    "data/processed/banana_structured_sections.json",
    encoding="utf-8"
) as f:
    sections = json.load(f)

tokenizer = Tokenizer.from_file(
    "models/multilingual_minilm/tokenizer.json"
)

tokenizer.no_truncation()
tokenizer.no_padding()

LIMIT = 128

for section in sections:
    if "Banana streak disease" not in section["section_heading"]:
        continue

    encoding = tokenizer.encode(section["text"])

    print("Total tokens:", len(encoding.ids))

    if len(encoding.ids) > LIMIT:
        # Show the text covered by the first 128 tokens
        offsets = [
            end for start, end in encoding.offsets[:LIMIT]
            if end > start
        ]

        cutoff = max(offsets)

        print("\nTEXT INCLUDED:")
        print("=" * 55)
        print(section["text"][:cutoff])

        print("\nTEXT OMITTED:")
        print("=" * 55)
        print(section["text"][cutoff:])

        print("\nCutoff character position:", cutoff)
