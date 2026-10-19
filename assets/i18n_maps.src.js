/* FR → EN translation layer for the region map pages.
   GENERATED into assets/i18n_maps.js by assets/i18n_build.py (dictionary + this engine) — edit this file, then rebuild.

   The pages are written in French. When html[lang] becomes "en" (set by the site menu's EN/FR button,
   see nav.js), every text node / title / placeholder whose whitespace-normalised text is in the dictionary
   is swapped for its English version, and nodes the page scripts add later (popups, lists, map labels) are
   translated as they appear. Switching back to French restores the originals. */
(function () {
  var DICT = __DICT__, RIV = __RIV__;
  var root = document.documentElement;
  var ATTRS = ['title', 'placeholder', 'aria-label'];
  var origText = new WeakMap(), setText = new WeakMap(), origAttr = new WeakMap();
  var touched = new Set();          // text nodes we changed (strong refs are fine: pages are single-view)
  var touchedEl = new Set();
  var busy = false;

  var MONTHS = { janvier: 'January', 'février': 'February', mars: 'March', avril: 'April', mai: 'May', juin: 'June', juillet: 'July',
    'août': 'August', septembre: 'September', octobre: 'October', novembre: 'November', 'décembre': 'December' };
  var TECH = __TECH__.map(function (r) { return [new RegExp(r[0], 'g'), r[1]]; });
  function tech(s) { for (var i = 0; i < TECH.length; i++) s = s.replace(TECH[i][0], TECH[i][1]); return s; }

  function isEN() { return /^en/i.test(root.lang || ''); }
  function norm(s) { return s.replace(/\s+/g, ' ').trim(); }

  // translate one whitespace-normalised string; returns null when nothing applies
  function tr(s) {
    if (!s) return null;
    if (DICT.hasOwnProperty(s)) return DICT[s];
    if (RIV.hasOwnProperty(s)) return RIV[s];
    var m;
    // « la Loire · le Cher · l'Allier » legends, or any " · " list whose parts all translate
    if (s.indexOf(' · ') > 0) {
      var parts = s.split(' · '), any = false, out = [];
      for (var i = 0; i < parts.length; i++) {
        var p = parts[i], t = DICT[p] || RIV[p] || null;
        if (!t) { var r = /^(le |la |les |l'|l’)(.+)$/i.exec(p); if (r && RIV[p.charAt(0).toUpperCase() + p.slice(1)]) t = r[2]; }
        if (t) any = true;
        out.push(t || p);
      }
      if (any) return out.join(' · ');
    }
    if ((m = /^Cépages — (.+)$/.exec(s))) return 'Grapes — ' + (DICT[m[1]] || m[1]);
    // hint bar: « commune : Pauillac — choisissez une appellation »
    if ((m = /^(commune|appellation|région) : (.+?)(?: (— .+))?$/.exec(s)))
      return { commune: 'commune', appellation: 'appellation', 'région': 'region' }[m[1]] + ': ' + m[2] + (m[3] ? ' ' + (DICT[m[3]] || m[3]) : '');
    if ((m = /^([\d\s  ]+) communes · aire géographique$/.exec(s))) return m[1] + ' communes · geographical area';
    if ((m = /^Reconnue en (\d{4})$/.exec(s))) return 'Recognised in ' + m[1];
    if ((m = /^Aire — (\d+) communes? ?:$/.exec(s))) return 'Area — ' + m[1] + ' commune' + (m[1] > 1 ? 's' : '') + ':';
    if ((m = /^(?:Reconnue par décret|[Dd]écret) du (\d+)(?:er)? (\S+) (\d{4})(.*)$/.exec(s)) && MONTHS[m[2]])
      return (/^R/.test(s) ? 'Recognised by decree of ' : 'Decree of ') + m[1] + ' ' + MONTHS[m[2]] + ' ' + m[3] + (m[4] ? tech(m[4]) : '');
    // yields, alcohol, sugar, decrees… assembled by the page scripts: technical phrase table
    if (/hl\/ha|%|g\/l|décret|Rendement|TAV|TAN|[Rr]ichesse|butoir|reconnue/.test(s)) { var t2 = tech(s); if (t2 !== s) return t2; }
    if ((m = /^Les (\d+) (.+)$/.exec(s)) && /^(Grands Crus|appellations|communes|crus)$/i.test(m[2])) return 'The ' + m[1] + ' ' + m[2];
    if ((m = /^(.+) \((\d+) crus?\)$/.exec(s)) && DICT[m[1]]) return DICT[m[1]] + ' (' + m[2] + ' crus)';
    if ((m = /^(.*\S)\s?:$/.exec(s)) && DICT[m[1]]) return DICT[m[1]] + ':';
    return null;
  }

  function doText(n) {
    var v = n.nodeValue;
    if (setText.get(n) === v) return;                 // already ours
    if (!/[A-Za-zÀ-ÿ]/.test(v)) return;
    var t = tr(norm(v));
    if (t == null) { if (origText.has(n) && setText.get(n) !== v) { origText.delete(n); touched.delete(n); } return; }
    origText.set(n, v);
    var lead = /^\s*/.exec(v)[0], trail = /\s*$/.exec(v)[0];
    var out = lead + t + trail;
    setText.set(n, out); n.nodeValue = out; touched.add(n);
  }
  function doAttrs(el) {
    for (var i = 0; i < ATTRS.length; i++) {
      var a = ATTRS[i], v = el.getAttribute(a); if (!v) continue;
      var o = origAttr.get(el) || {};
      if (o['_set_' + a] === v) continue;
      var t = tr(norm(v)); if (t == null) continue;
      o[a] = v; o['_set_' + a] = t; origAttr.set(el, o); el.setAttribute(a, t); touchedEl.add(el);
    }
  }
  function skip(el) {
    return el && el.closest && el.closest('script,style,noscript,.fw-menu,.fw-bar,.fw-dock,.fw-theme-btn,[data-no-i18n]');
  }
  function walk(rootNode) {
    if (rootNode.nodeType === 3) { if (!skip(rootNode.parentElement)) doText(rootNode); return; }
    if (rootNode.nodeType !== 1 || skip(rootNode)) return;
    doAttrs(rootNode);
    var w = document.createTreeWalker(rootNode, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT, {
      acceptNode: function (n) {
        if (n.nodeType === 1) return skip(n) ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT;
        return NodeFilter.FILTER_ACCEPT;
      } });
    var n; while ((n = w.nextNode())) { if (n.nodeType === 3) doText(n); else doAttrs(n); }
  }
  function toEN() { busy = true; walk(document.body); busy = false; }
  function toFR() {
    busy = true;
    touched.forEach(function (n) { if (origText.has(n) && setText.get(n) === n.nodeValue) n.nodeValue = origText.get(n); });
    touched.clear(); origText = new WeakMap(); setText = new WeakMap();
    touchedEl.forEach(function (el) { var o = origAttr.get(el) || {};
      ATTRS.forEach(function (a) { if (o[a] != null && el.getAttribute(a) === o['_set_' + a]) el.setAttribute(a, o[a]); }); });
    touchedEl.clear(); origAttr = new WeakMap();
    busy = false;
  }

  var mo = new MutationObserver(function (list) {
    if (busy || !isEN()) return;
    busy = true;
    for (var i = 0; i < list.length; i++) {
      var r = list[i];
      if (r.type === 'childList') { for (var j = 0; j < r.addedNodes.length; j++) walk(r.addedNodes[j]); }
      else if (r.type === 'characterData') { if (!skip(r.target.parentElement)) doText(r.target); }
      else if (r.type === 'attributes' && r.target.nodeType === 1 && !skip(r.target)) doAttrs(r.target);
    }
    busy = false;
  });
  var last = null;
  function sync() { var l = isEN() ? 'en' : 'fr'; if (l === last) return; last = l; if (l === 'en') toEN(); else if (last !== null) toFR(); }
  function start() {
    mo.observe(document.body, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: ATTRS });
    new MutationObserver(sync).observe(root, { attributes: true, attributeFilter: ['lang'] });
    last = 'fr'; sync();
  }
  if (document.body) start(); else document.addEventListener('DOMContentLoaded', start);
})();
