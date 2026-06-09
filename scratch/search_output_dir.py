import os

path = "app.py"
results = []
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if "OUTPUT_DIR" in line:
                results.append(f"Line {idx+1}: {line.strip()}")

with open("scratch/search_results.txt", "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(results))

print(f"Found {len(results)} matches for OUTPUT_DIR.")
