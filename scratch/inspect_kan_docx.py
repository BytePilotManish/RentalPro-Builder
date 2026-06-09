import docx
import os

path = r"d:\rental pro\new\19-05-2026 - kan (2.docx"
if os.path.exists(path):
    doc = docx.Document(path)
    print(f"Document loaded successfully. Total paragraphs: {len(doc.paragraphs)}, Total tables: {len(doc.tables)}")
    
    # Print first 20 non-empty paragraphs
    count = 0
    print("\n--- Non-empty Paragraphs ---")
    for idx, p in enumerate(doc.paragraphs):
        if p.text.strip():
            count += 1
            print(f"P {idx+1}: {p.text[:100]}")
            for r in p.runs:
                if r.text.strip():
                    print(f"  Run: {r.text[:50]} | Font: {r.font.name}")
            if count >= 15:
                break
                
    # Check tables
    for t_idx, t in enumerate(doc.tables):
        print(f"\n--- Table {t_idx+1} ({len(t.rows)} rows, {len(t.columns)} cols) ---")
        for r_idx, row in enumerate(t.rows[:3]):
            for c_idx, cell in enumerate(row.cells):
                if cell.text.strip():
                    print(f"  Row {r_idx+1} Col {c_idx+1}: {cell.text[:100]}")
else:
    print("File not found.")
