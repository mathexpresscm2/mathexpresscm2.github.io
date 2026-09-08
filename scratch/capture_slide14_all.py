import asyncio
from playwright.async_api import async_playwright
import os

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Mobile view K7
        page = await browser.new_page(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        file_k7 = os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html')
        await page.goto(f'file:///{file_k7}')
        await page.wait_for_timeout(500)
        for _ in range(13):
            await page.keyboard.press('ArrowRight')
        await page.wait_for_timeout(500)
        await page.screenshot(path=r'scratch\mobile_k7_slide14_top.png')
        await page.evaluate("document.querySelector('#slide-14 .slide-content').scrollTop = 420")
        await page.wait_for_timeout(300)
        await page.screenshot(path=r'scratch\mobile_k7_slide14_scrolled.png')
        await page.close()
        
        # 2. Desktop view K7 (to ensure 100% intact)
        page_desk = await browser.new_page(viewport={'width': 1440, 'height': 900})
        await page_desk.goto(f'file:///{file_k7}')
        await page_desk.wait_for_timeout(500)
        for _ in range(13):
            await page_desk.keyboard.press('ArrowRight')
        await page_desk.wait_for_timeout(500)
        await page_desk.screenshot(path=r'scratch\desktop_k7_slide14.png')
        await page_desk.close()
        
        # 3. Mobile view K8
        page_k8 = await browser.new_page(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        file_k8 = os.path.abspath('Meeting/Khoi 8/Tuan 10 - Hop khoi 8/index.html')
        await page_k8.goto(f'file:///{file_k8}')
        await page_k8.wait_for_timeout(500)
        for _ in range(13):
            await page_k8.keyboard.press('ArrowRight')
        await page_k8.wait_for_timeout(500)
        await page_k8.screenshot(path=r'scratch\mobile_k8_slide14_top.png')
        await page_k8.close()
        
        print('All screenshots captured successfully!')
        await browser.close()

asyncio.run(capture())
