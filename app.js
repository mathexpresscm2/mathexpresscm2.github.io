/**
 * MATHEXPRESS INTERNAL PRESENTATION & COMMUNICATION PORTAL
 * Application Logic & Dynamic Interactions
 */

document.addEventListener('DOMContentLoaded', () => {
  // State Management
  let presentationsData = [];
  let announcementsData = [];
  let currentFilterCategory = 'all';
  let currentFilterAudience = 'all';
  let currentSearchQuery = '';
  let activePresentation = null;
  let currentSlideIndex = 0;
  let bookmarkedIds = JSON.parse(localStorage.getItem('mx_bookmarks') || '[]');

  // DOM Elements
  const presentationsGrid = document.getElementById('presentations-grid');
  const resultCountEl = document.getElementById('result-count');
  const searchInput = document.getElementById('search-input');
  const categoryChips = document.querySelectorAll('.filter-chip');
  const audienceSelect = document.getElementById('audience-select');
  const themeToggleBtn = document.getElementById('theme-toggle');
  const noticeContainer = document.getElementById('notice-container');

  // Modal Elements
  const slideModal = document.getElementById('slide-modal');
  const modalCloseBtn = document.getElementById('modal-close');
  const modalTitle = document.getElementById('modal-title');
  const modalMeta = document.getElementById('modal-meta');
  const slideCanvasTitle = document.getElementById('slide-canvas-title');
  const slideCanvasSubtitle = document.getElementById('slide-canvas-subtitle');
  const slideCanvasContent = document.getElementById('slide-canvas-content');
  const slideCanvasBadge = document.getElementById('slide-canvas-badge');
  const slidePageIndicator = document.getElementById('slide-page-indicator');
  const prevSlideBtn = document.getElementById('prev-slide');
  const nextSlideBtn = document.getElementById('next-slide');
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');
  const tabSpeakerNotes = document.getElementById('tab-speaker-notes');
  const tabActionItems = document.getElementById('tab-action-items');
  const tabDownloads = document.getElementById('tab-downloads');
  const fullscreenBtn = document.getElementById('fullscreen-btn');

  // Initial Load
  initTheme();
  fetchData();

  // Theme Handling
  function initTheme() {
    const savedTheme = localStorage.getItem('mx_theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
  }

  themeToggleBtn.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('mx_theme', newTheme);
    updateThemeIcon(newTheme);
    showToast(`Đã chuyển sang giao diện ${newTheme === 'dark' ? 'Tối' : 'Sáng'}`);
  });

  function updateThemeIcon(theme) {
    themeToggleBtn.innerHTML = theme === 'dark' 
      ? `<svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/></svg>`
      : `<svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/></svg>`;
  }

  // Fetch JSON Data
  async function fetchData() {
    try {
      const [presRes, ancRes] = await Promise.all([
        fetch('data/presentations.json'),
        fetch('data/announcements.json')
      ]);

      presentationsData = await presRes.json();
      announcementsData = await ancRes.json();
    } catch (error) {
      console.warn('Fetch failed (e.g. file:// protocol), using fallback JS data:', error);
      presentationsData = window.INITIAL_PRESENTATIONS || [];
      announcementsData = window.INITIAL_ANNOUNCEMENTS || [];
    }

    renderAnnouncements();
    renderPresentations();
  }

  // Render Announcements Sidebar
  function renderAnnouncements() {
    if (!noticeContainer || !announcementsData.length) return;

    noticeContainer.innerHTML = announcementsData.map(anc => `
      <div class="notice-item">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
          <span class="badge badge-amber">${anc.badge}</span>
          <span style="font-size: 0.75rem; color: var(--text-muted); font-family: var(--font-mono);">${anc.date}</span>
        </div>
        <h4>${anc.title}</h4>
        <p>${anc.summary}</p>
      </div>
    `).join('');
  }

  // Render Presentation Cards
  function renderPresentations() {
    const filtered = presentationsData.filter(item => {
      const catLower = currentFilterCategory.toLowerCase();
      const matchCategory = currentFilterCategory === 'all' || 
        (item.category && item.category.toLowerCase() === catLower) ||
        item.title.toLowerCase().includes(catLower) ||
        (item.audienceBadge && item.audienceBadge.toLowerCase().includes(catLower)) ||
        (item.tags && item.tags.some(tag => tag.toLowerCase().includes(catLower)));

      const matchAudience = currentFilterAudience === 'all' || item.audienceBadge.includes(currentFilterAudience);
      const matchSearch = currentSearchQuery === '' || 
        item.title.toLowerCase().includes(currentSearchQuery.toLowerCase()) ||
        item.speaker.toLowerCase().includes(currentSearchQuery.toLowerCase()) ||
        item.summary.toLowerCase().includes(currentSearchQuery.toLowerCase()) ||
        (item.tags && item.tags.some(tag => tag.toLowerCase().includes(currentSearchQuery.toLowerCase())));

      return matchCategory && matchAudience && matchSearch;
    });

    resultCountEl.textContent = `Hiển thị ${filtered.length} bản trình chiếu`;

    if (filtered.length === 0) {
      presentationsGrid.innerHTML = `
        <div class="empty-state">
          <svg width="48" height="48" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
          <h4>Không tìm thấy bài trình chiếu phù hợp</h4>
          <p style="color: var(--text-muted); font-size: 0.9rem;">Thử thay đổi từ khóa tìm kiếm hoặc bỏ bộ lọc hiện tại.</p>
        </div>
      `;
      return;
    }

    presentationsGrid.innerHTML = filtered.map(item => {
      const isBookmarked = bookmarkedIds.includes(item.id);
      const badgeClass = item.audienceBadge.includes('GV') ? 'badge-gv' : (item.audienceBadge.includes('TG') ? 'badge-tg' : 'badge-amber');
      const hasWebDeck = !!item.webViewerUrl;
      
      return `
        <article class="presentation-card card-col-4" data-id="${item.id}">
          <div class="card-cover">
            <div class="cover-svg-pattern"></div>
            <div class="card-badges">
              <span class="badge ${badgeClass}">${item.audienceBadge}</span>
              <button class="bookmark-btn ${isBookmarked ? 'active' : ''}" data-bookmark-id="${item.id}" title="Lưu bài học">
                <svg width="16" height="16" fill="${isBookmarked ? 'currentColor' : 'none'}" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/></svg>
              </button>
            </div>
            <div class="cover-content">
              <div class="cover-icon">
                <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"/></svg>
              </div>
              <div class="cover-title">${item.title}</div>
            </div>
          </div>

          <div class="card-body">
            <div class="card-meta">
              <span>📅 ${item.date}</span>
              <span>•</span>
              <span>⏱️ ${item.duration}</span>
            </div>
            <h3 class="card-title">${item.title}</h3>
            <p class="card-summary">${item.summary}</p>
            
            <div class="card-speaker">
              <div class="speaker-avatar">${item.speaker.charAt(0)}</div>
              <span>${item.speaker}</span>
            </div>

            <div class="card-footer" style="flex-direction: column; gap: 8px;">
              ${hasWebDeck ? `
                <a href="${item.webViewerUrl}" target="_blank" class="btn btn-primary" style="width: 100%; text-decoration: none;">
                  <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                  Mở Slide Tương Tác (${item.audienceBadge})
                </a>
              ` : ''}

              <button class="btn btn-secondary open-modal-btn" data-pres-id="${item.id}" style="width: 100%;">
                <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
                Xem Tóm Tắt & Ghi Chú
              </button>
            </div>
          </div>
        </article>
      `;
    }).join('');

    // Attach Event Listeners to cards
    document.querySelectorAll('.open-modal-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const presId = e.currentTarget.getAttribute('data-pres-id');
        openSlideModal(presId);
      });
    });

    document.querySelectorAll('.bookmark-btn').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.stopPropagation();
        const id = e.currentTarget.getAttribute('data-bookmark-id');
        toggleBookmark(id);
      });
    });
  }

  // Toggle Bookmarks
  function toggleBookmark(id) {
    if (bookmarkedIds.includes(id)) {
      bookmarkedIds = bookmarkedIds.filter(bId => bId !== id);
      showToast('Đã xóa khỏi danh sách bài lưu');
    } else {
      bookmarkedIds.push(id);
      showToast('Đã lưu bài trình chiếu vào thư viện cá nhân');
    }
    localStorage.setItem('mx_bookmarks', JSON.stringify(bookmarkedIds));
    renderPresentations();
  }

  // Filters & Search Listeners
  categoryChips.forEach(chip => {
    chip.addEventListener('click', () => {
      categoryChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      currentFilterCategory = chip.getAttribute('data-category');
      renderPresentations();
    });
  });

  audienceSelect.addEventListener('change', (e) => {
    currentFilterAudience = e.target.value;
    renderPresentations();
  });

  searchInput.addEventListener('input', (e) => {
    currentSearchQuery = e.target.value;
    renderPresentations();
  });

  // Modal Functionality
  function openSlideModal(id) {
    activePresentation = presentationsData.find(p => p.id === id);
    if (!activePresentation) return;

    currentSlideIndex = 0;
    modalTitle.textContent = activePresentation.title;
    modalMeta.textContent = `${activePresentation.category} • ${activePresentation.speaker} • ${activePresentation.date}`;

    renderSlideContent();
    renderSidebarData();

    slideModal.classList.add('active');
    document.body.style.overflow = 'hidden';
  }

  function closeSlideModal() {
    slideModal.classList.remove('active');
    document.body.style.overflow = '';
  }

  modalCloseBtn.addEventListener('click', closeSlideModal);
  slideModal.addEventListener('click', (e) => {
    if (e.target === slideModal) closeSlideModal();
  });

  // Render Slide in Canvas
  function renderSlideContent() {
    if (!activePresentation || !activePresentation.slides.length) return;

    const slide = activePresentation.slides[currentSlideIndex];
    slideCanvasTitle.textContent = slide.title;
    slideCanvasSubtitle.textContent = slide.subtitle || '';
    
    let contentHTML = slide.content;

    if (activePresentation.webViewerUrl) {
      contentHTML += `
        <div style="margin-top: 20px; padding-top: 16px; border-top: 1px dashed rgba(255,255,255,0.2);">
          <a href="${activePresentation.webViewerUrl}" target="_blank" class="btn btn-primary" style="width: 100%; text-decoration: none;">
            <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
            Mở Bản Trình Chiếu Tương Tác Khối 8 (Toàn Màn Hình)
          </a>
        </div>
      `;
    }

    slideCanvasContent.innerHTML = contentHTML;
    slideCanvasBadge.textContent = slide.badge || `Slide ${slide.page}`;
    slidePageIndicator.textContent = `Slide ${currentSlideIndex + 1} / ${activePresentation.slides.length}`;

    prevSlideBtn.disabled = currentSlideIndex === 0;
    nextSlideBtn.disabled = currentSlideIndex === activePresentation.slides.length - 1;

    // Update Speaker Notes tab dynamically per slide
    tabSpeakerNotes.innerHTML = `
      <div class="notes-box">
        <strong>💡 Ghi chú dành cho diễn giả / Trợ giảng:</strong><br>
        ${slide.notes || 'Không có ghi chú thêm cho slide này.'}
      </div>
      <div style="font-size: 0.88rem; color: var(--text-muted); line-height: 1.6;">
        <h5 style="color: var(--text-main); font-weight: 700; margin-bottom: 8px;">Tóm Tắt Ý Chính Cuộc Họp:</h5>
        <p>${activePresentation.summary}</p>
      </div>
    `;
  }

  // Render Action Items & Downloads
  function renderSidebarData() {
    if (!activePresentation) return;

    // Render Action Items
    tabActionItems.innerHTML = `
      <h5 style="color: var(--text-main); font-weight: 700; margin-bottom: 12px; font-size: 0.92rem;">Danh Sách Việc Cần Làm Sau Họp:</h5>
      <ul class="action-list">
        ${activePresentation.actionItems.map((item, idx) => `
          <li>
            <input type="checkbox" id="act-${idx}">
            <label for="act-${idx}">${item}</label>
          </li>
        `).join('')}
      </ul>
    `;

    // Render Download Links
    tabDownloads.innerHTML = `
      <h5 style="color: var(--text-main); font-weight: 700; margin-bottom: 12px; font-size: 0.92rem;">Tải Về & Trình Chiếu Direct Link:</h5>

      ${activePresentation.webViewerUrl ? `
        <a href="${activePresentation.webViewerUrl}" target="_blank" class="download-link-card" style="border-color: var(--primary); background-color: var(--primary-light);">
          <div style="display: flex; align-items: center; gap: 12px;">
            <div class="download-icon">
              <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
            </div>
            <div>
              <div style="font-weight: 700; font-size: 0.9rem; color: var(--primary);">Slide Web Tương Tác Khối 8 (.html)</div>
              <div style="font-size: 0.75rem; color: var(--text-muted); font-family: var(--font-mono);">MathJax + TikZ Enabled</div>
            </div>
          </div>
          <span class="btn btn-primary" style="padding: 6px 12px; font-size: 0.78rem;">Mở Web Deck</span>
        </a>
      ` : ''}

      <a href="${activePresentation.pptxUrl}" class="download-link-card" onclick="alert('Đang tải file bài giảng PowerPoint (.pptx)...')">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div class="download-icon">
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
          </div>
          <div>
            <div style="font-weight: 700; font-size: 0.9rem;">Bản Trình Chiếu PowerPoint (.pptx)</div>
            <div style="font-size: 0.75rem; color: var(--text-muted); font-family: var(--font-mono);">${activePresentation.fileSize}</div>
          </div>
        </div>
        <span class="btn btn-secondary" style="padding: 6px 12px; font-size: 0.78rem;">Tải Về</span>
      </a>

      <a href="${activePresentation.pdfUrl}" class="download-link-card" onclick="alert('Đang tải file tài liệu PDF...')">
        <div style="display: flex; align-items: center; gap: 12px;">
          <div class="download-icon" style="background-color: rgba(79, 70, 229, 0.1); color: var(--secondary);">
            <svg width="20" height="20" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"/></svg>
          </div>
          <div>
            <div style="font-weight: 700; font-size: 0.9rem;">Tài Liệu Đọc & Bài Tập (.pdf)</div>
            <div style="font-size: 0.75rem; color: var(--text-muted); font-family: var(--font-mono);">4.2 MB</div>
          </div>
        </div>
        <span class="btn btn-secondary" style="padding: 6px 12px; font-size: 0.78rem;">Tải Về</span>
      </a>
    `;
  }

  // Slide Navigation Events
  prevSlideBtn.addEventListener('click', () => {
    if (currentSlideIndex > 0) {
      currentSlideIndex--;
      renderSlideContent();
    }
  });

  nextSlideBtn.addEventListener('click', () => {
    if (activePresentation && currentSlideIndex < activePresentation.slides.length - 1) {
      currentSlideIndex++;
      renderSlideContent();
    }
  });

  // Keyboard navigation for slides
  document.addEventListener('keydown', (e) => {
    if (!slideModal.classList.contains('active')) return;

    if (e.key === 'ArrowLeft' && currentSlideIndex > 0) {
      currentSlideIndex--;
      renderSlideContent();
    } else if (e.key === 'ArrowRight' && activePresentation && currentSlideIndex < activePresentation.slides.length - 1) {
      currentSlideIndex++;
      renderSlideContent();
    } else if (e.key === 'Escape') {
      closeSlideModal();
    }
  });

  // Modal Sidebar Tabs Handling
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetTab = btn.getAttribute('data-tab');
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      document.getElementById(`tab-${targetTab}`).classList.add('active');
    });
  });

  // Fullscreen Mode Handler
  fullscreenBtn.addEventListener('click', () => {
    const playerArea = document.querySelector('.slide-player-area');
    if (!document.fullscreenElement) {
      playerArea.requestFullscreen().catch(err => alert(`Không thể bật chế độ toàn màn hình: ${err.message}`));
    } else {
      document.exitFullscreen();
    }
  });

  // Toast Helper
  function showToast(message) {
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
      toastContainer = document.createElement('div');
      toastContainer.className = 'toast-container';
      document.body.appendChild(toastContainer);
    }

    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `
      <svg width="18" height="18" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/></svg>
      <span>${message}</span>
    `;

    toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.remove();
    }, 3000);
  }
});
