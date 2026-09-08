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
        
        # Capture mobile top view
        await page.screenshot(path='scratch/mobile_k7_slide6_final_top.png')
        
        # Scroll to middle
        await page.evaluate('''() => {
            const el = document.querySelector('#slide-6 .slide-content');
            if (el) el.scrollTop = 300;
        }''')
        await page.wait_for_timeout(500)
        await page.screenshot(path='scratch/mobile_k7_slide6_final_mid.png')
        
        # Scroll to bottom
        await page.evaluate('''() => {
            const el = document.querySelector('#slide-6 .slide-content');
            if (el) el.scrollTop = 700;
        }''')
        await page.wait_for_timeout(500)
        await page.screenshot(path='scratch/mobile_k7_slide6_final_bottom.png')
        
        # 2. Desktop verification (1920 x 1080)
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
            const counter = document.getElementById('slideCounter');
            if (counter) counter.textContent = '6/16';
        }''')
        await d_page.wait_for_timeout(1500)
        await d_page.screenshot(path='scratch/desktop_k7_slide6_final.png')
        
        # 3. Test fallback when image URL fails
        test_context = await browser.new_context(viewport={'width': 393, 'height': 851})
        t_page = await test_context.new_page()
        # Abort request to hinh_bai1.svg to simulate broken image / content URI issue
        await t_page.route('**/*hinh_bai1.svg*', lambda route: route.abort())
        await t_page.goto(f'file:///{file_path}')
        await t_page.wait_for_timeout(1000)
        await t_page.evaluate('''() => {
            const slides = document.querySelectorAll('.slide');
            slides.forEach((s, i) => {
                if (i === 5) s.classList.add('active');
                else s.classList.remove('active');
            });
        }''')
        await t_page.wait_for_timeout(1000)
        await t_page.screenshot(path='scratch/mobile_k7_slide6_fallback_test.png')
        
        await browser.close()
        print("All Slide 6 verifications completed!")

asyncio.run(main())
