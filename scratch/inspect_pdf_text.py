import os

# Check which PDF libraries are installed
try:
    import pypdf
    print("[OK] pypdf is installed")
except ImportError:
    try:
        import PyPDF2 as pypdf
        print("[OK] PyPDF2 is installed")
    except ImportError:
        pypdf = None
        print("[NO] pypdf/PyPDF2 is not installed")

try:
    import pdfplumber
    print("[OK] pdfplumber is installed")
except ImportError:
    pdfplumber = None
    print("[NO] pdfplumber is not installed")

# Try to extract text from d:\rental pro\new\kannada pdf.pdf
pdf_path = r"d:\rental pro\new\kannada pdf.pdf"
if os.path.exists(pdf_path):
    print(f"PDF exists: Size {os.path.getsize(pdf_path)} bytes")
    if pypdf:
        try:
            reader = pypdf.PdfReader(pdf_path)
            print(f"Total pages via pypdf: {len(reader.pages)}")
            for idx in range(len(reader.pages)):
                text = reader.pages[idx].extract_text()
                print(f"--- Page {idx+1} (Length: {len(text)}) ---")
                print(text[:300])
        except Exception as e:
            print(f"pypdf extraction failed: {e}")
    if pdfplumber:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                print(f"Total pages via pdfplumber: {len(pdf.pages)}")
                for idx, page in enumerate(pdf.pages):
                    text = page.extract_text() or ""
                    print(f"--- pdfplumber Page {idx+1} (Length: {len(text)}) ---")
                    print(text[:300])
        except Exception as e:
            print(f"pdfplumber extraction failed: {e}")
else:
    print("PDF not found")
