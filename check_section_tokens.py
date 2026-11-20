
import json
from pathlib import Path
from tokenizers import Tokenizer

MODEL_DIR = Path("models/multilingual_minilm")
DATA_PATH = Path(
    "data/processed/banana_structured_sections.json"
)

tokenizer = Tokenizer.from_file(
    str(MODEL_DIR / "tokenizer.json")
)

# Disable truncation to measure complete token lengths
tokenizer.no_truncation()
tokenizer.no_padding()

with open(DATA_PATH, encoding="utf-8") as f:
    sections = json.load(f)

MAX_TOKENS = 128

for section in sections:
    encoding = tokenizer.encode(section["text"])
    token_count = len(encoding.ids)

    print("\n" + "=" * 55)
    print("Section:", section["section_heading"])
    print("Characters:", len(section["text"]))
    print("Tokens:", token_count)
    print("Limit:", MAX_TOKENS)
    print(
        "Would be truncated:",
        token_count > MAX_TOKENS
    )
