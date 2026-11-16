"""Builds Infos/Geography/Drawing_France.html — « L'importance de la géographie » / "The Importance of Geography".

An animated, seekable "film" made from the user's deck « regions/Drawing France the Easy way.pptx »:
France in numbers → the rivers and the wines along them → drawing France from a hexagon
(guides, rivers, cities, wine regions) → the real map.

Everything is a pure function of the time t, so play / pause / rewind / scrub / chapter jumps are exact.
- maps: the deck's relief maps; river layers are extracted as transparent overlays (difference with the base map)
- drawing: geometry read from the pptx shapes (slides 11, 14, 18) by pptx_geom.py, redrawn as SVG strokes
Run:  python3 gen_page.py
"""
import json
import math
import re
import sys
import zipfile
from io import BytesIO
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

HERE = Path(__file__).resolve().parent
INFOS = HERE.parent.parent
REPO = INFOS.parent
sys.path.insert(0, str(INFOS / 'Vine_and_Vineyard' / '_source'))
sys.path.insert(0, str(HERE))
from common import base_css, att  # noqa: E402
import pptx_geom as G  # noqa: E402

PPTX = REPO.parent.parent / 'regions' / 'Drawing France the Easy way.pptx'
OUTDIR = INFOS / 'Geography'
OUT = OUTDIR / 'Drawing_France.html'
IMG = OUTDIR / 'img'
VER = '1'
DIM = ' class="dim"'

# map placement in the 720 x 540 stage (slide points); the deck's maps are 1057 x 1252 px
MX, MY, MW, MH = 132.5, 0.5, 455.0, 539.0
SLIDE_MAP_X = 264  # where the map sat on the original slides


def f(v):
    return ('%.1f' % v).rstrip('0').rstrip('.')


def A(tin, dur, fx, out=None, extra=''):
    s = '%s,%s,%s' % (f(tin), f(dur), fx)
    if out is not None:
        s += ',' + f(out)
    return f' data-a="{s}"{extra}'


def tr(fr, en, tag='span', cls='', extra=''):
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c}{extra} data-fr="{att(fr)}" data-en="{att(en)}">{fr}</{tag}>'


# ------------------------------------------------------------------ images
def load(zf, i):
    return Image.open(BytesIO(zf.read(f'ppt/media/image{i}.jpeg'))).convert('RGB')


def save_webp(im, name, w=910, q=80):
    h = round(im.height * w / im.width)
    im.resize((w, h), Image.LANCZOS).save(IMG / name, 'WEBP', quality=q, method=6)




# ------------------------------------------------------------------ timeline
class TL:
    def __init__(self):
        self.t = 0.0
        self.scenes = []      # dicts: id, chap, start, end
        self.chapters = []    # dicts: id, fr, en, start
        self.svg = {'maps': [], 'final': []}
        self.cards = []
        self.notes = []

    def chapter(self, cid, fr, en):
        self.chapters.append(dict(id=cid, fr=fr, en=en, start=round(self.t, 2)))


tl = TL()
LEG = '<sup class="n">%s</sup>'


def item(t, fr, en, hl=(), cls=''):
    h = f' data-hl="{" ".join(hl)}"' if hl else ''
    c = f' {cls}' if cls else ''
    return (f'<li class="it{c}"{A(t, .6, "rise")}{h} data-fr="{att(fr)}" data-en="{att(en)}" tabindex="0">{fr}</li>')


def notes_block(sid, start, end, kicker, title, body, legend=''):
    n = len(tl.chapters)
    kicker = (f'Chapitre {n:02d}', f'Chapter {n:02d}')
    tl.notes.append(
        f'<section class="nb" data-s="{f(start)},{f(end)}" id="nb-{sid}">'
        f'{tr(kicker[0], kicker[1], "p", "kick")}{tr(title[0], title[1], "h3")}{legend}<ol class="its">{"".join(body)}</ol></section>')


def card(tin, tout, fr, en, sub=None, cls=''):
    s = tr(sub[0], sub[1], 'p', 'csub') if sub else ''
    c = f' {cls}' if cls else ''
    tl.cards.append(f'<div class="card{c}"{A(tin, .7, "fade", tout)}>{tr(fr, en, "p", "ctitle")}{s}</div>')


# ================================================================ PART 1 — the hydrographic basins
# Base map + rivers come from the HQ pipeline (GeoJson Files/Geography_Rivers/hq: build_hq.py then film_assets.py):
# film_map.webp = river-less relief map; film_geo.json = rivers (mouth → source), basins, named places, in stage units.
GEO_DIR = REPO.parent.parent / 'GeoJson Files' / 'Geography_Rivers' / 'hq' / 'film'
RW = {1: (1.0, 2.8), 2: (.75, 2.0), 3: (.6, 1.4)}      # stroke width at the source / at the mouth, by rank
GEO = {}
RIV = {'chunks': {}, 'bdone': set(), 'defs': [], 'halo': [], 'line': [], 'top': []}               # river halos under every stroke; markers & labels on top


def load_geo():
    import shutil
    GEO.update(json.load(open(GEO_DIR / 'film_geo.json', encoding='utf-8')))
    GEO['mtn'] = json.load(open(GEO_DIR / 'film_mountains.json', encoding='utf-8'))
    shutil.copyfile(GEO_DIR / 'film_map.webp', IMG / 'map_relief.webp')
    from scipy.spatial import cKDTree
    GEO['tree'] = cKDTree(np.vstack([np.asarray(r['pts']) for r in GEO['rivers'].values()]))
    dense = []
    for r in GEO['rivers'].values():
        P = np.asarray(r['pts'])
        for a, b in zip(P[:-1], P[1:]):
            n = max(1, int(np.hypot(*(b - a)) / 1.5))
            dense.extend(a + (b - a) * k / n for k in range(n))
    GEO['dense'] = cKDTree(np.asarray(dense))
    R_ = json.load(open(GEO_DIR.parent / 'rivers_px.json', encoding='utf-8'))
    GEO['rp'] = {k: R_[k] for k in ('W', 'H', 'scale', 'Emin', 'Nmax', 'margin')}
    # Corsica: same scale, true east-west position, moved north just enough to fit in the frame
    C = json.load(open(GEO_DIR / 'film_corsica.json', encoding='utf-8'))
    shutil.copyfile(GEO_DIR / 'film_corsica.webp', IMG / 'map_corsica.webp')
    GEO['corse_dy'] = GEO['corse_dx'] = 0.0
    x, y = l93_stage(C['Emin'] - C['margin'] / C['scale'], C['Nmax'] + C['margin'] / C['scale'])
    Kf = 540.0 / (GEO['rp']['H'] - 200)
    w, h = C['W'] * Kf, C['H'] * Kf
    # inset: same scale, moved into the frame (bottom-right corner)
    GEO['corse_dx'] = min(0.0, 704 - (x + w))
    GEO['corse_dy'] = min(0.0, 536 - (y + h))
    GEO['corse'] = (x + GEO['corse_dx'], y + GEO['corse_dy'], w, h)


def l93_stage(E, N):
    R_ = GEO['rp']
    Kf = 540.0 / (R_['H'] - 200)
    x0, y0 = GEO['place'][:2]
    return (((E - R_['Emin']) * R_['scale'] + R_['margin'] - 100) * Kf + x0,
            ((R_['Nmax'] - N) * R_['scale'] + R_['margin'] - 100) * Kf + y0)


_TRF = []


def ll(lon, lat):
    """lon/lat → stage units (Corsica moved with its image)"""
    if not _TRF:
        from pyproj import Transformer
        _TRF.append(Transformer.from_crs(4326, 2154, always_xy=True))
    x, y = l93_stage(*_TRF[0].transform(lon, lat))
    if lon > 8.3 and lat < 43.2:
        x += GEO['corse_dx']; y += GEO['corse_dy']
    return x, y


def relief_img():
    x, y, w, h = GEO['place']
    cx, cy, cw, ch = GEO['corse']
    return (f'<image href="img/map_relief.webp?v={VER}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" preserveAspectRatio="none"/>'
            f'<image href="img/map_corsica.webp?v={VER}" x="{f(cx)}" y="{f(cy)}" width="{f(cw)}" height="{f(ch)}" preserveAspectRatio="none"/>')


def _cum(P):
    d = np.r_[0, np.cumsum(np.hypot(*np.diff(P, axis=0).T))]
    return d


def draw_river(name, tin, dur, chunks=6):
    """The river draws itself from its source down to the sea, in chunks that widen downstream."""
    r = GEO['rivers'][name]
    P, T = np.asarray(r['pts'])[::-1], np.asarray(r['t'])[::-1]     # stored mouth → source; drawn source → sea
    w0, w1 = RW[r['rank']]
    d = _cum(P); L = d[-1]
    n = max(2, min(chunks, int(L // 25) + 1))
    cuts = [int(np.searchsorted(d, L * k / n)) for k in range(n)] + [len(P) - 1]
    for k in range(n):
        i, j = cuts[k], max(cuts[k + 1], cuts[k] + 1)
        seg = P[i:j + 1]
        if len(seg) < 2:
            continue
        w = w0 + (w1 - w0) * float(T[i:j + 1].mean())
        a, b = d[i] / L, d[j] / L
        sl = _cum(seg)[-1]
        dd = 'M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in seg)
        t1, du = tin + dur * a, max(.05, dur * (b - a))
        pid = f'p{len(RIV["defs"])}'
        RIV['defs'].append(f'<path id="{pid}" d="{dd}"/>')
        RIV['chunks'].setdefault(name, []).append((pid, w))
        RIV['halo'].append(f'<use href="#{pid}" class="rh" style="stroke-width:{w + 1.5:.2f}" data-len="{sl:.1f}"{A(t1, du, "line")}/>')
        RIV['line'].append(f'<use href="#{pid}" class="rv" style="stroke-width:{w:.2f}" data-len="{sl:.1f}"{A(t1, du, "line")}/>')


def at(name, frac, off=8.0):
    """Point beside a river at a fraction of its length (mouth = 0), on the side with fewer rivers."""
    P = np.asarray(GEO['rivers'][name]['pts'])
    d = _cum(P); s = d[-1] * frac
    k = min(len(P) - 2, int(np.searchsorted(d, s)))
    p = P[k]; v = P[min(k + 3, len(P) - 1)] - P[max(k - 3, 0)]
    nv = np.array([-v[1], v[0]]) / (np.hypot(*v) or 1)
    cands = [p + nv * off, p - nv * off]
    return max(cands, key=lambda c: GEO['tree'].query(c)[0])


OBS = []      # boxes the persistent names must avoid: (x0, y0, x1, y1, weight)
LBL = []      # persistent names (countries, mountains, cities), placed at the end by place_names()


def marker(mid, n, xy, tin, out):
    x, y = xy
    OBS.append((x - 7.5, y - 7.5, x + 7.5, y + 7.5, 1.0))
    RIV['top'].append(f'<g class="num" id="{mid}" data-c="{f(x)},{f(y)}"{A(tin, .5, "pop", out)}>'
                      f'<circle cx="{f(x)}" cy="{f(y)}" r="6.8"/><text x="{f(x)}" y="{f(y + .4)}">{n}</text></g>')


def rlabel(fr, en, xy, tin, out=None, cls='rname'):
    x, y = xy
    w = len(fr) * 11 * .5 / 2 + 2
    OBS.append((x - w, y - 7.5, x + w, y + 7.5, 3.0))
    RIV['top'].append(f'<text class="{cls}" x="{f(x)}" y="{f(y)}" data-c="{f(x)},{f(y)}" data-fr="{att(fr)}" data-en="{att(en)}"'
                      f'{A(tin, .8, "pop", out)}>{fr}</text>')


def basin_ref(name):
    """Each basin outline is stored once in <defs> (plus a mask that dims everything outside it) and reused."""
    bid = 'b' + str(list(GEO['basins']).index(name))
    if bid not in RIV['bdone']:
        RIV['bdone'].add(bid)
        RIV['defs'].append(f'<path id="{bid}" d="{ring_path(GEO["basins"][name])}"/>'
                           f'<mask id="m{bid}" maskUnits="userSpaceOnUse" x="-10" y="-10" width="740" height="560">'
                           f'<rect x="-10" y="-10" width="740" height="560" fill="#fff"/><use href="#{bid}" fill="#000"/></mask>')
    return bid


def ring_path(rings):
    return ''.join('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in r) + 'Z' for r in rings)


# ---------------------------------------------------------------- 1. intro
def scene_intro():
    t0 = tl.t
    tl.chapter('intro', 'Introduction', 'Introduction')
    dur = 9
    card(t0 - .7, t0 + dur - .4, 'L’importance de la <em>géographie</em>', 'The importance of <em>geography</em>',
         ('Les fleuves expliquent les vignobles : suivez l’eau, vous trouverez le vin.',
          'Rivers explain the vineyards: follow the water and you will find the wine.'), 'hero')
    notes_block('intro', t0, t0 + dur, ('Prologue', 'Prologue'), ('Pourquoi la géographie ?', 'Why geography?'), [
        item(t0 + .5, 'Pendant des siècles, le vin a voyagé par l’eau : les vignobles se sont installés le long des fleuves, près des ports et des villes.',
             'For centuries wine travelled by water: vineyards grew up along rivers, close to ports and towns.'),
        item(t0 + 4.5, 'Retenez cinq fleuves et leurs affluents, et vous saurez situer presque toutes les régions viticoles françaises.',
             'Learn five rivers and their tributaries, and you can place almost every French wine region.')])
    tl.scenes.append(dict(id='intro', start=t0, end=t0 + dur))
    tl.t += dur


# ---------------------------------------------------------------- 2. France in numbers
NAMES = {'Manche': ('La Manche', 'The Channel'), 'Mer du Nord': ('Mer du Nord', 'North Sea'),
         'Atlantique': ('Océan<br>Atlantique', 'Atlantic<br>Ocean'), 'Méditerranée': ('Mer Méditerranée', 'Mediterranean Sea'),
         'Belgique': ('BELGIQUE', 'BELGIUM'), 'Luxembourg': ('LUX.', 'LUX.'), 'Allemagne': ('ALLEMAGNE', 'GERMANY'),
         'Suisse': ('SUISSE', 'SWITZERLAND'), 'Italie': ('ITALIE', 'ITALY'), 'Espagne': ('ESPAGNE', 'SPAIN'),
         'Andorre': ('AND.', 'AND.'), 'Monaco': ('MON.', 'MON.'),
         'Alpes': ('Alpes', 'Alps'), 'Pyrénées': ('Pyrénées', 'Pyrenees'), 'Massif central': ('Massif<br>central', 'Massif<br>Central'),
         'Jura': ('Jura', 'Jura'), 'Vosges': ('Vosges', 'Vosges')}


def place_label(key, cls, tin, out, dx=0, dy=0):
    x, y = GEO['labels'][key]
    x += dx; y += dy
    fr, en = NAMES[key]

    def lines(s):
        parts = s.split('<br>')
        return ''.join(f'<tspan x="{f(x)}" dy="{("%.2fem" % (-(len(parts) - 1) * .55)) if k == 0 else "1.1em"}">{p}</tspan>' for k, p in enumerate(parts))
    return (f'<text class="{cls}" x="{f(x)}" y="{f(y)}" data-c="{f(x)},{f(y)}" data-fr="{att(lines(fr))}" data-en="{att(lines(en))}"'
            f'{A(tin, .7, "pop", out)}>{lines(fr)}</text>')


def scene_numbers():
    t0 = tl.t
    tl.chapter('chiffres', 'La France en chiffres', 'France in numbers')
    its, t = [], t0 + .6
    rows = [
        ('<b>Superficie :</b> 551 695 km² (France métropolitaine, Corse comprise), soit environ 213 000 miles carrés — à peu près les quatre cinquièmes du Texas.',
         '<b>Area:</b> 551,695 km² (mainland France including Corsica), about 213,000 square miles — roughly four-fifths the size of Texas.', None),
        ('<b>Population :</b> 66,8 millions d’habitants en métropole, 69,1 millions avec l’outre-mer (Insee, 1<sup>er</sup> janvier 2026).',
         '<b>Population:</b> 66.8 million in mainland France, 69.1 million including the overseas departments (Insee, 1 January 2026).', None),
        ('<b>Mers :</b> la France s’ouvre sur la mer du Nord, la Manche, l’océan Atlantique et la Méditerranée — environ 3 430 km de côtes (≈ 2 130 miles).',
         '<b>Seas:</b> France opens onto the North Sea, the Channel, the Atlantic Ocean and the Mediterranean — about 3,430 km of coastline (≈ 2,130 miles).',
         ('sea', ['Manche', 'Atlantique', 'Méditerranée'])),
        ('<b>Voisins :</b> 8 pays — Belgique, Luxembourg, Allemagne, Suisse, Italie, Monaco, Andorre, Espagne — et environ 2 750 km de frontières terrestres (≈ 1 710 miles).',
         '<b>Neighbours:</b> 8 countries — Belgium, Luxembourg, Germany, Switzerland, Italy, Monaco, Andorra, Spain — and about 2,750 km of land borders (≈ 1,710 miles).',
         ('country', ['Belgique', 'Luxembourg', 'Allemagne', 'Suisse', 'Italie', 'Espagne'])),
        ('<b>Grandes villes :</b> Paris, Marseille, Lyon, Toulouse, Nice et Nantes — les six communes les plus peuplées.',
         '<b>Major cities:</b> Paris, Marseille, Lyon, Toulouse, Nice and Nantes — the six most populous communes.', 'majors'),
        ('<b>Montagnes :</b> les Alpes, les Pyrénées, le Massif central, le Jura et les Vosges.',
         '<b>Mountains:</b> the Alps, the Pyrenees, the Massif Central, the Jura and the Vosges.',
         None),
        ('<b>Cinq grands fleuves</b> — la Seine, le Rhin, la Loire, le Rhône et la Garonne — et <b>six grands bassins hydrographiques</b> en métropole.',
         '<b>Five great rivers</b> — the Seine, the Rhine, the Loire, the Rhône and the Garonne — and <b>six great river basins</b> in mainland France.', 'basins'),
        ('<b>Découpage administratif :</b> 13 régions en métropole (18 avec l’outre-mer) depuis 2016, 96 départements métropolitains (101 au total), environ 2 000 cantons et 34 875 communes (2026).',
         '<b>Administrative divisions:</b> 13 regions in mainland France (18 with the overseas regions) since 2016, 96 mainland départements (101 in all), about 2,000 cantons and 34,875 communes (2026).', None),
    ]
    marks = []
    t_basins = None
    for fr, en, lab in rows:
        its.append(item(t, fr, en))
        if lab == 'basins':
            t_basins = t
        elif lab == 'majors':
            for k, (nm, lo, la) in enumerate(MAJORS):
                LBL.append(dict(kind='major', fr=nm, en=nm, xy=ll(lo, la), tin=t + .4 + k * .3))
        elif lab and lab[0] == 'country':
            for k, key in enumerate(lab[1]):
                LBL.append(dict(kind='country', fr=NAMES[key][0], en=NAMES[key][1], xy=tuple(GEO['labels'][key]), tin=t + .4 + k * .3))
        elif lab:
            cls, keys = lab
            for k, key in enumerate(keys):
                marks.append(place_label(key, cls, t + .4 + k * .3, None))
        t += 6.2 if lab else 5.2
    end = t + 2
    # labels stay until the end of the chapter
    marks = [m.replace(',pop"', f',pop,{f(end - .6)}"') for m in marks]
    outlines = ''.join(f'<use href="#{basin_ref(bn)}" class="bline"{A(t_basins + .4 + k * .25, 1, "fade", end - .6)}/>'
                       for k, bn in enumerate(GEO['basins']))
    tl.svg['maps'].append(f'<g class="scene" data-s="{f(t0)},{f(end)}">{outlines}{"".join(marks)}</g>')
    notes_block('chiffres', t0, end, None, ('La France en chiffres', 'France in numbers'), its)
    tl.scenes.append(dict(id='chiffres', start=t0, end=end))
    tl.t = end


# ---------------------------------------------------------------- 3. the mountains (the rivers start there)
MOUNTAINS = [
    ('Alpes', ('Les Alpes', 'The Alps'), ('Mont Blanc', 'Mont Blanc'), '≈ 4 806 m',
     ('<b>Les Alpes</b> — la plus haute chaîne d’Europe occidentale, couronnée par le mont Blanc (≈ 4 806 m). Leurs glaciers et leurs neiges nourrissent l’Isère et la Durance… et donc le Rhône.',
      '<b>The Alps</b> — the highest range in Western Europe, crowned by Mont Blanc (≈ 4,806 m). Their glaciers and snows feed the Isère and the Durance… and so the Rhône.')),
    ('Pyrénées', ('Les Pyrénées', 'The Pyrenees'), ('Vignemale', 'Vignemale'), '3 298 m',
     ('<b>Les Pyrénées</b> — une muraille de 430 km entre la France et l’Espagne ; côté français, le point culminant est le Vignemale (3 298 m). Elles donnent naissance à la Garonne, à l’Adour et aux gaves.',
      '<b>The Pyrenees</b> — a 430-km wall between France and Spain; on the French side, the highest summit is the Vignemale (3,298 m). The Garonne, the Adour and the gaves are born here.')),
    ('Massif central', ('Le Massif central', 'The Massif Central'), ('Puy de Sancy', 'Puy de Sancy'), '1 885 m',
     ('<b>Le Massif central</b> — un vieux massif aux volcans éteints, culminant au puy de Sancy (1 885 m). C’est le grand château d’eau du pays : la Loire, l’Allier, le Cher, la Vienne, la Creuse, la Dordogne, le Lot et le Tarn y prennent leur source.',
      '<b>The Massif Central</b> — an ancient upland of extinct volcanoes, topped by the Puy de Sancy (1,885 m). It is the country’s great water tower: the Loire, Allier, Cher, Vienne, Creuse, Dordogne, Lot and Tarn all rise here.')),
    ('Jura', ('Le Jura', 'The Jura'), ('Crêt de la Neige', 'Crêt de la Neige'), '1 720 m',
     ('<b>Le Jura</b> — des plis calcaires en arc le long de la Suisse, jusqu’au crêt de la Neige (1 720 m). Le Doubs et l’Ain y naissent avant de rejoindre la Saône et le Rhône.',
      '<b>The Jura</b> — limestone folds curving along the Swiss border, up to the Crêt de la Neige (1,720 m). The Doubs and the Ain rise here before joining the Saône and the Rhône.')),
    ('Vosges', ('Les Vosges', 'The Vosges'), ('Grand Ballon', 'Grand Ballon'), '1 424 m',
     ('<b>Les Vosges</b> — des « ballons » arrondis face à la plaine d’Alsace, jusqu’au Grand Ballon (1 424 m). La Moselle y prend sa source.',
      '<b>The Vosges</b> — rounded “ballons” facing the Alsace plain, up to the Grand Ballon (1,424 m). The Moselle rises here.')),
]


def scene_mountains():
    t0 = tl.t
    tl.chapter('montagnes', 'Les montagnes', 'The mountains')
    t = t0 + .6
    its = [item(t, 'Avant les fleuves, les montagnes : c’est là que tombent la pluie et la neige, et c’est là que les fleuves prennent leur source.',
                'Before the rivers, the mountains: that is where rain and snow fall, and where the rivers rise.')]
    t += 5
    shapes, tops = [], []
    for key, name, peak, alt, txt in MOUNTAINS:
        its.append(item(t, *txt))
        d = ''.join('M' + 'L'.join(f'{x:.1f},{y:.1f}' for x, y in r) + 'Z' for r in GEO['mtn']['ranges'][key])
        shapes.append(f'<path class="mtn" d="{d}"{A(t + .2, 1.4, "fade")}/>')
        x, y = GEO['labels'][key]
        LBL.append(dict(kind='mount', fr=NAMES[key][0], en=NAMES[key][1], xy=tuple(GEO['labels'][key]), tin=t + .5))
        px, py = GEO['mtn']['peaks'][key]
        left = px > 560 or key == 'Pyrénées'
        alt_en = re.sub(r'(\d) (\d)', r'\1,\2', alt)
        tx = px - 6 if left else px + 6
        anc = ' style="text-anchor:end"' if left else ''
        tops.append(f'<g class="peak" data-c="{f(px)},{f(py)}"{A(t + 1.1, .6, "pop")}>'
                    f'<path d="M{f(px)},{f(py - 4.2)}L{f(px + 4)},{f(py + 2.6)}L{f(px - 4)},{f(py + 2.6)}Z"/>'
                    f'<text x="{f(tx)}" y="{f(py)}"{anc} data-fr="{att(peak[0] + " " + alt)}" data-en="{att(peak[1] + " " + alt_en)}">{peak[0]} {alt}</text></g>')
        t += 7
    its.append(item(t, 'Ce sont les <b>châteaux d’eau</b> de la France : presque tous les grands fleuves descendent de ces cinq massifs. Seule la Seine fait exception : elle naît sur le modeste plateau de Langres.',
                    'These are France’s <b>water towers</b>: almost every great river comes down from these five ranges. The Seine is the exception: it rises on the modest Langres plateau.'))
    t += 7
    its.append(item(t, 'Leurs piémonts abritent aussi des vignobles : l’Alsace au pied des Vosges, le Jura, la Savoie dans les Alpes, Jurançon et Irouléguy au pied des Pyrénées, les Côtes d’Auvergne dans le Massif central.',
                    'Their foothills shelter vineyards too: Alsace at the foot of the Vosges, the Jura, Savoie in the Alps, Jurançon and Irouléguy at the foot of the Pyrenees, Côtes d’Auvergne in the Massif Central.'))
    end = t + 7
    tl.svg['maps'].append(f'<g class="scene" data-s="{f(t0)},{f(end)}">{"".join(shapes)}{"".join(tops)}</g>')
    notes_block('montagnes', t0, end, None, ('Les montagnes', 'The mountains'), its)
    tl.scenes.append(dict(id='montagnes', start=t0, end=end))
    tl.t = end


# ---------------------------------------------------------------- 4. the basins
def scene_rivers_title():
    t0 = tl.t
    tl.chapter('fleuves', 'L’importance des fleuves', 'Why rivers matter')
    dur = 9
    card(t0, t0 + dur - .4, 'L’importance des <em>fleuves</em>… et de leurs affluents', 'The importance of <em>rivers</em>… and their tributaries',
         ('Bassin par bassin, suivons chaque fleuve de sa source jusqu’à la mer et voyons quels vins poussent sur ses rives.',
          'Basin by basin, let’s follow each river from its source to the sea and see which wines grow along its banks.'))
    notes_block('fleuves', t0, t0 + dur, None, ('Les fleuves', 'The rivers'), [
        item(t0 + .8, 'Un fleuve se jette dans la mer ; ses affluents se jettent dans le fleuve. Toutes les terres dont les eaux finissent dans le même fleuve forment son <b>bassin versant</b>.',
             'A river (<i>fleuve</i>) flows into the sea; its tributaries flow into the river. All the land whose water ends up in the same river forms its <b>basin</b>.'),
        item(t0 + 5, 'La France métropolitaine compte six grands bassins hydrographiques. Chaque rivière se dessine de sa source jusqu’à la mer, et chaque bassin reste sur la carte.',
             'Mainland France has six great river basins. Each river draws itself from its source down to the sea, and each basin stays on the map.')])
    tl.scenes.append(dict(id='fleuves', start=t0, end=t0 + dur))
    tl.t += dur


MAJORS = [('Paris', 2.352, 48.857), ('Marseille', 5.370, 43.296), ('Lyon', 4.835, 45.764), ('Toulouse', 1.444, 43.605),
          ('Nice', 7.262, 43.710), ('Nantes', -1.554, 47.218)]
TOWNS = {   # wine towns, shown in their basin's chapter
    'garonne': [('Bordeaux', -0.579, 44.838), ('Saint-Émilion', -0.155, 44.894), ('Bergerac', 0.483, 44.853), ('Cahors', 1.441, 44.448),
                ('Cognac', -0.329, 45.696), ('Pau', -0.370, 43.295)],
    'loire': [('Angers', -0.554, 47.478), ('Saumur', -0.077, 47.260), ('Tours', 0.689, 47.394), ('Sancerre', 2.837, 47.331)],
    'seine': [('Reims', 4.032, 49.258), ('Épernay', 3.955, 49.040), ('Chablis', 3.800, 47.815)],
    'nord': [],
    'rhin': [('Strasbourg', 7.752, 48.573), ('Colmar', 7.358, 48.079)],
    'rhone': [('Dijon', 5.041, 47.322), ('Beaune', 4.840, 47.024), ('Mâcon', 4.832, 46.307), ('Arbois', 5.774, 46.903),
              ('Chambéry', 5.918, 45.564), ('Avignon', 4.806, 43.949), ('Montpellier', 3.877, 43.611), ('Narbonne', 3.004, 43.184),
              ('Perpignan', 2.895, 42.699)],
    'corse': [('Patrimonio', 9.364, 42.704)],
    'corse_major': [('Ajaccio', 8.737, 41.919), ('Bastia', 9.450, 42.697)],
}


def basin(sid, bname, chap, title, main, main_lab, main_txt, trib_head, tribs, wines, extra_labels=()):
    """Spotlight on one basin → main river draws from its mouth → numbered tributaries one by one → wines."""
    t0 = tl.t
    tl.chapter(sid, *chap)
    bid = basin_ref(bname)
    t = t0 + .8
    its = [item(t, *main_txt)]
    rv = ([(main, main_lab[0], main_lab[1])] if main else []) + [(riv, fr, en) for fr, en, riv, _f in tribs if riv != main]
    EXPLORE.append(dict(bname=bname, title=title, intro=main_txt, rivers=rv, tribs=[r for _a, _b, r, _f in tribs], wines=wines))
    if main:
        L = GEO['rivers'][main]['len']
        dmain = min(6.5, max(3.5, L / 70))
        draw_river(main, t + .3, dmain)
        rlabel(main_lab[0], main_lab[1], at(main, main_lab[2], 11), t + .3 + dmain * (1 - main_lab[2]))
        t += max(5.4, dmain + 1.4)
    for fr, en, key in extra_labels:
        x, y = GEO['labels'][key]
        rlabel(fr, en, (x, y), t0 + 1.2, None, 'rname')
    its.append(item(t, *trib_head))
    names = [(fr, en) for fr, en, _riv, _f in tribs]
    leg_i = len(its)
    its.append('')            # the legend, filled once the marker times are known
    tt = t + .4
    pops = []
    for k, (fr, en, riv, frac) in enumerate(tribs):
        L = GEO['rivers'][riv]['len']
        d = min(2.6, max(1.0, L / 60))
        if riv == main:          # the main river can also be numbered in the legend (already drawn)
            d = 0
        else:
            draw_river(riv, tt, d)
        pops.append(tt + d * (1 - frac))
        marker(f'{sid}-n{k + 1}-0', k + 1, at(riv, frac), pops[-1], 99999)
        tt += .9
    # each numbered chip in the side panel appears with its number on the map (and lights up with it)
    its[leg_i] = '<li class="legw">' + legend(names, pops, ids=[f'{sid}-n{k + 1}-leg' for k in range(len(names))]) + '</li>'
    t = max(tt + 1.2, t + 4)
    towns = TOWNS.get(sid, [])
    if towns:
        names_ = ', '.join(n for n, _a, _b in towns)
        its.append(item(t, f'<b>Villes du vin :</b> {names_}.', f'<b>Wine towns:</b> {names_}.'))
        for k, (nm, lo, la) in enumerate(towns):
            LBL.append(dict(kind='wine', fr=nm, en=nm, xy=ll(lo, la), tin=t + .4 + k * .25))
        t += 5
    num_name = {k + 1: (fr_, en_) for k, (fr_, en_, _r, _f) in enumerate(tribs)}

    def badges(txt, hl, lang):
        """Put each river's number (as on the map) just before the river's name; numbers whose name isn't in the line go first."""
        lead = ''
        for h in sorted(hl, key=int, reverse=True):
            nm = num_name.get(int(h), ('', ''))[lang]
            b = f'<span class="hlb">{h}</span>'
            i = txt.find(nm) if nm else -1
            if i < 0 and nm:            # « la Leyre » vs « Leyre », « d’Oloron »…: try the last word
                i = txt.find(nm.split()[-1])
            if i >= 0:
                j = txt.rfind('<b>', 0, i)          # keep the badge outside the bold run if the name opens it
                if j >= 0 and j + 3 == i:
                    i = j
                txt = txt[:i] + b + txt[i:]
            else:
                lead = b + lead
        return lead + txt
    for fr, en, hl in wines:
        its.append(item(t, badges(fr, hl, 0), badges(en, hl, 1), [f'{sid}-n{h}' for h in hl]))
        t += 5.8
    end = t + 2
    cap_k = tr('Bassin', 'Basin', 'text', 'bk', ' x="20" y="30"')
    cap_t = tr(title[0], title[1], 'text', 'bt', ' x="20" y="52"')
    RIV['top'][:] = [s.replace(',99999"', f',{f(end - .3)}"') for s in RIV['top']]
    tl.svg['maps'].append(
        f'<g class="scene" data-s="{f(t0)},{f(end)}">'
        f'<rect x="-10" y="-10" width="740" height="560" class="spot" mask="url(#m{bid})"{A(t0, 1.2, "fade", end - .5)}/>'
        f'<use href="#{bid}" class="bact"{A(t0 + .2, 1.2, "fade", end - .5)}/>'
        f'<g class="bcap"{A(t0 + .2, .8, "fade", end - .5)}>{cap_k}{cap_t}</g></g>')
    notes_block(sid, t0, end, None, title, its)
    tl.scenes.append(dict(id=sid, start=t0, end=end))
    tl.t = end


def legend(names, tin, step=.12, ids=None):
    """tin = start time (chips staggered by step) or one time per chip; ids make the chips light up with the map numbers."""
    times = tin if isinstance(tin, (list, tuple)) else [tin + k * step for k in range(len(names))]
    idat = [f' class="num" id="{i}"' for i in ids] if ids else [''] * len(names)
    lis = ''.join(f'<li{idat[k]}{A(times[k], .5, "rise")}><b>{k + 1}</b>{tr(fr, en)}</li>'
                  for k, (fr, en) in enumerate(names))
    return f'<ol class="leg">{lis}</ol>'


def rivers():
    basin('garonne', 'Adour-Garonne', ('Adour-Garonne', 'Adour–Garonne'), ('Adour-Garonne', 'Adour–Garonne'),
          'Garonne', ('Garonne', 'Garonne', .45),
          ('La Garonne descend des Pyrénées, passe à Toulouse et à Bordeaux, puis rejoint la Dordogne pour former l’estuaire de la Gironde.',
           'The Garonne comes down from the Pyrenees, flows past Toulouse and Bordeaux, then meets the Dordogne to form the Gironde estuary.'),
          ('Ses affluents, puis les fleuves voisins du même bassin :', 'Its tributaries, then the neighbouring rivers of the same basin:'),
          [('Dordogne', 'Dordogne', 'Dordogne', .3), ('Lot', 'Lot', 'Lot', .35), ('Tarn', 'Tarn', 'Tarn', .4),
           ('Gers', 'Gers', 'Gers', .4), ('Ariège', 'Ariège', 'Ariège', .45), ('Adour', 'Adour', 'Adour', .35),
           ('Gave de Pau', 'Gave de Pau', 'Gave de Pau', .5), ('Gave d’Oloron', 'Gave d’Oloron', "Gave d'Oloron", .25),
           ('Saison', 'Saison', 'Saison', .7), ('Leyre', 'Leyre', 'Leyre', .5), ('Charente', 'Charente', 'Charente', .35)],
          [('<b>Gironde</b> — rive gauche : Médoc et Haut-Médoc ; rive droite : Blaye et Bourg.',
            '<b>Gironde</b> — left bank: Médoc and Haut-Médoc; right bank: Blaye and Bourg.', []),
           ('<b>Dordogne</b> — Saint-Émilion, Pomerol, Fronsac : les vins de la « rive droite » ; plus en amont, Bergerac et Monbazillac.',
            '<b>Dordogne</b> — Saint-Émilion, Pomerol, Fronsac: the “Right Bank” wines; further upstream, Bergerac and Monbazillac.', ['1']),
           ('<b>Garonne, en aval de Langon</b> — les Graves, Pessac-Léognan, Sauternes et Barsac. <b>Entre Dordogne et Garonne</b> — l’Entre-deux-Mers.',
            '<b>Garonne, below Langon</b> — Graves, Pessac-Léognan, Sauternes and Barsac. <b>Between the Dordogne and the Garonne</b> — Entre-deux-Mers.', ['1']),
           ('<b>Lot</b> — Cahors. <b>Tarn</b> — Gaillac et, entre Tarn et Garonne, Fronton.',
            '<b>Lot</b> — Cahors. <b>Tarn</b> — Gaillac and, between the Tarn and the Garonne, Fronton.', ['2', '3']),
           ('<b>Gers et Adour</b> — Madiran, Saint-Mont, le floc de Gascogne et l’armagnac. <b>Gave de Pau</b> — Jurançon et Béarn.',
            '<b>Gers and Adour</b> — Madiran, Saint-Mont, Floc de Gascogne and Armagnac. <b>Gave de Pau</b> — Jurançon and Béarn.', ['4', '6', '7']),
           ('L’Adour (avec ses gaves), la Leyre et la Charente ont leur propre embouchure : ce ne sont pas des affluents de la Garonne, mais ils appartiennent au même bassin.',
            'The Adour (with its gaves), the Leyre and the Charente have their own mouths: they are not tributaries of the Garonne, but they belong to the same basin.', ['6', '10', '11']),
           ('<b>Charente</b> — le cognac et le pineau des Charentes.', '<b>Charente</b> — Cognac and Pineau des Charentes.', ['11'])],
          extra_labels=[('Gironde', 'Gironde', 'Gironde')])
    basin('loire', 'Loire-Bretagne', ('Loire-Bretagne', 'Loire–Brittany'), ('Loire-Bretagne', 'Loire–Brittany'),
          'Loire', ('Loire', 'Loire', .3),
          ('Le plus long fleuve de France (environ 1 000 km) naît dans le Massif central, remonte vers le nord jusqu’à Orléans, puis file vers l’ouest jusqu’à Nantes et l’Atlantique.',
           'France’s longest river (about 1,000 km) rises in the Massif Central, flows north to Orléans, then west to Nantes and the Atlantic.'),
          ('Ses affluents, de l’embouchure vers l’amont, puis deux fleuves côtiers :', 'Its tributaries, from the mouth upstream, then two coastal rivers:'),
          [('Layon', 'Layon', 'Layon', .5), ('Mayenne', 'Mayenne', 'Mayenne', .4), ('Sarthe', 'Sarthe', 'Sarthe', .7),
           ('Loir', 'Loir', 'Loir', .55), ('Vienne', 'Vienne', 'Vienne', .3), ('Creuse', 'Creuse', 'Creuse', .5),
           ('Indre', 'Indre', 'Indre', .45), ('Cher', 'Cher', 'Cher', .45), ('Allier', 'Allier', 'Allier', .35),
           ('Vilaine', 'Vilaine', 'Vilaine', .35), ('Sèvre niortaise', 'Sèvre Niortaise', 'Sèvre Niortaise', .5)],
          [('<b>Basse Loire</b> — le Muscadet, autour de Nantes.', '<b>Lower Loire</b> — Muscadet, around Nantes.', []),
           ('<b>Layon</b> — les liquoreux : Coteaux du Layon, Quarts de Chaume, Bonnezeaux.',
            '<b>Layon</b> — sweet wines: Coteaux du Layon, Quarts de Chaume, Bonnezeaux.', ['1']),
           ('<b>Loire moyenne</b> — l’Anjou et le Saumurois, puis la Touraine : Vouvray, Montlouis…',
            '<b>Middle Loire</b> — Anjou and Saumur, then Touraine: Vouvray, Montlouis…', []),
           ('<b>Loir</b> — Jasnières et Coteaux du Loir. <b>Vienne</b> — Chinon.', '<b>Loir</b> — Jasnières and Coteaux du Loir. <b>Vienne</b> — Chinon.', ['4', '5']),
           ('<b>Cher</b> — Quincy, Reuilly (sur l’Arnon, son affluent) et Touraine-Chenonceaux.',
            '<b>Cher</b> — Quincy, Reuilly (on its tributary, the Arnon) and Touraine-Chenonceaux.', ['8']),
           ('<b>Loire du Centre</b> — Sancerre, Pouilly-Fumé, Menetou-Salon…', '<b>Central Loire</b> — Sancerre, Pouilly-Fumé, Menetou-Salon…', []),
           ('<b>Allier</b> — Saint-Pourçain et Côtes d’Auvergne.', '<b>Allier</b> — Saint-Pourçain and Côtes d’Auvergne.', ['9'])])
    basin('seine', 'Seine-Normandie', ('Seine-Normandie', 'Seine–Normandy'), ('Seine-Normandie', 'Seine–Normandy'),
          'Seine', ('Seine', 'Seine', .2),
          ('La Seine naît sur le plateau de Langres, traverse Paris et se jette dans la Manche au Havre.',
           'The Seine rises on the Langres plateau, flows through Paris and reaches the Channel at Le Havre.'),
          ('Ses affluents, de l’embouchure vers l’amont :', 'Its tributaries, from the mouth upstream:'),
          [('Oise', 'Oise', 'Oise', .35), ('Aisne', 'Aisne', 'Aisne', .45), ('Marne', 'Marne', 'Marne', .4),
           ('Yonne', 'Yonne', 'Yonne', .35), ('Serein', 'Serein', 'Serein', .5), ('Aube', 'Aube', 'Aube', .45)],
          [('<b>Marne</b> — la Champagne : Montagne de Reims, vallée de la Marne, Côte des Blancs.',
            '<b>Marne</b> — Champagne: Montagne de Reims, Vallée de la Marne, Côte des Blancs.', ['3']),
           ('<b>Haute Seine et Aube</b> — la Côte des Bar, au sud de la Champagne.',
            '<b>Upper Seine and Aube</b> — the Côte des Bar, the southern part of Champagne.', ['6']),
           ('<b>Yonne</b> — Irancy et l’Auxerrois ; <b>Serein</b>, son affluent — Chablis.',
            '<b>Yonne</b> — Irancy and the Auxerrois; <b>Serein</b>, its tributary — Chablis.', ['4', '5'])])
    basin('nord', 'Artois-Picardie', ('Artois-Picardie', 'Artois–Picardy'), ('Artois-Picardie', 'Artois–Picardy'),
          None, None,
          ('Le plus petit bassin : des fleuves de plaine qui filent vers la Manche ou la mer du Nord.',
           'The smallest basin: lowland rivers heading for the Channel or the North Sea.'),
          ('Ses fleuves :', 'Its rivers:'),
          [('Somme', 'Somme', 'Somme', .45), ('Escaut', 'Scheldt (Escaut)', 'Escaut', .5), ('Lys', 'Lys', 'Lys', .5)],
          [('<b>Escaut et Lys</b> — ils traversent la Belgique pour rejoindre la mer du Nord à Anvers ; la Lys se jette dans l’Escaut à Gand.',
            '<b>Scheldt and Lys</b> — they cross Belgium to reach the North Sea at Antwerp; the Lys joins the Scheldt at Ghent.', ['2', '3']),
           ('Pas de grand vignoble ici : trop au nord pour l’AOC. Mais la bière, elle, y est reine.',
            'No great vineyards here: too far north for AOC wine. Beer, on the other hand, is king.', [])])
    basin('rhin', 'Rhin-Meuse', ('Rhin-Meuse', 'Rhine–Meuse'), ('Rhin-Meuse', 'Rhine–Meuse'),
          'Rhin', ('Rhin', 'Rhine', .5),
          ('Le Rhin marque la frontière avec l’Allemagne avant de filer vers la mer du Nord.',
           'The Rhine marks the border with Germany before heading for the North Sea.'),
          ('Les fleuves du bassin : le Rhin, le plus grand ; la Moselle, qui le rejoint en Allemagne à Coblence ; la Meuse, qui gagne la mer du Nord par la Belgique et les Pays-Bas :',
           'The basin’s rivers: the Rhine, the largest; the Moselle, which joins it in Germany at Koblenz; the Meuse, which reaches the North Sea through Belgium and the Netherlands:'),
          [('Rhin', 'Rhine', 'Rhin', .7), ('Moselle', 'Moselle', 'Moselle', .45), ('Meuse', 'Meuse', 'Meuse', .4)],
          [('<b>Rhin</b> — l’Alsace, tous types de vins, sur les collines au pied des Vosges qui dominent la plaine du Rhin.',
            '<b>Rhine</b> — Alsace, wines of every style, on the Vosges foothills overlooking the Rhine plain.', ['1']),
           ('<b>Moselle</b> — les Côtes de Toul et l’AOC Moselle.', '<b>Moselle</b> — Côtes de Toul and the Moselle AOC.', ['2'])])
    basin('rhone', 'Rhône-Méditerranée', ('Rhône-Méditerranée', 'Rhône–Mediterranean'), ('Rhône-Méditerranée', 'Rhône–Mediterranean'),
          'Rhône', ('Rhône', 'Rhône', .25),
          ('Le Rhône sort du lac Léman à Genève, reçoit la Saône à Lyon, puis descend plein sud jusqu’à la Méditerranée.',
           'The Rhône leaves Lake Geneva, receives the Saône at Lyon, then runs due south to the Mediterranean.'),
          ('Ses affluents, de l’embouchure vers l’amont, puis les fleuves côtiers du Languedoc-Roussillon :',
           'Its tributaries, from the mouth upstream, then the coastal rivers of Languedoc-Roussillon:'),
          [('Gard', 'Gard', 'Gard', .4), ('Durance', 'Durance', 'Durance', .35), ('Verdon', 'Verdon', 'Verdon', .45),
           ('Drôme', 'Drôme', 'Drôme', .5), ('Isère', 'Isère', 'Isère', .35), ('Saône', 'Saône', 'Saône', .4),
           ('Doubs', 'Doubs', 'Doubs', .3), ('Ain', 'Ain', 'Ain', .45),
           ('Hérault', 'Hérault', 'Hérault', .45), ('Aude', 'Aude', 'Aude', .35), ('Agly', 'Agly', 'Agly', .5)],
          [('<b>Saône</b> — la Bourgogne : Côte de Nuits, Côte de Beaune, Côte chalonnaise, Mâconnais… puis le Beaujolais.',
            '<b>Saône</b> — Burgundy: Côte de Nuits, Côte de Beaune, Côte Chalonnaise, Mâconnais… then Beaujolais.', ['6']),
           ('<b>Entre Saône, Doubs et Ain</b> — le Jura ; <b>le long de l’Ain et du haut Rhône</b> — le Bugey.',
            '<b>Between the Saône, Doubs and Ain</b> — the Jura; <b>along the Ain and the upper Rhône</b> — Bugey.', ['7', '8']),
           ('<b>Isère</b> — les vins de Savoie (Combe de Savoie).', '<b>Isère</b> — Savoie wines (Combe de Savoie).', ['5']),
           ('<b>Rhône, en aval de Lyon</b> — le Rhône septentrional : Côte-Rôtie, Condrieu, Hermitage, Cornas… <b>Drôme</b> — la Clairette de Die.',
            '<b>Rhône, below Lyon</b> — the Northern Rhône: Côte-Rôtie, Condrieu, Hermitage, Cornas… <b>Drôme</b> — Clairette de Die.', ['4']),
           ('<b>Bas Rhône</b> — le Rhône méridional : Châteauneuf-du-Pape, Gigondas, Tavel… <b>Au sud de la Durance</b> — la Provence.',
            '<b>Lower Rhône</b> — the Southern Rhône: Châteauneuf-du-Pape, Gigondas, Tavel… <b>South of the Durance</b> — Provence.', ['1', '2', '3']),
           ('<b>Hérault et Aude</b> — le Languedoc : Terrasses du Larzac, Pic Saint-Loup, Corbières, Minervois, Limoux…',
            '<b>Hérault and Aude</b> — Languedoc: Terrasses du Larzac, Pic Saint-Loup, Corbières, Minervois, Limoux…', ['9', '10']),
           ('<b>Agly</b> — le Roussillon : Côtes du Roussillon Villages, Maury.', '<b>Agly</b> — Roussillon: Côtes du Roussillon Villages, Maury.', ['11'])],
          extra_labels=[('Léman', 'Lake Geneva', 'Léman')])


BASIN_LAB = {'Adour-Garonne': ('Adour-<br>Garonne', 'Adour–<br>Garonne', -0.45, 44.1), 'Loire-Bretagne': ('Loire-<br>Bretagne', 'Loire–<br>Brittany', -2.4, 47.95),
             'Seine-Normandie': ('Seine-<br>Normandie', 'Seine–<br>Normandy', -1.5, 48.75), 'Artois-Picardie': ('Artois-<br>Picardie', 'Artois–<br>Picardy', 2.75, 50.25),
             'Rhin-Meuse': ('Rhin-<br>Meuse', 'Rhine–<br>Meuse', 6.25, 48.85), 'Rhône-Méditerranée': ('Rhône-<br>Méditerranée', 'Rhône–<br>Mediterranean', 5.6, 44.55)}


def scene_synthesis():
    from pyproj import Transformer
    trf = Transformer.from_crs(4326, 2154, always_xy=True)
    t0 = tl.t
    tl.chapter('bassins', 'Les six bassins', 'The six basins')
    t = t0 + .6
    its = [item(t, 'Six bassins, et presque chaque vignoble au bord de l’eau : retenez les fleuves, vous retiendrez les vins.',
                'Six basins, and almost every vineyard close to the water: remember the rivers and you will remember the wines.'),
           item(t + 7, 'Chaque bassin a son agence de l’eau : six agences pour la métropole et la Corse, rattachée au bassin Rhône-Méditerranée.',
                'Each basin has its own water agency: six agencies for mainland France and Corsica, which goes with the Rhône–Mediterranean basin.'),
           item(t + 14, 'La <b>Corse</b> forme un bassin à part, aux fleuves courts et torrentueux ; ses vins : Patrimonio, Ajaccio et les Vins de Corse.',
                '<b>Corsica</b> forms a basin of its own, with short, fast-flowing rivers; its wines: Patrimonio, Ajaccio and Vin de Corse.')]
    for k, (nm, lo, la) in enumerate(TOWNS['corse_major']):
        LBL.append(dict(kind='major', fr=nm, en=nm, xy=ll(lo, la), tin=t + 14.4 + k * .3))
    for k, (nm, lo, la) in enumerate(TOWNS['corse']):
        LBL.append(dict(kind='wine', fr=nm, en=nm, xy=ll(lo, la), tin=t + 15 + k * .3))
    end = t + 21
    x0, y0, w, h = GEO['place']
    labs = []
    # (lon, lat) → stage units, same projection and crop as film_assets.py
    R_ = json.load(open(GEO_DIR.parent / 'rivers_px.json', encoding='utf-8'))
    Kf = 540.0 / (R_['H'] - 200)
    for k, (bn, (fr, en, lon, lat)) in enumerate(BASIN_LAB.items()):
        E, N = trf.transform(lon, lat)
        px = (E - R_['Emin']) * R_['scale'] + R_['margin']; py = (R_['Nmax'] - N) * R_['scale'] + R_['margin']
        x, y = (px - 100) * Kf + x0, (py - 100) * Kf + y0

        def lines(s, x=x):
            parts = s.split('<br>')
            return ''.join(f'<tspan x="{f(x)}" dy="{("%.2fem" % (-(len(parts) - 1) * .55)) if i == 0 else "1.1em"}">{p}</tspan>' for i, p in enumerate(parts))
        OBS.append((x - 30, y - 14, x + 30, y + 14, .6))
        labs.append(f'<text class="blab" x="{f(x)}" y="{f(y)}" data-c="{f(x)},{f(y)}" data-fr="{att(lines(fr))}" data-en="{att(lines(en))}"'
                    f'{A(t + .8 + k * .4, .8, "pop")}>{lines(fr)}</text>')
    outl = ''.join(f'<use href="#{basin_ref(bn)}" class="bline"{A(t + .3, 1.2, "fade")}/>' for bn in GEO['basins'])
    tl.svg['maps'].append(f'<g class="scene" data-s="{f(t0)},{f(end)}">{outl}{"".join(labs)}</g>')
    notes_block('bassins', t0, end, None, ('Les six bassins', 'The six basins'), its)
    tl.scenes.append(dict(id='bassins', start=t0, end=end))
    tl.t = end


EXPLORE = []


def slug(name):
    import unicodedata
    return re.sub(r'[^a-z0-9]+', '-', unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode().lower()).strip('-')


def scene_explore():
    """Last frame = the whole network. Rivers are clickable on the map and in a list of basins in the notes panel."""
    t0 = tl.t
    tl.chapter('explorer', 'Explorer la carte', 'Explore the map')
    dur = 4
    end = t0 + dur
    card(t0, t0 + 3.2, 'À vous !', 'Your turn!',
         ('Cliquez sur un fleuve, sur la carte ou dans la liste, pour le mettre en valeur.',
          'Click a river, on the map or in the list, to highlight it.'))
    hl, hit = [], []
    blocks, dets = [], []
    for b in EXPLORE:
        bs = slug(b['bname'])
        btn = []
        for k, (riv, fr, en) in enumerate(b['rivers']):
            rs = slug(riv)
            w0 = RW[GEO['rivers'][riv]['rank']][1]
            uses_h = ''.join(f'<use href="#{pid}" class="hlh" style="stroke-width:{w + 3.2:.2f}"/>' for pid, w in RIV['chunks'][riv])
            uses_v = ''.join(f'<use href="#{pid}" class="hlv" style="stroke-width:{max(w + .9, 1.6):.2f}"/>' for pid, w in RIV['chunks'][riv])
            x, y = at(riv, .5, 11)
            lab = (f'<text class="hlname" x="{f(x)}" y="{f(y)}" data-fr="{att(fr)}" data-en="{att(en)}">{fr}</text>')
            hl.append(f'<g class="hlr" data-r="{rs}" data-b="{bs}">{uses_h}{uses_v}{lab}</g>')
            hit.append(''.join(f'<use href="#{pid}" class="hit" data-r="{rs}"/>' for pid, _w in RIV['chunks'][riv]))
            num = b['tribs'].index(riv) + 1 if riv in b['tribs'] else None
            main = ' main' if k == 0 and riv not in b['tribs'] else ''
            btn.append(f'<button type="button" class="exr{main}" data-r="{rs}">{f"<b>{num}</b>" if num else ""}{tr(fr, en)}</button>')
            # wines along this river: lines whose bold text names it, or that highlight its number
            names = {riv, fr, en}
            lines = []
            for wfr, wen, whl in b['wines']:
                bold = ' '.join(re.findall(r'<b>(.*?)</b>', wfr))
                if any(re.search(r'\b' + re.escape(n) + r'\b', bold) for n in names) or (num and str(num) in whl):
                    lines.append(f'<li>{tr(wfr, wen)}</li>')
            wl = (f'<ul class="exw">{"".join(lines)}</ul>' if lines else
                  tr('Pas de vignoble majeur sur ses rives.', 'No major vineyard along its banks.', 'p', 'exnone'))
            dets.append(f'<div class="exd" data-r="{rs}">{tr("Bassin " + b["title"][0], b["title"][1] + " basin", "p", "exk")}'
                        f'{tr(fr, en, "h4")}{wl}</div>')
        blocks.append(f'<li class="exbk"><button type="button" class="exb" data-b="{bs}">{tr(b["title"][0], b["title"][1])}</button>'
                      f'<div class="exrs">{"".join(btn)}</div></li>')
        dets.append(f'<div class="exd" data-b="{bs}">{tr("Bassin", "Basin", "p", "exk")}{tr(b["title"][0], b["title"][1], "h4")}'
                    f'{tr(b["intro"][0], b["intro"][1], "p", "exi")}</div>')
    n = len(tl.chapters)
    tl.notes.append(
        f'<section class="nb exn" data-s="{f(t0)},{f(end)}" id="nb-explorer">'
        f'{tr(f"Chapitre {n:02d}", f"Chapter {n:02d}", "p", "kick")}{tr("Explorer la carte", "Explore the map", "h3")}'
        f'{tr("Cliquez sur un fleuve — sur la carte ou ci-dessous — ou sur le nom d’un bassin. Cliquez à nouveau pour tout réafficher.", "Click a river — on the map or below — or a basin name. Click again to show everything.", "p", "exhelp")}'
        f'<div class="exdet">{"".join(dets)}</div>'
        f'<ol class="exlist" data-k="explore-list">{"".join(blocks)}</ol></section>')
    tl.svg['maps'].append(f'<g class="scene explore" data-s="{f(t0)},{f(end)}"><g class="hls">{"".join(hl)}</g><g class="hits">{"".join(hit)}</g></g>')
    tl.scenes.append(dict(id='explorer', start=t0, end=end))
    tl.t = end
    tl.explore = t0


STYLE = {   # font size, width factor, text class
    'country': (8.5, .78, 'country'), 'mount': (11.5, .5, 'mount'), 'major': (9.5, .58, 'ctxt major'), 'wine': (8, .55, 'ctxt wine')}


def place_names():
    """Greedy placement: each name takes the candidate spot that overlaps the least with river names, markers,
    river lines, other names and the frame. Cities keep their dot fixed; area names may shift a little."""
    placed = []
    out = []
    order = sorted(LBL, key=lambda L: ['country', 'mount', 'major', 'wine'].index(L['kind']))

    def overlap(a, b):
        w = min(a[2], b[2]) - max(a[0], b[0]); h = min(a[3], b[3]) - max(a[1], b[1])
        return w * h if w > 0 and h > 0 else 0.0

    dots = [L['xy'] for L in LBL if L['kind'] in ('major', 'wine')]

    def bdist(box, pt):
        dx = max(box[0] - pt[0], 0, pt[0] - box[2]); dy = max(box[1] - pt[1], 0, pt[1] - box[3])
        return math.hypot(dx, dy)

    for L in order:
        fs, wf, cls = STYLE[L['kind']]
        lines = L['fr'].split('<br>')
        tw = max(len(x) for x in lines) * fs * wf
        th = fs * (1.15 * len(lines))
        x, y = L['xy']
        cands = []
        if L['kind'] in ('major', 'wine'):
            g = 3.5
            for dx, dy, anc in [(g, 0, 'start'), (-g, 0, 'end'), (0, -th / 2 - g, 'middle'), (0, th / 2 + g, 'middle'),
                                (g, -th / 2 - 1, 'start'), (g, th / 2 + 1, 'start'), (-g, -th / 2 - 1, 'end'), (-g, th / 2 + 1, 'end')]:
                cx = x + dx + (tw / 2 if anc == 'start' else -tw / 2 if anc == 'end' else 0)
                cands.append((cx, y + dy, anc, abs(dx) + abs(dy)))
        else:
            for dx in (0, -8, 8, -16, 16, -24, 24):
                for dy in (0, -8, 8, -16, 16):
                    cands.append((x + dx, y + dy, 'middle', math.hypot(dx, dy)))
        best = None
        for cx, cy, anc, dist in cands:
            box = (cx - tw / 2, cy - th / 2, cx + tw / 2, cy + th / 2)
            sc = dist * .05
            sc += sum(overlap(box, o[:4]) * o[4] for o in OBS) * .2
            pad = (box[0] - 1.5, box[1] - 1.5, box[2] + 1.5, box[3] + 1.5)
            sc += sum(overlap(pad, b) for b in placed) * .8
            if L['kind'] in ('major', 'wine'):      # the label must read as belonging to its own dot
                own = bdist(box, (x, y))
                sc += sum(6 for d_ in dots if d_ != (x, y) and math.dist(d_, (x, y)) < 40 and bdist(box, d_) < own + 2)
                sc += sum(30 for d_ in dots if d_ != (x, y) and bdist(pad, d_) < 1)
            else:                                   # range and country names never cover a town's dot
                sc += sum(30 for d_ in dots if bdist(pad, d_) < 2)
            sc += len(GEO['dense'].query_ball_point([cx, cy], r=max(tw, th) / 2)) * (.6 if L['kind'] != 'country' else .2)
            if box[0] < 2 or box[2] > 718 or box[1] < 2 or box[3] > 538:
                sc += 100
            if best is None or sc < best[0]:
                best = (sc, cx, cy, anc, box)
        _sc, cx, cy, anc, box = best
        placed.append(box)
        tx = cx - tw / 2 if anc == 'start' else cx + tw / 2 if anc == 'end' else cx

        def tsp(s, tx=tx):
            parts = s.split('<br>')
            return ''.join(f'<tspan x="{f(tx)}" dy="{("%.2fem" % (-(len(parts) - 1) * .55)) if i == 0 else "1.1em"}">{p}</tspan>' for i, p in enumerate(parts))
        txt = (f'<text class="{cls}" x="{f(tx)}" y="{f(cy)}" style="text-anchor:{anc}" '
               f'data-fr="{att(tsp(L["fr"]))}" data-en="{att(tsp(L["en"]))}">{tsp(L["fr"])}</text>')
        if L['kind'] in ('major', 'wine'):
            r = 2.6 if L['kind'] == 'major' else 2.0
            out.append(f'<g class="city {L["kind"]}" data-c="{f(x)},{f(y)}"{A(L["tin"], .6, "pop")}>'
                       f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}"/>{txt}</g>')
        else:
            out.append(f'<g data-c="{f(cx)},{f(cy)}"{A(L["tin"], .7, "pop")}>{txt}</g>')
    return '<g class="names">' + ''.join(out) + '</g>'


def part1_layers():
    """Persistent layers for the whole film: relief map at the bottom, then river halos, rivers, markers."""
    return (f'<g class="scene" data-s="0,{f(tl.t)}">{relief_img()}</g>',
            f'<defs>{"".join(RIV["defs"])}</defs><g class="rivers"><g>{"".join(RIV["halo"])}</g><g>{"".join(RIV["line"])}</g></g>',
            place_names() + f'<g class="rtop">{"".join(RIV["top"])}</g>')


# ---------------------------------------------------------------- 4. drawing France
LABELS = {
    'Atlantic\nOcean': (['Océan', 'Atlantique'], ['Atlantic', 'Ocean']),
    'Manche': (['La Manche'], ['The Channel']),
    'Mediterranean Sea': (['Mer Méditerranée'], ['Mediterranean Sea']),
    'BELGIUM': (['BELGIQUE'], ['BELGIUM']), 'LUXEMBOURG': (['LUXEMBOURG'], ['LUXEMBOURG']),
    'GERMANY': (['ALLEMAGNE'], ['GERMANY']), 'SWISSZERLAND': (['SUISSE'], ['SWITZERLAND']),
    'ITALY': (['ITALIE'], ['ITALY']), 'SPAIN': (['ESPAGNE'], ['SPAIN']),
    'Loire': (['Loire'], ['Loire']), 'garonne': (['Garonne'], ['Garonne']), 'Rhône': (['Rhône'], ['Rhône']),
    'Rhin': (['Rhin'], ['Rhine']), 'Saône': (['Saône'], ['Saône']),
    'Alsace': (['Alsace'], ['Alsace']), 'Burgundy': (['Bourgogne'], ['Burgundy']),
    'South\nWest': (['Sud-', 'Ouest'], ['South', 'West']), 'Champagne': (['Champagne'], ['Champagne']),
    'Chablis': (['Chablis'], ['Chablis']), 'Rhone': (['Rhône'], ['Rhône']),
    'Languedoc\nRoussillon': (['Languedoc', 'Roussillon'], ['Languedoc', 'Roussillon']),
    'Provence': (['Provence'], ['Provence']), 'Corsica': (['Corse'], ['Corsica']),
    'Savoie\nJura': (['Savoie', 'Jura'], ['Savoie', 'Jura']), 'Bordeaux': (['Bordeaux'], ['Bordeaux']),
}


def pts_of(lf, n=56):
    """Leaf → list of polylines in slide coords (affine transform baked in)."""
    m, w, h, prst = lf['m'], lf['w'], lf['h'], lf['prst']
    if prst in ('line', 'straightConnector1'):
        P = [(0, 0), (w, h)]
    elif prst == 'hexagon':
        x1 = min(w, h) * .25
        dy = h / 2 * 1.1547 * math.sin(math.radians(60)); vc = h / 2
        P = [(0, vc), (x1, vc - dy), (w - x1, vc - dy), (w, vc), (w - x1, vc + dy), (x1, vc + dy), (0, vc)]
    elif prst == 'arc':
        st = G._adj_from(lf, 'adj1', 16200000) / 60000.0
        en = G._adj_from(lf, 'adj2', 0) / 60000.0
        sw = (en - st) % 360
        P = []
        for k in range(n + 1):
            a = st + sw * k / n
            P.append(G._ell(w / 2, h / 2, a))
    elif prst in ('ellipse', 'donut'):
        P = [(w / 2 + w / 2 * math.cos(2 * math.pi * k / n), h / 2 + h / 2 * math.sin(2 * math.pi * k / n)) for k in range(n + 1)]
    else:
        return None
    return [m.pt(x, y) for x, y in P]


def dpath(P):
    return 'M' + 'L'.join(f'{f(x)},{f(y)}' for x, y in P)


def plen(P):
    return sum(math.hypot(P[k + 1][0] - P[k][0], P[k + 1][1] - P[k][1]) for k in range(len(P) - 1))


def stroke(lf, cls, tin, dur, out=None, marker=False, reverse=False):
    P = pts_of(lf)
    if reverse:
        P = P[::-1]
    mk = ' marker-end="url(#arr)"' if marker else ''
    return f'<path class="{cls}" d="{dpath(P)}" data-len="{f(plen(P))}"{mk}{A(tin, dur, "draw", out)}/>'


def label(lf, key, cls, tin, dur=.8, fx='fade', out=None, dx=0, dy=0, size=None):
    fr, en = LABELS[key]
    m = lf['m']
    cx, cy = m.pt(lf['w'] / 2, lf['h'] / 2)
    cx += dx; cy += dy
    a, b = m.v[0], m.v[1]
    ang = math.degrees(math.atan2(b, a))
    if ang > 90:
        ang -= 180
    if ang < -90:
        ang += 180
    rot = f' transform="rotate({f(ang)} {f(cx)} {f(cy)})"' if abs(ang) > 2 else ''

    def lines(L):
        n = len(L)
        return ''.join(f'<tspan x="{f(cx)}" dy="{("%.2fem" % (-(n - 1) * .55)) if k == 0 else "1.1em"}">{s}</tspan>' for k, s in enumerate(L))
    fs = f' style="font-size:{size}px"' if size else ''
    return (f'<text class="{cls}" x="{f(cx)}" y="{f(cy)}"{rot}{fs} data-c="{f(cx)},{f(cy)}" data-fr="{att(lines(fr))}" data-en="{att(lines(en))}"'
            f'{A(tin, dur, fx, out)}>{lines(fr)}</text>')


def france_outline():
    """Mainland France (union of the six Sandre basins of film 1) fitted onto the drawing: uniform scale + shift, no
    rotation, least squares on the 8 cities the method places (so France sits where the drawing expects it)."""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    if 'basins' not in GEO:
        load_geo()
    rings = [r for b in GEO['basins'].values() for r in (b if isinstance(b[0][0], list) else [b]) if len(r) > 3]
    u = unary_union([Polygon(r).buffer(.6) for r in rings]).buffer(-.6)
    main = max(getattr(u, 'geoms', [u]), key=lambda q: q.area).simplify(.4)
    cities = [(2.352, 48.857, 351, 189), (7.752, 48.573, 511, 190), (5.041, 47.322, 428, 253), (4.835, 45.764, 427, 331),
              (5.370, 43.296, 427, 422), (1.444, 43.605, 276, 401), (-0.579, 44.838, 230, 362), (-1.554, 47.218, 208, 252)]
    S_ = np.array([ll(a, b) for a, b, _c, _d in cities]); D_ = np.array([[c, d] for _a, _b, c, d in cities], float)
    ms, md = S_.mean(0), D_.mean(0)
    sc = ((S_ - ms) * (D_ - md)).sum() / ((S_ - ms) ** 2).sum()
    P_ = (np.asarray(main.exterior.coords) - ms) * sc + md
    return [tuple(q) for q in P_]


def scene_drawing():
    zf = zipfile.ZipFile(PPTX)
    S11, S14, S18 = G.leaves(zf, 11), G.leaves(zf, 14), G.leaves(zf, 18)
    parts = []
    t_draw0 = tl.t

    # ---- 4a. the hexagon and its guides
    t0 = tl.t
    tl.chapter('hexagone', 'L’hexagone et ses repères', 'The hexagon and its guides')
    card(t0 - (.7 if t0 == 0 else 0), t0 + 4.6, 'Dessiner la France, <em>facilement</em>', 'Drawing France <em>the easy way</em>',
         ('Prenez une feuille et un crayon, et suivez le guide.', 'Grab a sheet of paper and a pencil, and follow along.'))
    t = t0 + 5
    its = []

    def step(fr, en, gap=5.4):
        nonlocal t
        its.append(item(t, fr, en))
        t0_ = t
        t += gap
        return t0_

    s_fr = step('<b>La France : l’Hexagone.</b> Regardez sa forme : six côtés à peu près égaux — trois bordés par la mer (Manche, Atlantique, Méditerranée), trois par la terre (Pyrénées, Alpes et Jura, Rhin et Ardennes). Les Français surnomment d’ailleurs leur pays « l’Hexagone ».',
                '<b>France: the Hexagon.</b> Look at its shape: six roughly equal sides — three on the sea (Channel, Atlantic, Mediterranean), three on land (Pyrenees, Alps and Jura, Rhine and Ardennes). The French even nickname their country “l’Hexagone”.', 7)
    s = step('Dessinez par-dessus un grand hexagone, pointe en haut : il épouse presque exactement la France.',
             'Draw a large hexagon over it, point upwards: it fits France almost exactly.')
    parts.append(stroke(S11['4'], 'ink hex', s + .3, 3.2))
    s = step('Creusez légèrement chacun des six côtés : ni les côtes ni les frontières ne sont droites.',
             'Hollow out each of the six sides a little: neither coasts nor borders are straight.')
    for k, i in enumerate(['11', '12', '14', '10', '8', '13']):
        parts.append(stroke(S11[i], 'ink arc', s + .3 + k * .45, 1.4))
    # the real outline of France, under the hexagon: appears first, then fades once the sides are hollowed
    t_out = t - .2
    FP = france_outline()
    fd = 'M' + 'L'.join(f'{f(x)},{f(y)}' for x, y in FP) + 'Z'
    parts.insert(0, f'<path class="fr-fill" d="{fd}"{A(s_fr + 1.6, 1.4, "fade", t_out)}/>'
                    f'<path class="fr-line" d="{fd}" data-len="{f(plen(FP + FP[:1]))}"{A(s_fr + .4, 2.8, "draw", t_out)}/>'
                    + tr('La France : <tspan class="em">l’Hexagone</tspan>', 'France: <tspan class="em">the Hexagon</tspan>', 'text', 'stitle',
                         f' x="360" y="52"{A(s_fr + .2, .9, "fade", t_out)}'))
    s = step('Placez les mers : la Manche au nord-ouest, l’Atlantique à l’ouest, la Méditerranée au sud…',
             'Add the seas: the Channel to the north-west, the Atlantic to the west, the Mediterranean to the south…')
    parts.append(label(S14['19'], 'Manche', 'sea', s + .3))
    parts.append(label(S14['18'], 'Atlantic\nOcean', 'sea', s + 1.2))
    parts.append(label(S14['20'], 'Mediterranean Sea', 'sea', s + 2.1))
    s = step('… puis les voisins, dans le sens des aiguilles d’une montre : Belgique, Luxembourg, Allemagne, Suisse, Italie… et l’Espagne au sud-ouest.',
             '… then the neighbours, clockwise: Belgium, Luxembourg, Germany, Switzerland, Italy… and Spain to the south-west.')
    for k, i in enumerate(['21', '22', '23', '24', '25', '26']):
        parts.append(label(S14[i], S14[i]['text'], 'country', s + .3 + k * .45))
    s = step('Tracez l’axe vertical, puis deux horizontales : l’une par les deux sommets du haut, l’autre par les deux sommets du bas.',
             'Draw the vertical axis, then two horizontals: one through the two upper corners, one through the two lower corners.')
    parts.append(stroke(S11['6'], 'guide', s + .3, 1.6, reverse=True))
    parts.append(stroke(S11['7'], 'guide', s + 1.4, 1.6, reverse=True))
    parts.append(stroke(S11['28'], 'guide', s + 2.4, 1.6, reverse=True))
    s = step('Divisez les deux côtés verticaux en trois parts égales et tracez deux nouvelles horizontales : le « tiers haut » et le « tiers bas ».',
             'Divide both vertical sides into three equal parts and draw two more horizontals: the “upper third” and the “lower third” lines.', 6.4)
    for i in ('38', '39', '41', '45', '46', '47'):
        parts.append(stroke(S11[i], 'hint', s + .3, .8, out=s + 5.6, marker=True))
    for k, i in enumerate(['29', '32', '31', '33']):
        parts.append(stroke(S11[i], 'guide', s + 1.2 + k * .5, 1.2, reverse=(i in ('29', '31'))))
    s = step('Coupez en deux les côtés obliques du haut et descendez deux verticales : à gauche et à droite.',
             'Halve the two upper slanted sides and drop two verticals: one on the left, one on the right.')
    for i in ('62', '64'):
        parts.append(stroke(S11[i], 'hint', s + .3, .8, out=s + 5, marker=True))
    parts.append(stroke(S11['58'], 'guide', s + 1, 1.6))
    parts.append(stroke(S11['61'], 'guide', s + 1.6, 1.6))
    s = step('Enfin, dessinez une petite bouche boudeuse sur la côte atlantique, entre les deux lignes du bas : c’est l’estuaire de la Gironde.',
             'Finally, draw a little sulky mouth on the Atlantic coast, between the two lower lines: that is the Gironde estuary.', 6)
    parts.append(stroke(S11['76'], 'hint', s + .3, .8, out=s + 5.4, marker=True))
    parts.append(stroke(S11['71'], 'ink mouth', s + 1, 1.2))
    parts.append(stroke(S11['72'], 'ink mouth', s + 1.8, 1.2))
    end = t + .5
    notes_block('hexagone', t0, end, ('Chapitre 3', 'Chapter 3'), ('L’hexagone et ses repères', 'The hexagon and its guides'), its)
    tl.scenes.append(dict(id='hexagone', start=t0, end=end))
    tl.t = end

    # ---- 4b. rivers
    t0 = tl.t
    tl.chapter('dessin-fleuves', 'Placer les fleuves', 'Placing the rivers')
    card(t0, t0 + 4.4, 'Vous avez maintenant toutes les bases pour placer les grands fleuves et les grandes villes.',
         'This will give you all the basics to place the main rivers and cities.',
         ('D’abord, les grands fleuves.', 'First, the major rivers.'))
    t = t0 + 4.8
    its = []
    s = step('<b>La Loire</b> : depuis la côte, suivez le tiers haut vers l’est jusqu’un peu au-delà de l’axe central, puis tournez vers le sud. (En réalité, elle coule dans l’autre sens : elle naît dans le Massif central.)',
             '<b>The Loire</b>: from the coast, follow the upper-third line east to just past the central axis, then turn south. (In reality it flows the other way: it rises in the Massif Central.)', 6.4)
    parts.append(stroke(S14['65'], 'river', s + .3, 1.8))
    parts.append(stroke(S14['67'], 'river', s + 2.1, 1.2, reverse=True))
    parts.append(label(S14['55'], 'Loire', 'rlab', s + 3))
    s = step('<b>La Garonne</b> : du coin de la bouche, une diagonale vers le sud-est jusqu’à la verticale de gauche.',
             '<b>The Garonne</b>: from the corner of the mouth, a diagonal running south-east to the left-hand vertical.')
    parts.append(stroke(S14['74'], 'river', s + .3, 1.6, reverse=True))
    parts.append(label(S14['79'], 'garonne', 'rlab', s + 1.9))
    s = step('<b>Le Rhin</b> : un court trait le long du coin nord-est, du tiers haut jusqu’au sommet.',
             '<b>The Rhine</b>: a short stroke along the north-east corner, from the upper-third line up to the top.')
    parts.append(stroke(S14['77'], 'river', s + .3, 1.2, reverse=True))
    parts.append(label(S14['81'], 'Rhin', 'rlab', s + 1.5))
    s = step('<b>Le Rhône</b> : il arrive de l’est le long du tiers bas (depuis Genève), puis descend la verticale de droite jusqu’à la mer.',
             '<b>The Rhône</b>: it arrives from the east along the lower-third line (from Geneva), then runs down the right-hand vertical to the sea.', 6)
    parts.append(stroke(S14['73'], 'river', s + .3, 1.2))
    parts.append(stroke(S14['71'], 'river', s + 1.5, 1.4))
    parts.append(label(S14['80'], 'Rhône', 'rlab', s + 2.9))
    s = step('<b>La Saône</b> : du point où le Rhône tourne, remontez vers le nord jusqu’au tiers haut.',
             '<b>The Saône</b>: from the point where the Rhône turns, go back north up to the upper-third line.')
    parts.append(stroke(S14['82'], 'river', s + .3, 1.4))
    parts.append(label(S14['84'], 'Saône', 'rlab', s + 1.7))
    end = t + .5
    notes_block('dessin-fleuves', t0, end, ('Chapitre 4', 'Chapter 4'), ('Les grands fleuves', 'The major rivers'), its)
    tl.scenes.append(dict(id='dessin-fleuves', start=t0, end=end))
    tl.t = end

    # ---- 4c. cities
    t0 = tl.t
    tl.chapter('villes', 'Placer les villes', 'Placing the cities')
    card(t0, t0 + 3.4, 'Maintenant, plaçons les villes.', 'Now, let’s place the cities.')
    t = t0 + 3.8
    its = []
    cities = [('65', '45', 'PARIS', 'Paris', 'sur l’axe central, sur la ligne des deux sommets du haut.', 'on the central axis, on the line through the two upper corners.'),
              ('66', '46', 'Strasbourg', 'Strasbourg', 'au bout de cette même ligne, dans le coin nord-est, sur le Rhin.', 'at the end of that same line, in the north-east corner, on the Rhine.'),
              ('67', '47', 'Dijon', 'Dijon', 'verticale de droite × tiers haut, au bout de la Saône.', 'right-hand vertical × upper third, at the top of the Saône.'),
              ('68', '50', 'Lyon', 'Lyon', 'verticale de droite × tiers bas, là où la Saône rejoint le Rhône.', 'right-hand vertical × lower third, where the Saône meets the Rhône.'),
              ('69', '51', 'Marseille', 'Marseille', 'au pied de la verticale de droite, sur la Méditerranée.', 'at the foot of the right-hand vertical, on the Mediterranean.'),
              ('70', '52', 'Toulouse', 'Toulouse', 'verticale de gauche × ligne des sommets du bas, sur la Garonne.', 'left-hand vertical × the line through the lower corners, on the Garonne.'),
              ('71', '53', 'Bordeaux', 'Bordeaux', 'au coin de la bouche, sur la Garonne.', 'at the corner of the mouth, on the Garonne.'),
              ('72', '54', 'Nantes', 'Nantes', 'sur la côte, au tiers haut, à l’embouchure de la Loire.', 'on the coast, on the upper-third line, at the mouth of the Loire.')]
    for dot, lab, txt, name, fr, en in cities:
        s = step(f'<b>{name}</b> : {fr}', f'<b>{name}</b>: {en}', 4.6)
        lf = S18[dot]
        cx, cy = lf['m'].pt(lf['w'] / 2, lf['h'] / 2)
        parts.append(f'<g class="city" data-c="{f(cx)},{f(cy)}"{A(s + .3, .6, "pop")}><circle cx="{f(cx)}" cy="{f(cy)}" r="7" class="halo"/>'
                     f'<circle cx="{f(cx)}" cy="{f(cy)}" r="3.6"/></g>')
        lb = S18[lab]
        lx, ly = lb['m'].pt(lb['w'] / 2, lb['h'] / 2)
        disp = 'Paris' if txt == 'PARIS' else txt
        parts.append(f'<text class="clab" x="{f(lx)}" y="{f(ly)}" data-c="{f(lx)},{f(ly)}"{A(s + .7, .7, "fade")}>{disp}</text>')
    end = t + .5
    notes_block('villes', t0, end, ('Chapitre 5', 'Chapter 5'), ('Les grandes villes', 'The main cities'), its)
    tl.scenes.append(dict(id='villes', start=t0, end=end))
    tl.t = end

    # ---- 4d. wine regions
    t0 = tl.t
    tl.chapter('regions', 'Placer les régions viticoles', 'Placing the wine regions')
    card(t0, t0 + 3.4, 'Enfin, les régions viticoles…', 'Finally, the wine regions…')
    t = t0 + 3.8
    its = []
    regs = [
        (['78'], [('98', 'Bordeaux')], '#8e1f33', ('Bordeaux', 'autour de la bouche : la Gironde, la Garonne et la Dordogne.'), ('Bordeaux', 'around the mouth: the Gironde, the Garonne and the Dordogne.')),
        (['76'], [('90', 'South\nWest')], '#c08a3e', ('Le Sud-Ouest', 'en amont, autour de Toulouse et de la Garonne.'), ('The South-West', 'upstream, around Toulouse and the Garonne.')),
        (['80', '81'], [('88', 'Loire'), ('89', 'Loire')], '#5f8f5a', ('La Loire', 'tout le long du fleuve, de Nantes jusqu’à Sancerre.'), ('The Loire', 'all along the river, from Nantes to Sancerre.')),
        (['64'], [('86', 'Alsace')], '#9aae3e', ('L’Alsace', 'le long du Rhin, au pied des Vosges.'), ('Alsace', 'along the Rhine, at the foot of the Vosges.')),
        (['73', '74'], [('87', 'Burgundy'), ('92', 'Chablis')], '#7a3b6e', ('La Bourgogne', 'le long de la Saône, de Dijon vers Lyon (jusqu’au Beaujolais) ; Chablis, à part, vers Paris.'), ('Burgundy', 'along the Saône, from Dijon towards Lyon (down to Beaujolais); Chablis, set apart, towards Paris.')),
        (['75'], [('93', 'Rhone')], '#b2452e', ('La vallée du Rhône', 'entre Lyon et la mer.'), ('The Rhône Valley', 'between Lyon and the sea.')),
        (['85'], [('97', 'Savoie\nJura')], '#4f8fb0', ('La Savoie et le Jura', 'à l’est de la Saône, vers le Jura et les Alpes.'), ('Savoie and the Jura', 'east of the Saône, towards the Jura and the Alps.')),
        (['82'], [('91', 'Champagne')], '#d9a92e', ('La Champagne', 'à l’est de Paris.'), ('Champagne', 'east of Paris.')),
        (['79'], [('94', 'Languedoc\nRoussillon')], '#c4683a', ('Le Languedoc-Roussillon', 'le long du golfe du Lion, du Rhône aux Pyrénées.'), ('Languedoc-Roussillon', 'along the Gulf of Lion, from the Rhône to the Pyrenees.')),
        (['83'], [('95', 'Provence')], '#d27a95', ('La Provence', 'à l’est du Rhône, jusqu’à la Côte d’Azur.'), ('Provence', 'east of the Rhône, as far as the Côte d’Azur.')),
        (['84'], [('96', 'Corsica')], '#6b8f3a', ('La Corse', 'en mer, au sud-est.'), ('Corsica', 'out at sea, to the south-east.')),
    ]
    reg_parts = []
    for ovals, labs, col, fr, en in regs:
        s = step(f'<b>{fr[0]}</b> : {fr[1]}', f'<b>{en[0]}</b>: {en[1]}', 4.4)
        for k, o in enumerate(ovals):
            lf = S18[o]
            P = pts_of(lf, 64)
            cx, cy = lf['m'].pt(lf['w'] / 2, lf['h'] / 2)
            reg_parts.append(f'<path class="reg" d="{dpath(P)}Z" style="--c:{col}" data-c="{f(cx)},{f(cy)}"{A(s + .3 + k * .5, .7, "pop")}/>')
        for k, (lid, key) in enumerate(labs):
            reg_parts.append(label(S18[lid], key, 'glab', s + .7 + k * .5))
    parts.append('<g class="regs">' + ''.join(reg_parts) + '</g>')
    end = t + .5
    notes_block('regions', t0, end, ('Chapitre 6', 'Chapter 6'), ('Les régions viticoles', 'The wine regions'), its)
    tl.scenes.append(dict(id='regions', start=t0, end=end))
    tl.t = end

    # regions go on top of rivers/cities: reorder so .regs sits under city dots & labels
    regs_svg = parts.pop()
    first_city = next(k for k, p in enumerate(parts) if p.startswith('<g class="city"'))
    parts.insert(first_city, regs_svg)
    paper = '<rect x="0" y="0" width="720" height="540" class="paper"/><rect x="0" y="0" width="720" height="540" fill="url(#grid)"/>'
    return f'<g class="scene drawing" data-s="{f(t_draw0)},{f(tl.t)}">{paper}{"".join(parts)}</g>'


# ---------------------------------------------------------------- 5. the result
def scene_final():
    t0 = tl.t
    tl.chapter('resultat', 'Et voilà !', 'Et voilà!')
    card(t0, t0 + 3.6, 'Et voilà…', 'Et voilà…', ('Regardons le résultat.', 'Let’s look at the end result.'))
    t = t0 + 4
    notes = ''.join(f'<text class="note"{A(t + 1.4 + k * .35, .6, "pop")} x="{x}" y="{y}" data-c="{x},{y}">{c}</text>'
                    for k, (c, x, y) in enumerate([('♪', 70, 150), ('♫', 112, 128), ('♪', 150, 160), ('♬', 96, 196)]))
    svg = (f'<g class="scene" data-s="{f(t0)},{f(t0 + 40)}">'
           f'<rect x="0" y="0" width="720" height="540" class="paper"/>'
           f'<image href="img/map_wine_regions.webp?v={VER}" x="190" y="-8" width="474" height="562" preserveAspectRatio="xMidYMid meet"{A(t, 1.8, "fade")}/>'
           f'<text class="tada" x="110" y="262" data-c="110,262"{A(t + 1, .8, "pop")}>Tadaaa !</text>{notes}</g>')
    tl.svg['final'].append(svg)
    its = [item(t, 'Comparez avec votre croquis : la Loire, le Rhône, la Garonne… et les vignobles sont bien là où vous les avez placés.',
                'Compare it with your sketch: the Loire, the Rhône, the Garonne… and the vineyards are right where you put them.'),
           item(t + 7, 'Vous connaissez maintenant la géographie qui structure tout le vignoble français. Il ne reste plus qu’à la goûter.',
                'You now know the geography behind the whole French vineyard. All that is left is to taste it.')]
    end = t + 14
    card(t + 12.5, end + 10, 'Fin', 'The end', ('Revoir le film, ou explorer la carte interactive des vignobles.',
                                             'Watch it again, or explore the interactive vineyard map.'), 'endcard')
    tl.svg['final'][-1] = svg.replace(f'data-s="{f(t0)},{f(t0 + 40)}"', f'data-s="{f(t0)},{f(end)}"')
    notes_block('resultat', t0, end, ('Épilogue', 'Epilogue'), ('Le résultat', 'The result'), its)
    tl.scenes.append(dict(id='resultat', start=t0, end=end))
    tl.t = end


# ------------------------------------------------------------------ context (Part 1): why wine follows geography
CONTEXT = dict(
    title=('Le vin et la <em>géographie</em>', 'Wine and <em>geography</em>'),
    lead=('Pourquoi les grands vignobles français sont-ils presque tous au bord de l’eau ou à flanc de coteau ? Ni hasard ni simple tradition : '
          'le relief, les fleuves et les sols ont décidé, pendant des siècles, où l’on pouvait faire du bon vin… et où l’on pouvait le vendre.',
          'Why do nearly all of France’s great vineyards sit by the water or on a hillside? It is neither chance nor mere tradition: '
          'for centuries, relief, rivers and soils decided where good wine could be made… and where it could be sold.'),
    points=[
        (('Le fleuve, première route du vin', 'The river, wine’s first road'),
         ('Jusqu’à l’arrivée du chemin de fer, au milieu du XIX<sup>e</sup> siècle, le vin voyage en fût par l’eau : une barrique pleine pèse près de 300 kg, et les routes sont lentes, chères et cahoteuses. Un vignoble sans rivière navigable ne peut guère vendre loin.',
          'Until the railways arrived in the mid-19th century, wine travelled in casks by water: a full barrel weighs close to 300 kg, and roads were slow, costly and rough. A vineyard without a navigable river could hardly sell far away.'),
         ('Les Romains remontent la vallée du Rhône, puis la Saône et la Moselle ; les vins d’Auxerre descendent l’Yonne et la Seine jusqu’à Paris.',
          'The Romans worked their way up the Rhône valley, then the Saône and the Moselle; the wines of Auxerre floated down the Yonne and the Seine to Paris.')),
        (('Le port ouvre le monde', 'The port opens up the world'),
         ('Là où le fleuve rejoint la mer, le vin trouve ses clients étrangers. Les ports font la fortune des vignobles qui les entourent.',
          'Where the river meets the sea, wine finds its foreign customers. Ports made the fortune of the vineyards around them.'),
         ('Bordeaux expédie son « claret » en Angleterre pendant les trois siècles où l’Aquitaine est anglaise (1152-1453) ; au XVII<sup>e</sup> siècle, les marchands hollandais achètent les vins de la Charente et de la Loire pour les distiller : c’est la naissance du cognac.',
          'Bordeaux shipped its “claret” to England during the three centuries when Aquitaine was English (1152–1453); in the 17th century, Dutch merchants bought Charente and Loire wines to distil them: the birth of Cognac.')),
        (('Le coteau draine', 'The slope drains'),
         ('La vigne n’aime pas avoir les pieds dans l’eau. Sur une pente, la pluie s’écoule au lieu de stagner ; le sol, souvent mince et pauvre, oblige les racines à descendre profondément. La vigne pousse moins, mais ses raisins sont plus concentrés.',
          'Vines hate wet feet. On a slope, rain runs off instead of lying in the soil; the ground, often thin and poor, forces the roots to dig deep. The vine grows less, but its grapes are more concentrated.'),
         ('Les grands crus de la Côte d’Or occupent la mi-pente ; le bas, plus profond et plus humide, donne des appellations plus simples.',
          'The Côte d’Or’s grands crus sit mid-slope; the deeper, wetter ground at the foot gives humbler appellations.')),
        (('Le coteau protège du gel et capte le soleil', 'The slope wards off frost and catches the sun'),
         ('L’air froid, plus lourd, glisse vers le fond des vallées : les gelées de printemps y frappent plus fort qu’à mi-coteau. Une pente tournée vers le sud ou le sud-est reçoit en outre les rayons plus directement, ce qui compte beaucoup dans les vignobles du nord.',
          'Cold air, being heavier, slides down to the valley floor, where spring frosts bite harder than mid-slope. A slope facing south or south-east also catches the sun’s rays more squarely, which matters a great deal in northern vineyards.'),
         ('En Champagne, en Alsace ou sur les bords de la Loire, les meilleures parcelles regardent le soleil.',
          'In Champagne, in Alsace or along the Loire, the best plots face the sun.')),
        (('L’eau adoucit le climat', 'Water softens the climate'),
         ('Une grande masse d’eau se réchauffe et se refroidit lentement : elle tempère les gelées et les coups de chaleur sur ses rives. Ses brumes d’automne peuvent aussi favoriser la « pourriture noble » (<i>Botrytis cinerea</i>), qui donne les grands vins liquoreux.',
          'A large body of water warms up and cools down slowly, so it tempers frosts and heat spikes along its banks. Its autumn mists can also encourage “noble rot” (<i>Botrytis cinerea</i>), the source of great sweet wines.'),
         ('Un dicton médocain veut que les meilleurs vins « voient la rivière » ; à Sauternes, les eaux fraîches du Ciron rencontrent la Garonne plus chaude et font naître les brumes du matin.',
          'A Médoc saying holds that the best wines “can see the river”; at Sauternes, the cool waters of the Ciron meet the warmer Garonne and raise the morning mists.')),
        (('Les fleuves ont fait les sols', 'Rivers built the soils'),
         ('Au fil des millénaires, les cours d’eau ont roulé et déposé graviers et galets arrachés aux montagnes. Ces sols caillouteux drainent très bien et emmagasinent la chaleur du jour.',
          'Over millennia, rivers rolled and dropped gravel and pebbles torn from the mountains. These stony soils drain very well and store the day’s heat.'),
         ('Les croupes de graves du Médoc (qui ont donné leur nom aux Graves) et les galets roulés de Châteauneuf-du-Pape, apportés par le Rhône depuis les Alpes.',
          'The gravel mounds of the Médoc (which gave the Graves its name) and the rolled pebbles of Châteauneuf-du-Pape, carried down from the Alps by the Rhône.')),
        (('La montagne fait écran', 'Mountains act as a shield'),
         ('Une chaîne de montagnes arrête les nuages venus de l’océan : derrière elle, le climat est plus sec et plus ensoleillé. Les vignes s’installent sur ses contreforts, à l’abri.',
          'A mountain range stops the clouds coming in from the ocean: behind it, the climate is drier and sunnier. Vineyards settle on its sheltered foothills.'),
         ('Protégée par les Vosges, Colmar est l’une des villes les plus sèches de France — une aubaine pour les vins d’Alsace.',
          'Sheltered by the Vosges, Colmar is one of the driest towns in France — a blessing for Alsace wines.')),
    ],
    close=('En résumé : <b>suivez l’eau et cherchez la pente</b>. Le fleuve a apporté les sols, les clients et la douceur du climat ; le coteau a apporté le drainage, le soleil et la protection contre le gel.',
           'In short: <b>follow the water and look for the slope</b>. The river brought the soils, the customers and a milder climate; the slope brought drainage, sunshine and shelter from frost.'),
)


def context_html(C, sub=None, sid=''):
    if not C:
        return ''
    subt = tr(sub[0], sub[1], 'p', 'ctxsub') if sub else ''
    idattr = f' id="{sid}"' if sid else ''
    cards = ''.join(
        f'<li class="ctxc"><span class="ctxn">{k + 1}</span>{tr(t[0], t[1], "h3")}{tr(b[0], b[1], "p")}'
        f'{tr("<b>Exemple —</b> " + e[0], "<b>Example —</b> " + e[1], "p", "ctxe")}</li>'
        for k, (t, b, e) in enumerate(C['points']))
    # small wine-regions map of France (the site's own Carte de France export) → links to the interactive map
    cmap = ('<a class="ctxmap" href="../../Vignobles%20de%20France%20%E2%80%94%20Carte%20de%20France.html">'
            '<img src="../../assets/aoc_map_bg.svg" width="2200" height="2060" loading="lazy" '
            'alt="Carte des régions viticoles françaises / Map of the French wine regions">'
            + tr('Les régions viticoles<br>carte interactive →', 'The wine regions<br>interactive map →', 'span') + '</a>')
    return (f'<section class="ctx"{idattr}><div class="ctxhead">{cmap}<div class="ctxtxt"><p class="kick" data-fr="Contexte" data-en="Background">Contexte</p>'
            f'{tr(C["title"][0], C["title"][1], "h2")}{subt}{tr(C["lead"][0], C["lead"][1], "p", "ctxl")}</div></div>'
            f'<ol class="ctxg">{cards}</ol>{tr(C["close"][0], C["close"][1], "p", "ctxs")}</section>')


SOURCES = [
    ('Insee, <i>Bilan démographique 2025</i>, Insee Première, janvier 2026 (population au 1<sup>er</sup> janvier 2026).',
     'Insee, <i>Bilan démographique 2025</i>, Insee Première, January 2026 (population on 1 January 2026).', 'https://www.insee.fr/fr/statistiques/8719824'),
    ('DGCL, <i>Les structures territoriales au 1<sup>er</sup> janvier</i> (BIS n° 206) : 34 875 communes au 1<sup>er</sup> janvier 2026.',
     'DGCL, <i>Les structures territoriales au 1<sup>er</sup> janvier</i> (BIS No 206): 34,875 communes on 1 January 2026.', 'https://www.collectivites-locales.gouv.fr/actualites/bis-206-les-structures-territoriales-au-1er-janvier'),
    ('CIA, <i>The World Factbook</i>, « France » : frontières terrestres et littoral de la France métropolitaine.',
     'CIA, <i>The World Factbook</i>, “France”: land borders and coastline of metropolitan France.', 'https://www.cia.gov/the-world-factbook/countries/france/'),
    ('Cours d’eau, plans d’eau et trait de côte : BD TOPAGE® (IGN / OFB), diffusée par le Sandre, Licence Ouverte Etalab 2.0.',
     'Rivers, lakes and coastline: BD TOPAGE® (IGN / OFB), distributed by Sandre, Etalab Open Licence 2.0.', 'https://www.sandre.eaufrance.fr/'),
    ('Méthode de l’hexagone et carte finale : présentation « Drawing France the Easy Way » de Christophe A. Paul.',
     'Hexagon method and final map: “Drawing France the Easy Way” presentation by Christophe A. Paul.', None),
    ('Bassins hydrographiques : Sandre, référentiel « Bassin hydrographique » (France métropolitaine), Licence Ouverte Etalab 2.0.',
     'River basins: Sandre, “Bassin hydrographique” reference dataset (mainland France), Etalab Open Licence 2.0.', 'https://www.sandre.eaufrance.fr/'),
    ('Relief : Terrain Tiles (Mapzen / Amazon Web Services) — SRTM, EU-DEM et autres sources ; ombrage et teintes de l’auteur.',
     'Relief: Terrain Tiles (Mapzen / Amazon Web Services) — SRTM, EU-DEM and other sources; shading and colours by the author.', 'https://registry.opendata.aws/terrain-tiles/'),
    ('Carte et texte : Christophe A. Paul, d’après sa présentation « Drawing France the Easy Way ».',
     'Map and text: Christophe A. Paul, after his presentation “Drawing France the Easy Way”.', None),
]


PARTS = {
    # Part 1 — France in numbers + the six river basins, on the author's own relief map (GeoJson Files/Geography_Rivers/hq).
    # Still a local draft (git-ignored) until the user approves it.
    1: dict(out=HERE / '_part1' / 'Geography_Part1.html', img=HERE / '_part1' / 'img',
            title=('L’importance de la géographie', 'The Importance of Geography'),
            h1=('L’importance de la <em>géographie</em>', 'The importance of <em>geography</em>'),
            tagline=('La France en chiffres, ses montagnes, puis ses six bassins hydrographiques : chaque fleuve se dessine de sa source jusqu’à la mer, avec les vins qui poussent sur ses rives. Lancez la lecture, mettez en pause, revenez en arrière ou sautez directement à un chapitre.',
                     'France in numbers, its mountains, then its six river basins: each river draws itself from source to sea, with the wines that grow along its banks. Play, pause, rewind, or jump straight to a chapter.'),
            desc='Un film interactif : la France en chiffres, puis ses six bassins hydrographiques, fleuve par fleuve, et les vins qui les bordent.',
            sources=[0, 1, 2, 3, 5, 6, 7], css='CSS1', context=CONTEXT),
    # Part 2 — Drawing France (was 4:59 → end of the single film)
    2: dict(out=OUTDIR / 'Drawing_France.html', img=IMG,
            title=('Dessiner la France', 'Drawing France'),
            h1=('Dessiner la <em>France</em>', 'Drawing <em>France</em>'),
            tagline=('Un hexagone, quelques traits… et vous saurez dessiner la France de mémoire, puis y placer ses grands fleuves, ses villes et ses régions viticoles. Lancez la lecture, mettez en pause, revenez en arrière ou sautez directement à un chapitre.',
                     'A hexagon and a few lines… and you will be able to draw France from memory, then place its great rivers, its cities and its wine regions. Play, pause, rewind, or jump straight to a chapter.'),
            desc='Un film interactif : dessiner la France à main levée à partir d’un hexagone, puis y placer les grands fleuves, les villes et les régions viticoles.',
            sources=[4], css='', context=None),
}


def build_film(part):
    """One film (its own timeline) → the HTML block of the player + its JSON data."""
    global tl
    tl = TL()
    zf = zipfile.ZipFile(PPTX)
    if part == 1:
        load_geo()
        scene_intro()
        scene_numbers()
        scene_mountains()
        scene_rivers_title()
        rivers()
        scene_synthesis()
        scene_explore()
        base, riv, top = part1_layers()
        tl.svg['maps'] = [base, riv] + tl.svg['maps'] + [top]
        drawing = ''
    else:
        save_webp(load(zf, 15), 'map_wine_regions.webp', w=1000, q=82)
        drawing = scene_drawing()
        scene_final()
    tl.t = round(tl.t, 1)      # scene ends are written with 1 decimal: keep the total on the same grid
    total = tl.t

    chaps = []
    for k, c in enumerate(tl.chapters):
        nxt = tl.chapters[k + 1]['start'] if k + 1 < len(tl.chapters) else total
        chaps.append(dict(id=c['id'], start=c['start'], end=nxt))
    ticks = ''.join(f'<i style="left:{c["start"] / total * 100:.3f}%"></i>' for c in tl.chapters[1:])
    chap_btns = ''.join(
        f'<li><button type="button" class="ch" data-i="{k}"><span class="chn">{k + 1:02d}</span>'
        f'{tr(c["fr"], c["en"], "span", "cht")}<span class="chd">{int((chaps[k]["end"] - c["start"]) // 60)}:{int((chaps[k]["end"] - c["start"]) % 60):02d}</span>'
        f'<span class="chp"></span></button></li>' for k, c in enumerate(tl.chapters))
    defs = ('<defs><radialGradient id="soft"><stop offset="0" stop-color="#fff"/><stop offset=".86" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>'
            '<pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse"><path d="M18 0H0V18" fill="none" class="gridl"/></pattern>'
            '<marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" class="arrh"/></marker></defs>') if part == 2 else ''
    stage_svg = (f'<svg class="scr" viewBox="0 0 720 540" role="img" aria-label="{att(PARTS[part]["title"][0])}">{defs}'
                 f'<rect width="720" height="540" class="stagebg"/>'
                 f'{"".join(tl.svg["maps"])}{drawing}{"".join(tl.svg["final"])}</svg>')
    html = FILM_TPL
    for k, v in {'%FID%': str(part), '%STAGE%': stage_svg, '%CARDS%': ''.join(tl.cards), '%NOTES%': ''.join(tl.notes),
                 '%CHAPS%': chap_btns, '%TICKS%': ticks, '%TOTAL%': f'{int(total // 60)}:{int(total % 60):02d}'}.items():
        html = html.replace(k, v)
    print(f'  film {part}: {total:.0f} s, {len(tl.chapters)} chapters')
    return html, dict(total=total, chapters=chaps, explore=getattr(tl, 'explore', None))


def scope_css(css, scope):
    """Prefix every selector of a flat stylesheet with the film it belongs to."""
    def fix(m):
        sels = []
        for sel in m.group(1).split(','):
            sel = sel.strip()
            sels.append(sel.replace('.film', '.film' + scope, 1) if sel.startswith('.film') else f'.film{scope} {sel}')
        return ','.join(sels) + '{'
    return re.sub(r'([^{}]+)\{', fix, css)


BASICS = dict(
    title=('Vins de France : les bases', 'French Wines: The Basics'),
    eyebrow=('Les bases · deux films interactifs', 'The basics · two interactive films'),
    h1=('Vins de France : <em>les bases</em>', 'French wines: <em>the basics</em>'),
    tagline=('Deux films pour poser les bases : d’abord la géographie — les montagnes, les six bassins et leurs fleuves, et les vins qui poussent sur leurs rives —, puis comment dessiner la France de mémoire et y placer ses régions viticoles. Lancez la lecture, mettez en pause, revenez en arrière ou sautez directement à un chapitre.',
             'Two films to lay the foundations: first the geography — the mountains, the six river basins and their rivers, and the wines that grow along their banks —, then how to draw France from memory and place its wine regions. Play, pause, rewind, or jump straight to a chapter.'),
    desc='Deux films interactifs : la géographie de la France (montagnes, bassins, fleuves et vins qui les bordent), puis comment dessiner la France et y placer les régions viticoles.',
    film_eyebrows={1: ('Film 1 · La géographie', 'Film 1 · Geography'), 2: ('Film 2 · Le dessin', 'Film 2 · Drawing')},
    # section title + subtitle replacing a film's own title on this page
    film_heads={2: (('Apprendre les <em>vins de France</em>', 'Learning <em>French wine</em>'),
                    ('La façon la plus simple d’apprendre les vins de France : connaître la géographie de la France',
                     'Easiest way to learn French wine: know the geography of France'))},
)

PAGES = {
    # the published page: both films, each under its own heading, the context section after film 1
    'basics': dict(out=OUTDIR / 'French_Wines_The_Basics.html', img=IMG, head=BASICS, films=[1, 2], context=CONTEXT),
    # Part 1 draft page: the basins film, the context, then « Dessiner la France » (git-ignored until approved)
    1: dict(out=HERE / '_part1' / 'Geography_Part1.html', img=HERE / '_part1' / 'img', head=1, films=[1, 2], context=CONTEXT),
    # the standalone « Dessiner la France » page
    2: dict(out=OUTDIR / 'Drawing_France.html', img=IMG, head=2, films=[2], context=None),
}


def build(page='basics'):
    global IMG, OUT
    import os
    G = PAGES[page]
    IMG, OUT = G['img'], G['out']
    OUT.parent.mkdir(parents=True, exist_ok=True)
    IMG.mkdir(parents=True, exist_ok=True)
    H = G['head'] if isinstance(G['head'], dict) else PARTS[G['head']]
    eyebrows = H.get('film_eyebrows')

    def fhead(part, P):
        fh = H.get('film_heads', {}).get(part)
        if not fh:
            return tr(P['h1'][0], P['h1'][1], 'h2')
        return tr(fh[0][0], fh[0][1], 'h2') + tr(fh[1][0], fh[1][1], 'p', 'fsub')
    body, data, css, srcs = [], {}, CSS, []
    for k, part in enumerate(G['films']):
        P = PARTS[part]
        html, d = build_film(part)
        data[str(part)] = d
        if P['css']:
            css += scope_css(globals()[P['css']], f'[data-f="{part}"]')
        if k == 0 and G['context']:      # « Le vin et la géographie » comes first, before the map film
            if eyebrows:   # multi-film page: film 1's title becomes the context section's subtitle (no separate heading)
                body.append(context_html(G['context'], sub=P['h1'], sid=f'film-{part}'))
            else:
                body.append(context_html(G['context']))
        if k > 0 or (eyebrows and not G['context']):      # a second film (or every film, on a multi-film page) gets its own heading
            eb = eyebrows[part] if eyebrows else ('Géographie · film interactif', 'Geography · interactive film')
            body.append(f'<section class="film-head" id="film-{part}">{tr(eb[0], eb[1], "p", "eyebrow")}'
                        f'{fhead(part, P)}<div class="rule"></div>{tr(P["tagline"][0], P["tagline"][1], "p", "tagline")}</section>')
        body.append(html)
        srcs += [i for i in P['sources'] if i not in srcs]

    def link(u):
        return f' <a href="{u}" target="_blank" rel="noopener">↗</a>' if u else ''
    src = ''.join(f'<li>{tr(SOURCES[i][0], SOURCES[i][1])}{link(SOURCES[i][2])}</li>' for i in sorted(srcs))

    html = TEMPLATE
    for k, v in {'%BASECSS%': base_css(), '%CSS%': css, '%BODY%': '\n'.join(body), '%DATA%': json.dumps(data, separators=(',', ':')),
                 '%PTITLE%': json.dumps(list(H['title']), ensure_ascii=False), '%SOURCES%': src, '%JS%': JS, '%T_FR%': H['title'][0], '%DESC%': H['desc'],
                 '%H1%': tr(H['h1'][0], H['h1'][1], 'h1'),
                 '%EYEBROW%': tr(*H.get('eyebrow', ('Géographie · film interactif', 'Geography · interactive film')), 'p', 'eyebrow'), '%TAG%': tr(H['tagline'][0], H['tagline'][1], 'p', 'tagline')}.items():
        html = html.replace(k, v)
    # site assets (theme, menu, favicon, background) are linked from the repo root: fix the depth for wherever the page lives
    rel = os.path.relpath(REPO, OUT.parent).replace(os.sep, '/') + '/'
    if rel != '../../':
        html = html.replace('"../../', '"' + rel).replace("'../../", "'" + rel).replace('(../../', '(' + rel).replace('&quot;../../', '&quot;' + rel)
    OUT.write_text(html, encoding='utf-8')
    print(f'wrote {OUT.relative_to(REPO)} — {len(html) // 1024} KB')


# ------------------------------------------------------------------ template
TEMPLATE = r'''<!doctype html>
<html lang="fr">
<head>
<!--fw-theme:start--><script src="../../assets/theme.js"></script><!--fw-theme:end-->
<!--fw-favicon:start--><link rel="icon" href="../../favicon.ico" sizes="48x48"><link rel="icon" type="image/png" href="../../assets/favicon.png" sizes="192x192"><link rel="apple-touch-icon" href="../../apple-touch-icon.png"><!--fw-favicon:end-->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%T_FR%</title>
<meta name="description" content="%DESC%">
<style>
%BASECSS%
%CSS%
</style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <a class="back" href="../../index.html" data-fr="← Accueil" data-en="← Home">← Accueil</a>
    <button class="lang" id="langbtn" type="button" aria-label="Language"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.6 2.8 2.6 15.2 0 18M12 3c-2.6 2.8-2.6 15.2 0 18"/></svg><span id="langlbl">English</span></button>
  </div>
  <header>
    %EYEBROW%
    %H1%
    <div class="rule"></div>
    %TAG%
  </header>

%BODY%

  <section class="srcs">
    <h2 data-fr="Sources et crédits" data-en="Sources and credits">Sources et crédits</h2>
    <ol>%SOURCES%</ol>
  </section>
</div>
<script>window.PAGE_TITLE = %PTITLE%; window.FILMS_DATA = %DATA%;</script>
<script>
%JS%
</script>
</body>
</html>
'''

FILM_TPL = r'''  <div class="film" data-f="%FID%">
    <nav class="chapters panel" aria-label="Chapitres">
      <p class="kick" data-fr="Chapitres" data-en="Chapters">Chapitres</p>
      <ol>%CHAPS%</ol>
    </nav>
    <div class="player">
      <div class="stage" data-k="stage">
        %STAGE%
        <div class="cards">%CARDS%</div>
        <div class="endbtns" data-k="endbtns">
          <button type="button" class="pill" data-k="replay" data-fr="↺ Revoir" data-en="↺ Watch again">↺ Revoir</button>
          <a class="pill" href="../../Vignobles%20de%20France%20%E2%80%94%20Carte%20de%20France.html" data-fr="Carte des vignobles →" data-en="Vineyard map →">Carte des vignobles →</a>
        </div>
        <button type="button" class="bigplay" data-k="bigplay" aria-label="Lecture / Play"><svg viewBox="0 0 24 24"><path d="M8 5v14l11-7z"/></svg></button>
      </div>
      <div class="ctrl panel">
        <div class="bar">
          <input type="range" class="seek" data-k="seek" min="0" max="1000" step="1" value="0" aria-label="Position">
          <div class="ticks" aria-hidden="true">%TICKS%</div>
        </div>
        <div class="btns">
          <button type="button" data-k="b-restart" class="ib" data-tip-fr="Depuis le début (Début)" data-tip-en="From the start (Home)"><svg viewBox="0 0 24 24"><path d="M6 5h2v14H6zM20 5v14L9 12z"/></svg></button>
          <button type="button" data-k="b-prev" class="ib" data-tip-fr="Chapitre précédent (Maj+←)" data-tip-en="Previous chapter (Shift+←)"><svg viewBox="0 0 24 24"><path d="M11 6v12l-8.5-6zM21 6v12l-8.5-6z"/></svg></button>
          <button type="button" data-k="b-back" class="ib" data-tip-fr="Reculer de 5 s (←)" data-tip-en="Back 5 s (←)"><svg viewBox="0 0 24 24"><path d="M12 5V2L7 6l5 4V7a6 6 0 1 1-6 6H4a8 8 0 1 0 8-8z"/><text x="12" y="16.2" font-size="6.4" text-anchor="middle" font-weight="700">5</text></svg></button>
          <button type="button" data-k="b-play" class="ib play" data-tip-fr="Lecture / pause (Espace)" data-tip-en="Play / pause (Space)"><svg viewBox="0 0 24 24" class="i-play"><path d="M8 5v14l11-7z"/></svg><svg viewBox="0 0 24 24" class="i-pause"><path d="M6 5h4v14H6zM14 5h4v14h-4z"/></svg></button>
          <button type="button" data-k="b-fwd" class="ib" data-tip-fr="Avancer de 5 s (→)" data-tip-en="Forward 5 s (→)"><svg viewBox="0 0 24 24"><path d="M12 5V2l5 4-5 4V7a6 6 0 1 0 6 6h2a8 8 0 1 1-8-8z"/><text x="12" y="16.2" font-size="6.4" text-anchor="middle" font-weight="700">5</text></svg></button>
          <button type="button" data-k="b-next" class="ib" data-tip-fr="Chapitre suivant (Maj+→)" data-tip-en="Next chapter (Shift+→)"><svg viewBox="0 0 24 24"><path d="M13 6v12l8.5-6zM3 6v12l8.5-6z"/></svg></button>
          <span class="time"><span data-k="tcur">0:00</span> / %TOTAL%</span>
          <span class="sp"></span>
          <label class="speed"><span data-fr="Vitesse" data-en="Speed">Vitesse</span>
            <select class="spd" data-k="speed"><option value="0.75">0,75×</option><option value="1" selected>1×</option><option value="1.25">1,25×</option><option value="1.5">1,5×</option><option value="2">2×</option></select></label>
          <button type="button" data-k="b-full" class="ib" data-tip-fr="Plein écran (F)" data-tip-en="Full screen (F)"><svg viewBox="0 0 24 24"><path d="M4 9V4h5v2H6v3zM20 9V4h-5v2h3v3zM4 15v5h5v-2H6v-3zM20 15v5h-5v-2h3v-3z"/></svg></button>
        </div>
      </div>
    </div>
    <aside class="notes panel" data-k="notes" aria-live="polite">%NOTES%</aside>
  </div>
'''

CSS = r'''
  .wrap{max-width:1440px;}
  .kick{text-transform:uppercase;letter-spacing:.28em;font-size:10px;font-weight:700;color:var(--gold);margin:0 0 8px;}
  .film{display:grid;grid-template-columns:220px minmax(0,1fr) 340px;gap:16px;align-items:start;}
  .player{min-width:0;}
  .stage{position:relative;aspect-ratio:4/3;border-radius:16px;overflow:hidden;background:#f6efe0;box-shadow:var(--shadow);
    border:1px solid var(--hair);cursor:pointer;user-select:none;-webkit-user-select:none;}
  .scr{position:absolute;inset:0;width:100%;height:100%;display:block;}
  .stagebg,.paper{fill:#f6efe0;}
  .gridl{stroke:rgba(80,110,150,.10);stroke-width:.6;}
  image.dim{filter:saturate(.6) brightness(.9);opacity:.45;}
  .scene{will-change:opacity;}
  /* drawing */
  .fr-fill{fill:#5f8f5a;fill-opacity:.16;stroke:none;}
  .fr-line{fill:none;stroke:#4f7f4a;stroke-width:1.5;stroke-linejoin:round;}
  .stitle{font:500 26px/1 var(--serif);fill:#3a1219;text-anchor:middle;}
  .stitle .em{font-style:italic;fill:#8e1f33;}
  .ink{fill:none;stroke:#2b211c;stroke-linecap:round;stroke-linejoin:round;}
  .hex{stroke-width:3.2;}
  .arc{stroke-width:1.8;}
  .mouth{stroke-width:1.6;}
  .guide{fill:none;stroke:#6b5f55;stroke-width:.9;stroke-dasharray:none;opacity:.75;}
  .hint{fill:none;stroke:#c0392b;stroke-width:1.6;}
  .arrh{fill:#c0392b;}
  .river{fill:none;stroke:#2f6fb0;stroke-width:4.2;stroke-linecap:round;}
  .sea{font:italic 600 15px/1 var(--serif);fill:#2a4f86;text-anchor:middle;dominant-baseline:central;}
  .country{font:600 9.5px/1 var(--sans);letter-spacing:.14em;fill:#7a6d62;text-anchor:middle;dominant-baseline:central;}
  .rlab{font:italic 600 12px/1 var(--serif);fill:#1f5a98;text-anchor:middle;dominant-baseline:central;paint-order:stroke;stroke:#f6efe0;stroke-width:3px;}
  .city circle{fill:#8e1f33;}
  .city .halo{fill:#8e1f33;opacity:.18;}
  .clab{font:700 10.5px/1 var(--sans);fill:#8e1f33;text-anchor:middle;dominant-baseline:central;paint-order:stroke;stroke:#f6efe0;stroke-width:3px;}
  .reg{fill:var(--c);fill-opacity:.5;stroke:var(--c);stroke-width:1.2;}
  .glab{font:italic 700 12px/1 var(--serif);fill:#20120e;text-anchor:middle;dominant-baseline:central;paint-order:stroke;stroke:rgba(246,239,224,.85);stroke-width:2.6px;}
  .num circle{fill:#fffdf8;stroke:#8e1f33;stroke-width:1.4;transition:fill .25s;}
  .num text{font:700 9.5px/1 var(--sans);fill:#8e1f33;text-anchor:middle;dominant-baseline:central;}
  .num.hot circle{fill:#8e1f33;}
  .num.hot text{fill:#fff;}
  .tada{font:italic 700 46px/1 var(--serif);fill:#8e1f33;text-anchor:middle;}
  .note{font:30px/1 var(--serif);fill:#2b211c;text-anchor:middle;}
  /* overlay cards */
  .cards{position:absolute;inset:0;pointer-events:none;}
  .card{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;
    padding:6% 10%;background:radial-gradient(80% 70% at 50% 50%,rgba(246,239,224,.94),rgba(246,239,224,.80));opacity:0;visibility:hidden;}
  .ctitle{font:500 clamp(20px,3.6vw,44px)/1.1 var(--serif);color:#3a1219;margin:0;}
  .ctitle em{color:#8e1f33;}
  .csub{font:300 clamp(13px,1.5vw,18px)/1.55 var(--sans);color:#5a3a40;max-width:34em;margin:16px 0 0;}
  .card.hero .ctitle{font-size:clamp(26px,5vw,62px);}
  .card.endcard{background:rgba(246,239,224,.72);}
  .endbtns{position:absolute;left:0;right:0;bottom:16%;display:flex;gap:12px;justify-content:center;opacity:0;visibility:hidden;transition:opacity .4s;}
  .endbtns.on{opacity:1;visibility:visible;}
  .pill{font:600 12px/1 var(--sans);letter-spacing:.08em;text-decoration:none;cursor:pointer;color:#fff;background:#8e1f33;border:0;border-radius:999px;padding:11px 18px;}
  .pill+.pill{background:#fffdf8;color:#8e1f33;border:1px solid rgba(142,31,51,.35);}
  .bigplay{position:absolute;left:50%;top:78%;width:84px;height:84px;margin:-42px 0 0 -42px;border-radius:50%;border:0;cursor:pointer;
    background:rgba(142,31,51,.9);box-shadow:0 10px 30px rgba(60,10,20,.35);display:grid;place-items:center;transition:opacity .3s,transform .2s;}
  .bigplay svg{width:40px;height:40px;fill:#fff;margin-left:5px;}
  .bigplay:hover{transform:scale(1.06);}
  .film.started .bigplay{opacity:0;pointer-events:none;}
  /* controls */
  .ctrl{margin-top:12px;padding:10px 14px 12px;border-radius:14px;}
  .bar{position:relative;height:22px;}
  .bar input{position:absolute;inset:0;width:100%;margin:0;background:transparent;-webkit-appearance:none;appearance:none;cursor:pointer;z-index:2;}
  .bar input::-webkit-slider-runnable-track{height:6px;border-radius:3px;background:linear-gradient(90deg,var(--gold) var(--p,0%),var(--track) var(--p,0%));}
  .bar input::-moz-range-track{height:6px;border-radius:3px;background:linear-gradient(90deg,var(--gold) var(--p,0%),var(--track) var(--p,0%));}
  .bar input::-webkit-slider-thumb{-webkit-appearance:none;width:16px;height:16px;border-radius:50%;background:var(--gold);margin-top:-5px;border:2px solid var(--solid);}
  .bar input::-moz-range-thumb{width:13px;height:13px;border-radius:50%;background:var(--gold);border:2px solid var(--solid);}
  .bar input{--track:rgba(128,128,128,.25);}
  .ticks{position:absolute;left:8px;right:8px;top:6px;height:10px;pointer-events:none;z-index:3;}
  .ticks i{position:absolute;top:0;width:2px;height:10px;margin-left:-1px;background:var(--solid);opacity:.9;}
  .btns{display:flex;align-items:center;gap:4px;flex-wrap:wrap;margin-top:6px;}
  .ib{width:38px;height:38px;border-radius:50%;border:1px solid transparent;background:transparent;color:var(--gold-soft);cursor:pointer;display:grid;place-items:center;padding:0;}
  .ib:hover{border-color:var(--hair-hi);background:var(--glass-hi);}
  .ib svg{width:20px;height:20px;fill:currentColor;}
  .ib text{fill:currentColor;font-family:var(--sans);}
  .ib.play{width:46px;height:46px;background:var(--gold);color:var(--solid);}
  .ib.play svg{width:24px;height:24px;}
  .ib .i-pause,.film.playing .ib .i-play{display:none;}
  .film.playing .ib .i-pause{display:block;}
  .time{font:600 12px/1 var(--sans);font-variant-numeric:tabular-nums;color:var(--muted);margin-left:8px;}
  .sp{flex:1;}
  .speed{display:flex;align-items:center;gap:6px;font:600 10px/1 var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);}
  .speed select{font:600 12px var(--sans);color:var(--parchment);background:var(--glass-hi);border:1px solid var(--hair);border-radius:8px;padding:5px 6px;}
  /* chapters */
  .chapters{padding:14px 10px;border-radius:14px;position:sticky;top:12px;max-height:calc(100vh - 24px);overflow:auto;}
  .chapters .kick{padding-left:8px;}
  .chapters ol{list-style:none;margin:0;padding:0;}
  .ch{position:relative;display:grid;grid-template-columns:22px 1fr auto;gap:6px;align-items:baseline;width:100%;text-align:left;cursor:pointer;
    background:none;border:0;border-radius:9px;padding:8px 8px 10px;color:var(--parchment);font:400 13px/1.3 var(--sans);overflow:hidden;}
  .ch:hover{background:var(--track);}
  .chn{font:700 10px/1 var(--sans);color:var(--gold);letter-spacing:.06em;}
  .chd{font:600 10px/1 var(--sans);color:var(--faint);font-variant-numeric:tabular-nums;}
  .chp{position:absolute;left:8px;right:8px;bottom:4px;height:2px;border-radius:1px;background:linear-gradient(90deg,var(--gold) var(--cp,0%),transparent var(--cp,0%));opacity:.8;}
  .ch.on{background:var(--glass-hi);box-shadow:inset 3px 0 0 var(--gold);}
  .ch.on .cht{font-weight:700;}
  /* notes */
  .notes{border-radius:14px;padding:16px 16px 10px;position:relative;min-height:200px;max-height:calc(100vh - 24px);overflow:auto;position:sticky;top:12px;}
  .nb{display:none;}
  .nb.on{display:block;}
  .nb h3{font:500 22px/1.15 var(--serif);color:var(--title);margin:0 0 12px;}
  .its{list-style:none;margin:0;padding:0;}
  .it{font:400 14px/1.55 var(--sans);color:var(--muted);padding:9px 10px 9px 12px;margin:0 0 4px;border-left:2px solid var(--hair);border-radius:0 8px 8px 0;cursor:pointer;opacity:0;visibility:hidden;transition:background .25s,border-color .25s,color .25s;}
  .it:hover{background:var(--track);}
  .it.now{color:var(--parchment);border-left-color:var(--gold);background:var(--track);}
  .it b{color:var(--gold-soft);}
  .legw{list-style:none;margin:2px 0 8px;}
  .leg{list-style:none;margin:0;padding:0 0 0 12px;display:flex;flex-wrap:wrap;gap:6px;}
  .leg li{display:inline-flex;align-items:center;gap:6px;font:500 12.5px/1 var(--sans);color:var(--parchment);background:var(--track);border:1px solid var(--hair);border-radius:999px;padding:5px 10px 5px 5px;opacity:0;visibility:hidden;}
  .leg li.hot{background:#8e1f33;border-color:#8e1f33;color:#fff;}
  .leg li.hot b{background:#fff;color:#8e1f33;}
  .hlb{display:inline-grid;place-items:center;min-width:18px;height:18px;padding:0 4px;margin:0 4px 0 0;border-radius:9px;background:#8e1f33;color:#fff;font:700 10px/1 var(--sans);vertical-align:1px;}
  .leg b{display:inline-grid;place-items:center;width:18px;height:18px;border-radius:50%;background:#8e1f33;color:#fff;font:700 10px/1 var(--sans);}
  .ctx{margin:clamp(44px,6vw,72px) auto 0;max-width:1100px;}
  .ctx h2{font:500 clamp(26px,3.6vw,38px)/1.1 var(--serif);color:var(--title);margin:0 0 12px;}
  .ctx h2 em{font-style:italic;color:var(--gold-soft);}
  .ctxhead{display:flow-root;margin-bottom:clamp(26px,3.5vw,40px);}   /* text wraps around the floated map */
  .ctxtxt{display:contents;}
  .ctxmap{float:right;width:clamp(190px,27vw,340px);margin:0 0 clamp(18px,2.5vw,28px) clamp(18px,3vw,40px);display:block;text-decoration:none;text-align:center;}
  .ctxmap img{display:block;width:100%;height:auto;filter:drop-shadow(0 6px 14px rgba(40,10,15,.22));transition:transform .25s;}
  .ctxmap:hover img{transform:scale(1.04);}
  .ctxmap span{display:block;margin-top:8px;font:600 13.5px/1.35 var(--sans);letter-spacing:.08em;text-transform:uppercase;color:var(--gold);}
  @media (max-width:640px){.ctxhead{display:flex;flex-direction:column;}.ctxtxt{display:block;}.ctxmap{order:2;float:none;width:min(320px,85%);margin:8px auto 0;}}
  .ctxsub{font:400 clamp(19px,2.4vw,26px)/1.2 var(--serif);color:var(--muted);margin:-4px 0 14px;}
  .ctxsub em{font-style:italic;color:var(--gold-soft);}
  .ctx + .film{margin-top:clamp(28px,4vw,44px);}
  .ctxl{font:300 16px/1.7 var(--sans);color:var(--muted);max-width:780px;margin:0 0 22px;}
  .ctxg{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;}
  .ctxc{position:relative;background:var(--glass);border:1px solid var(--hair);border-radius:14px;padding:18px 18px 16px 58px;}
  .ctxn{position:absolute;left:16px;top:16px;width:28px;height:28px;border-radius:50%;display:grid;place-items:center;
    background:#8e1f33;color:#fff;font:700 13px/1 var(--sans);}
  .ctxc h3{font:500 19px/1.2 var(--serif);color:var(--title);margin:2px 0 8px;}
  .ctxc p{font:400 14px/1.6 var(--sans);color:var(--muted);margin:0 0 8px;}
  .ctxc p.ctxe{font-size:13px;color:var(--parchment);opacity:.85;border-top:1px solid var(--hair);padding-top:8px;margin:0;}
  .ctxe b,.ctxs b{color:var(--gold-soft);}
  .ctxs{font:italic 400 17px/1.6 var(--serif);color:var(--parchment);text-align:center;max-width:760px;margin:24px auto 0;}
  .film-head{text-align:center;margin:clamp(56px,7vw,90px) 0 clamp(22px,3vw,34px);}
  .film-head h2{font-family:var(--serif);font-weight:500;font-size:clamp(34px,5.5vw,62px);line-height:1;margin:0;color:var(--title);}
  .film-head h2 em{font-style:italic;color:var(--gold-soft);}
  .film-head .fsub{font:400 clamp(18px,2.3vw,25px)/1.3 var(--serif);font-style:italic;color:var(--muted);max-width:940px;margin:14px auto 0;text-wrap:balance;}
  .srcs{margin:44px auto 0;max-width:900px;}
  .srcs h2{font:500 22px/1.2 var(--serif);color:var(--title);margin:0 0 10px;}
  .srcs ol{margin:0;padding-left:20px;font:400 13px/1.6 var(--sans);color:var(--muted);}
  .srcs a{color:var(--gold);text-decoration:none;}
  /* full screen */
  .film:fullscreen{background:var(--solid);padding:16px;grid-template-columns:minmax(0,1fr) 360px;align-content:center;overflow:auto;}
  .film:fullscreen .chapters{display:none;}
  .film:fullscreen .stage{max-height:calc(100vh - 130px);margin:0 auto;}
  @media (max-width:1180px){
    .film{grid-template-columns:minmax(0,1fr) 320px;}
    .chapters{grid-column:1 / -1;position:static;max-height:none;padding:10px;}
    .chapters ol{display:flex;gap:6px;overflow-x:auto;padding-bottom:4px;scrollbar-width:thin;}
    .chapters li{flex:0 0 auto;}
    .ch{grid-template-columns:auto auto;white-space:nowrap;border:1px solid var(--hair);}
    .chd{display:none;}
  }
  @media (max-width:820px){
    .film{grid-template-columns:minmax(0,1fr);}
    .notes{position:static;max-height:none;}
    .stage{border-radius:12px;}
    .bigplay{width:64px;height:64px;margin:-32px 0 0 -32px;}
    .bigplay svg{width:30px;height:30px;}
    .ib{width:34px;height:34px;}
    .speed>span{display:none;}
    .it:not(.shown),.leg li:not(.shown){display:none;}
    .notes{min-height:0;}
  }
'''

CSS1 = r'''
  .stage,.stagebg,.paper{background:#fff;fill:#fff;}
  .rh{fill:none;stroke:#eef5ee;stroke-opacity:.85;stroke-linecap:round;stroke-linejoin:round;}
  .rv{fill:none;stroke:#2870b2;stroke-linecap:round;stroke-linejoin:round;}
  .spot{fill:#fff;fill-opacity:.5;}
  .bact{fill:none;stroke:#8e1f33;stroke-width:1.1;stroke-dasharray:3 2.2;stroke-opacity:.75;}
  .bline{fill:none;stroke:#8e1f33;stroke-width:.9;stroke-dasharray:3 2.2;stroke-opacity:.6;}
  .bcap .bk{font:700 8.5px/1 var(--sans);letter-spacing:.28em;text-transform:uppercase;fill:#a07a2c;}
  .bcap .bt{font:italic 600 19px/1 var(--serif);fill:#3a1219;}
  .rname{font:italic 700 11px/1 var(--serif);fill:#1d5690;text-anchor:middle;dominant-baseline:central;paint-order:stroke;stroke:rgba(255,255,255,.9);stroke-width:3px;}
  .blab{font:italic 700 12.5px/1 var(--serif);fill:#5a1626;text-anchor:middle;dominant-baseline:central;paint-order:stroke;stroke:rgba(255,255,255,.88);stroke-width:3.2px;}
  .sea{font:italic 600 13px/1 var(--serif);fill:#2a5a8f;text-anchor:middle;dominant-baseline:central;}
  .country{font:600 8.5px/1 var(--sans);letter-spacing:.16em;fill:#6f645b;text-anchor:middle;dominant-baseline:central;paint-order:stroke;stroke:rgba(255,255,255,.85);stroke-width:2.4px;}
  .mount{font:italic 700 11.5px/1 var(--serif);fill:#5b4630;text-anchor:middle;dominant-baseline:central;paint-order:stroke;stroke:rgba(255,255,255,.8);stroke-width:3px;}
  .city circle{stroke:#fff;stroke-width:.9;}
  .city.major circle{fill:#3a1219;}
  .city.wine circle{fill:#8e1f33;}
  .ctxt{dominant-baseline:central;paint-order:stroke;stroke:rgba(255,255,255,.92);stroke-linejoin:round;}
  .ctxt.major{font:700 9.5px/1 var(--sans);fill:#3a1219;stroke-width:2.8px;}
  .ctxt.wine{font:italic 600 8px/1 var(--sans);fill:#7a1a2c;stroke-width:2.4px;}
  .film.picked .names{opacity:.55;}
  .mtn{fill:#8a5a2b;fill-opacity:.14;stroke:#7a4a22;stroke-width:1;stroke-opacity:.75;stroke-linejoin:round;}
  .peak path{fill:#4a2e18;stroke:#fff;stroke-width:.8;}
  .peak text{font:600 8.5px/1 var(--sans);fill:#4a2e18;dominant-baseline:central;paint-order:stroke;stroke:rgba(255,255,255,.9);stroke-width:2.6px;}
  .num circle{stroke-width:1.2;}
  .num text{font-size:8px;}
  /* explorer (last chapter) */
  .hlr{display:none;pointer-events:none;}
  .hlr.on,.hlr.hov{display:inline;}
  .hlr.hov:not(.on){opacity:.55;}
  .hlh{fill:none;stroke:#fff;stroke-opacity:.92;stroke-linecap:round;stroke-linejoin:round;}
  .hlv{fill:none;stroke:#8e1f33;stroke-linecap:round;stroke-linejoin:round;}
  .hlname{font:italic 700 13px/1 var(--serif);fill:#8e1f33;text-anchor:middle;dominant-baseline:central;paint-order:stroke;stroke:#fff;stroke-width:3.4px;}
  .hit{fill:none;stroke:transparent;stroke-width:9;pointer-events:stroke;cursor:pointer;}
  .rivers,.rtop{transition:opacity .35s;}
  .film.picked .rivers{opacity:.4;}
  .film.picked .rtop{opacity:.3;}
  .film.exploring .stage{cursor:default;}
  .film.exploring .bigplay{display:none;}
  .endbtns{left:14px;right:auto;bottom:14px;justify-content:flex-start;}
  .endbtns .pill{padding:8px 13px;font-size:11px;}
  .exhelp{font:400 13px/1.5 var(--sans);color:var(--muted);margin:0 0 12px;}
  .exlist{list-style:none;margin:0;padding:0;}
  .exbk{margin:0 0 12px;}
  .exb{display:block;width:100%;text-align:left;cursor:pointer;background:none;border:0;border-bottom:1px solid var(--hair);padding:6px 2px;margin-bottom:7px;
    font:italic 600 16px/1.2 var(--serif);color:var(--title);}
  .exb:hover,.exb.on{color:var(--gold-soft);border-bottom-color:var(--gold);}
  .exrs{display:flex;flex-wrap:wrap;gap:5px;}
  .exr{display:inline-flex;align-items:center;gap:5px;cursor:pointer;font:500 12.5px/1 var(--sans);color:var(--parchment);background:var(--track);
    border:1px solid var(--hair);border-radius:999px;padding:5px 10px;}
  .exr b{display:inline-grid;place-items:center;width:17px;height:17px;margin-left:-5px;border-radius:50%;background:rgba(142,31,51,.85);color:#fff;font:700 9.5px/1 var(--sans);}
  .exr.main{font-weight:700;border-color:var(--hair-hi);}
  .exr:hover{border-color:var(--hair-hi);}
  .exr.on{background:#8e1f33;border-color:#8e1f33;color:#fff;}
  .exr.on b{background:#fff;color:#8e1f33;}
  .exdet{margin:0 0 14px;}
  .exd{display:none;border-left:2px solid var(--gold);background:var(--track);border-radius:0 10px 10px 0;padding:10px 12px;}
  .exd.on{display:block;}
  .exd h4{font:500 20px/1.15 var(--serif);color:var(--title);margin:2px 0 6px;}
  .exk{font:700 9.5px/1 var(--sans);letter-spacing:.24em;text-transform:uppercase;color:var(--gold);margin:0;}
  .exw{margin:0;padding-left:16px;font:400 13px/1.5 var(--sans);color:var(--muted);}
  .exw li{margin:3px 0;}
  .exw b{color:var(--gold-soft);}
  .exi,.exnone{font:400 13px/1.5 var(--sans);color:var(--muted);margin:0;}
'''

JS = r'''
(function(){
  var LANG = 'fr';
  try{ var s = localStorage.getItem('fw_lang'); if(s==='fr'||s==='en') LANG = s; }catch(e){}
  var FILMS = [], active = null;

  // ---------------------------------------------------------------- language (whole page)
  function applyLang(){
    document.documentElement.lang = LANG;
    document.title = window.PAGE_TITLE[LANG==='fr' ? 0 : 1];
    var nodes = document.querySelectorAll('[data-fr]');
    for(var i=0;i<nodes.length;i++){ var v = nodes[i].getAttribute('data-'+LANG); if(v!==null) nodes[i].innerHTML = v; }
    var tips = document.querySelectorAll('[data-tip-fr]');
    for(var j=0;j<tips.length;j++){ var tt = tips[j].getAttribute('data-tip-'+LANG); tips[j].title = tt; tips[j].setAttribute('aria-label', tt); }
    var lb = document.getElementById('langlbl'); if(lb) lb.textContent = LANG==='fr' ? 'English' : 'Français';
    var sels = document.querySelectorAll('select.spd');
    for(var m=0;m<sels.length;m++){ var opts = sels[m].options; for(var k=0;k<opts.length;k++) opts[k].text = (LANG==='fr' ? opts[k].value.replace('.', ',') : opts[k].value) + '×'; }
  }
  var lbtn = document.getElementById('langbtn');
  if(lbtn) lbtn.addEventListener('click', function(){
    LANG = LANG==='fr' ? 'en' : 'fr';
    try{ localStorage.setItem('fw_lang', LANG); }catch(e){}
    applyLang();
  });
  document.addEventListener('fw:lang', function(e){
    var l = (e.detail && e.detail.lang) || document.documentElement.lang;
    if((l==='fr'||l==='en') && l!==LANG){ LANG = l; applyLang(); }
  });
  applyLang();

  // keyboard goes to the film last played or clicked (the first one by default)
  document.addEventListener('keydown', function(e){
    var tag = (e.target.tagName||'').toLowerCase();
    if(tag==='input' && !e.target.classList.contains('seek') || tag==='select' || tag==='textarea' || e.metaKey || e.ctrlKey || e.altKey) return;
    if(document.querySelector('.fw-search-open, .fw-lang-ov')) return;
    (active || FILMS[0]).key(e);
  });
  document.addEventListener('visibilitychange', function(){ if(document.hidden) FILMS.forEach(function(f){ f.pause(); }); });

  var els = document.querySelectorAll('.film[data-f]');
  for(var n=0;n<els.length;n++) FILMS.push(initFilm(els[n], window.FILMS_DATA[els[n].getAttribute('data-f')]));
  // deep links: #garonne, #villes… (any film) or #t=95 (first film)
  var hh = decodeURIComponent(location.hash.slice(1)), done = false;
  FILMS.forEach(function(f){ if(!done && f.deep(hh)) done = true; });
  if(!done && /^t=\d/.test(hh) && FILMS[0]) FILMS[0].go(parseFloat(hh.slice(2)));
  // plain anchors (#film-1, #film-2…): re-scroll once the menu/theme scripts have settled the layout
  if(!done && hh && document.getElementById(hh)){
    var tgt = document.getElementById(hh);
    window.addEventListener('load', function(){ setTimeout(function(){ tgt.scrollIntoView({block:'start'}); }, 60); });
  }

  function initFilm(film, F){
  var TOTAL = F.total, CH = F.chapters, api = {};
  var $ = function(k){ return film.querySelector('[data-k="' + k + '"]'); };
  var stage = $('stage'), seek = $('seek');
  film.addEventListener('pointerdown', function(){ active = api; });

  // ---------------------------------------------------------------- timeline elements
  function num(v){ return parseFloat(v); }
  var scenes = [].map.call(film.querySelectorAll('[data-s]'), function(el){
    var p = el.getAttribute('data-s').split(',');
    return {el:el, s:num(p[0]), e:num(p[1]), vis:-1, nb:el.classList.contains('nb'), on:null};
  });
  var anims = [].map.call(film.querySelectorAll('[data-a]'), function(el){
    var p = el.getAttribute('data-a').split(',');
    var a = {el:el, i:num(p[0]), d:num(p[1]), fx:p[2], o:p[3]!==undefined ? num(p[3]) : null, last:-1,
             svg: el instanceof SVGElement, li: el.classList.contains('it')};
    if(a.fx==='draw'||a.fx==='line'){ a.len = num(el.getAttribute('data-len')); el.style.strokeDasharray = a.len + ' ' + a.len; }
    if(a.fx==='pop'){ var c = (el.getAttribute('data-c')||'0,0').split(','); a.cx = num(c[0]); a.cy = num(c[1]); }
    if(a.fx==='reveal') a.R = num(el.getAttribute('data-rad'));
    if(a.li){ a.hl = (el.getAttribute('data-hl')||'').split(' ').filter(Boolean);
      el.addEventListener('click', function(){ go(a.i + .01); });
      el.addEventListener('keydown', function(ev){ if(ev.key==='Enter'){ go(a.i + .01); } });
    }
    return a;
  });
  var items = anims.filter(function(a){ return a.li; });
  var nums = film.querySelectorAll('.num');
  var chBtns = film.querySelectorAll('.ch');

  function clamp(x){ return x<0 ? 0 : x>1 ? 1 : x; }
  function ease(x){ return x<.5 ? 4*x*x*x : 1 - Math.pow(-2*x+2, 3)/2; }
  function back(x){ var c1 = 1.70158, c3 = c1 + 1; return 1 + c3*Math.pow(x-1,3) + c1*Math.pow(x-1,2); }

  // ---------------------------------------------------------------- render(t): everything is a function of t
  var T = 0, playing = false, speed = 1, lastHot = '', lastCh = -1, lastNow = null;
  function render(t){
    var i, a;
    for(i=0;i<scenes.length;i++){
      var sc = scenes[i];
      if(sc.nb){ var onb = t>=sc.s && (t<sc.e || sc.e>=TOTAL-0.06); if(onb!==sc.on){ sc.on = onb; sc.el.classList.toggle('on', onb); } continue; }
      var vin = sc.s<=0.01 ? (t>=0 ? 1 : 0) : clamp((t - sc.s)/0.45 + 1);
      var vout = sc.e>=TOTAL-0.06 ? 1 : clamp((sc.e - t)/0.45);
      var v = Math.min(vin, vout);
      if(t < sc.s - 0.45 || t > sc.e + 0.45) v = 0;
      if(Math.abs(v - sc.vis) > 0.001){
        sc.vis = v;
        sc.el.style.opacity = v; sc.el.style.display = v>0 ? '' : 'none';
      }
    }
    for(i=0;i<anims.length;i++){
      a = anims[i];
      var p = a.d>0 ? clamp((t - a.i)/a.d) : (t>=a.i ? 1 : 0);
      var op = 1;
      if(a.o!==null) op = 1 - clamp((t - a.o)/0.5);
      var key = Math.round(p*1000) + ':' + Math.round(op*100);
      if(key===a.last) continue;
      a.last = key;
      var el = a.el, shown = p>0 && op>0;
      if(a.fx==='draw'||a.fx==='line'){
        el.style.strokeDashoffset = (a.len * (1 - (a.fx==='line' ? p : ease(p)))).toFixed(2);
        el.style.opacity = shown ? op : 0;
      } else if(a.fx==='reveal'){
        el.setAttribute('r', (a.R * ease(p)).toFixed(1));
      } else if(a.fx==='pop'){
        var sc2 = p<=0 ? .01 : .35 + .65*back(p);
        el.style.opacity = shown ? Math.min(1, p*2)*op : 0;
        el.setAttribute('transform', 'translate(' + a.cx + ' ' + a.cy + ') scale(' + sc2.toFixed(3) + ') translate(' + (-a.cx) + ' ' + (-a.cy) + ')');
      } else if(a.fx==='rise'){
        el.style.opacity = shown ? p*op : 0;
        el.style.visibility = shown ? 'visible' : 'hidden';
        el.classList.toggle('shown', shown);
        el.style.transform = 'translateY(' + ((1-p)*8).toFixed(1) + 'px)';
      } else {
        el.style.opacity = shown ? p*op : 0;
        el.style.visibility = shown ? 'visible' : 'hidden';
      }
    }
    // the current narration line + highlighted map numbers
    var now = null;
    for(i=0;i<items.length;i++){ a = items[i]; if(a.i<=t && (!now || a.i>=now.i) && a.el.parentNode.parentNode.classList.contains('on')) now = a; }
    if(now!==lastNow){
      if(lastNow) lastNow.el.classList.remove('now');
      if(now){ now.el.classList.add('now'); var ne = now.el; requestAnimationFrame(function(){ keepVisible(ne); }); }
      lastNow = now;
    }
    var hot = now ? now.hl.join(' ') : '';
    if(hot!==lastHot){
      lastHot = hot;
      for(i=0;i<nums.length;i++){
        var id = nums[i].id, on = false;
        for(var h=0; now && h<now.hl.length; h++) if(id.indexOf(now.hl[h] + '-')===0) on = true;
        nums[i].classList.toggle('hot', on);
      }
    }
    // chapters
    var ci = 0; for(i=0;i<CH.length;i++) if(t>=CH[i].start) ci = i;
    for(i=0;i<chBtns.length;i++){
      var c = CH[i], cp = clamp((t - c.start)/(c.end - c.start));
      chBtns[i].style.setProperty('--cp', (cp*100).toFixed(1) + '%');
    }
    if(ci!==lastCh){
      if(lastCh>=0) chBtns[lastCh].classList.remove('on');
      chBtns[ci].classList.add('on'); lastCh = ci;
      if(window.innerWidth<=1180) chBtns[ci].scrollIntoView({block:'nearest', inline:'center', behavior:'smooth'});
      if(active===api){ try{ history.replaceState(null, '', '#' + CH[ci].id); }catch(e){} }
    }
    seek.value = Math.round(t/TOTAL*1000);
    seek.style.setProperty('--p', (t/TOTAL*100).toFixed(2) + '%');
    $('tcur').textContent = fmt(t);
    $('endbtns').classList.toggle('on', t >= TOTAL - 1.2);
    if(F.explore!=null){
      var ex = t >= F.explore - .01;
      if(ex!==film.classList.contains('exploring')){ film.classList.toggle('exploring', ex); if(!ex && picked) pick(null); }
    }
  }
  function keepVisible(el){
    var box = $('notes');
    if(window.innerWidth<=820) return;
    var r = el.getBoundingClientRect(), b = box.getBoundingClientRect();
    if(r.bottom > b.bottom - 8 || r.top < b.top) box.scrollTop += r.top - b.top - b.height/3;
  }
  function fmt(t){ t = Math.max(0, Math.floor(t)); return Math.floor(t/60) + ':' + ('0' + t%60).slice(-2); }

  // ---------------------------------------------------------------- clock
  var prev = 0;
  function frame(ts){
    if(!playing) return;
    var dt = prev ? (ts - prev)/1000 : 0; prev = ts;
    if(dt > .25) dt = .25;
    T = Math.min(TOTAL, T + dt*speed);
    render(T);
    if(T>=TOTAL){ pause(); return; }
    requestAnimationFrame(frame);
  }
  function play(){
    if(T>=TOTAL-0.05) T = 0;
    FILMS.forEach(function(f){ if(f!==api) f.pause(); });
    active = api; playing = true; prev = 0; film.classList.add('playing', 'started');
    requestAnimationFrame(frame);
  }
  function pause(){ playing = false; film.classList.remove('playing'); }
  function toggle(){ playing ? pause() : play(); }
  function go(t){ T = Math.max(0, Math.min(TOTAL, t)); film.classList.add('started'); render(T); }
  function chapterAt(t){ var ci = 0; for(var i=0;i<CH.length;i++) if(t>=CH[i].start - .01) ci = i; return ci; }
  function prevChapter(){ var ci = chapterAt(T); go(T - CH[ci].start > 2 || ci===0 ? CH[ci].start : CH[ci-1].start); }
  function nextChapter(){ var ci = chapterAt(T); if(ci < CH.length-1) go(CH[ci+1].start); }

  $('b-play').addEventListener('click', toggle);
  $('bigplay').addEventListener('click', function(e){ e.stopPropagation(); play(); });
  stage.addEventListener('click', function(e){
    if(e.target.closest('a,button')) return;
    if(film.classList.contains('exploring')){ var h = e.target.closest('.hit'); pick(h ? 'r' : null, h ? h.getAttribute('data-r') : null); return; }
    toggle();
  });
  // ---------------------------------------------------------------- explorer (last chapter of Part 1)
  var picked = '';
  function pick(kind, id){
    var key = kind ? kind + ':' + id : '';
    if(key===picked) key = '';
    picked = key;
    var i, on = film.querySelectorAll('.hlr.on,.exr.on,.exb.on,.exd.on');
    for(i=0;i<on.length;i++) on[i].classList.remove('on');
    film.classList.toggle('picked', !!key);
    if(!key) return;
    var attr = kind==='b' ? 'data-b' : 'data-r';
    var sel = film.querySelectorAll('.hlr[' + attr + '="' + id + '"],.ex' + kind + '[' + attr + '="' + id + '"],.exd[' + attr + '="' + id + '"]');
    for(i=0;i<sel.length;i++) sel[i].classList.add('on');
    if(kind==='r'){ var g = film.querySelector('.hlr[data-r="' + id + '"]'); if(g && g.parentNode.lastChild!==g) g.parentNode.appendChild(g); }
  }
  var exl = $('explore-list');
  if(exl){
    exl.addEventListener('click', function(e){
      var b = e.target.closest('.exr,.exb'); if(!b) return;
      if(T < F.explore) go(TOTAL);
      if(b.classList.contains('exb')) pick('b', b.getAttribute('data-b')); else pick('r', b.getAttribute('data-r'));
    });
    stage.addEventListener('mouseover', function(e){
      var h = e.target.closest && e.target.closest('.hit'); var old = film.querySelector('.hlr.hov');
      if(old && (!h || old.getAttribute('data-r')!==h.getAttribute('data-r'))) old.classList.remove('hov');
      if(h){ var g = film.querySelector('.hlr[data-r="' + h.getAttribute('data-r') + '"]'); if(g) g.classList.add('hov'); }
    });
  }
  $('b-back').addEventListener('click', function(){ go(T - 5); });
  $('b-fwd').addEventListener('click', function(){ go(T + 5); });
  $('b-prev').addEventListener('click', prevChapter);
  $('b-next').addEventListener('click', nextChapter);
  $('b-restart').addEventListener('click', function(){ go(0); });
  $('replay').addEventListener('click', function(e){ e.stopPropagation(); go(0); play(); });
  $('speed').addEventListener('change', function(){ speed = parseFloat(this.value); });
  seek.addEventListener('input', function(){ go(this.value/1000*TOTAL); });
  for(var b=0;b<chBtns.length;b++) chBtns[b].addEventListener('click', function(){
    go(CH[+this.getAttribute('data-i')].start); if(!playing) play();
  });
  $('b-full').addEventListener('click', fullscreen);
  function fullscreen(){
    var d = document;
    if(d.fullscreenElement || d.webkitFullscreenElement){ (d.exitFullscreen || d.webkitExitFullscreen).call(d); }
    else { var r = film.requestFullscreen || film.webkitRequestFullscreen; if(r) r.call(film); }
  }
  api.key = function(e){
    var k = e.key;
    if(k===' ' || k==='k'){ e.preventDefault(); toggle(); }
    else if(k==='ArrowLeft'){ e.preventDefault(); e.shiftKey ? prevChapter() : go(T - 5); }
    else if(k==='ArrowRight'){ e.preventDefault(); e.shiftKey ? nextChapter() : go(T + 5); }
    else if(k==='Home'){ e.preventDefault(); go(0); }
    else if(k==='f'){ fullscreen(); }
  };
  api.pause = pause;
  api.go = go;
  api.deep = function(h){
    for(var c=0;c<CH.length;c++) if(CH[c].id===h){ active = api; go(CH[c].start); film.scrollIntoView({block:'start'}); return true; }
    return false;
  };
  render(0);
  return api;
  }
})();
'''


if __name__ == '__main__':
    # default: the published page « Vins de France : les bases » (both films); --part 1 / --part 2 = old drafts
    build(int(sys.argv[sys.argv.index('--part') + 1]) if '--part' in sys.argv else 'basics')
