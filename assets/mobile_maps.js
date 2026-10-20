/* Region maps on phones (loaded by theme.js on every page; only acts on pages laid out as #app > aside + main > #map).
 * ≤760 px wide (or a phone held sideways): the map fills the whole screen and the sidebar becomes a bottom sheet
 * with three tabs — Appellations (the list), Calques / Layers (checkboxes), Légende / Legend (the legend cards that
 * floated over the map). Drag or tap the sheet's head to open/close it. The title card, hover hint and compass are
 * hidden; info cards open full-width under the toolbar. Back to the desktop layout when the screen gets wider.
 * 2026-10-20 (user: layers too big, map could not be panned over the whole screen, AOC list barely visible). */
(function () {
  'use strict';
  if (window.__fwMobileMaps) return;
  window.__fwMobileMaps = true;
  var root = document.documentElement;
  var MQ = window.matchMedia('(max-width:760px), (pointer:coarse) and (max-height:500px)');

  var CSS = [
    'html.fw-ms,html.fw-ms body{overscroll-behavior:none;}',
    'html.fw-ms #app{position:fixed!important;inset:0!important;display:block!important;height:auto!important;max-height:none!important;}',
    'html.fw-ms #app>main{position:absolute!important;inset:0!important;height:auto!important;}',
    /* the sheet */
    'html.fw-ms #app>aside{position:absolute!important;left:0;right:0;bottom:0;z-index:800;height:var(--ms-h,84px)!important;max-height:none!important;',
    '  border-right:0!important;border-top:3px solid #c9a24b;border-radius:14px 14px 0 0;box-shadow:0 -8px 28px rgba(43,19,22,.28);',
    '  display:flex!important;flex-direction:column;overflow:hidden!important;transition:height .26s cubic-bezier(.2,.8,.2,1);}',
    'html.fw-ms #app>aside.ms-drag,html.fw-ms #app>aside.ms-now{transition:none;}',
    '.fw-ms-head{flex:none;padding:6px 12px 8px;touch-action:none;cursor:grab;user-select:none;-webkit-user-select:none;}',
    '.fw-ms-grip{width:42px;height:5px;border-radius:3px;background:rgba(201,162,75,.75);margin:0 auto 6px;}',
    '.fw-ms-row{display:flex;align-items:center;gap:8px;}',
    '.fw-ms-title{flex:1;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-size:16px;font-weight:600;line-height:1.25;}',
    '.fw-ms-chev{flex:none;width:30px;height:26px;border:0;background:none;color:#c9a24b;font-size:16px;line-height:1;cursor:pointer;padding:0;transition:transform .2s;}',
    'aside.ms-open .fw-ms-chev{transform:rotate(180deg);}',
    '.fw-ms-tabs{display:flex;gap:6px;margin-top:7px;}',
    '.fw-ms-tab{flex:1;min-width:0;font:700 11px/1 ui-sans-serif,system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;',
    '  padding:9px 4px;border-radius:999px;border:1px solid rgba(201,162,75,.55);background:transparent;color:inherit;cursor:pointer;',
    '  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}',
    'aside.ms-open .fw-ms-tab.on{background:#c9a24b;border-color:#c9a24b;color:#3a0a14;}',
    '.fw-ms-body{flex:1 1 auto;min-height:0;overflow-y:auto;overflow-x:hidden;-webkit-overflow-scrolling:touch;overscroll-behavior:contain;',
    '  padding-bottom:calc(14px + env(safe-area-inset-bottom,0px));}',
    /* everything inside the sheet scrolls as one: no nested scroll boxes */
    '.fw-ms-body>:not(.fw-ms-legend),.fw-ms-body .listwrap,.fw-ms-body .side-scroll{flex:none!important;overflow:visible!important;max-height:none!important;height:auto!important;}',
    '.fw-ms-body .brand{display:none!important;}',
    '.fw-ms-body .layers{border-top:0!important;}',
    '.fw-ms-body .layer-row{padding:8px 4px!important;font-size:14px!important;}',
    '.fw-ms-body .layer-row input{width:18px!important;height:18px!important;}',
    /* tabs: show only the chosen part */
    'aside[data-ms-tab="list"] .fw-ms-layers,aside[data-ms-tab="list"] .fw-ms-legend{display:none!important;}',
    'aside[data-ms-tab="layers"] .fw-ms-body>:not(.fw-ms-layers):not(:has(.fw-ms-layers)),',
    'aside[data-ms-tab="layers"] .fw-ms-body :has(>.fw-ms-layers)>:not(.fw-ms-layers):not(:has(.fw-ms-layers)){display:none!important;}',
    'aside[data-ms-tab="legend"] .fw-ms-body>:not(.fw-ms-legend){display:none!important;}',
    '.fw-ms-legend{padding:12px 16px;display:flex;flex-direction:column;gap:12px;}',
    '.fw-ms-legend>*{position:static!important;inset:auto!important;transform:none!important;max-width:none!important;width:auto!important;',
    '  max-height:none!important;margin:0!important;display:block;box-shadow:none!important;}',
    '.fw-ms-legend>[style*="display: none"],.fw-ms-legend>[style*="display:none"]{display:none!important;}',
    '.fw-ms-empty{padding:18px 16px;font:13px/1.45 ui-sans-serif,system-ui,sans-serif;opacity:.75;}',
    /* map overlays: hide the desktop cards, keep Leaflet controls above the sheet */
    'html.fw-ms #app #title-card,html.fw-ms #app .hint,html.fw-ms #app #hint,html.fw-ms #app #compass{display:none!important;}',
    'html.fw-ms #app .leaflet-bottom{bottom:var(--ms-h,84px);transition:bottom .26s cubic-bezier(.2,.8,.2,1);}',
    'html.fw-ms #app .leaflet-control-attribution{font-size:9px;max-width:60vw;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}',
    /* info cards (hover tip, detail card, readout) open full-width under the toolbar, above the sheet */
    'html.fw-ms #app .info-tip,html.fw-ms #app .info-detail,html.fw-ms #app #readout{position:fixed!important;left:8px!important;right:8px!important;',
    '  top:var(--fw-bar-b,64px)!important;bottom:auto!important;width:auto!important;max-width:none!important;z-index:1001!important;',
    '  max-height:calc(100% - var(--fw-bar-b,64px) - var(--ms-h,84px) - 12px)!important;}'
  ].join('\n');

  function addCss() {
    if (document.getElementById('fw-ms-css')) return;
    var st = document.createElement('style'); st.id = 'fw-ms-css'; st.textContent = CSS;
    (document.head || root).appendChild(st);
  }

  var app, aside, head, body, legendBox, title, tabs = {}, moved = [], state = 'peek', tab = 'list', built = false;
  var isEN = function () { return (root.getAttribute('lang') || '').slice(0, 2) === 'en'; };
  var LABELS = { list: ['Appellations', 'Appellations'], info: ['Infos', 'Info'], layers: ['Calques', 'Layers'], legend: ['Légende', 'Legend'] };

  function pageOk() {
    app = document.getElementById('app');
    aside = app && app.querySelector(':scope>aside');
    return !!(aside && app.querySelector(':scope>main #map'));
  }

  function peekH() { return head ? head.offsetHeight : 84; }
  function heightFor(s) {
    var H = app.clientHeight, top = parseFloat(getComputedStyle(root).getPropertyValue('--fw-bar-b')) || 64;
    if (s === 'full') return Math.max(peekH(), H - top - 6);
    if (s === 'half') return Math.max(peekH(), Math.round(H * 0.52));
    return peekH();
  }
  function setH(px) { root.style.setProperty('--ms-h', px + 'px'); }
  function setState(s, now) {
    state = s;
    if (now) { aside.classList.add('ms-now'); }
    setH(heightFor(s));
    aside.classList.toggle('ms-open', s !== 'peek');
    if (now) { aside.offsetHeight; aside.classList.remove('ms-now'); }   // eslint-disable-line no-unused-expressions
  }
  function setTab(t) {
    tab = t; aside.setAttribute('data-ms-tab', t);
    Object.keys(tabs).forEach(function (k) { tabs[k].classList.toggle('on', k === t); });
    body.scrollTop = 0;
  }
  function labels() {
    var en = isEN();
    Object.keys(tabs).forEach(function (k) { tabs[k].textContent = LABELS[k === 'list' && !aside.querySelector('.listwrap') ? 'info' : k][en ? 1 : 0]; });
    var h1 = aside.querySelector('.brand h1');
    if (title && h1) {                                   // the name only (plan pages add a <small> subtitle)
      var t = ''; h1.childNodes.forEach(function (n) { if (n.nodeType === 3 || (n.nodeType === 1 && !/^(SMALL|BR)$/.test(n.tagName))) t += n.textContent; });
      title.textContent = t.trim() || h1.textContent.trim();
    }
  }

  function build() {
    if (built || !pageOk()) return;
    built = true; moved = [];
    var layers = Array.prototype.filter.call(aside.querySelectorAll('.layers'), function (el) {
      if (el.classList.contains('calques-panel')) return true;
      var t = el.querySelector('.panel-title');
      return t && /^(calques|layers)$/i.test(t.textContent.trim());
    });
    var all = Array.prototype.slice.call(app.querySelectorAll('aside .legend, main>.legend, main>[id$="legend"]'));
    var legends = all.filter(function (el) { return !all.some(function (o) { return o !== el && o.contains(el); }); });

    head = document.createElement('div'); head.className = 'fw-ms-head';
    head.innerHTML = '<div class="fw-ms-grip"></div><div class="fw-ms-row"><div class="fw-ms-title"></div>' +
      '<button type="button" class="fw-ms-chev" aria-label="Ouvrir / fermer">▲</button></div><div class="fw-ms-tabs"></div>';
    title = head.querySelector('.fw-ms-title');
    body = document.createElement('div'); body.className = 'fw-ms-body';
    while (aside.firstChild) body.appendChild(aside.firstChild);
    aside.appendChild(head); aside.appendChild(body);

    layers.forEach(function (el) { el.classList.add('fw-ms-layers'); });
    legendBox = document.createElement('div'); legendBox.className = 'fw-ms-legend';
    legends.forEach(function (el) { moved.push([el, el.parentNode, el.nextSibling]); legendBox.appendChild(el); });
    body.appendChild(legendBox);

    var hasList = Array.prototype.some.call(body.children, function (el) {
      return el !== legendBox && !el.classList.contains('brand') && !el.classList.contains('fw-ms-layers') &&
        (el.querySelector('.layers') ? Array.prototype.some.call(el.children, function (c) { return !c.classList.contains('fw-ms-layers'); }) : true);
    });
    var bar = head.querySelector('.fw-ms-tabs');
    ['list', 'layers', 'legend'].forEach(function (k) {
      if (k === 'list' && !hasList) return;
      if (k === 'layers' && !layers.length) return;
      if (k === 'legend' && !legends.length) return;
      var b = document.createElement('button'); b.type = 'button'; b.className = 'fw-ms-tab';
      b.addEventListener('click', function (e) {
        e.stopPropagation();
        if (state !== 'peek' && tab === k) { setState('peek'); return; }
        setTab(k); if (state === 'peek') setState('half');
      });
      tabs[k] = b; bar.appendChild(b);
    });
    root.classList.add('fw-ms');
    setTab(tabs.list ? 'list' : Object.keys(tabs)[0] || 'list');
    labels();
    setState('peek', true);
    drag();
    refit();
  }

  function teardown() {
    if (!built) return;
    built = false;
    moved.reverse().forEach(function (m) { m[1].insertBefore(m[0], m[2] && m[2].parentNode === m[1] ? m[2] : null); });
    if (legendBox) legendBox.remove();
    while (body.firstChild) aside.insertBefore(body.firstChild, head);
    head.remove(); body.remove();
    Array.prototype.forEach.call(aside.querySelectorAll('.fw-ms-layers'), function (el) { el.classList.remove('fw-ms-layers'); });
    aside.classList.remove('ms-open', 'ms-drag', 'ms-now'); aside.removeAttribute('data-ms-tab');
    root.classList.remove('fw-ms'); root.style.removeProperty('--ms-h');
    tabs = {};
    refit();
  }

  // Leaflet must re-measure the map box after the layout switches
  function refit() {
    setTimeout(function () { (window.__fwMaps || []).forEach(function (m) { try { m.invalidateSize(false); } catch (e) {} }); }, 60);
  }

  // drag the head: follow the finger, snap to peek / half / full; a plain tap toggles
  function drag() {
    var y0, h0, moved, t0;
    head.addEventListener('pointerdown', function (e) {
      if (e.target.closest('.fw-ms-tab')) return;
      y0 = e.clientY; h0 = aside.offsetHeight; moved = false; t0 = Date.now();
      try { head.setPointerCapture(e.pointerId); } catch (x) {}
    });
    head.addEventListener('pointermove', function (e) {
      if (y0 == null) return;
      var dy = e.clientY - y0;
      if (!moved && Math.abs(dy) < 6) return;
      moved = true; aside.classList.add('ms-drag');
      setH(Math.max(peekH(), Math.min(heightFor('full'), h0 - dy)));
    });
    function end(e) {
      if (y0 == null) return;
      var dy = e.clientY - y0, fast = Date.now() - t0 < 250; y0 = null;
      aside.classList.remove('ms-drag');
      if (!moved) { setState(state === 'peek' ? 'half' : 'peek'); return; }
      var h = aside.offsetHeight, opts = ['peek', 'half', 'full'], best = state;
      if (fast && Math.abs(dy) > 30) {
        var i = opts.indexOf(state); best = opts[Math.max(0, Math.min(2, i + (dy < 0 ? 1 : -1)))];
      } else {
        var d = 1e9; opts.forEach(function (s) { var x = Math.abs(heightFor(s) - h); if (x < d) { d = x; best = s; } });
      }
      setState(best);
    }
    head.addEventListener('pointerup', end);
    head.addEventListener('pointercancel', end);
  }

  // a fly to an appellation from the full-height list: drop to half height so the target is visible
  document.addEventListener('fw:fly', function () { if (built && state === 'full') setState('half', true); });

  function check() { if (MQ.matches) build(); else teardown(); }
  function start() {
    if (!pageOk()) return;
    addCss();
    check();
    if (MQ.addEventListener) MQ.addEventListener('change', check); else MQ.addListener(check);
    window.addEventListener('resize', function () { if (built) setState(state, true); });
    new MutationObserver(function () { if (built) labels(); }).observe(root, { attributes: true, attributeFilter: ['lang'] });
    var h1 = aside.querySelector('.brand h1');
    if (h1) new MutationObserver(function () { if (built) labels(); }).observe(h1, { childList: true, characterData: true, subtree: true });
  }

  // apply the full-screen layout before the map is created (CSS only needs the html class)
  if (MQ.matches) { addCss(); root.classList.add('fw-ms'); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
  // not a map page after all: drop the early class
  document.addEventListener('DOMContentLoaded', function () { if (!pageOk()) root.classList.remove('fw-ms'); });
})();
