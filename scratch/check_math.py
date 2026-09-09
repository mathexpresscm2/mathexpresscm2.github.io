import re
import sys
import zipfile
import xml.etree.ElementTree as ET

sys.stdout.reconfigure(encoding='utf-8')

# Read docx
docx_path = r'd:\WorkSpace\mathexpresscm2.github.io\Meeting\Khoi 6\Tuan 10 - Hop khoi 6\Tháng 9-2026 Trao đổi chuyên môn.docx'
with zipfile.ZipFile(docx_path) as z:
    xml_content = z.read('word/document.xml')
    tree = ET.fromstring(xml_content)
    docx_paras = []
    for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
        t = ''.join(node.text for node in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t') if node.text)
        if t:
            docx_paras.append(t)

print("=== CHECKING MATH PROBLEMS IN DOCX ===")
for i, p in enumerate(docx_paras):
    if any(k in p for k in ['Dạng 1', 'Dạng 2', 'Dạng 3', 'Ví dụ 1', 'Ví dụ 2', 'nông trại', 'trứng', 'chuyên']):
        print(f'{i}: {p}')

print("\n=== CHECKING SAMPLES IN DOCX (Mẫu nhận xét) ===")
for i in range(220, len(docx_paras)):
    print(f'{i}: {docx_paras[i]}')
