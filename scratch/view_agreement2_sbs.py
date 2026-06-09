with open(r"d:\rental pro\new\scratch\agreement2_decoded_side_by_side.txt", "r", encoding="utf-8") as f:
    for line in f:
        # We only print the ESCAPED and UNICODE lines to see the details, and the PARAGRAPH header
        if any(term in line for term in ["PARAGRAPH", "RAW ESCAPED", "UNICODE"]):
            print(line.strip().encode('ascii', 'backslashreplace').decode('ascii'))
