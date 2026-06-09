import re
import json
import os

# Load word mapping dictionary from document for reference/exact matches
word_map_path = "scratch/word_mapping.json"
word_map = {}
if os.path.exists(word_map_path):
    with open(word_map_path, "r", encoding="utf-8") as f:
        word_map = json.load(f)

# Hardcoded character mappings matching scratch/convert_docx_to_unicode.py
vowels_map = {
    "ಅ": "C", "ಆ": "D", "ಇ": "E", "ಈ": "F", "ಉ": "G", "ಊ": "H",
    "ಋ": "IÄ", "ಎ": "J", "ಏ": "K", "ಐ": "L", "ಒ": "M", "ಓ": "N", "ಔ": "O"
}

consonants_map = {
    "ಕ": {"base": "PÀ", "halant": "Pï", "aa": "PÁ", "i": "Q", "e": "PÉ", "au": "PË"},
    "ಖ": {"base": "R", "halant": "Sï", "aa": "SÁ", "i": "T", "e": "SÉ", "au": "SË"},
    "ಗ": {"base": "UÀ", "halant": "Uï", "aa": "UÁ", "i": "V", "e": "UÉ", "au": "UË"},
    "ಘ": {"base": "WÀ", "halant": "Wï", "aa": "WÁ", "i": "X", "e": "WÉ", "au": "WË"},
    "ಞ": {"base": "k", "halant": "k", "aa": "k", "i": "k", "e": "k", "au": "k"},
    "ಚ": {"base": "ZÀ", "halant": "Zï", "aa": "ZÁ", "i": "a", "e": "ZÉ", "au": "Zೌ"},
    "ಛ": {"base": "bÀ", "halant": "bï", "aa": "bÁ", "i": "c", "e": "bÉ", "au": "bË"},
    "ಜ": {"base": "d", "halant": "eï", "aa": "eÁ", "i": "f", "e": "eÉ", "au": "eË"},
    "ಝ": {"base": "gÀhÄ", "halant": "gÀhiï", "aa": "gÀhiÁ", "i": "jhÄ", "e": "gÉhÄ", "au": "gÀhiË"},
    "ಞ": {"base": "Y", "halant": "Y", "aa": "Y", "i": "Y", "e": "Y", "au": "Y"},
    "ಟ": {"base": "l", "halant": "mï", "aa": "mÁ", "i": "n", "e": "mÉ", "au": "mË"},
    "ಠ": {"base": "oÀ", "halant": "oï", "aa": "oÁ", "i": "p", "e": "oÉ", "au": "oË"},
    "ಡ": {"base": "qÀ", "halant": "qï", "aa": "qÁ", "i": "r", "e": "qÉ", "au": "qೌ"},
    "ಢ": {"base": "qsÀ", "halant": "qsï", "aa": "qsÁ", "i": "rü", "e": "qsÉ", "au": "qsË"},
    "ಣ": {"base": "t", "halant": "uï", "aa": "uÁ", "i": "tÂ", "e": "uÉ", "au": "uË"},
    "ತ": {"base": "vÀ", "halant": "vï", "aa": "vÁ", "i": "w", "e": "vÉ", "au": "vË"},
    "ಥ": {"base": "xÀ", "halant": "xï", "aa": "xÁ", "i": "y", "e": "xÉ", "au": "xË"},
    "ದ": {"base": "zÀ", "halant": "zï", "aa": "zÁ", "i": "¢", "e": "zÉ", "au": "zË"},
    "ಧ": {"base": "zsÀ", "halant": "zsï", "aa": "zsÁ", "i": "¢ü", "e": "zsÉ", "au": "zsË"},
    "ನ": {"base": "£À", "halant": "£ï", "aa": "£Á", "i": "¤", "e": "£É", "au": "£Ë"},
    "ಪ": {"base": "¥À", "halant": "¥ï", "aa": "¥Á", "i": "¦", "e": "¥É", "au": "¥Ë"},
    "ಫ": {"base": "¥sÀ", "halant": "¥sï", "aa": "¥sÁ", "i": "¦ü", "e": "¥sÉ", "au": "¥sË"},
    "ಬ": {"base": "§", "halant": "¨ï", "aa": "¨Á", "i": "©", "e": "¨É", "au": "¨Ë"},
    "ಭ": {"base": "¨sÀ", "halant": "¨sï", "aa": "¨sÁ", "i": "©ü", "e": "¨sÉ", "au": "¨sË"},
    "ಮ": {"base": "ªÀÄ", "halant": "ªÀiï", "aa": "ªÀiÁ", "i": "«Ä", "e": "ªÉÄ", "au": "ªÀiË"},
    "ಯ": {"base": "AiÀÄ", "halant": "AiÀiï", "aa": "AiÀiÁ", "i": "¬Ä", "e": "AiÉÄ", "au": "AiÀiË"},
    "ರ": {"base": "gÀ", "halant": "gï", "aa": "gÁ", "i": "j", "e": "gÉ", "au": "gË"},
    "ಲ": {"base": "®", "halant": "¯ï", "aa": "¯Á", "i": "°", "e": "¯É", "au": "¯Ë"},
    "ವ": {"base": "ªÀ", "halant": "ªï", "aa": "ªÁ", "i": "«", "e": "ªÉ", "au": "ªË"},
    "ಶ": {"base": "±À", "halant": "±ï", "aa": "±Á", "i": "²", "e": "±É", "au": "±Ë"},
    "ಷ": {"base": "µÀ", "halant": "µï", "aa": "µÁ", "i": "¶", "e": "µÉ", "au": "µË"},
    "ಸ": {"base": "¸À", "halant": "¸ï", "aa": "¸Á", "i": "¹", "e": "¸É", "au": "¸Ë"},
    "ಹ": {"base": "ºÀ", "halant": "ºï", "aa": "ºÁ", "i": "»", "e": "ºÉ", "au": "ºË"},
    "ಳ": {"base": "¼À", "halant": "¼ï", "aa": "¼Á", "i": "½", "e": "¼É", "au": "¼ೌ"}
}

# Special override/manual overrides from convert_docx_to_unicode mapping
special_consonant_combos = {
    # e.g. "ಯಿ": "¬Ä", "ಯು": "0iÀÄÄ", "ಯೊ": "0iÉÆ" etc.
    ("ಯ", "ಿ"): "¬Ä",
    ("ಯ", "ು"): "0iÀÄÄ",
    ("ಯ", "ೊ"): "0iÉÆ",
    ("ಯ", "ೋ"): "0iÉÆÃ",
    ("ವ", "ು"): "ªÀÅ",
    ("ವ", "ೂ"): "ªÀÇ",
}

vattakshara_map = {
    "ಕ": "Ì", "ಖ": "Í", "ಗ": "Î", "ಘ": "Ï", "ಞ": "Õ", "ಚ": "Ñ", "ಛ": "Ò", "ಜ": "Ó",
    "ಝ": "Ô", "ಟ": "Ö", "ಠ": "×", "ಡ": "Ø", "ಢ": "Ù", "ಣ": "Ú", "ತ": "Û", "ಥ": "Ü",
    "ದ": "Ý", "ಧ": "Þ", "ನ": "ß", "ಪ": "à", "ಫ": "á", "ಬ": "â", "ಭ": "ã", "ಮ": "ä",
    "ಯ": "å", "ರ": "æ", "ಲ": "è", "ವ": "é", "ಶ": "ê", "ಷ": "ë", "ಸ": "ì", "ಹ": "í",
    "ಳ": "î"
}

def unicode_to_nudi_word(word):
    # If the word is already in our dictionary, return it!
    if word in word_map:
        return word_map[word]
        
    # Segment word into syllables
    # Consonant C, Halant H, Matra M, Sign S
    C = r"[\u0c95-\u0cb9\u0cb3\u0cde]"
    V = r"[\u0c85-\u0c94\u0ce0\u0ce1]"
    M = r"[\u0cbe-\u0cc4\u0cc6-\u0cc8\u0cca-\u0ccc\u0cd5\u0cd6]"
    H = r"\u0ccd"
    S = r"[\u0c82\u0c83]"
    
    # Syllable patterns
    # pattern 1: Consonant cluster with optional matra and optional anusvara
    # pattern 2: Vowel with optional anusvara
    pattern = re.compile(
        f"({C}{H}(?:\u200d)?{C}(?:{H}(?:\u200d)?{C})*{M}?{S}?|"
        f"{C}{M}?{S}?|"
        f"{V}{S}?|"
        f"[0-9\u0ce6-\u0cef.,/()\-–\\[\\]]+|"
        f".)"
    )
    
    syllables = pattern.findall(word)
    nudi_syllables = []
    
    for syl in syllables:
        if not syl.strip():
            nudi_syllables.append(syl)
            continue
            
        # Check if numbers or special chars
        if re.match(r"^[0-9.,/()\-–\[\]\s]+$", syl):
            nudi_syllables.append(syl)
            continue
            
        # Match vowels
        if syl in vowels_map:
            nudi_syllables.append(vowels_map[syl])
            continue
        if len(syl) == 2 and syl[0] in vowels_map and syl[1] == "ಂ":
            nudi_syllables.append(vowels_map[syl[0]] + "A")
            continue
            
        # Process consonant syllable
        # Check if it has arkavattu (starts with ರ + ್ + Consonant)
        has_arka = False
        rest = syl
        if syl.startswith("ರ್"):
            has_arka = True
            rest = syl[2:]
            
        # Parse rest: Consonant cluster
        # C1 ( + ್ + C2 + ್ + C3 ... ) + Matra + Sign
        # Let's extract the base consonant (C1) and any vattaksharas (C2, C3...)
        parts = rest.split("್")
        # If there are no halants, parts length is 1
        base_with_matra = parts[0]
        vattas = []
        if len(parts) > 1:
            # The last element might contain a matra/sign
            last_part = parts[-1]
            # Intermediate elements are just consonants
            for x in parts[1:-1]:
                vattas.append(x)
            
            # Extract consonant and matra from last_part
            # Last part is e.g. "ತ" or "ತಿ" (C + M + S)
            m = re.match(f"^({C})(.*)$", last_part)
            if m:
                vattas.append(m.group(1))
                matra_sign = m.group(2)
            else:
                vattas.append(last_part)
                matra_sign = ""
                
            # Wait, the vowel sign actually applies to the base consonant in Nudi!
            # E.g. "ಕ್ತಿ" is Nudi(ಕಿ) + vattakshara(ತ)
            # So the matra_sign belongs to the base_with_matra!
            base_with_matra = base_with_matra + matra_sign
        else:
            base_with_matra = parts[0]
            
        # Now convert base_with_matra to Nudi
        # base_with_matra is e.g. "ಕ", "ಕಾ", "ಕಿ", "ಕೀ", "ಕು", "ಕೂ", "ಕೃ", "ಕೆ", "ಕೇ", "ಕೈ", "ಕೊ", "ಕೋ", "ಕೌ", "ಕ್"
        nudi_base = ""
        m = re.match(f"^({C})(.*)$", base_with_matra)
        if m:
            cons = m.group(1)
            matras_and_signs = m.group(2)
            
            # Check if there is an anusvara/visarga at the end
            has_anusvara = False
            has_visarga = False
            if "ಂ" in matras_and_signs:
                has_anusvara = True
                matras_and_signs = matras_and_signs.replace("ಂ", "")
            if "ಃ" in matras_and_signs:
                has_visarga = True
                matras_and_signs = matras_and_signs.replace("ಃ", "")
                
            # Map based on consonant + matra
            if (cons, matras_and_signs) in special_consonant_combos:
                nudi_base = special_consonant_combos[(cons, matras_and_signs)]
            elif cons in consonants_map:
                cfg = consonants_map[cons]
                if not matras_and_signs:
                    nudi_base = cfg["base"]
                elif matras_and_signs == "್":
                    nudi_base = cfg["halant"]
                elif matras_and_signs == "ಾ":
                    nudi_base = cfg["aa"]
                elif matras_and_signs == "ಿ":
                    nudi_base = cfg["i"]
                elif matras_and_signs == "ೀ":
                    nudi_base = cfg["i"] + "Ã"
                elif matras_and_signs == "ು":
                    nudi_base = cfg["base"] + "Ä"
                elif matras_and_signs == "ೂ":
                    nudi_base = cfg["base"] + "Æ"
                elif matras_and_signs == "ೃ":
                    nudi_base = cfg["base"] + "È"
                elif matras_and_signs == "ೆ":
                    nudi_base = cfg["e"]
                elif matras_and_signs == "ೇ":
                    nudi_base = cfg["e"] + "Ã"
                elif matras_and_signs == "ೈ":
                    nudi_base = cfg["e"] + "Ê"
                elif matras_and_signs == "ೊ":
                    nudi_base = cfg["e"] + "Æ"
                elif matras_and_signs == "ೋ":
                    nudi_base = cfg["e"] + "Æ" + "Ã"
                elif matras_and_signs == "ೌ":
                    nudi_base = cfg["au"]
                else:
                    # Fallback
                    nudi_base = cfg["base"] + matras_and_signs
            else:
                nudi_base = cons + matras_and_signs
                
            # Add anusvara/visarga
            if has_anusvara:
                nudi_base += "A"
            if has_visarga:
                nudi_base += "B"
        else:
            nudi_base = base_with_matra
            
        # Append vattaksharas
        nudi_vattas = ""
        for v in vattas:
            if v in vattakshara_map:
                nudi_vattas += vattakshara_map[v]
            else:
                nudi_vattas += v
                
        # Combine
        syl_nudi = nudi_base + nudi_vattas
        if has_arka:
            syl_nudi += "ð"
            
        nudi_syllables.append(syl_nudi)
        
    return "".join(nudi_syllables)

def unicode_to_nudi(text):
    # Split text into lines, then words, converting each and keeping whitespace
    lines = text.split("\n")
    converted_lines = []
    for line in lines:
        words = line.split(" ")
        converted_words = [unicode_to_nudi_word(w) for w in words]
        converted_lines.append(" ".join(converted_words))
    return "\n".join(converted_lines)

# Test cases
test_words = [
    "ಮನೆ", "ಬಾಡಿಗೆ", "ಕರಾರು", "ಪತ್ರ", "ಸನ್", "ಬೆಂಗಳೂರು", "ಧರ್ಮರಾಯ", "ಷಣ್ಮುಖಪ್ಪ", "ಪಾರ್ವತಮ್ಮ", "ಲಕ್ಷ್ಮಿಪುರ", "ಆರ್.ಸಿ.ಸಿ"
]
with open("scratch/test_unicode_to_nudi_results.txt", "w", encoding="utf-8") as f:
    for w in test_words:
        res = unicode_to_nudi(w)
        exact = res == word_map.get(w, 'N/A')
        f.write(f"Unicode: {w:<12} -> Nudi: {res:<15} (Exact match: {exact})\n")
print("Test completed. Output written to scratch/test_unicode_to_nudi_results.txt.")
