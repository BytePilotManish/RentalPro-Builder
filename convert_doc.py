import os
import win32com.client

def convert_doc_to_docx():
    word = None
    try:
        # Get absolute paths
        current_dir = os.path.dirname(os.path.abspath(__file__))
        doc_path = os.path.join(current_dir, "RENTAL AGREEMENT.doc")
        docx_path = os.path.join(current_dir, "RENTAL AGREEMENT.docx")
        
        print(f"Converting:\n  Source: {doc_path}\n  Target: {docx_path}")
        
        if not os.path.exists(doc_path):
            print("Error: RENTAL AGREEMENT.doc not found.")
            return
            
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        
        doc = word.Documents.Open(doc_path)
        # FileFormat=16 is for wdFormatXMLDocument (.docx)
        doc.SaveAs2(docx_path, FileFormat=16)
        doc.Close()
        print("Conversion successful!")
        
    except Exception as e:
        print(f"Error during conversion: {e}")
    finally:
        if word:
            word.Quit()

if __name__ == "__main__":
    convert_doc_to_docx()
