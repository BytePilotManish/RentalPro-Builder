import os

path = "frontend/src/App.jsx"
results = []
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if "App Settings" in line or "layout" in line.lower() or "stamp" in line.lower() or "setting" in line.lower():
                results.append(f"Line {idx+1}: {line.strip()}")

with open("scratch/search_results.txt", "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(results[:100]))

print(f"Found {len(results)} matches.")
