import re

file_path = 'Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Desktop guarantee in <style>
desktop_css = """
        /* Đảm bảo bảng trên PC màn hình lớn luôn hiển thị 100% tất cả các cột */
        @media (min-width: 769px) {
            #slide-4 th,
            #slide-4 td {
                display: table-cell !important;
            }
        }
"""

# Insert desktop_css before @media (max-width: 768px)
if "/* Đảm bảo bảng trên PC màn hình lớn" not in content:
    content = content.replace("@media (max-width: 768px) {", desktop_css + "\n        @media (max-width: 768px) {")

# 2. Add mobile tab rules inside @media (max-width: 768px)
mobile_tab_css = """
            /* Phân loại cột theo Tab trên Mobile (Phương án 2) */
            #slide-4[data-track="chuyen"] .col-nangcao,
            #slide-4[data-track="chuyen"] .col-coban {
                display: none !important;
            }
            #slide-4[data-track="chuyen"] table {
                min-width: 100% !important;
                width: 100% !important;
            }

            #slide-4[data-track="nangcao"] .col-chuyen,
            #slide-4[data-track="nangcao"] .col-coban {
                display: none !important;
            }
            #slide-4[data-track="nangcao"] table {
                min-width: 100% !important;
                width: 100% !important;
            }

            #slide-4[data-track="coban"] .col-chuyen,
            #slide-4[data-track="coban"] .col-nangcao {
                display: none !important;
            }
            #slide-4[data-track="coban"] table {
                min-width: 100% !important;
                width: 100% !important;
            }

            #slide-4[data-track="all"] table,
            #slide-4:not([data-track]) table {
                min-width: 580px !important;
            }
"""

if "/* Phân loại cột theo Tab trên Mobile (Phương án 2) */" not in content:
    content = content.replace("/* Tối ưu Slide 4: Bảng Khung chương trình cuộn 2 chiều mượt mà */", mobile_tab_css + "\n            /* Tối ưu Slide 4: Bảng Khung chương trình cuộn 2 chiều mượt mà */")

# 3. Add Tab Buttons in Slide 4
tabs_html = """            <!-- Bộ lọc chọn hệ lớp trên Mobile (Segmented Tabs - Phương án 2) -->
            <div
                class="mobile-track-tabs flex md:hidden items-center justify-between gap-1 p-1 bg-slate-100 border border-slate-200 rounded-xl mb-2 w-full max-w-[98%] shadow-2xs">
                <button type="button" onclick="switchTrack('all', this)"
                    class="track-tab-btn active flex-1 py-1.5 px-1 text-[11.5px] font-bold rounded-lg transition-all text-center bg-brand-blue text-white shadow-xs">
                    Tất cả
                </button>
                <button type="button" onclick="switchTrack('chuyen', this)"
                    class="track-tab-btn flex-1 py-1.5 px-1 text-[11.5px] font-bold rounded-lg transition-all text-center text-slate-600 hover:text-brand-blue">
                    Chuyên
                </button>
                <button type="button" onclick="switchTrack('nangcao', this)"
                    class="track-tab-btn flex-1 py-1.5 px-1 text-[11.5px] font-bold rounded-lg transition-all text-center text-slate-600 hover:text-brand-blue">
                    Nâng cao
                </button>
                <button type="button" onclick="switchTrack('coban', this)"
                    class="track-tab-btn flex-1 py-1.5 px-1 text-[11.5px] font-bold rounded-lg transition-all text-center text-slate-600 hover:text-brand-blue">
                    Cơ bản
                </button>
            </div>
"""

# Place tabs right before mobile-swipe-hint in Slide 4
if "mobile-track-tabs" not in content:
    content = content.replace('<!-- Gợi ý vuốt ngang trên Mobile -->', tabs_html + '\n            <!-- Gợi ý vuốt ngang trên Mobile -->')

# 4. Add switchTrack function and update touch listeners in <script>
script_addition = """
        // Chuyển tab lọc hệ lớp Slide 4 trên Mobile
        function switchTrack(track, btn) {
            const slide4 = document.getElementById('slide-4');
            if (!slide4) return;
            slide4.setAttribute('data-track', track);

            const btns = slide4.querySelectorAll('.track-tab-btn');
            btns.forEach(b => {
                b.classList.remove('bg-brand-blue', 'text-white', 'shadow-xs');
                b.classList.add('text-slate-600');
            });
            btn.classList.add('bg-brand-blue', 'text-white', 'shadow-xs');
            btn.classList.remove('text-slate-600');

            const hint = document.getElementById('slide-4-swipe-hint');
            if (hint) {
                if (track === 'all') {
                    hint.classList.remove('hidden');
                } else {
                    hint.classList.add('hidden');
                }
            }
        }
"""

if "function switchTrack" not in content:
    content = content.replace("function openLightbox", script_addition + "\n        function openLightbox")

# Add id="slide-4-swipe-hint" to mobile-swipe-hint
content = content.replace('class="mobile-swipe-hint flex md:hidden', 'id="slide-4-swipe-hint" class="mobile-swipe-hint flex md:hidden')

# Update touch listener to isolate #slide-4 table and scroll containers
content = content.replace(
    "if (e.target.closest('button, input, select, textarea, a, #lightbox-modal')) return;",
    "if (e.target.closest('button, input, select, textarea, a, #lightbox-modal, #slide-4 table, #slide-4 .border-slate-300, .mobile-track-tabs')) return;"
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Applied Slide 4 Tabs & Touch Isolation successfully!")
