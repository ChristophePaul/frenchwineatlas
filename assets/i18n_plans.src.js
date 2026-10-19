/* FR → EN translation layer for the cadastral plan pages (Plan Cadastraux/, Bourgogne climats/).
   GENERATED into assets/i18n_plans.js by assets/i18n_plans_build.py (dictionary + this engine) — edit this file, then rebuild.

   Same principle as i18n_maps.js: when html[lang] becomes "en" (site menu EN/FR button, nav.js), text nodes and
   title / placeholder / aria-label attributes found in the dictionary are swapped for English, including nodes the
   page scripts add later; switching back to French restores the originals.
   In addition:
   - HTML: whole elements (AOC card rows, Burgundy intro paragraphs) are swapped by their textContent, because their
     sentences are split across <b>/<a> tags and cannot be translated piece by piece;
   - PAT: regex rules for text assembled by the page scripts (counts, legend lines, parcel popups);
   - French number formats (1 155,2) become English (1,155.2) in figures. */
(function () {
  var DICT = __DICT__, HTML = __HTML__, PAT = __PAT__, SUBS = __SUBS__, TECH = __TECH__;
  var root = document.documentElement;
  var ATTRS = ['title', 'placeholder', 'aria-label'];
  var HSEL = '.row, p.lede';
  var origText = new WeakMap(), setText = new WeakMap(), origAttr = new WeakMap();
  var touched = new Set(), touchedEl = new Set(), swapped = new Set();
  var busy = false;
  PAT = PAT.map(function (r) { return [new RegExp(r[0]), r[1]]; });
  TECH = TECH.map(function (r) { return [new RegExp(r[0], 'g'), r[1]]; });

  function isEN() { return /^en/i.test(root.lang || ''); }
  function norm(s) { return s.replace(/\s+/g, ' ').trim(); }
  // 1 155,2 → 1,155.2
  function num(s) {
    return s.replace(/(\d{1,3}(?:[  ]\d{3})+)/g, function (m) { return m.replace(/[  ]/g, ','); })
            .replace(/(\d),(\d{1,2})(?!\d)/g, '$1.$2');
  }
  function tr(s) {
    if (!s) return null;
    if (DICT.hasOwnProperty(s)) return DICT[s];
    var m, i;
    // bare figures: "2 676,6", "1 155,2 ha", "93 %"
    if (/^[\d  ,.]+(?: ?(?:ha|a|ca|%|km|m))?$/.test(s)) { var n = num(s); return n !== s ? n : null; }
    for (i = 0; i < PAT.length; i++) {
      var mm = PAT[i][0].exec(s);
      if (mm) {
        // captured parts are translated again when they are known strings (e.g. « Part de la commune dans l’aire » + aocShort)
        return num(PAT[i][1].replace(/\$(\d)/g, function (_, k) { var g = mm[+k] || ''; return DICT[g] || g; }));
      }
    }
    // « · » lists whose parts translate (legend lines, eyebrows)
    if (s.indexOf(' · ') > 0) {
      var parts = s.split(' · '), any = false, out = [];
      for (i = 0; i < parts.length; i++) { var p = parts[i], q = DICT[p] || null; if (q) any = true; out.push(q || p); }
      if (any) return out.join(' · ');
    }
    // hover line « · 36 a 95 ca · Le Taureau · hors appellation »
    if (/^· /.test(s) || / · /.test(s)) {
      var t2 = s; for (i = 0; i < SUBS.length; i++) t2 = t2.split(SUBS[i][0]).join(SUBS[i][1]);
      if (t2 !== s) return num(t2);
    }
    if (/hl\/ha|g\/l|TAV|butoir/.test(s)) { var t3 = s; for (i = 0; i < TECH.length; i++) t3 = t3.replace(TECH[i][0], TECH[i][1]); if (t3 !== s) return t3; }
    if ((m = /^(.*\S)\s?:$/.exec(s)) && DICT[m[1]]) return DICT[m[1]] + ':';
    return null;
  }

  function doText(n) {
    var v = n.nodeValue;
    if (setText.get(n) === v) return;
    if (!/[A-Za-zÀ-ÿ\d]/.test(v)) return;
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
  // whole-element swap (card rows, intro paragraphs); returns true when the element is now English
  function doHTML(el) {
    if (el._fwEN) return true;
    if (!el.matches || !el.matches(HSEL)) return false;
    var k = norm(el.textContent), h = HTML[k];
    if (h == null) return false;
    // keep live ids (e.g. <b id="l-pc">) — the English HTML carries the same markup
    el._fwFR = el.innerHTML; el.innerHTML = h; el._fwEN = true; swapped.add(el);
    return true;
  }
  function skip(el) {
    return el && el.closest && el.closest('script,style,noscript,.fw-menu,.fw-bar,.fw-dock,.fw-theme-btn,[data-no-i18n]');
  }
  function walk(rootNode) {
    if (rootNode.nodeType === 3) { var pe = rootNode.parentElement; if (!skip(pe) && !(pe && pe.closest(HSEL) && pe.closest(HSEL)._fwEN)) doText(rootNode); return; }
    if (rootNode.nodeType !== 1 || skip(rootNode)) return;
    if (doHTML(rootNode)) return;
    doAttrs(rootNode);
    var w = document.createTreeWalker(rootNode, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT, {
      acceptNode: function (n) {
        if (n.nodeType === 1) { if (skip(n)) return NodeFilter.FILTER_REJECT; if (doHTML(n)) return NodeFilter.FILTER_REJECT; return NodeFilter.FILTER_ACCEPT; }
        return NodeFilter.FILTER_ACCEPT;
      } });
    var n; while ((n = w.nextNode())) { if (n.nodeType === 3) doText(n); else doAttrs(n); }
  }
  function toEN() { busy = true; walk(document.body); mo.takeRecords(); busy = false; }
  function toFR() {
    busy = true;
    swapped.forEach(function (el) { if (el._fwEN) { el.innerHTML = el._fwFR; el._fwEN = false; } });
    swapped.clear();
    touched.forEach(function (n) { if (origText.has(n) && setText.get(n) === n.nodeValue) n.nodeValue = origText.get(n); });
    touched.clear(); origText = new WeakMap(); setText = new WeakMap();
    touchedEl.forEach(function (el) { var o = origAttr.get(el) || {};
      ATTRS.forEach(function (a) { if (o[a] != null && el.getAttribute(a) === o['_set_' + a]) el.setAttribute(a, o[a]); }); });
    touchedEl.clear(); origAttr = new WeakMap();
    mo.takeRecords();   // our own edits: not page changes
    busy = false;
  }

  var mo = new MutationObserver(function (list) {
    if (busy || !isEN()) return;
    busy = true;
    for (var i = 0; i < list.length; i++) {
      var r = list[i];
      if (r.type === 'childList') {
        // a script rewrote a swapped element: it is French again
        if (r.target._fwEN && r.target.matches && r.target.matches(HSEL)) { r.target._fwEN = false; swapped.delete(r.target); walk(r.target); continue; }
        for (var j = 0; j < r.addedNodes.length; j++) walk(r.addedNodes[j]);
      }
      else if (r.type === 'characterData') { if (!skip(r.target.parentElement)) doText(r.target); }
      else if (r.type === 'attributes' && r.target.nodeType === 1 && !skip(r.target)) doAttrs(r.target);
    }
    mo.takeRecords();
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
