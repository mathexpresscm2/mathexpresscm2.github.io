/**
 * MATHEXPRESS · CỔNG CHUYÊN MÔN THCS
 * Trang chủ: bento (họp mới nhất, thông báo, các khối) + dòng thời gian theo khối.
 * Dữ liệu: data/presentations.json, data/announcements.json
 * (mở bằng file:// thì dùng bản dự phòng data/fallback_data.js).
 */
(function () {
  'use strict';

  // ---- Nhóm hiển thị (thứ tự = thứ tự ô và tab) ----
  var GROUPS = [
    { key: 'k6', label: 'Khối 6', short: '6', tone: 'indigo' },
    { key: 'k7', label: 'Khối 7', short: '7', tone: 'sky' },
    { key: 'k8', label: 'Khối 8', short: '8', tone: 'emerald' },
    { key: 'k9', label: 'Khối 9', short: '9', tone: 'rose' },
    { key: 'bt', label: 'GV Bổ trợ', short: 'BT', tone: 'amber' },
    { key: 'tg', label: 'Trợ giảng', short: 'TG', tone: 'purple' }
  ];

  var state = { items: [], notices: [], group: 'all', query: '' };
  var $ = function (id) { return document.getElementById(id); };

  // ---- Tiện ích ----
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function groupOf(p) {
    var t = (p.category + ' ' + p.audienceBadge + ' ' + p.title).toLowerCase();
    if (t.indexOf('khối 6') > -1) return 'k6';
    if (t.indexOf('khối 7') > -1) return 'k7';
    if (t.indexOf('khối 8') > -1) return 'k8';
    if (t.indexOf('khối 9') > -1) return 'k9';
    if (t.indexOf('bổ trợ') > -1) return 'bt';
    if (t.indexOf('trợ giảng') > -1) return 'tg';
    return 'other';
  }

  function groupInfo(key) {
    for (var i = 0; i < GROUPS.length; i++) if (GROUPS[i].key === key) return GROUPS[i];
    return { key: 'other', label: 'Khác', short: '•', tone: 'slate' };
  }

  // "Tuần 14" lấy từ tiêu đề hoặc tên thư mục (Tuan 14, Tuan 02...)
  function weekOf(p) {
    var m = /tu[aầ]n\s*0?(\d+)/i.exec(p.title) || /Tuan\s*0?(\d+)/i.exec(p.webViewerUrl || '');
    return m ? parseInt(m[1], 10) : null;
  }

  function slideCount(p) {
    var m = /(\d+)\s*slide/i.exec(p.duration || '');
    return m ? parseInt(m[1], 10) : null;
  }

  var MONTHS = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'];
  function fmtDate(iso) {
    var d = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || '');
    return d ? d[3] + '/' + d[2] + '/' + d[1] : (iso || '');
  }
  function dayMonth(iso) {
    var d = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || '');
    return d ? { day: d[3], month: 'Th' + MONTHS[parseInt(d[2], 10) - 1] } : { day: '', month: '' };
  }

  function norm(s) {
    return String(s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd');
  }

  function matches(p, q) {
    if (!q) return true;
    var hay = norm([p.title, p.summary, p.category, p.audienceBadge, (p.tags || []).join(' ')].join(' '));
    return norm(q).split(/\s+/).every(function (w) { return hay.indexOf(w) > -1; });
  }

  // ---- Tải dữ liệu ----
  function load() {
    Promise.all([
      fetch('data/presentations.json').then(function (r) { if (!r.ok) throw r; return r.json(); }),
      fetch('data/announcements.json').then(function (r) { if (!r.ok) throw r; return r.json(); })
    ]).then(function (res) {
      init(res[0], res[1]);
    }).catch(function () {
      init(window.INITIAL_PRESENTATIONS || [], window.INITIAL_ANNOUNCEMENTS || []);
    });
  }

  function init(pres, notices) {
    state.items = pres.map(function (p) {
      return Object.assign({}, p, { _g: groupOf(p), _w: weekOf(p), _n: slideCount(p) });
    }).sort(function (a, b) { return (b.date || '').localeCompare(a.date || ''); });
    state.notices = notices.slice().sort(function (a, b) { return (b.date || '').localeCompare(a.date || ''); });

    // Nhớ khối đang xem (theo trình duyệt từng người)
    try {
      var g = localStorage.getItem('mx_group');
      if (g && (g === 'all' || GROUPS.some(function (x) { return x.key === g; }))) state.group = g;
    } catch (e) { }

    renderLatest();
    renderNotices();
    renderGroups();
    renderTabs();
    renderTimeline();
  }

  // ---- Ô lớn: họp mới nhất ----
  function renderLatest() {
    var p = state.items[0];
    if (!p) { $('latest-title').textContent = 'Chưa có buổi họp'; return; }
    var g = groupInfo(p._g);
    $('latest').setAttribute('data-tone', g.tone);
    $('latest-title').textContent = p.title;
    $('latest-meta').innerHTML =
      '<span><i class="fa-regular fa-calendar"></i> ' + fmtDate(p.date) + '</span>' +
      (p._n ? '<span><i class="fa-solid fa-layer-group"></i> ' + p._n + ' slide</span>' : '') +
      '<span><i class="fa-solid fa-users"></i> ' + esc(p.audienceBadge) + '</span>';
    $('latest-summary').textContent = p.summary;
    $('latest-actions').innerHTML = actionsHtml(p, true);
    $('latest-num').textContent = g.short;
  }

  function actionsHtml(p, big) {
    var out = '';
    if (p.webViewerUrl) {
      out += '<a class="btn btn--primary' + (big ? ' btn--lg' : '') + '" href="' + encodeURI(p.webViewerUrl) + '" target="_blank" rel="noopener">' +
        '<i class="fa-solid fa-display"></i> Mở slide</a>';
    }
    out += '<button type="button" class="btn btn--ghost' + (big ? ' btn--lg' : '') + '" data-open="' + esc(p.id) + '">' +
      '<i class="fa-regular fa-file-lines"></i> Tóm tắt</button>';
    return out;
  }

  // ---- Thông báo ----
  function noticeUrl(n) {
    if (n.url) return n.url;
    // Tự nối thông báo với bộ slide cùng "Tuần X - ... Khối Y" nếu có
    var t = norm(n.title);
    for (var i = 0; i < state.items.length; i++) {
      var p = state.items[i];
      if (p._w && p._g.charAt(0) === 'k' && t.indexOf('tuan ' + p._w + ' ') > -1 && t.indexOf('khoi ' + p._g.charAt(1)) > -1) return p.webViewerUrl;
    }
    return '';
  }

  function renderNotices() {
    var list = state.notices.slice(0, 5);
    $('notice-count').textContent = state.notices.length + ' tin';
    $('notice-list').innerHTML = list.map(function (n) {
      var url = noticeUrl(n);
      var inner =
        '<div class="notice__top"><span class="pill pill--' + (n.priority === 'High' ? 'hot' : 'soft') + '">' + esc(n.badge || n.category) + '</span>' +
        '<time datetime="' + esc(n.date) + '">' + fmtDate(n.date) + '</time></div>' +
        '<h3>' + esc(n.title) + '</h3>' +
        '<p>' + esc(n.summary) + '</p>';
      return '<li class="notice">' + (url
        ? '<a href="' + encodeURI(url) + '" target="_blank" rel="noopener">' + inner + '<span class="notice__go">Mở slide <i class="fa-solid fa-arrow-right"></i></span></a>'
        : '<div>' + inner + '</div>') + '</li>';
    }).join('');
  }

  // ---- Ô các khối ----
  function renderGroups() {
    $('group-tiles').innerHTML = GROUPS.map(function (g) {
      var its = state.items.filter(function (p) { return p._g === g.key; });
      var last = its[0];
      return '<button type="button" class="gtile" data-tone="' + g.tone + '" data-group="' + g.key + '"' + (its.length ? '' : ' disabled') + '>' +
        '<span class="gtile__num">' + g.short + '</span>' +
        '<span class="gtile__label">' + g.label + '</span>' +
        '<span class="gtile__meta">' + its.length + ' buổi họp' + (last ? ' · mới nhất ' + fmtDate(last.date).slice(0, 5) : '') + '</span>' +
        '</button>';
    }).join('');
  }

  // ---- Tab lọc ----
  function renderTabs() {
    var tabs = [{ key: 'all', label: 'Tất cả' }].concat(GROUPS);
    $('group-tabs').innerHTML = tabs.map(function (g) {
      var on = state.group === g.key;
      return '<button type="button" role="tab" class="tab" data-group="' + g.key + '" aria-selected="' + on + '">' + g.label + '</button>';
    }).join('');
    document.querySelectorAll('.gtile').forEach(function (b) {
      b.classList.toggle('is-on', b.getAttribute('data-group') === state.group);
    });
  }

  // ---- Dòng thời gian ----
  function renderTimeline() {
    var its = state.items.filter(function (p) {
      return (state.group === 'all' || p._g === state.group) && matches(p, state.query);
    });
    var gl = state.group === 'all' ? 'tất cả các khối' : groupInfo(state.group).label;
    $('tl-count').textContent = its.length + ' buổi họp · ' + gl + (state.query ? ' · tìm "' + state.query + '"' : '');

    if (!its.length) {
      $('timeline-list').innerHTML = '<li class="empty"><i class="fa-regular fa-face-meh"></i><p>Không có buổi họp phù hợp. Thử từ khóa khác hoặc chọn "Tất cả".</p></li>';
      return;
    }

    $('timeline-list').innerHTML = its.map(function (p, i) {
      var g = groupInfo(p._g), dm = dayMonth(p.date);
      var tags = (p.tags || []).filter(function (t) { return !/^(khối \d|toán \d|họp giáo viên)$/i.test(t); }).slice(0, 4);
      return '<li class="ev" data-tone="' + g.tone + '" style="--i:' + Math.min(i, 8) + '">' +
        '<div class="ev__date"><b>' + dm.day + '</b><span>' + dm.month + '</span></div>' +
        '<div class="ev__dot" aria-hidden="true"></div>' +
        '<article class="ev__card">' +
        '<div class="ev__top">' +
        '<span class="pill pill--tone">' + g.label + '</span>' +
        (p._w ? '<span class="pill pill--soft">Tuần ' + p._w + '</span>' : '') +
        (p._n ? '<span class="muted">' + p._n + ' slide</span>' : '') +
        (i === 0 && state.group === 'all' && !state.query ? '<span class="pill pill--hot">Mới nhất</span>' : '') +
        '</div>' +
        '<h3>' + esc(p.title) + '</h3>' +
        '<p class="ev__sum">' + esc(p.summary) + '</p>' +
        (tags.length ? '<div class="ev__tags">' + tags.map(function (t) { return '<span>#' + esc(t) + '</span>'; }).join('') + '</div>' : '') +
        '<div class="ev__actions">' + actionsHtml(p, false) + '</div>' +
        '</article></li>';
    }).join('');
  }

  function setGroup(g, scroll) {
    state.group = g;
    try { localStorage.setItem('mx_group', g); } catch (e) { }
    renderTabs();
    renderTimeline();
    if (scroll) $('timeline').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // ---- Hộp tóm tắt ----
  var modalItem = null, lastFocus = null;

  function openModal(id) {
    modalItem = state.items.filter(function (p) { return p.id === id; })[0];
    if (!modalItem) return;
    lastFocus = document.activeElement;
    $('modal-title').textContent = modalItem.title;
    $('modal-meta').textContent = groupInfo(modalItem._g).label + ' · ' + fmtDate(modalItem.date) + (modalItem.speaker ? ' · ' + modalItem.speaker : '');
    showTab('sum');
    $('summary-modal').hidden = false;
    document.body.classList.add('no-scroll');
    $('modal-close').focus();
  }

  function closeModal() {
    $('summary-modal').hidden = true;
    document.body.classList.remove('no-scroll');
    if (lastFocus) lastFocus.focus();
  }

  function showTab(tab) {
    var p = modalItem, html = '';
    document.querySelectorAll('.mtab').forEach(function (b) { b.classList.toggle('is-on', b.getAttribute('data-tab') === tab); });
    if (tab === 'sum') {
      html = '<p class="lead">' + esc(p.summary) + '</p>' + (p.slides || []).map(function (s) {
        // nội dung slide tóm tắt do Bộ phận Chuyên môn soạn trong presentations.json (HTML tin cậy)
        return '<section class="msec"><h4>' + esc(s.title) + '</h4>' + (s.subtitle ? '<p class="muted">' + esc(s.subtitle) + '</p>' : '') +
          '<div class="msec__body">' + (s.content || '') + '</div>' +
          (s.notes ? '<p class="note"><i class="fa-regular fa-lightbulb"></i> ' + esc(s.notes) + '</p>' : '') + '</section>';
      }).join('');
    } else if (tab === 'todo') {
      var acts = p.actionItems || [];
      html = acts.length ? '<ul class="todo">' + acts.map(function (a, i) {
        return '<li><input type="checkbox" id="todo-' + i + '"><label for="todo-' + i + '">' + esc(a) + '</label></li>';
      }).join('') + '</ul>' : '<p class="muted">Chưa có danh sách việc cần làm.</p>';
    } else {
      var files = [];
      if (p.webViewerUrl) files.push({ url: p.webViewerUrl, icon: 'fa-display', name: 'Slide tương tác (HTML)', hint: 'Mở trên máy tính hoặc điện thoại' });
      if (p.pdfUrl && p.pdfUrl !== '#' && /\.pdf$/i.test(p.pdfUrl)) files.push({ url: p.pdfUrl, icon: 'fa-file-pdf', name: 'Văn bản kế hoạch (PDF)', hint: 'Tài liệu gốc của buổi họp' });
      if (p.pptxUrl && p.pptxUrl !== '#' && /\.(pptx|docx)$/i.test(p.pptxUrl)) files.push({ url: p.pptxUrl, icon: /docx$/i.test(p.pptxUrl) ? 'fa-file-word' : 'fa-file-powerpoint', name: /docx$/i.test(p.pptxUrl) ? 'Văn bản (DOCX)' : 'PowerPoint (PPTX)', hint: 'Tải về máy' });
      html = files.map(function (f) {
        return '<a class="file" href="' + encodeURI(f.url) + '" target="_blank" rel="noopener"><i class="fa-solid ' + f.icon + '"></i><span><b>' + f.name + '</b><small>' + f.hint + '</small></span><i class="fa-solid fa-arrow-up-right-from-square"></i></a>';
      }).join('');
    }
    $('modal-body').innerHTML = html;
    $('modal-body').scrollTop = 0;
  }

  // ---- Sự kiện ----
  document.addEventListener('click', function (e) {
    var t = e.target.closest('[data-open]');
    if (t) { openModal(t.getAttribute('data-open')); return; }
    t = e.target.closest('.gtile');
    if (t && !t.disabled) { setGroup(t.getAttribute('data-group'), true); return; }
    t = e.target.closest('.tab');
    if (t) { setGroup(t.getAttribute('data-group'), false); return; }
    t = e.target.closest('.mtab');
    if (t) { showTab(t.getAttribute('data-tab')); return; }
    if (e.target.id === 'summary-modal' || e.target.closest('#modal-close')) closeModal();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !$('summary-modal').hidden) closeModal();
    if (e.key === '/' && document.activeElement !== $('search-input') && !/input|textarea/i.test(document.activeElement.tagName)) {
      e.preventDefault();
      $('search-input').focus();
    }
  });

  var searchT;
  $('search-input').addEventListener('input', function (e) {
    clearTimeout(searchT);
    var v = e.target.value.trim();
    searchT = setTimeout(function () {
      state.query = v;
      renderTimeline();
    }, 120);
  });
  $('search-input').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') $('timeline').scrollIntoView({ behavior: 'smooth', block: 'start' });
  });

  // ---- Giao diện sáng / tối ----
  function syncThemeIcon() {
    var dark = document.documentElement.getAttribute('data-theme') === 'dark';
    $('theme-toggle').innerHTML = '<i class="fa-solid ' + (dark ? 'fa-sun' : 'fa-moon') + '" aria-hidden="true"></i>';
  }
  $('theme-toggle').addEventListener('click', function () {
    var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('mx_theme', next); } catch (e) { }
    syncThemeIcon();
  });
  syncThemeIcon();

  load();
})();
