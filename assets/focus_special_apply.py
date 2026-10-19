#!/usr/bin/env python3
"""Appellation focus mode for the region maps that do NOT use the shared template (2026-10-14).

Selecting an appellation fades every other appellation fill to 10 % so its true coverage stands out.
  Cote-d_Or.html      — villages, grands crus, sous-régionales, dénominations (régionales keep the full map);
                        a selected grand cru shows only its parcel; grand-cru parcels + hatching fade too;
                        fitPad() frames the selection between title card, legend and info card.
  Saone-et-Loire.html — every appellation except the régionales; hatching fades too.
  Alsace.html         — selecting a Grand Cru fades the other parcels + every commune fill
                        (run AFTER focus_apply.py and focus_exit_apply.py, which give the commune-level focus).
  Bordeaux.html, Beaujolais.html — other communes keep a 10 % tint of their usual colour (was plain cream).

Usage (from WEB Site/):  python3 assets/focus_special_apply.py <page.html> [...]
Already-patched pages are skipped. Run after contour_fade_apply.py / soften_fills_apply.py.
"""
import sys

FADE = "{color:'#c9bfa6',weight:0.4,fillColor:fill,fillOpacity:0.1}"

COTE_DOR = [
    ("const on=(selectedAppel && APPEL_CODES[selectedAppel] && APPEL_CODES[selectedAppel].has(code));\n",
     "// a selected grand cru is shown by its parcels only, so every commune fades behind it\n"
     "    const on=(selectedAppel && !GC_SET.has(selectedAppel) && APPEL_CODES[selectedAppel] && APPEL_CODES[selectedAppel].has(code));\n"
     "    if(focusDim() && !on) return " + FADE + ";\n"),
    ("const GC_STYLE=function(f,on){ const white=f.properties.white;\n",
     "const GC_STYLE=function(f,on){ const white=f.properties.white;\n"
     "    if(focusDim() && !on) return {pane:'gcPane',color:'#c9bfa6',weight:0.4,opacity:0.5,fillColor:f.properties.color,fillOpacity:0.1,lineJoin:'round'};\n"),
    ("let selectedAppel=null;\n",
     "let selectedAppel=null;\n"
     "  // focus mode: selecting a village, grand cru, sous-régionale or dénomination (or a name listed here) dims every\n"
     "  // other AOC fill (communes, grand crus, hatching) to 10 %; only the régionales keep the full map\n"
     "  const FOCUS_KINDS=new Set(['village','grandcru','subreg','denom']);\n"
     "  const FOCUS_APPELS=new Set(['Côte de Nuits-Villages','Côte de Beaune-Villages','Côte de Beaune',\"Bourgogne Côte d'Or\",'Bourgogne Hautes Côtes de Nuits','Bourgogne Hautes Côtes de Beaune','Bourgogne Le Chapitre','Bourgogne Montrecul','Bourgogne La Chapelle Notre-Dame']);\n"
     "  function focusDim(){ return !!(selectedAppel && (FOCUS_APPELS.has(selectedAppel) || FOCUS_KINDS.has((META[selectedAppel]||{}).kind))); }\n"
     "  function applyFocusPane(){ var hp=map.getPane('hatchPane'); if(hp) hp.style.opacity=focusDim()?'0.1':''; }\n"),
    ("selectedAppel=name; layer.setStyle(styleFor); styleGC();",
     "selectedAppel=name; layer.setStyle(styleFor); styleGC(); applyFocusPane();"),
    ("selectedAppel=null; layer.setStyle(styleFor); styleGC();",
     "selectedAppel=null; layer.setStyle(styleFor); styleGC(); applyFocusPane();"),
    ("map.flyToBounds(b,{paddingTopLeft:[360,70],paddingBottomRight:[40,40],maxZoom:14,duration:0.75})",
     "map.flyToBounds(b,Object.assign(fitPad(),{maxZoom:14,duration:0.75}))"),
    ("map.flyToBounds(b,{paddingTopLeft:[360,70],paddingBottomRight:[40,40],maxZoom:big?11:12.5,duration:0.75})",
     "map.flyToBounds(b,Object.assign(fitPad(),{maxZoom:big?11:12.5,duration:0.75}))"),
    ("  function buildReadout(name,eyebrow){",
     """  // frame a selection in the map space left free by the title card (top-left), the appellations legend
  // (bottom-left) and the open info card (right); on narrow screens the title card may be overlapped first,
  // then the info-card margin shrinks
  function fitPad(){
    const mr=map.getContainer().getBoundingClientRect(), W=mr.width, H=mr.height;
    const vis=function(id){ const el=document.getElementById(id); if(!el||el.style.display==='none'||!el.offsetParent) return null;
      const r=el.getBoundingClientRect(); return (r.width&&r.height)?r:null; };
    const tc=vis('title-card'), ro=vis('readout'), lg=vis('appel-legend');
    let left=40, right=40, top=70, bottom=40;
    if(tc) left=Math.max(left,tc.right-mr.left+16);
    if(ro&&ro.width<W-40) right=Math.max(right,mr.right-ro.left+16);
    if(left+right>W-160) left=20;
    if(left+right>W-160) right=Math.max(20,W-180-left);
    if(lg){ // keep clear of the legend: either start right of it or stop above it, whichever leaves more room
      const lgRight=lg.right-mr.left+16, lgTop=H-(lg.top-mr.top)+16;
      const wA=W-Math.max(left,lgRight)-right, hA=H-top-bottom;
      const wB=W-left-right, hB=H-top-Math.max(bottom,lgTop);
      if(wA>=120&&(wA*hA>=wB*hB||hB<120)) left=Math.max(left,lgRight);
      else if(hB>=120) bottom=Math.max(bottom,lgTop);
    }
    return {paddingTopLeft:[left,top],paddingBottomRight:[right,bottom]};
  }
  function buildReadout(name,eyebrow){"""),
]

SAONE = [
    ("    const on=(selectedAppel && APPEL_CODES[selectedAppel] && APPEL_CODES[selectedAppel].has(code));\n    if(fill===CREAM){",
     "    const on=(selectedAppel && APPEL_CODES[selectedAppel] && APPEL_CODES[selectedAppel].has(code));\n"
     "    if(focusDim() && !on) return " + FADE + ";\n    if(fill===CREAM){"),
    ("let selectedAppel=null;       // single unified selection\n",
     "let selectedAppel=null;       // single unified selection\n"
     "  // focus mode: selecting any appellation except a régionale dims every other AOC fill (and the hatching) to 10 %\n"
     "  function focusDim(){ return !!(selectedAppel && (META[selectedAppel]||{}).kind!=='regionale'); }\n"
     "  function applyFocusPane(){ var hp=map.getPane('hatchPane'); if(hp) hp.style.opacity=focusDim()?'0.1':''; }\n"),
    ("    selectedAppel=name;\n    layer.setStyle(styleFor);\n",
     "    selectedAppel=name;\n    layer.setStyle(styleFor); applyFocusPane();\n"),
    ("selectedAppel=null; layer.setStyle(styleFor); readout.style.display='none';",
     "selectedAppel=null; layer.setStyle(styleFor); applyFocusPane(); readout.style.display='none';"),
]

ALSACE = [
    ("function gcStyleFor(nm){ if(gcColorMode){",
     "function gcStyleFor(nm){\n    // focus mode: while a Grand Cru is selected, every other parcel fades to 10 %\n"
     "    if(gcSelName && gcSelName!==nm){ var d=gcColorMode?{fillColor:(GRAPE_COLOR[domOf(nm)]||GC_FILL)}:gcBaseStyle(); "
     "return Object.assign({},d,{color:'#c9bfa6',weight:0.4,opacity:0.5,fillOpacity:0.1}); }\n    if(gcColorMode){"),
    ("function clearGCSel(){ if(gcSelName){ resetGC(gcSelName); gcSelName=null; } }",
     "function clearGCSel(){ if(gcSelName){ gcSelName=null; grandcruLayer.setStyle(function(f){return gcStyleFor(f.properties.name);}); if(FOCUS_NAME==='__gc__') setFocus(null); } }"),
    ("  function selectGC(nm){\n    if(gcSelName&&gcSelName!==nm) resetGC(gcSelName);\n    gcSelName=nm; var l=GC_LYR[nm]; if(!l) return;\n",
     "  function selectGC(nm){\n    clearHighlight();\n    gcSelName=nm; var l=GC_LYR[nm]; if(!l) return;\n"
     "    grandcruLayer.setStyle(function(f){return gcStyleFor(f.properties.name);});\n"
     "    FOCUS_NEXT='__gc__'; setFocus(new Set(['__gc__']));           // fade every commune fill behind the parcel\n"),
    ("  document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&FOCUS_CODES) clearHighlight(); });",
     "  document.addEventListener('keydown',function(e){ if(e.key!=='Escape') return; if(typeof hideGC==='function'&&gcSelName) hideGC(); if(FOCUS_CODES) clearHighlight(); });"),
]

def tint(fill):
    return [('}else if(selected){ lyr.setStyle({fillColor:"#efe7d4",fillOpacity:1,color:"#cbbf9f",weight:0.3});',
             '}else if(selected){ // focus mode: every other commune keeps a 10 % tint of its usual colour\n'
             '        lyr.setStyle({fillColor:' + fill + ',fillOpacity:0.1,color:"#cbbf9f",weight:0.3});')]

PAGES = {
    'Cote-d_Or.html': (COTE_DOR, 'function focusDim('),
    'Saone-et-Loire.html': (SAONE, 'function focusDim('),
    'Alsace.html': (ALSACE, "FOCUS_NEXT='__gc__'"),
    'Bordeaux.html': (tint('defaultFill(code)'), '10 % tint of its usual colour'),
    'Beaujolais.html': (tint('baseFill(code)[0]'), '10 % tint of its usual colour'),
}

for path in sys.argv[1:]:
    name = path.replace('\\', '/').split('/')[-1]
    if name not in PAGES:
        print('skip (not a special page)', path); continue
    reps, marker = PAGES[name]
    s = open(path, encoding='utf-8').read()
    if marker in s:
        print('skip (already patched)', path); continue
    if name == 'Alsace.html' and 'function setFocus(' not in s:
        sys.exit('Alsace.html: run focus_apply.py and focus_exit_apply.py first')
    for a, b in reps:
        if s.count(a) != 1:
            sys.exit('%s: expected exactly one match for %r (found %d)' % (path, a[:60], s.count(a)))
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)
    print('ok', path)
