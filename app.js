/**
 * MATHEXPRESS · THƯ VIỆN BÀI TRÌNH CHIẾU (phong cách SlideShare)
 * Dữ liệu: data/presentations.json
 * (mở bằng file:// thì dùng bản dự phòng data/fallback_data.js).
 */
(function () {
  'use strict';

  var GROUPS = [
    { key: 'all', label: 'Tất cả' },
    { key: 'k6', label: 'Khối 6', num: '6' },
    { key: 'k7', label: 'Khối 7', num: '7' },
    { key: 'k8', label: 'Khối 8', num: '8' },
    { key: 'k9', label: 'Khối 9', num: '9' },
    { key: 'bt', label: 'Bổ trợ', num: 'BT' },
    { key: 'tg', label: 'Trợ giảng', num: 'TG' }
  ];

  var items = [], current = 'all';
  var $ = function (id) { return document.getElementById(id); };

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
    return 'all';
  }

  function groupInfo(key) {
    for (var i = 0; i < GROUPS.length; i++) if (GROUPS[i].key === key) return GROUPS[i];
    return GROUPS[0];
  }

  function fmtDate(iso) {
    var d = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || '');
    return d ? d[3] + '/' + d[2] + '/' + d[1] : (iso || '');
  }

  function slideCount(p) {
    var m = /(\d+)\s*slide/i.exec(p.duration || '');
    return m ? m[1] : '';
  }

  function renderFilters() {
    $('filters').innerHTML = GROUPS.map(function (g) {
      var n = g.key === 'all' ? items.length : items.filter(function (p) { return p._g === g.key; }).length;
      if (!n) return '';
      return '<button type="button" data-g="' + g.key + '" aria-pressed="' + (g.key === current) + '">' + g.label + '</button>';
    }).join('');
  }

  function renderGrid() {
    var list = items.filter(function (p) { return current === 'all' || p._g === current; });
    $('count').textContent = list.length + ' bài trình chiếu';
    $('grid').innerHTML = list.map(function (p) {
      var g = groupInfo(p._g), n = slideCount(p);
      return '<a class="card" data-g="' + p._g + '" href="' + encodeURI(p.webViewerUrl || '#') + '" target="_blank" rel="noopener">' +
        '<div class="thumb" data-num="' + (g.num || '') + '">' +
        '<span class="thumb__brand">MathExpress · ' + g.label + '</span>' +
        '<span class="thumb__title">' + esc(p.title) + '</span>' +
        (n ? '<span class="thumb__count">' + n + ' slide</span>' : '') +
        '</div>' +
        '<h2>' + esc(p.title) + '</h2>' +
        '<p class="meta">' + esc(p.audienceBadge || g.label) + ' · ' + fmtDate(p.date) + '</p>' +
        '</a>';
    }).join('');
  }

  $('filters').addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (!b) return;
    var g = b.getAttribute('data-g');
    // Bấm lại khối đang chọn thì bỏ chọn, quay về Tất cả
    current = (g === current) ? 'all' : g;
    renderFilters();
    renderGrid();
  });

  $('theme').addEventListener('click', function () {
    var dark = document.documentElement.getAttribute('data-theme') !== 'dark';
    if (dark) document.documentElement.setAttribute('data-theme', 'dark');
    else document.documentElement.removeAttribute('data-theme');
    try { localStorage.setItem('mx_theme', dark ? 'dark' : 'light'); } catch (e) { }
  });

  function init(data) {
    items = data.filter(function (p) { return p.webViewerUrl; }).map(function (p) {
      return Object.assign({}, p, { _g: groupOf(p) });
    }).sort(function (a, b) { return (b.date || '').localeCompare(a.date || ''); });
    renderFilters();
    renderGrid();
  }

  fetch('data/presentations.json')
    .then(function (r) { if (!r.ok) throw r; return r.json(); })
    .then(init)
    .catch(function () { init(window.INITIAL_PRESENTATIONS || []); });
})();
