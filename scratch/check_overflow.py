import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('file:///' + os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html'))
    for s_id in ['slide-10', 'slide-11']:
        page.evaluate(f'''() => {{
            const slides = document.querySelectorAll('.slide');
            slides.forEach(s => s.classList.remove('active'));
            document.getElementById('{s_id}').classList.add('active');
        }}''')
        page.wait_for_timeout(200)
        res = page.evaluate('''() => {
            const s = document.querySelector('.slide.active');
            const overflows = [];
            for (const el of s.querySelectorAll('*')) {
                const r = el.getBoundingClientRect();
                if (r.right > 390.5) {
                    overflows.push({
                        tag: el.tagName,
                        cls: el.className.slice(0, 30),
                        right: Math.round(r.right),
                        text: (el.innerText || '').slice(0, 40)
                    });
                }
            }
            return overflows;
        }''')
        print(f"{s_id} overflowing elements ({len(res)}):")
        for o in res[:6]:
            print("  ", o)
    browser.close()
