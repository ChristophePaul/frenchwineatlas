#!/usr/bin/env python3
"""Sidebar appellation rows show the appellation's FULL area, like the commune popup (2026-10-14).

Before: a sidebar row outlined only the communes painted in that appellation's colour (its "communeTop"
group), so e.g. Saint-Bris showed 2 communes from the sidebar but 5 from the popup (Chitry, Irancy and
Vincelottes are painted in their more specific appellation's colour but are in the Saint-Bris area).
Now a row whose name is a real appellation highlights its whole area and the count shows the number of
communes in that area. Group rows that are not a single appellation ("Chablis / Petit Chablis",
"Bourgogne régionale", "Côtes du Rhône Villages (aire)"…) keep the colour-group behaviour.

Usage (from WEB Site/):  python3 assets/sidebar_area_apply.py <page.html> [...]   (skips pages already done)
"""
import sys

REPS = [
    ("  function highlightFill(name){\n",
     "  function highlightFill(name){\n"
     "    // a real appellation: show its full area (same as the commune popup), not just the communes painted in its colour\n"
     "    if(APPEL_CODES[name]&&APPEL_CODES[name].size){ highlightAppel(name); return; }\n"),
    ("<b>'+a.count+'</b></div>'; }); }\n    else if(AOC_FILL)",
     "<b>'+(APPEL_CODES[a.name]?APPEL_CODES[a.name].size:a.count)+'</b></div>'; }); }\n    else if(AOC_FILL)"),
]
for path in sys.argv[1:]:
    s = open(path, encoding='utf-8').read()
    if 'function highlightFill(' not in s:
        print('skip (no sidebar fill rows)', path); continue
    if 'show its full area (same as the commune popup)' in s:
        print('skip (already patched)', path); continue
    for a, b in REPS:
        if s.count(a) != 1:
            sys.exit('%s: expected exactly one match for %r (found %d)' % (path, a[:50], s.count(a)))
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)
    print('ok', path)
