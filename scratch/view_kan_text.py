import docx
import os

path = r"d:\rental pro\new\19-05-2026 - kan (2.docx"
if os.path.exists(path):
    doc = docx.Document(path)
    lines = []
    for idx, p in enumerate(doc.paragraphs):
        if p.text.strip():
            lines.append(f"P {idx+1}: {p.text}")
    
    with open("scratch/kan_text.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("Written to scratch/kan_text.txt")
else:
    print("File not found.")
