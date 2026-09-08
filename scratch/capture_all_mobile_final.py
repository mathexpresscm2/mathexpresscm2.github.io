import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

os.makedirs('scratch/mobile_final_screenshots', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        viewport={'width': 390, 'height': 844},
        user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15'
    )
    html_path = os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html')
    page.goto(f'file:///{html_path}')
    page.wait_for_timeout(1000)

    for i in range(1, 17):
        page.evaluate(f'''() => {{
            const slides = document.querySelectorAll(".slide");
            slides.forEach((s, idx) => {{
                if (idx === ({i} - 1)) {{
                    s.classList.add("active");
                }} else {{
                    s.classList.remove("active");
                }}
            }});
            const counter = document.getElementById("slideCounter");
            if (counter) counter.textContent = "{i}/" + slides.length;
        }}''')
        page.wait_for_timeout(250)
        page.screenshot(path=f'scratch/mobile_final_screenshots/slide_{i:02d}_top.png')

        # Scroll to bottom if scrollable
        is_scrollable = page.evaluate(f'''() => {{
            const s = document.getElementById("slide-{i}");
            const c = s ? s.querySelector(".slide-content") : null;
            if (c && c.scrollHeight > c.clientHeight + 10) {{
                c.scrollTop = c.scrollHeight;
                return true;
            }}
            return false;
        }}''')
        page.wait_for_timeout(150)
        if is_scrollable:
            page.screenshot(path=f'scratch/mobile_final_screenshots/slide_{i:02d}_bottom.png')
        print(f"Captured Slide {i:02d} (Scrollable={is_scrollable})")

    browser.close()
print("All mobile screenshots captured successfully!")
