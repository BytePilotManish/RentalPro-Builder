import re

with open(r"d:\rental pro\new\scratch\numbers_occurrences.txt", "r", encoding="utf-8") as f:
    for line in f:
        # Ignore dates, pincodes, and age
        # Pincodes: 56xxxx
        # Dates: xx-xx-xxxx or xx/xx/xxxx
        # Year: 2026, 2023
        clean_line = line.strip()
        if not clean_line:
            continue
        text = clean_line.split('->', 1)[1] if '->' in clean_line else clean_line
        # Remove typical patterns
        text_no_dates = re.sub(r'\d{2}-\d{2}-\d{4}', '', text)
        text_no_dates = re.sub(r'56\d{4}', '', text_no_dates) # pincode
        text_no_dates = re.sub(r'202\d', '', text_no_dates) # year
        
        # Check if there are other numbers
        other_nums = re.findall(r'\d+', text_no_dates)
        if other_nums:
            # check if any other numbers are small integers like 1 to 20
            small_ints = [int(x) for x in other_nums if int(x) < 30]
            if small_ints:
                print(clean_line.encode('ascii', 'backslashreplace').decode('ascii'))
