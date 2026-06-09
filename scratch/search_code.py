import os

search_terms = ["/tenants", "tenants", "TenantCreate"]
results = []

path = "app.py"
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            line_str = line.strip()
            for term in search_terms:
                if term in line:
                    results.append(f"Line {idx+1} ({term}): {line_str}")
                    break

with open("scratch/search_results.txt", "w", encoding="utf-8") as f_out:
    f_out.write("\n".join(results))

print(f"Search complete. Found {len(results)} lines. Saved to scratch/search_results.txt")
