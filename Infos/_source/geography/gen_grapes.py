"""Builds the grape map « Les cépages de France » — the leading red and white grape of each wine region and sub-region,
on the hydrographic relief map (GeoJson Files/Geography_Rivers/hq), with zoom / pan and click-to-zoom.

Geometry: sub-region = union of AOC outlines (GeoJson Files/MapGame/game_geo.json); region outlines from the same file.
Data: grapes_data.py.   Output (draft, git-ignored): _grapes/Grapes_Map.html + _grapes/img/
Run:  python3 gen_grapes.py
"""
import json
import os
from pathlib import Path

import numpy as np
from PIL import Image
from pyproj import Transformer
from shapely.geometry import MultiPolygon, Polygon, box
from shapely.ops import polylabel, unary_union

import gen_page as GP
import re
import sys
import unicodedata
from grapes_data import REGIONS, SUBS
from common import att

HERE = Path(__file__).resolve().parent
OUT = HERE / '_grapes' / 'Grapes_Map.html'
IMG = OUT.parent / 'img'
GAME = GP.REPO.parent.parent / 'GeoJson Files' / 'MapGame' / 'game_geo.json'
VER = '1'
f, tr = GP.f, GP.tr


# ------------------------------------------------------------------ geometry → stage units
def setup():
    IMG.mkdir(parents=True, exist_ok=True)
    GP.IMG = IMG
    GP.load_geo()                              # GEO: placement, Corsica inset, rivers…
    hq = GP.GEO_DIR.parent
    im = Image.open(hq / 'map_hq.png').convert('RGB')
    im = im.crop((100, 100, im.width - 100, im.height - 100))
    im.resize((3000, round(im.height * 3000 / im.width)), Image.LANCZOS).save(IMG / 'map_rivers.webp', 'WEBP', quality=78, method=6)
    Image.open(hq / 'corsica_hq.png').convert('RGB').save(IMG / 'map_corsica_hq.webp', 'WEBP', quality=82, method=6)


TRF = Transformer.from_crs(4326, 2154, always_xy=True)


def to_stage(ring):
    a = np.asarray(ring, float)
    E, N = TRF.transform(a[:, 0], a[:, 1])
    x, y = GP.l93_stage(np.asarray(E), np.asarray(N))
    if a[:, 0].mean() > 8.3 and a[:, 1].mean() < 43.2:       # Corsica inset
        x = x + GP.GEO['corse_dx']; y = y + GP.GEO['corse_dy']
    return np.c_[x, y]


def shape_of(polys, clip=None):
    """list of [[lon,lat],…] rings (outer only) → shapely geometry in stage units"""
    geoms = []
    for ring in polys:
        if len(ring) < 4:
            continue
        a = np.asarray(ring, float)
        if clip and not (clip[0] <= a[:, 1].mean() <= clip[1]):
            continue
        p = Polygon(to_stage(ring))
        if not p.is_valid:
            p = p.buffer(0)
        geoms.append(p)
    return unary_union(geoms).buffer(.25).buffer(-.25) if geoms else None


def path_of(g, tol=.12):
    g = g.simplify(tol)
    parts = list(g.geoms) if isinstance(g, MultiPolygon) else [g]
    out = []
    for p in parts:
        if p.area < .4:
            continue
        for ring in [p.exterior] + list(p.interiors):
            c = np.asarray(ring.coords)
            out.append('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in c) + 'Z')
    return ''.join(out)


def anchor(g):
    parts = list(g.geoms) if isinstance(g, MultiPolygon) else [g]
    big = max(parts, key=lambda p: p.area)
    pt = polylabel(big, tolerance=.3)
    return pt.x, pt.y


# ------------------------------------------------------------------ build
# ------------------------------------------------------------------ authorised grapes (cahiers des charges)
sys.path.insert(0, str(GP.INFOS / 'Vine_and_Vineyard' / 'Cepages' / '_source'))
from parse import parse_all  # noqa: E402

RED_CODES = {'N', 'Rg'}


def _n(s):
    return re.sub(r'[^a-z0-9]', '', unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower())


CDC = {_n(a['name']): a for a in parse_all()}

# each AOC's detail pop-up on its regional map (the links the site search uses: assets/search_index.js)
MAPPOP = {}
try:
    _t = (GP.INFOS.parent / 'assets' / 'search_index.js').read_text(encoding='utf-8')
    for _d in json.loads(_t[_t.index('=') + 1:].rstrip().rstrip(';'))['docs']:
        if _d['k'] == 'aoc' and _d.get('L', {}).get('map'):
            for _x in [_d['t']] + (_d.get('a') or '').split(','):
                if _x.strip():
                    MAPPOP.setdefault(_n(_x), _d['L']['map'])
    for _x in ('Blanquette de Limoux', 'Blanquette méthode ancestrale'):     # mapped with Limoux (« Limoux · Blanquette · Crémant »)
        MAPPOP.setdefault(_n(_x), MAPPOP.get('limoux'))
except Exception as e:
    print('no map pop-up links:', e)
HA = {}
try:
    _src = GP.INFOS / 'Vine_and_Vineyard' / 'Cepages' / '_source'
    _code = (_src / 'build.py').read_text(encoding='utf-8')
    _map = eval(re.search(r'HA_MAP = (\{.*?\})\n', _code, re.S).group(1))
    for nm, h, _p in json.load(open(_src / 'ha.json', encoding='utf-8')):
        if nm in _map:
            HA[_map[nm]] = int(re.sub(r'[^\d]', '', h))
except Exception as e:      # national planted areas only break ties
    print('no national areas:', e)


NICE = {'sauvignon': 'Sauvignon blanc', 'cot': 'Côt (malbec)', 'fer': 'Fer servadou', 'cabernet-sauvignon': 'Cabernet sauvignon',
        'chenin': 'Chenin blanc', 'melon': 'Melon de Bourgogne', 'vermentino': 'Vermentino (rolle)', 'sciaccarello': 'Sciaccarellu',
        'piquepoul blanc': 'Piquepoul', 'muscat à petits grains': 'Muscat à petits grains'}
LEAD_ALIAS = {'rolle': 'vermentino', 'braucol': 'fer', 'ferservadou': 'fer', 'sciaccarellu': 'sciaccarello', 'piquepoul': 'piquepoulblanc',
              'sauvignonblanc': 'sauvignon', 'chenin blanc': 'chenin', 'cheninblanc': 'chenin', 'melondebourgogne': 'melon',
              'cabernetsauvignon': 'cabernetsauvignon', 'cot': 'cot'}


def gname(key):
    return NICE.get(key, key[:1].upper() + key[1:])


def is_lead(key, lead):
    if not lead:
        return False
    lk = _n(lead[0].split(' (')[0])
    lk = LEAD_ALIAS.get(lk, lk)
    k = _n(key)
    return k == lk or k.startswith(lk) or lk.startswith(k)


def grape_lists(aoc_names, lead_red, lead_white, maxn=5):
    """Up to maxn red and maxn white grapes authorised in these AOCs: principal ones first (bold), then accessory (italic)."""
    stat = {}
    for nm in aoc_names:
        a = CDC.get(_n(nm))
        if not a:
            continue
        seen = set()
        for w in a['wines']:
            for g in w['grapes']:
                if g['adapt']:
                    continue                     # climate-adaptation trial varieties are left out
                d = stat.setdefault(g['id'], dict(key=g['key'], red=g['code'] in RED_CODES, main=False, n=0))
                if g['role'] in ('P', ''):
                    d['main'] = True
                if g['id'] not in seen:
                    d['n'] += 1; seen.add(g['id'])
    out = {}
    for colour, lead in (('red', lead_red), ('white', lead_white)):
        L = [(gid, d) for gid, d in stat.items() if d['red'] == (colour == 'red')]
        L.sort(key=lambda x: (not is_lead(x[1]['key'], lead), not x[1]['main'], -x[1]['n'], -HA.get(x[0], 0), x[1]['key']))
        out[colour] = [[gname(d['key']) + (' rouge' if colour == 'red' and d['key'].startswith('muscat') else ''), 1 if d['main'] else 0]
                       for _gid, d in L[:maxn]]
    return out


LBL_EN = [('vin de liqueur', 'liqueur wine'), ('vin doux naturel', 'vin doux naturel'), ('vins', 'wines'), ('vin', 'wine'),
          ('rouges', 'red'), ('rouge', 'red'), ('blancs', 'white'), ('blanc', 'white'), ('rosés', 'rosé'), ('rosé', 'rosé'),
          ('liquoreux', 'sweet'), ('moelleux', 'medium-sweet'), ('mousseux', 'sparkling'), ('effervescents', 'sparkling'),
          ('effervescent', 'sparkling'), ('tranquilles', 'still'), ('tranquille', 'still'), ('secs', 'dry'), ('sec', 'dry'),
          ('de paille', 'straw wine'), ('jaune', 'jaune'), (' et ', ' and '), ('primeur', 'primeur'), ('nouveau', 'nouveau')]


def label_en(s):
    out = s.lower()
    for a, b in LBL_EN:
        out = re.sub(r'\b' + re.escape(a.strip()) + r'\b', b.strip(), out) if a.strip() != 'et' else out.replace(' et ', ' and ')
    return out[:1].upper() + out[1:]


PALETTE = ['#b5446e', '#d08a3c', '#4f8a55', '#3f78b0', '#8a5bb0', '#c0563f', '#2f9488', '#9a8a2a']


def _tx(cls, x, y, fr, en):
    tr_ = f' data-fr="{att(fr)}" data-en="{att(en)}"' if fr != en else ''      # same in both languages: no translation needed
    return f'<text class="{cls}" x="{x}" y="{y}"{tr_}>{fr}</text>'


def badge(kind, key, name, red, white, x, y, col=None):
    """A label card: area name + red cluster & grape + white cluster & grape. Counter-scaled by the page script."""
    rf, re_ = (red if red else ('—', '—'))
    if white:
        wf, we = white
    else:
        wf, we = ('— (rouge seulement)', '— (red only)')
    wmax = max(len(name[0]), len(name[1]), len(rf) + 3, len(re_) + 3, len(wf) + 3, len(we) + 3)
    w = 14 + wmax * 4.6
    h = 40
    return (f'<g class="bd {kind}" data-k="{key}" data-x="{f(x)}" data-y="{f(y)}" data-w="{f(w)}" data-h="{h}" transform="translate({f(x)} {f(y)})">'
            f'<g class="bdi">'
            f'<rect class="bdbox" x="{f(-w / 2)}" y="{-h / 2}" width="{f(w)}" height="{h}" rx="7"/>'
            + (f'<rect x="{f(-w / 2 + 1.2)}" y="{-h / 2 + 5}" width="3" height="{h - 10}" rx="1.5" fill="{col}"/>' if col else '')
            + _tx('bdt', 0, -9.5, name[0], name[1]) +
            f'<use href="#grape-r" x="{f(-w / 2 + 5)}" y="-4" width="9" height="11"/>'
            + _tx('bdg r', f(-w / 2 + 16), 2, rf, re_) +
            f'<use href="#grape-w" x="{f(-w / 2 + 5)}" y="7" width="9" height="11"/>'
            + _tx('bdg w', f(-w / 2 + 16), 13, wf, we) +
            f'</g><g class="bdm"><circle r="9"/><use href="#grape-r" x="-8" y="-6" width="8" height="10"/>'
            f'<use href="#grape-w" x="0" y="-6" width="8" height="10"/></g></g>')


def build():
    setup()
    game = json.load(open(GAME, encoding='utf-8'))
    aocs, regs = game['aocs'], game['regions']
    missing = sorted({a for s in SUBS for a in s[5] if a not in aocs})
    if missing:
        print('AOCs not in game_geo:', missing)

    region_paths, sub_paths, badges, data = [], [], [], {'regions': {}, 'subs': {}, 'aocs': {}}
    subcol = {}
    # regions
    for rk, (fr, en, red, white) in REGIONS.items():
        g = shape_of([r for r in regs[rk]])
        if g is None:
            continue
        x0, y0, x1, y1 = g.bounds
        key = 'r-' + GP.slug(rk)
        region_paths.append(f'<path class="rg" data-k="{key}" d="{path_of(g, .25)}"/>')
        x, y = anchor(g)
        badges.append(badge('reg', key, (fr, en), red, white, x, y))
        data['regions'][key] = dict(bb=[round(v, 1) for v in (x0, y0, x1, y1)], fr=fr, en=en,
                                    red=red, white=white, subs=[],
                                    g=grape_lists([a['name'] for a in CDC.values() if a['region'] == rk], red, white))
    # sub-regions
    count = {}
    for rk, fr, en, red, white, names, clip, nfr, nen in SUBS:
        col = PALETTE[len(count) % len(PALETTE)]; count[fr] = 1          # cycle through all sub-regions so neighbours differ
        rings = [ring for a in names if a in aocs for ring in aocs[a]]
        g = shape_of(rings, clip)
        if g is None:
            print('empty', fr); continue
        key = 's-' + GP.slug(fr)
        x0, y0, x1, y1 = g.bounds
        sub_paths.append(f'<path class="sa" data-k="{key}" style="--c:{col}" d="{path_of(g, .2)}"/>')
        subcol[fr] = (col, key)
        x, y = anchor(g)
        badges.append(badge('sub', key, (fr, en), red, white, x, y, col))
        rkey = 'r-' + GP.slug(rk)
        data['subs'][key] = dict(bb=[round(v, 1) for v in (x0, y0, x1, y1)], fr=fr, en=en, red=red, white=white,
                                 region=rkey, aocs=[a for a in names if a in aocs], note=[nfr, nen], area=round(g.area, 1),
                                 g=grape_lists(names, red, white))
        data['regions'][rkey]['subs'].append(key)

    # AOCs: outline + label + full grape list per wine type, with the blend percentages of the cahier des charges
    sub_of = {}
    for s_ in SUBS:
        for a in s_[5]:
            sub_of.setdefault(a, s_)
    items = []
    for name, rings in aocs.items():
        g = shape_of(rings)
        if g is None or g.area < .02:
            continue
        items.append((g.area, name, g))
    items.sort(key=lambda t: -t[0])                 # big ones first, so small ones are drawn (and clicked) on top
    aoc_paths = []
    for area, name, g in items:
        s_ = sub_of.get(name)
        cdc = CDC.get(_n(name))
        col, skey = subcol.get(s_[1], ('#8a7a70', None)) if s_ else ('#8a7a70', None)
        rk = s_[0] if s_ else (cdc['region'] if cdc else None)
        rkey = 'r-' + GP.slug(rk) if rk and ('r-' + GP.slug(rk)) in data['regions'] else None
        key = 'a-' + GP.slug(name)
        wines, reds, whites = [], [], []
        for w in (cdc['wines'] if cdc else []):
            gl = []
            for x in w['grapes']:
                main = 1 if x['role'] in ('P', '') else 0
                nm = gname(x['key']) + (' rouge' if x['code'] in RED_CODES and x['key'].startswith('muscat') else '')
                gl.append([nm, main, x['pct'], x['code'], 1 if x['adapt'] else 0])
                if main and not x['adapt']:
                    (reds if x['code'] in RED_CODES else whites).append((nm, x['key'], x['id']))
            gl.sort(key=lambda r: -r[1])                       # principal grapes first, then accessory (stable)
            wines.append(dict(l=[w['label'], label_en(w['label'])], g=gl))
        # label: the sub-region's (or region's) leading grape first, then by planted area in France
        lead_r = s_[3] if s_ else (REGIONS.get(rk, (0, 0, None, None))[2] if rk else None)
        lead_w = s_[4] if s_ else (REGIONS.get(rk, (0, 0, None, None))[3] if rk else None)
        reds = [n for n, _k, _i in sorted(dict((r[2], r) for r in reds).values(), key=lambda r: (not is_lead(r[1], lead_r), -HA.get(r[2], 0)))]
        whites = [n for n, _k, _i in sorted(dict((r[2], r) for r in whites).values(), key=lambda r: (not is_lead(r[1], lead_w), -HA.get(r[2], 0)))]

        def line(L):
            if not L:
                return None
            t_ = ', '.join(L[:2]) + (' …' if len(L) > 2 else '')
            return (t_, t_)
        x0, y0, x1, y1 = g.bounds
        tol = min(.5, max(.05, area ** .5 * .03))          # detail in proportion to size: grands crus stay sharp
        aoc_paths.append(f'<path class="ac" data-k="{key}" style="--c:{col}" d="{path_of(g, tol)}"/>')
        x, y = anchor(g)
        rl, wl = line(reds), line(whites)
        rl = rl[0] if rl else '—'
        wl = wl[0] if wl else None
        bw = 14 + max(len(name), len(rl) + 3, len(wl or '— (red only)') + 3) * 4.6
        data['aocs'][key] = dict(x=round(x, 2), y=round(y, 2), w=round(bw, 1), c=col, rl=rl, wl=wl,       # label, drawn by the page script
                                 bb=[round(v, 2) for v in (x0, y0, x1, y1)], fr=name, en=name, region=rkey, sub=skey,
                                 area=round(area, 2), pri=0 if s_ else 1, m=MAPPOP.get(_n(name)), wines=wines, notes=cdc['notes'] if cdc else [])
    print(len(data['aocs']), 'AOCs on the map')

    # list panel
    lis = []
    for rkey, R in data['regions'].items():
        subs = ''.join(f'<li><button type="button" class="gs" data-k="{k}">{tr(data["subs"][k]["fr"], data["subs"][k]["en"])}</button></li>'
                       for k in R['subs'])
        lis.append(f'<li class="gr"><button type="button" class="grb" data-k="{rkey}">{tr(R["fr"], R["en"])}</button><ul>{subs}</ul></li>')

    x, y, w, h = GP.GEO['place']
    cx, cy, cw, ch = GP.GEO['corse']
    defs = (
        '<defs>'
        '<radialGradient id="gr-r" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#b0457a"/><stop offset=".55" stop-color="#6e1d48"/><stop offset="1" stop-color="#3b0a26"/></radialGradient>'
        '<radialGradient id="gr-w" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#f4f1b0"/><stop offset=".55" stop-color="#c9cc63"/><stop offset="1" stop-color="#8d9a33"/></radialGradient>'
        + ''.join(
            f'<symbol id="grape-{k}" viewBox="0 0 20 24"><path d="M10 5.2 C10 3 11 1.6 12.6 .8" fill="none" stroke="#6b4a2b" stroke-width="1.3" stroke-linecap="round"/>'
            f'<path d="M11.4 2.4 C14 0.6 17.6 1.2 18.6 3.4 C16.4 4.8 13.4 4.6 11.4 2.4Z" fill="#7d9a3a"/>'
            + ''.join(f'<circle cx="{cx_}" cy="{cy_}" r="2.55" fill="url(#gr-{k})" stroke="rgba(0,0,0,.25)" stroke-width=".35"/>'
                      for cx_, cy_ in [(4.2, 7.6), (8.4, 7.2), (12.6, 7.4), (16.4, 8.2), (6.2, 11.6), (10.4, 11.4), (14.5, 11.8),
                                       (8.2, 15.6), (12.4, 15.6), (10.2, 19.6)])
            + '</symbol>' for k in ('r', 'w'))
        + '</defs>')
    svg = (f'<svg class="gmap" id="gmap" viewBox="0 0 720 540" role="img" aria-label="Carte des cépages">{defs}'
           f'<rect x="-2000" y="-2000" width="4720" height="4540" class="sea"/>'
           f'<g class="world"><image href="img/map_rivers.webp?v={VER}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" preserveAspectRatio="none"/>'
           f'<image href="img/map_corsica_hq.webp?v={VER}" x="{f(cx)}" y="{f(cy)}" width="{f(cw)}" height="{f(ch)}" preserveAspectRatio="none"/>'
           f'<g class="subs">{"".join(sub_paths)}</g><g class="aocs">{"".join(aoc_paths)}</g><g class="regs">{"".join(region_paths)}</g>'
           f'<g class="badges">{"".join(badges)}</g></g></svg>')

    body = f'''
  <div class="gwrap">
    <div class="gstage" id="gstage">
      {svg}
      <div class="gctl">
        <button type="button" id="z-in" data-tip-fr="Zoomer" data-tip-en="Zoom in">+</button>
        <button type="button" id="z-out" data-tip-fr="Dézoomer" data-tip-en="Zoom out">−</button>
        <button type="button" id="z-home" data-tip-fr="Toute la France" data-tip-en="All of France"><svg viewBox="0 0 24 24"><path d="M4 11 12 4l8 7v9h-5v-6H9v6H4z"/></svg></button>
        <button type="button" id="z-full" data-tip-fr="Plein écran" data-tip-en="Full screen"><svg viewBox="0 0 24 24"><path d="M4 9V4h5v2H6v3zM20 9V4h-5v2h3v3zM4 15v5h5v-2H6v-3zM20 15v5h-5v-2h3v-3z"/></svg></button>
      </div>
      <p class="ghint" data-fr="Molette ou pincement pour zoomer · glisser pour se déplacer · cliquer sur une région" data-en="Scroll or pinch to zoom · drag to move · click a region">Molette ou pincement pour zoomer · glisser pour se déplacer · cliquer sur une région</p>
      <div class="gcard gpop" id="gcard" hidden></div>
      <div class="gleg"><span><svg viewBox="0 0 20 24"><use href="#grape-r"/></svg>{tr("Cépage rouge principal", "Leading red grape")}</span>
        <span><svg viewBox="0 0 20 24"><use href="#grape-w"/></svg>{tr("Cépage blanc principal", "Leading white grape")}</span></div>
    </div>
    <aside class="gside panel">
      <p class="kick" data-fr="Régions et sous-régions" data-en="Regions and sub-regions">Régions et sous-régions</p>
      <ul class="glist">{"".join(lis)}</ul>
    </aside>
  </div>
  <p class="gnote">{tr("Cépages dominants des vins d’appellation (AOC), par surface plantée. Les contours sont ceux des aires d’appellation (INAO).",
                      "Leading grapes of appellation (AOC) wines, by planted area. Outlines are those of the appellation areas (INAO).")}</p>
'''
    src = ''.join(f'<li>{tr(a, b)}</li>' for a, b in [
        ('Aires d’appellation : INAO, délimitations parcellaires des AOC (2026), Licence Ouverte Etalab 2.0.',
         'Appellation areas: INAO, AOC parcel delimitations (2026), Etalab Open Licence 2.0.'),
        ('Cours d’eau et trait de côte : BD TOPAGE® (IGN / OFB), diffusée par le Sandre, Licence Ouverte Etalab 2.0.',
         'Rivers and coastline: BD TOPAGE® (IGN / OFB), distributed by Sandre, Etalab Open Licence 2.0.'),
        ('Relief : Terrain Tiles (Mapzen / Amazon Web Services) — SRTM, EU-DEM et autres sources ; ombrage et teintes de l’auteur.',
         'Relief: Terrain Tiles (Mapzen / Amazon Web Services) — SRTM, EU-DEM and other sources; shading and colours by the author.'),
        ('Carte et texte : Christophe A. Paul.', 'Map and text: Christophe A. Paul.')])

    aoc_link = '../../Infos/Vine_and_Vineyard/Cepages/Cepages_et_Appellations.html'   # root-relative like the template; fixed below for the page's depth
    map_link = '../../Vignobles%20de%20France%20%E2%80%94%20Carte%20de%20France.html'
    html = GP.TEMPLATE
    title = ('Les cépages de France', 'The grapes of France')
    for k, v in {'%BASECSS%': GP.base_css(), '%CSS%': CSS, '%BODY%': body, '%DATA%': '{}',
                 '%PTITLE%': json.dumps(list(title), ensure_ascii=False), '%SOURCES%': src, '%JS%': GP.JS + JS.replace('%GDATA%', json.dumps(data, ensure_ascii=False, separators=(',', ':'))).replace('%AOCL%', aoc_link).replace('%MAPL%', map_link),
                 '%T_FR%': title[0], '%DESC%': 'Carte interactive : les deux cépages principaux, un rouge et un blanc, de chaque région et sous-région viticole française.',
                 '%H1%': tr('Les <em>cépages</em> de France', 'The <em>grapes</em> of France', 'h1'),
                 '%TAG%': tr('Pour chaque région et sous-région viticole, son cépage rouge et son cépage blanc principaux, avec quelques autres cépages autorisés — '
                             f'une sélection, pas une liste exhaustive : la liste complète des cépages de chaque appellation se trouve dans la section <a href="{aoc_link}">Cépages et appellations</a> ou sur la carte <a href="{map_link}">Vignobles de France</a>. '
                             'Zoomez, déplacez-vous, cliquez sur une région.',
                             'For each wine region and sub-region, its leading red and white grapes, with a few other authorised varieties — '
                             f'a selection, not an exhaustive list: the full list of grapes for each appellation is in the <a href="{aoc_link}">Grapes and appellations</a> section or on the <a href="{map_link}">Vineyards of France</a> map. '
                             'Zoom, move around, click a region.', 'p', 'tagline')}.items():
        html = html.replace(k, v)
    html = html.replace('data-fr="Géographie · film interactif" data-en="Geography · interactive film">Géographie · film interactif',
                        'data-fr="Géographie · carte interactive" data-en="Geography · interactive map">Géographie · carte interactive')
    rel = os.path.relpath(GP.REPO, OUT.parent).replace(os.sep, '/') + '/'
    html = html.replace('"../../', '"' + rel).replace("'../../", "'" + rel).replace('(../../', '(' + rel).replace('&quot;../../', '&quot;' + rel)
    OUT.write_text(html, encoding='utf-8')
    for extra in ('map_relief.webp', 'map_corsica.webp'):      # copied by gen_page.load_geo, not used here
        (IMG / extra).unlink(missing_ok=True)
    print(f'wrote {OUT.relative_to(GP.REPO)} — {len(html) // 1024} KB, {len(data["regions"])} regions, {len(data["subs"])} sub-regions')
    embed_cepages(body, data)


# ------------------------------------------------------------------ embed in « Cépages & Appellations »
CEP = GP.INFOS / 'Vine_and_Vineyard' / 'Cepages'
CEP_IMG = 'img/grape_map'


def embed_cepages(body, data):
    """Writes Cepages/_source/grape_map_fragment.json (css / html / js) + images; Cepages build.py inserts it above the search."""
    import shutil
    (CEP / CEP_IMG).mkdir(parents=True, exist_ok=True)
    for fn in ('map_rivers.webp', 'map_corsica_hq.webp'):
        shutil.copyfile(IMG / fn, CEP / CEP_IMG / fn)
    map_link = '../../../Vignobles%20de%20France%20%E2%80%94%20Carte%20de%20France.html'
    intro = tr('Pour chaque région et sous-région viticole, son cépage rouge et son cépage blanc principaux, avec quelques autres cépages autorisés — '
               'une sélection, pas une liste exhaustive : la liste complète des cépages de chaque appellation se trouve juste en dessous, dans la '
               f'<a href="#combo">recherche par cépage ou par appellation</a>, ou sur la carte <a href="{map_link}">Vignobles de France</a>. '
               'Zoomez, déplacez-vous, cliquez sur une région.',
               'For each wine region and sub-region, its leading red and white grapes, with a few other authorised varieties — '
               'a selection, not an exhaustive list: the full list of grapes for each appellation is just below, in the '
               f'<a href="#combo">search by grape or by appellation</a>, or on the <a href="{map_link}">Vineyards of France</a> map. '
               'Zoom, move around, click a region.', 'p', 'gintro')
    html = (f'<section class="gmapsec" id="carte-cepages">'
            f'<div class="sec-head"><h2 data-fr="Les cépages de France, région par région" data-en="The grapes of France, region by region">Les cépages de France, région par région</h2></div>'
            f'{intro}{body}</section>')
    html = html.replace('href="img/map_rivers.webp', f'href="{CEP_IMG}/map_rivers.webp').replace('href="img/map_corsica_hq.webp', f'href="{CEP_IMG}/map_corsica_hq.webp')
    # page-level rules of the standalone page are left out; colour variables this page lacks are defined on the section
    keep = [ln for ln in CSS.splitlines() if not ln.strip().startswith(('.wrap', '.kick', '.srcs'))]
    css = ('  .gmapsec{margin:28px 0 30px;--track:rgba(245,239,227,.07);--title:#fff;--shadow:0 18px 50px rgba(10,1,4,.5);}\n'
           '  html[data-theme="cream"] .gmapsec{--track:rgba(46,20,25,.05);--title:#3a1219;--shadow:0 10px 30px rgba(90,30,40,.10);}\n'
           '  .gmapsec .kick{text-transform:uppercase;letter-spacing:.28em;font-size:10px;font-weight:700;color:var(--gold);margin:0 0 8px;}\n'
           '  .gintro{font-size:14.5px;line-height:1.65;color:var(--muted);max-width:900px;margin:0 0 16px;}\n'
           '  .gintro a{color:var(--gold-soft);text-decoration:underline;text-underline-offset:2px;}\n' + '\n'.join(keep))
    js = JS.replace('%GDATA%', json.dumps(data, ensure_ascii=False, separators=(',', ':'))).replace('%AOCL%', '#combo').replace('%MAPL%', map_link)
    # on this page the full list is the search right below the map
    js = (js.replace('section <a href=\\"\' + AOCL + \'\\">Cépages et appellations</a>', '<a href=\\"\' + AOCL + \'\\">recherche ci-dessous</a>')
            .replace('<a href=\\"\' + AOCL + \'\\">Grapes and appellations</a> section', 'the <a href=\\"\' + AOCL + \'\\">search below</a>'))
    out = CEP / '_source' / 'grape_map_fragment.json'
    json.dump(dict(css=css, html=html, js=js), open(out, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'wrote {out.relative_to(GP.REPO)} — {out.stat().st_size // 1024} KB (+ {CEP_IMG}/)')


CSS = r'''
  .wrap{max-width:1440px;}
  .kick{text-transform:uppercase;letter-spacing:.28em;font-size:10px;font-weight:700;color:var(--gold);margin:0 0 8px;}
  .gwrap{display:grid;grid-template-columns:minmax(0,1fr) 340px;gap:16px;align-items:start;}
  .gstage{position:relative;border-radius:16px;overflow:hidden;background:#fff;box-shadow:var(--shadow);border:1px solid var(--hair);
    height:min(78vh,860px);touch-action:none;user-select:none;-webkit-user-select:none;}
  .gstage:fullscreen{border-radius:0;height:100vh;}
  .gmap{position:absolute;inset:0;width:100%;height:100%;display:block;cursor:grab;}
  .gmap.drag{cursor:grabbing;}
  .sea{fill:#fff;}
  .rg{fill:rgba(142,31,51,.0);stroke:#8e1f33;stroke-width:.7;stroke-dasharray:2.2 1.6;stroke-opacity:.55;cursor:pointer;vector-effect:non-scaling-stroke;}
  .rg:hover,.rg.on{fill:rgba(142,31,51,.08);stroke-opacity:.95;}
  .sa{fill:var(--c);fill-opacity:.2;stroke:var(--c);stroke-width:.9;stroke-opacity:.8;cursor:pointer;vector-effect:non-scaling-stroke;display:none;}
  .gmap.zsub .sa{display:inline;}
  .gmap.zsub .rg{fill:none;pointer-events:none;}
  .ac{fill:var(--c);fill-opacity:.07;stroke:var(--c);stroke-width:.8;stroke-opacity:.85;cursor:pointer;vector-effect:non-scaling-stroke;display:none;}
  .gmap.zaoc .ac{display:inline;}
  .gmap.zaoc .sa{fill-opacity:0;stroke-opacity:.3;pointer-events:none;}
  .ac:hover{fill-opacity:.24;}
  .ac.on{fill-opacity:.34;stroke-width:1.8;stroke-opacity:1;}
  .sa:hover{fill-opacity:.32;stroke-opacity:1;}
  .sa.on{fill-opacity:.38;stroke-opacity:1;stroke-width:1.8;}
  .bd{cursor:pointer;}
  .bd.sub,.gmap.zsub .bd.reg{display:none;}
  .gmap.zsub .bd.sub{display:inline;}
  .bd.aoc,.gmap.zaoc .bd.sub{display:none;}
  .gmap.zaoc .bd.aoc{display:inline;}
  .bd.off{display:none !important;}
  .bdm{display:none;}
  .bd.mini .bdi{display:none;}
  .bd.mini .bdm{display:inline;}
  .bdbox{fill:rgba(255,255,255,.93);stroke:rgba(142,31,51,.35);stroke-width:.7;filter:drop-shadow(0 1px 1.5px rgba(60,20,30,.22));}
  .bd:hover .bdbox,.bd.on .bdbox{stroke:#8e1f33;stroke-width:1.2;}
  .bdm circle{fill:rgba(255,255,255,.93);stroke:rgba(142,31,51,.45);stroke-width:.7;}
  .bdt{font:italic 700 8.6px/1 var(--serif);fill:#3a1219;text-anchor:middle;dominant-baseline:central;}
  .bdg{font:600 7px/1 var(--sans);dominant-baseline:central;}
  .bdg.r{fill:#6e1d48;}
  .bdg.w{fill:#5d6a1e;}
  .gctl{position:absolute;right:12px;top:12px;display:flex;flex-direction:column;gap:6px;}
  .gctl button{width:36px;height:36px;border-radius:10px;border:1px solid rgba(142,31,51,.25);background:rgba(255,253,248,.95);color:#8e1f33;
    font:600 20px/1 var(--sans);cursor:pointer;display:grid;place-items:center;box-shadow:0 2px 8px rgba(60,20,30,.12);}
  .gctl svg{width:18px;height:18px;fill:currentColor;}
  .ghint{position:absolute;left:12px;bottom:8px;margin:0;font:500 11px/1.3 var(--sans);color:#6b5b55;background:rgba(255,255,255,.85);padding:4px 8px;border-radius:8px;}
  .gleg{position:absolute;left:12px;top:12px;display:flex;flex-direction:column;gap:4px;background:rgba(255,255,255,.9);padding:7px 10px;border-radius:10px;
    font:600 11px/1.2 var(--sans);color:#3a1219;box-shadow:0 2px 8px rgba(60,20,30,.1);}
  .gleg span{display:flex;align-items:center;gap:6px;}
  .gleg svg{width:13px;height:16px;}
  .gside{border-radius:14px;padding:14px;max-height:min(78vh,860px);overflow:auto;position:sticky;top:12px;}
  .gpop{position:absolute;z-index:5;width:330px;max-height:72%;overflow:auto;padding:14px 14px 12px;border-radius:14px;
    background:#fffdf8;border:1px solid rgba(142,31,51,.28);box-shadow:0 12px 34px rgba(60,20,30,.28);
    --parchment:#2e1419;--muted:rgba(46,20,25,.74);--faint:rgba(46,20,25,.5);--track:rgba(46,20,25,.05);--hair:rgba(142,31,51,.16);
    --hair-hi:rgba(142,31,51,.45);--title:#3a1219;--gold:#9a6a1f;--gold-soft:#8e1f33;}
  .gpop[hidden]{display:none;}
  .gpop.sheet{left:8px !important;right:8px;bottom:8px;top:auto !important;width:auto;max-height:62%;}
  .gpop .gx{position:absolute;right:8px;top:8px;width:28px;height:28px;border-radius:50%;border:1px solid var(--hair);background:#fff;color:#8e1f33;
    font:400 18px/1 var(--sans);cursor:pointer;display:grid;place-items:center;padding:0;}
  .gpop .gx:hover{border-color:var(--hair-hi);}
  .gpop h3{padding-right:30px;}
  .gcard .gk{font:700 9.5px/1 var(--sans);letter-spacing:.24em;text-transform:uppercase;color:var(--gold);margin:0;}
  .gcard h3{font:500 23px/1.15 var(--serif);color:var(--title);margin:4px 0 10px;}
  .gcard .gpair{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:0 0 6px;}
  .gcard .gl{display:block;font:400 12px/1.45 var(--sans);font-style:normal;color:var(--muted);margin-top:6px;padding-top:6px;border-top:1px solid var(--hair);}
  .gcard .gl b{display:inline;font:700 12px/1.45 var(--sans);color:var(--parchment);}
  .gcard .gl i{font-style:italic;}
  .gcard .gkey{font:400 11px/1.4 var(--sans);color:var(--faint);margin:0 0 10px;}
  .gcard .gkey b{font-weight:700;}
  .gcard .gkey a,.tagline a{color:var(--gold-soft);text-decoration:underline;text-underline-offset:2px;}
  .gcard .gg{display:flex;align-items:flex-start;gap:8px;background:var(--track);border:1px solid var(--hair);border-radius:10px;padding:8px;}
  .gcard .gg svg{width:26px;height:31px;flex:none;}
  .gcard .gg .gm{display:block;font:600 13.5px/1.2 var(--sans);color:var(--parchment);}
  .gcard .gg small{display:block;font:600 9px/1 var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--faint);margin-bottom:3px;}
  .gcard p.gn{font:400 13px/1.5 var(--sans);color:var(--muted);margin:0 0 8px;}
  .gcard .gaocs{display:flex;flex-wrap:wrap;gap:4px;margin:6px 0 0;}
  .gcard .gaocs button{font:500 11px/1 var(--sans);color:var(--gold-soft);background:none;border:1px solid var(--hair-hi);border-radius:999px;padding:4px 8px;cursor:pointer;}
  .gcard .gaocs button:hover{background:var(--track);}
  .gcard .aw{margin:0 0 9px;}
  .gcard .awl{font:700 9.5px/1 var(--sans);letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin:0 0 5px;}
  .gcard .awg{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:3px 12px;font:400 12.5px/1.5 var(--sans);color:var(--parchment);}
  .gcard .awg b{font-weight:700;}
  .gcard .awg i{color:var(--muted);}
  .gcard .dt{display:inline-block;width:7px;height:7px;border-radius:50%;margin-right:5px;vertical-align:1px;border:1px solid rgba(0,0,0,.15);}
  .gcard .pc{font:600 10.5px/1 var(--sans);color:#8e1f33;background:rgba(142,31,51,.07);border-radius:5px;padding:2px 5px;}
  .gcard .ad{font:600 9px/1 var(--sans);letter-spacing:.06em;text-transform:uppercase;color:var(--faint);border:1px solid var(--hair);border-radius:5px;padding:2px 4px;}
  .gcard .anotes{margin:4px 0 0;padding-left:16px;font:400 12px/1.45 var(--sans);color:var(--muted);}
  .gcard .anotes li{margin:2px 0;}
  .gcard .gaocs span{font:500 11px/1 var(--sans);color:var(--muted);border:1px solid var(--hair);border-radius:999px;padding:4px 8px;}
  .gcard .gsubs{display:flex;flex-wrap:wrap;gap:5px;}
  .glist{list-style:none;margin:0;padding:0;}
  .gr{margin:0 0 8px;}
  .grb{display:block;width:100%;text-align:left;background:none;border:0;border-bottom:1px solid var(--hair);padding:6px 2px;cursor:pointer;
    font:italic 600 16px/1.2 var(--serif);color:var(--title);}
  .grb:hover,.grb.on{color:var(--gold-soft);border-bottom-color:var(--gold);}
  .gr ul{list-style:none;margin:6px 0 0;padding:0;display:flex;flex-wrap:wrap;gap:5px;}
  .gs{cursor:pointer;font:500 12.5px/1 var(--sans);color:var(--parchment);background:var(--track);border:1px solid var(--hair);border-radius:999px;padding:6px 10px;}
  .gs:hover{border-color:var(--hair-hi);}
  .gs.on{background:#8e1f33;border-color:#8e1f33;color:#fff;}
  .gnote{font:400 13px/1.6 var(--sans);color:var(--muted);max-width:900px;margin:14px auto 0;text-align:center;}
  .srcs{margin:44px auto 0;max-width:900px;}
  .srcs h2{font:500 22px/1.2 var(--serif);color:var(--title);margin:0 0 10px;}
  .srcs ol{margin:0;padding-left:20px;font:400 13px/1.6 var(--sans);color:var(--muted);}
  @media (max-width:980px){
    .gwrap{grid-template-columns:minmax(0,1fr);}
    .gside{position:static;max-height:none;}
    .gstage{height:72vh;}
    .ghint{display:none;}
  }
'''

JS = r'''
(function(){
  var D = %GDATA%, AOCL = '%AOCL%', MAPL = '%MAPL%';
  var svg = document.getElementById('gmap'), stage = document.getElementById('gstage');
  // AOC labels are built here from the data (same markup as the region / sub-region labels written in the page)
  (function(){
    var out = [], fr = document.documentElement.lang !== 'en';
    Object.keys(D.aocs).forEach(function(k){
      var a = D.aocs[k], w = a.w, x0 = -w/2;
      var wl = a.wl || '', wlFr = a.wl || '— (rouge seulement)', wlEn = a.wl || '— (red only)';
      out.push('<g class="bd aoc" data-k="' + k + '" data-x="' + a.x + '" data-y="' + a.y + '" data-w="' + w + '" data-h="40" transform="translate(' + a.x + ' ' + a.y + ')">' +
        '<g class="bdi"><rect class="bdbox" x="' + x0 + '" y="-20" width="' + w + '" height="40" rx="7"/>' +
        '<rect x="' + (x0 + 1.2) + '" y="-15" width="3" height="30" rx="1.5" fill="' + a.c + '"/>' +
        '<text class="bdt" x="0" y="-9.5">' + a.fr + '</text>' +
        '<use href="#grape-r" x="' + (x0 + 5) + '" y="-4" width="9" height="11"/><text class="bdg r" x="' + (x0 + 16) + '" y="2">' + a.rl + '</text>' +
        '<use href="#grape-w" x="' + (x0 + 5) + '" y="7" width="9" height="11"/><text class="bdg w" x="' + (x0 + 16) + '" y="13"' +
        (a.wl ? '' : ' data-fr="' + wlFr + '" data-en="' + wlEn + '"') + '>' + (a.wl ? wl : (fr ? wlFr : wlEn)) + '</text></g>' +
        '<g class="bdm"><circle r="9"/><use href="#grape-r" x="-8" y="-6" width="8" height="10"/><use href="#grape-w" x="0" y="-6" width="8" height="10"/></g></g>');
    });
    svg.querySelector('.badges').insertAdjacentHTML('beforeend', out.join(''));
  })();
  var badges = [].slice.call(svg.querySelectorAll('.bd'));
  var LANG = function(){ return document.documentElement.lang==='en' ? 'en' : 'fr'; };
  var W0 = 720, H0 = 540, MAXK = 40, SUBK = 2.2, AOCK = 6;
  var V = {x:0, y:0, w:W0, h:H0}, anim = null, sel = null;

  function fit(v){
    var r = stage.getBoundingClientRect(), ar = r.width / r.height;
    var w = v.w, h = v.h;
    if(w / h > ar) h = w / ar; else w = h * ar;
    w = Math.min(Math.max(w, W0/MAXK), W0*1.6); h = w / ar;
    var cx = v.x + v.w/2, cy = v.y + v.h/2;
    return {x:cx - w/2, y:cy - h/2, w:w, h:h};
  }
  function apply(){
    svg.setAttribute('viewBox', V.x.toFixed(2)+' '+V.y.toFixed(2)+' '+V.w.toFixed(2)+' '+V.h.toFixed(2));
    var r = stage.getBoundingClientRect();
    var k = W0 / V.w;                       // zoom factor
    var upp = V.w / r.width;               // svg units per screen px
    svg.classList.toggle('zsub', k >= SUBK);
    svg.classList.toggle('zaoc', k >= AOCK);
    layout(upp, k >= AOCK ? 'aoc' : k >= SUBK ? 'sub' : 'reg');
    place();
  }
  // badges keep a constant on-screen size; the ones that would overlap shrink to a mini marker, then hide
  function layout(upp, lvl){
    var s = upp * 1.4, boxes = [];
    var list = badges.filter(function(b){ return b.classList.contains(lvl); });
    // sub-regions: biggest first; AOCs: those of the sub-regions first (then the regional umbrellas), biggest first
    function pr(k){ var a = D.aocs[k]; if(a) return a.pri * 1e6 - a.area; var s_ = D.subs[k]; return s_ ? -s_.area : 0; }
    list.sort(function(a, b){ return pr(a.dataset.k) - pr(b.dataset.k); });
    if(sel){ list.sort(function(a, b){ return (b.dataset.k===sel) - (a.dataset.k===sel); }); }
    for(var i=0;i<list.length;i++){
      var b = list[i], x = +b.dataset.x, y = +b.dataset.y, w = +b.dataset.w * s, h = +b.dataset.h * s;
      b.setAttribute('transform', 'translate('+x+' '+y+') scale('+s.toFixed(4)+')');
      var full = [x - w/2, y - h/2, x + w/2, y + h/2], m = 10*s, mini = [x - m, y - m, x + m, y + m];
      b.classList.remove('mini', 'off');
      if(!hits(full, boxes)){ boxes.push(full); }
      else if(!hits(mini, boxes)){ b.classList.add('mini'); boxes.push(mini); }
      else b.classList.add('off');
    }
  }
  function hits(a, list){ for(var i=0;i<list.length;i++){ var b = list[i]; if(a[0]<b[2] && a[2]>b[0] && a[1]<b[3] && a[3]>b[1]) return true; } return false; }

  function goTo(t, ms){
    t = fit(t); var s = {x:V.x, y:V.y, w:V.w, h:V.h}, t0 = performance.now(); ms = ms===undefined ? 650 : ms;
    if(ms===0 || /noanim/.test(location.search)){ V = t; apply(); return; }
    if(anim) cancelAnimationFrame(anim);
    (function step(now){
      var p = Math.min(1, (now - t0) / ms), e = p<.5 ? 4*p*p*p : 1 - Math.pow(-2*p+2, 3)/2;
      // zoom in log space so the motion feels even
      var lw = Math.exp(Math.log(s.w) + (Math.log(t.w) - Math.log(s.w)) * e);
      var cx = (s.x + s.w/2) + ((t.x + t.w/2) - (s.x + s.w/2)) * e, cy = (s.y + s.h/2) + ((t.y + t.h/2) - (s.y + s.h/2)) * e;
      var lh = lw * t.h / t.w;
      V = {x:cx - lw/2, y:cy - lh/2, w:lw, h:lh}; apply();
      if(p < 1) anim = requestAnimationFrame(step); else anim = null;
    })(t0);
  }
  function zoomAt(f, px, py){
    var r = stage.getBoundingClientRect();
    var ux = V.x + (px - r.left) / r.width * V.w, uy = V.y + (py - r.top) / r.height * V.h;
    var w = Math.min(Math.max(V.w / f, W0/MAXK), W0*1.6), h = w * V.h / V.w;
    V = {x:ux - (ux - V.x) * w / V.w, y:uy - (uy - V.y) * h / V.h, w:w, h:h}; apply();
  }
  function home(){ goTo({x:60, y:-4, w:600, h:548}); }
  function bbView(bb, pad){
    var w = bb[2]-bb[0], h = bb[3]-bb[1], p = Math.max(w, h) * (pad||.35) + 6;
    return {x:bb[0]-p, y:bb[1]-p, w:w+2*p, h:h+2*p};
  }

  // ------------------------------------------------------------ selection
  function grapeBox(cls, label, g, empty, list){
    var li = (list || []).map(function(x){ return x[1] ? '<b>' + x[0] + '</b>' : '<i>' + x[0] + '</i>'; }).join(', ');
    return '<div class="gg"><svg viewBox="0 0 20 24"><use href="#grape-' + cls + '"/></svg><span><small>' + label + '</small><b class="gm">' +
      (g ? g[LANG()==='fr' ? 0 : 1] : empty) + '</b>' + (li ? '<em class="gl">' + li + '</em>' : '') + '</span></div>';
  }
  var DOT = {N:'#7b2350', Rg:'#c9404e', B:'#c9cc63', G:'#9a918c', Rs:'#e58ca2'};
  function pctTr(p){ return LANG()==='fr' ? p : p.replace(/de l'assemblage/g, 'of the blend').replace(/du vignoble/g, 'of the vineyard')
    .replace(/vignoble/g, 'vineyard').replace(/assemblage/g, 'blend').replace(/de l'encépagement/g, 'of the plantings').replace(/encépagement/g, 'plantings'); }
  function popL(o){ return o.m ? MAPL.replace(/[^\/]*$/, '') + o.m.split('#')[0].split('/').map(encodeURIComponent).join('/') + '#' + o.m.split('#')[1] : MAPL; }   // the AOC's pop-up on its regional map
  function aocCard(k){
    var c = document.getElementById('gcard'), fr = LANG()==='fr', o = D.aocs[k];
    var where = o.sub ? D.subs[o.sub][fr ? 'fr' : 'en'] : (o.region ? D.regions[o.region][fr ? 'fr' : 'en'] : '');
    var h = '<button type="button" class="gx" aria-label="' + (fr ? 'Fermer' : 'Close') + '">×</button><p class="gk">Appellation' + (where ? ' · ' + where : '') + '</p>';
    h += '<h3>' + o.fr + '</h3>';
    if(!o.wines.length) h += '<p class="gn">' + (fr ? 'Eau-de-vie : pas de liste de cépages dans ce jeu de données.' : 'A spirit: no grape list in this dataset.') + '</p>';
    o.wines.forEach(function(w){
      h += '<div class="aw"><p class="awl">' + w.l[fr ? 0 : 1] + '</p><ul class="awg">' + w.g.map(function(x){
        var n = x[1] ? '<b>' + x[0] + '</b>' : '<i>' + x[0] + '</i>';
        return '<li><span class="dt" style="background:' + (DOT[x[3]] || '#999') + '"></span>' + n +
          (x[2] ? ' <span class="pc">' + pctTr(x[2]) + '</span>' : '') + (x[4] ? ' <span class="ad">' + (fr ? 'adaptation' : 'adaptation') + '</span>' : '') + '</li>';
      }).join('') + '</ul></div>';
    });
    h += '<p class="gkey">' + (fr ? '<b>Principaux</b> en gras, <i>accessoires</i> en italique ; les pourcentages sont ceux du cahier des charges (part de l’assemblage ou du vignoble). Fiche complète : <a href=\"' + AOCL + '\">Cépages</a> et <a href=\"' + popL(o) + '\">Appellations</a>.'
                             : '<b>Principal</b> in bold, <i>accessory</i> in italics; percentages are those of the cahier des charges (share of the blend or of the vineyard). Full entry: <a href=\"' + AOCL + '\">Grapes</a> and <a href=\"' + popL(o) + '\">Appellations</a>.') + '</p>';
    if(o.notes.length) h += '<p class="gk">' + (fr ? 'Règles d’assemblage' : 'Blending rules (in French)') + '</p><ul class="anotes">' + o.notes.map(function(n){ return '<li>' + n + '</li>'; }).join('') + '</ul>';
    c.innerHTML = h; c.hidden = false; place();
  }
  function card(k){
    if(D.aocs[k]) return aocCard(k);
    var c = document.getElementById('gcard'), fr = LANG()==='fr', o = D.subs[k] || D.regions[k], isSub = !!D.subs[k];
    if(!o){ c.innerHTML = ''; c.hidden = true; return; }
    var h = '<button type="button" class="gx" aria-label="' + (fr ? 'Fermer' : 'Close') + '">×</button><p class="gk">' + (isSub ? (fr ? 'Sous-région · ' : 'Sub-region · ') + D.regions[o.region][fr ? 'fr' : 'en'] : (fr ? 'Région' : 'Region')) + '</p>';
    h += '<h3>' + o[fr ? 'fr' : 'en'] + '</h3><div class="gpair">' +
      grapeBox('r', fr ? 'Rouge' : 'Red', o.red, '—', o.g.red) + grapeBox('w', fr ? 'Blanc' : 'White', o.white, fr ? '— rouge seulement' : '— red only', o.g.white) + '</div>' +
      '<p class="gkey">' + (fr ? 'Cépages autorisés : <b>principaux</b> en gras, <i>accessoires</i> en italique (cahiers des charges, 5 au plus par couleur). Liste complète : section <a href=\"' + AOCL + '\">Cépages et appellations</a> ou carte <a href=\"' + MAPL + '\">Vignobles de France</a>.'
                               : 'Authorised grapes: <b>principal</b> in bold, <i>accessory</i> in italics (cahiers des charges, up to 5 per colour). Full list: <a href=\"' + AOCL + '\">Grapes and appellations</a> section or <a href=\"' + MAPL + '\">Vineyards of France</a> map.') + '</p>';
    if(isSub){
      if(o.note[0]) h += '<p class="gn">' + o.note[fr ? 0 : 1] + '</p>';
      h += '<p class="gk">' + (fr ? 'Appellations — cliquez pour le détail' : 'Appellations — click for details') + '</p><div class="gaocs">' + o.aocs.map(function(a){
        var ak = 'a-' + slug(a); return D.aocs[ak] ? '<button type="button" data-k="' + ak + '">' + a + '</button>' : '<span>' + a + '</span>'; }).join('') + '</div>';
    } else if(o.subs.length > 1){
      h += '<div class="gsubs">' + o.subs.map(function(s){ return '<button type="button" class="gs" data-k="' + s + '">' + D.subs[s][fr ? 'fr' : 'en'] + '</button>'; }).join('') + '</div>';
    }
    c.innerHTML = h; c.hidden = false; place();
  }
  // the card sits on the map, next to the area's label, and follows it while zooming / panning
  function place(){
    var c = document.getElementById('gcard');
    if(!sel || c.hidden) return;
    var r = stage.getBoundingClientRect(), b = svg.querySelector('.bd[data-k="' + sel + '"]');
    if(r.width < 600 || !b){ c.classList.add('sheet'); return; }
    c.classList.remove('sheet');
    if(D.regions[sel]){                                           // a whole region: dock beside the zoom buttons
      c.style.left = Math.max(8, r.width - c.offsetWidth - 58).toFixed(0) + 'px'; c.style.top = '12px'; return;
    }
    var sx = (+b.dataset.x - V.x) / V.w * r.width, sy = (+b.dataset.y - V.y) / V.h * r.height;
    var pw = c.offsetWidth, ph = c.offsetHeight, br = b.getBoundingClientRect();
    var bl = br.width ? br.left - r.left : sx - 30, bR = br.width ? br.right - r.left : sx + 30;
    var left = bR + 12, top = sy - ph / 2;                        // to the right of the label…
    if(left + pw > r.width - 8) left = bl - 12 - pw;             // …or to its left
    left = Math.max(8, Math.min(left, r.width - pw - 8));
    top = Math.max(8, Math.min(top, r.height - ph - 8));
    c.style.left = left.toFixed(0) + 'px'; c.style.top = top.toFixed(0) + 'px';
  }
  function closeCard(){
    sel = null; var c = document.getElementById('gcard'); c.hidden = true; c.innerHTML = '';
    var on = document.querySelectorAll('#gmap .on, .gside .on'); for(var i=0;i<on.length;i++) on[i].classList.remove('on');
    apply();
  }
  document.getElementById('gcard').addEventListener('click', function(e){
    if(e.target.closest('.gx')){ closeCard(); return; }
    var b = e.target.closest('[data-k]'); if(b) select(b.getAttribute('data-k'));
  });
  document.getElementById('gcard').addEventListener('wheel', function(e){ e.stopPropagation(); }, {passive:true});
  function slug(s){ return s.normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''); }
  function select(k, zoom){
    sel = k;
    var on = document.querySelectorAll('.on'); for(var i=0;i<on.length;i++) if(on[i].closest('#gmap, .gside')) on[i].classList.remove('on');
    var m = document.querySelectorAll('[data-k="' + k + '"]'); for(var j=0;j<m.length;j++) m[j].classList.add('on');
    card(k);
    var o = D.aocs[k] || D.subs[k] || D.regions[k];
    if(zoom!==false && o && D.aocs[k]){
      var va = bbView(o.bb, .6);
      if(W0 / va.w < AOCK){ var ca = {x:va.x + va.w/2, y:va.y + va.h/2}, wa = W0 / AOCK * .98, ha = wa * .75; va = {x:ca.x - wa/2, y:ca.y - ha/2, w:wa, h:ha}; }
      goTo(va);
    } else if(zoom!==false && o){
      var v = bbView(o.bb, D.subs[k] ? .45 : .12);
      if(D.subs[k] && W0 / v.w < SUBK){ var c = {x:v.x + v.w/2, y:v.y + v.h/2}, w = W0 / SUBK * .98, hh = w * .75; v = {x:c.x - w/2, y:c.y - hh/2, w:w, h:hh}; }
      if(!D.subs[k] && W0 / v.w < SUBK && o.subs.length > 1){ var c2 = {x:v.x + v.w/2, y:v.y + v.h/2}, w2 = W0 / SUBK * .98, h2 = w2 * .75; v = {x:c2.x - w2/2, y:c2.y - h2/2, w:w2, h:h2}; }
      goTo(v);
    } else apply();
  }
  document.addEventListener('fw:lang', function(){ if(sel) card(sel); });
  function tips(){ var l = LANG(), b = stage.querySelectorAll('[data-tip-fr]');
    for(var i=0;i<b.length;i++){ var t = b[i].getAttribute('data-tip-' + l); b[i].title = t; b[i].setAttribute('aria-label', t); } }
  tips();
  new MutationObserver(function(){ tips(); if(sel) card(sel); }).observe(document.documentElement, {attributes:true, attributeFilter:['lang']});
  document.getElementById('langbtn') && document.getElementById('langbtn').addEventListener('click', function(){ setTimeout(function(){ if(sel) card(sel); }, 0); });

  // ------------------------------------------------------------ pointer: drag, pinch, click
  var pts = {}, moved = false, last = null, pinch0 = null;
  svg.addEventListener('pointerdown', function(e){
    svg.setPointerCapture(e.pointerId); pts[e.pointerId] = {x:e.clientX, y:e.clientY}; moved = false;
    if(anim){ cancelAnimationFrame(anim); anim = null; }
    var ids = Object.keys(pts);
    if(ids.length===2){ var a = pts[ids[0]], b = pts[ids[1]]; pinch0 = {d:Math.hypot(a.x-b.x, a.y-b.y), w:V.w}; }
    last = {x:e.clientX, y:e.clientY};
  });
  svg.addEventListener('pointermove', function(e){
    if(!pts[e.pointerId]) return;
    pts[e.pointerId] = {x:e.clientX, y:e.clientY};
    var ids = Object.keys(pts), r = stage.getBoundingClientRect();
    if(ids.length===2 && pinch0){
      var a = pts[ids[0]], b = pts[ids[1]], d = Math.hypot(a.x-b.x, a.y-b.y);
      zoomAt(V.w / (pinch0.w * pinch0.d / d), (a.x+b.x)/2, (a.y+b.y)/2); moved = true; return;
    }
    var dx = e.clientX - last.x, dy = e.clientY - last.y;
    if(Math.abs(dx) + Math.abs(dy) > 2) moved = true;
    if(moved){ svg.classList.add('drag'); V.x -= dx / r.width * V.w; V.y -= dy / r.height * V.h; apply(); }
    last = {x:e.clientX, y:e.clientY};
  });
  function up(e){
    delete pts[e.pointerId]; pinch0 = null; svg.classList.remove('drag');
    if(!moved && e.type==='pointerup'){
      var t = document.elementFromPoint(e.clientX, e.clientY), el = t && t.closest && t.closest('[data-k]');
      if(el && svg.contains(el)) select(el.getAttribute('data-k'));
      else if(sel) closeCard();
    }
  }
  svg.addEventListener('pointerup', up); svg.addEventListener('pointercancel', up);
  svg.addEventListener('wheel', function(e){ e.preventDefault(); if(anim){ cancelAnimationFrame(anim); anim = null; } zoomAt(Math.exp(-e.deltaY * .0022), e.clientX, e.clientY); }, {passive:false});
  svg.addEventListener('dblclick', function(e){ zoomAt(2, e.clientX, e.clientY); });

  document.getElementById('z-in').addEventListener('click', function(){ var c = {x:V.x+V.w/2, y:V.y+V.h/2}; goTo({x:c.x - V.w/4, y:c.y - V.h/4, w:V.w/2, h:V.h/2}, 350); });
  document.getElementById('z-out').addEventListener('click', function(){ var c = {x:V.x+V.w/2, y:V.y+V.h/2}; goTo({x:c.x - V.w, y:c.y - V.h, w:V.w*2, h:V.h*2}, 350); });
  document.getElementById('z-home').addEventListener('click', function(){ closeCard(); home(); });
  document.getElementById('z-full').addEventListener('click', function(){
    var d = document; if(d.fullscreenElement){ d.exitFullscreen(); } else if(stage.requestFullscreen){ stage.requestFullscreen(); }
  });
  document.querySelector('.gside').addEventListener('click', function(e){ var b = e.target.closest('[data-k]'); if(b){ select(b.getAttribute('data-k')); if(window.innerWidth <= 980) stage.scrollIntoView({behavior:'smooth'}); } });
  window.addEventListener('resize', function(){ V = fit(V); apply(); });
  document.addEventListener('fullscreenchange', function(){ setTimeout(function(){ V = fit(V); apply(); }, 60); });

  V = fit({x:60, y:-4, w:600, h:548}); apply();
  var h0 = decodeURIComponent(location.hash.slice(1));
  if(h0 && (D.subs[h0] || D.regions[h0] || D.aocs[h0])) select(h0);
})();
'''

if __name__ == '__main__':
    build()
