import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        file_path = os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html')
        
        # 1. Mobile (Pixel 5: 393 x 851)
        mobile_context = await browser.new_context(
            viewport={'width': 393, 'height': 851},
            device_scale_factor=2.75,
            is_mobile=True,
            has_touch=True
        )
        page = await mobile_context.new_page()
        await page.goto(f'file:///{file_path}')
        await page.wait_for_timeout(1000)
        
        # Navigate to Slide 4 (index 3)
        await page.evaluate('''() => {
            const slides = document.querySelectorAll('.slide');
            slides.forEach((s, i) => {
                if (i === 3) s.classList.add('active');
                else s.classList.remove('active');
            });
            const counter = document.getElementById('slideCounter');
            if (counter) counter.textContent = '4/16';
        }''')
        await page.wait_for_timeout(1000)
        
        # Inject CSS for Slide 4
        css = '''
            #slide-4 .slide-content {
                justify-content: flex-start !important;
                align-items: stretch !important;
                padding: 0.75rem 0.875rem 6rem 0.875rem !important;
            }

            #slide-4 .rounded-xl.border.border-slate-300 {
                overflow-x: auto !important;
                overflow-y: visible !important;
                max-width: 100% !important;
                -webkit-overflow-scrolling: touch !important;
                height: auto !important;
                max-height: none !important;
                flex-shrink: 0 !important;
                border-radius: 0.75rem !important;
            }

            #slide-4 table {
                min-width: 580px !important;
                width: 100% !important;
            }

            #slide-4 .table-custom th,
            #slide-4 .table-custom td {
                padding: 0.45rem 0.5rem !important;
                font-size: 0.82rem !important;
                line-height: 1.3 !important;
            }

            #slide-4 .table-custom th {
                font-size: 0.85rem !important;
                padding: 0.55rem 0.4rem !important;
            }

            #slide-4 .bg-orange-50 {
                margin-top: 0.875rem !important;
                margin-bottom: 2rem !important;
                flex-shrink: 0 !important;
                max-width: 100% !important;
                padding: 0.75rem !important;
            }
        '''
        await page.add_style_tag(content=css)
        await page.wait_for_timeout(500)
        
        # Also add a swipe hint before table in slide 4
        await page.evaluate('''() => {
            const tableWrap = document.querySelector('#slide-4 .rounded-xl.border.border-slate-300');
            if (tableWrap) {
                const hint = document.createElement('div');
                hint.className = 'mobile-swipe-hint flex items-center justify-between text-[12px] text-brand-blue bg-blue-50 border border-blue-200 rounded-lg py-1.5 px-3 mb-2 font-semibold shadow-xs';
                hint.innerHTML = '<span><i class="fa-solid fa-arrows-left-right mr-1.5 text-brand-orange animate-pulse"></i>Vuốt ngang xem đủ các lớp</span><span class="text-slate-500 font-normal text-[11px]">Chuyên • Nâng cao • Cơ bản</span>';
                tableWrap.parentNode.insertBefore(hint, tableWrap);
            }
        }''')
        await page.wait_for_timeout(500)
        
        # 1. Capture top view (left columns)
        await page.screenshot(path='scratch/mobile_k7_slide4_opt_top_left.png')
        
        # 2. Scroll horizontally to the right of table
        await page.evaluate('''() => {
            const wrap = document.querySelector('#slide-4 .rounded-xl.border.border-slate-300');
            if (wrap) wrap.scrollLeft = 240;
        }''')
        await page.wait_for_timeout(500)
        await page.screenshot(path='scratch/mobile_k7_slide4_opt_top_right.png')
        
        # 3. Scroll vertically down to see buổi 12 (Kiểm tra quý I) and Tháng 10
        await page.evaluate('''() => {
            const el = document.querySelector('#slide-4 .slide-content');
            if (el) el.scrollTop = 380;
        }''')
        await page.wait_for_timeout(500)
        await page.screenshot(path='scratch/mobile_k7_slide4_opt_mid.png')
        
        # 4. Scroll vertically to bottom (see buổi 16, 17 and footer note)
        await page.evaluate('''() => {
            const el = document.querySelector('#slide-4 .slide-content');
            if (el) el.scrollTop = 800;
        }''')
        await page.wait_for_timeout(500)
        await page.screenshot(path='scratch/mobile_k7_slide4_opt_bottom.png')
        
        # Metrics check
        metrics = await page.evaluate('''() => {
            const content = document.querySelector('#slide-4 .slide-content');
            const wrap = document.querySelector('#slide-4 .rounded-xl.border.border-slate-300');
            return {
                contentScrollHeight: content ? content.scrollHeight : 0,
                contentClientHeight: content ? content.clientHeight : 0,
                wrapScrollWidth: wrap ? wrap.scrollWidth : 0,
                wrapClientWidth: wrap ? wrap.clientWidth : 0,
            };
        }''')
        print("Slide 4 Metrics:", metrics)
        
        # 5. Desktop check (1920x1080)
        desktop_context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        d_page = await desktop_context.new_page()
        await d_page.goto(f'file:///{file_path}')
        await d_page.wait_for_timeout(1000)
        await d_page.evaluate('''() => {
            const slides = document.querySelectorAll('.slide');
            slides.forEach((s, i) => {
                if (i === 3) s.classList.add('active');
                else s.classList.remove('active');
            });
            const counter = document.getElementById('slideCounter');
            if (counter) counter.textContent = '4/16';
        }''')
        await d_page.wait_for_timeout(1000)
        await d_page.screenshot(path='scratch/desktop_k7_slide4_check.png')
        
        await browser.close()

asyncio.run(main())
