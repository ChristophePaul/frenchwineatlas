#!/usr/bin/env python3
"""Let the site search open an AOC on a regional map: Bordeaux.html#aoc=Pauillac.

    python3 assets/search_hooks_apply.py [pages…]      (default: every regional map)

Adds window.fwOpenAppel(name) inside each map's script, next to its showDetail(), calling the
map's own select function (highlightAppel or selectAppel) and showing the AOC card. search.js
reads #aoc= on load and calls it once the map is ready. Idempotent — rerun after rebuilding a map.
"""
import pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent
START, END = '/*fw-search-hook*/', '/*fw-search-hook:end*/'

HOOK_HIGHLIGHT = (START + "window.fwOpenAppel=function(n){if(typeof APPEL_CODES==='undefined'||!APPEL_CODES[n])return false;"
                  "highlightAppel(n);try{showDetail(n);}catch(e){}return true;};" + END)
HOOK_SELECT = (START + "window.fwOpenAppel=function(n){selectAppel(n);return true;};" + END)


def apply(p):
    t = p.read_text(encoding='utf-8')
    t = re.sub(re.escape(START) + r'.*?' + re.escape(END), '', t, flags=re.S)
    if 'function showDetail(' not in t:
        return 'no showDetail'
    hook = HOOK_SELECT if re.search(r'function selectAppel\(', t) else HOOK_HIGHLIGHT
    if hook is HOOK_HIGHLIGHT and not re.search(r'function highlightAppel\(', t):
        return 'no select function'
    t = t.replace('function showDetail(', hook + 'function showDetail(', 1)
    p.write_text(t, encoding='utf-8')
    return 'ok (' + ('selectAppel' if hook is HOOK_SELECT else 'highlightAppel') + ')'


pages = [SITE / a for a in sys.argv[1:]] or [p for p in sorted(list(SITE.glob('*.html')) + list((SITE / 'Bourgogne Regions').glob('*.html')))
                                              if 'function showDetail(' in p.read_text(encoding='utf-8', errors='ignore')]
for p in pages:
    print(f'{p.relative_to(SITE)}: {apply(p)}')
