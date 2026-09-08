import io, os, sys, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

def deep_audit():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 390, 'height': 844})
        html_path = os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html')
        page.goto(f'file:///{html_path}')
        page.wait_for_timeout(1000)

        nav_rect = page.evaluate('() => document.querySelector(".fixed.bottom-6").getBoundingClientRect()')
        nav_top = nav_rect['top']
        print(f"Navigation bar top is at y = {nav_top}")

        report = []

        for i in range(1, 17):
            s_id = f"slide-{i}"
            page.evaluate(f'''() => {{
                const slides = document.querySelectorAll(".slide");
                slides.forEach(s => s.classList.remove("active"));
                const target = document.getElementById("{s_id}");
                if (target) target.classList.add("active");
            }}''')
            page.wait_for_timeout(300)

            data = page.evaluate(f'''() => {{
                const s = document.getElementById("{s_id}");
                if (!s) return {{ error: "not found" }};
                const c = s.querySelector(".slide-content");
                const h1_2 = s.querySelector("h1, h2");
                const title = h1_2 ? h1_2.innerText.trim().replace(/\\n/g, ' ') : "";

                // Scroll to bottom
                if (c) c.scrollTop = c.scrollHeight;
                if (s) s.scrollTop = s.scrollHeight;

                // 1. Elements with overflow:hidden where scrollHeight > clientHeight + 10
                let hiddenOverflows = [];
                const all = s.querySelectorAll("*");
                for (let el of all) {{
                    const st = window.getComputedStyle(el);
                    if ((st.overflowY === "hidden" || st.overflow === "hidden") && el.scrollHeight > el.clientHeight + 15) {{
                        hiddenOverflows.push({{
                            tag: el.tagName,
                            cls: (el.className || "").slice(0, 40),
                            sh: el.scrollHeight,
                            ch: el.clientHeight,
                            diff: el.scrollHeight - el.clientHeight
                        }});
                    }}
                }}

                // 2. Horizontal overflow
                let horizOverflows = [];
                for (let el of all) {{
                    const r = el.getBoundingClientRect();
                    if (r.right > 390.5 && !el.closest(".overflow-x-auto") && !el.classList.contains("mobile-swipe-hint")) {{
                        horizOverflows.push({{
                            tag: el.tagName,
                            cls: (el.className || "").slice(0, 40),
                            right: Math.round(r.right)
                        }});
                    }}
                }}

                // 3. Last child clearance above navigation bar (762px)
                let lastChildBottom = 0;
                let isCoveredByNav = false;
                if (c && c.children.length > 0) {{
                    const lastEl = c.children[c.children.length - 1];
                    const lr = lastEl.getBoundingClientRect();
                    lastChildBottom = Math.round(lr.bottom);
                    if (lr.bottom > 745) {{
                        isCoveredByNav = true;
                    }}
                }}

                return {{
                    slide: {i},
                    title,
                    scrollable: c ? (c.scrollHeight > c.clientHeight) : false,
                    contentScrollHeight: c ? c.scrollHeight : s.scrollHeight,
                    contentClientHeight: c ? c.clientHeight : s.clientHeight,
                    hiddenOverflows,
                    horizOverflows: horizOverflows.slice(0, 3),
                    lastChildBottom,
                    isCoveredByNav
                }};
            }}''')

            report.append(data)
            print(f"Slide {i:02d} | '{data['title'][:35]}'")
            print(f"   Scrollable: {data['scrollable']} ({data['contentScrollHeight']}px vs {data['contentClientHeight']}px) | LastBottom: {data['lastChildBottom']}px (Nav at {round(nav_top)}px)")
            if data['hiddenOverflows']:
                print(f"   ⚠️ HIDDEN CLIPPED ELEMENTS: {len(data['hiddenOverflows'])} items! E.g. {data['hiddenOverflows'][0]}")
            if data['horizOverflows']:
                print(f"   ⚠️ HORIZONTAL OVERFLOW: {len(data['horizOverflows'])} items! E.g. {data['horizOverflows'][0]}")
            if data['isCoveredByNav']:
                print(f"   ⚠️ COVERED BY NAV BAR! (Bottom {data['lastChildBottom']}px > 745px)")
            if not data['hiddenOverflows'] and not data['horizOverflows'] and not data['isCoveredByNav']:
                print(f"   ✅ Perfect on Mobile!")
            print("-" * 60)

        browser.close()

    with open("scratch/deep_audit_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    deep_audit()
