"""Builds « Placez l'AOC » / "Pin the AOC" — Infos/Literature/Map_Game.html + map_game_data.js.
Geography comes from GeoJson Files/MapGame/game_geo.json (python3 build_geo.py there, slow);
this script only adds levels, links, towns and writes the page. Run:  python3 gen_map_game.py
"""
import glob
import json
import os
import re
import unicodedata
import urllib.parse
from pathlib import Path

from shapely.geometry import Polygon

import gen_games  # noqa: F401  (sets sys.path for base_css / quiz_bank)
from gen_games import base_css, quiz_bank, OUTDIR, HERE

WEB = HERE.parent.parent.parent
GEO = WEB.parent / 'GeoJson Files' / 'MapGame' / 'game_geo.json'

SPIRITS = {'Cognac': (1, '../../Cognac.html'), 'Armagnac': (2, '../../South-West%20Toulouse.html')}

# 15 main cities (always shown) + wine towns (levels 1–2, zoomed in). A town whose name is part of the
# AOC being asked (Beaune, Cognac, Bordeaux…) is hidden for that question by the page.
MAIN = [('Paris', 48.857, 2.352), ('Reims', 49.258, 4.032), ('Strasbourg', 48.573, 7.752), ('Dijon', 47.322, 5.041),
        ('Lyon', 45.764, 4.836), ('Avignon', 43.949, 4.806), ('Marseille', 43.296, 5.370), ('Nice', 43.710, 7.262),
        ('Montpellier', 43.611, 3.877), ('Perpignan', 42.699, 2.895), ('Toulouse', 43.605, 1.444), ('Bordeaux', 44.838, -0.579),
        ('Nantes', 47.218, -1.554), ('Tours', 47.394, 0.685), ('Ajaccio', 41.919, 8.739)]
SECOND = [('Épernay', 49.040, 3.959), ('Troyes', 48.297, 4.074), ('Colmar', 48.079, 7.358), ('Mulhouse', 47.750, 7.336),
          ('Metz', 49.119, 6.176), ('Nancy', 48.692, 6.184), ('Auxerre', 47.798, 3.567), ('Beaune', 47.025, 4.837),
          ('Chalon-sur-Saône', 46.781, 4.854), ('Mâcon', 46.307, 4.828), ('Villefranche-sur-Saône', 45.990, 4.718),
          ('Vienne', 45.525, 4.874), ('Valence', 44.933, 4.892), ('Orange', 44.138, 4.807), ('Nîmes', 43.837, 4.360),
          ('Béziers', 43.344, 3.216), ('Narbonne', 43.184, 3.004), ('Carcassonne', 43.213, 2.351), ('Toulon', 43.124, 5.928),
          ('Aix-en-Provence', 43.529, 5.447), ('Bastia', 42.697, 9.451), ('Pau', 43.295, -0.370), ('Bayonne', 43.493, -1.475),
          ('Bergerac', 44.853, 0.483), ('Cahors', 44.448, 1.441), ('Agen', 44.203, 0.616), ('Albi', 43.929, 2.148),
          ('Libourne', 44.915, -0.244), ('Angers', 47.478, -0.563), ('Saumur', 47.260, -0.077), ('Orléans', 47.903, 1.909),
          ('Bourges', 47.081, 2.399), ('Clermont-Ferrand', 45.778, 3.087), ('Chambéry', 45.564, 5.918), ('Annecy', 45.899, 6.129),
          ('Lons-le-Saunier', 46.675, 5.555), ('Besançon', 47.238, 6.024), ('Cognac', 45.696, -0.329), ('Angoulême', 45.650, 0.156),
          ('La Rochelle', 46.160, -1.151), ('Poitiers', 46.580, 0.340), ('Limoges', 45.834, 1.262), ('Rodez', 44.350, 2.575),
          ('Auch', 43.646, 0.586), ('Mont-de-Marsan', 43.890, -0.500), ('Grenoble', 45.188, 5.724), ('Saint-Étienne', 45.434, 4.390),
          ('Roanne', 46.036, 4.068), ('Moulins', 46.566, 3.333), ('Nevers', 46.990, 3.159), ('Blois', 47.586, 1.335),
          ('Laval', 48.073, -0.770), ('Le Mans', 48.006, 0.199), ('Lorient', 47.748, -3.367), ('Rennes', 48.117, -1.678),
          ('Lille', 50.629, 3.057), ('Rouen', 49.443, 1.099), ('Caen', 49.183, -0.370), ('Brest', 48.390, -4.486)]


# ---- link to the parcel map (same rules as WEB Site/plan_links_apply.py) ----
def slug(s):
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-').lower()


PLANS = {os.path.basename(p)[:-5].lower(): '../../Plan%20Cadastraux/' + urllib.parse.quote(os.path.basename(os.path.dirname(p))) + '/' + urllib.parse.quote(os.path.basename(p))
         for p in sorted(glob.glob(str(WEB / 'Plan Cadastraux' / '*' / '*.html')))}
PLAN_ALIAS = {'Clairette de Die': 'diois', 'Crémant de Die': 'diois', 'Coteaux de Die': 'diois', 'Châtillon-en-Diois': 'diois',
              'Anjou Brissac': 'anjou-villages-brissac', 'Pouilly-Fumé': 'pouilly-fume', 'Pouilly-sur-Loire': 'pouilly-fume',
              'Côtes de Bergerac': 'bergerac', 'Côtes de Montravel': 'montravel', 'Haut-Montravel': 'montravel',
              'Saint-Émilion Grand Cru': 'saint-emilion', 'Graves Supérieures': 'graves', 'Corrèze': 'correze',
              'Coulée de Serrant': 'coulee-de-serrant', 'Boutenac': 'boutenac', 'La Livinière': 'la-liviniere', 'Champagne': 'champagne-grands-crus'}


def plan_of(name):
    if name in PLAN_ALIAS and PLAN_ALIAS[name] in PLANS:
        return PLANS[PLAN_ALIAS[name]]
    if name.startswith('Alsace Grand Cru'):
        return PLANS.get('alsace-grands-crus')
    return PLANS.get(slug(name))


def water():
    """Gironde estuary, taken from the Bordeaux region map (commune outlines run to mid-estuary, so the land fill hides it)."""
    s = (WEB / 'Bordeaux.html').read_text(encoding='utf-8')
    i = s.index('window.MAPDATA=') + len('window.MAPDATA=')
    est = json.JSONDecoder().raw_decode(s, i)[0]['estuary']
    feats = est['features'] if 'features' in est else [est]
    out = []
    for f in feats:
        g = f['geometry']
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
        for poly in polys:
            for ring in poly:
                out.append([[round(x, 4), round(y, 4)] for x, y in ring])
    return out


def main():
    geo = json.load(open(GEO))
    acom = json.load(open(GEO.parent / 'aoc_communes.json'))
    aocs, missing_plan = [], []
    for a in quiz_bank.AOCS:
        n = a['name']
        p = plan_of(n)
        if not p:
            missing_plan.append(n)
        aocs.append(dict(n=n, r=a['region'], lv=quiz_bank.level_of(n), card=quiz_bank.cep_link(n), plan=p, src=geo['src'][n], c=acom[n]))
    for n, (lv, card) in SPIRITS.items():
        region = 'Charentes' if n == 'Cognac' else 'Sud-Ouest'
        aocs.append(dict(n=n, r=region, lv=lv, card=card, plan=None, src=geo['src'][n], c=acom[n], sp=1))
    regions = sorted({a['r'] for a in aocs}, key=lambda r: slug(r))
    labels = {}
    for r, rings in geo['regions'].items():
        big = max((Polygon(x) for x in rings), key=lambda p: p.area)
        c = big.representative_point() if not big.contains(big.centroid) else big.centroid
        labels[r] = [round(c.x, 3), round(c.y, 3)]
    towns = [[n, la, lo, 1] for n, la, lo in MAIN] + [[n, la, lo, 2] for n, la, lo in SECOND]
    data = dict(aocs=aocs, shapes=geo['aocs'], regions=geo['regions'], regionLabels=labels, regionList=regions,
                regions_en={r: quiz_bank.REGION_EN.get(r, r) for r in regions},
                water=water(), deptBoxes=json.load(open(GEO.parent / 'dept_boxes.json')),
                depts=geo['depts'], france=geo['france'], rivers=geo['rivers'], towns=towns)
    js = ('/* GENERATED by Infos/_source/games/gen_map_game.py — do not edit by hand. */\n'
          'window.MAPGAME = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n')
    (OUTDIR / 'map_game_data.js').write_text(js)
    html = ((HERE / 'map_template.html').read_text()
            .replace('@@BASE_CSS@@', base_css())
            .replace('@@LEAFLET_CSS@@', (HERE / 'leaflet_css.txt').read_text())
            .replace('@@LEAFLET_JS@@', (HERE / 'leaflet_js.txt').read_text()))
    assert '@@' not in html.replace('@preserve', ''), html[html.index('@@'):html.index('@@') + 40]
    (OUTDIR / 'Map_Game.html').write_text(html)
    by_lv = {k: sum(1 for a in aocs if a['lv'] <= k) for k in (1, 2, 3)}
    print(f'map_game_data.js: {len(js) / 1e6:.2f} MB, {len(aocs)} AOCs (pools {by_lv}); no parcel map for {len(missing_plan)}: {missing_plan}')


if __name__ == '__main__':
    main()
