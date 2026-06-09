with open(r"d:\rental pro\new\frontend\src\App.jsx", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("TEMPLATE CARDS AND TITLES:")
in_card = False
card_lines = []
for idx, line in enumerate(lines):
    if "onClick={" in line or "card" in line.lower() or "h3" in line.lower():
        # print some lines that look like template cards
        if any(term in line.lower() for term in ["rental", "agreement", "template", "kannada", "commercial", "residential"]):
            print(f"Line {idx+1}: {line.strip()}")
