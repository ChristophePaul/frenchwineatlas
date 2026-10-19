"""Carte de France & Carte des IGP (SVG maps): same smooth zoom as the Leaflet maps / « Placez l'AOC ».

These pages zoomed by rewriting the SVG group transform every frame, which forces the whole vector map to be
re-rasterised (one frame could take ~1 s). Now, while the zoom eases or the map is dragged, the already-drawn
<svg> is only moved/scaled with a GPU CSS transform; the real SVG transform is committed once, when the motion
stops (sharp redraw). Wheel sensitivity matches Leaflet's getWheelDelta × 0.045 (×0.12 for trackpad pinch).
Idempotent; rerun after regenerating either map.

Run:  python3 assets/svgmap_smooth_apply.py
"""
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
PAGES = ['Vignobles de France — Carte de France.html', 'Vignobles de France — Carte des IGP.html']
MARK = '/*fw-svgsmooth*/'

OLD_APPLY = "function apply(){vp.setAttribute('transform','translate('+tx+' '+ty+') scale('+scale+')')}"
NEW_APPLY = (MARK + "let cS=1,cTx=0,cTy=0,box0=null;"
    # GPU layer: a plain div around the <svg> (an <svg> root itself is re-rasterised on every scale change)
    "const zwrap=(()=>{const w=document.createElement('div');w.style.cssText='position:absolute;inset:0;transform-origin:0 0;will-change:transform;';"
    "svg.parentNode.insertBefore(w,svg);w.appendChild(svg);return w;})();"
    # committed SVG transform (sharp) + cached un-transformed geometry of the <svg> box
    "function geo(){if(!box0){const r=svg.getBoundingClientRect(),vb=svg.viewBox.baseVal,u=Math.min(r.width/vb.width,r.height/vb.height);"
    "box0={l:r.left,t:r.top,u:u,ox:(r.width-vb.width*u)/2-vb.x*u,oy:(r.height-vb.height*u)/2-vb.y*u};}return box0;}"
    "window.addEventListener('resize',()=>{commit();box0=null;});"
    "function commit(){vp.setAttribute('transform','translate('+tx+' '+ty+') scale('+scale+')');cS=scale;cTx=tx;cTy=ty;zwrap.style.transform='';}"
    # visual = committed scaled by k about the svg origin, expressed as a CSS transform in px on the wrapper
    "function apply(){const g=geo(),k=scale/cS,dx=tx-k*cTx,dy=ty-k*cTy;"
    "zwrap.style.transform='translate('+(g.ox+g.u*dx-k*g.ox)+'px,'+(g.oy+g.u*dy-k*g.oy)+'px) scale('+k+')';}")

OLD_END = "else{tx=tTx;ty=tTy;scale=tScale;apply();raf=null;}}"
NEW_END = "else{tx=tTx;ty=tTy;scale=tScale;raf=null;if(!drag)commit();}}"

OLD_TOVB = "function toVB(cx,cy){const pt=svg.createSVGPoint();pt.x=cx;pt.y=cy;return pt.matrixTransform(svg.getScreenCTM().inverse());}"
NEW_TOVB = "function toVB(cx,cy){const g=geo();return {x:(cx-g.l-g.ox)/g.u,y:(cy-g.t-g.oy)/g.u};}"

OLD_WHEEL = "zoomTo(p.x,p.y,Math.exp(-ev.deltaY*0.0016));"
NEW_WHEEL = ("const pf=/Mac/.test(navigator.platform)?(window.devicePixelRatio||1)*3:/Linux/.test(navigator.platform)&&/Chrome/.test(navigator.userAgent)?(window.devicePixelRatio||1):2*(window.devicePixelRatio||1);"
             "const wd=ev.deltaMode===1?-ev.deltaY*20:ev.deltaMode===2?-ev.deltaY*60:-ev.deltaY/pf;"
             "zoomTo(p.x,p.y,Math.pow(2,wd*(ev.ctrlKey?0.12:0.045)));")

OLD_DRAGK = "const r=svg.getBoundingClientRect();const k=(2200.0)/r.width;"
NEW_DRAGK = "const k=1/geo().u;"

OLD_UP = "window.addEventListener('pointerup',()=>{if(drag)svg.classList.remove('drag');drag=null});"
NEW_UP = "window.addEventListener('pointerup',()=>{if(drag){svg.classList.remove('drag');drag=null;if(!raf)commit();}});"

REPL = [(OLD_APPLY, NEW_APPLY), (OLD_END, NEW_END), (OLD_TOVB, NEW_TOVB), (OLD_WHEEL, NEW_WHEEL),
        (OLD_DRAGK, NEW_DRAGK), (OLD_UP, NEW_UP)]

for name in PAGES:
    p = SITE / name
    s = p.read_text(encoding='utf-8')
    if MARK in s:
        if 'zwrap' in s:
            print('  already done:', name)
            continue
        a = s.index(MARK); b = s.index('px) scale(\'+k+\')\';}', a) + len('px) scale(\'+k+\')\';}')
        s = s[:a] + NEW_APPLY + s[b:]
        p.write_text(s, encoding='utf-8')
        print('  upgraded:', name)
        continue
    for old, new in REPL:
        assert s.count(old) == 1, (name, old[:50])
        s = s.replace(old, new)
    p.write_text(s, encoding='utf-8')
    print('  patched:', name)
