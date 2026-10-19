#!/usr/bin/env python3
"""Add the Coteaux du Lyonnais AOC to the Beaujolais map and rename it
« Vignobles du Beaujolais et du Lyonnais » (2026-10-14).

Source: cahier des charges « Coteaux du Lyonnais », décret n° 2011-1083 du 8 septembre 2011
(AOC initialement reconnue par le décret du 9 mai 1984). Aire géographique: 49 communes of the Rhône
in the CDC = 48 communes today (Chassagny and Saint-Andéol-le-Château are both in Beauvallon since 2018).

Adds the appellation (communes + fiche), a « Coteaux du Lyonnais » region button, a sage-green base fill
+ legend row, and renames <title>/<h1>. Usage (from WEB Site/):
    python3 assets/beaujolais_lyonnais_apply.py "Bourgogne Regions/Beaujolais.html"
Skips a page that already has the appellation.
"""
import json, sys

NAME = 'Coteaux du Lyonnais'
# insee codes of the INAO delimitation (2026-06-15 shapefile, app = Coteaux du Lyonnais) — same 48 as the CDC list
CODES = ["69021", "69022", "69028", "69043", "69046", "69049", "69051", "69057", "69059", "69067", "69072", "69076",
         "69083", "69086", "69091", "69094", "69096", "69100", "69112", "69116", "69117", "69125", "69127", "69131",
         "69133", "69136", "69141", "69148", "69153", "69154", "69171", "69175", "69177", "69179", "69190", "69194",
         "69200", "69207", "69216", "69219", "69231", "69236", "69241", "69249", "69250", "69255", "69260", "69268"]
META = {
    "year": 1984,
    "year_note": "AOC reconnue par décret du 9 mai 1984 · cahier des charges : décret du 8 septembre 2011",
    "colors": ["R", "RO", "W"],
    "codes": CODES,
    "grapes": {"red": [["Gamay N"], ["Gamay de Bouze N", "Gamay de Chaudenay N"]],
               "white": [["Aligoté B", "Chardonnay B"], ["Pinot Blanc B"]]},
    "communes_doc": 48,
    "yield": "60 hl/ha (butoir : rouge et rosé 69, blanc 72 hl/ha)",
    "desc": "Les coteaux de l'ouest et du sud-ouest de Lyon, entre le Beaujolais et les Côtes du Rhône : "
            "rouges et rosés de gamay, blancs de chardonnay et d'aligoté.",
    "mention": "« Primeur » / « Nouveau » autorisée (récolte de l'année)",
}
FILL = '#9db07f'          # sage green, distinct from the Beaujolais rose and the Bourgogne cream
REPS = [
    ('<title data-fr="Vignobles du Beaujolais — Carte des appellations" data-en="Beaujolais Vineyards — Appellation Map">'
     'Vignobles du Beaujolais — Carte des appellations</title>',
     '<title data-fr="Vignobles du Beaujolais et du Lyonnais — Carte des appellations" '
     'data-en="Beaujolais &amp; Lyonnais Vineyards — Appellation Map">'
     'Vignobles du Beaujolais et du Lyonnais — Carte des appellations</title>'),
    ('<h1>Vignobles du Beaujolais</h1>', '<h1>Vignobles du Beaujolais et du Lyonnais</h1>'),
    ('<p class="eyebrow">Rhône &amp; Saône-et-Loire · Auvergne-Rhône-Alpes</p>',
     '<p class="eyebrow">Rhône &amp; Saône-et-Loire · Beaujolais &amp; Lyonnais</p>'),
    ('const BEAUJO=new Set(), BOURG=new Set();',
     'const BEAUJO=new Set(), BOURG=new Set(), LYON=new Set(appellations["Coteaux du Lyonnais"]||[]);'),
    ('if(BOURG.has(code))return ["#efdfbb",1]; return ["#efe7d4",1]; }',
     'if(BOURG.has(code))return ["#efdfbb",1]; if(LYON.has(code))return ["' + FILL + '",0.6]; return ["#efe7d4",1]; }'),
    ('Beaujolais &amp; Bourgogne</div><div class="al-row"><span class="al-sw" style="background:#efe7d4"></span>',
     'Beaujolais &amp; Bourgogne</div><div class="al-row"><span class="al-sw" style="background:rgba(157,176,127,.6)">'
     '</span>Coteaux du Lyonnais</div><div class="al-row"><span class="al-sw" style="background:#efe7d4"></span>'),
]

for path in sys.argv[1:]:
    s = open(path, encoding='utf-8').read()
    i = s.find('window.MAPDATA'); j = s.find('{', i); md, end = json.JSONDecoder().raw_decode(s[j:])
    if NAME in md['appellations']:
        print('skip (already added)', path); continue
    have = {f['properties']['code'] for f in md['communes']['features']}
    miss = [c for c in CODES if c not in have]
    if miss:
        sys.exit('%s: communes missing from the map: %s' % (path, miss))
    md['appellations'][NAME] = CODES
    md['meta'][NAME] = META
    md['groups'][NAME] = [NAME]
    s = s[:j] + json.dumps(md, ensure_ascii=False, separators=(',', ':')) + s[j + end:]
    for a, b in REPS:
        if s.count(a) != 1:
            sys.exit('%s: expected exactly one match for %r (found %d)' % (path, a[:60], s.count(a)))
        s = s.replace(a, b)
    open(path, 'w', encoding='utf-8').write(s)
    print('ok', path)
