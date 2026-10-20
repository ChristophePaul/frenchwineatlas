#!/usr/bin/env python3
"""Carte de France & Carte des IGP: two-finger pinch zoom on phones and tablets (2026-10-20).

The pages' own pan code follows one pointer only, and the browser handled the pinch itself (whole-page zoom),
so a pinch either zoomed the page or made the map jump. This patch:
1. sets touch-action:none on the map (the page no longer zooms or scrolls under the fingers);
2. tracks every pointer: with two fingers down, the map zooms around the point between them and follows them
   (pan + zoom together), using the same scale/tx/ty + apply()/later() engine as the wheel zoom;
3. when one finger lifts, the other carries on panning without a jump; a pinch never counts as a click.

Idempotent (marker /*fw-svgpinch*/). Run after svgmap_smooth_apply.py and svgmap_perf_apply.py:
    python3 assets/svgmap_pinch_apply.py
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
PAGES = ['Vignobles de France — Carte de France.html', 'Vignobles de France — Carte des IGP.html']
CSS = ('<!--fw-svgpinch:start--><style id="fw-svgpinch-css">#stage svg{touch-action:none}</style>'
       '<!--fw-svgpinch:end-->\n')
ANCHOR = 'function viewCenter(){'
JS = (
    "/*fw-svgpinch*/(()=>{const pts=new Map();let pin=null,noClick=false;"
    "const two=()=>{const a=[...pts.values()];return {d:Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y)||1,"
    "m:toVB((a[0].x+a[1].x)/2,(a[0].y+a[1].y)/2)};};"
    "svg.addEventListener('pointerdown',ev=>{pts.set(ev.pointerId,{x:ev.clientX,y:ev.clientY});"
    "if(pts.size===2){drag=null;svg.classList.remove('drag');if(raf){cancelAnimationFrame(raf);raf=null;}"
    "const t=two();pin={d:t.d,px:(t.m.x-tx)/scale,py:(t.m.y-ty)/scale,s:scale};noClick=true;}});"
    "window.addEventListener('pointermove',ev=>{if(!pts.has(ev.pointerId))return;"
    "pts.set(ev.pointerId,{x:ev.clientX,y:ev.clientY});if(!pin||pts.size<2)return;"
    "const t=two(),ns=Math.max(1,Math.min(pin.s*t.d/pin.d,10));"
    "scale=tScale=ns;tx=tTx=t.m.x-pin.px*ns;ty=tTy=t.m.y-pin.py*ns;apply();},{passive:true});"
    "const up=ev=>{if(!pts.delete(ev.pointerId))return;"
    "if(pin&&pts.size<2){pin=null;if(scale<=1.0001){scale=tScale=1;tx=tTx=0;ty=tTy=0;apply();}"
    "const r=[...pts.values()][0];if(r){drag={x:r.x,y:r.y,tx,ty,moved:true};}else later();}"
    "if(!pts.size)setTimeout(()=>{noClick=false;},0);};"
    "window.addEventListener('pointerup',up);window.addEventListener('pointercancel',up);"
    "svg.addEventListener('click',ev=>{if(noClick){ev.stopPropagation();ev.preventDefault();}},true);})();\n"
)

for name in PAGES:
    p = SITE / name
    s = p.read_text(encoding='utf-8'); s0 = s
    s = re.sub(r'<!--fw-svgpinch:start-->.*?<!--fw-svgpinch:end-->\n?', '', s, flags=re.S)
    k = s.find('</head>'); s = s[:k] + CSS + s[k:]
    s = re.sub(r'/\*fw-svgpinch\*/.*?\}\)\(\);\n', '', s, flags=re.S)
    assert s.count(ANCHOR) == 1, name
    s = s.replace(ANCHOR, JS + ANCHOR)
    if s != s0:
        p.write_text(s, encoding='utf-8'); print('patched', name)
    else:
        print('unchanged', name)
