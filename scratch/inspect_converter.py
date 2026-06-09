import os
import sys
import json
import kannada_converter

src_dir = os.path.dirname(kannada_converter.__file__)
mappings_dir = os.path.join(src_dir, "mappings")

# Read mappings/unicode_to_ascii.json and mappings/ascii_to_unicode.json
info = {}
for file in os.listdir(mappings_dir):
    if file.endswith('.json'):
        path = os.path.join(mappings_dir, file)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            info[file] = {
                "size": len(data),
                "keys_sample": list(data.keys())[:10],
                "values_sample": list(data.values())[:10]
            }

with open("scratch/converter_info.txt", "w", encoding="utf-8") as f:
    f.write(f"Source dir: {src_dir}\n")
    f.write(json.dumps(info, indent=2, ensure_ascii=False))

print("Written converter info to scratch/converter_info.txt successfully.")
