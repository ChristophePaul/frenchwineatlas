"""Region maps: add the AOCs that were missing from every regional map, and apply official renamings.

Added (audit 2026-10-13 against the INAO parcel file 2026-06-15):
  - Pineau des Charentes  → Cognac.html                         (régionale overlay: same communes as the Cognac area)
  - Floc de Gascogne      → South-West Toulouse.html (Gers), Landes_et_Pyrenees_Occidentales.html, South West Bergerac.html
  - Duché d'Uzès          → Rhone-meridional.html               (own fill; 87 Gard communes added to the map)
  - Haut-Poitou           → Anjou_et_de_Touraine.html           (own fill; Vienne/Deux-Sèvres communes + Vienne outline added)
  - Laudun (Rhone-meridional.html) gets its full card (cru 2024).
Renamed (INAO names): Corbières-Boutenac → Boutenac, Minervois-la-Livinière → La Livinière, label Anjou-Villages Brissac → Anjou Brissac.

Commune lists: GeoJson Files/MapGame/aoc_communes.json (INAO rows / CDC commune lists, today's INSEE codes).
Commune outlines: GeoJson Files/communes.geojson. Facts: the AOCs' cahiers des charges (Cahiers des Charges/…).
Idempotent. Rerun after rebuilding any of these maps, then  python3 assets/i18n_build.py.

Run:  python3 assets/region_aoc_additions.py
"""
import json
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
GEO = SITE.parent / 'GeoJson Files'
AC = json.load(open(GEO / 'MapGame' / 'aoc_communes.json', encoding='utf-8'))
_COM = None


def communes_geo():
    global _COM
    if _COM is None:
        _COM = {f['properties']['code']: f for f in json.load(open(GEO / 'communes.geojson', encoding='utf-8'))['features']}
    return _COM


def load(page):
    s = (SITE / page).read_text(encoding='utf-8')
    m = re.search(r'MAPDATA\s*=\s*', s)
    d, end = json.JSONDecoder().raw_decode(s[m.end():])
    return s, m.end(), m.end() + end, d


def save(page, s, a, b, d):
    (SITE / page).write_text(s[:a] + json.dumps(d, ensure_ascii=False) + s[b:], encoding='utf-8')


def ensure_communes(d, codes):
    have = {f['properties']['code'] for f in d['communes']['features']}
    geo = communes_geo()
    n = len(d['communes']['features'])
    added = 0
    for c in sorted(codes):
        if c in have or c not in geo:
            continue
        f = geo[c]
        d['communes']['features'].append({'id': 'c%04d' % n, 'type': 'Feature',
                                          'properties': {'code': c, 'nom': f['properties']['nom'], 'dep': c[:2]},
                                          'geometry': f['geometry']})
        n += 1
        added += 1
    return added


def ensure_dept(d, dep, nom):
    if any(f['properties'].get('code') == dep for f in d['departements']['features']):
        return
    from shapely.geometry import shape, mapping
    from shapely.ops import unary_union
    geo = communes_geo()
    u = unary_union([shape(f['geometry']).buffer(0) for c, f in geo.items() if c[:2] == dep]).simplify(0.0008)

    def rnd(o):
        return [rnd(x) for x in o] if isinstance(o, (list, tuple)) and o and isinstance(o[0], (list, tuple)) else [round(o[0], 5), round(o[1], 5)]
    g = mapping(u)
    d['departements']['features'].append({'type': 'Feature', 'properties': {'code': dep, 'nom': nom},
                                          'geometry': {'type': g['type'], 'coordinates': rnd(g['coordinates'])}})


def names_of(d, codes):
    nm = {f['properties']['code']: f['properties']['nom'] for f in d['communes']['features']}
    return sorted({nm[c] for c in codes if c in nm})


def add_aoc(d, name, meta, codes, mode, color, label=None):
    """mode 'regional' = sidebar overlay (blankets other fills); 'fill' = its own colour on the map."""
    codes = [c for c in codes if c in {f['properties']['code'] for f in d['communes']['features']}]
    meta = dict(meta)
    meta['communes'] = names_of(d, codes) if len(codes) <= 40 else []
    d['appelMeta'][name] = meta
    for c in codes:
        lst = d['communeAppels'].setdefault(c, [])
        if name not in lst:
            lst.append(name)
    entry = {'name': name, 'label': label or name, 'color': color, 'count': len(codes)}
    if mode == 'regional':
        rl = d.setdefault('regionalLegend', None) or []
        rl = [x for x in rl if x['name'] != name] + [entry]
        d['regionalLegend'] = rl
    else:
        for c in codes:
            if c not in d['communeFill']:
                d['communeFill'][c] = color
                d['communeTop'][c] = name
        fl = [x for x in (d.get('fillLegend') or []) if x['name'] != name] + [entry]
        d['fillLegend'] = fl
    if d.get('appelOrder') is not None and name not in d['appelOrder']:
        d['appelOrder'].append(name)
    return len(codes)


def rename(d, old, new):
    """Exact-value rename inside the map data structures (not free text)."""
    n = 0
    if old in d.get('appelMeta', {}):
        d['appelMeta'][new] = d['appelMeta'].pop(old); n += 1
    for c, lst in d.get('communeAppels', {}).items():
        for i, a in enumerate(lst):
            if a == old:
                lst[i] = new; n += 1
    for c, a in d.get('communeTop', {}).items():
        if a == old:
            d['communeTop'][c] = new; n += 1
    for key in ('fillLegend', 'regionalLegend'):
        for x in d.get(key) or []:
            if x.get('name') == old:
                x['name'] = new; n += 1
            if x.get('label') == old:
                x['label'] = new; n += 1
    if d.get('appelOrder'):
        d['appelOrder'] = [new if a == old else a for a in d['appelOrder']]
    return n


# ---------------------------------------------------------------- facts (from the cahiers des charges)
PINEAU = {'colors': ['W', 'RO'], 'year_note': 'AOC 1945 (décret du 12 octobre 1945) · vin de liqueur',
          'grapes': {'white': [['Ugni blanc B', 'Colombard B', 'Folle blanche B', 'Montils B', 'Sémillon B', 'Sauvignon B',
                                'Merlot blanc B', 'Jurançon blanc B', 'Meslier Saint-François B'], ['Trousseau gris G (≤ 10 %)']],
                     'red': [['Cabernet franc N', 'Cabernet-Sauvignon N', 'Merlot N', 'Cot N'], []]},
          'yield': '68 hl de moût/ha',
          'abv': 'Vin de liqueur · 16 à 22 % vol. · mutage à l’eau-de-vie de Cognac (≥ 60 % vol.)',
          'note': 'Blanc, rosé ou rouge. Aire : les communes délimitées pour le Cognac (décret de 1909).',
          'desc': 'Vin de liqueur des Charentes : moût de raisin frais muté à l’eau-de-vie de Cognac rassise. Il se décline en blanc (raisins blancs ou rouges) et en rosé ou rouge.'}
FLOC = {'colors': ['W', 'RO'], 'year_note': 'AOC 1990 (décret du 27 novembre 1990) · vin de liqueur',
        'grapes': {'white': [['Colombard B', 'Gros manseng B', 'Ugni blanc B'], ['Baroque B', 'Folle blanche B', 'Mauzac B', 'Petit manseng B',
                                                                                  'Sauvignon B', 'Sauvignon gris G', 'Sémillon B']],
                   'red': [['Cabernet franc N', 'Cabernet-Sauvignon N', 'Cot N', 'Fer N', 'Merlot N', 'Tannat N (≤ 50 %)'], []]},
        'yield': '72 hl de moût/ha',
        'abv': 'Vin de liqueur · 16 à 18 % vol. · mutage à l’Armagnac (≥ 52 % vol.)',
        'note': 'Blanc ou rosé. 285 communes du Gers, des Landes et du Lot-et-Garonne.',
        'desc': 'Vin de liqueur de Gascogne : moût de raisin frais muté à l’Armagnac jeune. Les producteurs se sont regroupés en syndicat en 1976 ; l’AOC date de 1990.'}
UZES = {'colors': ['R', 'RO', 'W'], 'year_note': 'AOC 2013 (cahier des charges homologué le 19 juillet 2013)',
        'grapes': {'red': [['Syrah N (≥ 40 % en rouge)', 'Grenache N (≥ 20 % en rouge)'], ['Carignan N', 'Cinsaut N', 'Mourvèdre N']],
                   'white': [['Viognier B (≥ 40 %)', 'Grenache blanc B (≥ 20 %)'], ['Marsanne B', 'Roussanne B', 'Vermentino B', 'Clairette B', 'Ugni blanc B']]},
        'yield': 'Rouges 48 hl/ha · rosés et blancs 55 hl/ha',
        'note': '87 communes du Gard, autour d’Uzès. Rosés : grenache ≥ 40 % et syrah ≥ 20 % (l’inverse des rouges).',
        'desc': 'Appellation du Gard autour d’Uzès, issue du vin de pays de l’Uzège (puis « Duché d’Uzès », 1992). Rouges à base de syrah et grenache, blancs à base de viognier et grenache blanc.'}
POITOU = {'colors': ['R', 'RO', 'W'], 'year_note': 'AOVDQS 1970 (arrêté du 23 octobre 1970) · AOC 2011',
          'grapes': {'white': [['Sauvignon B', 'Sauvignon gris G'], []],
                     'red': [['Cabernet franc N (≥ 60 %)'], ['Gamay N', 'Pinot noir N', 'Merlot N', 'Cabernet-Sauvignon N']]},
          'yield': 'Blancs 68 hl/ha · rouges et rosés 60 hl/ha',
          'note': '23 communes : 22 dans la Vienne, au nord de Poitiers, et Thénezay (Deux-Sèvres).',
          'desc': 'Petit vignoble du Poitou, au nord de Poitiers : blancs vifs de sauvignon, rouges et rosés à dominante de cabernet franc.'}
LAUDUN = {'colors': ['R', 'W'], 'year_note': 'Cru des Côtes du Rhône 2024 (INAO, 11 septembre 2024) · premier millésime 2024',
          'grapes': {'red': [['Grenache N (≥ 50 %)', 'Syrah N (≥ 25 %)'], ['Mourvèdre N', 'Carignan N', 'Cinsaut N', 'Counoise N', 'Brun argenté N']],
                     'white': [['Clairette B (≥ 25 %)', 'Grenache blanc B (≥ 25 %)'], ['Roussanne B', 'Viognier B']]},
          'note': 'Rouges et blancs uniquement. Auparavant Côtes du Rhône Villages « Laudun » (depuis 1967).',
          'desc': '18e cru des Côtes du Rhône, sur trois communes du Gard (Laudun-l’Ardoise, Saint-Victor-la-Coste, Tresques). Rouges de grenache et syrah ; blancs de clairette et grenache blanc, avec roussanne ou viognier.'}


def main():
    # Cognac — Pineau des Charentes
    s, a, b, d = load('Cognac.html')
    n = add_aoc(d, 'Pineau des Charentes', PINEAU, AC['Pineau des Charentes'], 'regional', '#b8862f')
    save('Cognac.html', s, a, b, d); print('Cognac: Pineau des Charentes', n, 'communes')

    # Floc de Gascogne on the three South-West maps that hold its communes
    for page in ['South-West Toulouse.html', 'Landes_et_Pyrenees_Occidentales.html', 'South West Bergerac.html']:
        s, a, b, d = load(page)
        n = add_aoc(d, 'Floc de Gascogne', FLOC, AC['Floc de Gascogne'], 'regional', '#c98a3a')
        save(page, s, a, b, d); print(page + ': Floc de Gascogne', n, 'communes')

    # Rhône méridional — Duché d'Uzès (+ communes), Laudun card
    s, a, b, d = load('Rhone-meridional.html')
    k = ensure_communes(d, AC["Duché d'Uzès"])
    n = add_aoc(d, "Duché d'Uzès", UZES, AC["Duché d'Uzès"], 'fill', '#8d6b9e')
    meta = dict(LAUDUN); meta['communes'] = d['appelMeta'].get('Laudun', {}).get('communes', [])
    d['appelMeta']['Laudun'] = meta
    save('Rhone-meridional.html', s, a, b, d); print("Rhône méridional: Duché d'Uzès", n, 'communes (', k, 'outlines added) + Laudun card')

    # Anjou-Touraine — Haut-Poitou (+ Vienne communes & outline), Anjou Brissac label
    s, a, b, d = load('Anjou_et_de_Touraine.html')
    k = ensure_communes(d, AC['Haut-Poitou'])
    ensure_dept(d, '86', 'Vienne')
    n = add_aoc(d, 'Haut-Poitou', POITOU, AC['Haut-Poitou'], 'fill', '#6a8f4e')
    r = rename(d, 'Anjou-Villages Brissac', 'Anjou Brissac')
    save('Anjou_et_de_Touraine.html', s, a, b, d); print('Anjou-Touraine: Haut-Poitou', n, 'communes (', k, 'outlines added),', r, 'label renames')

    # Languedoc — official names
    s, a, b, d = load('Languedoc.html')
    r = rename(d, 'Corbières-Boutenac', 'Boutenac') + rename(d, 'Minervois-la-Livinière', 'La Livinière') + rename(d, 'Minervois-La Livinière', 'La Livinière')
    save('Languedoc.html', s, a, b, d); print('Languedoc:', r, 'renames')


if __name__ == '__main__':
    main()
