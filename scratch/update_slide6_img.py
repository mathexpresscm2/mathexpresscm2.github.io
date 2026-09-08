import base64

# 1. Read files
with open('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/hinh_bai1.svg', 'rb') as f:
    b64_bai1 = base64.b64encode(f.read()).decode('utf-8')

with open('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Target in Slide 6:
target_old = '''                        <!-- Hình vẽ SVG -->
                        <div class="mt-3 flex justify-center bg-white p-3 rounded-xl border border-slate-200 shadow-sm">
                            <img src="hinh_bai1.svg" class="h-44 xl:h-48 object-contain cursor-pointer"
                                alt="Hình minh họa Bài 1" onclick="openLightbox(this)" />
                        </div>'''

target_new = f'''                        <!-- Hình vẽ SVG -->
                        <div class="mt-3 flex flex-col items-center justify-center bg-white p-3 rounded-xl border border-slate-200 shadow-sm">
                            <img src="hinh_bai1.svg" onerror="if(!this.dataset.fallback){{this.dataset.fallback=1;this.src='data:image/svg+xml;base64,{b64_bai1}';}}" class="h-44 xl:h-48 object-contain cursor-pointer"
                                alt="Hình minh họa Bài 1" onclick="openLightbox(this)" />
                            <span class="block md:hidden text-[11px] text-slate-400 font-medium mt-1"><i
                                    class="fa-solid fa-magnifying-glass-plus mr-1"></i>Chạm để phóng to</span>
                        </div>'''

if target_old in content:
    content = content.replace(target_old, target_new)
    with open('Meeting/Khoi 7/Tuan 10 - Hop khoi 7/index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated Slide 6 image container with base64 fallback and mobile hint!")
else:
    print("Could not find target_old in index.html")
