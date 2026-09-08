import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # Mobile view (Pixel 5)
        mobile_context = await browser.new_context(
            viewport={'width': 393, 'height': 851},
            device_scale_factor=2.75,
            is_mobile=True,
            has_touch=True
        )
        page = await mobile_context.new_page()
        
        file_path = os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html')
        await page.goto(f'file:///{file_path}')
        await page.wait_for_timeout(1000)
        
        # Navigate to slide 7
        await page.evaluate('''() => {
            const slides = document.querySelectorAll('.slide');
            slides.forEach((s, i) => {
                if (i === 6) s.classList.add('active');
                else s.classList.remove('active');
            });
            const counter = document.getElementById('slideCounter');
            if (counter) counter.textContent = '7/16';
        }''')
        await page.wait_for_timeout(1000)
        
        # Inject Option 1 CSS
        css = '''
            #slide-7 .zoom-115 {
                zoom: 1 !important;
                transform: none !important;
                padding: 0.75rem !important;
                overflow: visible !important;
                height: auto !important;
                max-height: none !important;
                flex-shrink: 0 !important;
                margin-bottom: 2rem !important;
            }

            #slide-7 .slide-content {
                justify-content: flex-start !important;
            }

            #slide-7 .p-4.bg-slate-50\\/70 {
                padding: 0.625rem !important;
                gap: 0.625rem !important;
            }

            #slide-7 img[alt*="Hình"] {
                height: 8.5rem !important;
            }

            #slide-7 .md\\:col-span-5,
            #slide-7 .md\\:col-span-7 {
                padding: 0.875rem !important;
            }

            #slide-7 .whitespace-nowrap {
                white-space: normal !important;
                word-break: break-word !important;
            }
        '''
        await page.add_style_tag(content=css)
        await page.wait_for_timeout(500)
        
        # 1. Capture mobile top view
        await page.screenshot(path='scratch/mobile_k7_slide7_opt1_top.png')
        
        # 2. Scroll to middle (see image and error column)
        await page.evaluate('''() => {
            const el = document.querySelector('#slide-7 .slide-content');
            if (el) el.scrollTop = 380;
        }''')
        await page.wait_for_timeout(500)
        await page.screenshot(path='scratch/mobile_k7_slide7_opt1_mid.png')
        
        # 3. Scroll to bottom (see solution column and notes)
        await page.evaluate('''() => {
            const el = document.querySelector('#slide-7 .slide-content');
            if (el) el.scrollTop = 850;
        }''')
        await page.wait_for_timeout(500)
        await page.screenshot(path='scratch/mobile_k7_slide7_opt1_bottom.png')
        
        # Metrics check
        metrics = await page.evaluate('''() => {
            const card = document.querySelector('#slide-7 .zoom-115');
            const content = document.querySelector('#slide-7 .slide-content');
            return {
                cardScrollHeight: card ? card.scrollHeight : 0,
                contentScrollHeight: content ? content.scrollHeight : 0,
                contentClientHeight: content ? content.clientHeight : 0,
                maxScrollTop: content ? (content.scrollHeight - content.clientHeight) : 0
            };
        }''')
        print("Opt1 Metrics:", metrics)
        
        await browser.close()

asyncio.run(main())
