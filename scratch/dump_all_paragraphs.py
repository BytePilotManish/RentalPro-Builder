import docx

doc = docx.Document(r"d:\rental pro\new\19-05-2026 - kan (2.docx")
print("Paragraphs in the document:")
for idx, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if not text:
        continue
    # Check if this paragraph contains numbers or points
    print(f"P {idx}: {text}")
