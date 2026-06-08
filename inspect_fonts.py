import os
import docx

def inspect_fonts(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(current_dir, filename)
    if not os.path.exists(path):
        print(f"File {filename} does not exist.")
        return
    
    doc = docx.Document(path)
    print(f"\n=== INSPECTING FONTS IN {filename} ===")
    
    # Check document-wide default style font size
    try:
        default_font_size = doc.styles['Normal'].font.size
        print(f"Normal Style Font Size: {default_font_size}")
    except Exception as e:
        print(f"Could not read Normal style font size: {e}")
        
    for idx, p in enumerate(doc.paragraphs):
        text = p.text.strip()
        if not text:
            continue
        p_font_size = p.style.font.size
        print(f"Paragraph {idx} (Style: {p.style.name}, Font Size: {p_font_size}): {text[:40]}...")
        for r_idx, run in enumerate(p.runs):
            if run.text.strip():
                print(f"  Run {r_idx} (Font Size: {run.font.size}, Bold: {run.font.bold}): '{run.text.strip()[:30]}'")

if __name__ == "__main__":
    inspect_fonts("RENTAL AGREEMENT.docx")
    inspect_fonts("TEMPLATE.docx")
