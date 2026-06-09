with open(r"d:\rental pro\new\scratch\all_paragraphs_unicode.txt", "r", encoding="utf-8") as f:
    content = f.read()

import re
lines = content.split('\n')
p_info = ""
found = False
for line in lines:
    if line.startswith('P '):
        p_info = line
    elif line.strip():
        # Check if line contains "10" or "11" or "12" or "13" or "14" or "15" or "16" or "17" or "18"
        # but specifically search for points at the beginning of the line
        match = re.match(r'^\s*(\d+)[\.\)]', line)
        if match:
            val = int(match.group(1))
            if 9 <= val <= 20:
                print(f"FOUND: {p_info} -> {line[:100].encode('ascii', 'backslashreplace').decode('ascii')}")
                found = True

if not found:
    print("No points 10-18 found at the beginning of paragraphs.")
