import docx

doc = docx.Document(r"d:\rental pro\new\19-05-2026 - kan (2.docx")

print("DUMP OF PARAGRAPHS 132 to 191 WITH CP1252 REPRESENTATION:")
for idx in range(132, 192):
    p = doc.paragraphs[idx]
    text = p.text
    if text.strip():
        # Encode as CP1252 or raw ascii escapes to see the exact bytes/characters
        escaped = text.encode('ascii', 'backslashreplace').decode('ascii')
        print(f"P {idx}: {escaped}")
