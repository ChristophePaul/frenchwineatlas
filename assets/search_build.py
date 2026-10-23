#!/usr/bin/env python3
"""Build assets/search_index.js — the data behind the site-wide search (assets/search.js).

    python3 assets/search_build.py

Rerun after adding, renaming or rebuilding pages (after nav_build.py: the page list and the menu
paths come from nav.js). Nothing is fetched: everything is read from the site's own files.

What is indexed (one « doc » per result):
  · aoc    — the 315 AOCs of the grape search page (+ every name on a regional map that is not one
             of them: Alsace grands crus, Burgundy villages…), with links to the regional map (opens
             the AOC), the cadastral plan, the decree (PDF) and the grape page
  · grape  — the grapes of the grape search page (synonyms searchable)
  · igp    — the IGPs of the IGP map (opens the IGP)
  · climat — Burgundy premier / grand cru climats (from the climats maps)
  · quote  — the literature quotes (opens the quote)
  · map / plan / page — every page of the menu; the text pages are cut into sections (h1–h3),
             in French and English (data-en), each linking to its #anchor
  · cdc    — the decrees of the AOC library (PDF)
The quizzes' questions are not indexed (answers would show up). Cadastral plans: title only.
"""
import html, json, pathlib, re, unicodedata
from html.parser import HTMLParser
from urllib.parse import unquote, quote
import posixpath

SITE = pathlib.Path(__file__).resolve().parent.parent
ASSETS = SITE / 'assets'
OUT = ASSETS / 'search_index.js'

GAMES = {'Infos/Literature/' + n for n in ('Jeux.html', 'Wine_Quiz.html', 'Taste_Quiz.html', 'Map_Game.html', 'Bon_Cep.html', 'IGP_Game.html')}
CEP = 'Infos/Vine_and_Vineyard/Cepages/Cepages_et_Appellations.html'
IGP_MAP = 'Vignobles de France — Carte des IGP.html'
QUOTES = 'Infos/Literature/Wine_Quotes.html'
VINTAGES = 'Infos/Vintages/Vintage_Chart.html'
DECREES = 'Infos/AOC_Decree/'
TEXT_MAX = 2400          # characters of text kept per section and language (the snippet + matching)


def fold(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()


def key(s):
    """Name key for matching AOC names across sources."""
    s = re.sub(r'\s*\(.*?\)', '', s)
    return re.sub(r'[^a-z0-9]+', ' ', fold(s).replace('œ', 'oe')).strip()


def clean(s):
    return re.sub(r'\s+', ' ', html.unescape(s)).strip()


def strip_tags(s):
    return clean(re.sub(r'<[^>]+>', ' ', s or ''))


def read(p):
    return (SITE / p).read_text(encoding='utf-8', errors='ignore')


def grab_json(t, marker):
    i = t.find(marker)
    if i < 0: return None
    i += len(marker)
    while t[i] in ' \t\n=': i += 1
    return json.JSONDecoder().raw_decode(t[i:])[0]


# ---------------------------------------------------------------- pages from the menu
nav = (ASSETS / 'nav.js').read_text(encoding='utf-8')
SITE_TREE = grab_json(nav, 'var SITE = ')
PAGES = {}      # path → (fr, en, crumb_fr, crumb_en)
for it in SITE_TREE['top']:
    PAGES[it[0]] = (it[1], it[2] if len(it) > 2 else it[1], '', '')


def walk(gs, pf, pe):
    for g in gs:
        f, e = pf + [g['fr']], pe + [g['en']]
        for it in g.get('items', []):
            PAGES[it[0]] = (it[1], it[2] if len(it) > 2 else it[1], ' › '.join(f), ' › '.join(e))
        walk(g.get('groups', []), f, e)


walk(SITE_TREE['groups'], [], [])

docs = []


def doc(kind, url, tf, te, cf='', ce='', xf='', xe='', **extra):
    d = {'k': kind, 'u': url, 't': tf}
    if te and te != tf: d['te'] = te
    if cf: d['c'] = cf
    if ce and ce != cf: d['ce'] = ce
    if xf: d['x'] = xf[:TEXT_MAX]
    if xe and xe != xf: d['xe'] = xe[:TEXT_MAX]
    d.update({k: v for k, v in extra.items() if v not in (None, '', []) and (v != {} or k == 'L')})
    docs.append(d)
    return d


# ---------------------------------------------------------------- text pages → sections
class Sections(HTMLParser):
    SKIP = {'script', 'style', 'svg', 'noscript', 'template', 'head', 'title', 'select', 'option', 'button'}
    HEAD = {'h1', 'h2', 'h3'}
    VOID = {'br', 'img', 'input', 'meta', 'link', 'hr', 'wbr', 'source', 'area', 'col', 'base', 'embed', 'param', 'track'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # (tag, id, fr_only, skip, is_head)
        self.secs = [{'id': '', 'hf': '', 'he': '', 'fr': [], 'en': []}]
        self.cur_id = ''
        self.hbuf = None         # heading being read: [fr parts, en parts]

    def flags(self):
        fr_only = any(s[2] for s in self.stack)
        skip = any(s[3] for s in self.stack)
        return fr_only, skip

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.VOID:
            if tag == 'br': self.data(' ')
            return
        _, skip = self.flags()
        is_skip = tag in self.SKIP or 'hidden' in a or 'fw-' in (a.get('class') or '')
        eid = a.get('id') or ''
        if eid and not skip and tag in ('section', 'article', 'h1', 'h2', 'h3', 'h4', 'details', 'figure') or (eid and tag == 'div' and not self.cur_id):
            self.cur_id = eid
        is_head = tag in self.HEAD and not skip
        if is_head:
            self.secs.append({'id': eid or self.cur_id, 'hf': '', 'he': '', 'fr': [], 'en': []})
            self.hbuf = [[], []]
        en = a.get('data-en')
        if en is not None and not skip and not is_skip:
            t = strip_tags(en)
            self.secs[-1]['en'].append(t)
            if self.hbuf is not None: self.hbuf[1].append(t)
        self.stack.append((tag, eid, en is not None, is_skip, is_head))

    def handle_endtag(self, tag):
        if tag in self.VOID: return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                popped = self.stack[i:]
                del self.stack[i:]
                if any(p[4] for p in popped) and self.hbuf is not None:
                    s = self.secs[-1]
                    s['hf'] = clean(' '.join(self.hbuf[0]))
                    s['he'] = clean(' '.join(self.hbuf[1])) or s['hf']
                    self.hbuf = None
                break

    def data(self, d):
        fr_only, skip = self.flags()
        if skip: return
        s = self.secs[-1]
        s['fr'].append(d)
        if not fr_only: s['en'].append(d)
        if self.hbuf is not None:
            self.hbuf[0].append(d)
            if not fr_only: self.hbuf[1].append(d)

    handle_data = data


def page_title(t, path):
    m = re.search(r'<title([^>]*)>(.*?)</title>', t, re.S)
    fr = clean(m.group(2)) if m else path
    en = re.search(r'data-en="([^"]*)"', m.group(1)) if m else None
    return fr, (clean(en.group(1)) if en else '')


def meta_desc(t):
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', t)
    return clean(m.group(1)) if m else ''


def text_page(path, info, kind='page'):
    t = read(path)
    p = Sections(); p.feed(t)
    fr, en, cf, ce = info
    desc = meta_desc(t)
    secs = []
    for s in p.secs:
        xf = clean(' '.join(s['fr'])); xe = clean(' '.join(s['en']))
        if s['hf'] and xf.startswith(s['hf']): xf = xf[len(s['hf']):].strip()
        if s['he'] and xe.startswith(s['he']): xe = xe[len(s['he']):].strip()
        if not s['hf'] and secs:                        # text before any heading: page intro
            pass
        if secs and (len(xf) < 60 and not s['hf'] or not s['hf'] and secs):
            secs[-1]['xf'] += ' ' + xf; secs[-1]['xe'] += ' ' + xe
            continue
        secs.append({'id': s['id'], 'hf': s['hf'], 'he': s['he'], 'xf': xf, 'xe': xe})
    # first block = the page itself
    first = secs.pop(0) if secs else {'xf': '', 'xe': ''}
    if secs and len(first['xf']) < 200 and not first.get('hf'):
        pass
    doc(kind, path, fr, en, cf, ce, (desc + ' ' + first['xf']).strip(), (first['xe']).strip())
    for s in secs:
        if not s['hf'] or len(s['xf']) < 20: continue
        crumb_f = (cf + ' › ' if cf else '') + fr
        crumb_e = (ce + ' › ' if ce else '') + en
        doc('sec', path + ('#' + s['id'] if s['id'] else ''), s['hf'], s['he'], crumb_f, crumb_e, s['xf'], s['xe'])


# ---------------------------------------------------------------- grapes & AOCs (grape search page)
cep = grab_json(read(CEP), 'var DATA = ')
GRAPE = {g['id']: g for g in cep['grapes']}
COLOUR = {'B': ('Blanc', 'White'), 'N': ('Noir', 'Black'), 'G': ('Gris', 'Grey'), 'Rs': ('Rosé', 'Pink'), 'R': ('Rosé', 'Pink'), 'Rg': ('Rouge', 'Red')}
for g in cep['grapes']:
    cfr, cen = COLOUR.get(g['c'], ('', ''))
    doc('grape', CEP + '#cepage=' + g['id'], g['n'], '',
        'Cépages', 'Grapes', g.get('fr', ''), g.get('en', ''),
        a=g.get('syn', ''), o=g.get('orig', ''), ha=g.get('ha'), col=g['c'])

# decrees (AOC library)
manifest = json.loads(read(DECREES + 'manifest.json'))
DECREE = {}
for m in manifest:
    k = key(m['appellation'])
    DECREE.setdefault(k, m)
    doc('cdc', DECREES + m['file'], 'Cahier des charges — ' + m['appellation'], 'Specification — ' + m['appellation'],
        'Bibliothèque des décrets › ' + m['region'] + (' › ' + m['sub'] if m.get('sub') else ''),
        'AOC decree library › ' + m['region'] + (' › ' + m['sub'] if m.get('sub') else ''),
        en=(DECREES + m['en']) if m.get('en') else '')

ROLE = {'P': 'p', 'C': 's', 'S': 's', 'A': 's', '': 'p'}
AOC = {}     # key → doc
for a in cep['aocs']:
    colours = []
    main, minor = [], []
    for w in a['w']:
        if w['l'] not in colours: colours.append(w['l'])
        for gid, role, pct, adapt in w['g']:
            lst = main if role in ('', 'P') else minor
            n = GRAPE[gid]['n'] if gid in GRAPE else gid
            if n not in main and n not in minor: lst.append(n)
    d = doc('aoc', CEP + '#aoc=' + a['id'], a['n'], '', a['r'], a['r'], ' · '.join(a.get('notes') or []), '',
            a=a.get('aka', ''), w=colours, g=main[:8], g2=minor[:8], r=a['r'],
            L={'cep': CEP + '#aoc=' + a['id']})
    AOC[key(a['n'])] = d
    for alias in (a.get('aka') or '').split(','):
        if alias.strip(): AOC.setdefault(key(alias), d)

# ---------------------------------------------------------------- regional maps: AOC lists + plan links
REGION_MAPS = [p for p, v in PAGES.items() if v[2].startswith('Cartes régionales')]
MAP_ONLY = 0
for path in REGION_MAPS:
    t = read(path)
    fr, en, cf, ce = PAGES[path]
    meta = grab_json(t, '"appelMeta":') or grab_json(t, '"appellations":') or {}
    plans = grab_json(t, 'FW_PLAN_LINKS=') or {}
    base = posixpath.dirname(path)
    names = list(meta)
    doc('map', path, 'Carte — ' + fr, 'Map — ' + en, cf, ce, meta_desc(t) + ' ' + ', '.join(names), ', '.join(names))
    for n in names:
        if n.startswith('__'): continue
        alts = [x.strip() for x in n.split(' ou ')]
        d = None
        for x in alts:
            d = AOC.get(key(x)) or AOC.get(key(re.sub(r'^Alsace Grand Cru ', '', x)))
            if d: break
        m = meta.get(n) if isinstance(meta.get(n), dict) else {}
        if not d:
            MAP_ONLY += 1
            # a dénomination / grand cru of a larger AOC: find the parent by dropping words from the end
            words = alts[0].split(); parent = None
            while len(words) > 1 and not parent:
                words = words[:-1]; parent = AOC.get(key(' '.join(words)))
            cols = {'W': 'Blanc', 'R': 'Rouge', 'RO': 'Rosé', 'RS': 'Rosé', 'S': 'Effervescent'}
            d = doc('aoc', path + '#aoc=' + quote(n), alts[0], '', fr, en, clean(m.get('year_note', '')) if m else '', '',
                    a=', '.join(alts[1:]), w=[cols.get(c, c) for c in (m.get('colors') or [])], r=fr,
                    par=parent['t'] if parent else '', L={'cep': parent['L']['cep']} if parent and 'cep' in parent['L'] else {})
            AOC[key(alts[0])] = d
            if parent and 'map' not in parent['L']:
                parent['L']['map'] = path + '#aoc=' + quote(n); parent['L']['mapn'] = [fr, en]
        L = d['L']
        if 'map' not in L:
            L['map'] = path + '#aoc=' + quote(n); L['mapn'] = [fr, en]
        if n in plans and 'plan' not in L:
            L['plan'] = posixpath.normpath(posixpath.join(base, unquote(plans[n])))

for k, d in AOC.items():
    m = DECREE.get(key(d['t']))
    if m and 'cdc' not in d['L']:
        d['L']['cdc'] = DECREES + m['file']
        if m.get('en'): d['L']['cdce'] = DECREES + m['en']
    if d['L'].get('plan') and not (SITE / d['L']['plan']).exists():
        print('missing plan', d['L']['plan']); del d['L']['plan']

# ---------------------------------------------------------------- IGPs
t = read(IGP_MAP)
igps = grab_json(t, 'const DATA=')
detail = grab_json(t, 'const DETAIL=') or {}
CAT = {'reg': ('IGP régionale', 'Regional IGP'), 'dep': ('IGP départementale', 'Departmental IGP'),
       'zone': ('IGP de zone', 'Local IGP'), 'spir': ('IG spiritueux', 'Spirit IG')}
for g in igps:
    de = detail.get(g['name'], {})
    c = CAT.get(g['cat'], ('IGP', 'IGP'))
    doc('igp', IGP_MAP + '#igp=' + quote(g['name']), g['name'], '', 'Carte des IGP › ' + c[0], 'IGP map › ' + c[1],
        ' · '.join(filter(None, [', '.join(de.get('colours', [])), ', '.join(de.get('styles', [])), ', '.join(de.get('denoms', []))])), '',
        a=', '.join(de.get('denoms', [])), w=de.get('colours'), n=g.get('n'))

# ---------------------------------------------------------------- Burgundy climats
TIER = {'premier_cru': ('Premier cru', 'Premier cru'), 'grand_cru': ('Grand cru', 'Grand cru'),
        'village_climat': ('Climat communal', 'Village climat')}
seen = set()
for path, v in PAGES.items():
    if 'Bourgogne climats/' not in path: continue
    t = read(path)
    for m in re.finditer(r'"properties":\{"tier":"([^"]+)","name":"([^"]+)"(.*?)\}', t):
        tier, name, rest = m.groups()
        if '"neighbour":true' in rest or tier not in TIER: continue
        if fold(name) in ('village', 'premier cru (generique)'): continue
        app = re.search(r'"app":"([^"]+)"', rest); app = app.group(1) if app else v[0]
        ha = re.search(r'"area_ha":([\d.]+)', rest)
        sk = (fold(name), fold(app), tier)
        if sk in seen: continue
        seen.add(sk)
        tf, te = TIER.get(tier, (tier.replace('_', ' '), tier.replace('_', ' ')))
        doc('climat', path, name, '', 'Climats de Bourgogne › ' + app, 'Burgundy climats › ' + app,
            tf + ' · ' + app + (f' · {float(ha.group(1)):.2f} ha' if ha else ''),
            te + ' · ' + app + (f' · {float(ha.group(1)):.2f} ha' if ha else ''), tier=tier)

# ---------------------------------------------------------------- quotes
qd = grab_json(read(QUOTES), 'var DATA = ')
for q in qd['q']:
    doc('quote', QUOTES + '#q=' + q['id'], q.get('fr') or q.get('en') or q.get('o', ''), q.get('en', ''),
        q.get('a', ''), q.get('ae', ''), ' · '.join(filter(None, [q.get('a'), q.get('l'), q.get('wf'), q.get('o')])),
        ' · '.join(filter(None, [q.get('ae'), q.get('le'), q.get('we'), q.get('o')])))

# ---------------------------------------------------------------- vintage chart rows
vd = grab_json(read(VINTAGES), 'var DATA = ')
for r in vd['rows']:
    doc('sec', VINTAGES, 'Millésimes — ' + r['fr'], 'Vintages — ' + r['en'], 'Comprendre le vin › Millésimes', 'Wine knowledge › Vintage chart',
        'Notes des millésimes ' + r['fr'] + ' depuis ' + str(r.get('from', '')), 'Vintage ratings ' + r['en'] + ' since ' + str(r.get('from', '')))

years = {}
for r in vd['rows']:
    for y, sc in (r.get('v') or {}).items():
        if sc is not None: years.setdefault(y, []).append((sc, r['fr'], r['en']))
for y, lst in years.items():
    lst.sort(key=lambda x: -x[0])
    best = [x for x in lst if x[0] >= 8] or lst[:3]
    doc('sec', VINTAGES + '#y=' + y + '&by=year', 'Millésime ' + y, 'Vintage ' + y, 'Comprendre le vin › Millésimes', 'Wine knowledge › Vintage chart',
        'Les meilleures régions en ' + y + ' : ' + ', '.join(f'{x[1]} {x[0]}/10' for x in best[:12]),
        'Best regions in ' + y + ': ' + ', '.join(f'{x[2]} {x[0]}/10' for x in best[:12]))

# ---------------------------------------------------------------- every menu page
for path, info in PAGES.items():
    if path in REGION_MAPS: continue
    if path.startswith('Plan Cadastraux/'):
        doc('plan', path, 'Plan cadastral — ' + info[0], 'Cadastral map — ' + info[1], info[2], info[3]); continue
    if 'Bourgogne climats/' in path:
        doc('map', path, info[0] + ' — climats', info[1] + ' — climats', info[2], info[3], meta_desc(read(path))); continue
    if path in GAMES or path.startswith('Vignobles de France') or path == 'index.html':
        t = read(path)
        doc('page', path, info[0], info[1], info[2], info[3], meta_desc(t)); continue
    text_page(path, info)

for d in docs:
    if d.get('L') == {}: del d['L']
out = {'v': 1, 'docs': docs}
js = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
OUT.write_text('/* GENERATED by search_build.py — do not edit. */\nwindow.FW_SEARCH_DATA=' + js + ';\n', encoding='utf-8')
import time
sj = ASSETS / 'search.js'
sj.write_text(re.sub(r"var INDEX_V = '[^']*'", "var INDEX_V = '" + time.strftime('%Y%m%d%H%M') + "'", sj.read_text(encoding='utf-8'), count=1), encoding='utf-8')
nj = ASSETS / 'nav.js'
nj.write_text(re.sub(r"/\*@SV@\*/'[^']*'", "/*@SV@*/'" + time.strftime('%Y%m%d%H%M') + "'", nj.read_text(encoding='utf-8')), encoding='utf-8')
from collections import Counter
print(Counter(d['k'] for d in docs), f'map-only AOCs {MAP_ONLY}', f'{len(js)//1024} KB → {OUT.relative_to(SITE)}')
