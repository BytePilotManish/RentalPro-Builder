with open(r"d:\rental pro\new\frontend\src\App.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "startNewKannadaAgreement" in line:
        print(f"Line {idx+1}: {line.strip()}")
        # Let's print the next 30 lines
        for j in range(idx+1, min(idx+35, len(lines))):
            print(f"  Line {j+1}: {lines[j].strip().encode('ascii', 'backslashreplace').decode('ascii')}")
        break
