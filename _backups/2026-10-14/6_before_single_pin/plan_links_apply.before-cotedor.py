#!/usr/bin/env python3
"""Add an « Accéder au plan cadastral → » button to the AOC detail popups of every
region map that has a matching page in Plan Cadastraux/ (same style as Alsace.html's
grand cru card). Idempotent: rerun after adding plan pages or rebuilding a map.
"""
import json, os, re, glob, unicodedata, urllib.parse

ROOT = os.path.dirname(os.path.abspath(__file__))
PLANS = os.path.join(ROOT, 'Plan Cadastraux')

def slug(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-').lower()

# slug of plan file -> relative href
INDEX = {}
for p in sorted(glob.glob(os.path.join(PLANS, '*', '*.html'))):
    folder, fn = os.path.basename(os.path.dirname(p)), os.path.basename(p)
    INDEX[fn[:-5].lower()] = 'Plan%20Cadastraux/' + urllib.parse.quote(folder) + '/' + urllib.parse.quote(fn)

# popup name -> plan file stem, where the plain slug does not match
ALIAS = {
    'Anjou Brissac': 'Anjou-Villages-Brissac',
    'Pouilly-Fumé ou Blanc Fumé de Pouilly': 'Pouilly-Fume',
    'Pouilly-sur-Loire': 'Pouilly-Fume',          # identical INAO area, shared page
    'Vin de Corse ou Corse Figari': 'Vin-de-Corse-Figari',
    'Côtes de Bergerac': 'Bergerac',              # same area as Bergerac
    'Côtes de Montravel': 'Montravel', 'Haut-Montravel': 'Montravel',
    'Corrèze Coteaux de la Vézère': 'Correze', 'Corrèze vin de paille': 'Correze',
    'Côtes de Bordeaux Blaye': 'Blaye-Cotes-de-Bordeaux',
    'Côtes de Bordeaux Cadillac': 'Cadillac-Cotes-de-Bordeaux',
    'Côtes de Bordeaux Castillon': 'Castillon-Cotes-de-Bordeaux',
    'Côtes de Bordeaux Francs': 'Francs-Cotes-de-Bordeaux',
    'Côtes de Bordeaux Sainte-Foy': 'Sainte-Foy-Cotes-de-Bordeaux',
    'Saint-Émilion Grand Cru': 'Saint-Emilion',
    'Graves Supérieures': 'Graves',
    'Bordeaux Haut-Benauge': 'Entre-deux-Mers-Haut-Benauge',
    'Clairette de Die': 'Diois', 'Crémant de Die': 'Diois', 'Coteaux de Die': 'Diois',   # one INAO area, one page
    'Châtillon-en-Diois': 'Diois',
    'Beaujolais (régionale)': 'Beaujolais',          # Beaujolais map label of the regional AOC
}

def resolve(name):
    if name in ALIAS: return INDEX.get(ALIAS[name].lower())
    if name.startswith('Alsace Grand Cru '): name = name[len('Alsace Grand Cru '):]
    if name.startswith('Fiefs Vendéens'): name = 'Fiefs Vendéens'
    return INDEX.get(slug(name.split(' ou ')[0]))

def names(s, key):
    i = s.find(key)
    if i < 0: return []
    j = i + len(key)
    while s[j] in ' \n\t': j += 1
    return list(json.JSONDecoder().raw_decode(s, j)[0])

CSS = """
.fw-plan-link{display:flex;align-items:center;justify-content:center;gap:8px;margin:10px 0 2px;padding:8px 12px;border-radius:6px;
  background:#6a1426;color:#f3ecdd!important;border:1px solid #c9a24b;text-decoration:none!important;font-family:ui-sans-serif,system-ui,sans-serif;
  font-size:12px;font-weight:600;letter-spacing:.03em;box-shadow:0 3px 10px rgba(106,20,38,.22);transition:background .15s;cursor:pointer;
  position:sticky;bottom:0;z-index:2;}
.fw-plan-link span{color:#c9a24b;font-size:15px;line-height:1;transition:transform .15s;}
.fw-plan-link:hover{background:#86192f;}
.fw-plan-link:hover span{transform:translateX(3px);}
html[data-theme="cream"] .fw-plan-link{box-shadow:0 3px 10px rgba(90,40,30,0.07)}
html[data-theme="cream"] .fw-plan-link span{color:#8a5d17}
"""

def block(links):
    js = ('var FW_PLAN_LINKS=' + json.dumps(links, ensure_ascii=False, sort_keys=True) + ';\n'
          'function fwPlanLink(n){var h=FW_PLAN_LINKS[n];if(!h)return "";'
          'var en=/^en/i.test(document.documentElement.lang||"");'
          'return \'<a class="fw-plan-link" href="\'+h+\'">\'+(en?"Access the parcel map":"Accéder au plan cadastral")'
          '+\' <span aria-hidden="true" style="color:#c9a24b">→</span></a>\';}')
    return ('<!-- fw-plan-links:start -->\n<style id="fw-plan-links-css">' + CSS + '</style>\n'
            '<script id="fw-plan-links">\n' + js + '\n</script>\n<!-- fw-plan-links:end -->\n')

# showDetail patches (old -> new); every page has exactly one of these
PATCHES = [
    ("detail.innerHTML='<div class=\"ro-card\">'+tipHTML(appel)+'</div>';",
     "detail.innerHTML='<div class=\"ro-card\">'+tipHTML(appel)+'</div>'+fwPlanLink(appel);"),
    # Bordeaux: hover detail panel + selected-appellation readout
    ("detail.innerHTML='<div class=\"tip-card\">'+inner+'</div>';",
     "detail.innerHTML='<div class=\"tip-card\">'+inner+'</div>'+fwPlanLink(appel);"),
    ("'<div class=\"ro-communes\">'+n+' commune'+(n>1?'s':'')+' dans l\\'aire géographique.</div>', true);",
     "'<div class=\"ro-communes\">'+n+' commune'+(n>1?'s':'')+' dans l\\'aire géographique.</div>'+fwPlanLink(name), true);"),
]

report = []
# region maps in a sub-folder (same Bordeaux-style template) get their plan hrefs prefixed with ../
SUBPAGES = [os.path.join(ROOT, 'Bourgogne Regions', 'Beaujolais.html'), os.path.join(ROOT, 'Bourgogne Regions', 'Saone-et-Loire.html')]
for f in sorted(glob.glob(os.path.join(ROOT, '*.html'))) + SUBPAGES:
    s = open(f, encoding='utf-8').read()
    ns = names(s, '"appelMeta":') or names(s, '"appellations":')
    if not ns: continue
    up = '../' * (os.path.relpath(f, ROOT).count(os.sep))
    links = {n: up + resolve(n) for n in ns if resolve(n)}
    s = re.sub(r'<!-- fw-plan-links:start -->.*?<!-- fw-plan-links:end -->\n', '', s, flags=re.S)
    patched = 0
    for old, new in PATCHES:
        if new in s: patched += 1
        elif old in s: s = s.replace(old, new, 1); patched += 1
    if links:
        s = s.replace('</head>', block(links) + '</head>', 1)
    elif patched:  # helper must exist even with no plans
        s = s.replace('</head>', block({}) + '</head>', 1)
    open(f, 'w', encoding='utf-8').write(s)
    miss = [n for n in ns if n not in links]
    report.append((os.path.basename(f), len(links), len(ns), patched, miss))

for fn, k, t, p, miss in report:
    print(f'{fn}: {k}/{t} linked, {p} popup(s) patched')
    if miss: print('   no plan:', ' | '.join(miss))
