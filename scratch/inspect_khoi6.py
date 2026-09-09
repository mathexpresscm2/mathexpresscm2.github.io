import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
file_path = 'd:/WorkSpace/mathexpresscm2.github.io/Meeting/Khoi 6/Tuan 10 - Hop khoi 6/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

slides = re.findall(r'<div class="slide[^"]*"', text)
print(f'Total lines: {len(text.splitlines())}, Total slides: {len(slides)}')

headers = re.findall(r'<h2[^>]*>(.*?)</h2>', text, re.DOTALL)
print('\n=== HEADERS FOUND IN SLIDES ===')
for i, h in enumerate(headers):
    clean_h = re.sub(r'<[^>]+>', '', h).strip()
    clean_h = ' '.join(clean_h.split())
    print(f'Slide {i+1}: {clean_h}')

# Let's inspect slide IDs if any
slide_ids = re.findall(r'id="(slide-[^"]+)"', text)
print('\nSlide IDs:', slide_ids)
