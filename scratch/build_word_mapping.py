import os
import sys
import docx
import json

# Import mapping/functions from scratch.convert_docx_to_unicode
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scratch.convert_docx_to_unicode import process_line

def build_mapping():
    in_file = r"d:\rental pro\new\19-05-2026 - kan (2.docx"
    if not os.path.exists(in_file):
        print("File not found")
        return
        
    doc = docx.Document(in_file)
    word_map = {}
    
    for p in doc.paragraphs:
        if not p.text.strip():
            continue
        # Split into words
        nudi_words = p.text.split()
        for nw in nudi_words:
            nw_clean = nw.strip(".,()[]{}<>:;-–\"' ಃ")
            if not nw_clean:
                continue
            uni = process_line(nw_clean)
            if uni and nw_clean:
                word_map[uni] = nw_clean

    # Also map some basic characters and numbers
    # Save the mapping
    with open("scratch/word_mapping.json", "w", encoding="utf-8") as f:
        json.dump(word_map, f, indent=2, ensure_ascii=False)
        
    print(f"Built mapping with {len(word_map)} words.")

if __name__ == "__main__":
    build_mapping()
