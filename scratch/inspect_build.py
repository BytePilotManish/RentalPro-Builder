import os

path = "frontend/dist/assets/index-C3qNB9oX.js"
if os.path.exists(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    start = 0
    count = 0
    while True:
        idx = content.find("propertiesList", start)
        if idx == -1:
            break
        count += 1
        print(f"Occurrence {count} at index {idx}:")
        ctx_start = max(0, idx - 100)
        ctx_end = min(len(content), idx + 100)
        print("  Context:", content[ctx_start:ctx_end])
        start = idx + len("propertiesList")
    print(f"Total occurrences found: {count}")
else:
    print("Build file not found.")
