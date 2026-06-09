import re

with open(r"d:\rental pro\new\scratch\all_paragraphs_unicode.txt", "r", encoding="utf-8") as f:
    content = f.read()

# Let's write a list of any occurrences of numbers in the file
with open(r"d:\rental pro\new\scratch\numbers_occurrences.txt", "w", encoding="utf-8") as out:
    lines = content.split('\n')
    p_info = ""
    for line in lines:
        if line.startswith('P '):
            p_info = line
        elif line.strip():
            # Check if there is any number in the line
            numbers = re.findall(r'\d+', line)
            if numbers:
                out.write(f"{p_info} -> {line}\n")

print("Done searching for any numbers.")
