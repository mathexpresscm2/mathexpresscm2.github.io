import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html', encoding='utf-8') as f:
    for num, line in enumerate(f, 1):
        if 'id="slide-' in line or 'class="slide' in line:
            print(f'{num}: {line.strip()}')
