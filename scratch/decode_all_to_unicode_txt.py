import sys
import os
import re
import docx

# Import mapping and function from convert_docx_to_unicode.py
sys.path.append(os.path.join(os.getcwd(), 'scratch'))
from convert_docx_to_unicode import process_line

doc = docx.Document(r"d:\rental pro\new\19-05-2026 - kan (2.docx")

with open(r"d:\rental pro\new\scratch\all_paragraphs_unicode.txt", "w", encoding="utf-8") as f:
    f.write(f"Total paragraphs: {len(doc.paragraphs)}\n\n")
    for idx, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if text:
            unicode_text = process_line(text)
            f.write(f"P {idx} (Raw: {repr(text)}):\n{unicode_text}\n\n")

print("Successfully decoded all paragraphs and wrote to scratch/all_paragraphs_unicode.txt")
