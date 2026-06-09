with open(r"d:\rental pro\new\frontend\src\App.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

with open(r"d:\rental pro\new\scratch\templates_list_results.txt", "w", encoding="utf-8") as out:
    for idx, line in enumerate(lines):
        if "-1" in line or "Template" in line:
            # check if it looks like a template list or card rendering
            if any(term in line for term in ["id:", "title:", "description:", "const templates", "const DEFAULT_TEMPLATES"]):
                out.write(f"Line {idx+1}: {line.strip()}\n")

print("Done. Saved to scratch/templates_list_results.txt")
