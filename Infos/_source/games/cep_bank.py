"""Question bank for game 4 « Le bon cep » / "Grape Expectations" (Infos/Literature/Bon_Cep.html).

Built only from the Cépages & appellations data (Vine_and_Vineyard/Cepages/_source/data/*.txt via parse.py),
so every answer can be checked on that page.

Question types (cat):
  aoc2g   which grape is allowed in <AOC wine>?            (may carry « all / none of the above »)
  g2aoc   in which AOC is <grape> allowed?                 (may carry « all / none of the above »)
  blend   which blend is allowed in <AOC wine>?
  odd     which grape is NOT allowed in <AOC wine>?
  solo    the only grape of <AOC wine>?
  b2aoc   which AOC allows this blend?
  adapt   adaptation varieties (level 3 only)

Safety rules:
  - a wrong grape is allowed in NO wine of the AOC, and shares no base name with an allowed grape
    (no Sauvignon Gris against Sauvignon, no Muscat rosé against Muscat blanc…);
  - a wrong AOC allows the grape (or the whole blend) in none of its wines.
A question: dict(id, lv, cat, q=(fr,en), o=[(fr,en)×4], a=index, fix=bool (last option stays last), x=(fr,en), href, lk)
"""
import random
import re
import sys
import unicodedata
from pathlib import Path

INFOS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(INFOS / 'Vine_and_Vineyard' / 'Cepages' / '_source'))
from parse import parse_all, display  # noqa: E402
from quiz_bank import FAMOUS, KNOWN, REGION_EN, slug  # noqa: E402

RNG = random.Random(2026)
CEP = '../Vine_and_Vineyard/Cepages/Cepages_et_Appellations.html'
LK_AOC = ('Fiche de l’appellation (Cépages & appellations)', 'Appellation card (Grapes & appellations)')
LK_GRP = ('Fiche du cépage (Cépages & appellations)', 'Grape card (Grapes & appellations)')

ALL = (('Toutes ces réponses', 'All of the above'))
NONE = (('Aucune de ces réponses', 'None of the above'))

NEIGH = {
    'Bordeaux': ['Sud-Ouest', 'Charentes', 'Val de Loire'], 'Sud-Ouest': ['Bordeaux', 'Languedoc', 'Charentes'],
    'Charentes': ['Bordeaux', 'Sud-Ouest', 'Val de Loire'], 'Val de Loire': ['Bordeaux', 'Bourgogne', 'Charentes'],
    'Bourgogne': ['Beaujolais', 'Champagne', 'Jura'], 'Beaujolais': ['Bourgogne', 'Vallée du Rhône', 'Savoie-Bugey'],
    'Champagne': ['Bourgogne', 'Alsace-Lorraine'], 'Alsace-Lorraine': ['Champagne', 'Jura'],
    'Jura': ['Savoie-Bugey', 'Bourgogne', 'Alsace-Lorraine'], 'Savoie-Bugey': ['Jura', 'Vallée du Rhône', 'Beaujolais'],
    'Vallée du Rhône': ['Provence', 'Languedoc', 'Beaujolais'], 'Provence': ['Vallée du Rhône', 'Corse', 'Languedoc'],
    'Corse': ['Provence', 'Roussillon'], 'Languedoc': ['Roussillon', 'Vallée du Rhône', 'Sud-Ouest'],
    'Roussillon': ['Languedoc', 'Provence'],
}

# well-known grapes (canonical key, colour code) — the only ones used at level 1
STAR = {('pinot noir', 'N'), ('gamay', 'N'), ('syrah', 'N'), ('merlot', 'N'), ('cabernet franc', 'N'),
        ('cabernet-sauvignon', 'N'), ('grenache', 'N'), ('cot', 'N'), ('tannat', 'N'), ('mourvèdre', 'N'),
        ('carignan', 'N'), ('cinsaut', 'N'), ('poulsard', 'N'), ('trousseau', 'N'), ('meunier', 'N'),
        ('chardonnay', 'B'), ('sauvignon', 'B'), ('chenin', 'B'), ('sémillon', 'B'), ('riesling', 'B'),
        ('viognier', 'B'), ('melon', 'B'), ('aligoté', 'B'), ('savagnin', 'B'), ('muscadelle', 'B'),
        ('marsanne', 'B'), ('roussanne', 'B'), ('gros manseng', 'B'), ('petit manseng', 'B'), ('gewurztraminer', 'Rs'),
        ('mauzac', 'B'), ('altesse', 'B'), ('jacquère', 'B'), ('vermentino', 'B'), ('piquepoul blanc', 'B'),
        ('muscat à petits grains', 'B'), ('sylvaner', 'B'), ('pinot gris', 'G'), ('pinot blanc', 'B'),
        ('clairette', 'B'), ('grenache blanc', 'B'), ('macabeu', 'B'), ('ugni blanc', 'B')}
COLOUR_W = {'blanc', 'blanche', 'noir', 'noire', 'gris', 'grise', 'rose', 'rosé', 'rouge'}

LABEL = {  # wine label → (fr suffix, en suffix); '=' prefix: the label is the whole title
    'Rouge': ('rouge', 'red'), 'Blanc': ('blanc', 'white'), 'Rouge, Rosé': ('rouge et rosé', 'red and rosé'),
    'Rosé': ('rosé', 'rosé'), 'Blanc liquoreux': ('liquoreux', 'sweet white'), 'Blanc moelleux': ('moelleux', 'medium-sweet white'),
    'Vin doux naturel': ('vin doux naturel', 'vin doux naturel'), 'Blanc effervescent': ('effervescent blanc', 'white sparkling'),
    'Blanc, Rosé effervescent': ('effervescent blanc et rosé', 'sparkling white and rosé'),
    'Vin de paille': ('vin de paille', 'vin de paille (straw wine)'), 'Vin jaune': ('vin jaune', 'vin jaune'),
    'Gris': ('gris', 'gris (pale rosé)'), 'Rosé effervescent': ('effervescent rosé', 'sparkling rosé'),
    'Vin de liqueur blanc': ('vin de liqueur blanc', 'white vin de liqueur'),
    'Blanc tranquille et mousseux': ('blanc tranquille et mousseux', 'still and sparkling white'),
    'Vin de liqueur rouge, rosé': ('vin de liqueur rouge et rosé', 'red and rosé vin de liqueur'),
    'Vendanges tardives, Sélection de grains nobles': ('Vendanges tardives et Sélection de grains nobles', 'Vendanges Tardives and Sélection de Grains Nobles'),
    'Blanc moelleux, liquoreux': ('moelleux et liquoreux', 'medium-sweet and sweet white'),
    'Méthode ancestrale': ('méthode ancestrale', 'méthode ancestrale'), 'VDN ambré, blanc': ('VDN ambré et blanc', 'amber and white VDN'),
    'Vendanges tardives': ('Vendanges tardives', 'Vendanges Tardives'), 'Blanc sec': ('blanc sec', 'dry white'),
    'Rouge, Clairet': ('rouge et clairet', 'red and clairet'), 'Rouge effervescent': ('effervescent rouge', 'sparkling red'),
    'Bourgogne Gamay': ('=Bourgogne Gamay', '=Bourgogne Gamay'), 'Blanc, Rouge, Rosé': ('blanc, rouge et rosé', 'white, red and rosé'),
    'Mousseux, pétillant blanc': ('mousseux et pétillant blanc', 'white sparkling and semi-sparkling'),
    'Mousseux, pétillant rosé (dont Cerdon)': ('mousseux et pétillant rosé (dont Cerdon)', 'rosé sparkling and semi-sparkling (incl. Cerdon)'),
    'Blanc tranquille': ('blanc tranquille', 'still white'), 'Blanc tranquille « Molette »': ('blanc tranquille « Molette »', 'still white “Molette”'),
    'Mousseux': ('mousseux', 'sparkling'), 'Mousseux, Crémant': ('mousseux et crémant', 'sparkling and crémant'),
    'Rouge (Hengst, Kirchberg de Barr, Vorbourg)': ('rouge (Hengst, Kirchberg de Barr, Vorbourg)', 'red (Hengst, Kirchberg de Barr, Vorbourg)'),
    'Zotzenberg': ('=Alsace Grand Cru Zotzenberg', '=Alsace Grand Cru Zotzenberg'),
    'Altenberg de Bergheim (assemblage)': ('=Alsace Grand Cru Altenberg de Bergheim (assemblage)', '=Alsace Grand Cru Altenberg de Bergheim (blend)'),
    'Kaefferkopf (assemblage)': ('=Alsace Grand Cru Kaefferkopf (assemblage)', '=Alsace Grand Cru Kaefferkopf (blend)'),
    'Blanc, Vin de liqueur': ('blanc et vin de liqueur', 'white and vin de liqueur'),
    'Vin doux naturel, Vin de liqueur (blanc)': ('VDN et vin de liqueur blancs', 'white VDN and vin de liqueur'),
    'Vin doux naturel, Vin de liqueur (rouge)': ('VDN et vin de liqueur rouges', 'red VDN and vin de liqueur'),
    'Gris de gris': ('gris de gris', 'gris de gris'), 'Anjou Gamay': ('=Anjou Gamay', '=Anjou Gamay'),
    'Mousseux blanc': ('mousseux blanc', 'white sparkling'), 'Mousseux rosé': ('mousseux rosé', 'rosé sparkling'),
    'Rosé demi-sec': ('rosé demi-sec', 'off-dry rosé'), 'Mousseux blanc, rosé': ('mousseux blanc et rosé', 'white and rosé sparkling'),
    'Touraine Gamay, Primeur': ('=Touraine Gamay et primeur', '=Touraine Gamay and primeur'),
    'Mousseux, pétillant': ('mousseux et pétillant', 'sparkling and semi-sparkling'), 'Rosé, Gris': ('rosé et gris', 'rosé and gris'),
    'Brut (2e fermentation en bouteille)': ('brut (2e fermentation en bouteille)', 'brut (bottle-fermented)'),
    'Blanc, Vin de paille': ('blanc et vin de paille', 'white and vin de paille'), 'Rouge, Blanc': ('rouge et blanc', 'red and white'),
    'VDN blanc': ('VDN blanc', 'white VDN'), 'VDN ambré, grenat, rosé, tuilé': ('VDN ambré, grenat, rosé et tuilé', 'amber, grenat, rosé and tuilé VDN'),
    'VDN rouge (rimage, traditionnel)': ('VDN rouge (rimage, traditionnel)', 'red VDN (rimage, traditionnel)'),
    'VDN rosé': ('VDN rosé', 'rosé VDN'), 'VDN grenat, tuilé': ('VDN grenat et tuilé', 'grenat and tuilé VDN'),
    'Rouge sec': ('rouge sec', 'dry red'), 'VDN grenat': ('VDN grenat', 'grenat VDN'),
    'VDN ambré, rosé, tuilé': ('VDN ambré, rosé et tuilé', 'amber, rosé and tuilé VDN'),
    'Rouge (Coteaux de la Vézère)': ('rouge (Coteaux de la Vézère)', 'red (Coteaux de la Vézère)'),
    'Blanc (Coteaux de la Vézère)': ('blanc (Coteaux de la Vézère)', 'white (Coteaux de la Vézère)'),
    'Vin de liqueur rosé': ('vin de liqueur rosé', 'rosé vin de liqueur'), 'Blanc, Mousseux': ('blanc et mousseux', 'white and sparkling'),
    'Rouge primeur': ('rouge primeur', 'red primeur'), 'Blanc sec, moelleux': ('blanc sec et moelleux', 'dry and medium-sweet white'),
    'Rosé (gris)': ('rosé (gris)', 'rosé (gris)'), 'VDN': ('VDN', 'VDN'),
}
SIMPLE = {'Rouge', 'Blanc', 'Rouge, Rosé', 'Rosé'}


def strip_acc(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


def base(key):
    return ' '.join(w for w in key.split(' ') if strip_acc(w) not in {strip_acc(c) for c in COLOUR_W}) or key


def fam(code):
    return 'N' if code in ('N', 'Rg') else 'B'


def wine_fam(label):
    lo = label.lower()
    red = any(w in lo for w in ('rouge', 'grenat', 'gamay'))
    white = any(w in lo for w in ('blanc', 'ambré', 'jaune', 'paille', 'liquoreux', 'moelleux'))
    return 'N' if red and not white else 'B' if white and not red else None


# =================================================================================== data
AOCS = parse_all()
BY = {a['name']: a for a in AOCS}
G = {}          # grape id → dict(name, key, code, aocs:set, regions:Counter-like dict)
for a in AOCS:
    for w in a['wines']:
        w['ids'] = {g['id'] for g in w['grapes']}
        w['fam'] = wine_fam(w['label'])
        fr, en = LABEL[w['label']]
        if a['name'].startswith(('Crémant', 'Champagne', 'Blanquette')) and 'effervescent' in fr:
            fr, en = fr.replace('effervescent ', ''), en.replace(' sparkling', '').replace('sparkling ', '')
        w['t'] = (fr[1:], en[1:]) if fr.startswith('=') else (f"{a['name']} {fr}", f"{a['name']} {en}")
        for g in w['grapes']:
            d = G.setdefault(g['id'], dict(id=g['id'], key=g['key'], code=g['code'], aocs=set(), reg={},
                                           name=display(g['key'], g['code'])))
            d['aocs'].add(a['name'])
            d['reg'][a['region']] = d['reg'].get(a['region'], 0) + 1
    a['ids'] = set().union(*[w['ids'] for w in a['wines']]) if a['wines'] else set()
    a['bases'] = {base(G[i]['key']) for i in a['ids']}
    a['adapt'] = {g['id'] for w in a['wines'] for g in w['grapes'] if g['adapt']}
for d in G.values():
    d['star'] = (d['key'], d['code']) in STAR
    d['adapt_only'] = False
missing = {k for k in STAR if not any((d['key'], d['code']) == k for d in G.values())}
assert not missing, missing
for d in G.values():
    if d['key'] == 'cot':
        d['name'] = 'Cot (Malbec) Noir'
ADAPT_IDS = {i for a in AOCS for i in a['adapt']}
# a grape that is ONLY ever listed as an adaptation variety never appears before level 3
for i in ADAPT_IDS:
    G[i]['adapt_only'] = not any(g['id'] == i and not g['adapt'] for a in AOCS for w in a['wines'] for g in w['grapes'])


def tier(name):
    return 1 if name in FAMOUS else 2 if name in KNOWN else 3


def R(r, lang):
    return r if lang == 0 else REGION_EN.get(r, r)


def home(gid, lang):
    reg = sorted(G[gid]['reg'].items(), key=lambda kv: -kv[1])[:2]
    return ', '.join(R(r, lang) for r, _ in reg)


def nm(gid):
    return G[gid]['name']


def same(x):
    return (x, x)


def cep_aoc(name):
    return CEP + '#aoc=' + slug(name)


def cep_grape(gid):
    return CEP + '#cepage=' + gid


def ok_wrong(a, gid):
    """gid may be offered as a WRONG grape for AOC a."""
    return gid not in a['ids'] and base(G[gid]['key']) not in a['bases']


def lvl_grapes(w, lv):
    """grapes of wine w that may be the RIGHT answer at level lv."""
    out = []
    for g in w['grapes']:
        d = G[g['id']]
        if lv == 1 and not (d['star'] and g['role'] in ('', 'P') and not g['adapt']):
            continue
        if lv == 2 and (g['adapt'] or d['adapt_only']):
            continue
        if lv < 3 and w['fam'] and fam(g['code']) != w['fam']:
            continue  # level 1-2: no white grape in a red wine (Côte-Rôtie viognier is a level-3 trap)
        out.append(g['id'])
    return out


def wrong_pool(a, lv, f):
    """WRONG grape candidates of colour family f for AOC a, by level: far away → neighbours → same region."""
    r = a['region']
    near = set(NEIGH.get(r, []))
    cand = [i for i, d in G.items() if fam(d['code']) == f and ok_wrong(a, i) and not (lv < 3 and d['adapt_only'])]
    if lv == 1:
        p = [i for i in cand if G[i]['star'] and not (set(G[i]['reg']) & (near | {r}))]
    elif lv == 2:
        p = [i for i in cand if len(G[i]['aocs']) >= 2 and r not in G[i]['reg'] and set(G[i]['reg']) & near]
        if len(p) < 6:
            p += [i for i in cand if len(G[i]['aocs']) >= 3 and r not in G[i]['reg'] and i not in p]
    else:
        p = [i for i in cand if r in G[i]['reg']]
        if len(p) < 6:
            p += [i for i in cand if set(G[i]['reg']) & near and i not in p]
    return sorted(p)


def pick(pool, n):
    pool = sorted(set(pool))
    return RNG.sample(pool, n) if len(pool) >= n else None


ROLE = {'P': ('principaux', 'principal'), '': (None, None), 'C': ('complémentaires', 'complementary'),
        'S': ('secondaires', 'secondary'), 'A': ('accessoires', 'accessory')}


SUMS = []       # shared grape-list strings, referenced as §n§ in explanations (the page bolds the options' grapes)
SUMI = {}


def summary(w, lang, hi=()):
    """placeholder for the grape list of wine w (in language lang)."""
    k = (id(w), lang)
    if k not in SUMI:
        SUMI[k] = len(SUMS)
        SUMS.append(summary_text(w, lang))
    return f'§{SUMI[k]}§'


def summary_text(w, lang, hi=()):
    """grape list of a wine, grouped by role; ids in hi are bolded."""
    groups = {}
    for g in w['grapes']:
        k = 'adapt' if g['adapt'] else g['role']
        groups.setdefault(k, []).append(g['id'])
    parts = []
    for k in ('', 'P', 'C', 'S', 'A', 'adapt'):
        if k not in groups:
            continue
        ids = groups[k]
        names = [('<b>' + nm(i) + '</b>') if i in hi else nm(i) for i in ids[:20]]
        if len(ids) > 20:
            names.append(('+ %d autres' if lang == 0 else '+ %d more') % (len(ids) - 20))
        lab = ('variétés d’adaptation', 'adaptation varieties')[lang] if k == 'adapt' else ROLE[k][lang]
        parts.append(', '.join(names) + (f' ({lab})' if lab else ''))
    return ' ; '.join(parts) if lang == 0 else '; '.join(parts)


def where(gid, lang):
    return (f'{nm(gid)} ({home(gid, lang)})')


Q = []
SEEN = set()


def add(id_, lv, cat, q, items, ans, fix, x, href, lk, m=(None, None, None)):
    assert len(items) == 4 and len({t[0] for t in items}) == 4, (id_, items)
    if id_ in SEEN:
        return
    SEEN.add(id_)
    Q.append(dict(id=id_, lv=lv, cat=cat, q=q, o=items, a=ans, fix=fix, x=x, href=href, lk=lk, m=m))


def special_mode():
    """None, ('all'|'none', special_is_right)"""
    if RNG.random() >= 0.45:
        return None
    return (RNG.choice(['all', 'none']), RNG.random() < 0.5)


# =================================================================================== 1) aoc2g
def gen_aoc2g():
    for a in AOCS:
        for wi, w in enumerate(a['wines']):
            for lv in (1, 2, 3):
                if tier(a['name']) > lv or (lv == 1 and w['label'] not in SIMPLE):
                    continue
                rights = lvl_grapes(w, lv)
                if lv == 3:  # level 3 likes the rare ones: accessories and adaptation varieties first
                    rare = [i for i in rights if i in a['adapt'] or any(g['id'] == i and g['role'] in ('A', 'C', 'S') for g in w['grapes'])]
                    rights = rare or rights
                for k in range(2 if lv < 3 else 1):
                    if not rights:
                        break
                    r1 = RNG.choice(rights)
                    f = fam(G[r1]['code'])
                    pool = wrong_pool(a, lv, f)
                    sm = special_mode()
                    t = w['t']
                    q = (f'Quel cépage est autorisé en AOC <b>{t[0]}</b> ?', f'Which grape is allowed in <b>{t[1]}</b>?')
                    idb = f'aoc2g-{lv}-{slug(a["name"])}-{wi}-{k}'
                    if sm is None:
                        d = pick(pool, 3)
                        if not d:
                            continue
                        items = [same(nm(r1))] + [same(nm(i)) for i in d]
                        x = tuple((f'Oui : le cépage {nm(r1)} y est autorisé. Les autres sont absents de l’appellation : '
                                   + ', '.join(where(i, 0) for i in d) + '. Encépagement : ' + summary(w, 0, {r1}) + '.') if L == 0 else
                                  (f'Yes: {nm(r1)} is allowed. The others are not allowed anywhere in the appellation: '
                                   + ', '.join(where(i, 1) for i in d) + '. Grapes: ' + summary(w, 1, {r1}) + '.') for L in (0, 1))
                        add(idb, lv, 'aoc2g', q, items, 0, False, x, cep_aoc(a['name']), LK_AOC, (a['name'], wi, None))
                        continue
                    kind, sp_right = sm
                    sp = ALL if kind == 'all' else NONE
                    if kind == 'all' and sp_right:
                        three = [i for i in rights if fam(G[i]['code']) == f]
                        if len(three) < 3:
                            continue
                        three = RNG.sample(three, 3)
                        items = [same(nm(i)) for i in three] + [sp]
                        x = tuple(('Les trois sont autorisés : ' if L == 0 else 'All three are allowed: ') + ', '.join(nm(i) for i in three)
                                  + ('. Encépagement : ' if L == 0 else '. Grapes: ') + summary(w, L, set(three)) + '.' for L in (0, 1))
                        add(idb, lv, 'aoc2g', q, items, 3, True, x, cep_aoc(a['name']), LK_AOC, (a['name'], wi, None))
                    elif kind == 'none' and sp_right:
                        d = pick(pool, 3)
                        if not d:
                            continue
                        items = [same(nm(i)) for i in d] + [sp]
                        x = tuple((('Aucun des trois n’est autorisé : ' if L == 0 else 'None of the three is allowed: ')
                                   + ', '.join(where(i, L) for i in d) + ('. Encépagement : ' if L == 0 else '. Grapes: ')
                                   + summary(w, L) + '.') for L in (0, 1))
                        add(idb, lv, 'aoc2g', q, items, 3, True, x, cep_aoc(a['name']), LK_AOC, (a['name'], wi, None))
                    else:  # special offered but wrong → exactly one right grape
                        d = pick(pool, 2)
                        if not d:
                            continue
                        items = [same(nm(r1))] + [same(nm(i)) for i in d] + [sp]
                        x = tuple(((f'Seul le cépage {nm(r1)} est autorisé ; pas ' + ' ni '.join(where(i, 0) for i in d)) if L == 0 else
                                   (f'Only {nm(r1)} is allowed; not ' + ' or '.join(where(i, 1) for i in d)))
                                  + ('. Encépagement : ' if L == 0 else '. Grapes: ') + summary(w, L, {r1}) + '.' for L in (0, 1))
                        add(idb, lv, 'aoc2g', q, items, 0, True, x, cep_aoc(a['name']), LK_AOC, (a['name'], wi, None))


# =================================================================================== 2) g2aoc
def aoc_has(name, gid):
    return gid in BY[name]['ids']


def wrong_aocs(gid, right, lv):
    rr = BY[right]['region']
    near = set(NEIGH.get(rr, []))
    cand = [a['name'] for a in AOCS if not aoc_has(a['name'], gid) and a['wines']
            and not a['name'].startswith(right.split(' ')[0]) and not right.startswith(a['name'].split(' ')[0])]
    if lv == 1:
        p = [n for n in cand if n in FAMOUS and BY[n]['region'] not in G[gid]['reg']]
    elif lv == 2:
        p = [n for n in cand if tier(n) <= 2 and (BY[n]['region'] in near or BY[n]['region'] == rr)]
        if len(p) < 6:
            p += [n for n in cand if tier(n) <= 2 and n not in p]
    else:
        p = [n for n in cand if BY[n]['region'] == rr]
        if len(p) < 6:
            p += [n for n in cand if BY[n]['region'] in near and n not in p]
    return p


def wine_of(name, gid):
    return [w['t'] for w in BY[name]['wines'] if gid in w['ids']]


def gen_g2aoc():
    for gid, d in sorted(G.items()):
        for lv in (1, 2, 3):
            if lv == 1 and not d['star']:
                continue
            if lv < 3 and d['adapt_only']:
                continue
            if lv == 2 and len(d['aocs']) < 2:
                continue
            # right AOCs: where the grape counts at this level
            rights = sorted(n for n in d['aocs'] if tier(n) <= lv and any(gid in lvl_grapes(w, lv) for w in BY[n]['wines']))
            if lv == 3:
                rights = sorted(n for n in d['aocs'] if any(gid in lvl_grapes(w, 3) for w in BY[n]['wines']))
            nvar = 3 if lv == 1 else 2
            for k in range(min(nvar, len(rights))):
                r1 = RNG.choice(rights)
                pool = wrong_aocs(gid, r1, lv)
                sm = special_mode()
                q = (f'Dans quelle appellation le cépage <b>{nm(gid)}</b> est-il autorisé ?', f'In which appellation is <b>{nm(gid)}</b> allowed?')
                idb = f'g2aoc-{lv}-{gid}-{k}'
                href = cep_grape(gid)

                def wi(n, L):
                    return ', '.join(t[L] for t in wine_of(n, gid))

                def no(ns, L):
                    return ', '.join(f'{n} ({R(BY[n]["region"], L)})' for n in ns)
                if sm is None:
                    dd = pick(pool, 3)
                    if not dd:
                        continue
                    x = (f'Le cépage {nm(gid)} est autorisé en AOC {r1} ({wi(r1, 0)}). Il ne l’est ni en ' + no(dd, 0).replace(', ', ', ni en ') + '.',
                         f'{nm(gid)} is allowed in {r1} ({wi(r1, 1)}). It is not allowed in ' + ', '.join(f'{n} ({R(BY[n]["region"], 1)})' for n in dd[:-1]) + f' or {dd[-1]} ({R(BY[dd[-1]]["region"], 1)}).')
                    add(idb, lv, 'g2aoc', q, [same(r1)] + [same(n) for n in dd], 0, False, x, href, LK_GRP, (None, None, gid))
                    continue
                kind, sp_right = sm
                sp = ALL if kind == 'all' else NONE
                if kind == 'all' and sp_right:
                    if len(rights) < 3:
                        continue
                    three = RNG.sample(rights, 3)
                    if len({n.split(' ')[0] for n in three}) < 3:
                        continue
                    x = (f'Le cépage {nm(gid)} est autorisé dans les trois : ' + ' ; '.join(f'{n} ({wi(n, 0)})' for n in three) + '.',
                         f'{nm(gid)} is allowed in all three: ' + '; '.join(f'{n} ({wi(n, 1)})' for n in three) + '.')
                    add(idb, lv, 'g2aoc', q, [same(n) for n in three] + [sp], 3, True, x, href, LK_GRP, (None, None, gid))
                elif kind == 'none' and sp_right:
                    dd = pick(pool, 3)
                    if not dd:
                        continue
                    x = (f'Le cépage {nm(gid)} n’est autorisé dans aucune des trois : ' + no(dd, 0) + f'. On le trouve par exemple en AOC {r1}.',
                         f'{nm(gid)} is allowed in none of the three: ' + no(dd, 1) + f'. You will find it in {r1}, for instance.')
                    add(idb, lv, 'g2aoc', q, [same(n) for n in dd] + [sp], 3, True, x, href, LK_GRP, (None, None, gid))
                else:
                    dd = pick(pool, 2)
                    if not dd:
                        continue
                    x = (f'Seule l’AOC {r1} autorise le cépage {nm(gid)} ({wi(r1, 0)}) ; pas ' + no(dd, 0).replace(', ', ' ni ') + '.',
                         f'Only {r1} allows {nm(gid)} ({wi(r1, 1)}); not ' + no(dd, 1).replace(', ', ' or ') + '.')
                    add(idb, lv, 'g2aoc', q, [same(r1)] + [same(n) for n in dd] + [sp], 0, True, x, href, LK_GRP, (None, None, gid))


# =================================================================================== 3) blend / 4) odd one out
def plus(ids):
    return ' + '.join(nm(i) for i in ids)


def gen_blend_odd():
    for a in AOCS:
        for wi, w in enumerate(a['wines']):
            for lv in (1, 2, 3):
                if tier(a['name']) > lv or (lv == 1 and w['label'] not in SIMPLE):
                    continue
                rights = lvl_grapes(w, lv)
                if w['fam'] is None or len(rights) < 3:
                    continue
                f = w['fam']
                rights = [i for i in rights if fam(G[i]['code']) == f]
                pool = wrong_pool(a, lv, f)
                if len(rights) < 3 or len(pool) < 3:
                    continue
                t = w['t']
                # blend: right combo of n grapes; each wrong combo swaps ONE grape for an intruder
                n = 2 if lv == 1 else 3
                combo = sorted(RNG.sample(rights, n), key=nm)
                intr = RNG.sample(pool, 3)
                wrongs = []
                for j, bad in enumerate(intr):
                    c = list(combo)
                    c[j % n] = bad
                    wrongs.append(sorted(c, key=nm))
                items = [same(plus(combo))] + [same(plus(c)) for c in wrongs]
                if len({i[0] for i in items}) == 4:
                    x = tuple(((f'{plus(combo)} : tous autorisés. Les intrus : ' if L == 0 else f'{plus(combo)}: all allowed. The intruders: ')
                               + ', '.join(where(i, L) for i in intr) + ('. Encépagement : ' if L == 0 else '. Grapes: ')
                               + summary(w, L, set(combo)) + '.') for L in (0, 1))
                    add(f'blend-{lv}-{slug(a["name"])}-{wi}', lv, 'blend',
                        (f'Quel assemblage est autorisé en AOC <b>{t[0]}</b> ?', f'Which blend is allowed in <b>{t[1]}</b>?'),
                        items, 0, False, x, cep_aoc(a['name']), LK_AOC, (a['name'], wi, None))
                # odd one out
                three = RNG.sample(rights, 3)
                bad = RNG.choice(pool)
                x = (f'Le cépage {where(bad, 0)} n’est pas autorisé. Encépagement : ' + summary(w, 0, set(three)) + '.',
                     f'{where(bad, 1)} is not allowed. Grapes: ' + summary(w, 1, set(three)) + '.')
                add(f'odd-{lv}-{slug(a["name"])}-{wi}', lv, 'odd',
                    (f'Quel cépage est l’intrus, <u>non autorisé</u> en AOC <b>{t[0]}</b> ?', f'Which grape is the odd one out, <u>not allowed</u> in <b>{t[1]}</b>?'),
                    [same(nm(bad))] + [same(nm(i)) for i in three], 0, False, x, cep_aoc(a['name']), LK_AOC, (a['name'], wi, None))


# =================================================================================== 5) solo
def gen_solo():
    for a in AOCS:
        for wi, w in enumerate(a['wines']):
            if len(w['grapes']) != 1:
                continue
            gid = w['grapes'][0]['id']
            for lv in (1, 2, 3):
                if tier(a['name']) > lv or (lv == 1 and not G[gid]['star']):
                    continue
                pool = wrong_pool(a, lv, fam(G[gid]['code']))
                d = pick(pool, 3)
                if not d:
                    continue
                t = w['t']
                add(f'solo-{lv}-{slug(a["name"])}-{wi}', lv, 'solo',
                    (f'En AOC <b>{t[0]}</b>, un seul cépage est autorisé. Lequel ?', f'<b>{t[1]}</b> may use one grape only. Which one?'),
                    [same(nm(gid))] + [same(nm(i)) for i in d], 0, False,
                    (f'Le cahier des charges de l’AOC {t[0]} n’autorise que le cépage {nm(gid)}. Les autres : ' + ', '.join(where(i, 0) for i in d) + '.',
                     f'The {t[1]} rulebook allows {nm(gid)} only. The others: ' + ', '.join(where(i, 1) for i in d) + '.'),
                    cep_aoc(a['name']), LK_AOC, (a['name'], wi, None))


# =================================================================================== 6) b2aoc
def allows_all(name, ids):
    return any(set(ids) <= w['ids'] for w in BY[name]['wines'])


def gen_b2aoc():
    for a in AOCS:
        for wi, w in enumerate(a['wines']):
            for lv in (2, 3):
                if tier(a['name']) > lv:
                    continue
                rights = lvl_grapes(w, lv)
                if w['fam']:
                    rights = [i for i in rights if fam(G[i]['code']) == w['fam']]
                if len(rights) < 3:
                    continue
                combo = sorted(RNG.sample(rights, 3), key=nm)
                r, near = a['region'], set(NEIGH.get(a['region'], []))
                cand = [b['name'] for b in AOCS if b['wines'] and not allows_all(b['name'], combo) and b['name'] != a['name']
                        and not b['name'].startswith(a['name'].split(' ')[0]) and not a['name'].startswith(b['name'].split(' ')[0])]
                share = {n: len(set(combo) & BY[n]['ids']) for n in cand}
                if lv == 2:
                    p = [n for n in cand if tier(n) <= 2 and share[n] >= 1 and (BY[n]['region'] in near or BY[n]['region'] == r)]
                else:
                    p = [n for n in cand if share[n] >= 2 and BY[n]['region'] == r]
                    if len(p) < 3:
                        p += [n for n in cand if share[n] >= 2 and BY[n]['region'] in near and n not in p]
                d = pick(p, 3)
                if not d:
                    continue

                def miss(n, L):
                    m = [nm(i) for i in combo if i not in BY[n]['ids']]
                    if not m:  # all three exist, but never in the same wine
                        return f'{n} : jamais les trois dans le même vin' if L == 0 else f'{n}: never all three in the same wine'
                    return f'{n} : ' + ('sans ' if L == 0 else 'no ') + ', '.join(m) if L == 0 else f'{n}: no ' + ', '.join(m)
                add(f'b2aoc-{lv}-{slug(a["name"])}-{wi}', lv, 'b2aoc',
                    (f'Quelle appellation autorise, dans un même vin, l’assemblage <b>{plus(combo)}</b> ?',
                     f'Which appellation allows the blend <b>{plus(combo)}</b> in one and the same wine?'),
                    [same(a['name'])] + [same(n) for n in d], 0, False,
                    (f'L’AOC {w["t"][0]} autorise les trois. ' + ' ; '.join(miss(n, 0) for n in d) + '.',
                     f'{w["t"][1]} allows all three. ' + '; '.join(miss(n, 1) for n in d) + '.'),
                    cep_aoc(a['name']), LK_AOC, (a['name'], wi, None))


# =================================================================================== 7) adaptation (level 3)
def gen_adapt():
    adapt_names = sorted(ADAPT_IDS)
    for a in AOCS:
        if not a['adapt']:
            continue
        for wi, w in enumerate(a['wines']):
            ad = [g['id'] for g in w['grapes'] if g['adapt']]
            if not ad:
                continue
            t = w['t']
            for k, gid in enumerate(ad):
                f = fam(G[gid]['code'])
                pool = [i for i in adapt_names if fam(G[i]['code']) == f and ok_wrong(a, i)]
                if len(pool) < 3:
                    pool += [i for i in wrong_pool(a, 3, f) if i not in pool]
                d = pick(pool, 3)
                if not d:
                    continue
                x = (f'Le cépage {nm(gid)} fait partie des « variétés d’intérêt à fins d’adaptation » (VIFA) admises en AOC {t[0]} pour faire face au changement climatique, '
                     'limitées à 5 % de l’encépagement et 10 % de l’assemblage. Les autres n’y sont pas autorisés : '
                     + ', '.join(where(i, 0) for i in d) + '.',
                     f'{nm(gid)} is one of the “varieties of interest for adaptation” (VIFA) admitted in {t[1]} to cope with climate change, '
                     'capped at 5% of the vineyard and 10% of the blend. The others are not allowed there: '
                     + ', '.join(where(i, 1) for i in d) + '.')
                add(f'adapt-{slug(a["name"])}-{wi}-{gid}', 3, 'adapt',
                    (f'Pour s’adapter au changement climatique, quel cépage a été admis comme <i>variété d’adaptation</i> en AOC <b>{t[0]}</b> ?',
                     f'To adapt to climate change, which grape has been admitted as an <i>adaptation variety</i> in <b>{t[1]}</b>?'),
                    [same(nm(gid))] + [same(nm(i)) for i in d], 0, False, x, cep_aoc(a['name']), LK_AOC, (a['name'], wi, None))
    # where was <adaptation grape> admitted?
    for gid in adapt_names:
        homes = sorted(n for n in AOCS_WITH_ADAPT(gid))
        for k in range(min(2, len(homes))):
            r1 = homes[k]
            rr = BY[r1]['region']
            cand = [b['name'] for b in AOCS if not aoc_has(b['name'], gid) and b['wines'] and (b['region'] == rr or b['adapt'])]
            d = pick(cand, 3)
            if not d:
                continue
            add(f'adapt-where-{gid}-{k}', 3, 'adapt',
                (f'Le cépage <b>{nm(gid)}</b> a été admis comme variété d’adaptation au changement climatique dans… ?',
                 f'<b>{nm(gid)}</b> has been admitted as a climate-change adaptation variety in…?'),
                [same(r1)] + [same(n) for n in d], 0, False,
                (f'Le cépage {nm(gid)} est une variété d’adaptation en AOC {r1}. Il n’est autorisé ni en ' + ', ni en '.join(d) + '.',
                 f'{nm(gid)} is an adaptation variety in {r1}. It is not allowed in ' + ', '.join(d) + '.'),
                cep_grape(gid), LK_GRP, (None, None, gid))


def AOCS_WITH_ADAPT(gid):
    return [a['name'] for a in AOCS if gid in a['adapt']]


# =================================================================================== checks
def verify(q):
    """re-check every right/wrong claim against the data (options are matched back to ids / AOC names)."""
    byname = {d['name']: i for i, d in G.items()}
    assert len(byname) == len(G)
    o = [t[0] for t in q['o']]
    sp = q['fix'] and o[3] in (ALL[0], NONE[0])
    items = o[:3] if sp else o
    a_right = None if (sp and q['a'] == 3) else q['a']
    cat, (aoc, wi, gid) = q['cat'], q['m']
    if cat in ('aoc2g', 'solo', 'odd', 'adapt') and aoc:
        A, w = BY[aoc], BY[aoc]['wines'][wi]
        ids = [byname[t] for t in items]
        for k, i in enumerate(ids):
            right = (k == a_right) or (sp and q['a'] == 3 and o[3] == ALL[0])
            if cat == 'odd':
                right = not right
            if right:
                assert i in w['ids'] and (cat != 'adapt' or i in A['adapt']), (q['id'], o[k])
            else:
                assert ok_wrong(A, i), (q['id'], o[k])
    elif cat == 'blend':
        A, w = BY[aoc], BY[aoc]['wines'][wi]
        for k, t in enumerate(items):
            ids = [byname[x] for x in t.split(' + ')]
            if k == a_right:
                assert set(ids) <= w['ids'], q['id']
            else:
                assert any(ok_wrong(A, i) for i in ids), q['id']
    elif cat in ('g2aoc', 'adapt'):
        for k, n in enumerate(items):
            right = (k == a_right) or (sp and q['a'] == 3 and o[3] == ALL[0])
            assert aoc_has(n, gid) == right, (q['id'], n)
            if cat == 'adapt' and right:
                assert gid in BY[n]['adapt']
    elif cat == 'b2aoc':
        combo = [byname[x] for x in re.sub('<[^>]+>', '', q['q'][1]).split('blend ')[1].split(' in one')[0].split(' + ')]
        for k, n in enumerate(items):
            assert allows_all(n, combo) == (k == a_right), (q['id'], n)


def bank():
    if not Q:
        gen_aoc2g()
        gen_g2aoc()
        gen_blend_odd()
        gen_solo()
        gen_b2aoc()
        gen_adapt()
        for q in Q:
            verify(q)
    return Q


if __name__ == '__main__':
    from collections import Counter
    b = bank()
    print(len(b), 'questions')
    print(Counter((q['lv'], q['cat']) for q in b))
    print(Counter(q['lv'] for q in b))
    print('special:', Counter((q['lv'], q['o'][3][1]) for q in b if q['fix']))
    for q in RNG.sample(b, 6):
        print('---', q['id'], q['q'][1], [o[1] for o in q['o']], 'ANS', q['a'])
        print('   ', q['x'][1])
