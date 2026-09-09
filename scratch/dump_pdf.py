import fitz
import sys

sys.stdout.reconfigure(encoding='utf-8')
doc = fitz.open('d:/WorkSpace/mathexpresscm2.github.io/Meeting/Khoi 6/Tuan 10 - Hop khoi 6/Tháng 9-2026 Trao đổi chuyên môn.pdf')
print(f'Total pages: {len(doc)}')

for i, page in enumerate(doc):
    print(f'\n==================== PAGE {i+1} ====================')
    text = page.get_text()
    print(text)
