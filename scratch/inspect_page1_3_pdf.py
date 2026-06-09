with open(r"d:\rental pro\new\scratch\pdf_decoded_unicode.txt", "r", encoding="utf-8") as f:
    content = f.read()

pages = content.split('=== PAGE ')
for page in pages:
    if not page.strip():
        continue
    page_num_str = page.split(' ===')[0]
    page_num = int(page_num_str)
    
    if page_num <= 3:
        print(f"\n================ PAGE {page_num} ================")
        lines = page.split('\n')[1:]
        for idx, line in enumerate(lines):
            if line.strip():
                print(f"L{idx+1}: {line.strip().encode('ascii', 'backslashreplace').decode('ascii')}")
