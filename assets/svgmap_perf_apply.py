#!/usr/bin/env python3
"""Carte de France & Carte des IGP: make wheel/trackpad zoom fast and steady (2026-10-15).

1. The blue sea glow (8 coastline strokes with 26-unit Gaussian blurs) and the #france CSS drop-shadow were
   re-rendered on every zoom commit — up to ~1 s per redraw when zoomed in. They are now baked once into
   assets/seafade.webp (source: assets/seafade_src.svg, rendered with headless Chrome) and drawn as an <image>.
2. The sharp SVG redraw (commit) now waits until the zoom has been idle for 160 ms, instead of firing on every
   tiny pause of a trackpad gesture (each pause caused a heavy redraw = jitter).
3. While the map moves, hover effects on regions / IGPs are switched off (no repaint storms under the cursor).

Idempotent. Run after svgmap_smooth_apply.py:  python3 assets/svgmap_perf_apply.py
To re-bake the image: render assets/seafade_src.svg at 2200×2060 (transparent) and save as assets/seafade.webp.
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
PAGES = ['Vignobles de France — Carte de France.html', 'Vignobles de France — Carte des IGP.html']
IMG = '<image id="seafadeImg" href="assets/seafade.webp" x="0" y="0" width="2200" height="2060" preserveAspectRatio="none" style="pointer-events:none"/>'
CSS = ('<!--fw-svgperf:start--><style id="fw-svgperf-css">#france{filter:none !important}'
       '.zmove #igp,.zmove #regions,.zmove #labels{pointer-events:none}</style><!--fw-svgperf:end-->\n')

END_OLD = "else{tx=tTx;ty=tTy;scale=tScale;raf=null;if(!drag)commit();}}"
END_NEW = "else{tx=tTx;ty=tTy;scale=tScale;raf=null;if(!drag)later();}}"
UP_OLD = "if(drag){svg.classList.remove('drag');drag=null;if(!raf)commit();}"
UP_NEW = "if(drag){svg.classList.remove('drag');drag=null;if(!raf)later();}"
COMMIT_OLD = "function commit(){vp.setAttribute("
COMMIT_NEW = ("let cT=null;function later(){clearTimeout(cT);cT=setTimeout(()=>{if(!raf&&!drag)commit();},160);}"
              "function commit(){clearTimeout(cT);zwrap.classList.remove('zmove');vp.setAttribute(")
APPLY_OLD = "function apply(){const g=geo(),"
APPLY_NEW = "function apply(){zwrap.classList.add('zmove');const g=geo(),"

for name in PAGES:
    p = SITE / name
    s = p.read_text(encoding='utf-8'); s0 = s
    # 1. baked sea glow
    s = re.sub(r'<g id="seafade"[^>]*>.*?</g>', IMG, s, count=1, flags=re.S)
    s = re.sub(r'<!--fw-svgperf:start-->.*?<!--fw-svgperf:end-->\n?', '', s, flags=re.S)
    k = s.find('</head>'); s = s[:k] + CSS + s[k:]
    # 2./3. debounced commit + no hover while moving
    if 'function later()' not in s:
        for old, new in [(END_OLD, END_NEW), (UP_OLD, UP_NEW), (COMMIT_OLD, COMMIT_NEW), (APPLY_OLD, APPLY_NEW)]:
            assert s.count(old) == 1, (name, old[:40])
            s = s.replace(old, new)
    if s != s0:
        p.write_text(s, encoding='utf-8'); print('  patched:', name)
    else:
        print('  unchanged:', name)
