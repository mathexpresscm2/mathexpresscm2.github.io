import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        file_path = os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html')
        
        # 1. Mobile (Pixel 5)
        mobile_context = await browser.new_context(
            viewport={'width': 393, 'height': 851},
            device_scale_factor=2.75,
            is_mobile=True,
            has_touch=True
        )
        page = await mobile_context.new_page()
        await page.goto(f'file:///{file_path}')
        await page.wait_for_timeout(1000)
        
        # Navigate to Slide 6 (index 5)
        await page.evaluate('''() => {
            const slides = document.querySelectorAll('.slide');
            slides.forEach((s, i) => {
                if (i === 5) s.classList.add('active');
                else s.classList.remove('active');
            });
            const counter = document.getElementById('slideCounter');
            if (counter) counter.textContent = '6/16';
        }''')
        await page.wait_for_timeout(1500)
        
        await page.screenshot(path='scratch/mobile_k7_slide6_current_top.png')
        
        # Metrics check
        metrics = await page.evaluate('''() => {
            const card = document.querySelector('#slide-6 .zoom-115');
            const content = document.querySelector('#slide-6 .slide-content');
            const img = document.querySelector('#slide-6 img[alt*="Hình"]');
            return {
                cardScrollHeight: card ? card.scrollHeight : 0,
                cardClientHeight: card ? card.clientHeight : 0,
                contentScrollHeight: content ? content.scrollHeight : 0,
                contentClientHeight: content ? content.clientHeight : 0,
                imgNaturalWidth: img ? img.naturalWidth : 0,
                imgNaturalHeight: img ? img.naturalHeight : 0,
                imgComplete: img ? img.complete : false
            };
        }''')
        print("Slide 6 Metrics:", metrics)
        
        # 2. Desktop (1920 x 1080)
        desktop_context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        d_page = await desktop_context.new_page()
        await d_page.goto(f'file:///{file_path}')
        await d_page.wait_for_timeout(1000)
        await d_page.evaluate('''() => {
            const slides = document.querySelectorAll('.slide');
            slides.forEach((s, i) => {
                if (i === 5) s.classList.add('active');
                else s.classList.remove('active');
            });
        }''')
        await d_page.wait_for_timeout(1500)
        await d_page.screenshot(path='scratch/desktop_k7_slide6_current.png')
        
        await browser.close()

asyncio.run(main())
