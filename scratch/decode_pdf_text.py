import sys
import os
import pypdf

# Add scratch to path for conversion
sys.path.append(os.path.join(os.getcwd(), 'scratch'))
from convert_docx_to_unicode import process_line

pdf_path = r"d:\rental pro\new\kannada pdf.pdf"
reader = pypdf.PdfReader(pdf_path)
print(f"Total pages: {len(reader.pages)}")

with open(r"d:\rental pro\new\scratch\pdf_decoded_unicode.txt", "w", encoding="utf-8") as out:
    for idx, page in enumerate(reader.pages):
        raw_text = page.extract_text() or ""
        decoded_lines = []
        for line in raw_text.split('\n'):
            if line.strip():
                decoded_lines.append(process_line(line))
            else:
                decoded_lines.append("")
        decoded_text = '\n'.join(decoded_lines)
        out.write(f"=== PAGE {idx+1} ===\n{decoded_text}\n\n")

print("PDF decoded text written to scratch/pdf_decoded_unicode.txt")
