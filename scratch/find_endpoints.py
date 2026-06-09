with open(r"d:\rental pro\new\app.py", "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        if "@app." in line:
            print(f"Line {idx+1}: {line.strip()}")
