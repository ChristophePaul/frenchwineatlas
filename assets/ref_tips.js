/* French Wine — source pop-ups for superscript references.
   Any <sup><a href="#id">n</a></sup> whose #id is on the page (a sources-list entry) shows that entry in a small
   card on mouse-over or keyboard focus. On touch screens the first tap opens the card, a second tap follows the link.
   Loaded by assets/theme.js on every page; pages without such references are not affected. */
(function () {
  if (window.__fwRefTips) return; window.__fwRefTips = true;
  var root = document.documentElement;
  var tip = null, cur = null, hideT = 0, showT = 0;
  var touch = window.matchMedia && window.matchMedia('(hover: none)').matches;

  var CSS =
    '.fw-reftip{position:absolute;z-index:100001;max-width:min(380px,calc(100vw - 24px));padding:10px 13px 11px;border-radius:12px;' +
    'font:400 12.5px/1.55 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;letter-spacing:0;text-align:left;' +
    'background:#2a0a12;color:rgba(245,239,227,.92);border:1px solid rgba(217,179,107,.55);box-shadow:0 12px 34px rgba(0,0,0,.45);' +
    'opacity:0;transform:translateY(4px);transition:opacity .14s,transform .14s;pointer-events:auto;}' +
    '.fw-reftip.on{opacity:1;transform:none;}' +
    '.fw-reftip .n{display:inline-block;min-width:18px;margin-right:6px;font-weight:700;color:#d9b36b;}' +
    '.fw-reftip a{color:#d9b36b;}' +
    '.fw-reftip i{font-style:italic;}' +
    'html[data-theme="cream"] .fw-reftip{background:#fffdf8;color:#2e1419;border-color:rgba(142,31,51,.4);box-shadow:0 10px 28px rgba(90,30,40,.18);}' +
    'html[data-theme="cream"] .fw-reftip .n,html[data-theme="cream"] .fw-reftip a{color:#8e1f33;}' +
    'html[lang="fr"] .fw-reftip .L.en,html[lang="en"] .fw-reftip .L.fr{display:none;}' +
    '@media print{.fw-reftip{display:none!important;}}';

  function target(a) {
    var h = a.getAttribute('href') || '';
    if (h.charAt(0) !== '#' || h.length < 2) return null;
    var el = document.getElementById(decodeURIComponent(h.slice(1)));
    return el && el.tagName === 'LI' ? el : null;     // only entries of a sources list
  }
  function refLink(e) {
    var a = e.target && e.target.closest && e.target.closest('sup a[href^="#"]');
    return a && target(a) ? a : null;
  }
  function make() {
    if (tip) return;
    var st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);
    tip = document.createElement('div'); tip.className = 'fw-reftip'; tip.setAttribute('role', 'tooltip'); tip.id = 'fw-reftip';
    tip.addEventListener('mouseenter', function () { clearTimeout(hideT); });
    tip.addEventListener('mouseleave', function () { hide(160); });
    document.body.appendChild(tip);
  }
  function show(a) {
    clearTimeout(hideT); make();
    var li = target(a); if (!li) return;
    var ol = li.parentNode, n = 1;
    if (ol && ol.tagName === 'OL') { n = Array.prototype.indexOf.call(ol.children, li) + (+ol.getAttribute('start') || 1); }
    tip.innerHTML = '<span class="n">' + n + '.</span>' + li.innerHTML;
    var links = tip.querySelectorAll('a'); for (var i = 0; i < links.length; i++) { links[i].target = '_blank'; links[i].rel = 'noopener'; }
    tip.classList.remove('on'); tip.style.left = '0px'; tip.style.top = '0px';
    var r = a.getBoundingClientRect(), w = tip.offsetWidth, h = tip.offsetHeight, vw = root.clientWidth;
    var x = Math.max(12, Math.min(r.left + r.width / 2 - w / 2, vw - w - 12));
    var above = r.top - h - 10 > 8;
    var y = above ? r.top - h - 10 : r.bottom + 10;
    tip.style.left = (x + window.scrollX) + 'px'; tip.style.top = (y + window.scrollY) + 'px';
    a.setAttribute('aria-describedby', 'fw-reftip');
    cur = a;
    requestAnimationFrame(function () { tip.classList.add('on'); });
  }
  function hide(delay) {
    clearTimeout(showT); clearTimeout(hideT);
    hideT = setTimeout(function () {
      if (tip) tip.classList.remove('on');
      if (cur) cur.removeAttribute('aria-describedby');
      cur = null;
    }, delay || 0);
  }

  if (!touch) {
    document.addEventListener('mouseover', function (e) {
      var a = refLink(e); if (!a) return;
      clearTimeout(hideT); clearTimeout(showT);
      showT = setTimeout(function () { show(a); }, 90);
    });
    document.addEventListener('mouseout', function (e) {
      var a = refLink(e); if (!a) return;
      if (e.relatedTarget && tip && tip.contains(e.relatedTarget)) return;
      clearTimeout(showT); hide(180);
    });
  }
  document.addEventListener('focusin', function (e) { var a = refLink(e); if (a) show(a); });
  document.addEventListener('focusout', function (e) { if (refLink(e)) hide(150); });
  document.addEventListener('click', function (e) {
    var a = refLink(e);
    if (a && touch && cur !== a) { e.preventDefault(); show(a); return; }   // 1st tap: preview; 2nd tap: jump
    if (!a && tip && !tip.contains(e.target)) hide(0);
    if (a) hide(0);
  }, true);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') hide(0); });
  window.addEventListener('scroll', function () { if (cur && touch) hide(0); }, { passive: true });
})();
