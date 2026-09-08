import asyncio
from playwright.async_api import async_playwright
import os
import base64

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        file_path = os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html')
        
        # Read base64 of hinh_bai1.svg
        svg_bytes = open('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/hinh_bai1.svg', 'rb').read()
        svg_b64 = 'data:image/svg+xml;base64,' + base64.b64encode(svg_bytes).decode('utf-8')
        
        # 1. Mobile view (Pixel 5: 393 x 851)
        mobile_context = await browser.new_context(
            viewport={'width': 393, 'height': 851},
            device_scale_factor=2.75,
            is_mobile=True,
            has_touch=True
        )
        page = await mobile_context.new_page()
        await page.goto(f'file:///{file_path}')
        await page.wait_for_timeout(1000)
        
        # Go to slide 6 (index 5)
        await page.evaluate(f'''() => {{
            const slides = document.querySelectorAll('.slide');
            slides.forEach((s, i) => {{
                if (i === 5) s.classList.add('active');
                else s.classList.remove('active');
            }});
            const counter = document.getElementById('slideCounter');
            if (counter) counter.textContent = '6/16';
            
            // Also test base64 fallback for img
            const img = document.querySelector('#slide-6 img[alt*="Hình"]');
            if (img) {{
                img.src = "{svg_b64}";
            }}
        }}''')
        await page.wait_for_timeout(1000)
        
        # Inject CSS
        css = '''
            #slide-6 .zoom-115 {
                zoom: 1 !important;
                transform: none !important;
                padding: 0.75rem !important;
                overflow: visible !important;
                height: auto !important;
                max-height: none !important;
                flex-shrink: 0 !important;
                margin-bottom: 2rem !important;
            }

            #slide-6 .slide-content {
                justify-content: flex-start !important;
            }

            #slide-6 img[alt*="Hình"] {
                height: 8.5rem !important;
            }

            #slide-6 .p-4\\.5,
            #slide-6 .p-5 {
                padding: 0.875rem !important;
            }

            #slide-6 .p-3\\.5.bg-emerald-50 {
                padding: 0.875rem !important;
                font-size: 0.85rem !important;
            }
        '''
        await page.add_style_tag(content=css)
        await page.wait_for_timeout(500)
        
        # 1. Top screenshot
        await page.screenshot(path='scratch/mobile_k7_slide6_opt_top.png')
        
        # 2. Middle screenshot
        await page.evaluate('''() => {
            const el = document.querySelector('#slide-6 .slide-content');
            if (el) el.scrollTop = 320;
        }''')
        await page.wait_for_timeout(500)
        await page.screenshot(path='scratch/mobile_k7_slide6_opt_mid.png')
        
        # 3. Bottom screenshot
        await page.evaluate('''() => {
            const el = document.querySelector('#slide-6 .slide-content');
            if (el) el.scrollTop = 700;
        }''')
        await page.wait_for_timeout(500)
        await page.screenshot(path='scratch/mobile_k7_slide6_opt_bottom.png')
        
        # Metrics check
        metrics = await page.evaluate('''() => {
            const card = document.querySelector('#slide-6 .zoom-115');
            const content = document.querySelector('#slide-6 .slide-content');
            return {
                cardScrollHeight: card ? card.scrollHeight : 0,
                contentScrollHeight: content ? content.scrollHeight : 0,
                contentClientHeight: content ? content.clientHeight : 0,
                maxScrollTop: content ? (content.scrollHeight - content.clientHeight) : 0
            };
        }''')
        print("Slide 6 Opt Metrics:", metrics)
        
        await browser.close()

asyncio.run(main())
