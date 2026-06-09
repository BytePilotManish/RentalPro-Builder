import docx
import os

path = r"d:\rental pro\new\19-05-2026 - kan (2.docx"
if os.path.exists(path):
    doc = docx.Document(path)
    for idx, p in enumerate(doc.paragraphs):
        if p.text.strip():
            # Convert text to CP1252 or Latin-1 representation
            text = p.text
            latin1_text = text.encode('utf-8', errors='ignore').decode('latin-1', errors='ignore')
            print(f"P {idx+1} (repr): {repr(text)}")
            print(f"P {idx+1} (plain): {text}")
            break
else:
    print("File not found.")
