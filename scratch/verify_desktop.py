import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

os.makedirs('scratch/desktop_verification', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # Standard 1080p Desktop widescreen
    page = browser.new_page(viewport={'width': 1920, 'height': 1080})
    html_path = os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html')
    page.goto(f'file:///{html_path}')
    page.wait_for_timeout(1000)

    slides_to_check = [1, 2, 4, 6, 7, 9, 10, 11, 13, 14, 16]
    for s_idx in slides_to_check:
        page.evaluate(f'''() => {{
            const slides = document.querySelectorAll(".slide");
            slides.forEach((s, idx) => {{
                if (idx === ({s_idx} - 1)) {{
                    s.classList.add("active");
                }} else {{
                    s.classList.remove("active");
                }}
            }});
            const counter = document.getElementById("slideCounter");
            if (counter) counter.textContent = "{s_idx}/" + slides.length;
        }}''')
        page.wait_for_timeout(300)
        page.screenshot(path=f'scratch/desktop_verification/desktop_slide_{s_idx}.png')
        print(f"Captured Desktop Slide {s_idx}")

    browser.close()
print("Desktop verification complete!")
