with open(r"d:\rental pro\new\frontend\src\App.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"d:\rental pro\new\scratch\search_templates_results.txt", "w", encoding="utf-8") as out:
    for idx, line in enumerate(lines):
        line_lower = line.lower()
        if "template" in line_lower or "card" in line_lower or "commercial" in line_lower or "kannada" in line_lower or "-1" in line_lower:
            out.write(f"Line {idx+1}: {line.strip()}\n")

print("Done. Saved to scratch/search_templates_results.txt")
