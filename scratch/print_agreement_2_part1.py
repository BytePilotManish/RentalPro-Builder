import sys
import os
import docx

sys.path.append(os.path.join(os.getcwd(), 'scratch'))
from convert_docx_to_unicode import process_line

doc = docx.Document(r"d:\rental pro\new\19-05-2026 - kan (2.docx")

print("--- AGREEMENT 2 PART 1 ---")
for idx in range(132, 156):
    p = doc.paragraphs[idx]
    text = p.text.strip()
    if text:
        unicode_text = process_line(text)
        print(f"P {idx}: {unicode_text.encode('ascii', 'backslashreplace').decode('ascii')}")
