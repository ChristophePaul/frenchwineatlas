/* French Wine — site-wide copyright notice « © 2026 Christophe A. Paul ».
   Loaded by assets/theme.js on every page (no page needs editing; rebuilt pages keep it).
   - Leaflet maps with a credits line: appended to it (same line).
   - Other full-screen Leaflet maps: a small control in the map's bottom-right corner.
   - Scrolling pages: a centred line at the very end of the page.
   - Full-screen apps that do not scroll: a small fixed tag at the bottom-left. */
(function () {
  if (window.__fwCopy) return; window.__fwCopy = true;
  var HOLDER = 'Christophe A. Paul', YEAR = '2026';
  var root = document.documentElement;

  function lang() {
    var l = '';
    try { l = localStorage.getItem('fw_lang') || ''; } catch (e) {}
    return (root.lang || l || 'fr').slice(0, 2) === 'en' ? 'en' : 'fr';
  }

  var CSS =
    '.fw-copy{font:400 11px/1.4 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;letter-spacing:.04em;' +
    'color:rgba(245,239,227,.55);pointer-events:auto;}' +
    'html[data-theme="cream"] .fw-copy{color:rgba(46,20,25,.58);}' +
    '.fw-copy b{font-weight:600;}' +
    '.fw-copy-foot{display:block;clear:both;text-align:center;padding:18px 16px 22px;margin:0;}' +
    '.fw-copy-tag{position:fixed;right:8px;bottom:6px;z-index:9000;font-size:10px;padding:2px 8px;border-radius:999px;' +
    'background:rgba(24,5,11,.45);pointer-events:none;}' +
    'html[data-theme="cream"] .fw-copy-tag{background:rgba(255,253,248,.75);}' +
    '@media (max-width:560px){.fw-copy-tag{right:auto;left:8px;}}' +
    '.leaflet-control.fw-copy-map{margin:0 0 0 0!important;clear:both;float:right;padding:1px 7px;font-size:10px;' +
    'background:rgba(24,5,11,.55);color:rgba(245,239,227,.75);border-radius:4px 0 0 0;}' +
    'html[data-theme="cream"] .leaflet-control.fw-copy-map{background:rgba(255,253,248,.82);color:rgba(46,20,25,.7);}' +
    '.fw-copy-attr{font:inherit;letter-spacing:0;color:inherit!important;}' +
    '@media print{.fw-copy-tag,.fw-copy-map{position:static;}}';

  var el = null;
  function render() {
    if (el && el.classList.contains('fw-copy-attr')) { el.innerHTML = ' \u00B7 \u00A9\u00A0' + YEAR + ' <b>' + HOLDER + '</b>'; return; }
    if (el) el.innerHTML = '\u00A9\u00A0' + YEAR + ' <b>' + HOLDER + '</b> \u00B7 ' + (lang() === 'en' ? 'All rights reserved' : 'Tous droits r\u00E9serv\u00E9s');
  }

  function bigMap() {
    var maps = document.querySelectorAll('.leaflet-container'), best = null, area = 0;
    for (var i = 0; i < maps.length; i++) {
      var r = maps[i].getBoundingClientRect(), a = r.width * r.height;
      if (a > area) { area = a; best = maps[i]; }
    }
    // only when the map fills most of the window (a full-screen map page)
    return best && area > 0.45 * innerWidth * innerHeight ? best : null;
  }

  function mount() {
    if (document.querySelector('.fw-copy')) return;
    var st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);
    el = document.createElement('div');
    el.setAttribute('role', 'contentinfo');
    var map = bigMap(), corner = map && map.querySelector('.leaflet-bottom.leaflet-right');
    var attr = map && map.querySelector('.leaflet-control-attribution');
    if (attr) {
      // the map already has a credits line: join it on the same line (a second line would push the credits
      // up into the map's bottom hint card). Leaflet rewrites the credits when layers change → re-append.
      el = document.createElement('span');
      el.className = 'fw-copy fw-copy-attr';
      var put = function () { if (!attr.contains(el)) { attr.appendChild(el); render(); } };
      put();
      new MutationObserver(put).observe(attr, { childList: true });
    } else if (corner) {
      el.className = 'fw-copy leaflet-control fw-copy-map';
      corner.appendChild(el);                    // bottom corner: last child sits at the very bottom
    } else {
      // a page that fits the window (full-screen map or app) gets a small fixed tag, so it does not start scrolling;
      // a normal scrolling page gets a line at its very end
      var se = document.scrollingElement || root;
      var fits = se.scrollHeight <= innerHeight + 2;
      el.className = 'fw-copy ' + (fits ? 'fw-copy-tag' : 'fw-copy-foot');
      document.body.appendChild(el);
    }
    render();
    new MutationObserver(render).observe(root, { attributes: true, attributeFilter: ['lang'] });
    document.addEventListener('fw:lang', render);
  }
  // maps are built by page scripts: wait for the load event, then one frame
  function go() { setTimeout(mount, 60); }
  if (document.readyState === 'complete') go(); else window.addEventListener('load', go);
})();
