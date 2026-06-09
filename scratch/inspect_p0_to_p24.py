import docx

doc = docx.Document(r"d:\rental pro\new\19-05-2026 - kan (2.docx")
print("Non-empty paragraphs in 0 to 24:")
for idx in range(0, 25):
    text = doc.paragraphs[idx].text.strip()
    if text:
        print(f"P {idx}: '{text}'")
