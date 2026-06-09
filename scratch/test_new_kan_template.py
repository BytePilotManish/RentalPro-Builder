import docx
import os

def delete_paragraph(paragraph):
    p_element = paragraph._element
    p_element.getparent().remove(p_element)
    paragraph._element = None

def create_kan_template_2():
    in_file = r"d:\rental pro\new\19-05-2026 - kan (2.docx"
    out_file = r"d:\rental pro\new\TEMPLATE_KAN.docx"
    
    if not os.path.exists(in_file):
        print("Source file not found")
        return
        
    doc = docx.Document(in_file)
    print(f"Original paragraphs: {len(doc.paragraphs)}")
    
    # Keep original indices 132 to 191 inclusive.
    end_idx = len(doc.paragraphs) - 1
    for idx in range(end_idx, 191, -1):
        delete_paragraph(doc.paragraphs[idx])
        
    for idx in range(131, -1, -1):
        delete_paragraph(doc.paragraphs[idx])
        
    print(f"Remaining paragraphs: {len(doc.paragraphs)}")
    
    # Let's map substitutions:
    # Notice: these indices are 0-based in the remaining document!
    # Original idx 132 becomes 0, 133 becomes 1, etc.
    # Formula: template_idx = orig_idx - 132
    
    substitutions = {
        133: [
            ("JgÀqÀÄ ¸Á«gÀzÀ E¥ÀàvÁÛgÀ£ÉÃ", "{{AGREEMENT_YEAR_WORDS}}"),
            ("ªÉÄÃ", "{{AGREEMENT_MONTH}}")
        ],
        134: [
            ("ºÀvÉÆÛA¨sÀvÀÄÛ (19-05-2026)", "{{AGREEMENT_DATE}}")
        ],
        135: [
            ("²æÃªÀÄw.dAiÀÄ®PÀëöäªÀÄä", "{{OWNER_NAME}}")
        ],
        150: [
            ("²æÃªÀÄw.£ÀgÀ¸ÀªÀÄä", "{{TENANT_NAME}}"),
            ("²æÃ.ªÀÄÄ¤ºÀÄZÀÑAiÀÄå gÀªÀgÀ ªÀÄUÀ£ÁzÀ", "{{TENANT_PARENT}}"), # Guardian info
            ("55", "{{TENANT_AGE}}")
        ],
        154: [
            ("g\xc0\xc6.30,000/- (\xaa\xc0\xc4\xc6\xaa\xc0v\xc0\xc4\xdb \xb8\xc1\xabg\xc0)", "g\xc0.{{DEPOSIT_AMOUNT}}/- ({{DEPOSIT_AMOUNT_WORDS}})")
        ],
        155: [
            ("g\xc0\xc6.4,000/- (\xa3\xc1\xae\xc4\xcc \xb8\xc1\xabg\xc0)", "g\xc0.{{RENT_AMOUNT}}/- ({{RENT_AMOUNT_WORDS}})")
        ],
        156: [
            ("10-01-2026", "{{LEASE_START_DATE}}"),
            ("11 (\xba\xc0\xa3\xc9\xc6\xdfAz\xc0\xc4)", "{{LEASE_PERIOD_NUM}} ({{LEASE_PERIOD}})")
        ],
        158: [
            ("5%", "{{ESCALATION_RATE}}")
        ],
        178: [
            ("11", "{{LEASE_PERIOD_NUM}}"),
            ("3 (\xaa\xc0\xc4\xc6g\xc0\xc4)", "{{NOTICE_PERIOD_NUM}} ({{NOTICE_PERIOD}})")
        ],
        184: [
            ("\xa8\xc1rU\xc9z\xc1g\xc0g\xc0 \xb8\xc0\xbb", "{{TENANT_SIG_NAMES}}\n\n\xa8\xc1rU\xc9z\xc1g\xc0g\xc0 \xb8\xc0\xbb")
        ],
        191: [
            ("\xaa\xc0i\xc1\xb0\xc3P\xc0g\xc0 \xb8\xc0\xbb", "{{OWNER_SIG_NAMES}}\n\n\xaa\xc0i\xc1\xb0\xc3P\xc0g\xc0 \xb8\xc0\xbb")
        ]
    }
    
    substitutions[155].append(("28", "{{RENT_PAYMENT_DAY}}"))
    
    # Process replacements
    for orig_idx in sorted(list(set(list(substitutions.keys()) + [135, 150, 152]))):
        new_idx = orig_idx - 132
        p = doc.paragraphs[new_idx]
        text = p.text
        
        # Dynamic address extraction for second agreement:
        if orig_idx == 135:
            # Split before Owner Name: double space + \xb2\xe6\xc3\xaa\xc0\xc4w.dAi\xc0\xc4\xaeP\xc0\xeb\xf6\xe4\xaa\xc0\xc4\xe4
            target_token = "  \xb2\xe6\xc3\xaa\xc0\xc4w.dAi\xc0\xc4\xaeP\xc0\xeb\xf6\xe4\xaa\xc0\xc4\xe4"
            split_idx = text.find(target_token)
            if split_idx != -1:
                owner_addr_str = text[:split_idx]
                print(f"Extracted Owner Address: {owner_addr_str.encode('ascii', 'backslashreplace').decode('ascii')}")
                text = text.replace(owner_addr_str, "{{OWNER_ADDRESS}}")
        elif orig_idx == 150:
            # Split before Tenant Parent: \xb2\xe6\xc3.\xaa\xc0\xc4\xc4\xa4\xba\xc0\xc4Z\xc0\xd1Ai\xc0\xc4\xe5
            target_token = " \xb2\xe6\xc3.\xaa\xc0\xc4\xc4\xa4\xba\xc0\xc4Z\xc0\xd1Ai\xc0\xc4\xe5"
            split_idx = text.find(target_token)
            if split_idx != -1:
                tenant_addr_str = text[:split_idx]
                print(f"Extracted Tenant Address: {tenant_addr_str.encode('ascii', 'backslashreplace').decode('ascii')}")
                text = text.replace(tenant_addr_str, "{{TENANT_ADDRESS}}")
        elif orig_idx == 152:
            # Premises description and address extraction
            # Address is everything from start of text until the description starts.
            # In CP1252: description starts with " P\xc0l\xd6q\xc0z\xc0" (which maps to " \u0c95\u0c9f\u0ccd\u0ca1\u0ca1\u0ca6... \u0ca8\u0cc6\u0cb2 මහಡಿಯ...")
            # Let's inspect raw text of paragraph 152 and search for description start
            desc_start_token = " P\xc0l\xd6q\xc0z\xc0"
            split_idx = text.find(desc_start_token)
            if split_idx != -1:
                # The text before is "Dz\xc1V \xa4\xaa\xc0\xc4\xe4 \xb8\xc0A\xa5\xc0\xc6t\xf0 \xaa\xc0i\xc1\xb0\xc3P\xc0v\xc0\xe9P\xc9\xcc \xba\xc1U\xc0\xc6 \xba\xc0P\xc0\xcc\xa8s\xc1z\xc0\xe5v\xc9U\xc9 M\xbc\xc0\xa5\xc0n\xd6g\xc0\xc4\xaa\xc0 \xa8\xc9AU\xc0\xbc\xc0\xc6g\xc0\xc4 \u2013 560096, \xa3\xc0A\xa2\xa4 \xaf\xc9\xc3Om\xef, P\xc0Ap\xc3g\xc0\xaa\xc0\xa3\xc0U\xc0g\xc0, 9\xa3\xc9\xc3 \xaa\xc0\xc4\xc4R\xe5g\xc0\xb8\xc9\xdb, 8\xa3\xc9\xc3 Cq\xc0\xd8g\xc0\xb8\xc9\xdb, 860\xa3\xc9\xc3 \xa3\xc0A\xa7g\xc0\xc4\xbc\xc0\xee"
                # In Kannada: "ಆದಾಗಿ ನನ್ನ ಸಂಪೂರ್ಣ ಮಾಲೀಕತ್ವಕ್ಕೆ ಹಾಗೂ ಹಕ್ಕಬಾದ್ಯತೆಗೆ ಒಳಪಟ್ಟಿರುವ ಬೆಂಗಳೂರು – 560096, ನಂದಿನಿ ಲೇಔಟ್..."
                # Wait, we want to extract the premises address which is "ಬೆಂಗಳೂರು – 560096, ನಂದಿನಿ ಲೇಔಟ್, ಕಂಠೀರವನಗರ, 9ನೇ ಮುಖ್ಯರಸ್ತೆ, 8ನೇ ಅಡ್ಡರಸ್ತೆ, 860ನೇ ನಂಬರುಳ್ಳ"
                # Let's find " \xa8\xc9AU\xc0\xbc\xc0\xc6g\xc0\xc4" (which is " ಬೆಂಗಳೂರು")
                addr_token = " \xa8\xc9AU\xc0\xbc\xc0\xc6g\xc0\xc4"
                addr_start = text.find(addr_token)
                if addr_start != -1:
                    premises_addr_str = text[addr_start + 1 : split_idx]
                    print(f"Extracted Premises Address: {premises_addr_str.encode('ascii', 'backslashreplace').decode('ascii')}")
                    text = text.replace(premises_addr_str, "{{PREMISES_ADDRESS}}")
                
                # The description is from split_idx to the end of the text
                premises_desc_str = text[text.find(desc_start_token) + 1 :]
                print(f"Extracted Premises Description: {premises_desc_str.encode('ascii', 'backslashreplace').decode('ascii')}")
                text = text.replace(premises_desc_str, "{{PREMISES_DESCRIPTION}}")
                
        subs = substitutions.get(orig_idx, [])
        for search_nudi, replace_nudi in subs:
            if search_nudi in text:
                print(f"Replacing in paragraph {orig_idx}: {search_nudi.encode('ascii', 'backslashreplace').decode('ascii')} -> {replace_nudi}")
                text = text.replace(search_nudi, replace_nudi)
            else:
                print(f"[WARNING] Match failed in paragraph {orig_idx} for string {search_nudi.encode('ascii', 'backslashreplace').decode('ascii')}.")
                
        p.text = text
        for run in p.runs:
            run.font.name = 'Nudi Akshar-02'
            run.font.size = docx.shared.Pt(12)
            
    doc.save(out_file)
    print("New template created successfully.")

if __name__ == "__main__":
    create_kan_template_2()
