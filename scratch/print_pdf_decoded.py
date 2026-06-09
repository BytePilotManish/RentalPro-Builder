with open(r"d:\rental pro\new\scratch\pdf_decoded_unicode.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Let's print out page-by-page content, encoding/decoding to ascii safe print
pages = content.split('=== PAGE ')
for page in pages:
    if not page.strip():
        continue
    page_num_str = page.split(' ===')[0]
    page_num = int(page_num_str)
    
    # We only care about page 4 to 8
    if page_num >= 4:
        print(f"\n================ PAGE {page_num} ================")
        lines = page.split('\n')[1:] # Skip first line which is page num info
        for line in lines:
            if line.strip():
                print(line.strip().encode('ascii', 'backslashreplace').decode('ascii'))
