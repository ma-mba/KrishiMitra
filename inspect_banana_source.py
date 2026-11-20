
import json
from pathlib import Path

path = Path("data/processed/kau_english_pages.json")

with open(path, "r", encoding="utf-8") as f:
    pages = json.load(f)

for page in pages:
    if page["page"] == 222:
        print("=" * 60)
        print("ORIGINAL PDF PAGE 222")
        print("=" * 60)
        print(page["text"])
        break
else:
    print("Page 222 not found.")
