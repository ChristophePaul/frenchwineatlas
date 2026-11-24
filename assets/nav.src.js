/* French Wine — site-wide menu + FR/EN switch.
   Loaded on every page by theme.js. nav.js is GENERATED from this file by nav_build.py (which fills SITE).

   Where it mounts:
   · Leaflet maps  → a toolbar [☰ Menu | EN | ◐] in the map's top-right corner, beside the zoom control
                     (the zoom is moved there if the page had it top-left).
   · SVG maps (#ctrl, Carte de France / IGP) → the same toolbar beside #ctrl.
   · Pages with a top bar (.topbar) → a « Menu » pill next to the theme / language buttons.
   · Everything else → a small fixed dock top-right (bottom-right on phones).

   Menu styles (visitor's choice, switch at the bottom of the menu, localStorage fw_menu_style, or a ?menu= link):
   dropdown (« Déroulant »), drawer (« Tiroir »), mega (« Colonnes », default; ≥980px only, narrower → drawer).

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
  // the choice: localStorage fw_lang, or the fw_lang cookie kept by theme.js (survives a change of address)
  function stored() {
    var s = ''; try { s = localStorage.getItem('fw_lang') || ''; } catch (e) {}
    if (s !== 'en' && s !== 'fr') s = window.fwLangCookie ? window.fwLangCookie.get() : '';
    return s === 'en' || s === 'fr' ? s : '';
  }
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
    if (window.fwLangCookie) window.fwLangCookie.set(l);
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
    '  .fw-bar .fw-ml,.fw-bar .fw-sl,.fw-dock .fw-pill .fw-sl{display:none;}}',
    '.fw-bar>button .fw-sl{display:none;} @media (min-width:1100px){.fw-bar>button .fw-sl{display:inline;}}',
    '@media (max-width:640px){.fw-pill .fw-sl{display:none;} .fw-pill:has(.fw-sl){padding-left:11px!important;padding-right:11px!important;gap:0!important;}}',
    '/* side drawer (style B, 2026-11-16) */',
    '.fw-ov{position:fixed;inset:0;z-index:100001;background:rgba(30,8,14,.42);-webkit-backdrop-filter:blur(2px);backdrop-filter:blur(2px);animation:fwFade .2s ease-out;}',
    '.fw-ov[hidden]{display:none;}',
    '@keyframes fwFade{from{opacity:0}}',
    '@keyframes fwSlide{from{transform:translateX(48px);opacity:0}}',
    '@keyframes fwIn{from{transform:translateX(26px);opacity:0}}',
    '@keyframes fwOut{from{transform:translateX(-26px);opacity:0}}',
    '.fw-menu{position:fixed;top:0;right:0;bottom:0;z-index:100002;width:min(420px,calc(100vw - 32px));display:flex;flex-direction:column;background:#fbf6ea;color:#2e1419;box-shadow:-20px 0 50px rgba(30,8,14,.35);font:14px/1.35 ui-sans-serif,system-ui,-apple-system,\"Segoe UI\",Arial,sans-serif;text-align:left;animation:fwSlide .26s cubic-bezier(.2,.8,.2,1);}',
    '.fw-menu[hidden]{display:none;}',
    '.fw-menu *{box-sizing:border-box;}',
    '.fw-mh{position:relative;flex:none;padding:22px 60px 38px 22px;background:#6a1426 radial-gradient(130% 150% at 100% 0,rgba(201,162,75,.25),transparent 60%);color:#fbf1dc;}',
    '.fw-mh small{display:block;font:600 10.5px/1 ui-sans-serif,system-ui,-apple-system,\"Segoe UI\",Arial,sans-serif;letter-spacing:.18em;text-transform:uppercase;opacity:.75;margin-bottom:7px;}',
    '.fw-mh b{display:block;font:500 29px/1.05 \"Iowan Old Style\",\"Palatino Linotype\",Palatino,Georgia,serif;color:#fbf1dc;letter-spacing:0;}',
    '.fw-mh b em{color:#d9b36b;}',
    '.fw-x{all:unset;position:absolute;right:14px;top:14px;width:34px;height:34px;border-radius:50%;display:grid;place-items:center;cursor:pointer;color:#fbf1dc;background:rgba(255,255,255,.12);font-size:22px;line-height:1;}',
    '.fw-x:hover{background:rgba(255,255,255,.24);}',
    '.fw-x:focus-visible{outline:2px solid #d9b36b;outline-offset:2px;}',
    '.fw-qw{position:relative;flex:none;margin:-22px 16px 0;z-index:1;}',
    '.fw-qw svg{position:absolute;left:14px;top:50%;width:17px;height:17px;transform:translateY(-50%);color:#9a6a1f;pointer-events:none;}',
    '.fw-q{display:block;width:100%;margin:0;padding:12px 14px 12px 41px;border:1px solid rgba(154,106,31,.25);border-radius:11px;background:#fff;color:#2e1419;font:inherit;font-size:15px;outline:none;box-shadow:0 6px 18px rgba(60,15,25,.16);-webkit-appearance:none;appearance:none;}',
    '.fw-q:focus{border-color:#8e1f33;box-shadow:0 6px 18px rgba(60,15,25,.16),0 0 0 3px rgba(142,31,51,.14);}',
    '.fw-crumbs{flex:none;display:flex;align-items:center;flex-wrap:wrap;gap:2px 3px;padding:14px 18px 2px;font:600 11px/1.3 ui-sans-serif,system-ui,-apple-system,\"Segoe UI\",Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:#9a6a1f;}',
    '.fw-crumbs[hidden]{display:none;}',
    '.fw-crumbs button{all:unset;cursor:pointer;padding:3px 4px;border-radius:4px;}',
    '.fw-crumbs button:hover{background:rgba(154,106,31,.12);color:#6a1426;}',
    '.fw-crumbs button:focus-visible{outline:2px solid #9a6a1f;}',
    '.fw-crumbs .fw-back{display:inline-grid;place-items:center;width:28px;height:28px;padding:0;margin-right:6px;border-radius:50%;border:1px solid rgba(154,106,31,.4);}',
    '.fw-crumbs .fw-back svg{width:15px;height:15px;}',
    '.fw-crumbs i{font-style:normal;opacity:.45;}',
    '.fw-crumbs .fw-here{color:#6a1426;padding:3px 4px;}',
    '.fw-body{flex:1;min-height:0;overflow-y:auto;overscroll-behavior:contain;padding:8px 12px 14px;}',
    '.fw-go-in{animation:fwIn .22s ease-out;}',
    '.fw-go-out{animation:fwOut .22s ease-out;}',
    '.fw-row{all:unset;box-sizing:border-box;display:flex;align-items:center;gap:13px;width:100%;padding:10px 10px;border-bottom:1px solid rgba(154,106,31,.18);cursor:pointer;color:#2e1419;text-decoration:none;font-size:15px;line-height:1.25;}',
    '.fw-row:hover,.fw-row.fw-kb{background:rgba(154,106,31,.1);border-radius:10px;border-bottom-color:transparent;}',
    '.fw-row:focus-visible{outline:2px solid #9a6a1f;outline-offset:-2px;border-radius:10px;}',
    '.fw-ic{flex:none;width:36px;height:36px;border-radius:50%;display:grid;place-items:center;background:rgba(142,31,51,.08);color:#8e1f33;}',
    '.fw-ic svg{width:18px;height:18px;}',
    '.fw-sec{padding:13px 10px;}',
    '.fw-sec .fw-ic{width:42px;height:42px;border-radius:12px;}',
    '.fw-sec .fw-ic svg{width:22px;height:22px;}',
    '.fw-sec .fw-t>span{font:500 19px/1.15 \"Iowan Old Style\",\"Palatino Linotype\",Palatino,Georgia,serif;color:#6a1426;}',
    '.fw-t{flex:1;min-width:0;}',
    '.fw-t small{display:block;font-size:12px;opacity:.6;margin-top:2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}',
    '.fw-n{flex:none;font-size:11px;font-weight:600;color:#9a6a1f;background:rgba(201,162,75,.16);padding:2px 8px;border-radius:10px;}',
    '.fw-chev{flex:none;width:16px;height:16px;color:#9a6a1f;}',
    '.fw-row.fw-cur{background:rgba(142,31,51,.09);border-radius:10px;border-bottom-color:transparent;}',
    '.fw-row.fw-cur .fw-t>span{color:#8e1f33;font-weight:700;}',
    '.fw-row.fw-cur .fw-ic{background:#8e1f33;color:#fff;}',
    '.fw-dot{flex:none;width:8px;height:8px;border-radius:50%;background:#c9a24b;}',
    '.fw-row.fw-has-cur .fw-n{background:#8e1f33;color:#fff;}',
    '.fw-empty{padding:18px 10px;opacity:.6;font-size:14px;}',
    '.fw-foot{flex:none;display:flex;gap:8px;padding:12px 16px calc(12px + env(safe-area-inset-bottom,0px));border-top:1px solid rgba(154,106,31,.25);background:#f4ead6;}',
    '.fw-foot a{flex:1;min-width:0;display:flex;flex-direction:column;align-items:center;gap:4px;padding:8px 4px;border-radius:9px;border:1px solid rgba(154,106,31,.3);background:#fff;color:#6a1426;text-decoration:none;font-size:12px;font-weight:600;text-align:center;line-height:1.15;}',
    '.fw-foot a:hover{border-color:#8e1f33;}',
    '.fw-foot a.fw-cur{background:#8e1f33;color:#fff;border-color:#8e1f33;}',
    '.fw-foot svg{width:19px;height:19px;}',
    'html.fw-menu-open,html.fw-menu-open body{overflow:hidden!important;}',
    'html[data-theme="dark"] .fw-ov{background:rgba(0,0,0,.55);}',
    'html[data-theme="dark"] .fw-menu{background:#1f080e;color:#f1e7d3;box-shadow:-20px 0 50px rgba(0,0,0,.6);border-left:1px solid rgba(217,179,107,.22);}',
    'html[data-theme="dark"] .fw-mh{background-color:#3d0d19;}',
    'html[data-theme="dark"] .fw-q{background:#2b0d15;color:#f1e7d3;border-color:rgba(217,179,107,.3);box-shadow:0 6px 18px rgba(0,0,0,.45);}',
    'html[data-theme="dark"] .fw-q:focus{border-color:#c9a24b;box-shadow:0 6px 18px rgba(0,0,0,.45),0 0 0 3px rgba(201,162,75,.15);}',
    'html[data-theme="dark"] .fw-qw svg,html[data-theme="dark"] .fw-crumbs,html[data-theme="dark"] .fw-chev,html[data-theme="dark"] .fw-n{color:#c9a24b;}',
    'html[data-theme="dark"] .fw-crumbs .fw-here,html[data-theme="dark"] .fw-crumbs button:hover{color:#e7cf9c;}',
    'html[data-theme="dark"] .fw-crumbs .fw-back{border-color:rgba(217,179,107,.4);}',
    'html[data-theme="dark"] .fw-row{color:#f1e7d3;border-bottom-color:rgba(217,179,107,.14);}',
    'html[data-theme="dark"] .fw-row:hover,html[data-theme="dark"] .fw-row.fw-kb{background:rgba(217,179,107,.1);}',
    'html[data-theme="dark"] .fw-ic{background:rgba(217,179,107,.1);color:#e7cf9c;}',
    'html[data-theme="dark"] .fw-sec .fw-t>span{color:#e7cf9c;}',
    'html[data-theme="dark"] .fw-n{background:rgba(201,162,75,.14);}',
    'html[data-theme="dark"] .fw-row.fw-cur{background:rgba(201,162,75,.14);}',
    'html[data-theme="dark"] .fw-row.fw-cur .fw-t>span{color:#e7cf9c;}',
    'html[data-theme="dark"] .fw-row.fw-cur .fw-ic,html[data-theme="dark"] .fw-row.fw-has-cur .fw-n{background:#c9a24b;color:#1f080e;}',
    'html[data-theme="dark"] .fw-foot{background:#170509;border-top-color:rgba(217,179,107,.2);}',
    'html[data-theme="dark"] .fw-foot a{background:#2b0d15;color:#e7cf9c;border-color:rgba(217,179,107,.3);}',
    'html[data-theme="dark"] .fw-foot a:hover{border-color:#c9a24b;}',
    'html[data-theme="dark"] .fw-foot a.fw-cur{background:#c9a24b;color:#1f080e;border-color:#c9a24b;}',
    '@media (max-width:560px){.fw-mh{padding:18px 56px 34px 18px;} .fw-mh b{font-size:25px;} .fw-row{padding:11px 8px;}}',
    '/* mega-menu (style C, wide screens, 2026-11-16) */',
    '@keyframes fwDrop{from{transform:translateY(-14px);opacity:0}}',
    '.fw-menu.fw-mega{top:14px;left:14px;right:14px;bottom:auto;width:auto;max-height:calc(100vh - 28px);border-radius:14px;overflow:hidden;box-shadow:0 24px 70px -10px rgba(30,8,14,.55);animation:fwDrop .22s cubic-bezier(.2,.8,.2,1);}',
    '.fw-mega .fw-mh{padding:17px 70px 17px 24px;}',
    '.fw-mega .fw-mh small{display:none;}',
    '.fw-mega .fw-mh b{font-size:27px;}',
    '.fw-mega .fw-x{top:50%;margin-top:-17px;}',
    '.fw-mega .fw-qw{position:absolute;top:10px;right:64px;width:min(440px,42%);margin:0;}',
    '.fw-mega .fw-q{box-shadow:none;border-color:transparent;}',
    '.fw-mega .fw-crumbs{display:none;}',
    '.fw-mega .fw-body{padding:0;overflow:hidden;}',
    '.fw-cols{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));}',
    '.fw-col{max-height:calc(100vh - 28px - 64px - 62px - 46px);overflow-y:auto;overscroll-behavior:contain;padding:0 20px 20px;border-right:1px solid rgba(154,106,31,.22);}',
    '.fw-col:last-child{border-right:0;}',
    '.fw-col h4{position:sticky;top:0;z-index:1;display:flex;align-items:center;gap:9px;margin:0 -20px 6px;padding:18px 20px 10px;background:#fbf6ea;font:700 11.5px/1.2 ui-sans-serif,system-ui,-apple-system,\"Segoe UI\",Arial,sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#6a1426;}',
    '.fw-col h4 svg{width:21px;height:21px;color:#8e1f33;flex:none;}',
    '.fw-col h4 .fw-n{margin-left:auto;letter-spacing:0;}',
    '.fw-col h5{margin:14px 0 3px;font:600 15px/1.2 \"Iowan Old Style\",\"Palatino Linotype\",Palatino,Georgia,serif;color:#9a6a1f;}',
    '.fw-col h6{margin:8px 0 2px;font:600 10.5px/1.2 ui-sans-serif,system-ui,-apple-system,\"Segoe UI\",Arial,sans-serif;letter-spacing:.08em;text-transform:uppercase;opacity:.55;}',
    '.fw-lk{display:block;margin:0 -8px;padding:3px 8px;border-radius:6px;color:#2e1419;text-decoration:none;font-size:13.5px;line-height:1.3;}',
    '.fw-lk:hover{background:rgba(154,106,31,.12);color:#8e1f33;}',
    '.fw-lk.fw-cur{background:#8e1f33;color:#fff;font-weight:600;}',
    '.fw-col details{border-bottom:1px solid rgba(154,106,31,.16);}',
    '.fw-col summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:8px;padding:7px 0;font:600 14.5px/1.2 \"Iowan Old Style\",\"Palatino Linotype\",Palatino,Georgia,serif;color:#6a1426;user-select:none;}',
    '.fw-col summary::-webkit-details-marker{display:none;}',
    '.fw-col summary::before{content:"";width:6px;height:6px;border-right:1.6px solid #9a6a1f;border-bottom:1.6px solid #9a6a1f;transform:rotate(-45deg);transition:transform .15s;flex:none;}',
    '.fw-col details[open]>summary::before{transform:rotate(45deg);}',
    '.fw-col summary:hover{color:#8e1f33;}',
    '.fw-col summary .fw-n{margin-left:auto;font-family:ui-sans-serif,system-ui,-apple-system,\"Segoe UI\",Arial,sans-serif;}',
    '.fw-col details .fw-lk{margin-left:6px;}',
    '.fw-col details[open]{padding-bottom:8px;}',
    '.fw-mega .fw-body.fw-res{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:0 14px;align-content:start;padding:14px 18px;overflow-y:auto;max-height:calc(100vh - 28px - 64px - 62px - 46px);}',
    '.fw-mega .fw-foot{padding:10px 20px;}',
    '.fw-mega .fw-foot a{flex:none;flex-direction:row;gap:8px;padding:8px 14px;font-size:13px;}',
    'html[data-theme="dark"] .fw-col{border-right-color:rgba(217,179,107,.18);}',
    'html[data-theme="dark"] .fw-col h4{background:#1f080e;color:#e7cf9c;}',
    'html[data-theme="dark"] .fw-col h4 svg{color:#c9a24b;}',
    'html[data-theme="dark"] .fw-col h5{color:#c9a24b;}',
    'html[data-theme="dark"] .fw-lk{color:#f1e7d3;}',
    'html[data-theme="dark"] .fw-lk:hover{background:rgba(217,179,107,.12);color:#e7cf9c;}',
    'html[data-theme="dark"] .fw-lk.fw-cur{background:#c9a24b;color:#1f080e;}',
    'html[data-theme="dark"] .fw-col details{border-bottom-color:rgba(217,179,107,.14);}',
    'html[data-theme="dark"] .fw-col summary{color:#e7cf9c;}',
    '/* refined dropdown (style A, 2026-11-16) */',
    '@keyframes fwPop{from{opacity:0;transform:translateY(-6px) scale(.98)}}',
    '.fw-ov.fw-clear{background:transparent;-webkit-backdrop-filter:none;backdrop-filter:none;animation:none;}',
    '.fw-menu.fw-dd{top:auto;right:auto;bottom:auto;width:min(390px,calc(100vw - 16px));max-height:min(82vh,760px);border-radius:12px;overflow:hidden;box-shadow:0 22px 60px -12px rgba(60,15,25,.45),0 0 0 1px rgba(154,106,31,.3);animation:fwPop .18s ease-out;transform-origin:top right;}',
    '.fw-dd .fw-mh{order:0;padding:15px 52px 13px 18px;background:linear-gradient(180deg,#fff9ec,#fbf6ea);border-bottom:1px solid rgba(154,106,31,.22);}',
    '.fw-dd .fw-mh small{display:none;}',
    '.fw-dd .fw-mh b{font-size:23px;color:#6a1426;}',
    '.fw-dd .fw-mh b em{color:#9a6a1f;}',
    '.fw-dd .fw-x{top:50%;margin-top:-17px;right:10px;color:#6a1426;background:transparent;}',
    '.fw-dd .fw-x:hover{background:rgba(154,106,31,.14);}',
    '.fw-dd .fw-qw{order:1;margin:12px 14px 2px;}',
    '.fw-dd .fw-q{padding:9px 12px 9px 38px;font-size:14px;border-radius:9px;border-color:rgba(154,106,31,.38);box-shadow:none;}',
    '.fw-dd .fw-q:focus{box-shadow:0 0 0 3px rgba(142,31,51,.12);}',
    '.fw-dd .fw-crumbs{display:none;}',
    '.fw-dd .fw-foot{order:2;background:transparent;border-top:0;border-bottom:1px solid rgba(154,106,31,.22);padding:10px 14px 12px;gap:6px;}',
    '.fw-dd .fw-foot a{padding:8px 4px 7px;font-size:11.5px;}',
    '.fw-dd .fw-body{order:3;padding:6px 8px 12px;}',
    '.fw-dd details{margin:1px 0;}',
    '.fw-dd summary{list-style:none;cursor:pointer;display:flex;align-items:center;gap:10px;padding:7px 8px;border-radius:8px;user-select:none;}',
    '.fw-dd summary::-webkit-details-marker{display:none;}',
    '.fw-dd summary:hover{background:rgba(154,106,31,.1);}',
    '.fw-dd summary::after{content:"";width:6px;height:6px;margin:0 5px 2px;border-right:1.6px solid #9a6a1f;border-bottom:1.6px solid #9a6a1f;transform:rotate(45deg);transition:transform .15s;flex:none;}',
    '.fw-dd details:not([open])>summary::after{transform:rotate(-45deg);margin-bottom:0;}',
    '.fw-st{flex:1;min-width:0;}',
    '.fw-d1>summary{padding:8px;font-size:15px;font-weight:600;color:#6a1426;}',
    '.fw-d1>summary .fw-ic{width:32px;height:32px;border-radius:9px;}',
    '.fw-d1>summary .fw-ic svg{width:18px;height:18px;}',
    '.fw-d1>.fw-in{margin:2px 0 8px 24px;padding-left:10px;border-left:2px solid rgba(201,162,75,.42);}',
    '.fw-d2>summary,.fw-d3>summary{padding:6px 8px;font-size:14px;font-weight:600;color:#6a1426;}',
    '.fw-d2>.fw-in,.fw-d3>.fw-in{padding-left:12px;}',
    '.fw-dd .fw-lk{margin:0;padding:5px 10px;font-size:14px;}',
    '.fw-dd .fw-lk.fw-cur{box-shadow:0 2px 6px rgba(142,31,51,.3);}',
    '.fw-modes{order:9;flex:none;display:flex;align-items:center;gap:4px;padding:8px 14px;border-top:1px solid rgba(154,106,31,.2);background:#f4ead6;font:600 10.5px/1 ui-sans-serif,system-ui,-apple-system,\"Segoe UI\",Arial,sans-serif;color:#9a6a1f;}',
    '.fw-modes>span{margin-right:auto;letter-spacing:.1em;text-transform:uppercase;}',
    '.fw-modes button{all:unset;cursor:pointer;padding:6px 10px;border-radius:7px;border:1px solid rgba(154,106,31,.3);background:#fff;color:#6a1426;font:600 12px/1 ui-sans-serif,system-ui,-apple-system,\"Segoe UI\",Arial,sans-serif;}',
    '.fw-modes button:hover{border-color:#8e1f33;}',
    '.fw-modes button.on{background:#8e1f33;color:#fff;border-color:#8e1f33;}',
    '.fw-modes button[hidden]{display:none;}',
    '.fw-dd .fw-modes{background:transparent;}',
    'html[data-theme="dark"] .fw-dd .fw-mh{background:linear-gradient(180deg,#2c0b14,#1f080e);border-bottom-color:rgba(217,179,107,.2);}',
    'html[data-theme="dark"] .fw-dd .fw-mh b,html[data-theme="dark"] .fw-dd .fw-x{color:#e7cf9c;}',
    'html[data-theme="dark"] .fw-dd .fw-mh b em{color:#c9a24b;}',
    'html[data-theme="dark"] .fw-dd .fw-q{box-shadow:none;}',
    'html[data-theme="dark"] .fw-dd .fw-foot{background:transparent;border-bottom-color:rgba(217,179,107,.2);}',
    'html[data-theme="dark"] .fw-dd summary:hover{background:rgba(217,179,107,.1);}',
    'html[data-theme="dark"] .fw-d1>summary,html[data-theme="dark"] .fw-d2>summary,html[data-theme="dark"] .fw-d3>summary{color:#e7cf9c;}',
    'html[data-theme="dark"] .fw-d1>.fw-in{border-left-color:rgba(201,162,75,.3);}',
    'html[data-theme="dark"] .fw-modes{background:#170509;border-top-color:rgba(217,179,107,.2);color:#c9a24b;}',
    'html[data-theme="dark"] .fw-dd .fw-modes{background:transparent;}',
    'html[data-theme="dark"] .fw-modes button{background:#2b0d15;color:#e7cf9c;border-color:rgba(217,179,107,.3);}',
    'html[data-theme="dark"] .fw-modes button.on{background:#c9a24b;color:#1f080e;border-color:#c9a24b;}',
    '@media (prefers-reduced-motion:reduce){.fw-menu,.fw-ov,.fw-go-in,.fw-go-out,.fw-menu.fw-mega,.fw-menu.fw-dd{animation:none;}}',
    '@media print{.fw-mapbar .fw-bar,.fw-dock,.fw-menu,.fw-ov,.fw-pill{display:none!important;}}'
  ].join('\n');

  var IC_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>';
  var IC_SEARCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 20 20"/></svg>';
  var IC_GLOBE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.4 2.6 3.6 5.4 3.6 8.5s-1.2 5.9-3.6 8.5c-2.4-2.6-3.6-5.4-3.6-8.5s1.2-5.9 3.6-8.5Z"/></svg>';

  /* ---------------- menu drawer ---------------- */
  // A full-height drawer from the right over a dimmed page. The tree is walked one level at a time
  // (breadcrumb + back button); it opens on the level that holds the current page.
  var panel, ov, body, q, crumbs, foot, menuBtns = [], langBtn = null;
  var IC = {
    map: '<path d="M3 6.5 9 4l6 2.5L21 4v13.5L15 20l-6-2.5L3 20z"/><path d="M9 4v13.5M15 6.5V20"/>',
    grape: '<circle cx="9" cy="10" r="2.3"/><circle cx="14" cy="10" r="2.3"/><circle cx="11.5" cy="14.2" r="2.3"/><circle cx="16.5" cy="14.2" r="2.3"/><circle cx="14" cy="18.4" r="2.3"/><path d="M11.5 7.6c0-2 1.4-3.4 3.6-3.6"/>',
    grid: '<rect x="4" y="4" width="16" height="16" rx="1.5"/><path d="M4 10h16M10 4v16M14 10v10M10 15h10"/>',
    book: '<path d="M12 6.5C10 5 7 4.5 4 5v13c3-.5 6 0 8 1.5 2-1.5 5-2 8-1.5V5c-3-.5-6 0-8 1.5zM12 6.5v13"/>',
    home: '<path d="M4 11 12 4l8 7v9h-5v-6H9v6H4z"/>',
    france: '<path d="M10 3.5 13 5l3-.5 1.5 3 3 1.5-1 3.5 1 4-3.5 3-4 .5L9 21l-3.5-2 .5-3.5L3 13l1.5-3.5L4 6l3.5-.5z"/>',
    pin: '<path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0 1 13 0c0 5-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
    search: '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 20 20"/>',
    cols: '<rect x="3.5" y="5" width="17" height="14" rx="1.5"/><path d="M9.2 5v14M14.8 5v14"/>',
    drawer: '<rect x="3.5" y="5" width="17" height="14" rx="1.5"/><path d="M13 5v14"/>',
    chev: '<path d="m9 6 6 6-6 6"/>',
    back: '<path d="m15 6-6 6 6 6"/>'
  };
  function svg(k, cls) { return '<svg' + (cls ? ' class="' + cls + '"' : '') + ' viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + IC[k] + '</svg>'; }
  var SEC_IC = ['map', 'grape', 'grid', 'book'], TOP_IC = ['home', 'france', 'pin'];
  function href(p) { return BASE + encodeURI(p).replace(/#/g, '%23'); }
  function lbl(it) { return lang() === 'en' && it[2] ? it[2] : it[1]; }
  function gl(g) { return lang() === 'en' ? g.en : g.fr; }
  function isCur(p) { return here === p; }
  function hasCur(g) {
    return (g.items || []).some(function (it) { return isCur(it[0]); }) || (g.groups || []).some(hasCur);
  }
  function count(g) { return (g.items || []).length + (g.groups || []).reduce(function (n, s) { return n + count(s); }, 0); }
  function el(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html) e.innerHTML = html; return e; }
  function txt(tag, cls, t) { var e = el(tag, cls); e.textContent = t; return e; }

  var path = [];                     // the groups walked into, from the top
  function curPath() {
    var out = null;
    (function walk(gs, p) {
      gs.forEach(function (g) {
        if (out) return;
        var np = p.concat([g]);
        if ((g.items || []).some(function (it) { return isCur(it[0]); })) out = np; else walk(g.groups || [], np);
      });
    })(SITE.groups, []);
    return out || [];
  }
  function secIcon(top) { return SEC_IC[SITE.groups.indexOf(top)] || 'map'; }

  function itemRow(it, ic, sub) {
    var a = el('a', 'fw-row');
    a.href = href(it[0]);
    a.appendChild(el('span', 'fw-ic', svg(ic)));
    var t = el('span', 'fw-t'); t.appendChild(txt('span', '', lbl(it)));
    if (sub) t.appendChild(txt('small', '', sub));
    a.appendChild(t);
    if (isCur(it[0])) { a.classList.add('fw-cur'); a.setAttribute('aria-current', 'page'); a.appendChild(el('span', 'fw-dot')); }
    return a;
  }
  function groupRow(g, ic, sec) {
    var b = el('button', 'fw-row fw-grp' + (sec ? ' fw-sec' : '') + (hasCur(g) ? ' fw-has-cur' : ''));
    b.type = 'button';
    b.appendChild(el('span', 'fw-ic', svg(ic)));
    var t = el('span', 'fw-t'); t.appendChild(txt('span', '', gl(g)));
    var kids = (g.groups || []).map(gl).concat((g.items || []).map(lbl));
    t.appendChild(txt('small', '', kids.slice(0, 4).join(', ') + (kids.length > 4 ? '…' : '')));
    b.appendChild(t);
    b.appendChild(txt('span', 'fw-n', count(g)));
    b.insertAdjacentHTML('beforeend', svg('chev', 'fw-chev'));
    b.addEventListener('click', function () { path = path.concat([g]); render('in'); });
    return b;
  }
  // Wide screens show every section side by side (mega-menu); phones and narrow windows keep the drawer.
  // A footer button switches between the two (remembered in localStorage fw_menu_style).
  var MEGA_MIN = 980;
  (function () {                     // test links: ?menu=dropdown|drawer|mega picks the style
    var m = /[?&]menu=(dropdown|drawer|mega)\b/.exec(location.search);
    if (m) try { localStorage.setItem('fw_menu_style', m[1]); } catch (e) {}
  })();
  function menuStyle() { var s = ''; try { s = localStorage.getItem('fw_menu_style') || ''; } catch (e) {} return s === 'drawer' || s === 'dropdown' ? s : 'mega'; }
  function style() { var s = menuStyle(); return s === 'mega' && window.innerWidth < MEGA_MIN ? 'drawer' : s; }
  function isMega() { return style() === 'mega'; }
  function isDD() { return style() === 'dropdown'; }
  function ddGroup(g, lvl, ic) {
    var d = el('details', 'fw-d' + lvl), s = el('summary');
    if (hasCur(g)) d.open = true;
    if (ic) s.appendChild(el('span', 'fw-ic', svg(ic)));
    s.appendChild(txt('span', 'fw-st', gl(g))); s.appendChild(txt('span', 'fw-n', count(g)));
    d.appendChild(s);
    var inn = el('div', 'fw-in');
    (g.items || []).forEach(function (it) { inn.appendChild(megaLink(it)); });
    (g.groups || []).forEach(function (sg) { inn.appendChild(ddGroup(sg, lvl + 1)); });
    d.appendChild(inn);
    return d;
  }
  function renderDropdown() {
    crumbs.hidden = true;
    SITE.groups.forEach(function (g, i) { body.appendChild(ddGroup(g, 1, SEC_IC[i] || 'map')); });
  }
  function place() {                 // the dropdown hangs under the Menu button (or above it, phone dock)
    var st = panel.style;
    if (!isDD()) { st.left = st.right = st.top = st.bottom = st.width = ''; return; }
    var r = (opener.closest('.fw-bar, .fw-dock') || opener).getBoundingClientRect(), W = window.innerWidth, H = window.innerHeight;
    if (W <= 560) { st.left = '8px'; st.right = '8px'; st.width = 'auto'; }
    else { st.width = ''; st.right = 'auto'; st.left = Math.min(Math.max(8, r.right - panel.offsetWidth), W - panel.offsetWidth - 8) + 'px'; }
    if (r.bottom + 260 > H) { st.top = 'auto'; st.bottom = (H - r.top + 6) + 'px'; }
    else { st.top = (r.bottom + 6) + 'px'; st.bottom = 'auto'; }
  }
  function megaLink(it) {
    var a = txt('a', 'fw-lk', lbl(it)); a.href = href(it[0]);
    if (isCur(it[0])) { a.classList.add('fw-cur'); a.setAttribute('aria-current', 'page'); }
    return a;
  }
  function megaItems(g, into) {
    (g.items || []).forEach(function (it) { into.appendChild(megaLink(it)); });
    (g.groups || []).forEach(function (sg) { into.appendChild(txt('h6', '', gl(sg))); megaItems(sg, into); });
  }
  function renderMega() {
    crumbs.hidden = true;
    var cols = el('div', 'fw-cols');
    SITE.groups.forEach(function (g, i) {
      var col = el('div', 'fw-col'), h = el('h4', '', svg(SEC_IC[i] || 'map'));
      h.appendChild(txt('span', '', gl(g))); h.appendChild(txt('span', 'fw-n', count(g)));
      col.appendChild(h);
      var big = count(g) > 60;              // the cadastral plans: one folding block per sub-region
      (g.items || []).forEach(function (it) { col.appendChild(megaLink(it)); });
      (g.groups || []).forEach(function (sg) {
        if (big) {
          var d = el('details'), s = el('summary');
          if (hasCur(sg)) d.open = true;
          s.appendChild(txt('span', '', gl(sg))); s.appendChild(txt('span', 'fw-n', count(sg)));
          d.appendChild(s); megaItems(sg, d); col.appendChild(d);
        } else { col.appendChild(txt('h5', '', gl(sg))); megaItems(sg, col); }
      });
      cols.appendChild(col);
    });
    body.appendChild(cols);
  }
  function go(n) { if (n === path.length) return; path = path.slice(0, n); render('out'); }
  function renderCrumbs() {
    crumbs.innerHTML = '';
    crumbs.hidden = !path.length || !!q.value.trim() || isMega() || isDD();
    if (crumbs.hidden) return;
    var back = el('button', 'fw-back', svg('back'));
    back.type = 'button'; back.setAttribute('aria-label', T('Retour', 'Back'));
    back.addEventListener('click', function () { go(path.length - 1); });
    crumbs.appendChild(back);
    var top = txt('button', '', 'Menu'); top.type = 'button';
    top.addEventListener('click', function () { go(0); });
    crumbs.appendChild(top);
    path.forEach(function (g, i) {
      crumbs.appendChild(txt('i', '', '/'));
      if (i === path.length - 1) { crumbs.appendChild(txt('span', 'fw-here', gl(g))); return; }
      var b = txt('button', '', gl(g)); b.type = 'button';
      b.addEventListener('click', function () { go(i + 1); });
      crumbs.appendChild(b);
    });
  }
  function render(dir) {
    var mega = isMega(), dd = isDD();
    panel.classList.toggle('fw-mega', mega);
    panel.classList.toggle('fw-dd', dd);
    ov.classList.toggle('fw-clear', dd);
    body.classList.remove('fw-res');
    body.innerHTML = '';
    if (mega) return renderMega();
    if (dd) return renderDropdown();
    renderCrumbs();
    var list = el('div', dir ? 'fw-go-' + dir : '');
    if (!path.length) {
      SITE.groups.forEach(function (g, i) { list.appendChild(groupRow(g, SEC_IC[i] || 'map', true)); });
    } else {
      var g = path[path.length - 1], ic = secIcon(path[0]);
      (g.groups || []).forEach(function (sg) { list.appendChild(groupRow(sg, ic)); });
      (g.items || []).forEach(function (it) { list.appendChild(itemRow(it, ic)); });
    }
    body.appendChild(list);
    body.scrollTop = 0;
    if (dir) { var f = list.querySelector('.fw-row'); if (f && window.matchMedia('(pointer:fine)').matches && document.activeElement !== q) f.focus({ preventScroll: true }); }
  }
  function renderFoot() {
    foot.innerHTML = '';
    SITE.top.forEach(function (it, i) {
      var a = el('a', isCur(it[0]) ? 'fw-cur' : '', svg(TOP_IC[i] || 'map'));
      a.href = href(it[0]); a.appendChild(txt('span', '', lbl(it)));
      foot.appendChild(a);
    });
    renderModes();
  }
  function renderModes() {           // visitor's choice of menu style: Déroulant / Tiroir / Colonnes (remembered in fw_menu_style)
    var m = panel.querySelector('.fw-modes');
    m.innerHTML = ''; m.appendChild(txt('span', '', T('Affichage', 'Layout')));
    [['dropdown', T('Déroulant', 'Dropdown')], ['drawer', T('Tiroir', 'Drawer')], ['mega', T('Colonnes', 'Columns')]].forEach(function (o) {
      var b = txt('button', style() === o[0] ? 'on' : '', o[1]);
      b.type = 'button';
      if (o[0] === 'mega' && window.innerWidth < MEGA_MIN) b.hidden = true;
      b.addEventListener('click', function () {
        try { localStorage.setItem('fw_menu_style', o[0]); } catch (e) {}
        q.value = ''; path = curPath(); render(); renderFoot(); place(); scrollCur();
      });
      m.appendChild(b);
    });
  }
  function head() {
    panel.querySelector('.fw-mh small').textContent = 'Menu';
    panel.querySelector('.fw-mh b').innerHTML = T('Vins <em>de France</em>', 'Wines <em>of France</em>');
    panel.querySelector('.fw-x').setAttribute('aria-label', T('Fermer', 'Close'));
    q.placeholder = T('Aller à… (région, appellation, cru)', 'Go to… (region, appellation, cru)');
    renderFoot();
  }
  function fold(s) { return s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); }
  function flat() {
    var out = [];
    SITE.top.forEach(function (it, i) { out.push([it, '', TOP_IC[i] || 'map']); });
    (function walk(gs, p, ic) {
      gs.forEach(function (g, i) {
        var np = p.concat(gl(g)), gic = ic || SEC_IC[i] || 'map';
        (g.items || []).forEach(function (it) { out.push([it, np.join(' › '), gic]); });
        walk(g.groups || [], np, gic);
      });
    })(SITE.groups, [], null);
    return out;
  }
  var kb = -1;
  function search() {
    var v = fold(q.value.trim());
    if (!v) { kb = -1; render(); return; }
    renderCrumbs();
    var words = v.split(/\s+/);
    var hits = flat().filter(function (h) {
      var hay = fold(h[0][1] + ' ' + (h[0][2] || '') + ' ' + h[1]);
      return words.every(function (w) { return hay.indexOf(w) >= 0; });
    });
    body.innerHTML = ''; body.classList.add('fw-res');
    if (!hits.length) body.appendChild(txt('div', 'fw-empty', T('Aucune page trouvée.', 'No page found.')));
    hits.slice(0, 80).forEach(function (h) { body.appendChild(itemRow(h[0], h[2], h[1])); });
    body.scrollTop = 0;
    kb = hits.length ? 0 : -1; mark();
  }
  function mark() {
    var as = body.querySelectorAll('a');
    for (var i = 0; i < as.length; i++) as[i].classList.toggle('fw-kb', i === kb);
    if (as[kb]) as[kb].scrollIntoView({ block: 'nearest' });
  }
  function buildPanel() {
    ov = el('div', 'fw-ov'); ov.hidden = true;
    panel = el('div', 'fw-menu'); panel.hidden = true;
    panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-modal', 'true');
    panel.innerHTML = '<div class="fw-mh"><small></small><b></b><button class="fw-x" type="button">×</button></div>' +
      '<div class="fw-qw">' + svg('search') +
      '<input class="fw-q" type="search" autocomplete="off" spellcheck="false"></div>' +
      '<div class="fw-crumbs"></div><div class="fw-body"></div><div class="fw-foot"></div><div class="fw-modes"></div>';
    body = panel.querySelector('.fw-body'); q = panel.querySelector('.fw-q');
    crumbs = panel.querySelector('.fw-crumbs'); foot = panel.querySelector('.fw-foot');
    panel.setAttribute('aria-label', 'Menu');
    panel.querySelector('.fw-x').addEventListener('click', function () { close(); if (opener) opener.focus(); });
    q.addEventListener('input', search);
    q.addEventListener('keydown', function (e) {
      var as = body.querySelectorAll('a');
      if (e.key === 'ArrowDown' && q.value && as.length) { kb = Math.min(as.length - 1, kb + 1); mark(); e.preventDefault(); }
      else if (e.key === 'ArrowUp' && q.value && as.length) { kb = Math.max(0, kb - 1); mark(); e.preventDefault(); }
      else if (e.key === 'Enter' && q.value && as[kb < 0 ? 0 : kb]) { location.href = as[kb < 0 ? 0 : kb].href; }
      else if (e.key === 'Backspace' && !q.value && path.length) { go(path.length - 1); e.preventDefault(); }
    });
    [panel, ov].forEach(function (n) {
      ['mousedown', 'wheel', 'touchstart', 'dblclick', 'keydown'].forEach(function (ev) {
        n.addEventListener(ev, function (e) {
          if (e.key === 'Escape') { close(); if (opener) opener.focus(); }
          e.stopPropagation();          // keep the map (and page shortcuts) out of it
        });
      });
    });
    ov.addEventListener('click', close);
    document.body.appendChild(ov);
    document.body.appendChild(panel);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) { close(); } });
    var wasMega = null;
    window.addEventListener('resize', function () {
      if (panel.hidden) return;
      if (style() !== wasMega) { wasMega = style(); if (q.value) search(); else render(); renderFoot(); }
      place();
    });
  }
  var opener = null;
  function open(btn) {
    if (!panel) buildPanel();
    opener = btn;
    q.value = ''; kb = -1;
    head();
    path = curPath();
    render();
    ov.hidden = false; panel.hidden = false; place();
    root.classList.add('fw-menu-open');
    menuBtns.forEach(function (b) { b.setAttribute('aria-expanded', 'true'); });
    if (window.matchMedia('(pointer:fine)').matches) q.focus({ preventScroll: true });
    scrollCur();
  }
  function scrollCur() {
    requestAnimationFrame(function () {          // bring the current page into view (after layout)
      var cur = body.querySelector('.fw-cur'); if (!cur) return;
      var box = cur.closest('.fw-col') || body;
      var r = cur.getBoundingClientRect(), br = box.getBoundingClientRect();
      if (r.bottom > br.bottom - 8) box.scrollTop += r.top - br.top - (br.height - r.height) / 2;
    });
  }
  function close() {
    if (!panel || panel.hidden) return;
    panel.hidden = true; ov.hidden = true;
    root.classList.remove('fw-menu-open');
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
  /* ---------------- site search (assets/search.js, loaded on first use) ---------------- */
  // No search button on the cadastral plans, the games, or where the page asks not to have one.
  var NO_SEARCH = /^(Plan Cadastraux\/|Infos\/Literature\/(Jeux|Wine_Quiz|Taste_Quiz|Map_Game|Bon_Cep|IGP_Game|Color_Game)\.html$)/;
  var SEARCH_V = /*@SV@*/'';         // search.js version, stamped by search_build.py / nav_build.py
  var searchBtn = null, searchJs = null;
  function hasSearch() { return !NO_SEARCH.test(here) && !document.querySelector('meta[name="fw-no-search"]'); }
  function loadSearch() {
    if (window.fwSearch) return Promise.resolve(window.fwSearch);
    if (searchJs) return searchJs;
    searchJs = new Promise(function (ok, ko) {
      var s = document.createElement('script');
      s.src = BASE + 'assets/search.js?v=' + SEARCH_V;
      s.onload = function () { ok(window.fwSearch); }; s.onerror = function () { searchJs = null; ko(); };
      document.head.appendChild(s);
    });
    return searchJs;
  }
  function openSearch(btn) {
    close();
    // keys typed while search.js is still loading are passed on to the search field
    var early = '', grab = function (e) { if (e.key.length === 1 && !e.metaKey && !e.ctrlKey) { early += e.key; e.preventDefault(); } };
    if (!window.fwSearch) document.addEventListener('keydown', grab, true);
    loadSearch().then(function (fs) {
      document.removeEventListener('keydown', grab, true);
      fs.toggle(btn || searchBtn);
      if (early) fs.type(early);
    });
  }
  function searchButton(cls) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = cls;
    b.setAttribute('aria-haspopup', 'dialog'); b.setAttribute('aria-expanded', 'false');
    b.innerHTML = IC_SEARCH + '<span class="fw-sl"></span>';
    b.addEventListener('click', function (e) { e.preventDefault(); e.stopPropagation(); openSearch(b); });
    b.addEventListener('mousedown', function (e) { e.stopPropagation(); });
    searchBtn = b;
    return b;
  }
  function searchKeys() {
    document.addEventListener('keydown', function (e) {
      var t = e.target, typing = t && (t.isContentEditable || /^(INPUT|TEXTAREA|SELECT)$/.test(t.nodeName));
      if ((e.key === 'k' || e.key === 'K') && (e.metaKey || e.ctrlKey) && !e.altKey) { e.preventDefault(); openSearch(); }
      else if (e.key === '/' && !typing && !e.metaKey && !e.ctrlKey && !e.altKey) { e.preventDefault(); openSearch(); }
    });
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
    if (panel) head();
    menuBtns.forEach(function (b) {
      b.querySelector('.fw-ml').textContent = 'Menu';
      b.title = T('Toutes les pages du site', 'All pages of the site');
    });
    if (searchBtn) {
      searchBtn.querySelector('.fw-sl').textContent = T('Rechercher', 'Search');
      searchBtn.title = T('Rechercher dans tout le site  ( / )', 'Search the whole site  ( / )');
      searchBtn.setAttribute('aria-label', T('Rechercher', 'Search'));
    }
    if (langBtn) {
      langBtn.querySelector('.fw-ll').textContent = lang() === 'en' ? 'FR' : 'EN';
      langBtn.title = T('English version', 'Version française');
    }
    var th = document.querySelector('.fw-bar .fw-theme-btn, .fw-dock .fw-theme-btn');
    if (th) { var l = th.querySelector('.fw-tl'); th.title = l ? l.textContent : ''; }
    if (panel && !panel.hidden) { if (q.value) search(); else render(); }
  }

  /* ---------------- mounting ---------------- */
  function themeBtn() { return document.querySelector('.fw-theme-btn'); }

  function mapBar(zoomEl) {
    var bar = document.createElement('div'); bar.className = 'fw-bar';
    bar.appendChild(menuButton(''));
    if (hasSearch()) bar.appendChild(searchButton(''));
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
      if (hasSearch()) anchor.parentNode.insertBefore(searchButton(pill.className), anchor);
      anchor.parentNode.classList.add('fw-grp-inline');
      return;
    }
    var dock = document.createElement('div'); dock.className = 'fw-dock';
    dock.appendChild(pill);
    if (hasSearch()) dock.appendChild(searchButton('fw-theme-btn fw-pill'));
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
  function start() {
    if (started) return; started = true; mount(); adoptLateThemeButtons(); firstVisitLang();
    if (hasSearch()) searchKeys();
    // arriving from a search result: #aoc= / #igp= on a map, or words to highlight, or the results page itself
    var hl = ''; try { hl = sessionStorage.getItem('fw_hl') || ''; } catch (e) {}
    if (hl || /^#(aoc|igp)=/.test(location.hash) || document.getElementById('fw-results')) loadSearch();
  }
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
  // Shown automatically only on the home page, and only until a language has been chosen (fw_lang in
  // localStorage or its cookie, see theme.js). The choice is saved like the EN/FR button, so every page
  // then opens in that language, on later visits too.
  // A link to #lang (e.g. the home page footer « Changer de langue ») reopens it at any time.
  function firstVisitLang() {
    window.addEventListener('hashchange', function () { if (location.hash === '#lang') langChooser(true); });
    if (location.hash === '#lang') return langChooser(true);
    if (!/^(index\.html)?$/.test(here)) return;
    if (stored()) return;
    langChooser(false);
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

  window.fwNav = { search: openSearch, setLang: setLang, lang: lang, chooseLang: function () { langChooser(true); }, open: function () { if (menuBtns[0]) open(menuBtns[0]); } };
})();
