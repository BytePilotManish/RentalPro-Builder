with open(r"d:\rental pro\new\scratch\pdf_decoded_unicode.txt", "r", encoding="utf-8") as f:
    content = f.read()

pages = content.split('=== PAGE ')
page = pages[5] # Page 5 (1-based index 5, so pages[5] since pages[0] is empty before split or page 1 is pages[1])
# Let's verify page number
print(page.split('\n')[0])
for idx, line in enumerate(page.split('\n')[1:]):
    if line.strip():
        print(f"L{idx+1}: {line.strip().encode('ascii', 'backslashreplace').decode('ascii')}")
