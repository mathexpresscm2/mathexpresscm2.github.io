import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

def analyze():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 390, 'height': 844},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15'
        )
        page = context.new_page()
        html_path = os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html')
        page.goto(f'file:///{html_path}')
        page.wait_for_timeout(1000)

        nav_box = page.evaluate('() => document.querySelector(".fixed.bottom-6").getBoundingClientRect()')
        nav_top = nav_box['top']
        print(f"Navigation bar top is at y = {nav_top}px")

        issues = {}

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
            page.wait_for_timeout(200)

            # Check slide issues
            data = page.evaluate(f'''() => {{
                const slide = document.getElementById("slide-{i}");
                const content = slide.querySelector(".slide-content");
                const nav = document.querySelector(".fixed.bottom-6");
                const navRect = nav.getBoundingClientRect();

                // 1. Check title wrapping and height
                const header = slide.querySelector(".slide-header");
                const headerRect = header ? header.getBoundingClientRect() : null;

                // 2. Check if content is scrollable
                const isScrollable = content ? (content.scrollHeight > content.clientHeight) : false;

                // 3. Scroll to bottom
                let coveredElements = [];
                if (content && isScrollable) {{
                    content.scrollTop = content.scrollHeight;
                }}

                // Check all leaf elements in slide
                const allElements = slide.querySelectorAll("p, h1, h2, h3, h4, span, li, img, td, th, div");
                let horizontalOverflows = [];
                for (const el of allElements) {{
                    const r = el.getBoundingClientRect();
                    if (r.right > 390.5 && !el.closest(".overflow-x-auto") && !el.classList.contains("mobile-swipe-hint")) {{
                        horizontalOverflows.push({{
                            tag: el.tagName,
                            text: (el.innerText || "").slice(0, 30),
                            right: Math.round(r.right),
                            cls: el.className.slice(0, 30)
                        }});
                    }}
                }}

                // Check if last element in content overlaps with navigation bar
                let lastChildCovered = false;
                let lastChildBottom = 0;
                if (content && content.children.length > 0) {{
                    const last = content.children[content.children.length - 1];
                    const r = last.getBoundingClientRect();
                    lastChildBottom = r.bottom;
                    if (r.bottom > navRect.top - 5 && r.top < navRect.bottom) {{
                        lastChildCovered = true;
                    }}
                }}

                return {{
                    slide: {i},
                    isScrollable,
                    scrollHeight: content ? content.scrollHeight : slide.scrollHeight,
                    clientHeight: content ? content.clientHeight : slide.clientHeight,
                    horizontalOverflows: horizontalOverflows.slice(0, 3),
                    lastChildCovered,
                    lastChildBottom,
                    navTop: navRect.top
                }};
            }}''')

            slide_issues = []
            if data['horizontalOverflows']:
                slide_issues.append(f"Horizontal Overflow: {len(data['horizontalOverflows'])} items exceed 390px (e.g. {data['horizontalOverflows'][0]['tag']}: '{data['horizontalOverflows'][0]['text']}', right={data['horizontalOverflows'][0]['right']})")
            if data['lastChildCovered']:
                slide_issues.append(f"Covered by Nav bar: last child bottom={data['lastChildBottom']} > navTop={data['navTop']}")
            
            # Check special cases for non-scrollable slides:
            # If not scrollable, is content cramped or overflow hidden?
            if not data['isScrollable'] and i not in [1, 15, 16]:
                slide_issues.append(f"Non-scrollable slide: may have overflow clipped")

            issues[i] = slide_issues
            status_str = "⚠️ CẦN TỐI ƯU" if slide_issues else "✅ OK"
            print(f"Slide {i:02d} [{status_str}]: " + ("; ".join(slide_issues) if slide_issues else "Đọc tốt, vừa vặn"))

        browser.close()

if __name__ == '__main__':
    analyze()
