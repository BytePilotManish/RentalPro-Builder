import sys

# Reconfigure stdout to use utf-8 if possible
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

with open("frontend/src/App.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

output_lines = []
for idx, line in enumerate(lines):
    if "language" in line.lower() or "lang" in line.lower() or "hindi" in line.lower() or "kannada" in line.lower() or "translation" in line.lower() or "translate" in line.lower():
        output_lines.append(f"Line {idx+1}: {line.strip()}")

with open("scratch/search_results.txt", "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(output_lines))

print("Saved results to scratch/search_results.txt")
