import os
import kannada_converter

src_dir = os.path.dirname(kannada_converter.__file__)
mappings_dir = os.path.join(src_dir, "mappings")
print("Mappings files:", os.listdir(mappings_dir))

for file in os.listdir(mappings_dir):
    path = os.path.join(mappings_dir, file)
    print(f"\n=== {file} (size: {os.path.getsize(path)}) ===")
    with open(path, "r", encoding="utf-8") as f:
        # Print first 200 characters of the JSON file
        print(f.read()[:200])
