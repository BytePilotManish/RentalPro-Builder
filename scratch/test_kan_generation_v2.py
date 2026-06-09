import docx
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import replace_placeholders
from kannada_helper import unicode_to_nudi

def test_kan_gen():
    template_path = "TEMPLATE_KAN.docx"
    output_docx = "scratch/test_kan_output_v2.docx"
    
    if not os.path.exists(template_path):
        print("TEMPLATE_KAN.docx not found!")
        return
        
    doc = docx.Document(template_path)
    
    unicode_payload = {
        "AGREEMENT_YEAR_WORDS": "ಎರಡು ಸಾವಿರದ ಇಪ್ಪತ್ತಾರನೇ",
        "AGREEMENT_MONTH": "ಮೇ",
        "AGREEMENT_DATE": "ಹತ್ತೊಂಬತ್ತು (19-05-2026)",
        "OWNER_NAME": "ಶ್ರೀಮತಿ.ಜಯಲಕ್ಷ್ಮಮ್ಮ",
        "OWNER_PARENT": "",
        "OWNER_AGE": "",
        "OWNER_ADDRESS": "ಬೆಂಗಳೂರು – 560096, ನಂದಿನಿ ಲೇಔಟ್, ಕಂಠೀರವನಗರ, 9ನೇ ಮುಖ್ಯರಸ್ತೆ, 8ನೇ ಅಡ್ಡರಸ್ತೆ, 860ನೇ ನಂಬರುಳ್ಳ ಮನೆಯಲ್ಲಿ ವಾಸವಾಗಿರುವ",
        "TENANT_NAME": "ಶ್ರೀಮತಿ.ನರಸಮ್ಮ",
        "TENANT_PARENT": "ಶ್ರೀ.ಮುನಿಹುಚ್ಚಯ್ಯ ರವರ ಮಗನಾದ",
        "TENANT_AGE": "55",
        "TENANT_ADDRESS": "ಬೆಂಗಳೂರು – 560096, ನಂದಿನಿ ಲೇಔಟ್, ಕಂಠೀರವನಗರ, 9ನೇ ಮುಖ್ಯರಸ್ತೆ, 8ನೇ ಅಡ್ಡರಸ್ತೆ, 860ನೇ ನಂಬರುಳ್ಳ ಮನೆಯಲ್ಲಿ ವಾಸವಾಗಿರುವ",
        "PREMISES_ADDRESS": "ಬೆಂಗಳೂರು – 560096, ನಂದಿನಿ ಲೇಔಟ್, ಕಂಠೀರವನಗರ, 9ನೇ ಮುಖ್ಯರಸ್ತೆ, 8ನೇ ಅಡ್ಡರಸ್ತೆ, 860ನೇ ನಂಬರುಳ್ಳ",
        "PREMISES_DESCRIPTION": "ನೆಲ ಮಹಡಿಯಲ್ಲಿರುವ ಆರ್.ಸಿ.ಸಿ ಛಾವಣಿಯುಳ್ಳ ಉತ್ತರದ ಬಾಗಿಲುಳ್ಳ, ಒಂದು ಅಡುಗೆ ಮನೆ, ಒಂದು ಹಾಲ್, ಮತ್ತು ಬಾತ್ ರೂಮ್, ಶೌಚಾಲಯ, ಹಾಗೂ ವಿದ್ಯುತ್ ಮೀಟರ್ / ನೀರಿನ ಅನುಕೂಲವಿರುವ ವಾಸದ ಮನೆಯನ್ನು",
        "DEPOSIT_AMOUNT": "30,000",
        "DEPOSIT_AMOUNT_WORDS": "ಮೂವತ್ತು ಸಾವಿರ",
        "RENT_AMOUNT": "4,000",
        "RENT_AMOUNT_WORDS": "ನಾಲ್ಕು ಸಾವಿರ",
        "RENT_PAYMENT_DAY": "28",
        "LEASE_START_DATE": "10-01-2026",
        "LEASE_PERIOD_NUM": "11",
        "LEASE_PERIOD": "ಹನ್ನೊಂದು",
        "ESCALATION_RATE": "5%",
        "NOTICE_PERIOD_NUM": "3",
        "NOTICE_PERIOD": "ಮೂರು",
        "OWNER_SIG_NAMES": "ಜಯಲಕ್ಷ್ಮಮ್ಮ",
        "TENANT_SIG_NAMES": "ನರಸಮ್ಮ"
    }
    
    # Translate payload to Nudi ASCII
    translated_payload = {}
    for k, v in unicode_payload.items():
        translated_payload[k] = unicode_to_nudi(v)
        
    safe_uni = unicode_payload['OWNER_NAME'].encode('ascii', 'backslashreplace').decode('ascii')
    safe_nudi = translated_payload['OWNER_NAME'].encode('ascii', 'backslashreplace').decode('ascii')
    print(f"  Owner Unicode: {safe_uni} -> Nudi: {safe_nudi}")
    
    replace_placeholders(doc, translated_payload, font_name="Nudi Akshar-02")
    doc.save(output_docx)
    print(f"Saved generated document to {output_docx}")
    
    # Inspect generated paragraphs to verify replacement happened and font is set
    doc_new = docx.Document(output_docx)
    print("\nVerifying replaced runs:")
    found_owner = False
    for idx, p in enumerate(doc_new.paragraphs):
        # Jayalakshmamma maps to Nudi: dAiÀÄ®PÀëöäªÀÄä or containing dAiÀÄ
        if "dAiÀÄ" in p.text:
            found_owner = True
            print(f"Paragraph {idx} contains owner name!")
            for r in p.runs:
                if "dAiÀÄ" in r.text:
                    print(f"  Run text: {repr(r.text)} | Font Name: {r.font.name} | Size: {r.font.size}")
                    
    if found_owner:
        print("Success! Verification passed.")
    else:
        print("Warning: Replaced owner name not found in the output document.")

if __name__ == "__main__":
    test_kan_gen()
