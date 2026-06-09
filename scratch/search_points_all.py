import docx

doc = docx.Document(r"d:\rental pro\new\19-05-2026 - kan (2.docx")
print("Non-empty paragraphs:")
for idx, p in enumerate(doc.paragraphs):
    text = p.text.strip()
    if text:
        # Print paragraph index and the first 100 characters of text
        print(f"P {idx}: {text[:120]}")
