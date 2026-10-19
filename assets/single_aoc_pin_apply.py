#!/usr/bin/env python3
"""Bordeaux-style region maps (Bordeaux.html, Bourgogne Regions/Beaujolais.html): a commune with a single
appellation now behaves like the others when clicked (2026-10-14).

Before: clicking a single-appellation commune (e.g. every Coteaux du Lyonnais commune) showed a plain
« Commune · Appartient à » card — the popup did not lock, no detail panel, no « Accéder au plan cadastral ».
Now the appellation list is pinned as for multi-appellation communes and, when there is only one appellation,
its detail panel (with the plan button at the bottom) opens straight away.
Usage (from WEB Site/): python3 assets/single_aoc_pin_apply.py Bordeaux.html "Bourgogne Regions/Beaujolais.html"
"""
import sys
OLD1 = "    if(ordered.length<=1){ showCommune(code,nom); return; }\n"
NEW1 = "    // a single appellation is pinned like several (detail panel opened straight away, see below)\n"
OLD2 = "    hint('commune : '+nom+' — choisissez une appellation');\n  }\n  function unpin(){ "
NEW2 = ("    hint('commune : '+nom+' — choisissez une appellation');\n"
        "    if(ordered.length===1){ var li=tip.querySelector('.tip-li'); if(li) li.classList.add('active'); showDetail(ordered[0]); }\n"
        "  }\n  function unpin(){ ")
OLD3 = "'+ordered.length+' appellations</span>"
NEW3 = "'+ordered.length+' appellation'+(ordered.length>1?'s':'')+'</span>"   # « 1 appellation »
for path in sys.argv[1:]:
    s = open(path, encoding='utf-8').read()
    if NEW1 in s:
        print('skip (already patched)', path); continue
    for a, b in ((OLD1, NEW1), (OLD2, NEW2), (OLD3, NEW3)):
        if s.count(a) != 1: sys.exit('%s: expected one match for %r (found %d)' % (path, a[:50], s.count(a)))
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s); print('ok', path)
