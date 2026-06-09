import docx
import os

path = r"d:\rental pro\new\19-05-2026 - kan (2.docx"
if os.path.exists(path):
    doc = docx.Document(path)
    # Paragraphs 25 to 60
    for idx in range(25, 60):
        p = doc.paragraphs[idx]
        if p.text.strip():
            print(f"\n--- Paragraph {idx} ---")
            print(f"Full text (Nudi): {repr(p.text)}")
            for r_idx, r in enumerate(p.runs):
                if r.text.strip():
                    print(f"  Run {r_idx}: {repr(r.text)} | Font: {r.font.name}")
else:
    print("File not found")
