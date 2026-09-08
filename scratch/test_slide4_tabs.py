import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from playwright.sync_api import sync_playwright

os.makedirs('scratch/slide4_tabs_test', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 1. TEST DESKTOP
    page_desktop = browser.new_page(viewport={'width': 1920, 'height': 1080})
    page_desktop.goto('file:///' + os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html'))
    page_desktop.wait_for_timeout(500)
    page_desktop.evaluate('''() => {
        const slides = document.querySelectorAll(".slide");
        slides.forEach(s => s.classList.remove("active"));
        document.getElementById("slide-4").classList.add("active");
    }''')
    page_desktop.wait_for_timeout(300)
    
    desktop_info = page_desktop.evaluate('''() => {
        const tabs = document.querySelector("#slide-4 .mobile-track-tabs");
        const chuyen = document.querySelector("#slide-4 .col-chuyen");
        const nangcao = document.querySelector("#slide-4 .col-nangcao");
        const coban = document.querySelector("#slide-4 .col-coban");
        return {
            tabsVisible: tabs ? window.getComputedStyle(tabs).display : 'none',
            chuyenVisible: chuyen ? window.getComputedStyle(chuyen).display : 'none',
            nangcaoVisible: nangcao ? window.getComputedStyle(nangcao).display : 'none',
            cobanVisible: coban ? window.getComputedStyle(coban).display : 'none',
        };
    }''')
    print("Desktop verification:", desktop_info)
    page_desktop.screenshot(path='scratch/slide4_tabs_test/desktop_slide4.png')
    page_desktop.close()

    # 2. TEST MOBILE
    context_mobile = browser.new_context(
        viewport={'width': 390, 'height': 844},
        user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15',
        has_touch=True
    )
    page_mobile = context_mobile.new_page()
    page_mobile.goto('file:///' + os.path.abspath('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html'))
    page_mobile.wait_for_timeout(500)
    page_mobile.evaluate('''() => {
        const slides = document.querySelectorAll(".slide");
        slides.forEach(s => s.classList.remove("active"));
        document.getElementById("slide-4").classList.add("active");
    }''')
    page_mobile.wait_for_timeout(300)

    # Screenshot default (Tất cả)
    page_mobile.screenshot(path='scratch/slide4_tabs_test/mobile_tab_all.png')
    
    # Click Chuyên
    page_mobile.click('#slide-4 button:has-text("Chuyên")')
    page_mobile.wait_for_timeout(200)
    chuyen_w = page_mobile.evaluate('() => document.querySelector("#slide-4 table").offsetWidth')
    print(f"Mobile Tab 'Chuyên' table width: {chuyen_w}px (Screen is 390px)")
    page_mobile.screenshot(path='scratch/slide4_tabs_test/mobile_tab_chuyen.png')

    # Click Nâng cao
    page_mobile.click('#slide-4 button:has-text("Nâng cao")')
    page_mobile.wait_for_timeout(200)
    nangcao_w = page_mobile.evaluate('() => document.querySelector("#slide-4 table").offsetWidth')
    print(f"Mobile Tab 'Nâng cao' table width: {nangcao_w}px (Screen is 390px)")
    page_mobile.screenshot(path='scratch/slide4_tabs_test/mobile_tab_nangcao.png')

    # Click Cơ bản
    page_mobile.click('#slide-4 button:has-text("Cơ bản")')
    page_mobile.wait_for_timeout(200)
    coban_w = page_mobile.evaluate('() => document.querySelector("#slide-4 table").offsetWidth')
    print(f"Mobile Tab 'Cơ bản' table width: {coban_w}px (Screen is 390px)")
    page_mobile.screenshot(path='scratch/slide4_tabs_test/mobile_tab_coban.png')

    # 3. TEST TOUCH ISOLATION ON SLIDE 4
    # Attempt horizontal swipe on table: should NOT change slide!
    page_mobile.click('#slide-4 button:has-text("Tất cả")')
    page_mobile.wait_for_timeout(200)

    # Perform swipe gesture on table
    table_box = page_mobile.evaluate('() => document.querySelector("#slide-4 table").getBoundingClientRect()')
    start_x = table_box['x'] + table_box['width'] / 2
    start_y = table_box['y'] + table_box['height'] / 2
    
    # Swipe left (start_x -> start_x - 120)
    page_mobile.touchscreen.tap(start_x, start_y)
    # Simulate touchstart and touchend with deltaX = -100 on table
    slide_before = page_mobile.evaluate('() => document.querySelector(".slide.active").id')
    page_mobile.evaluate('''() => {
        const table = document.querySelector("#slide-4 table");
        const touchStart = new Touch({
            identifier: 1,
            target: table,
            clientX: 300,
            clientY: 400
        });
        const touchEnd = new Touch({
            identifier: 1,
            target: table,
            clientX: 150,
            clientY: 400
        });
        document.dispatchEvent(new TouchEvent('touchstart', { changedTouches: [touchStart] }));
        document.dispatchEvent(new TouchEvent('touchend', { changedTouches: [touchEnd] }));
    }''')
    page_mobile.wait_for_timeout(300)
    slide_after = page_mobile.evaluate('() => document.querySelector(".slide.active").id')
    print(f"Touch gesture on table: Before={slide_before}, After={slide_after} -> Nav blocked: {slide_before == slide_after}")

    page_mobile.close()
    browser.close()

print("Verification completed successfully!")
