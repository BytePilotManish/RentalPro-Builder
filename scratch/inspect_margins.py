import docx
import os

def check_geometry(path):
    if not os.path.exists(path):
        print(f"{path} not found.")
        return
        
    doc = docx.Document(path)
    print(f"\n=== Geometry of {os.path.basename(path)} ===")
    print(f"Total sections: {len(doc.sections)}")
    for i, sec in enumerate(doc.sections):
        print(f"Section {i+1}:")
        print(f"  Page Width: {sec.page_width.inches if sec.page_width else 'default'} inches")
        print(f"  Page Height: {sec.page_height.inches if sec.page_height else 'default'} inches")
        print(f"  Top Margin: {sec.top_margin.inches if sec.top_margin else 'default'} inches")
        print(f"  Bottom Margin: {sec.bottom_margin.inches if sec.bottom_margin else 'default'} inches")
        print(f"  Left Margin: {sec.left_margin.inches if sec.left_margin else 'default'} inches")
        print(f"  Right Margin: {sec.right_margin.inches if sec.right_margin else 'default'} inches")
        print(f"  Header Distance: {sec.header_distance.inches if sec.header_distance else 'default'} inches")
        print(f"  Footer Distance: {sec.footer_distance.inches if sec.footer_distance else 'default'} inches")

check_geometry(r"d:\rental pro\new\19-05-2026 - kan (2.docx")
check_geometry(r"d:\rental pro\new\TEMPLATE_KAN.docx")
