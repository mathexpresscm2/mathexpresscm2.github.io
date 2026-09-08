import os
import json
from playwright.sync_api import sync_playwright

def run_audit():
    os.makedirs('scratch/mobile_audit', exist_ok=True)
    results = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Mobile viewport 390x844 (iPhone 12/13/14/15 size)
        context = browser.new_context(
            viewport={'width': 390, 'height': 844},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        )
        page = context.new_page()
        html_path = os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html')
        page.goto(f'file:///{html_path}')
        page.wait_for_timeout(1000)

        total_slides = page.evaluate('() => document.querySelectorAll(".slide").length')
        print(f"Total slides found: {total_slides}")

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
            page.wait_for_timeout(400)

            # Audit slide elements
            info = page.evaluate(f'''() => {{
                const slide = document.getElementById("slide-{i}");
                if (!slide) return {{ error: "Not found" }};
                
                const header = slide.querySelector(".slide-header");
                const content = slide.querySelector(".slide-content");
                const nav = document.querySelector(".fixed.bottom-6");
                
                const slideRect = slide.getBoundingClientRect();
                const contentRect = content ? content.getBoundingClientRect() : null;
                const headerRect = header ? header.getBoundingClientRect() : null;
                const navRect = nav ? nav.getBoundingClientRect() : null;
                
                // Check if content is scrollable
                const slideScrollHeight = slide.scrollHeight;
                const slideClientHeight = slide.clientHeight;
                const contentScrollHeight = content ? content.scrollHeight : 0;
                const contentClientHeight = content ? content.clientHeight : 0;
                
                // Check if last element in content is covered by nav or offscreen
                let lastChildBottom = 0;
                let lastChildInfo = "";
                if (content && content.children.length > 0) {{
                    const lastEl = content.children[content.children.length - 1];
                    const r = lastEl.getBoundingClientRect();
                    lastChildBottom = r.bottom;
                    lastChildInfo = lastEl.tagName + "." + lastEl.className.slice(0, 30);
                }}

                // Check text truncation or overflow
                let overflowingElements = [];
                const allElements = slide.querySelectorAll("*");
                for (const el of allElements) {{
                    if (el.scrollWidth > slide.clientWidth + 10 && !el.classList.contains("table-custom") && el.tagName !== "TABLE") {{
                        overflowingElements.push({{
                            tag: el.tagName,
                            cls: el.className.slice(0, 40),
                            scrollWidth: el.scrollWidth,
                            clientWidth: el.clientWidth
                        }});
                    }}
                }}

                const slideOverflowY = window.getComputedStyle(slide).overflowY;
                const contentOverflowY = content ? window.getComputedStyle(content).overflowY : "";

                return {{
                    slide: {i},
                    slideScrollHeight,
                    slideClientHeight,
                    contentScrollHeight,
                    contentClientHeight,
                    slideOverflowY,
                    contentOverflowY,
                    lastChildBottom,
                    navTop: navRect ? navRect.top : 800,
                    overflowingElementsCount: overflowingElements.length,
                    overflowingElements: overflowingElements.slice(0, 3)
                }};
            }}''')

            # Initial screenshot (top)
            page.screenshot(path=f'scratch/mobile_audit/slide_{i}_top.png')

            # Scroll down slide if possible and take bottom screenshot
            scroll_performed = page.evaluate(f'''() => {{
                const slide = document.getElementById("slide-{i}");
                const content = slide.querySelector(".slide-content");
                let scrolled = false;
                if (slide.scrollHeight > slide.clientHeight) {{
                    slide.scrollTop = slide.scrollHeight;
                    scrolled = true;
                }}
                if (content && content.scrollHeight > content.clientHeight) {{
                    content.scrollTop = content.scrollHeight;
                    scrolled = true;
                }}
                return scrolled;
            }}''')
            page.wait_for_timeout(200)
            page.screenshot(path=f'scratch/mobile_audit/slide_{i}_bottom.png')

            info['scroll_performed'] = scroll_performed
            results.append(info)
            print(f"Slide {i}: slideScroll={info.get('slideScrollHeight')} vs client={info.get('slideClientHeight')}, contentScroll={info.get('contentScrollHeight')} vs client={info.get('contentClientHeight')}, scrollY={info.get('slideOverflowY')}/{info.get('contentOverflowY')}, lastBottom={info.get('lastChildBottom')}, navTop={info.get('navTop')}")

        browser.close()

    with open('scratch/mobile_audit/results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("Audit complete! Saved to scratch/mobile_audit/results.json")

if __name__ == '__main__':
    run_audit()
