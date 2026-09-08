import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 1. Test Mobile (Pixel 5: 393 x 851)
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
        
        # Go to slide 7 (index 6)
        await page.evaluate('''() => {
            const slides = document.querySelectorAll('.slide');
            slides.forEach((s, i) => {
                if (i === 6) s.classList.add('active');
                else s.classList.remove('active');
            });
            const counter = document.getElementById('slideCounter');
            if (counter) counter.textContent = '7/16';
        }''')
        await page.wait_for_timeout(1500)
        
        # Capture mobile top view
        await page.screenshot(path='scratch/mobile_k7_slide7_current_top.png')
        
        # Scroll down in slide-content
        await page.evaluate('''() => {
            const el = document.querySelector('#slide-7 .slide-content');
            if (el) el.scrollTop = 500;
        }''')
        await page.wait_for_timeout(500)
        await page.screenshot(path='scratch/mobile_k7_slide7_current_scrolled.png')
        
        # Full content height inspection
        metrics = await page.evaluate('''() => {
            const card = document.querySelector('#slide-7 .zoom-115');
            const content = document.querySelector('#slide-7 .slide-content');
            const questionBox = document.querySelector('#slide-7 .bg-brand-light');
            const imgBox = document.querySelector('#slide-7 img[alt*="Hình"]');
            const grid = document.querySelector('#slide-7 .grid');
            return {
                cardScrollHeight: card ? card.scrollHeight : 0,
                cardClientHeight: card ? card.clientHeight : 0,
                contentScrollHeight: content ? content.scrollHeight : 0,
                contentClientHeight: content ? content.clientHeight : 0,
                questionBoxHeight: questionBox ? questionBox.offsetHeight : 0,
                imgBoxHeight: imgBox ? imgBox.offsetHeight : 0,
                gridHeight: grid ? grid.offsetHeight : 0,
            };
        }''')
        print("Metrics:", metrics)
        
        # 2. Test Desktop (1920 x 1080)
        desktop_context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        d_page = await desktop_context.new_page()
        await d_page.goto(f'file:///{file_path}')
        await d_page.wait_for_timeout(1000)
        await d_page.evaluate('''() => {
            const slides = document.querySelectorAll('.slide');
            slides.forEach((s, i) => {
                if (i === 6) s.classList.add('active');
                else s.classList.remove('active');
            });
        }''')
        await d_page.wait_for_timeout(1500)
        await d_page.screenshot(path='scratch/desktop_k7_slide7_current.png')
        
        await browser.close()

asyncio.run(main())
