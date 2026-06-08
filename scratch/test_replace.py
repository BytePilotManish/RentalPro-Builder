import os
import sys
import docx
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import replace_placeholders

def run_test():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(current_dir)
    template_path = os.path.join(project_dir, "TEMPLATE.docx")
    output_docx = os.path.join(current_dir, "test_out.docx")
    
    doc = docx.Document(template_path)
    
    # 2 clauses instead of 9
    payload = {
        "AGREEMENT_DATE": "01ST Day of this April 2026",
        "AGREEMENT_PLACE": "Bangalore",
        "OWNER_NAME": "Mr. MANOJ M & SANCHITHA C J",
        "OWNER_PARENT": "S/O T Mahesh",
        "OWNER_AGE": "45",
        "OWNER_ADDRESS": "No,99,100 C Near Sri Kalikamba Temple, ChowdeshwariNagar, , Laggere, Bengaluru- 560 058",
        "TENANT_NAME": "Mr. RAJUGOWDA",
        "TENANT_PARENT": "S/O Subbegowda",
        "TENANT_AGE": "47",
        "TENANT_ADDRESS": "No. 18, 3rd Cross, Rajeev Gandhi Nagar, Laggere, Bengaluru-560 058",
        "PREMISES_ADDRESS": "No.99 & 100C, Near Sri Kalikamba Temple Chowdeshwari Nagar, Laggere, Bengaluru- 560 058",
        "PREMISES_DESCRIPTION": "One RCC Roofed Shops, with rolling Shutter and electricity, Toilet and water facility",
        "BUSINESS_NAME": "J S TRADERS",
        "LEASE_PERIOD": "eleven months",
        "LEASE_PERIOD_NUM": "11",
        "LEASE_END_DATE": "25/02/2027",
        "RENT_AMOUNT": "10,500.00",
        "RENT_AMOUNT_WORDS": "Ten Thousand Five Hundred",
        "RENT_PAYMENT_DAY": "15th",
        "ESCALATION_RATE": "5%",
        "DEPOSIT_AMOUNT": "50,000",
        "DEPOSIT_AMOUNT_WORDS": "Fifty Thousand",
        "DEPOSIT_MODE": "cash",
        "NOTICE_PERIOD": "three months",
        "OWNER_SIG_NAMES": "MANOJ M AND SANCHITHA C J",
        "TENANT_SIG_NAMES": "RAJUGOWDA",
        "AGREEMENT_CONDITIONS": [
            "This RENTAL AGREEMENT is for a period of {{LEASE_PERIOD}} from the date of execution of this agreement i.e., on {{LEASE_END_DATE}}.",
            "The OWNER has agreed to let out the said premises for a monthly rent of Rs.{{RENT_AMOUNT}} (Rupees {{RENT_AMOUNT_WORDS}} only)"
        ]
    }
    
    replace_placeholders(doc, payload)
    doc.save(output_docx)
    
    # Check paragraphs in generated doc
    print("=== GENERATED PARAGRAPHS ===")
    doc_new = docx.Document(output_docx)
    for idx, p in enumerate(doc_new.paragraphs):
        text = p.text.strip()
        if text:
            print(f"P{idx}: {text}")

if __name__ == "__main__":
    run_test()
