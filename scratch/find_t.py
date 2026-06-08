import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

with open("frontend/src/App.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

out = []
for idx, line in enumerate(lines):
    if "t(" in line:
        out.append(f"Line {idx+1}: {line.strip()}")

with open("scratch/t_occurrences.txt", "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(out))

print("Saved t occurrences to scratch/t_occurrences.txt")
