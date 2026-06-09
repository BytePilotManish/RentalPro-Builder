with open(r"d:\rental pro\new\scratch\pdf_decoded_unicode.txt", "r", encoding="utf-8") as f:
    content = f.read()

pages = content.split('=== PAGE ')
page = pages[5]
lines = page.split('\n')[1:]
for idx in range(min(12, len(lines))):
    line = lines[idx]
    if line.strip():
        print(f"L{idx+1}: {line.strip().encode('ascii', 'backslashreplace').decode('ascii')}")
