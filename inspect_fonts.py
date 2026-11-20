
import pymupdf
from collections import Counter

pdf_path = "data/raw/malayalam/pop_ml_2016.pdf"

doc = pymupdf.open(pdf_path)
fonts = Counter()

for page in doc:
    for font in page.get_fonts(full=True):
        font_name = font[3]
        fonts[font_name] += 1

print("Fonts found in Malayalam PDF:\n")

for name, count in fonts.most_common():
    print(f"{name}: {count} pages")

doc.close()
