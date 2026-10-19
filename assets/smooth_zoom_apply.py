"""Region maps: let the page's label overlay cooperate with the site-wide smooth zoom (assets/theme.js).

theme.js zooms every Leaflet map by CSS-scaling it per frame and fires 'smoothzoomstart' / 'smoothzoomend'.
Region maps redraw their whole HTML label overlay (renderLabels) on every 'zoom'/'move' event, which made the
zoom stutter; their old wheel code avoided that with `zoomAnimating` + a hidden `labelLayer`. This adds the same
two hooks for the shared zoom, right after the page's renderLabels binding. Idempotent; rerun after rebuilding a map.

Run:  python3 assets/smooth_zoom_apply.py
"""
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
ANCHOR = "map.on('zoom move viewreset zoomend moveend',renderLabels);"
MARK = '/*fw-smoothzoom*/'
SNIPPET = (MARK + "map.on('smoothzoomstart',function(){zoomAnimating=true;labelLayer.style.visibility='hidden';});"
           "map.on('smoothzoomend',function(){zoomAnimating=false;renderLabels();});")

done = skipped = 0
for p in sorted(list(SITE.glob('*.html')) + list((SITE / 'Bourgogne Regions').glob('*.html'))):
    s = p.read_text(encoding='utf-8')
    if 'zoomAnimating' not in s or ANCHOR not in s:
        continue
    if MARK in s:
        skipped += 1
        continue
    p.write_text(s.replace(ANCHOR, ANCHOR + '\n  ' + SNIPPET, 1), encoding='utf-8')
    done += 1
    print('  patched', p.relative_to(SITE))
print(f'{done} patched, {skipped} already done')
