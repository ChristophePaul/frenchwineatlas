#!/usr/bin/env python3
"""Rhône septentrional map: drop the Beaujolais / Côte roannaise / Côtes du Forez part (2026-10-14).

They have their own maps. Keeps only the 19 southernmost communes of the Rhône département
(the 10 needed for Côte-Rôtie + Condrieu and a band of 9 more so the département visibly continues north),
and, in the Loire département, its 5 Rhône-side appellation communes (Vérin, Saint-Michel-sur-Rhône, Chavanay,
Malleval, Saint-Pierre-de-Bœuf) + the Pilat communes within ~12 km + the southern strip down to the Ardèche;
removes Beaujolais + crus, Crémant de Bourgogne, Côte roannaise, Côtes du Forez from the data, clips
contours/rivers to the remaining communes, redraws the Rhône outline along its real borders only (the
northern cut edge stays open) and moves the RHÔNE label onto the kept area. Needs shapely.

Usage (from WEB Site/):  python3 assets/rhone_sept_trim_apply.py Rhone-septentrional.html
"""
import json, sys
from shapely.geometry import shape, mapping
from shapely.ops import unary_union
from shapely.validation import make_valid

CUT_LAT = 45.608          # Rhône (69) communes whose centroid lies south of this are kept (19 communes)
LOIRE_KM = 12             # Loire (42): keep communes within this distance of its appellation communes…
LOIRE_SOUTH = (45.36, 4.45)   # …and those south of this latitude and east of this longitude (link to the Ardèche)
DROP = {'Beaujolais', 'Brouilly', 'Côte de Brouilly', 'Juliénas', 'Régnié', 'Chénas', 'Moulin-à-Vent', 'Chiroubles',
        'Fleurie', 'Morgon', 'Saint-Amour', 'Crémant de Bourgogne', 'Côte roannaise', 'Côtes du Forez'}


def sh(f): return make_valid(shape(f['geometry'])).buffer(0)
def cy(f): return shape(f['geometry']).centroid.y
def r5(o):
    if isinstance(o, float): return round(o, 5)
    if isinstance(o, (list, tuple)): return [r5(x) for x in o]
    return o
def lines(h):
    if h.geom_type in ('LineString', 'MultiLineString'): return h
    ls = [x for x in getattr(h, 'geoms', []) if x.geom_type in ('LineString', 'MultiLineString')]
    return unary_union(ls) if ls else None


def trim(path):
    s = open(path, encoding='utf-8').read()
    i = s.find('window.MAPDATA='); j = s.find('{', i); md, end = json.JSONDecoder().raw_decode(s[j:])
    F = md['communes']['features']
    n69 = sum(1 for f in F if f['properties']['dep'] == '69'); n42 = sum(1 for f in F if f['properties']['dep'] == '42')
    if n69 < 30 and n42 < 100:
        print('skip (already trimmed)', path); return
    removed = {f['properties']['code'] for f in F if f['properties']['dep'] == '69' and cy(f) > CUT_LAT}
    # Loire: appellation communes (after dropping Roannais / Forez) + Pilat neighbours + southern strip
    def has_aoc(c): return any(a not in DROP for a in md['communeAppels'].get(c, []))
    L42 = [f for f in F if f['properties']['dep'] == '42']
    core = unary_union([sh(f) for f in L42 if has_aoc(f['properties']['code'])])
    deg = LOIRE_KM / (111 * 0.7022)                     # km → degrees of longitude at ~45.4°N
    for f in L42:
        c = shape(f['geometry']).centroid
        near = c.distance(core) <= deg
        south = c.y < LOIRE_SOUTH[0] and c.x > LOIRE_SOUTH[1]
        if not (near or south): removed.add(f['properties']['code'])
    md['communes']['features'] = [f for f in F if f['properties']['code'] not in removed]
    ca = {}
    for c, l in md['communeAppels'].items():
        if c in removed: continue
        l = [a for a in l if a not in DROP]
        if l: ca[c] = l
    md['communeAppels'] = ca
    # colour only communes that still carry an appellation on this map
    for k in ('communeFill', 'communeTop'):
        md[k] = {c: v for c, v in md[k].items() if c in ca and md['communeTop'].get(c) not in DROP}
    for x in md['fillLegend']:
        x['count'] = sum(1 for v in md['communeTop'].values() if v == x['name'])
    md['fillLegend'] = [x for x in md['fillLegend'] if x['name'] not in DROP]
    md['appelMeta'] = {k: v for k, v in md['appelMeta'].items() if k not in DROP}
    md['appelOrder'] = [a for a in md['appelOrder'] if a not in DROP]
    md['aoc'] = [c for c in md['aoc'] if c not in removed]
    area = unary_union([sh(f) for f in md['communes']['features']]).buffer(0.004)
    for key in ('contours', 'rivers'):
        out = []
        for f in md[key]['features']:
            g = shape(f['geometry'])
            if g.within(area): out.append(f); continue
            h = g.intersection(area)
            if h.is_empty: continue
            h = lines(h)
            if h is None or h.is_empty: continue
            gm = mapping(h); out.append({**f, 'geometry': {'type': gm['type'], 'coordinates': r5(gm['coordinates'])}})
        md[key]['features'] = out
    # outlines of the two trimmed départements: real borders only, the cut edges stay open
    for dep in ('69', '42'):
        kept = unary_union([sh(f) for f in md['communes']['features'] if f['properties']['dep'] == dep])
        for f in md['departements']['features']:
            if f['properties']['code'] == dep and f['geometry']['type'] in ('Polygon', 'MultiPolygon'):
                gm = mapping(lines(make_valid(shape(f['geometry'])).boundary.intersection(kept.buffer(0.003))))
                f['geometry'] = {'type': gm['type'], 'coordinates': r5(gm['coordinates'])}
    # département names onto the kept areas, clear of the crus (69: northern band; 42: Pilat west of the vineyards)
    spots = {'69': [f for f in md['communes']['features'] if f['properties']['dep'] == '69' and cy(f) > 45.55],
             '42': [f for f in md['communes']['features'] if f['properties']['dep'] == '42'
                    and not md['communeAppels'].get(f['properties']['code']) and shape(f['geometry']).centroid.x < 4.66]}
    for d in md['deptLabels']:
        if d['code'] in spots and spots[d['code']]:
            pt = unary_union([sh(f) for f in spots[d['code']]]).representative_point()
            d['lat'], d['lng'] = round(pt.y, 5), round(pt.x, 5)
    s = s[:j] + json.dumps(md, ensure_ascii=True, separators=(',', ':')) + s[j + end:]
    open(path, 'w', encoding='utf-8').write(s)
    print('ok', path, len(md['communes']['features']), 'communes')


for p in sys.argv[1:]:
    trim(p)
