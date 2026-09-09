import re
import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
file_path = 'd:/WorkSpace/mathexpresscm2.github.io/Meeting/Khoi 6/Tuan 10 - Hop khoi 6/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
slides = soup.find_all('div', class_=lambda c: c and 'slide' in c.split())

print(f'Total actual slide elements: {len(slides)}')
for idx, slide in enumerate(slides):
    s_id = slide.get('id', f'slide-{idx+1}')
    h2 = slide.find('h2')
    h2_text = h2.get_text(strip=True) if h2 else '(No h2)'
    print(f'\n--- Slide {idx+1} [id={s_id}]: {h2_text} ---')
    # Print brief summary of slide content
    text_content = ' '.join(slide.get_text(separator=' ', strip=True).split())
    print(text_content[:200] + '...')
