with open(r"d:\rental pro\new\frontend\src\App.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx in range(3580, 3615):
    print(f"Line {idx+1}: {lines[idx].strip().encode('ascii', 'backslashreplace').decode('ascii')}")
