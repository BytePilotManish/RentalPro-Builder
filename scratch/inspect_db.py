import sqlite3
import json
import docx
import os

def inspect_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, docx_path, pdf_path, agreement_data FROM agreements WHERE id = 7')
    row = cursor.fetchone()
    if not row:
        print("Agreement ID 7 not found.")
        return
        
    agreement_id = row[0]
    title = row[1]
    docx_path = row[2]
    pdf_path = row[3]
    data = json.loads(row[4])
    conditions = data.get("AGREEMENT_CONDITIONS", [])
    
    print(f"ID {agreement_id}: {title}")
    print(f"  docx_path: {docx_path}")
    print(f"  pdf_path: {pdf_path}")
    print(f"  Conditions in DB data: {len(conditions)}")
    for idx, cond in enumerate(conditions):
        print(f"    {idx+1}. {cond[:60]}...")
        
    if docx_path and os.path.exists(docx_path):
        print("\n=== Paragraphs in generated DOCX file ===")
        doc = docx.Document(docx_path)
        in_terms = False
        for idx, p in enumerate(doc.paragraphs):
            text = p.text.strip()
            if "terms and conditions" in text.lower():
                in_terms = True
                print(f"P{idx}: {text}")
                continue
            if in_terms:
                if "IN WITNESSES THEREOF" in text:
                    in_terms = False
                    print(f"P{idx}: {text}")
                    continue
                print(f"P{idx}: {text}")
    else:
        print(f"DOCX file does not exist at {docx_path}")
        
    conn.close()

if __name__ == "__main__":
    inspect_db()
