import bs4

file_path = 'Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Parse with bs4
soup = bs4.BeautifulSoup(html, 'html.parser')
slide4 = soup.find('div', id='slide-4')
table = slide4.find('table')

# Header
thead = table.find('thead')
th_row = thead.find('tr')
ths = th_row.find_all('th')
# ths: [Thời gian, Buổi học, Định hướng chuyên, Nâng cao, Mở rộng & Cơ bản]
if len(ths) >= 5:
    ths[-3]['class'] = ths[-3].get('class', []) + ['col-chuyen']
    ths[-2]['class'] = ths[-2].get('class', []) + ['col-nangcao']
    ths[-1]['class'] = ths[-1].get('class', []) + ['col-coban']

# Tbody rows
tbody = table.find('tbody')
for tr in tbody.find_all('tr'):
    tds = tr.find_all('td')
    if len(tds) >= 3:
        tds[-3]['class'] = tds[-3].get('class', []) + ['col-chuyen']
        tds[-2]['class'] = tds[-2].get('class', []) + ['col-nangcao']
        tds[-1]['class'] = tds[-1].get('class', []) + ['col-coban']

# Convert back to html string cleanly
new_table_html = str(table)

# Let's replace only the table in the original html so formatting and comments elsewhere are preserved
# Find original table in html
table_start = html.find('<table class="w-full text-[14px] md:text-[15px] text-slate-800 border-collapse table-custom"')
table_end = html.find('</table>', table_start) + len('</table>')

if table_start != -1 and table_end != -1:
    updated_html = html[:table_start] + new_table_html + html[table_end:]
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    print("Table column classes added successfully!")
else:
    print("Table markers not found!")
