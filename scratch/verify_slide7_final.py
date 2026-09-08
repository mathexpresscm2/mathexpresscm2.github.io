import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        file_path = os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html')
        
        # 1. Mobile verification (Pixel 5: 393 x 851)
        mobile_context = await browser.new_context(
            viewport={'width': 393, 'height': 851},
            device_scale_factor=2.75,
            is_mobile=True,
            has_touch=True
        )
        page = await mobile_context.new_page()
        await page.goto(f'file:///{file_path}')
        await page.wait_for_timeout(1000)
        
        # Navigate to Slide 7
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
        
        # Capture Top view
        await page.screenshot(path='scratch/mobile_k7_slide7_final_top.png')
        
        # Scroll to middle
        await page.evaluate('''() => {
            const el = document.querySelector('#slide-7 .slide-content');
            if (el) el.scrollTop = 360;
        }''')
        await page.wait_for_timeout(500)
        await page.screenshot(path='scratch/mobile_k7_slide7_final_mid.png')
        
        # Scroll to bottom
        await page.evaluate('''() => {
            const el = document.querySelector('#slide-7 .slide-content');
            if (el) el.scrollTop = 800;
        }''')
        await page.wait_for_timeout(500)
        await page.screenshot(path='scratch/mobile_k7_slide7_final_bottom.png')
        
        # 2. Desktop verification (1920 x 1080)
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
            const counter = document.getElementById('slideCounter');
            if (counter) counter.textContent = '7/16';
        }''')
        await d_page.wait_for_timeout(1500)
        await d_page.screenshot(path='scratch/desktop_k7_slide7_final.png')
        
        await browser.close()
        print("Screenshots captured successfully!")

asyncio.run(main())
