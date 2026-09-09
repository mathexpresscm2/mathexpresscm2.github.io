import sys
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')
file_path = 'd:/WorkSpace/mathexpresscm2.github.io/Meeting/Khoi 6/Tuan 10 - Hop khoi 6/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
slides = soup.find_all('div', class_=lambda c: c and 'slide' in c.split())

for i, s in enumerate(slides):
    s_id = s.get('id', f'slide-{i+1}')
    h2 = s.find('h2')
    title = h2.get_text(strip=True) if h2 else ''
    print(f'=== SLIDE {i+1} ({s_id}): {title} ===')
    # print text of slide
    lines = [line.strip() for line in s.get_text(separator='\n').split('\n') if line.strip()]
    print('\n'.join(lines[:15]))
    if len(lines) > 15:
        print(f'... ({len(lines)-15} more lines)')
    print()
