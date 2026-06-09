import docx

doc = docx.Document(r"d:\rental pro\new\19-05-2026 - kan (2.docx")
target_indices = [28, 43, 45, 135, 150, 240, 241]

with open(r"d:\rental pro\new\scratch\inspect_kan_p28_output.txt", "w", encoding="utf-8") as f:
    for idx in target_indices:
        p = doc.paragraphs[idx]
        f.write(f"=== Paragraph {idx} ===\n")
        f.write(f"Text: {p.text}\n")
        f.write(f"Bytes: {p.text.encode('latin1', 'replace')}\n")
        f.write(f"Repr: {repr(p.text)}\n\n")
