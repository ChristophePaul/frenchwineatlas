#!/usr/bin/env python3
"""Re-apply every 2026-10-14 region-map effect to freshly rebuilt pages, in the right order.

  1. contour_fade_apply.py   — dark-brown elevation curves that fade when zoomed out
  2. soften_fills_apply.py   — dark appellation colours blended toward cream
  3. focus_apply.py          — appellation focus mode (shared-template pages)
  4. focus_exit_apply.py     — leave focus: same row again, Escape, click a faded commune
  5. focus_special_apply.py  — focus mode for Côte-d'Or, Saône-et-Loire, Alsace grands crus, Bordeaux, Beaujolais
  6. sidebar_area_apply.py   — sidebar appellation rows show the full area (same as the commune popup)
  7. rhone_sept_trim_apply.py — Rhône septentrional only: drop the Beaujolais / Roannais / Forez part
  8. beaujolais_lyonnais_apply.py — Beaujolais only: add Coteaux du Lyonnais, rename « … et du Lyonnais »
  9. beaujolais_crus_mention_apply.py — Beaujolais only: crus' « mention » line per their CDC
 10. single_aoc_pin_apply.py — Bordeaux + Beaujolais: single-appellation communes lock the popup too

Usage (from WEB Site/):  python3 assets/map_effects_apply.py "Rhone-meridional.html" ["Bourgogne Regions/Cote-d_Or.html" ...]
Each step skips a page it does not apply to or that is already patched, so rerunning is safe.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))


def run(script, pages):
    if pages:
        subprocess.run([sys.executable, '-I', os.path.join(HERE, script)] + pages, check=True)


def has(path, text):
    return text in open(path, encoding='utf-8').read()


pages = sys.argv[1:]
if not pages:
    sys.exit(__doc__)
run('contour_fade_apply.py', [p for p in pages if has(p, 'contourPane')])
run('soften_fills_apply.py', pages)
run('focus_apply.py', [p for p in pages if has(p, 'function clearHighlight(){') and not has(p, 'function setFocus(')])
run('focus_exit_apply.py', [p for p in pages if has(p, 'function setFocus(')])
run('focus_special_apply.py', pages)
run('sidebar_area_apply.py', [p for p in pages if has(p, 'function highlightFill(')])
run('rhone_sept_trim_apply.py', [p for p in pages if os.path.basename(p) == 'Rhone-septentrional.html'])
run('beaujolais_lyonnais_apply.py', [p for p in pages if os.path.basename(p) == 'Beaujolais.html'])
run('beaujolais_crus_mention_apply.py', [p for p in pages if os.path.basename(p) == 'Beaujolais.html'])
run('single_aoc_pin_apply.py', [p for p in pages if os.path.basename(p) in ('Beaujolais.html', 'Bordeaux.html')])
