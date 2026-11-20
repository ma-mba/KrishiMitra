
from pathlib import Path
import pymupdf

matches = list(Path("data/raw").rglob("pop_ml_2016.pdf"))

if not matches:
    raise FileNotFoundError("Malayalam PDF not found")

with pymupdf.open(matches[0]) as doc:
    page = doc[20]  # Page 21

    data = page.get_text("dict")

    count = 0

    for block in data["blocks"]:
        for line in block.get("lines", []):
            for span in line["spans"]:
                content = span["text"].strip()

                if not content:
                    continue

                print("FONT:", span["font"])
                print("TEXT:", repr(content[:180]))
                print("-" * 40)

                count += 1

                if count >= 15:
                    break
            if count >= 15:
                break
        if count >= 15:
            break
