/* French Wine — site-wide menu + FR/EN switch.
   Loaded on every page by theme.js. nav.js is GENERATED from this file by nav_build.py (which fills SITE).

   Where it mounts:
   · Leaflet maps  → a toolbar [☰ Menu | EN | ◐] in the map's top-right corner, beside the zoom control
                     (the zoom is moved there if the page had it top-left).
   · SVG maps (#ctrl, Carte de France / IGP) → the same toolbar beside #ctrl.
   · Pages with a top bar (.topbar) → a « Menu » pill next to the theme / language buttons.
   · Everything else → a small fixed dock top-right (bottom-right on phones).

   Language: localStorage fw_lang + html[lang], the convention of the bilingual pages. On a page without
   its own switch, the EN/FR button swaps every [data-fr]/[data-en] element, so translating a page is
   just a matter of adding data-en attributes. It fires a 'fw:lang' event on document for page scripts. */
(function () {
  if (window.__fwNav) return; window.__fwNav = true;
  var SITE = /*@SITE@*/null;
  var root = document.documentElement;

  // site root = folder above assets/nav.js
  var me = document.currentScript && document.currentScript.src;
  if (!me) { var ss = document.getElementsByTagName('script'); for (var i = ss.length - 1; i >= 0; i--) if (/assets\/nav\.js/.test(ss[i].src)) { me = ss[i].src; break; } }
  var BASE = me.replace(/assets\/nav\.js.*$/, '');
  var here = (function () {
    var u = location.href.split('#')[0].split('?')[0];
    try { u = decodeURIComponent(u); } catch (e) {}
    var b = BASE; try { b = decodeURIComponent(b); } catch (e) {}
    return u.indexOf(b) === 0 ? u.slice(b.length) : u;
  })();

  /* ---------------- language ---------------- */
  function stored() { try { var s = localStorage.getItem('fw_lang'); return s === 'en' || s === 'fr' ? s : ''; } catch (e) { return ''; } }
  function lang() { return (stored() || root.lang || 'fr').slice(0, 2) === 'en' ? 'en' : 'fr'; }
  var OWN_LANG = null;               // the page's own FR/EN button, if any
  function T(fr, en) { return lang() === 'en' ? en : fr; }
  function applyDataLang(l) {
    var ns = document.querySelectorAll('[data-fr][data-en]');
    for (var i = 0; i < ns.length; i++) ns[i].innerHTML = ns[i].getAttribute('data-' + l);
    var ph = document.querySelectorAll('[data-fr-ph][data-en-ph]');
    for (i = 0; i < ph.length; i++) ph[i].placeholder = ph[i].getAttribute('data-' + l + '-ph');
    var tt = document.querySelector('title[data-en]');
    if (tt) document.title = tt.getAttribute('data-' + l);
  }
  function setLang(l) {
    try { localStorage.setItem('fw_lang', l); } catch (e) {}
    if (document.querySelector('[data-fr][data-en]')) root.lang = l;   // only claim the page is EN when it can show EN
    applyDataLang(l);
    refresh();
    try { document.dispatchEvent(new CustomEvent('fw:lang', { detail: l })); } catch (e) {}
  }

  /* ---------------- styles ---------------- */
  var CSS = [
    /* map toolbar */
    '.fw-mapbar{display:flex;align-items:flex-start;gap:8px;clear:both;}',
    '.fw-mapbar .leaflet-control-zoom,.fw-mapbar #ctrl{margin:0!important;position:static!important;float:none!important;}',
    '.fw-bar{display:flex;border-radius:6px;overflow:hidden;box-shadow:0 1px 6px rgba(40,10,15,.28);border:1px solid rgba(154,106,31,.45);background:rgba(251,246,234,.97);}',
    '.fw-bar>button{all:unset;box-sizing:border-box;height:32px;min-width:34px;padding:0 10px;display:inline-flex;align-items:center;justify-content:center;gap:7px;cursor:pointer;',
    '  font:600 11px/1 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:#6a1426;background:transparent;transition:background .15s;}',
    '.fw-bar>button+button{border-left:1px solid rgba(154,106,31,.3);}',
    '.fw-bar>button:hover,.fw-bar>button[aria-expanded="true"]{background:rgba(154,106,31,.14);}',
    '.fw-bar>button:focus-visible{outline:2px solid #9a6a1f;outline-offset:-2px;}',
    '.fw-bar svg{width:16px;height:16px;flex:none;}',
    '.fw-bar .fw-theme-btn{all:unset;box-sizing:border-box;height:32px;width:36px;display:inline-flex;align-items:center;justify-content:center;cursor:pointer;color:#6a1426;border-left:1px solid rgba(154,106,31,.3);}',
    '.fw-bar .fw-theme-btn:hover{background:rgba(154,106,31,.14);}',
    '.fw-bar .fw-theme-btn .fw-tl{display:none;}',
    'html[data-theme="dark"] .fw-bar{background:rgba(28,7,13,.9);border-color:rgba(217,179,107,.4);box-shadow:0 2px 10px rgba(0,0,0,.45);}',
    'html[data-theme="dark"] .fw-bar>button,html[data-theme="dark"] .fw-bar .fw-theme-btn{color:#e7cf9c;}',
    'html[data-theme="dark"] .fw-bar>button+button,html[data-theme="dark"] .fw-bar .fw-theme-btn{border-color:rgba(217,179,107,.25);}',
    'html[data-theme="dark"] .fw-bar>button:hover,html[data-theme="dark"] .fw-bar .fw-theme-btn:hover,html[data-theme="dark"] .fw-bar>button[aria-expanded="true"]{background:rgba(217,179,107,.14);}',
    /* zoom buttons in the site colours */
    '.fw-mapbar .leaflet-bar{border:1px solid rgba(154,106,31,.45)!important;border-radius:6px!important;box-shadow:0 1px 6px rgba(40,10,15,.28)!important;overflow:hidden;}',
    '.fw-mapbar .leaflet-bar a{background:rgba(251,246,234,.97);color:#6a1426;border-bottom-color:rgba(154,106,31,.3);width:32px;height:32px;line-height:32px;}',
    '.fw-mapbar .leaflet-bar a:hover{background:#f1e6cf;}',
    'html[data-theme="dark"] .fw-mapbar .leaflet-bar{border-color:rgba(217,179,107,.4)!important;}',
    'html[data-theme="dark"] .fw-mapbar .leaflet-bar a{background:rgba(28,7,13,.9);color:#e7cf9c;border-bottom-color:rgba(217,179,107,.25);}',
    'html[data-theme="dark"] .fw-mapbar .leaflet-bar a:hover{background:rgba(60,16,26,.95);}',
    '.fw-mapbar.fw-svg{position:absolute;top:12px;right:12px;z-index:20;}',
    /* top-right map cards slide down below the toolbar (--fw-bar-b is measured at mount) */
    /* map title cards always in front of everything drawn on the map (labels, markers, tooltips, popups ≤ 700), below the toolbar (1000) */
    '#title-card,.titlecard{z-index:900!important;}',
    '.fw-has-mapbar #readout,.fw-has-mapbar .titlecard,.fw-has-mapbar #aocPopup{top:var(--fw-bar-b,86px)!important;max-height:calc(100% - var(--fw-bar-b,86px) - 16px)!important;}',
    /* fixed dock for plain pages */
    '.fw-dock{position:fixed;top:14px;right:14px;z-index:100000;display:flex;gap:8px;align-items:center;}',
    '.fw-dock .fw-theme-btn{position:static!important;box-shadow:0 6px 18px rgba(0,0,0,.18);}',
    '.fw-pill{box-shadow:0 6px 18px rgba(0,0,0,.18);}',
    '.fw-grp-inline .fw-pill{box-shadow:none;}',
    '.fw-pill svg{width:15px;height:15px;flex:none;}',
    '@media (max-width:560px){html.fw-has-dock body{padding-bottom:72px;} .fw-dock{top:auto;bottom:14px;right:14px;} .fw-dock .fw-pill .fw-ml{display:none;} .fw-dock .fw-pill{padding:9px;}',
    '  .fw-bar .fw-ml{display:none;}}',
    /* dropdown panel */
    '.fw-menu{position:fixed;z-index:100001;width:min(390px,calc(100vw - 16px));max-height:min(80vh,760px);display:flex;flex-direction:column;',
    '  background:#fbf6ea;color:#2e1419;border:1px solid rgba(154,106,31,.5);border-top:3px solid #8e1f33;border-radius:10px;box-shadow:0 18px 50px rgba(40,10,15,.35);',
    '  font:14px/1.35 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;text-align:left;overflow:hidden;}',
    '.fw-menu[hidden]{display:none;}',
    '.fw-menu *{box-sizing:border-box;}',
    '.fw-mh{display:flex;align-items:center;gap:8px;padding:10px 10px 8px 14px;border-bottom:1px solid rgba(154,106,31,.22);}',
    '.fw-mh b{font:500 18px/1 "Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;color:#6a1426;flex:1;letter-spacing:0;}',
    '.fw-mh b em{color:#9a6a1f;}',
    '.fw-x{all:unset;cursor:pointer;width:28px;height:28px;display:grid;place-items:center;border-radius:50%;color:#6a1426;font-size:20px;line-height:1;}',
    '.fw-x:hover{background:rgba(154,106,31,.14);}',
    '.fw-q{margin:8px 12px 6px;padding:8px 11px;width:calc(100% - 24px);border:1px solid rgba(154,106,31,.4);border-radius:6px;background:#fff;color:#2e1419;font:inherit;font-size:14px;outline:none;}',
    '.fw-q:focus{border-color:#8e1f33;box-shadow:0 0 0 3px rgba(142,31,51,.12);}',
    '.fw-body{overflow-y:auto;overscroll-behavior:contain;padding:2px 6px 10px;}',
    '.fw-menu a{display:block;padding:6px 10px;border-radius:5px;color:#2e1419;text-decoration:none;}',
    '.fw-menu a:hover,.fw-menu a.fw-kb{background:rgba(154,106,31,.13);}',
    '.fw-menu a.fw-cur{background:#8e1f33;color:#fff;font-weight:600;}',
    '.fw-menu a small{display:block;font-size:11px;opacity:.6;margin-top:1px;}',
    '.fw-top{display:flex;flex-wrap:wrap;gap:4px;padding:4px 4px 6px;border-bottom:1px solid rgba(154,106,31,.18);margin-bottom:4px;}',
    '.fw-top a{border:1px solid rgba(154,106,31,.3);padding:5px 10px;font-size:13px;}',
    '.fw-menu details{margin:1px 0;}',
    '.fw-menu summary{list-style:none;cursor:pointer;padding:7px 10px;border-radius:5px;display:flex;align-items:center;gap:8px;user-select:none;}',
    '.fw-menu summary::-webkit-details-marker{display:none;}',
    '.fw-menu summary::before{content:"";width:6px;height:6px;border-right:1.6px solid currentColor;border-bottom:1.6px solid currentColor;transform:rotate(-45deg);transition:transform .15s;opacity:.7;flex:none;}',
    '.fw-menu details[open]>summary::before{transform:rotate(45deg);}',
    '.fw-menu summary:hover{background:rgba(154,106,31,.1);}',
    '.fw-menu summary .fw-n{margin-left:auto;font-size:11px;opacity:.5;}',
    '.fw-l1>summary{font-weight:700;color:#6a1426;font-size:12px;letter-spacing:.12em;text-transform:uppercase;}',
    '.fw-l2>summary{font-weight:600;font-size:13.5px;}',
    '.fw-l1>.fw-in{padding-left:8px;}',
    '.fw-l2>.fw-in{padding-left:16px;border-left:1px solid rgba(154,106,31,.22);margin-left:13px;}',
    '.fw-empty{padding:14px;opacity:.6;font-size:13px;}',
    'html[data-theme="dark"] .fw-menu{background:#1f080e;color:#f1e7d3;border-color:rgba(217,179,107,.4);border-top-color:#c9a24b;box-shadow:0 18px 50px rgba(0,0,0,.6);}',
    'html[data-theme="dark"] .fw-mh b,html[data-theme="dark"] .fw-x,html[data-theme="dark"] .fw-l1>summary{color:#e7cf9c;}',
    'html[data-theme="dark"] .fw-mh b em{color:#c9a24b;}',
    'html[data-theme="dark"] .fw-menu a{color:#f1e7d3;}',
    'html[data-theme="dark"] .fw-menu a.fw-cur{background:#c9a24b;color:#1f080e;}',
    'html[data-theme="dark"] .fw-q{background:#2b0d15;color:#f1e7d3;border-color:rgba(217,179,107,.35);}',
    'html[data-theme="dark"] .fw-q:focus{border-color:#c9a24b;box-shadow:0 0 0 3px rgba(201,162,75,.15);}',
    'html[data-theme="dark"] .fw-mh,html[data-theme="dark"] .fw-top{border-color:rgba(217,179,107,.2);}',
    'html[data-theme="dark"] .fw-top a{border-color:rgba(217,179,107,.3);}',
    'html[data-theme="dark"] .fw-l2>.fw-in{border-color:rgba(217,179,107,.2);}',
    '@media (max-width:560px){.fw-menu{left:8px!important;right:8px!important;top:8px!important;width:auto;max-height:calc(100vh - 80px);}}',
    '@media print{.fw-mapbar .fw-bar,.fw-dock,.fw-menu,.fw-pill{display:none!important;}}'
  ].join('\n');

  var IC_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>';
  var IC_GLOBE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.4 2.6 3.6 5.4 3.6 8.5s-1.2 5.9-3.6 8.5c-2.4-2.6-3.6-5.4-3.6-8.5s1.2-5.9 3.6-8.5Z"/></svg>';

  /* ---------------- menu panel ---------------- */
  var panel, body, q, menuBtns = [], langBtn = null;
  function href(p) { return BASE + encodeURI(p).replace(/#/g, '%23'); }
  function lbl(it) { return lang() === 'en' && it[2] ? it[2] : it[1]; }
  function gl(g) { return lang() === 'en' ? g.en : g.fr; }
  function isCur(p) { return here === p; }
  function hasCur(g) {
    return (g.items || []).some(function (it) { return isCur(it[0]); }) || (g.groups || []).some(hasCur);
  }
  function count(g) { return (g.items || []).length + (g.groups || []).reduce(function (n, s) { return n + count(s); }, 0); }
  function link(it, sub) {
    var a = document.createElement('a');
    a.href = href(it[0]);
    a.textContent = lbl(it);
    if (sub) { var s = document.createElement('small'); s.textContent = sub; a.appendChild(s); }
    if (isCur(it[0])) { a.className = 'fw-cur'; a.setAttribute('aria-current', 'page'); }
    return a;
  }
  function renderTree() {
    body.innerHTML = '';
    var top = document.createElement('div'); top.className = 'fw-top';
    SITE.top.forEach(function (it) { top.appendChild(link(it)); });
    body.appendChild(top);
    SITE.groups.forEach(function (g) { body.appendChild(group(g, 1)); });
  }
  function group(g, lvl) {
    var d = document.createElement('details'); d.className = 'fw-l' + lvl;
    if (hasCur(g)) d.open = true;
    var s = document.createElement('summary');
    s.innerHTML = '<span></span><span class="fw-n"></span>';
    s.firstChild.textContent = gl(g); s.lastChild.textContent = count(g);
    d.appendChild(s);
    var inn = document.createElement('div'); inn.className = 'fw-in';
    (g.items || []).forEach(function (it) { inn.appendChild(link(it)); });
    (g.groups || []).forEach(function (sg) { inn.appendChild(group(sg, lvl + 1)); });
    d.appendChild(inn);
    return d;
  }
  function fold(s) { return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); }
  function flat() {
    var out = [];
    SITE.top.forEach(function (it) { out.push([it, '']); });
    (function walk(gs, path) {
      gs.forEach(function (g) {
        var p = path.concat(gl(g));
        (g.items || []).forEach(function (it) { out.push([it, p.join(' › ')]); });
        walk(g.groups || [], p);
      });
    })(SITE.groups, []);
    return out;
  }
  var kb = -1;
  function search() {
    var v = fold(q.value.trim());
    if (!v) { renderTree(); kb = -1; return; }
    var words = v.split(/\s+/);
    var hits = flat().filter(function (h) {
      var hay = fold(h[0][1] + ' ' + (h[0][2] || '') + ' ' + h[1]);
      return words.every(function (w) { return hay.indexOf(w) >= 0; });
    });
    body.innerHTML = '';
    if (!hits.length) { var e = document.createElement('div'); e.className = 'fw-empty'; e.textContent = T('Aucune page trouvée.', 'No page found.'); body.appendChild(e); }
    hits.slice(0, 80).forEach(function (h) { body.appendChild(link(h[0], h[1])); });
    kb = hits.length ? 0 : -1; mark();
  }
  function mark() {
    var as = body.querySelectorAll('a');
    for (var i = 0; i < as.length; i++) as[i].classList.toggle('fw-kb', i === kb);
    if (as[kb]) as[kb].scrollIntoView({ block: 'nearest' });
  }
  function buildPanel() {
    panel = document.createElement('div'); panel.className = 'fw-menu'; panel.hidden = true;
    panel.setAttribute('role', 'dialog');
    panel.innerHTML = '<div class="fw-mh"><b>' + T('Vins <em>de France</em>', 'Wines <em>of France</em>') + '</b><button class="fw-x" type="button">×</button></div>' +
      '<input class="fw-q" type="search" autocomplete="off" spellcheck="false"><div class="fw-body"></div>';
    body = panel.querySelector('.fw-body'); q = panel.querySelector('.fw-q');
    panel.querySelector('.fw-x').addEventListener('click', close);
    q.addEventListener('input', search);
    q.addEventListener('keydown', function (e) {
      var as = body.querySelectorAll('a');
      if (e.key === 'ArrowDown' && as.length) { kb = Math.min(as.length - 1, kb + 1); mark(); e.preventDefault(); }
      else if (e.key === 'ArrowUp' && as.length) { kb = Math.max(0, kb - 1); mark(); e.preventDefault(); }
      else if (e.key === 'Enter' && as[kb < 0 ? 0 : kb]) { location.href = as[kb < 0 ? 0 : kb].href; }
    });
    ['mousedown', 'wheel', 'touchstart', 'dblclick', 'keydown'].forEach(function (ev) {
      panel.addEventListener(ev, function (e) {
        if (e.key === 'Escape') { close(); if (opener) opener.focus(); }
        e.stopPropagation();          // keep the map (and page shortcuts) out of it
      });
    });
    document.body.appendChild(panel);
    document.addEventListener('mousedown', function (e) {
      if (panel.hidden || panel.contains(e.target) || menuBtns.some(function (b) { return b.contains(e.target); })) return;
      close();
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) { close(); } });
    window.addEventListener('resize', function () { if (!panel.hidden) place(); });
  }
  var opener = null;
  function place() {
    var r = opener.getBoundingClientRect();
    var w = panel.offsetWidth;
    var left = Math.min(Math.max(8, r.right - w), window.innerWidth - w - 8);
    var below = r.bottom + 6;
    panel.style.left = left + 'px'; panel.style.right = 'auto';
    if (below + 200 > window.innerHeight) {          // button near the bottom (phone dock) → open upward
      panel.style.top = 'auto'; panel.style.bottom = (window.innerHeight - r.top + 6) + 'px';
    } else { panel.style.top = below + 'px'; panel.style.bottom = 'auto'; }
  }
  function open(btn) {
    if (!panel) buildPanel();
    opener = btn;
    q.value = ''; q.placeholder = T('Aller à… (région, appellation, cru)', 'Go to… (region, appellation, cru)');
    panel.querySelector('.fw-x').setAttribute('aria-label', T('Fermer', 'Close'));
    renderTree();
    panel.hidden = false; place();
    menuBtns.forEach(function (b) { b.setAttribute('aria-expanded', 'true'); });
    var cur = body.querySelector('.fw-cur'); if (cur) cur.scrollIntoView({ block: 'center' });
    if (window.matchMedia('(pointer:fine)').matches) q.focus();
  }
  function close() {
    if (!panel || panel.hidden) return;
    panel.hidden = true;
    menuBtns.forEach(function (b) { b.setAttribute('aria-expanded', 'false'); });
  }
  function toggleMenu(e) { e.preventDefault(); e.stopPropagation(); if (panel && !panel.hidden) close(); else open(e.currentTarget); }

  /* ---------------- buttons ---------------- */
  function menuButton(cls) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = cls;
    b.setAttribute('aria-haspopup', 'dialog'); b.setAttribute('aria-expanded', 'false');
    b.innerHTML = IC_MENU + '<span class="fw-ml"></span>';
    b.addEventListener('click', toggleMenu);
    menuBtns.push(b);
    return b;
  }
  function languageButton(cls) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = cls;
    b.innerHTML = IC_GLOBE + '<span class="fw-ll"></span>';
    b.addEventListener('click', function (e) { e.stopPropagation(); setLang(lang() === 'en' ? 'fr' : 'en'); });
    langBtn = b;
    return b;
  }
  function refresh() {
    if (panel) panel.querySelector('.fw-mh b').innerHTML = T('Vins <em>de France</em>', 'Wines <em>of France</em>');
    menuBtns.forEach(function (b) {
      b.querySelector('.fw-ml').textContent = 'Menu';
      b.title = T('Toutes les pages du site', 'All pages of the site');
    });
    if (langBtn) {
      langBtn.querySelector('.fw-ll').textContent = lang() === 'en' ? 'FR' : 'EN';
      langBtn.title = T('English version', 'Version française');
    }
    var th = document.querySelector('.fw-bar .fw-theme-btn, .fw-dock .fw-theme-btn');
    if (th) { var l = th.querySelector('.fw-tl'); th.title = l ? l.textContent : ''; }
    if (panel && !panel.hidden) {
      q.placeholder = T('Aller à… (région, appellation, cru)', 'Go to… (region, appellation, cru)');
      if (q.value) search(); else renderTree();
    }
  }

  /* ---------------- mounting ---------------- */
  function themeBtn() { return document.querySelector('.fw-theme-btn'); }

  function mapBar(zoomEl) {
    var bar = document.createElement('div'); bar.className = 'fw-bar';
    bar.appendChild(menuButton(''));
    if (!OWN_LANG) bar.appendChild(languageButton(''));
    var th = themeBtn();
    if (th) { th.classList.remove('fw-float'); bar.appendChild(th); }
    var wrap = document.createElement('div'); wrap.className = 'fw-mapbar';
    wrap.appendChild(bar);
    if (zoomEl) wrap.appendChild(zoomEl);
    return wrap;
  }

  function measure(wrap, container) {
    function m() {
      var b = wrap.getBoundingClientRect().bottom - container.getBoundingClientRect().top;
      if (b > 0) root.style.setProperty('--fw-bar-b', Math.round(b + 10) + 'px');
    }
    m(); window.addEventListener('resize', m);
  }

  /* Keep the map's own floating cards (title card, grand-cru card, info boxes…) clear of the toolbar:
     any positioned element that overlaps it is moved just below it. Re-checked on resize and whenever
     one of those cards changes (shown, filled, re-classed). The map itself is never walked. */
  function keepClear(wrap, scope, skip) {
    var busy = false, queued = false;
    function isSkipped(n) { return n === skip || n === wrap || (skip && skip.contains(n)) || wrap.contains(n) || (skip && n.contains && n.contains(skip)); }   // the last: a zoom wrapper around the map
    function cands() {
      var out = [];
      (function walk(el) {
        for (var c = el.firstElementChild; c; c = c.nextElementSibling) {
          if (isSkipped(c) || c.closest('.leaflet-control-container')) continue;
          var p = getComputedStyle(c).position;
          if (p === 'absolute' || p === 'fixed') out.push(c); else walk(c);
        }
      })(scope);
      return out;
    }
    function hit(a, b) { return a.left < b.right + 6 && a.right > b.left - 6 && a.top < b.bottom + 6 && a.bottom > b.top - 6; }
    function check() {
      queued = false; busy = true;
      var bar = wrap.getBoundingClientRect();
      cands().forEach(function (el) {
        if (el.hasAttribute('data-fw-top')) { el.style.top = el.getAttribute('data-fw-top'); el.removeAttribute('data-fw-top'); }
        if (el.hasAttribute('data-fw-mh')) { el.style.maxHeight = el.getAttribute('data-fw-mh'); el.removeAttribute('data-fw-mh'); }
        var cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden') return;
        var r = el.getBoundingClientRect();
        if (r.width < 4 || r.height < 4 || !hit(r, bar)) return;
        var par = (el.offsetParent || scope).getBoundingClientRect();
        if (par.bottom - r.bottom < 60 && r.height > 160 && r.bottom > bar.bottom + 80) {
          // anchored to the bottom (legend…): cap its height rather than stretch it
          el.setAttribute('data-fw-mh', el.style.maxHeight || '');
          el.style.maxHeight = Math.round(r.bottom - bar.bottom - 10) + 'px'; el.style.overflowY = 'auto';
          return;
        }
        el.setAttribute('data-fw-top', el.style.top || '');
        el.style.top = Math.round(bar.bottom - par.top + 10) + 'px';
      });
      obs.takeRecords(); busy = false;
    }
    function later() { if (!queued && !busy) { queued = true; requestAnimationFrame(check); } }
    var obs = new MutationObserver(function (recs) {
      if (busy) return;
      for (var i = 0; i < recs.length; i++) {
        var t = recs[i].target;
        if (t.nodeType === 1 && !isSkipped(t) && !(skip && skip.contains(t))) { later(); return; }
      }
    });
    obs.observe(scope, { childList: true, subtree: true, attributes: true, attributeFilter: ['style', 'class', 'hidden'] });
    window.addEventListener('resize', later);
    if (window.ResizeObserver) { var ro = new ResizeObserver(later); ro.observe(wrap); ro.observe(scope); }
    check(); setTimeout(check, 300); setTimeout(check, 1000); setTimeout(check, 2500);   // fonts / late-drawn cards
  }

  function mountLeaflet(container) {
    var corner = container.querySelector('.leaflet-control-container .leaflet-top.leaflet-right');
    if (!corner) return false;
    var zoom = container.querySelector('.leaflet-control-zoom');
    var wrap = mapBar(zoom);
    wrap.classList.add('leaflet-control');
    corner.insertBefore(wrap, corner.firstChild);
    if (window.L && L.DomEvent) { L.DomEvent.disableClickPropagation(wrap); L.DomEvent.disableScrollPropagation(wrap); }
    root.classList.add('fw-has-mapbar');
    measure(wrap, container);
    keepClear(wrap, container.parentNode, container);
    return true;
  }

  function mountSvg(ctrl) {
    var wrap = mapBar(null);
    wrap.classList.add('fw-svg');
    ctrl.parentNode.insertBefore(wrap, ctrl);
    wrap.appendChild(ctrl);
    root.classList.add('fw-has-mapbar');
    measure(wrap, wrap.parentNode);
    keepClear(wrap, wrap.parentNode, document.getElementById('map'));
  }

  function mountPlain() {
    var th = themeBtn();
    var pill = menuButton('fw-theme-btn fw-pill');
    // top bar pages: next to the page's own theme / language buttons
    var anchor = (th && !th.classList.contains('fw-float')) ? th : document.getElementById('themebtn');
    if (anchor && anchor.parentNode) {
      if (!anchor.classList.contains('fw-theme-btn')) pill.className = anchor.className + ' fw-pill';   // page's own button style
      anchor.parentNode.insertBefore(pill, anchor);
      anchor.parentNode.classList.add('fw-grp-inline');
      return;
    }
    var dock = document.createElement('div'); dock.className = 'fw-dock';
    dock.appendChild(pill);
    if (!OWN_LANG) dock.appendChild(languageButton('fw-theme-btn fw-pill'));
    if (th) { th.classList.remove('fw-float'); dock.appendChild(th); }
    document.body.appendChild(dock);
    root.classList.add('fw-has-dock');
  }

  function mainLeaflet() {
    var cs = document.querySelectorAll('.leaflet-container'), best = null, area = 0;
    for (var i = 0; i < cs.length; i++) {
      var r = cs[i].getBoundingClientRect(), a = r.width * r.height;
      if (a > area || !best) { best = cs[i]; area = a; }
    }
    return best;
  }

  function mount() {
    var st = document.createElement('style'); st.id = 'fw-nav-css'; st.textContent = CSS; document.head.appendChild(st);
    OWN_LANG = document.querySelector('#langbtn, .topbar #lang, .topbar .lang');
    if (!OWN_LANG) {
      var l = stored();
      if (l && document.querySelector('[data-fr][data-en]')) { root.lang = l; applyDataLang(l); }
    }
    new MutationObserver(refresh).observe(root, { attributes: true, attributeFilter: ['lang', 'data-theme'] });

    var isMap = document.getElementById('map') || document.querySelector('.leaflet-container');
    var tries = 0;
    (function attempt() {
      var lc = mainLeaflet();
      if (lc && mountLeaflet(lc)) return refresh();
      var ctrl = document.getElementById('ctrl');
      if (ctrl && ctrl.closest('#stage, main, #app')) { mountSvg(ctrl); return refresh(); }
      // a Leaflet map may still be starting (data decoding) — wait up to ~6 s before falling back
      if (isMap && window.L && tries++ < 60) return setTimeout(attempt, 100);
      mountPlain(); refresh();
    })();
  }
  // Start only once theme.js has built its button: a script injected at runtime can run after parsing
  // but before DOMContentLoaded, i.e. before the theme button exists (it would then float over the bar).
  var started = false;
  function start() { if (started) return; started = true; mount(); adoptLateThemeButtons(); firstVisitLang(); }
  if (window.__fwThemeMounted) start();
  else {
    document.addEventListener('fw:theme-mounted', start);
    window.addEventListener('load', start);                       // theme.js missing or failed: don't wait forever
  }
  // safety net: a floating theme button that appears after mounting is pulled into the bar / dock
  function adoptLateThemeButtons() {
    new MutationObserver(function () {
      var th = document.querySelector('.fw-theme-btn.fw-float');
      var home = document.querySelector('.fw-bar, .fw-dock');
      if (!th || !home) return;
      var dupe = home.querySelector('.fw-theme-btn');
      if (dupe && dupe !== th) { th.remove(); return; }
      th.classList.remove('fw-float'); home.appendChild(th); refresh();
    }).observe(document.body, { childList: true });
  }

  /* ---------------- first visit: choose a language ---------------- */
  // Shown on the home page at its first load of each browser session. The choice is saved in fw_lang like
  // the EN/FR button, so every page then opens in that language.
  // A link to #lang (e.g. the home page footer « Changer de langue ») reopens it at any time.
  function firstVisitLang() {
    window.addEventListener('hashchange', function () { if (location.hash === '#lang') langChooser(true); });
    if (location.hash === '#lang') return langChooser(true);
    // automatic: only on the home page, once per browser session (sessionStorage flag)
    if (!/^(index\.html)?$/.test(here)) return;
    try { if (sessionStorage.getItem('fw_lang_asked')) return; sessionStorage.setItem('fw_lang_asked', '1'); } catch (e) { return; }
    langChooser(!!stored());                                   // a language already chosen = the highlighted button
  }
  function langChooser(reopen) {
    if (document.querySelector('.fw-lang-ov')) return;
    var guess = reopen ? lang() : ((navigator.languages && navigator.languages[0]) || navigator.language || 'fr').slice(0, 2) === 'fr' ? 'fr' : 'en';
    if (!document.getElementById('fw-lang-css')) {
    var st = document.createElement('style'); st.id = 'fw-lang-css'; st.textContent = [
      '.fw-lang-ov{position:fixed;inset:0;z-index:2147483640;display:flex;align-items:center;justify-content:center;padding:16px;',
      '  background:rgba(20,4,9,.55);-webkit-backdrop-filter:blur(6px);backdrop-filter:blur(6px);animation:fwLangIn .3s ease;}',
      '@keyframes fwLangIn{from{opacity:0}to{opacity:1}}',
      '.fw-lang-card{width:min(440px,100%);text-align:center;border-radius:18px;padding:34px 28px 28px;',
      '  background:#2a0a12;color:#f5efe3;border:1px solid rgba(217,179,107,.4);outline:10px solid #992b28;outline-offset:3px;',
      '  box-shadow:0 30px 80px rgba(0,0,0,.5);font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;}',
      '.fw-lang-card h2{font:500 clamp(30px,6vw,40px)/1.05 "Cormorant Garamond",Georgia,"Times New Roman",serif;margin:0;}',
      '.fw-lang-card h2 em{font-style:italic;color:#e7cf9c;}',
      '.fw-lang-card .fw-lang-sub{margin:14px 0 24px;font-size:14px;line-height:1.5;color:rgba(245,239,227,.78);}',
      '.fw-lang-btns{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;}',
      '.fw-lang-btns button{all:unset;box-sizing:border-box;cursor:pointer;flex:1 1 150px;padding:14px 18px;border-radius:999px;',
      '  font:600 15px/1 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;letter-spacing:.04em;',
      '  color:#e7cf9c;border:1px solid rgba(217,179,107,.45);background:rgba(217,179,107,.08);transition:background .18s,border-color .18s;}',
      '.fw-lang-btns button:hover,.fw-lang-btns button:focus-visible{background:rgba(217,179,107,.22);border-color:#d9b36b;}',
      '.fw-lang-btns button{display:inline-flex;align-items:center;justify-content:center;gap:12px;}',
      '.fw-flag{width:36px;height:24px;flex:none;border-radius:3px;box-shadow:0 0 0 1px rgba(0,0,0,.18),0 2px 6px rgba(0,0,0,.2);}',
      'html[data-theme="cream"] .fw-lang-ov{background:rgba(90,40,30,.28);}',
      'html[data-theme="cream"] .fw-lang-card{background:#fffdf8;color:#2e1419;border-color:rgba(154,106,31,.35);box-shadow:0 30px 80px rgba(90,40,30,.25);}',
      'html[data-theme="cream"] .fw-lang-card h2 em{color:#8a5d17;}',
      'html[data-theme="cream"] .fw-lang-card .fw-lang-sub{color:rgba(46,20,25,.7);}',
      'html[data-theme="cream"] .fw-lang-btns button{color:#8e1f33;border-color:rgba(142,31,51,.35);background:rgba(142,31,51,.05);}',
      'html[data-theme="cream"] .fw-lang-btns button:hover,html[data-theme="cream"] .fw-lang-btns button:focus-visible{background:rgba(142,31,51,.12);border-color:#8e1f33;}'
    ].join('\n');
    document.head.appendChild(st);
    }
    var FLAG_FR = '<svg class="fw-flag" viewBox="0 0 3 2" aria-hidden="true"><rect width="1" height="2" fill="#002395"/><rect x="1" width="1" height="2" fill="#fff"/><rect x="2" width="1" height="2" fill="#ed2939"/></svg>';
    var FLAG_UK = '<svg class="fw-flag" viewBox="0 0 60 40" aria-hidden="true"><clipPath id="fw-ukus-a"><path d="M0 0H60L0 40Z"/></clipPath><clipPath id="fw-ukus-b"><path d="M60 0V40H0Z"/></clipPath><g clip-path="url(#fw-ukus-b)"><svg x="0" y="0" width="60" height="40" viewBox="0 0 60 30" preserveAspectRatio="xMidYMid slice"><clipPath id="fw-uk-c"><path d="M30 15h30v15zv15H0zH0V0zV0h30z"/></clipPath><path d="M0 0v30h60V0z" fill="#012169"/><path d="M0 0l60 30m0-30L0 30" stroke="#fff" stroke-width="6"/><path d="M0 0l60 30m0-30L0 30" clip-path="url(#fw-uk-c)" stroke="#C8102E" stroke-width="4"/><path d="M30 0v30M0 15h60" stroke="#fff" stroke-width="10"/><path d="M30 0v30M0 15h60" stroke="#C8102E" stroke-width="6"/></svg></g><g clip-path="url(#fw-ukus-a)"><svg x="0" y="0" width="60" height="40" viewBox="0 0 19 10" preserveAspectRatio="xMinYMin slice"><rect width="19" height="10" fill="#fff"/><rect y="0.000" width="19" height="0.769" fill="#B22234"/><rect y="1.538" width="19" height="0.769" fill="#B22234"/><rect y="3.077" width="19" height="0.769" fill="#B22234"/><rect y="4.615" width="19" height="0.769" fill="#B22234"/><rect y="6.154" width="19" height="0.769" fill="#B22234"/><rect y="7.692" width="19" height="0.769" fill="#B22234"/><rect y="9.231" width="19" height="0.769" fill="#B22234"/><rect width="7.6" height="5.385" fill="#3C3B6E"/><circle cx="0.65" cy="0.60" r=".26" fill="#fff"/><circle cx="1.91" cy="0.60" r=".26" fill="#fff"/><circle cx="3.17" cy="0.60" r=".26" fill="#fff"/><circle cx="4.43" cy="0.60" r=".26" fill="#fff"/><circle cx="5.69" cy="0.60" r=".26" fill="#fff"/><circle cx="6.95" cy="0.60" r=".26" fill="#fff"/><circle cx="0.65" cy="1.65" r=".26" fill="#fff"/><circle cx="1.91" cy="1.65" r=".26" fill="#fff"/><circle cx="3.17" cy="1.65" r=".26" fill="#fff"/><circle cx="4.43" cy="1.65" r=".26" fill="#fff"/><circle cx="5.69" cy="1.65" r=".26" fill="#fff"/><circle cx="6.95" cy="1.65" r=".26" fill="#fff"/><circle cx="0.65" cy="2.70" r=".26" fill="#fff"/><circle cx="1.91" cy="2.70" r=".26" fill="#fff"/><circle cx="3.17" cy="2.70" r=".26" fill="#fff"/><circle cx="4.43" cy="2.70" r=".26" fill="#fff"/><circle cx="5.69" cy="2.70" r=".26" fill="#fff"/><circle cx="6.95" cy="2.70" r=".26" fill="#fff"/><circle cx="0.65" cy="3.75" r=".26" fill="#fff"/><circle cx="1.91" cy="3.75" r=".26" fill="#fff"/><circle cx="3.17" cy="3.75" r=".26" fill="#fff"/><circle cx="4.43" cy="3.75" r=".26" fill="#fff"/><circle cx="5.69" cy="3.75" r=".26" fill="#fff"/><circle cx="6.95" cy="3.75" r=".26" fill="#fff"/><circle cx="0.65" cy="4.80" r=".26" fill="#fff"/><circle cx="1.91" cy="4.80" r=".26" fill="#fff"/><circle cx="3.17" cy="4.80" r=".26" fill="#fff"/><circle cx="4.43" cy="4.80" r=".26" fill="#fff"/><circle cx="5.69" cy="4.80" r=".26" fill="#fff"/><circle cx="6.95" cy="4.80" r=".26" fill="#fff"/></svg></g><path d="M60 0L0 40" stroke="#fff" stroke-width="1.6"/></svg>';   // English: half US (top-left, stars visible), half UK (bottom-right)
    var ov = document.createElement('div'); ov.className = 'fw-lang-ov';
    ov.innerHTML = '<div class="fw-lang-card" role="dialog" aria-modal="true" aria-labelledby="fw-lang-h">' +
      '<h2 id="fw-lang-h">Vins <em>de France</em><br>Wines <em>of France</em></h2>' +
      '<p class="fw-lang-sub">Choisissez votre langue<br>Choose your language</p>' +
      '<div class="fw-lang-btns"><button type="button" data-l="fr" lang="fr">' + FLAG_FR + 'Français</button>' +
      '<button type="button" data-l="en" lang="en">' + FLAG_UK + 'English</button></div></div>';
    function choose(l) {
      ov.remove(); document.removeEventListener('keydown', onKey, true);
      if (location.hash === '#lang') try { history.replaceState(null, '', location.pathname + location.search); } catch (e) {}
      if (OWN_LANG && lang() !== l) OWN_LANG.click();                       // page with its own switch: let it translate itself
      if (stored() !== l) setLang(l);
    }
    function onKey(e) { if (e.key === 'Escape') { e.preventDefault(); choose(guess); } }
    ov.addEventListener('click', function (e) { var b = e.target.closest('button[data-l]'); if (b) choose(b.getAttribute('data-l')); });
    document.addEventListener('keydown', onKey, true);
    document.body.appendChild(ov);
    var f = ov.querySelector('button[data-l="' + guess + '"]'); try { f.focus({ preventScroll: true }); } catch (e) {}
  }

  window.fwNav = { setLang: setLang, lang: lang, chooseLang: function () { langChooser(true); }, open: function () { if (menuBtns[0]) open(menuBtns[0]); } };
})();
