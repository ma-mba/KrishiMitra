
from pathlib import Path
import pymupdf

root = Path("data/raw")

def check_pdf(path):
    print("\n" + "=" * 60)
    print("FILE:", path.name)

    with pymupdf.open(path) as doc:
        print("TOTAL PAGES:", len(doc))

        # Check beginning, middle and end
        page_numbers = sorted(set([
            0,
            min(20, len(doc) - 1),
            len(doc) // 2,
            len(doc) - 1
        ]))

        for page_num in page_numbers:
            text = doc[page_num].get_text()

            malayalam_count = sum(
                0x0D00 <= ord(char) <= 0x0D7F
                for char in text
            )

            print(f"\nPAGE: {page_num + 1}")
            print("Characters:", len(text))
            print("Malayalam Unicode chars:", malayalam_count)
            print("Preview:", repr(text[:250]))

for pdf in root.rglob("*.pdf"):
    check_pdf(pdf)
