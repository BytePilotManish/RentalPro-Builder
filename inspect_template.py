import os
import docx

def inspect_template():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, "TEMPLATE.docx")
    
    doc = docx.Document(path)
    print("=== TEMPLATE PARAGRAPHS ===")
    for idx, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if text:
            print(f"P{idx}: {text}")

if __name__ == "__main__":
    inspect_template()
