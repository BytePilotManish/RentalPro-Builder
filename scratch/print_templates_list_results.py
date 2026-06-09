with open(r"d:\rental pro\new\scratch\templates_list_results.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip().encode('ascii', 'backslashreplace').decode('ascii'))
