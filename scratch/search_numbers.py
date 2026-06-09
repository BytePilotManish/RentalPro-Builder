import docx
import re

doc = docx.Document(r"d:\rental pro\new\19-05-2026 - kan (2.docx")
print("Non-empty paragraphs list:")
for idx, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if text:
        # Check if the text starts with a number or digit or dot or is a list item
        print(f"P {idx}: '{text}'")
