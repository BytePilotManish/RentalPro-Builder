with open(r"d:\rental pro\new\scratch\pdf_decoded_unicode.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Let's inspect page 4, 5, 6
pages = content.split('=== PAGE ')
for page in pages:
    if not page.strip():
        continue
    page_num_str = page.split(' ===')[0]
    page_num = int(page_num_str)
    
    if 4 <= page_num <= 6:
        print(f"\n================ PAGE {page_num} ================")
        # Print each line of the page content
        lines = page.split('\n')[1:] # Skip page header
        for idx, line in enumerate(lines):
            if line.strip():
                print(f"L{idx+1}: {line.strip().encode('ascii', 'backslashreplace').decode('ascii')}")
