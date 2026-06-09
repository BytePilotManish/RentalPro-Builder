import re
import json
import os
from runtime_paths import data_dir

# Load word mapping dictionary from scratch
# In production, we'll try to find it in the current directory or scratch folder.
word_map = {}
# Try multiple paths to locate word_mapping.json
possible_paths = [
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "scratch", "word_mapping.json"),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "word_mapping.json"),
    "scratch/word_mapping.json",
    "word_mapping.json"
]

for p in possible_paths:
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                word_map = json.load(f)
            break
        except Exception:
            pass

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

special_consonant_combos = {
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
    if not word:
        return ""
    # If the word is already in our dictionary, return it!
    if word in word_map:
        return word_map[word]
        
    # Segment word into syllables
    C = r"[\u0c95-\u0cb9\u0cb3\u0cde]"
    V = r"[\u0c85-\u0c94\u0ce0\u0ce1]"
    M = r"[\u0cbe-\u0cc4\u0cc6-\u0cc8\u0cca-\u0ccc\u0cd5\u0cd6]"
    H = r"\u0ccd"
    S = r"[\u0c82\u0c83]"
    
    pattern = re.compile(
        f"({C}{H}(?:\u200d)?{C}(?:{H}(?:\u200d)?{C})*{M}?{S}?|"
        f"{C}{M}?{S}?|"
        f"{V}{S}?|"
        f"[0-9\u0ce6-\u0cef.,/()\\-–\\[\\]]+|"
        f".)"
    )
    
    syllables = pattern.findall(word)
    nudi_syllables = []
    
    for syl in syllables:
        if not syl.strip():
            nudi_syllables.append(syl)
            continue
            
        if re.match(r"^[0-9.,/()\-–\[\]\s]+$", syl):
            nudi_syllables.append(syl)
            continue
            
        if syl in vowels_map:
            nudi_syllables.append(vowels_map[syl])
            continue
        if len(syl) == 2 and syl[0] in vowels_map and syl[1] == "ಂ":
            nudi_syllables.append(vowels_map[syl[0]] + "A")
            continue
            
        has_arka = False
        rest = syl
        if syl.startswith("ರ್"):
            has_arka = True
            rest = syl[2:]
            
        parts = rest.split("್")
        base_with_matra = parts[0]
        vattas = []
        if len(parts) > 1:
            last_part = parts[-1]
            for x in parts[1:-1]:
                vattas.append(x)
            
            m = re.match(f"^({C})(.*)$", last_part)
            if m:
                vattas.append(m.group(1))
                matra_sign = m.group(2)
            else:
                vattas.append(last_part)
                matra_sign = ""
                
            base_with_matra = base_with_matra + matra_sign
        else:
            base_with_matra = parts[0]
            
        nudi_base = ""
        m = re.match(f"^({C})(.*)$", base_with_matra)
        if m:
            cons = m.group(1)
            matras_and_signs = m.group(2)
            
            has_anusvara = False
            has_visarga = False
            if "ಂ" in matras_and_signs:
                has_anusvara = True
                matras_and_signs = matras_and_signs.replace("ಂ", "")
            if "ಃ" in matras_and_signs:
                has_visarga = True
                matras_and_signs = matras_and_signs.replace("ಃ", "")
                
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
                    nudi_base = cfg["base"] + matras_and_signs
            else:
                nudi_base = cons + matras_and_signs
                
            if has_anusvara:
                nudi_base += "A"
            if has_visarga:
                nudi_base += "B"
        else:
            nudi_base = base_with_matra
            
        nudi_vattas = ""
        for v in vattas:
            if v in vattakshara_map:
                nudi_vattas += vattakshara_map[v]
            else:
                nudi_vattas += v
                
        syl_nudi = nudi_base + nudi_vattas
        if has_arka:
            syl_nudi += "ð"
            
        nudi_syllables.append(syl_nudi)
        
    return "".join(nudi_syllables)

def unicode_to_nudi(text):
    if not isinstance(text, str):
        return text
    lines = text.split("\n")
    converted_lines = []
    for line in lines:
        words = line.split(" ")
        converted_words = [unicode_to_nudi_word(w) for w in words]
        converted_lines.append(" ".join(converted_words))
    return "\n".join(converted_lines)
