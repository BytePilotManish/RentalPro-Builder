import sys
import os
import docx

sys.path.append(os.path.join(os.getcwd(), 'scratch'))
from convert_docx_to_unicode import process_line

doc = docx.Document(r"d:\rental pro\new\19-05-2026 - kan (2.docx")

with open(r"d:\rental pro\new\scratch\agreement2_decoded_side_by_side.txt", "w", encoding="utf-8") as out:
    out.write("AGREEMENT 2 PARAGRAPHS SIDE-BY-SIDE:\n\n")
    for idx in range(132, 192):
        p = doc.paragraphs[idx]
        text = p.text
        if text.strip():
            unicode_text = process_line(text)
            escaped_raw = text.encode('ascii', 'backslashreplace').decode('ascii')
            out.write(f"--- PARAGRAPH {idx} ---\n")
            out.write(f"RAW (CP1252): {text}\n")
            out.write(f"RAW ESCAPED:  {escaped_raw}\n")
            out.write(f"UNICODE:      {unicode_text}\n\n")

print("Side-by-side output written to scratch/agreement2_decoded_side_by_side.txt")
