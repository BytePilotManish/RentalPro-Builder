import re

with open(r"d:\rental pro\new\scratch\all_paragraphs_unicode.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Let's find paragraphs containing numbers or points like 10, 11, etc.
with open(r"d:\rental pro\new\scratch\search_points_results.txt", "w", encoding="utf-8") as out_f:
    lines = content.split('\n')
    p_info = ""
    for line in lines:
        if line.startswith('P '):
            p_info = line
        elif line.strip():
            match = re.match(r'^\s*(\d+)[\.\s\)]', line)
            if match:
                num = int(match.group(1))
                if 1 <= num <= 25:
                    out_f.write(f"{p_info} -> {line}\n")
            elif any(str(n) in line[:10] for n in range(10, 20)):
                out_f.write(f"{p_info} -> {line}\n")
print("Wrote results to scratch/search_points_results.txt")

