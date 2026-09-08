import asyncio
from playwright.async_api import async_playwright
import os

css_test = """
<style>
@media (max-width: 768px) {
    #slide-14 .bg-blue-50\\/70 {
        padding: 0.875rem !important;
        overflow: visible !important;
        height: auto !important;
        margin: 0 !important;
    }
    #slide-14 .bg-white.rounded-xl {
        overflow: visible !important;
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
    }
    #slide-14 table,
    #slide-14 thead,
    #slide-14 tbody,
    #slide-14 tr,
    #slide-14 th,
    #slide-14 td {
        display: block !important;
        width: 100% !important;
    }
    #slide-14 thead {
        display: none !important;
    }
    #slide-14 td:first-child {
        margin-bottom: 0.875rem !important;
        border-radius: 0.75rem !important;
        border: 1px solid #bfdbfe !important;
        background-color: #ffffff !important;
        padding: 0.875rem !important;
        box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05) !important;
    }
    #slide-14 td:first-child::before {
        content: "📋 Dạng bài kiểm tra (Bài 1 - 5):";
        display: block;
        font-weight: 700;
        font-size: 0.95rem;
        color: #005b9f;
        margin-bottom: 0.625rem;
        padding-bottom: 0.375rem;
        border-bottom: 1px solid #e2e8f0;
    }
    #slide-14 td:last-child {
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
    }
}
</style>
"""

with open('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text_injected = text.replace('</head>', css_test + '</head>')
with open('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index_test14_before.html', 'w', encoding='utf-8') as f:
    f.write(text_injected)

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True)
        file_path = os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index_test14_before.html')
        await page.goto(f'file:///{file_path}')
        await page.wait_for_timeout(500)
        
        for _ in range(13):
            await page.keyboard.press('ArrowRight')
        await page.wait_for_timeout(500)
        
        out_path = os.path.abspath(r'scratch\mobile_slide14_with_header.png')
        await page.screenshot(path=out_path)
        print('Captured to', out_path)
        await browser.close()

asyncio.run(test())
if os.path.exists('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index_test14_before.html'):
    os.remove('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index_test14_before.html')
