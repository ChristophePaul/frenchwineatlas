import re,glob,sys
PRELUDE="""  // contour fade (shared): curves ramp from faint at the overview zoom (first fit) to full strength 2 levels in
  var CZ0=null, CONTOUR_LAYERS=[];
  function contourStyle(f){ const ix=(f.properties.idx===1), z=map.getZoom();
    const k=(z==null||CZ0==null)?0:Math.max(0,Math.min(1,(z-CZ0)/2));
    // 100 m index lines gently 0.5 → 0.95; 20 m lines 0.1 → 0.85
    return {color:ix?'#4a3112':'#5f4522',weight:ix?(0.6+0.2*k):(0.35+0.15*k),opacity:ix?(0.5+0.45*k):(0.1+0.75*k),fill:false,lineJoin:'round',lineCap:'round'}; }
  function contourFade(cl){ CONTOUR_LAYERS.push(cl); return cl; }
  function contourRestyle(){ CONTOUR_LAYERS.forEach(function(cl){ cl.setStyle(contourStyle); }); }
  map.on('zoomend',contourRestyle);
  (function(fb){ map.fitBounds=function(){ const r=fb.apply(this,arguments), z=this.getZoom();
    if(z!=null&&(CZ0==null||z<CZ0)){ CZ0=z; contourRestyle(); } return r; }; })(map.fitBounds);
"""
STYLE=re.compile(r"style:function\(f\)\{ const ix=\(f\.properties\.idx===1\);\n(?:\s*//[^\n]*\n)?\s*return \{color:ix\?[^}]*\}; \}\n(\s*)\}\)\.addTo\(map\);")
RHONE=re.compile(r"style:contourStyle\n(\s*)\}\)\.addTo\(map\);\n\s*// 20 m curves fade[^\n]*\n\s*map\.on\('zoomend',function\(\)\{ contourLayer\.setStyle\(contourStyle\); \}\);\n(\s*\}\n)\s*function contourStyle\(f\)\{.*?lineCap:'round'\}; \}\n",re.S)
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'contourFade(' in s: print('skip',f); continue
    m=RHONE.search(s)
    if m:
        s=s[:m.start()]+"style:contourStyle\n"+m.group(1)+"}).addTo(map));\n"+m.group(2)+s[m.end():]
        st=s.rfind('L.geoJSON(',0,m.start())
    else:
        m=STYLE.search(s); assert m,f
        st=s.rfind('L.geoJSON(',0,m.start())
        s=s[:m.start()]+"style:contourStyle\n"+m.group(1)+"}).addTo(map));"+s[m.end():]
    s=s[:st]+'contourFade('+s[st:]
    # prelude goes before the line holding "if(...contours){"
    ifp=s.rfind('if(',0,st); ln=s.rfind('\n',0,ifp)+1
    s=s[:ln]+PRELUDE+s[ln:]
    # initial fit must come after the prelude
    fit=s.find('map.fitBounds(',ln); assert fit>ln,f
    s=re.sub(r"(\.lg-contour\{width:16px;height:0;border-top:)1\.4px solid #[0-9a-fA-F]{6}",r"\g<1>1.6px solid #5f4522",s)
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
