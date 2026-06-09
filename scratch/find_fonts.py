import os

results = []
for root, dirs, files in os.walk("."):
    for file in files:
        if file.lower().endswith((".ttf", ".otf", ".woff", ".woff2")):
            results.append(os.path.join(root, file))

print(f"Fonts found ({len(results)}):")
for r in results:
    print(r)
