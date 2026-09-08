import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        page = await context.new_page()
        file_path = os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html')
        file_url = 'file:///' + file_path.replace('\\', '/')
        print('Navigating to', file_url)
        await page.goto(file_url)
        await page.wait_for_timeout(500)
        
        # Navigate to Slide 4
        for _ in range(3):
            await page.locator('#nextBtn').click()
            await page.wait_for_timeout(200)
            
        # Click on 'Nâng cao' tab button
        tab_btn = page.locator('.mobile-track-tabs button:has-text("Nâng cao")')
        await tab_btn.click()
        await page.wait_for_timeout(400)
        
        screenshot_path = os.path.abspath('scratch/screenshot_tab_nangcao.png')
        await page.screenshot(path=screenshot_path)
        print('Screenshot saved to', screenshot_path)
        
        # Check computed styles of the active button
        active_btn = page.locator('.track-tab-btn.active')
        color = await active_btn.evaluate('el => window.getComputedStyle(el).color')
        bg_color = await active_btn.evaluate('el => window.getComputedStyle(el).backgroundColor')
        text = await active_btn.text_content()
        print(f'Active button text: "{text.strip()}", Color: {color}, Background: {bg_color}')
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
