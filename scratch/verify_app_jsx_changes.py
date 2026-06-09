with open(r"d:\rental pro\new\frontend\src\App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

if "ಶ್ರೀಮತಿ.ಜಯಲಕ್ಷ್ಮಮ್ಮ" in content:
    print("[OK] startNewKannadaAgreement changes applied successfully.")
else:
    print("[ERROR] startNewKannadaAgreement changes NOT found!")
