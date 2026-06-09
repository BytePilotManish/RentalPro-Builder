with open(r"d:\rental pro\new\scratch\agreement2_decoded_side_by_side.txt", "r", encoding="utf-8") as f:
    content = f.read()

parts = content.split('--- PARAGRAPH ')
for part in parts:
    if not part.strip():
        continue
    p_num_str = part.split(' ---')[0]
    try:
        p_num = int(p_num_str)
    except ValueError:
        continue
    
    if p_num <= 155:
        print(f"\n================ PARAGRAPH {p_num} ================")
        lines = part.split('\n')[1:]
        for line in lines:
            if line.strip():
                print(line.strip().encode('ascii', 'backslashreplace').decode('ascii'))
