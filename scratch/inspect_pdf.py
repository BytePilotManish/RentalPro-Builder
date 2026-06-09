import os

pdf_path = r"d:\rental pro\new\kannada pdf.pdf"
if os.path.exists(pdf_path):
    print(f"File size: {os.path.getsize(pdf_path)} bytes")
    # Let's try importing some standard PDF reading packages.
    # We can try pypdf, pdfplumber, fitz (PyMuPDF), etc.
    try:
        import pypdf
        reader = pypdf.PdfReader(pdf_path)
        print(f"pypdf: Total pages: {len(reader.pages)}")
        text = ""
        for i, page in enumerate(reader.pages):
            page_text = page.extract_text()
            print(f"--- Page {i+1} Text (Sample) ---")
            print(repr(page_text[:400]))
            text += page_text + "\n"
        with open("scratch/pdf_text.txt", "w", encoding="utf-8") as f:
            f.write(text)
        print("Successfully wrote extracted text to scratch/pdf_text.txt")
    except Exception as e:
        print(f"Failed with pypdf: {e}")
else:
    print("PDF file not found.")
