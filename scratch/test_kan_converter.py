from kannada_converter import unicode_to_ascii, ascii_to_unicode

def test():
    try:
        text_uni = "ಮನೆ ಬಾಡಿಗೆ ಕರಾರು ಪತ್ರ"
        text_ascii = unicode_to_ascii(text_uni)
        
        with open("scratch/test_out.txt", "w", encoding="utf-8") as f:
            f.write(f"Unicode: {text_uni}\n")
            f.write(f"ASCII ords: {[ord(c) for c in text_ascii]}\n")
            f.write(f"ASCII text: {text_ascii}\n")
            
            text_uni_rev = ascii_to_unicode(text_ascii)
            f.write(f"Reverse: {text_uni_rev}\n")
            
        print("Success! Output written to scratch/test_out.txt")
    except Exception as e:
        import traceback
        with open("scratch/test_out.txt", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        print("Failed. Traceback written to scratch/test_out.txt")

if __name__ == "__main__":
    test()
