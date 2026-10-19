#!/usr/bin/env python3
"""Chablis & Auxerrois region map (Bourgogne Regions/Chablis_et_de_l_Auxerrois.html):
  1. « Chablis 1er Cru » and a full « Chablis Grand Cru » fiche in the commune info-tip (data: CDC Chablis, arrêté du
     11 décembre 2023 ; CDC Chablis grand cru, arrêté du 24 octobre 2024 ; communes from the INAO 2026 delimitation),
     with their climats as chips (same look as the Côte-d'Or premiers crus);
  2. a selected-appellation card (#readout.has-card, as on the Côte-d'Or map) opened by a sidebar row or by clicking an
     appellation in a commune's list; it ends with the plan button (fwPlanLink, from plan_links_apply.py).
Idempotent. Run from WEB Site/, then plan_links_apply.py and assets/i18n_build.py.
"""
import json, os
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(SITE, 'Bourgogne Regions', 'Chablis_et_de_l_Auxerrois.html')
s = open(F, encoding='utf-8').read()

# ---------- 1. data
i = s.find('window.MAPDATA'); j = s.find('{', i)
D, end = json.JSONDecoder().raw_decode(s, j)
PC_CODES = ['89034', '89068', '89081', '89104', '89123', '89168', '89175', '89242']   # INAO « Chablis premier cru »
CW = {'white': [['Chardonnay B'], []]}
D['appelMeta']['Chablis Grand Cru'] = {
    'colors': ['W'], 'communes': ['Chablis'],
    'year_note': 'AOC 1938 · sept climats sur la rive droite du Serein',
    'grapes': CW, 'yield': 'Blanc : 54 hl/ha (butoir 64)', 'abv': 'Titre naturel min. 11 % · total ≤ 13,5 % vol.',
    'note': 'Le nom d’un des sept climats peut suivre l’appellation (« Chablis Grand Cru Les Clos »).',
    'desc': 'Un seul coteau exposé sud-ouest face à la ville, sur marnes kimméridgiennes : chardonnays amples et profonds, '
            'd’une grande tension minérale, faits pour la garde.',
    'crusTitle': 'Les 7 climats', 'crus': ['Blanchot', 'Bougros', 'Grenouilles', 'Les Clos', 'Preuses', 'Valmur', 'Vaudésir']}
D['appelMeta']['Chablis 1er Cru'] = {
    'colors': ['W'], 'communes': ['Beine', 'Chablis', 'Chichée', 'Courgis', 'Fleys', 'Fontenay-près-Chablis', 'La Chapelle-Vaupelteigne', 'Maligny'],
    'year_note': 'AOC Chablis (1938), mention « premier cru » · 40 climats',
    'grapes': CW, 'yield': 'Blanc : 58 hl/ha (butoir 73)', 'abv': 'Titre naturel min. 10,5 % · total ≤ 13,5 % vol.',
    'note': 'Le nom du climat principal (porte-drapeau) peut couvrir tous les climats de son groupe.',
    'desc': 'Les meilleurs coteaux des deux rives du Serein, de part et d’autre des grands crus : chardonnays plus tendus '
            'que le Chablis, minéraux et de bonne garde.',
    'crusTitle': '17 porte-drapeaux (40 climats)',
    'crus': ['Beauroy', 'Berdiot', 'Chaume de Talvat', 'Côte de Jouan', 'Côte de Léchet', 'Côte de Vaubarousse', 'Fourchaume',
             'Les Beauregards', 'Les Fourneaux', 'Mont de Milieu', 'Montée de Tonnerre', 'Montmains', 'Vaillons', 'Vau de Vey',
             'Vau Ligneau', 'Vaucoupin', 'Vosgros']}
for c in PC_CODES:
    lst = D['communeAppels'][c]
    if 'Chablis 1er Cru' not in lst:
        lst.insert(1 if lst and lst[0] == 'Chablis Grand Cru' else 0, 'Chablis 1er Cru')
s = s[:j] + json.dumps(D, ensure_ascii=False, separators=(',', ':')) + s[end:]

# ---------- 2. card markup, styles and script
def rep(old, new):
    global s
    if new in s: return
    assert s.count(old) == 1, old[:70]
    s = s.replace(old, new)

rep('    <div class="hint" id="hint">',
    '    <div id="readout" class="has-card" style="display:none;">\n'
    '      <p class="ro-eyebrow" id="ro-eyebrow">Appellation sélectionnée</p>\n'
    '      <span class="ro-close" id="ro-close" aria-label="Fermer">×</span>\n'
    '      <div class="ro-card" id="ro-card"></div>\n'
    '    </div>\n    <div class="hint" id="hint">')
CSS = ('/* selected-appellation card (same as the Côte-d\'Or map) + climats chips */\n'
       '  #readout{position:absolute;top:70px;right:16px;z-index:650;width:320px;max-width:calc(100% - 32px);max-height:calc(100% - 90px);overflow-y:auto;'
       'background:rgba(247,242,231,.98);border:1px solid var(--gold);border-top:3px solid var(--bordeaux);border-radius:3px;'
       'padding:14px 16px;box-shadow:0 12px 30px rgba(43,19,22,.22);}\n'
       '  #readout .ro-eyebrow{font-family:ui-sans-serif,system-ui,sans-serif;text-transform:uppercase;letter-spacing:.22em;font-size:9.5px;color:var(--slate);margin:0 0 9px;padding-right:18px;}\n'
       '  #readout .ro-close{position:absolute;top:9px;right:12px;cursor:pointer;color:var(--slate);font-size:20px;line-height:1;padding:2px 5px;border-radius:2px;}\n'
       '  #readout .ro-close:hover{background:rgba(106,20,38,.12);color:var(--bordeaux);}\n'
       '  html[data-theme="cream"] #readout{border:1px solid #9a6a1f;border-top:3px solid rgba(90,30,40,0.18);box-shadow:0 12px 30px rgba(90,40,30,0.07)}\n'
       '  .ro-card .cru-block{margin-top:10px;padding-top:9px;border-top:1px dotted #c9b78a;}\n'
       '  .ro-card .cru-list{display:flex;flex-wrap:wrap;gap:3px;margin-top:5px;}\n'
       '  .ro-card .cru{font-family:ui-sans-serif,system-ui,sans-serif;font-size:9.5px;line-height:1.3;padding:2px 6px;'
       'background:rgba(106,20,38,.06);border:.5px solid rgba(201,162,75,.55);border-radius:3px;color:var(--ink);white-space:nowrap;}\n'
       '  html[data-theme="cream"] .ro-card .cru-block{border-top:1px dotted #9a6a1f}\n'
       '  html[data-theme="cream"] .ro-card .cru{background:rgba(255,253,248,0.61);border:.5px solid rgba(154,106,31,0.66)}\n')
k = s.find('</style>')
if '#readout{' not in s: s = s[:k] + CSS + s[k:]

# climats chips in the fiche (used by the info-detail popup and the card)
rep("    if(m.desc) h+='<div class=\"tip-desc\">'+m.desc+'</div>';\n    if(m.communes&&m.communes.length)",
    "    if(m.desc) h+='<div class=\"tip-desc\">'+m.desc+'</div>';\n"
    "    if(m.crus&&m.crus.length) h+='<div class=\"cru-block\"><div class=\"tip-k\">'+(m.crusTitle||'Climats')+'</div><div class=\"cru-list\">'+"
    "m.crus.map(function(c){return '<span class=\"cru\">'+c+'</span>';}).join('')+'</div></div>';\n    if(m.communes&&m.communes.length)")
# show / hide the card with the appellation highlight
rep("function clearHighlight(){ if(FOCUS_CODES) setFocus(null);",
    "function showReadout(name){ var ro=document.getElementById('readout'); if(!ro||!APPEL_META[name]) return;\n"
    "    document.getElementById('ro-card').innerHTML=tipHTML(name)+(typeof fwPlanLink==='function'?fwPlanLink(name):'');\n"
    "    ro.style.display='block'; ro.scrollTop=0; }\n"
    "  function hideReadout(){ var ro=document.getElementById('readout'); if(ro) ro.style.display='none'; }\n"
    "  function clearHighlight(){ hideReadout(); if(FOCUS_CODES) setFocus(null);")
rep("    var set=APPEL_CODES[name]; if(!set) return;\n    setFocus(set);",
    "    var set=APPEL_CODES[name]; if(!set) return;\n    setFocus(set); showReadout(name);")
# a click on an appellation in a commune's list: the card replaces the popup (as on the Côte-d'Or map)
rep("li.addEventListener('click',function(ev){ ev.stopPropagation(); highlightAppel(li.dataset.appel); }); }); }",
    "li.addEventListener('click',function(ev){ ev.stopPropagation(); var a=li.dataset.appel; hideTip(); highlightAppel(a); }); }); }")
rep("document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&FOCUS_CODES) clearHighlight(); });",
    "document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&FOCUS_CODES) clearHighlight(); });\n"
    "  document.getElementById('ro-close').addEventListener('click',function(){ clearHighlight(); });")
open(F, 'w', encoding='utf-8').write(s)
print('ok', F)
