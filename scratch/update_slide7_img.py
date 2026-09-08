import base64

with open('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/hinh_ngonhan.svg', 'rb') as f:
    b64_ngonhan = base64.b64encode(f.read()).decode('utf-8')

with open('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = '<img src="hinh_ngonhan.svg" class="h-44 xl:h-48 object-contain cursor-pointer"'
new = f'''<img src="hinh_ngonhan.svg" onerror="if(!this.dataset.fallback){{this.dataset.fallback=1;this.src='data:image/svg+xml;base64,{b64_ngonhan}';}}" class="h-44 xl:h-48 object-contain cursor-pointer"'''

if old in content:
    content = content.replace(old, new, 1)
    with open('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Slide 7 image fallback added successfully!")
else:
    print("Old string not found in index.html")
