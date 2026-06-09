import docx
import os

def delete_paragraph(paragraph):
    p_element = paragraph._element
    p_element.getparent().remove(p_element)
    paragraph._element = None

def create_perfect_template():
    in_file = r"d:\rental pro\new\19-05-2026 - kan (2.docx"
    out_file = r"d:\rental pro\new\TEMPLATE_KAN.docx"
    
    if not os.path.exists(in_file):
        print("Source file not found")
        return
        
    doc = docx.Document(in_file)
    print(f"Original paragraphs: {len(doc.paragraphs)}")
    
    # Keep original indices 25 to 274 inclusive.
    end_idx = len(doc.paragraphs) - 1
    for idx in range(end_idx, 274, -1):
        delete_paragraph(doc.paragraphs[idx])
        
    for idx in range(24, -1, -1):
        delete_paragraph(doc.paragraphs[idx])
        
    print(f"Remaining paragraphs: {len(doc.paragraphs)}")
    
    # Formula for template index: template_idx = orig_idx - 25
    substitutions = {
        # === PART 1 ===
        26: [
            ("JgÀqÀÄ ¸Á«gÀzÀ E¥ÀàvÁÛgÀ£ÉÃ", "{{AGREEMENT_YEAR_WORDS}}"),
            ("ªÉÄÃ", "{{AGREEMENT_MONTH}}")
        ],
        27: [
            ("ºÀvÉÆÛA¨sÀvÀÄÛ (19-05-2026)", "{{AGREEMENT_DATE}}")
        ],
        28: [
            ("¯ÉÃmï.ZÀAzÀæ¥Àà.©", "{{OWNER_PARENT}}"),
            ("41", "{{OWNER_AGE}}"),
            ("²æÃ.µÀtÄäR¥Àà.©.¹", "{{OWNER_NAME}}")
        ],
        43: [
            ("52", "{{TENANT_AGE}}"),
            ("²æÃªÀÄw.¥ÁªÀðvÀªÀÄä", "{{TENANT_NAME}}")
        ],
        45: [
            ("£É® ªÀiÁºÀrAiÀÄ°ègÀÄªÀ Dgï.¹.¹ bÁªÀtÂAiÀÄÄ¼Àî ¥ÀÆªÀðzÀ ¨ÁV®Ä¼Àî, MAzÀÄ CrUÉ ªÀÄ£É, MAzÀÄ ºÁ¯ï, MAzÀÄ gÀÆªÀiï, ªÀÄvÀÄÛ ¨Ávï gÀÆªÀiï, ±ËZÁ®AiÀÄ, ºÁUÀÆ «zÀÄåvï «ÄÃlgï / ¤Ãj£À C£ÀÄPÀÆ®«gÀÄªÀ ªÁ¸ÀzÀ ªÀÄ£ÉAiÀÄ£ÀÄß,", "{{PREMISES_DESCRIPTION}}")
        ],
        47: [
            ("gÀÆ.20,000/- (E¥ÀàvÀÄÛ ¸Á«gÀ)   ", "gÀ.{{DEPOSIT_AMOUNT}}/- ({{DEPOSIT_AMOUNT_WORDS}})")
        ],
        48: [
            ("gÀÆ.4,500/- (£Á®ÄÌ ¸Á«gÀzÀ L£ÀÆgÀÄ)", "gÀ.{{RENT_AMOUNT}}/- ({{RENT_AMOUNT_WORDS}})")
        ],
        49: [
            ("15-01-2026", "{{LEASE_START_DATE}}"),
            ("11 (ºÀ£ÉÆßAzÀÄ)", "{{LEASE_PERIOD_NUM}} ({{LEASE_PERIOD}})")
        ],
        51: [
            ("5%", "{{ESCALATION_RATE}}")
        ],
        78: [
            ("11", "{{LEASE_PERIOD_NUM}}"),
            ("3 (ªÀÄÆgÀÄ)", "{{NOTICE_PERIOD_NUM}} ({{NOTICE_PERIOD}})")
        ],
        84: [
            ("¨ÁrUÉzÁgÀgÀ ¸À»", "{{TENANT_SIG_NAMES}}\n\n¨ÁrUÉzÁgÀgÀ ¸À»")
        ],
        91: [
            ("ªÀiÁ°ÃPÀgÀ ¸À»", "{{OWNER_SIG_NAMES}}\n\nªÀiÁ°ÃPÀgÀ ¸À»"),
        ],
        
        # === PART 2 ===
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
            ("²æÃ.ªÀÄÄ¤ºÀÄZÀÑAiÀÄå gÀªÀgÀ ªÀÄUÀ£ÁzÀ", "{{TENANT_PARENT}}"),
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
        ],

        # === PART 3 ===
        237: [
            ("JgÀqÀÄ ¸Á«gÀzÀ E¥ÀàvÁÛgÀÄ", "{{AGREEMENT_YEAR_WORDS}}"),
            ("ªÉÄÃ", "{{AGREEMENT_MONTH}}")
        ],
        238: [
            ("ºÀvÉÆÛA¨sÀvÀÄÛ (19-05-2026)", "{{AGREEMENT_DATE}}")
        ],
        240: [
            ("²æÃªÀÄw.£ÀA¢¤.PÉ", "{{TENANT_NAME}}"),
            ("²æÃ.±ÉÃRgï gÀªÀgÀ zsÀªÀÄð¥ÀwßAiÀiÁzÀ", "{{TENANT_PARENT}}"),
            ("39", "{{TENANT_AGE}}")
        ],
        241: [
            ("²æÃ.¸ÁUÀgï.eÉ.r", "{{OWNER_NAME}}"),
            ("²æÃ.zÁåªÀ¥Àà gÀªÀgÀ ªÀÄUÀ£ÁzÀ", "{{OWNER_PARENT}}"),
            ("30", "{{OWNER_AGE}}")
        ],
        248: [
            ("gÀÆ.28,000/- (E¥ÀàvÉÛAlÄ ¸Á«gÀ)", "gÀ.{{RENT_AMOUNT}}/- ({{RENT_AMOUNT_WORDS}})")
        ],
        249: [
            ("01-04-2026", "{{LEASE_START_DATE}}")
        ],
        251: [
            ("MAzÀÄ (1) wAUÀ¼ÀÄ", "{{NOTICE_PERIOD_NUM}} ({{NOTICE_PERIOD}})")
        ],
        264: [
            ("01-04-2026", "{{LEASE_START_DATE}}")
        ],
        268: [
            ("ªÁºÀ£ÀzÀ ªÀiÁ°ÃPÀgÀÄ ¸À»", "{{OWNER_SIG_NAMES}}\n\nªÁºÀ£ÀzÀ ªÀiÁ°ÃPÀgÀÄ ¸À»")
        ],
        274: [
            ("ªÁºÀ£ÀzÀ ¨sÉÆÃUÀåzÁgÀgÀÄ ¸À»", "{{TENANT_SIG_NAMES}}\n\nªÁºÀ£ÀzÀ ¨sÉÆÃUÀåzÁgÀgÀÄ ¸À»")
        ]
    }
    
    # Extra field additions for specific paragraphs
    substitutions[48].append(("28", "{{RENT_PAYMENT_DAY}}"))
    substitutions[155].append(("28", "{{RENT_PAYMENT_DAY}}"))
    
    # Process replacements using a unique list of indices to prevent duplicate edits
    unique_indices = sorted(list(set(list(substitutions.keys()) + [28, 43, 45, 135, 150, 152, 240, 241])))
    for orig_idx in unique_indices:
        new_idx = orig_idx - 25
        p = doc.paragraphs[new_idx]
        text = p.text
        
        # Dynamic address extraction for all parts:
        if orig_idx == 28:
            end_addr_idx = text.find(" JA§")
            if end_addr_idx != -1:
                owner_addr_str = text[:end_addr_idx]
                text = text.replace(owner_addr_str, "{{OWNER_ADDRESS}}")
        elif orig_idx == 43:
            end_addr_idx = text.find(" JA§")
            if end_addr_idx != -1:
                tenant_addr_str = text[:end_addr_idx]
                text = text.replace(tenant_addr_str, "{{TENANT_ADDRESS}}")
        elif orig_idx == 45:
            start_token = " M\xbc\xc0\xa5\xac\xd6g\xc0\xac\xaa\xc0 " # " M¼À¥ÀnÖgÀÄªÀ "
            end_token = " JA\xa7" # " JA§"
            start_addr_idx = text.find(start_token)
            end_addr_idx = text.find(end_token)
            if start_addr_idx != -1 and end_addr_idx != -1:
                premises_addr_str = text[start_addr_idx + len(start_token) : end_addr_idx]
                text = text.replace(premises_addr_str, "{{PREMISES_ADDRESS}}")
        elif orig_idx == 135:
            target_token = "  \xb2\xe6\xc3\xaa\xc0\xc4w.dAi\xc0\xc4\xaeP\xc0\xeb\xf6\xe4\xaa\xc0\xc4\xe4"
            split_idx = text.find(target_token)
            if split_idx != -1:
                owner_addr_str = text[:split_idx]
                text = text.replace(owner_addr_str, "{{OWNER_ADDRESS}}")
        elif orig_idx == 150:
            target_token = " \xb2\xe6\xc3.\xaa\xc0\xc4\xc4\xa4\xba\xc0\xc4Z\xc0\xd1Ai\xc0\xc4\xe5"
            split_idx = text.find(target_token)
            if split_idx != -1:
                tenant_addr_str = text[:split_idx]
                text = text.replace(tenant_addr_str, "{{TENANT_ADDRESS}}")
        elif orig_idx == 152:
            desc_start_token = " P\xc0l\xd6q\xc0z\xc0"
            split_idx = text.find(desc_start_token)
            if split_idx != -1:
                addr_token = " \xa8\xc9AU\xc0\xbc\xc0\xc6g\xc0\xc4"
                addr_start = text.find(addr_token)
                if addr_start != -1:
                    premises_addr_str = text[addr_start + 1 : split_idx]
                    text = text.replace(premises_addr_str, "{{PREMISES_ADDRESS}}")
                premises_desc_str = text[text.find(desc_start_token) + 1 :]
                text = text.replace(premises_desc_str, "{{PREMISES_DESCRIPTION}}")
        elif orig_idx == 240:
            # Split before ªÁ¸ÀªÁVgÀÄªÀ in Nudi representation
            target_token = " \xaa\xc1\xb8\xc0\xaa\xc1Vg\xc0\xc4\xaa\xc0"
            split_idx = text.find(target_token)
            if split_idx != -1:
                tenant_addr_str = text[:split_idx]
                text = text.replace(tenant_addr_str, "{{TENANT_ADDRESS}}")
        elif orig_idx == 241:
            # Split before ªÁ¸ÀªÁVgÀÄªÀ in Nudi representation
            target_token = " \xaa\xc1\xb8\xc0\xaa\xc1Vg\xc0\xc4\xaa\xc0"
            split_idx = text.find(target_token)
            if split_idx != -1:
                owner_addr_str = text[:split_idx]
                text = text.replace(owner_addr_str, "{{OWNER_ADDRESS}}")
                
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
    print(f"Perfect full template successfully re-created and saved to {out_file}.")

if __name__ == "__main__":
    create_perfect_template()
