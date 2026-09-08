import os, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

def inspect_all():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Standard mobile viewport
        context = browser.new_context(
            viewport={'width': 390, 'height': 844},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15'
        )
        page = context.new_page()
        html_path = os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html')
        page.goto(f'file:///{html_path}')
        page.wait_for_timeout(1000)

        total_slides = 16

        for i in range(1, total_slides + 1):
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
            page.wait_for_timeout(300)

            res = page.evaluate(f'''() => {{
                const slide = document.getElementById("slide-{i}");
                if (!slide) return {{ error: "not found" }};
                const content = slide.querySelector(".slide-content");
                const nav = document.querySelector(".fixed.bottom-6");
                const navRect = nav ? nav.getBoundingClientRect() : {{ top: 760, bottom: 820 }};

                // Check title
                const h1_h2 = slide.querySelector("h1, h2");
                const title = h1_h2 ? h1_h2.innerText.trim() : "";

                // Check scrollability
                const scrollHeight = content ? content.scrollHeight : slide.scrollHeight;
                const clientHeight = content ? content.clientHeight : slide.clientHeight;
                const isScrollable = scrollHeight > clientHeight + 5;

                // Check overflow elements
                let clippedElements = [];
                let overflowingRight = [];

                const all = slide.querySelectorAll("*");
                for (const el of all) {{
                    const rect = el.getBoundingClientRect();
                    // Check if element is wider than slide
                    if (rect.width > 390.5 && !el.classList.contains("mobile-swipe-hint") && !el.closest(".overflow-x-auto")) {{
                        overflowingRight.push({{
                            tag: el.tagName,
                            cls: el.className.slice(0, 40),
                            width: Math.round(rect.width)
                        }});
                    }}
                }}

                // Check if last element is covered by nav when scrolled to bottom
                let coveredByNav = false;
                if (content && content.children.length > 0) {{
                    content.scrollTop = content.scrollHeight;
                    const lastChild = content.children[content.children.length - 1];
                    const r = lastChild.getBoundingClientRect();
                    if (r.bottom > navRect.top + 10) {{
                        coveredByNav = true;
                    }}
                }}

                return {{
                    slide: {i},
                    title: title.replace(/\\n/g, ' '),
                    scrollHeight,
                    clientHeight,
                    isScrollable,
                    overflowingRightCount: overflowingRight.length,
                    overflowingRight: overflowingRight.slice(0, 3),
                    coveredByNav
                }};
            }}''')

            print(f"Slide {i:02d}: '{res['title'][:40]}' | Scrollable: {res['isScrollable']} ({res['scrollHeight']}px vs {res['clientHeight']}px) | HorizOverflow: {res['overflowingRightCount']} | CoveredByNav: {res['coveredByNav']}")

        browser.close()

if __name__ == '__main__':
    inspect_all()
