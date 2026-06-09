from kannada_converter import ascii_to_unicode

def test():
    ascii_text = "ªÀÄ£É ¨ÁrUÉ PÀgÁgÀÄ ¥ÀvÀæ"
    try:
        uni_text = ascii_to_unicode(ascii_text)
        with open("scratch/test_out.txt", "w", encoding="utf-8") as f:
            f.write(f"ASCII: {ascii_text}\n")
            f.write(f"Unicode: {uni_text}\n")
        print("Success! Written to scratch/test_out.txt")
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()
