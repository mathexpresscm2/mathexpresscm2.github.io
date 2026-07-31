import re

data = [
    {
        "title": r"Dạng 1: Rút gọn biểu thức lũy thừa",
        "de_bai": r"Rút gọn các biểu thức sau $A = 2 + 2^2 + 2^3 + ... + 2^{100}$",
        "phuong_phap": [
            r"Bước $1$: Nhận xét tổng gồm các lũy thừa có cùng cơ số, số mũ cách đều.",
            r"Bước $2$: Xác định hai số hạng liên tiếp gấp nhau bao nhiêu lần rồi nhân cả biểu thức với số vừa tìm được",
            r"Bước $3$: Lấy biểu thức mới trừ biểu thức ban đầu để các số hạng ở giữa triệt tiêu.",
            r"Bước $4$: Rút gọn và tìm kết quả."
        ],
        "loi_sai": [
            r"❌ <strong>Nhầm lẫn hệ số của $A$ khi cơ số khác $2$</strong>",
            r"Lỗi sai: Áp dụng máy móc bài toán $2A - A = A$ cho các bài toán khác cơ số (như $3, 4, 5$).",
            r"❌ <strong>Nhầm lẫn khi nhân lũy thừa (Sai quy tắc lũy thừa)</strong>",
            r"Lỗi sai: Khi nhân $2A$, học sinh lấy cơ số nhân với $2$ hoặc cộng nhầm số mũ.",
            r"Ví dụ sai: $2 \cdot 2^3 = 4^3$ hoặc $2 \cdot 2^{100} = 2^{200}$"
        ],
        "huong_dan": [
            r"Ta có: $A = 2 + 2^2 + 2^3 + ... + 2^{100}$",
            r"Suy ra: $2A = 2^2 + 2^3 + 2^4 + ... + 2^{101}$",
            r"Suy ra: $2A - A = 2^2 + 2^3 + 2^4 + ... + 2^{101} - (2 + 2^2 + 2^3 + ... + 2^{100})$",
            r"$A = 2^2 + 2^3 + 2^4 + ... + 2^{101} - 2 - 2^2 - 2^3 - ... - 2^{100}$",
            r"$A = 2^{101} - 2$",
            r"Vậy $A = 2^{101} - 2$"
        ]
    },
    {
        "title": r"Dạng 2: Bài toán chia có dư và chia hết",
        "de_bai": r"Cho số $N = \overline{5a27b}$. Tìm chữ số $a, b$ để được số có năm chữ số khác nhau, biết khi chia số đó cho $3$ thì dư $2$, chia cho $5$ dư $1$ và chia hết cho $2$",
        "phuong_phap": [
            r"Xét lần lượt các dấu hiệu chia hết, ưu tiên điều kiện liên quan đến chữ số tận cùng trước, sau đó sử dụng dấu hiệu chia hết theo tổng các chữ số và kết hợp các điều kiện của đề bài để tìm các chữ số cần điền."
        ],
        "loi_sai": [
            r"❌ <strong>Quên trường hợp $a = 0$:</strong> Học sinh hay có thói quen nghĩ chữ số $a$ luôn thuộc $\{1; 2; 3; ...; 9\}$ mà quên mất $a$ nằm ở vị trí hàng nghìn (không phải hàng cao nhất/hàng chục nghìn) nên $a$ hoàn toàn có thể bằng $0$.",
            r'❌ <strong>Bỏ sót điều kiện "$5$ chữ số khác nhau":</strong> Không loại trường hợp $a = 6$ (vì đã trùng với $b = 6$), dẫn đến kết luận thừa nghiệm.',
            r"❌ <strong>Xử lý đoạn tổng chia dư sai:</strong> Khi $20 + a$ chia $3$ dư $2$, học sinh hay tính nhầm $a$ thay vì lập luận bài bản."
        ],
        "huong_dan": [
            r"Để $N$ chia $5$ dư $1$ và chia hết cho $2$ thì $b = 6$",
            r"Suy ra $N = \overline{5a276}$",
            r"Để $N$ chia $3$ dư $2$ thì $(5+a+2+7+6)$ chia $3$ dư $2$ hay $20+a$ chia $3$ dư $2$",
            r"Mà $a$ là chữ số, suy ra $a \in \{0; 3; 6; 9\}$.",
            r"Theo đề bài, các chữ số khác nhau nên $a \in \{0; 3; 9\}$",
            r"Vậy $a \in \{0; 3; 9\}$ và $b = 6$."
        ]
    },
    {
        "title": r"Dạng 3: Tìm số tự nhiên thỏa mãn quan hệ chia hết",
        "de_bai": r"Tìm số tự nhiên $n$ để: $3n+5$ chia hết cho $2n+1$.",
        "phuong_phap": [
            r"<strong>Cách $1$: phương pháp khử $n$</strong>",
            r"Ý tưởng chính là triệt tiêu biến $n$ để đưa về dạng chỉ còn lại số tự nhiên chia hết cho $2n+1$",
            r"<strong>Cách $2$: Phương pháp biến đổi theo số chia</strong>",
            r"Ý tưởng tách số bị chia $3n+5$ sao cho xuất hiện $2n+1$"
        ],
        "loi_sai": [
            r"❌ <strong>Quên phép thử lại:</strong>",
            r"Tại sao sai: Khi nhân thêm hệ số (ví dụ: nhân $2$ vào $3n+5$), phép suy ra chỉ là phép kéo theo một chiều ($A \vdots B \Rightarrow 2A \vdots B$). Đôi khi $2A \vdots B$ đúng nhưng $A \vdots B$ chưa chắc đúng.",
            r"❌ <strong>Sai lầm khi thực hiện phép trừ triệt tiêu $n$</strong>",
            r"$\left[(6n+10) - (6n+3)\right] \vdots 2n+1$ suy ra $(6n+10 - 6n - 3) \vdots 2n+1$ hay $7 \vdots 2n+1$"
        ],
        "huong_dan": [
            r"<strong>Cách $1$:</strong>",
            r"Ta có $3n+5$ chia hết cho $2n+1$.",
            r"Ta có $\begin{cases} (3n+5) \vdots 2n+1 \\ (2n+1) \vdots 2n+1 \end{cases}$ hay $\begin{cases} 2.(3n+5) \vdots 2n+1 \\ 3.(2n+1) \vdots 2n+1 \end{cases}$ hay $\begin{cases} (6n+10) \vdots 2n+1 \\ (6n+3) \vdots 2n+1 \end{cases}$",
            r"Suy ra $\left[(6n+10) - (6n+3)\right] \vdots 2n+1$ suy ra $(6n+10 - 6n - 3) \vdots 2n+1$ do đó $7 \vdots 2n+1$",
            r"Hay $2n+1 \in \{1; 7\}$ nên $2n \in \{0; 6\}$ (Giáo viên lưu ý không đề cập đến ước)",
            r"Suy ra $n \in \{0; 3\}$",
            r"Thử lại $n \in \{0; 3\}$ đều thỏa mãn. Vậy $n \in \{0; 3\}$",
            r"<strong>Cách $2$: Biến đổi theo số chia</strong>",
            r"Ta có $(3n+5) \vdots 2n+1$ suy ra $2 \cdot (3n+5) \vdots 2n+1$ hay $(6n+10) \vdots 2n+1$",
            r"Suy ra $(6n+10) \vdots 2n+1$ hay $(6n+3+7) \vdots 2n+1$ hay $\left[3.(2n+1)+7\right] \vdots 2n+1$",
            r"Vì $2n+1 \vdots 2n+1$ nên $3.(2n+1) \vdots 2n+1$",
            r"Để $(3n+5) \vdots 2n+1$ thì $7 \vdots 2n+1$",
            r"Do đó $2n+1 \in \{1; 7\}$ hay $n \in \{0; 3\}$. Thử lại $n \in \{0; 3\}$ đều thỏa mãn",
            r"Vậy $n \in \{0; 3\}$"
        ]
    },
    {
        "title": r"Dạng 4: Tìm cặp số tự nhiên từ phương trình tích",
        "de_bai": r"Tìm các cặp số tự nhiên $x, y$ biết: $(x+5)(y-3) = 15$",
        "phuong_phap": [
            r"Bước $1$: Đưa về dạng $A \cdot B = n$",
            r"Bước $2$: Liệt kê tất cả các ước của $n$",
            r"Bước $3$: Thay từng cặp vào để tìm $x; y$",
            r"Bước $4$: Kiểm tra điều kiện và kết luận."
        ],
        "loi_sai": [
            r"❌ Học sinh liệt kê thiếu ước",
            r"❌ Ghép sai cặp giá trị tương ứng giữa $x+5$ và $y-3$"
        ],
        "huong_dan": [
            r"Ta có $(x+5)(y-3) = 15$",
            r"Hay $(x+5);(y-3) \in $ Ư$(15)$",
            r"Mà Ư$(15) = \{1; 3; 5; 15\}$",
            r"Ta có bảng sau:",
            r"<table class='w-full border-collapse border border-slate-300 my-2 text-center'><thead><tr class='bg-slate-100'><th class='border border-slate-300 p-2'>$x+5$</th><th class='border border-slate-300 p-2'>$1$</th><th class='border border-slate-300 p-2'>$3$</th><th class='border border-slate-300 p-2'>$5$</th><th class='border border-slate-300 p-2'>$15$</th></tr></thead><tbody><tr><td class='border border-slate-300 p-2 font-bold'>$y-3$</td><td class='border border-slate-300 p-2'>$15$</td><td class='border border-slate-300 p-2'>$5$</td><td class='border border-slate-300 p-2'>$3$</td><td class='border border-slate-300 p-2'>$1$</td></tr><tr><td class='border border-slate-300 p-2 font-bold'>$x$</td><td class='border border-slate-300 p-2'>Không có giá trị</td><td class='border border-slate-300 p-2'>Không có giá trị</td><td class='border border-slate-300 p-2'>$0$</td><td class='border border-slate-300 p-2'>$10$</td></tr><tr><td class='border border-slate-300 p-2 font-bold'>$y$</td><td class='border border-slate-300 p-2'>$18$</td><td class='border border-slate-300 p-2'>$8$</td><td class='border border-slate-300 p-2'>$6$</td><td class='border border-slate-300 p-2'>$4$</td></tr><tr><td class='border border-slate-300 p-2 font-bold'>KL</td><td class='border border-slate-300 p-2'>KTM</td><td class='border border-slate-300 p-2'>KTM</td><td class='border border-slate-300 p-2'>TM</td><td class='border border-slate-300 p-2'>TM</td></tr></tbody></table>",
            r"Vậy $(x; y) \in \{(0; 6); (10; 4)\}$."
        ],
        "chot_lai": r"💡 <strong>Mẹo khắc phục khi trình bày bảng:</strong> Nhắc học sinh luôn kiểm tra lại tích của dòng $1$ và dòng $2$: $x+5$ và $y-3$ phải luôn bằng đúng $15$."
    },
    {
        "title": r"Dạng 5: Bài toán số nguyên tố",
        "de_bai": r"Tìm số nguyên tố $p$ sao cho $p+2$ và $p+16$ cũng là số nguyên tố.",
        "phuong_phap": [
            r"Thử các số nguyên tố nhỏ trước, sau đó xét các số nguyên tố lớn hơn $3$ theo dạng $3k+1$ hoặc $3k+2$, dùng tính chia hết cho $3$ để loại trừ các trường hợp không thỏa mãn."
        ],
        "loi_sai": [
            r"❌ Quên xét $p=2$ mà học sinh thường nhảy ngay vào xét $p=3$",
            r"❌ Thử $p=3$ thấy đúng $\rightarrow$ Kết luận luôn $p=3$ là số duy nhất mà không chứng minh cho trường hợp $p > 3$"
        ],
        "huong_dan": [
            r"TH1: $p = 2$ thì $p+2 = 4 ; p+16 = 18$ (Loại)",
            r"TH2: $p = 3$ thì $p+2 = 5 ; p+16 = 19$ (TM)",
            r"TH3: $p > 3; p = 3k+1 (k \in \mathbb{N}^*), p = 3k+2 (k \in \mathbb{N}^*)$",
            r"+ Với $p = 3k+1$ thì $p+2 = 3k+1+2 = 3k+3 = 3(k+1) \vdots 3$ và $p+2 > 3$. Nên $p+2$ là hợp số (loại)",
            r"+ Với $p = 3k+2$ thì $p+16 = 3k+2+16 = 3k+18 = 3(k+6) \vdots 3$ và $p+16 > 3$. Nên $p+16$ là hợp số (loại)",
            r"Vậy $p = 3$"
        ]
    },
    {
        "title": r"Dạng 6: Tìm ước chung thông qua phép chia có dư",
        "de_bai": r"Tìm số tự nhiên $x$ biết $253$ chia $x$ thì dư $3$, còn $361$ chia $x$ thì dư $11$.",
        "phuong_phap": [
            r"<strong>Đưa bài toán chia có dư về bài toán tìm ước chung.</strong>",
            r"+ Bước $1$: Xác định điều kiện của số chia: Số chia phải <strong>lớn hơn số dư</strong>.",
            r"+ Bước $2$: Chuyển các phép chia có dư thành phép chia hết: Nếu $a$ chia cho $x$ dư $r$ thì $a-r$ chia hết cho $x$",
            r"+ Bước $3$: Suy ra $x$ là ước chung của các số vừa tìm được.",
            r"+ Bước $4$: Tìm các ước chung, kết hợp điều kiện ban đầu để chọn đáp án."
        ],
        "loi_sai": [
            r"❌ Đặt điều kiện thiếu, chỉ nhớ điều kiện ở số dư đầu tiên $x > 3$ mà quên điều kiện $x > 11$"
        ],
        "huong_dan": [
            r"Điều kiện $(x > 11)$",
            r"Vì $253$ chia $x$ dư $3$ nên $(253 - 3)$ chia hết cho $x$",
            r"Hay $250$ chia hết cho $x$, tức là $x \in $ Ư$(250)$",
            r"$361$ chia $x$ dư $11$ nên $(361 - 11)$ chia hết cho $x$",
            r"Hay $350$ chia hết cho $x$, tức là $x \in $ Ư$(350)$",
            r"Suy ra $x \in $ ƯC$(250, 350)$",
            r"Ta có Ư$(250) = \{1; 2; 5; 10; 25; 50; 125; 250\}$",
            r"Ư$(350) = \{1; 2; 5; 7; 10; 14; 25; 35; 50; 70; 175; 350\}$",
            r"Suy ra $x \in \{1; 2; 5; 10; 25; 50\}$",
            r"Mà $x > 11$ nên $x \in \{25; 50\}$",
            r"Vậy $x \in \{25; 50\}$."
        ]
    },
    {
        "title": r"Dạng 7: Bài toán liên quan đến ƯCLN",
        "de_bai": r"Chứng minh hai số sau là hai số nguyên tố cùng nhau $n+1$ và $n+2$",
        "phuong_phap": [
            r"<strong>Sử dụng tính chất của Ước chung lớn nhất (ƯCLN) và phép biến đổi hiệu hai số.</strong>",
            r"+ Bước $1$: Gọi $d$ là ƯCLN của hai số cần chứng minh. $(d \in \mathbb{N}^*)$",
            r"+ Bước $2$: Vì $d$ là ước chung lớn nhất nên cả hai số chia hết cho $d$.",
            r"+ Bước $3$: Sử dụng tính chất: Nếu $a$ chia hết cho $d$ và $b$ chia hết cho $d$ thì $(a+b) \vdots d$ hoặc $(a-b) \vdots d$",
            r"+ Bước $4$: Chứng minh $1$ chia hết $d$, suy ra $d = 1$",
            r"+ Bước $5$: Kết luận hai số nguyên tố cùng nhau."
        ],
        "loi_sai": [
            r"❌ Thiếu điều kiện của $d$",
            r"❌ Trình bày sai phép trừ triệt tiêu $n$: $\left[(n+2)-(n+1)\right] \vdots d$ suy ra $(n+2-n-1) \vdots d$ hay $1 \vdots d$",
            r"❌ Chưa kết luận đúng yêu cầu đề bài. Sau khi tính ra $d=1$ học sinh dừng lại luôn mà không có dòng kết luận cuối cùng: vì ƯCLN$(n+1; n+2) = 1$ nên $n+1$ và $n+2$ là hai số nguyên tố cùng nhau."
        ],
        "huong_dan": [
            r"Gọi $d =$ ƯCLN$(n+1, n+2)$ $(d \in \mathbb{N}^*)$",
            r"Do đó $\begin{cases} n+1 \vdots d \\ n+2 \vdots d \end{cases}$",
            r"Suy ra $\left[(n+2) - (n+1)\right] \vdots d$",
            r"$1 \vdots d$",
            r"Nên $d=1$ (TM)",
            r"hay ƯCLN$(n+1, n+2) = 1$",
            r"Vậy $n+1$ và $n+2$ là hai số nguyên tố cùng nhau."
        ]
    }
]

html_output = ""

for i, slide in enumerate(data):
    html_output += f'''
    <!-- SLIDE {7 + i}: {slide['title'][:30]}... -->
    <div class="slide bg-white" id="slide-dang-{i+1}">
        <div class="slide-header p-6 bg-brand-light flex items-center justify-between">
            <h2 class="text-lg md:text-[30px] font-bold text-brand-blue uppercase"><i class="fa-solid fa-chalkboard-user mr-3 text-brand-orange"></i>{slide['title']}</h2>
            <img src="../../../logo.png" class="h-10 object-contain" alt="Logo">
        </div>
        <div class="slide-content p-6 overflow-y-auto flex flex-col">
            <div class="flex flex-col gap-5 w-full max-w-[96rem] mx-auto">
                
                <!-- Đề bài -->
                <div class="bg-brand-light border-l-[6px] border-brand-orange p-4 rounded-r-2xl shadow-sm w-full flex-shrink-0 grid grid-cols-1 gap-4 items-center">
                    <div class="space-y-1">
                        <strong class="text-brand-orange text-xl mb-1 flex items-center"><i class="fa-solid fa-file-signature mr-3"></i>Đề bài</strong>
                        <p class="text-base md:text-[18px] text-slate-800 font-medium leading-relaxed ml-2">
                            {slide['de_bai']}
                        </p>
                    </div>
                </div>

                <!-- Phương pháp (Nằm ngang ở trên) -->
                <div class="bg-brand-light border-l-[6px] border-brand-blue p-4 rounded-r-2xl shadow-sm w-full flex-shrink-0">
                    <strong class="text-brand-blue text-xl mb-1 flex items-center"><i class="fa-solid fa-pen-clip mr-3"></i>Phương pháp</strong>
                    <div class="text-[15px] md:text-[17.5px] text-slate-800 font-semibold space-y-1 pt-1 ml-2">
'''
    for pp in slide['phuong_phap']:
        html_output += f"                        <p>{pp}</p>\n"
    html_output += '''                    </div>
                </div>

                <!-- Lỗi sai và Hướng dẫn (Hàng dưới) -->
'''
    if i < 2 or i >= 5:
        # Dạng 1, 2, 6, 7: 50-50
        grid_class = "lg:grid-cols-2"
        col_span_ls = "lg:col-span-1"
        col_span_hd = "lg:col-span-1"
    else:
        # Dạng 3, 4, 5: 30-70
        grid_class = "lg:grid-cols-10"
        col_span_ls = "lg:col-span-3"
        col_span_hd = "lg:col-span-7"
        
    html_output += f'''                <div class="grid grid-cols-1 {grid_class} gap-6 w-full items-stretch">
                    <!-- Lỗi sai -->
                    <div class="{col_span_ls} bg-red-50/80 border border-red-200 rounded-2xl p-6 shadow-sm flex flex-col justify-between min-h-[250px]">
                        <div>
                            <strong class="text-red-600 block mb-3 text-lg md:text-xl uppercase font-bold border-b border-red-200 pb-2.5"><i class="fa-solid fa-circle-xmark mr-2"></i>Lỗi sai của học sinh</strong>
                            <div class="text-[15px] md:text-[17.5px] text-slate-700 leading-relaxed space-y-3">
'''
    for ls in slide['loi_sai']:
        html_output += f"                                <p>{ls}</p>\n"
    html_output += f'''                            </div>
                        </div>
                    </div>

                    <!-- Hướng dẫn -->
                    <div class="{col_span_hd} bg-emerald-50/80 border border-emerald-200 rounded-2xl p-6 shadow-sm flex flex-col justify-between min-h-[250px]">
                        <div>
                            <strong class="text-emerald-700 block mb-3 text-lg md:text-xl uppercase font-bold border-b border-emerald-200 pb-2.5"><i class="fa-solid fa-circle-check mr-2"></i>Hướng dẫn giải</strong>
                            <div class="text-[15px] md:text-[17.5px] text-slate-800 leading-relaxed space-y-3">
'''
    for hd in slide['huong_dan']:
        html_output += f"                                <p>{hd}</p>\n"
    html_output += '''                            </div>
                        </div>
                    </div>
                </div>
'''
    if 'chot_lai' in slide:
        html_output += f'''
                <!-- Chốt lại Container -->
                <div class="mt-2 flex flex-row items-center justify-start w-full gap-4 px-2">
                    <button onclick="document.getElementById('chot-lai-content-{i}').classList.toggle('hidden')"
                        class="w-10 h-10 shrink-0 flex items-center justify-center bg-yellow-100 hover:bg-yellow-200 text-yellow-800 font-bold rounded-full shadow-sm transition-colors border border-yellow-300 group z-10 relative">
                        <i class="fa-solid fa-lightbulb text-yellow-600 text-lg group-hover:scale-110 transition-transform"></i>
                    </button>
                    <div id="chot-lai-content-{i}"
                        class="hidden bg-yellow-50 border-l-4 border-yellow-400 p-2 md:p-3 rounded-r-lg shadow-sm flex-1 border-y border-r border-yellow-200 transition-all">
                        <p class="text-slate-800 font-medium text-sm md:text-base leading-relaxed m-0">
                            {slide['chot_lai']}
                        </p>
                    </div>
                </div>
'''

    html_output += '''            </div>
        </div>
    </div>
'''

with open("slides_generated.html", "w", encoding="utf-8") as f:
    f.write(html_output)
