with open(r"d:\rental pro\new\frontend\src\App.jsx", "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for the template cards. Typically they look like:
# "Commercial Rental Agreement (kannada)" or similar
# Let's search for the word "kannada" in a case-insensitive way
import re
for match in re.finditer(r'.{0,100}kannada.{0,100}', content, re.IGNORECASE):
    print(match.group(0).strip().encode('ascii', 'backslashreplace').decode('ascii'))
