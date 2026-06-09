import os

search_terms = ["propertieslist"]
results = []

for root, dirs, files in os.walk("."):
    # Skip build/dist/node_modules/git directories
    if any(p in root for p in ["node_modules", ".git", "dist", "build", "__pycache__"]):
        continue
    for file in files:
        if file.endswith((".jsx", ".js", ".py", ".html", ".css")):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    for idx, line in enumerate(f):
                        line_str = line.strip()
                        for term in search_terms:
                            if term in line.lower():
                                results.append(f"{path} Line {idx+1} ({term}): {line_str}")
                                break
            except Exception as e:
                pass

with open("scratch/search_results.txt", "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(results))

print(f"Search complete. Found {len(results)} lines. Saved to scratch/search_results.txt")
