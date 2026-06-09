import docx

doc = docx.Document("scratch/test_kan_output_v2.docx")
print("First few paragraphs text in generated doc:")
for idx, p in enumerate(doc.paragraphs[20:35]):
    print(f"P {idx+20}: '{p.text}'")
