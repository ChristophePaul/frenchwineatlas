"""Question bank for the wine quiz (Infos/Literature/Wine_Quiz.html).

Every question is built from data that is already published on the site, so each answer can be found there:
  - Cépages & appellations page  (Vine_and_Vineyard/Cepages/_source/data/*.txt via parse.py)
  - Crus classifications page    (_source/classifications/data.py + premiers_crus.json)
  - Vine glossary                (Vine_and_Vineyard/_source/glossary_data.py)
  - IGP map                      (IGP names embedded in « Vignobles de France — Carte des IGP.html »)
  - hand-written questions       (HAND below) from the Categories, Bottle sizes, Numbers, Tasting and Quotes pages.

A question: dict(id, lv (1-3), cat, q=(fr,en), a=(fr,en), d=[(fr,en)×3], x=(fr,en) explanation, href, lk=(fr,en) link label)
"""
import json
import random
import re
import sys
import unicodedata
from pathlib import Path

INFOS = Path(__file__).resolve().parents[2]
SITE = INFOS.parent
sys.path.insert(0, str(INFOS / 'Vine_and_Vineyard' / 'Cepages' / '_source'))
sys.path.insert(0, str(INFOS / 'Vine_and_Vineyard' / '_source'))
sys.path.insert(0, str(INFOS / '_source' / 'classifications'))
from parse import parse_all, display  # noqa: E402
import glossary_data as GL  # noqa: E402
import data as CL  # noqa: E402

RNG = random.Random(1855)

# links, relative to Infos/Literature/
CEP = '../Vine_and_Vineyard/Cepages/Cepages_et_Appellations.html'
CLA = '../Crus_Classifications.html'
GLO = '../Vine_and_Vineyard/'
IGP = '../../Vignobles de France — Carte des IGP.html'
CAT = '../Categories_of_French_Wines.html'
BOT = '../Bottle_Sizes.html'
NUM = '../French_Wine_in_Numbers.html'
TAS = '../Tasting/Wine_Tasting.html'
QUO = 'Wine_Quotes.html'

LK_CEP = ('Fiche de l’appellation (Cépages & appellations)', 'Appellation card (Grapes & appellations)')
LK_CLA = ('Les classifications des crus', 'Crus classifications')
LK_GLO = ('Glossaire de la vigne', 'Vine glossary')
LK_IGP = ('Carte des IGP', 'IGP map')
LK_CAT = ('Comprendre l’AOC-AOP', 'Understanding AOC-AOP')
LK_BOT = ('Formats de bouteilles', 'Bottle sizes')
LK_NUM = ('La France viticole en chiffres', 'French wine in numbers')
LK_TAS = ('Déguster le vin', 'Tasting wine')
LK_QUO = ('Le vin en citations', 'Wine in quotations')


def slug(s):
    s = unicodedata.normalize('NFD', s.lower().replace('œ', 'oe'))
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def same(x):
    return (x, x)


REGION_EN = {'Bourgogne': 'Burgundy', 'Val de Loire': 'Loire Valley', 'Vallée du Rhône': 'Rhône Valley',
             'Sud-Ouest': 'South-West', 'Corse': 'Corsica', 'Savoie-Bugey': 'Savoie-Bugey'}


def reg(r):
    return (r, REGION_EN.get(r, r))


# ---- how famous an AOC is → quiz level -----------------------------------------------------------
FAMOUS = {  # level 1
    'Alsace', 'Bandol', 'Beaujolais', 'Bordeaux', 'Bourgogne', 'Cahors', 'Chablis', 'Champagne', 'Chinon',
    'Châteauneuf-du-Pape', 'Condrieu', 'Côte-Rôtie', 'Côtes de Provence', 'Côtes du Rhône', 'Crozes-Hermitage',
    'Fleurie', 'Gevrey-Chambertin', 'Gigondas', 'Hermitage', 'Jurançon', 'Madiran', 'Margaux', 'Meursault', 'Morgon',
    'Muscadet', 'Médoc', 'Nuits-Saint-Georges', 'Pauillac', 'Pomerol', 'Pommard', 'Pouilly-Fuissé', 'Pouilly-Fumé',
    'Saint-Émilion', 'Sancerre', 'Sauternes', 'Tavel', 'Vouvray', 'Arbois', 'Banyuls', 'Bergerac', 'Corbières',
    'Minervois', 'Saumur', 'Beaune', 'Volnay', 'Saint-Julien', 'Saint-Estèphe', 'Moulin-à-Vent', 'Cornas',
    'Patrimonio', 'Ajaccio', 'Monbazillac', 'Graves', 'Pessac-Léognan', 'Vacqueyras', 'Cassis', 'Côtes du Roussillon',
}
KNOWN = {  # level 2 (everything else → level 3)
    'Aloxe-Corton', 'Anjou', 'Barsac', 'Beaujolais-Villages', 'Bellet', 'Blanquette de Limoux', 'Bonnezeaux',
    'Bourgueil', 'Brouilly', 'Buzet', 'Canon-Fronsac', 'Chambolle-Musigny', 'Chassagne-Montrachet', 'Chiroubles',
    'Château-Chalon', 'Château-Grillet', 'Chénas', 'Clairette de Die', 'Collioure', 'Corton', 'Corton-Charlemagne',
    'Costières de Nîmes', 'Coteaux du Layon', "Coteaux d'Aix-en-Provence", 'Crémant d\'Alsace', 'Crémant de Bourgogne',
    'Crémant de Loire', 'Crémant du Jura', 'Côte de Brouilly', 'Côte de Nuits-Villages', 'Côtes de Bordeaux',
    'Côtes de Bourg', 'Côtes du Jura', 'Côtes du Rhône Villages', 'Entre-deux-Mers', 'Faugères', 'Fitou', 'Fronsac',
    'Gaillac', 'Givry', 'Haut-Médoc', 'Irancy', 'Irouléguy', 'Juliénas', 'L\'Étoile', 'La Clape', 'Lalande-de-Pomerol',
    'Languedoc', 'Limoux', 'Lirac', 'Listrac-Médoc', 'Luberon', 'Mâcon', 'Marcillac', 'Marsannay', 'Maury', 'Mercurey',
    'Montagny', 'Montlouis-sur-Loire', 'Montrachet', 'Morey-Saint-Denis', 'Moulis-en-Médoc', 'Muscadet Sèvre et Maine',
    'Muscat de Beaumes-de-Venise', 'Muscat de Frontignan', 'Musigny', 'Pacherenc du Vic-Bilh', 'Palette', 'Pic Saint-Loup',
    'Picpoul de Pinet', 'Pineau des Charentes', 'Puligny-Montrachet', 'Quarts de Chaume', 'Quincy', 'Rasteau', 'Reuilly',
    'Richebourg', 'Rivesaltes', 'Romanée-Conti', 'Rully', 'Régnié', 'Saint-Amour', 'Saint-Chinian', 'Saint-Joseph',
    'Saint-Nicolas-de-Bourgueil', 'Saint-Véran', 'Saumur-Champigny', 'Savennières', 'Savigny-lès-Beaune', 'Santenay',
    'Clos de Vougeot', 'Vin de Corse', 'Vin de Savoie', 'Vosne-Romanée', 'Échezeaux', 'La Tâche', 'Ventoux',
    'Menetou-Salon', 'Touraine', 'Cheverny', 'Côtes de Duras', 'Fronton', 'Pécharmant', 'Rosé d\'Anjou', 'Vinsobres',
    'Cairanne', 'Saint-Péray', 'Chambertin', 'Bâtard-Montrachet', 'Grands-Échezeaux', 'Alsace Grand Cru', 'Saint-Mont',
    'Coteaux Champenois', 'Rosé des Riceys', 'Bourgogne Aligoté', 'Petit Chablis', 'Chablis Grand Cru', 'Côtes du Vivarais',
    'Roussette de Savoie', 'Macvin du Jura', 'Muscat du Cap Corse', 'Terrasses du Larzac', 'Côtes de Bergerac',
}


def level_of(name):
    return 1 if name in FAMOUS else 2 if name in KNOWN else 3


def pick(pool, n, avoid=()):
    pool = [p for p in dict.fromkeys(pool) if p not in avoid]
    return RNG.sample(pool, n) if len(pool) >= n else None


Q = []


def add(id_, lv, cat, q, a, d, x, href, lk):
    assert len(d) == 3 and a not in d, (id_, a, d)
    assert len({a[0], *[t[0] for t in d]}) == 4, (id_, a, d)
    Q.append(dict(id=id_, lv=lv, cat=cat, q=q, a=a, d=d, x=x, href=href, lk=lk))


# =================================================================================== AOC data
AOCS = parse_all()
BY = {a['name']: a for a in AOCS}
REGIONS = sorted({a['region'] for a in AOCS})
NEIGHBOUR_CLASH = {('Beaujolais', 'Bourgogne'), ('Bourgogne', 'Beaujolais')}


def cep_link(name):
    return CEP + '#aoc=' + slug(name)


# 1) which region is AOC X in?
for a in AOCS:
    n, r = a['name'], a['region']
    lv = level_of(n)
    if slug(r).split('-')[0][:5] in slug(n) or (r == 'Vallée du Rhône' and 'rhone' in slug(n)):
        lv = 1  # the name gives the region away (Crémant du Jura, Pineau des Charentes…)
    others = [x for x in REGIONS if x != r and (r, x) not in NEIGHBOUR_CLASH]
    if lv == 1:  # obvious: avoid regions with a similar-sounding AOC
        others = [x for x in others if x not in ('Charentes',)]
    d = pick(others, 3)
    add(f'reg-{slug(n)}', lv, 'region',
        (f'Dans quelle région viticole se trouve l’AOC <b>{n}</b> ?', f'In which wine region is the <b>{n}</b> AOC?'),
        reg(r), [reg(x) for x in d],
        (f'{n} est une appellation de la région {r}.', f'{n} is an appellation of the {REGION_EN.get(r, r)} region.'),
        cep_link(n), LK_CEP)

# 2) which of these AOCs is in region X?  (levels 1 and 2 only: famous names)
for r in REGIONS:
    mine = [a['name'] for a in AOCS if a['region'] == r]
    for lv, pool in ((1, FAMOUS), (2, KNOWN)):
        cand = [n for n in mine if n in pool]
        for n in cand[:4]:
            others = [a['name'] for a in AOCS if a['region'] != r and (r, a['region']) not in NEIGHBOUR_CLASH
                      and a['name'] in pool and not a['name'].startswith(n.split(' ')[0][:6])]
            d = pick(others, 3)
            if not d:
                continue
            add(f'inreg-{slug(r)}-{slug(n)}', lv, 'region',
                (f'Laquelle de ces appellations appartient à la région <b>{r}</b> ?',
                 f'Which of these appellations belongs to the <b>{REGION_EN.get(r, r)}</b> region?'),
                same(n), [same(x) for x in d],
                (f'{n} : région {r}. Les autres : ' + ', '.join(f'{x} ({BY[x]["region"]})' for x in d) + '.',
                 f'{n}: {REGION_EN.get(r, r)}. The others: ' + ', '.join(f'{x} ({REGION_EN.get(BY[x]["region"], BY[x]["region"])})' for x in d) + '.'),
                cep_link(n), LK_CEP)

# 3) single-grape wines: which grape makes the <AOC> <colour>?
LABELS = {'Blanc': ('blanc', 'white'), 'Rouge': ('rouge', 'red'), 'Rouge, Rosé': ('rouge (et rosé)', 'red (and rosé)'),
          'Rosé': ('rosé', 'rosé'), 'Blanc liquoreux': ('liquoreux', 'sweet white'), 'Blanc moelleux': ('moelleux', 'medium-sweet white'),
          'Vin jaune': ('« vin jaune »', '“vin jaune”'), 'Blanc effervescent': ('effervescent', 'sparkling')}
ALL_GRAPES = {}
for a in AOCS:
    for w in a['wines']:
        for g in w['grapes']:
            ALL_GRAPES.setdefault(g['code'], set()).add(display(g['key'], g['code']))
MAJOR = {'B': ['Chardonnay Blanc', 'Sauvignon Blanc', 'Chenin Blanc', 'Sémillon Blanc', 'Riesling Blanc', 'Viognier Blanc',
               'Melon Blanc', 'Aligoté Blanc', 'Savagnin Blanc', 'Muscadelle Blanc', 'Marsanne Blanc', 'Roussanne Blanc',
               'Gros Manseng Blanc', 'Petit Manseng Blanc', 'Gewurztraminer Rosé', 'Mauzac Blanc', 'Altesse Blanc',
               'Jacquère Blanc', 'Rolle Blanc', 'Piquepoul Blanc Blanc', 'Muscat à Petits Grains Blanc'],
         'N': ['Pinot Noir Noir', 'Gamay Noir', 'Syrah Noir', 'Merlot Noir', 'Cabernet Franc Noir', 'Cabernet-Sauvignon Noir',
               'Grenache Noir', 'Cot Noir', 'Tannat Noir', 'Mourvèdre Noir', 'Poulsard Noir', 'Trousseau Noir',
               'Mondeuse Noir', 'Négrette Noir', 'Fer Noir', 'Nielluccio Noir', 'Sciaccarello Noir', 'Carignan Noir']}
for a in AOCS:
    n = a['name']
    for w in a['wines']:
        if len(w['grapes']) != 1 or w['label'] not in LABELS:
            continue
        g = w['grapes'][0]
        gname = display(g['key'], g['code'])
        code = g['code']
        pool = [x for x in MAJOR.get(code, sorted(ALL_GRAPES.get(code, []))) if x in ALL_GRAPES.get(code, set())] \
            if code in MAJOR else sorted(ALL_GRAPES.get(code, []))
        d = pick(pool, 3, avoid=(gname,))
        if not d:
            continue
        lab = LABELS[w['label']]
        lv = level_of(n)
        add(f'grape-{slug(n)}-{slug(w["label"])}', lv, 'grape',
            (f'Quel est l’unique cépage du <b>{n} {lab[0]}</b> ?', f'What is the single grape variety of <b>{n} {lab[1]}</b>?'),
            same(gname), [same(x) for x in d],
            (f'Le cahier des charges du {n} {lab[0]} n’autorise que le {gname}.', f'The {n} {lab[1]} rulebook allows only {gname}.'),
            cep_link(n), LK_CEP)

# 4) special wine styles → which AOC makes it (keywords matched in the wine labels; EXCL = also makes it, unlabelled)
STYLES = [
    ('jaune', ('du vin jaune', 'vin jaune'), ['vin jaune'], []),
    ('paille', ('du vin de paille', 'vin de paille (straw wine)'), ['vin de paille'], []),
    ('vdn', ('un vin doux naturel', 'a vin doux naturel'), ['vin doux naturel', 'vdn'], ['Muscat', 'Banyuls', 'Maury', 'Rivesaltes', 'Rasteau', 'Roussillon', 'Macvin', 'Pineau', 'Floc', 'Clairette du Languedoc']),
    ('liqueur', ('un vin de liqueur', 'a vin de liqueur'), ['vin de liqueur'], ['Macvin', 'Pineau', 'Floc', 'Muscat', 'Banyuls', 'Maury', 'Rivesaltes', 'Rasteau', 'Roussillon']),
    ('clairet', ('du clairet', 'clairet'), ['clairet'], ['Bordeaux']),
    ('gris', ('un vin gris', 'a vin gris'), ['gris'], []),
    ('ancestrale', ('un vin de méthode ancestrale', 'an ancestral-method sparkling wine'), ['ancestrale'], ['Limoux', 'Bugey', 'Die']),
    ('vt', ('des vendanges tardives', 'vendanges tardives (late-harvest wines)'), ['vendanges tardives'], ['Alsace', 'Jurançon', 'Pacherenc', 'Gaillac']),
]
for key, (fr, en), kws, excl in STYLES:
    def has(a):
        txt = ' '.join(w['label'] for w in a['wines']).lower()
        return any(k in txt for k in kws)
    makers = [a['name'] for a in AOCS if has(a)]
    nonmakers = [a['name'] for a in AOCS if not has(a) and not any(e in a['name'] for e in excl)
                 and not any(k.split()[-1] in a['name'].lower() for k in kws)]
    for n in makers:
        lv = 1 if key in ('jaune', 'vdn') and n in FAMOUS else 2 if n in FAMOUS | KNOWN else 3
        pool = [x for x in nonmakers if (x in FAMOUS | KNOWN) == (lv < 3)]
        d = pick(pool, 3)
        add(f'style-{key}-{slug(n)}', lv, 'style',
            (f'Laquelle de ces appellations produit {fr} ?', f'Which of these appellations produces {en}?'),
            same(n), [same(x) for x in d],
            (f'{n} figure parmi les appellations qui produisent {fr}.', f'{n} is one of the appellations producing {en}.'),
            cep_link(n), LK_CEP)

# =================================================================================== classifications
RANK = [('Premier cru', 'First growth'), ('Deuxième cru', 'Second growth'), ('Troisième cru', 'Third growth'),
        ('Quatrième cru', 'Fourth growth'), ('Cinquième cru', 'Fifth growth')]
FAMOUS_1855 = {'Château Lafite Rothschild', 'Château Latour', 'Château Margaux', 'Château Haut-Brion',
               'Château Mouton Rothschild', 'Château Lynch-Bages', 'Château Pontet-Canet', 'Château Palmer',
               'Château Léoville Las Cases', 'Château Cos d’Estournel', 'Château Montrose', 'Château Talbot',
               'Château Beychevelle', 'Château Ducru-Beaucaillou', 'Château Pichon Baron', 'Château Pichon Comtesse de Lalande'}
for i, (_, _, items) in enumerate(CL.M1855):
    for name, where in items:
        lv = 1 if i == 0 else 2 if name in FAMOUS_1855 else 3
        d = [RANK[j] for j in RNG.sample([k for k in range(5) if k != i], 3)]
        x_fr = f'{name} ({where.split(" · ")[0]}) est un {RANK[i][0].lower()} classé en 1855.'
        x_en = f'{name} ({where.split(" · ")[0]}) is a {RANK[i][1].lower()} in the 1855 classification.'
        if '1973' in where:
            x_fr, x_en = (f'{name} est premier cru depuis 1973 — la seule promotion de l’histoire du classement.',
                          f'{name} has been a First Growth since 1973 — the only promotion in the classification’s history.')
        add(f'1855-{slug(name)}', lv, 'classif',
            (f'Au classement de 1855, <b>{name}</b> est un…', f'In the 1855 classification, <b>{name}</b> is a…'),
            RANK[i], d, (x_fr, x_en), CLA + '#medoc-1855', LK_CLA)
# commune of a 1855 growth (famous communes only)
COMMUNES = ['Pauillac', 'Margaux', 'Saint-Julien', 'Saint-Estèphe', 'Haut-Médoc']
for i, (_, _, items) in enumerate(CL.M1855):
    for name, where in items:
        c = where.split(' · ')[0]
        if c not in COMMUNES:
            continue
        lv = 2 if name in FAMOUS_1855 else 3
        d = pick([x for x in COMMUNES if x != c], 3)
        add(f'1855c-{slug(name)}', lv, 'classif',
            (f'Dans quelle appellation se trouve <b>{name}</b> (cru classé 1855) ?', f'In which appellation is <b>{name}</b> (1855 classified growth)?'),
            same(c), [same(x) for x in d],
            (f'{name} : {c}.', f'{name}: {c}.'), CLA + '#medoc-1855', LK_CLA)
# Sauternes
SRANK = [('Premier cru supérieur', 'Superior first growth'), ('Premier cru', 'First growth'), ('Deuxième cru', 'Second growth')]
for i, (_, _, items) in enumerate(CL.S1855):
    for name, where in items:
        lv = 1 if i == 0 else 3
        d = [SRANK[j] for j in range(3) if j != i] + [('Cru bourgeois', 'Cru bourgeois')]
        add(f's1855-{slug(name)}', lv, 'classif',
            (f'Au classement de 1855 des Sauternes et Barsac, <b>{name}</b> est un…', f'In the 1855 Sauternes & Barsac classification, <b>{name}</b> is a…'),
            SRANK[i], d,
            (f'{name} ({where}) : {SRANK[i][0].lower()}.' + (' C’est le seul « premier cru supérieur ».' if i == 0 else ''),
             f'{name} ({where}): {SRANK[i][1].lower()}.' + (' It is the only “superior first growth”.' if i == 0 else '')),
            CLA + '#sauternes-1855', LK_CLA)
# Saint-Émilion A
add('se-a', 2, 'classif',
    ('Quels sont les deux « premiers grands crus classés A » de Saint-Émilion (classement 2022) ?',
     'Which two châteaux are Saint-Émilion « premiers grands crus classés A » (2022 classification)?'),
    same('Figeac et Pavie'), [same('Cheval Blanc et Ausone'), same('Angélus et Pavie'), same('Figeac et Angélus')],
    ('En 2022, Figeac et Pavie sont les deux seuls « A » : Cheval Blanc, Ausone et Angélus se sont retirés du classement.',
     'In 2022 Figeac and Pavie are the only two “A”s: Cheval Blanc, Ausone and Angélus withdrew from the classification.'),
    CLA + '#saint-emilion', LK_CLA)
# Burgundy grands crus → village
BV = {}
for _, _, items in CL.BGC:
    for name, where, col in items:
        BV[name] = (where, col)
VILLAGES = ['Gevrey-Chambertin', 'Morey-Saint-Denis', 'Chambolle-Musigny', 'Vougeot', 'Flagey-Échezeaux', 'Vosne-Romanée',
            'Puligny-Montrachet', 'Chassagne-Montrachet']
for name, (where, col) in BV.items():
    if where not in VILLAGES:
        continue
    lv = 2 if name in ('Chambertin', 'Romanée-Conti', 'La Tâche', 'Clos de Vougeot', 'Musigny', 'Richebourg') else 3
    d = pick([v for v in VILLAGES if v != where and not (where.endswith('Montrachet') and v.endswith('Montrachet') and lv == 2)], 3)
    add(f'bgc-{slug(name)}', lv, 'classif',
        (f'Sur quelle commune se trouve le grand cru <b>{name}</b> ?', f'In which village is the <b>{name}</b> grand cru?'),
        same(where), [same(x) for x in d],
        (f'{name} : grand cru de {where}.', f'{name}: grand cru of {where}.'), CLA + '#bourgogne', LK_CLA)
# Burgundy white vs red grands crus
whites = [n for n, (w, c) in BV.items() if c == 'B' and 'Chablis' not in n]
reds = [n for n, (w, c) in BV.items() if c == 'R']
for n in whites:
    d = pick(reds, 3)
    add(f'bgcw-{slug(n)}', 3, 'classif',
        ('Lequel de ces grands crus de Bourgogne est un vin <b>blanc</b> ?', 'Which of these Burgundy grands crus is a <b>white</b> wine?'),
        same(n), [same(x) for x in d],
        (f'{n} est un grand cru blanc (chardonnay) ; les trois autres sont des rouges (pinot noir).',
         f'{n} is a white grand cru (Chardonnay); the other three are reds (Pinot Noir).'), CLA + '#bourgogne', LK_CLA)
# Alsace & Champagne grands crus
for n in CL.AGC:
    d = pick(CL.CGC + [x for x in BV if ' ' not in x], 3)
    add(f'agc-{slug(n)}', 3 if n not in ('Rangen', 'Schlossberg', 'Brand', 'Hengst', 'Schoenenbourg') else 2, 'classif',
        ('Lequel de ces noms est un <b>grand cru d’Alsace</b> ?', 'Which of these names is an <b>Alsace grand cru</b>?'),
        same(n), [same(x) for x in d],
        (f'{n} est l’un des 51 grands crus d’Alsace.', f'{n} is one of Alsace’s 51 grands crus.'), CLA + '#alsace', LK_CLA)
for n in CL.CGC:
    d = pick(CL.CPC, 3)
    add(f'cgc-{slug(n)}', 3, 'classif',
        ('Lequel de ces villages est classé <b>grand cru</b> en Champagne ?', 'Which of these villages is a Champagne <b>grand cru</b>?'),
        same(n), [same(x) for x in d],
        (f'{n} est l’un des 17 villages grands crus ; les autres sont des premiers crus.',
         f'{n} is one of the 17 grand cru villages; the others are premiers crus.'), CLA + '#champagne', LK_CLA)
# Burgundy premiers crus → appellation (Côte d'Or only, distinctive names)
PC = json.loads((INFOS / '_source' / 'classifications' / 'premiers_crus.json').read_text())
COTE_DOR = {'Gevrey-Chambertin', 'Morey-Saint-Denis', 'Chambolle-Musigny', 'Vougeot', 'Vosne-Romanée', 'Nuits-Saint-Georges',
            'Aloxe-Corton', 'Savigny-lès-Beaune', 'Beaune', 'Pommard', 'Volnay', 'Meursault', 'Puligny-Montrachet',
            'Chassagne-Montrachet', 'Saint-Aubin', 'Santenay', 'Monthélie', 'Auxey-Duresses', 'Pernand-Vergelesses', 'Fixin', 'Ladoix'}
names_count = {}
for row in PC:
    names_count[row[2]] = names_count.get(row[2], 0) + 1
STAR_PC = {'Les Amoureuses', 'Clos Saint-Jacques', 'Les Charmes', 'Les Perrières', 'Les Rugiens', 'Les Épenots',
           'Les Cazetiers', 'Les Suchots', 'Les Malconsorts', 'Aux Malconsorts', 'Les Saint-Georges', 'Les Vaucrains',
           'Les Pucelles', 'Les Combettes', 'Les Folatières', 'Clos des Ducs', 'Les Caillerets', 'Les Grèves', 'Clos des Mouches',
           'Les Genevrières', 'Cros Parantoux', 'Les Beaux Monts', 'Les Fuées', 'Les Cras'}
seen_pc = set()
for app_slug, app, climat, _, parent in PC:
    if app not in COTE_DOR or names_count[climat] != 1 or parent or climat in seen_pc \
            or slug(app).split('-')[0] in slug(climat):
        continue
    seen_pc.add(climat)
    lv = 2 if climat in STAR_PC else 3
    d = pick([x for x in COTE_DOR if x != app], 3)
    add(f'pc-{slug(app)}-{slug(climat)}', lv, 'classif',
        (f'Le premier cru <b>{climat}</b> appartient à quelle appellation ?', f'The premier cru <b>{climat}</b> belongs to which appellation?'),
        same(app), [same(x) for x in d],
        (f'{climat} est un premier cru de {app}.', f'{climat} is a premier cru of {app}.'),
        CLA + '#premiers-crus=' + climat.replace(' ', '%20'), ('Moteur des premiers crus', 'Premier cru search'))

# =================================================================================== IGP vs AOC
igp_html = (SITE / 'Vignobles de France — Carte des IGP.html').read_text()
IGPS = re.findall(r'"([^"]{2,60})": \{"colours"', igp_html)
AOC_NAMES = [a['name'] for a in AOCS]
for n in IGPS:
    if n in AOC_NAMES:
        continue
    lv = 1 if n in ("Pays d'Oc", 'Val de Loire', 'Côtes de Gascogne', 'Méditerranée') else 2 if n in (
        'Atlantique', 'Comté Tolosan', 'Comtés Rhodaniens', 'Terres du Midi', 'Var', 'Gard', 'Vaucluse', 'Ardèche', 'Charentais') else 3
    pool = [x for x in AOC_NAMES if (FAMOUS if lv == 1 else KNOWN if lv == 2 else set(AOC_NAMES)).__contains__(x)
            and not x.startswith(n[:5])]
    d = pick(pool, 3)
    add(f'igp-{slug(n)}', lv, 'categ',
        ('Lequel de ces noms est une <b>IGP</b> (et non une AOC) ?', 'Which of these names is an <b>IGP</b> (not an AOC)?'),
        same(n), [same(x) for x in d],
        (f'{n} est une Indication géographique protégée ; les trois autres sont des AOC.',
         f'{n} is a Protected Geographical Indication; the other three are AOCs.'), IGP, LK_IGP)

# =================================================================================== glossary
EASY = {'Baie', 'Cep', 'Cépage', 'Grappe', 'Pépin', 'Rafle', 'Sarment', 'Vendange', 'Millésime', 'Véraison', 'Floraison',
        'Terroir', 'Vieilles vignes', 'Phylloxéra', 'Mildiou', 'Pourriture noble', 'Agriculture biologique', 'Vin nature',
        'Rendement', 'Machine à vendanger', 'Débourrement', 'Clos', 'Taille', 'Greffe', 'Porte-greffe'}
HARD_CATS = {'ennemis', 'taille', 'vert', 'plantation', 'regles'}
by_cat = {}
for t in GL.TERMS:
    by_cat.setdefault(t[2], []).append(t)
for fr, en, cat, link, dfr, den in GL.TERMS:
    lv = 1 if fr in EASY else 3 if cat in HARD_CATS else 2
    word = fr.split(',')[0].split(' (')[0].lower()
    pool = [t for t in by_cat[cat] if t[0] != fr and word not in t[4].lower() and t[0].split(',')[0].split(' (')[0].lower() not in dfr.lower()]
    if len(pool) < 3:
        pool = [t for t in GL.TERMS if t[0] != fr and word not in t[4].lower()]
    d = RNG.sample(pool, 3)
    # the definition must not contain the word itself (would give the answer away) → skip those
    if word in dfr.lower() and len(word) > 3:
        continue
    add(f'glo-{slug(fr)}', lv, 'vine',
        (f'Que désigne le mot <b>{fr}</b> ?', f'What does <b>{en}</b> mean?'),
        (dfr, den), [(t[4], t[5]) for t in d],
        (f'{fr} : {dfr}', f'{en}: {den}'), GLO + link, LK_GLO)

# =================================================================================== hand-written
def H(id_, lv, cat, q, a, d, x, href, lk):
    add('h-' + id_, lv, cat, q, a, d, x, href, lk)


H('aop', 1, 'categ', ('Que signifie le sigle <b>AOP</b> ?', 'What does <b>AOP</b> stand for?'),
  ('Appellation d’origine protégée', 'Appellation d’Origine Protégée (Protected Designation of Origin)'),
  [('Appellation officielle de production', 'Appellation Officielle de Production'), ('Association des œnologues professionnels', 'Association des Œnologues Professionnels'),
   ('Agriculture d’origine paysanne', 'Agriculture d’Origine Paysanne')],
  ('AOP est l’équivalent européen de l’AOC française.', 'AOP is the European equivalent of the French AOC.'), CAT, LK_CAT)
H('inao', 1, 'categ', ('Quel organisme public gère les appellations en France ?', 'Which public body manages French appellations?'),
  same('INAO'), [same('FranceAgriMer'), same('DGCCRF'), same('OIV')],
  ('L’INAO (Institut national de l’origine et de la qualité) reconnaît et suit les AOC et les IGP.',
   'The INAO (Institut National de l’Origine et de la Qualité) recognises and oversees AOCs and IGPs.'), CAT, LK_CAT)
H('vdf', 1, 'categ', ('Quelle catégorie a remplacé l’ancien « Vin de Table » ?', 'Which category replaced the old “Vin de Table”?'),
  same('Vin de France'), [same('IGP'), same('Vin de Pays'), same('VDQS')],
  ('Depuis 2009, le Vin sans indication géographique s’étiquette « Vin de France ».', 'Since 2009, wine without a geographical indication is labelled “Vin de France”.'), CAT, LK_CAT)
H('igp-vdp', 1, 'categ', ('Les IGP sont les héritières des…', 'IGPs are the successors of the…'),
  ('Vins de Pays', 'Vins de Pays'), [('Vins de Table', 'Vins de Table'), ('VDQS', 'VDQS'), ('Grands crus', 'Grands crus')],
  ('Les Vins de Pays, créés en 1968, sont devenus les IGP.', 'The Vins de Pays, created in 1968, became the IGPs.'), CAT, LK_CAT)
H('3cat', 1, 'categ', ('Combien de catégories de vins y a-t-il aujourd’hui en France ?', 'How many wine categories are there in France today?'),
  same('3'), [same('2'), same('4'), same('5')],
  ('AOC/AOP, IGP et Vin de France — depuis la disparition des VDQS fin 2011.', 'AOC/AOP, IGP and Vin de France — since the VDQS disappeared at the end of 2011.'), CAT, LK_CAT)
H('phyllo', 1, 'categ', ('Quel insecte a ravagé le vignoble français à la fin du XIX<sup>e</sup> siècle ?', 'Which insect devastated French vineyards in the late 19th century?'),
  same('Le phylloxéra'), [same('La cicadelle'), same('Le doryphore'), same('La drosophile')],
  ('Ce puceron venu d’Amérique, signalé en 1863 dans le Gard, a ravagé plus de 40 % du vignoble.', 'This aphid from America, first recorded in 1863 in the Gard, devastated over 40 % of the vineyards.'), CAT, LK_CAT)
H('1935', 2, 'categ', ('En quelle année le décret-loi créant l’AOC a-t-il été signé ?', 'In which year was the decree-law creating the AOC signed?'),
  same('1935'), [same('1905'), same('1919'), same('1947')],
  ('Décret-loi du 30 juillet 1935, sous l’impulsion de Joseph Capus.', 'Decree-law of 30 July 1935, driven by Joseph Capus.'), CAT, LK_CAT)
H('first6', 3, 'categ', ('Laquelle de ces appellations faisait partie des <b>six premières AOC</b> (15 mai 1936) ?', 'Which of these was among the <b>first six AOCs</b> (15 May 1936)?'),
  same('Tavel'), [same('Pauillac'), same('Meursault'), same('Vouvray')],
  ('Les six premières : Arbois, Cassis, Châteauneuf-du-Pape, Cognac, Monbazillac et Tavel.', 'The first six: Arbois, Cassis, Châteauneuf-du-Pape, Cognac, Monbazillac and Tavel.'), CAT, LK_CAT)
H('first6b', 3, 'categ', ('Laquelle de ces appellations faisait partie des <b>six premières AOC</b> (1936) ?', 'Which of these was among the <b>first six AOCs</b> (1936)?'),
  same('Monbazillac'), [same('Sauternes'), same('Chablis'), same('Sancerre')],
  ('Sauternes, Chablis et Sancerre sont arrivés plus tard dans l’année 1936. Les six premières : Arbois, Cassis, Châteauneuf-du-Pape, Cognac, Monbazillac, Tavel.',
   'Sauternes, Chablis and Sancerre came later in 1936. The first six: Arbois, Cassis, Châteauneuf-du-Pape, Cognac, Monbazillac, Tavel.'), CAT, LK_CAT)
H('capus', 3, 'categ', ('Qui est considéré comme le « père » de l’AOC ?', 'Who is considered the “father” of the AOC?'),
  same('Joseph Capus'), [same('Louis Pasteur'), same('Jules Guyot'), same('Émile Peynaud')],
  ('Agronome et sénateur de la Gironde, Joseph Capus inspire les lois de 1927 et 1935 et préside le Comité national jusqu’en 1947.',
   'Agronomist and senator for the Gironde, Joseph Capus inspired the 1927 and 1935 laws and chaired the national committee until 1947.'), CAT, LK_CAT)
H('leroy', 3, 'categ', ('Dans quelle appellation le baron Le Roy a-t-il élaboré les règles qui ont servi de modèle aux AOC ?', 'In which appellation did Baron Le Roy draw up the rules that became the model for AOCs?'),
  same('Châteauneuf-du-Pape'), [same('Saint-Émilion'), same('Hermitage'), same('Gevrey-Chambertin')],
  ('Syndicat fondé en 1923 : sols, cépages, 12,5 % minimum, tri obligatoire.', 'Growers’ union founded in 1923: soils, grape list, 12.5 % minimum, compulsory sorting.'), CAT, LK_CAT)
H('1907', 3, 'categ', ('Quel événement a lieu dans le Midi en 1907 ?', 'What happened in the Midi in 1907?'),
  ('La révolte des vignerons', 'The growers’ revolt'), [('L’arrivée du phylloxéra', 'The arrival of phylloxera'), ('La création de l’INAO', 'The creation of the INAO'), ('Le premier classement des crus', 'The first classification of growths')],
  ('Ruinés par la fraude et la surproduction, quelque 600 000 personnes défilent à Montpellier le 9 juin 1907.', 'Ruined by fraud and overproduction, some 600,000 people marched in Montpellier on 9 June 1907.'), CAT, LK_CAT)
H('1911', 3, 'categ', ('Dans quelle région éclatent les émeutes viticoles de 1911 ?', 'In which region did the 1911 wine riots break out?'),
  same('Champagne'), [same('Bordeaux'), same('Bourgogne'), same('Languedoc')],
  ('La délimitation de 1908 excluait l’Aube : émeutes à Damery, Hautvillers, Aÿ, et 40 000 soldats envoyés.', 'The 1908 delimitation excluded the Aube: riots in Damery, Hautvillers, Aÿ, and 40,000 troops sent in.'), CAT, LK_CAT)
H('griffe', 3, 'categ', ('Quelle loi de 1889 donne la première définition légale du vin ?', 'Which 1889 law gave the first legal definition of wine?'),
  same('La loi Griffe'), [same('La loi Capus'), same('La loi Evin'), same('La loi Royer')],
  ('Le vin est réservé au produit de la fermentation des raisins frais.', 'Wine is reserved for the product of the fermentation of fresh grapes.'), CAT, LK_CAT)
H('vdqs', 3, 'categ', ('Quelle catégorie de vins a disparu fin 2011 ?', 'Which wine category disappeared at the end of 2011?'),
  same('VDQS'), [same('IGP'), same('Vin de France'), same('Crémant')],
  ('Les Vins délimités de qualité supérieure sont devenus AOC ou IGP.', 'The VDQS (Vins Délimités de Qualité Supérieure) became AOCs or IGPs.'), CAT, LK_CAT)
H('vdf-cepage', 2, 'categ', ('Un « Vin de France » peut-il indiquer un cépage et un millésime sur l’étiquette ?', 'Can a “Vin de France” show a grape variety and a vintage on its label?'),
  ('Oui, depuis 2009', 'Yes, since 2009'), [('Non, jamais', 'No, never'), ('Seulement le cépage', 'Only the grape'), ('Seulement le millésime', 'Only the vintage')],
  ('Depuis le 1er août 2009, à condition d’au moins 85 % du cépage ou de l’année indiqués.', 'Since 1 August 2009, provided at least 85 % is from the grape or year shown.'), CAT, LK_CAT)
H('vdp1968', 3, 'categ', ('En quelle année les Vins de Pays ont-ils été créés ?', 'In which year were the Vins de Pays created?'),
  same('1968'), [same('1935'), same('1973'), same('1992')], ('Décret du 13 septembre 1968.', 'Decree of 13 September 1968.'), CAT, LK_CAT)
H('inao2007', 3, 'categ', ('Depuis 2007, que signifie le « Q » de l’INAO ?', 'Since 2007, what does the “Q” in INAO stand for?'),
  ('Qualité', 'Quality (Qualité)'), [('Quota', 'Quota'), ('Quintal', 'Quintal'), ('Quartier', 'Quarter (Quartier)')],
  ('Institut national de l’origine et de la qualité depuis le 1er janvier 2007.', 'Institut National de l’Origine et de la Qualité since 1 January 2007.'), CAT, LK_CAT)
H('tastevin', 3, 'categ', ('Où la Confrérie des Chevaliers du Tastevin a-t-elle été fondée en 1934 ?', 'Where was the Confrérie des Chevaliers du Tastevin founded in 1934?'),
  same('Nuits-Saint-Georges'), [same('Beaune'), same('Dijon'), same('Vougeot')],
  ('Fondée le 16 novembre 1934 pour relancer les ventes de Bourgogne en pleine crise.', 'Founded on 16 November 1934 to revive Burgundy sales during the Depression.'), CAT, LK_CAT)
H('vougeot', 3, 'categ', ('Le Clos de Vougeot (≈ 50 ha) est partagé entre environ…', 'The Clos de Vougeot (≈ 50 ha) is shared by about…'),
  ('80 propriétaires', '80 owners'), [('5 propriétaires', '5 owners'), ('un seul propriétaire', 'a single owner'), ('300 propriétaires', '300 owners')],
  ('Propriété unique jusqu’en 1889, il est aujourd’hui morcelé entre quelque 80 propriétaires.', 'A single property until 1889, it is now split among some 80 owners.'), CAT, LK_CAT)
H('aoc-share', 3, 'categ', ('Quelle part de la surface du vignoble français est en AOC/AOP (2024) ?', 'What share of French vineyard area is AOC/AOP (2024)?'),
  same('≈ 55 %'), [same('≈ 15 %'), same('≈ 30 %'), same('≈ 90 %')],
  ('≈ 404 300 ha en AOC/AOP, 27 % en IGP, 5 % en Vin de France, 12 % pour le Cognac et l’Armagnac (FranceAgriMer).', '≈ 404,300 ha AOC/AOP, 27 % IGP, 5 % Vin de France, 12 % for Cognac and Armagnac (FranceAgriMer).'), CAT, LK_CAT)
H('pinard', 3, 'categ', ('En 1916, quelle était la ration quotidienne de vin (« pinard ») du soldat français ?', 'In 1916, what was the French soldier’s daily wine (“pinard”) ration?'),
  ('Un demi-litre', 'Half a litre'), [('Un verre', 'One glass'), ('Deux litres', 'Two litres'), ('Aucune', 'None')],
  ('Un quart de litre en 1914, un demi-litre en 1916, jusqu’à un litre en 1918.', 'A quarter-litre in 1914, half a litre in 1916, up to a litre in 1918.'), CAT, LK_CAT)

# bottle sizes
H('75cl', 1, 'bottle', ('Quelle est la contenance d’une bouteille de vin standard ?', 'How much does a standard wine bottle hold?'),
  same('75 cl'), [same('70 cl'), same('1 litre'), same('50 cl')],
  ('Le 75 cl est la norme légale en Europe depuis 1975.', '75 cl has been the legal standard in Europe since 1975.'), BOT + '#pourquoi-75cl', LK_BOT)
H('magnum', 1, 'bottle', ('Un magnum contient…', 'A magnum holds…'), ('2 bouteilles (1,5 L)', '2 bottles (1.5 L)'),
  [('3 bouteilles (2,25 L)', '3 bottles (2.25 L)'), ('4 bouteilles (3 L)', '4 bottles (3 L)'), ('1,5 bouteille (1,125 L)', '1.5 bottles (1.125 L)')],
  ('Magnum = 1,5 L.', 'Magnum = 1.5 L.'), BOT + '#gamme', LK_BOT)
H('6glasses', 1, 'bottle', ('Combien de verres de 12,5 cl sert une bouteille de 75 cl ?', 'How many 12.5 cl glasses does a 75 cl bottle pour?'),
  same('6'), [same('4'), same('8'), same('10')], ('75 ÷ 12,5 = 6.', '75 ÷ 12.5 = 6.'), BOT, LK_BOT)
H('clavelin', 1, 'bottle', ('Le clavelin (62 cl) est réservé à quel vin ?', 'The clavelin (62 cl) is reserved for which wine?'),
  ('Le vin jaune du Jura', 'Jura vin jaune'), [('Le champagne', 'Champagne'), ('Le sauternes', 'Sauternes'), ('Le muscadet', 'Muscadet')],
  ('Légende : 62 cl, c’est ce qui reste d’un litre après au moins 6 ans et 3 mois d’élevage sous voile.', 'Legend: 62 cl is what remains of a litre after at least 6 years 3 months under veil.'), BOT + '#autres', LK_BOT)
H('flute', 1, 'bottle', ('La flûte est obligatoire pour les AOC de quelle région ?', 'The flute bottle is mandatory for the AOCs of which region?'),
  same('Alsace'), [same('Bordeaux'), same('Bourgogne'), same('Champagne')],
  ('Elle est aussi autorisée à Cassis, Tavel, Muscadet, Château-Grillet, Côtes de Provence…', 'It is also allowed in Cassis, Tavel, Muscadet, Château-Grillet, Côtes de Provence…'), BOT + '#autres', LK_BOT)
H('barrique', 2, 'bottle', ('Quelle est la contenance d’une barrique bordelaise ?', 'How much does a Bordeaux barrique hold?'),
  same('225 L'), [same('114 L'), same('300 L'), same('600 L')],
  ('225 L ≈ 50 gallons ≈ 300 bouteilles = 25 caisses de 12.', '225 L ≈ 50 gallons ≈ 300 bottles = 25 cases of 12.'), BOT + '#pourquoi-75cl', LK_BOT)
H('jero', 2, 'bottle', ('En Champagne (et Bourgogne), un jéroboam contient…', 'In Champagne (and Burgundy), a jeroboam holds…'),
  same('3 L'), [same('4,5 L'), same('6 L'), same('1,5 L')], ('Jéroboam = 4 bouteilles. Attention : à Bordeaux, le nom désigne 4,5 à 5 L.', 'Jeroboam = 4 bottles. Beware: in Bordeaux the name means 4.5–5 L.'), BOT + '#gamme', LK_BOT)
H('mathu', 2, 'bottle', ('Un mathusalem contient…', 'A methuselah holds…'), ('6 L (8 bouteilles)', '6 L (8 bottles)'),
  [('3 L (4 bouteilles)', '3 L (4 bottles)'), ('9 L (12 bouteilles)', '9 L (12 bottles)'), ('12 L (16 bouteilles)', '12 L (16 bottles)')], ('Mathusalem = 6 L.', 'Methuselah = 6 L.'), BOT + '#gamme', LK_BOT)
H('nabu', 3, 'bottle', ('Combien de bouteilles de 75 cl dans un nabuchodonosor (15 L) ?', 'How many 75 cl bottles in a nebuchadnezzar (15 L)?'),
  same('20'), [same('15'), same('18'), same('24')], ('15 L ÷ 0,75 = 20 bouteilles.', '15 L ÷ 0.75 = 20 bottles.'), BOT + '#gamme', LK_BOT)
H('balth', 3, 'bottle', ('Un balthazar contient…', 'A balthazar holds…'), ('12 L (16 bouteilles)', '12 L (16 bottles)'),
  [('9 L (12 bouteilles)', '9 L (12 bottles)'), ('15 L (20 bouteilles)', '15 L (20 bottles)'), ('18 L (24 bouteilles)', '18 L (24 bottles)')], ('Balthazar = 12 L.', 'Balthazar = 12 L.'), BOT + '#gamme', LK_BOT)
H('salma', 3, 'bottle', ('Quel format contient 9 litres ?', 'Which size holds 9 litres?'), same('Salmanazar'),
  [same('Réhoboam'), same('Melchior'), same('Balthazar')], ('Salmanazar = 9 L = 12 bouteilles.', 'Salmanazar = 9 L = 12 bottles.'), BOT + '#gamme', LK_BOT)
H('imperiale', 3, 'bottle', ('À Bordeaux, une « impériale » contient…', 'In Bordeaux, an “imperial” holds…'), same('6 L'),
  [same('3 L'), same('4,5 L'), same('9 L')], ('À Bordeaux : double magnum 3 L, jéroboam 4,5-5 L, impériale 6 L.', 'In Bordeaux: double magnum 3 L, jeroboam 4.5–5 L, imperial 6 L.'), BOT + '#gamme', LK_BOT)
H('gallon', 3, 'bottle', ('Pourquoi vend-on le vin par caisses de 6 ou 12 ?', 'Why is wine sold in cases of 6 or 12?'),
  ('Un gallon impérial ≈ 6 bouteilles de 75 cl', 'One imperial gallon ≈ 6 bottles of 75 cl'),
  [('Une règle de l’Église au Moyen Âge', 'A medieval Church rule'), ('Le nombre de mois de l’élevage', 'The number of months of ageing'), ('Une norme imposée par l’ONU', 'A UN standard')],
  ('Le négoce, tourné vers l’Angleterre, comptait en gallons impériaux (4,546 L).', 'The trade, geared to England, counted in imperial gallons (4.546 L).'), BOT + '#pourquoi-75cl', LK_BOT)
H('dame', 3, 'bottle', ('Où expose-t-on des dames-jeannes au soleil pour obtenir des vins rancio ?', 'Where are demijohns left in the sun to make rancio wines?'),
  ('Banyuls et Maury', 'Banyuls and Maury'), [('Sauternes et Barsac', 'Sauternes and Barsac'), ('Arbois et Château-Chalon', 'Arbois and Château-Chalon'), ('Cassis et Bandol', 'Cassis and Bandol')],
  ('Les dames-jeannes (20 à 30 L) servent à l’oxydation ménagée des VDN du Roussillon.', 'Demijohns (20–30 L) are used for the controlled oxidation of Roussillon VDNs.'), BOT + '#autres', LK_BOT)
H('pot', 3, 'bottle', ('Quelle est la contenance traditionnelle du pot lyonnais ?', 'What is the traditional size of the Lyon “pot”?'),
  same('46 cl'), [same('25 cl'), same('37,5 cl'), same('62 cl')], ('Carafe à fond épais des bouchons lyonnais (aujourd’hui aussi 50 cl).', 'Thick-bottomed carafe of Lyon bistros (also 50 cl today).'), BOT + '#autres', LK_BOT)
H('1975', 3, 'bottle', ('Depuis quand le 75 cl est-il la norme légale en Europe ?', 'Since when has 75 cl been the legal standard in Europe?'),
  same('1975'), [same('1866'), same('1936'), same('2009')], ('Directive 75/106/CEE ; États-Unis en 1979.', 'Directive 75/106/EEC; United States in 1979.'), BOT + '#pourquoi-75cl', LK_BOT)

# numbers
H('ugni', 2, 'numbers', ('Quel est le cépage le plus planté en France ?', 'What is the most planted grape variety in France?'),
  same('Ugni blanc'), [same('Merlot'), same('Chardonnay'), same('Grenache')],
  ('≈ 92 500 ha, surtout pour le Cognac (FranceAgriMer 2024).', '≈ 92,500 ha, mostly for Cognac (FranceAgriMer 2024).'), NUM, LK_NUM)
H('lr', 2, 'numbers', ('Quel est le plus grand vignoble de France en surface ?', 'Which is France’s largest vineyard by area?'),
  same('Languedoc-Roussillon'), [same('Bordelais'), same('Champagne'), same('Val de Loire')],
  ('≈ 207 000 ha, loin devant Rhône-Provence et le Bordelais (≈ 112 000 ha chacun).', '≈ 207,000 ha, far ahead of Rhône-Provence and Bordeaux (≈ 112,000 ha each).'), NUM, LK_NUM)
H('italy', 2, 'numbers', ('Quel pays est le premier producteur mondial de vin en 2025 ?', 'Which country is the world’s largest wine producer in 2025?'),
  ('Italie', 'Italy'), [('France', 'France'), ('Espagne', 'Spain'), ('États-Unis', 'United States')],
  ('Italie 44,4 M hl, France 36,1, Espagne 28,7 (OIV).', 'Italy 44.4 M hl, France 36.1, Spain 28.7 (OIV).'), NUM, LK_NUM)
H('usa', 2, 'numbers', ('Quel est le premier pays (hors UE) acheteur de vins français ?', 'Which country (outside the EU) is the top buyer of French wine?'),
  ('États-Unis', 'United States'), [('Royaume-Uni', 'United Kingdom'), ('Chine', 'China'), ('Japon', 'Japan')],
  ('≈ 20 % de la valeur des exportations (2024).', '≈ 20 % of export value (2024).'), NUM, LK_NUM)
H('colours24', 3, 'numbers', ('En 2024, quelle a été la répartition rouge / blanc de la production française ?', 'In 2024, how did French red / white production compare?'),
  ('À égalité : 38 % / 38 %', 'Equal: 38 % / 38 %'), [('Rouge 60 % / blanc 25 %', 'Red 60 % / white 25 %'), ('Rouge 25 % / blanc 60 %', 'Red 25 % / white 60 %'), ('Rouge 50 % / blanc 10 %', 'Red 50 % / white 10 %')],
  ('Pour la première fois, rouge et blanc à parité ; rosé 24 %.', 'For the first time red and white were level; rosé 24 %.'), NUM, LK_NUM)
H('coop', 3, 'numbers', ('Quelle part du vin français est vinifiée par les caves coopératives ?', 'What share of French wine is made by cooperatives?'),
  same('≈ 40 %'), [same('≈ 5 %'), same('≈ 15 %'), same('≈ 75 %')], ('≈ 590 caves et unions, ≈ 85 000 vignerons coopérateurs.', '≈ 590 cellars and unions, ≈ 85,000 member growers.'), NUM, LK_NUM)
H('ha', 3, 'numbers', ('Quelle est la surface du vignoble français en production (2024) ?', 'What is the area of France’s vineyard in production (2024)?'),
  same('≈ 767 000 ha'), [same('≈ 150 000 ha'), same('≈ 2 millions d’ha'), same('≈ 350 000 ha')], ('766 674 ha, soit 3 % de la surface agricole utile.', '766,674 ha, i.e. 3 % of French farmland.'), NUM, LK_NUM)

# tasting
H('5tastes', 1, 'tasting', ('Combien de saveurs élémentaires la langue perçoit-elle ?', 'How many basic tastes does the tongue perceive?'),
  same('5'), [same('3'), same('4'), same('7')], ('Sucré, salé, acide, amer et umami.', 'Sweet, salty, sour, bitter and umami.'), TAS + '#gout', LK_TAS)
H('tonguemap', 2, 'tasting', ('La « carte de la langue » (sucré sur la pointe, amer au fond…) est…', 'The “tongue map” (sweet on the tip, bitter at the back…) is…'),
  ('Un mythe', 'A myth'), [('Une loi scientifique', 'A scientific law'), ('Vraie seulement pour le vin rouge', 'True only for red wine'), ('Vraie seulement chez l’enfant', 'True only in children')],
  ('Toutes les zones perçoivent toutes les saveurs ; le schéma vient d’une mauvaise lecture (1942) d’une thèse de 1901.', 'All areas detect all tastes; the diagram comes from a 1942 misreading of a 1901 thesis.'), TAS + '#gout', LK_TAS)
H('inaoglass', 2, 'tasting', ('Le verre de dégustation de référence (norme ISO 3591) est souvent appelé…', 'The reference tasting glass (ISO 3591) is often called…'),
  ('Le verre INAO', 'The INAO glass'), [('La coupe Pompadour', 'The Pompadour coupe'), ('Le verre ballon', 'The balloon glass'), ('La flûte', 'The flute')],
  ('Coupe en œuf allongé, ouverture plus étroite que la panse.', 'Elongated-egg bowl, opening narrower than its widest point.'), TAS + '#odorat', LK_TAS)
H('tertiary', 2, 'tasting', ('D’où viennent les arômes <b>tertiaires</b> ?', 'Where do <b>tertiary</b> aromas come from?'),
  ('Du vieillissement / de l’élevage', 'Ageing / maturation'), [('Du raisin lui-même', 'The grape itself'), ('De la fermentation', 'Fermentation'), ('Du bouchon', 'The cork')],
  ('Primaires = raisin, secondaires = fermentation, tertiaires = élevage et vieillissement.', 'Primary = grape, secondary = fermentation, tertiary = maturation and ageing.'), TAS + '#odorat', LK_TAS)
H('primary', 1, 'tasting', ('Les arômes <b>primaires</b> viennent…', '<b>Primary</b> aromas come from…'),
  ('Du raisin (le cépage)', 'The grape (the variety)'), [('Du fût de chêne', 'The oak barrel'), ('Du vieillissement en bouteille', 'Bottle ageing'), ('Du verre', 'The glass')],
  ('Primaires = raisin, secondaires = fermentation, tertiaires = élevage.', 'Primary = grape, secondary = fermentation, tertiary = maturation.'), TAS + '#odorat', LK_TAS)
H('legs', 3, 'tasting', ('Les « larmes » ou « jambes » sur la paroi du verre sont surtout dues à…', 'The “legs” or “tears” on the glass are mainly caused by…'),
  ('L’évaporation de l’alcool (effet Marangoni)', 'Alcohol evaporation (Marangoni effect)'),
  [('La glycérine', 'Glycerol'), ('Le sucre résiduel', 'Residual sugar'), ('Les tanins', 'Tannins')],
  ('Glycérol et sucre n’ont presque aucun effet sur les jambes (Nurgel & Pickering, 2005).', 'Glycerol and sugar have almost no effect on legs (Nurgel & Pickering, 2005).'), TAS + '#vue', LK_TAS)
H('swirl', 1, 'tasting', ('Pourquoi fait-on tourner le vin dans le verre ?', 'Why do we swirl wine in the glass?'),
  ('Pour libérer les arômes', 'To release the aromas'), [('Pour le refroidir', 'To cool it down'), ('Pour faire tomber le dépôt', 'To settle the sediment'), ('Pour en augmenter le degré', 'To raise its alcohol')],
  ('Un mouvement circulaire doux et continu aère le vin et libère ses arômes.', 'A gentle, continuous circular motion aerates the wine and releases its aromas.'), TAS + '#odorat', LK_TAS)

# classifications (hand)
H('1855count', 2, 'classif', ('Combien de crus rouges compte le classement de 1855 (Médoc + Haut-Brion) ?', 'How many red growths are in the 1855 classification (Médoc + Haut-Brion)?'),
  same('61'), [same('5'), same('27'), same('100')], ('5 premiers, 14 deuxièmes, 14 troisièmes, 10 quatrièmes, 18 cinquièmes.', '5 firsts, 14 seconds, 14 thirds, 10 fourths, 18 fifths.'), CLA + '#medoc-1855', LK_CLA)
H('mouton', 1, 'classif', ('Quel château a été promu premier cru en 1973 ?', 'Which château was promoted to First Growth in 1973?'),
  same('Mouton Rothschild'), [same('Lynch-Bages'), same('Palmer'), same('Pontet-Canet')],
  ('La seule modification majeure du classement de 1855.', 'The only major change to the 1855 classification.'), CLA + '#medoc-1855', LK_CLA)
H('haut-brion', 2, 'classif', ('Quel est le seul château classé en 1855 qui ne soit pas du Médoc ?', 'Which is the only château classified in 1855 that is not in the Médoc?'),
  same('Haut-Brion'), [same('Latour'), same('Margaux'), same('Lafite Rothschild')],
  ('Haut-Brion est à Pessac, dans les Graves (aujourd’hui Pessac-Léognan).', 'Haut-Brion is in Pessac, in the Graves (now Pessac-Léognan).'), CLA + '#medoc-1855', LK_CLA)
H('cantemerle', 3, 'classif', ('Quel château a été ajouté au classement de 1855… en 1856 ?', 'Which château was added to the 1855 classification… in 1856?'),
  same('Cantemerle'), [same('Belgrave'), same('Camensac'), same('La Lagune')], ('Cantemerle, cinquième cru, ajouté en 1856.', 'Cantemerle, fifth growth, added in 1856.'), CLA + '#medoc-1855', LK_CLA)
H('agc51', 2, 'classif', ('Combien de grands crus compte l’Alsace ?', 'How many grands crus are there in Alsace?'),
  same('51'), [same('17'), same('33'), same('7')], ('51 grands crus, dont Kaefferkopf, le dernier reconnu (2007).', '51 grands crus, the latest being Kaefferkopf (2007).'), CLA + '#alsace', LK_CLA)
H('cgc17', 2, 'classif', ('Combien de villages sont classés grands crus en Champagne ?', 'How many Champagne villages are rated grand cru?'),
  same('17'), [same('7'), same('42'), same('51')], ('17 grands crus et 42 premiers crus.', '17 grands crus and 42 premiers crus.'), CLA + '#champagne', LK_CLA)
H('bgc33', 2, 'classif', ('Combien d’AOC grands crus compte la Bourgogne ?', 'How many grand cru AOCs does Burgundy have?'),
  same('33'), [same('17'), same('51'), same('61')], ('Côte de Nuits, Côte de Beaune et Chablis (une AOC à 7 climats).', 'Côte de Nuits, Côte de Beaune and Chablis (one AOC with 7 climats).'), CLA + '#bourgogne', LK_CLA)
H('chablisgc', 2, 'classif', ('Combien de climats compte l’AOC Chablis Grand Cru ?', 'How many climats make up the Chablis Grand Cru AOC?'),
  same('7'), [same('3'), same('12'), same('40')], ('Blanchot, Bougros, Les Clos, Grenouilles, Preuses, Valmur, Vaudésir.', 'Blanchot, Bougros, Les Clos, Grenouilles, Preuses, Valmur, Vaudésir.'), CLA + '#bourgogne', LK_CLA)
H('moutonne', 3, 'classif', ('« La Moutonne », à Chablis, est…', '“La Moutonne”, in Chablis, is…'),
  ('Un monopole à cheval sur Vaudésir et Preuses, non classé comme climat', 'A monopole straddling Vaudésir and Preuses, not a classified climat'),
  [('Le 8<sup>e</sup> climat grand cru officiel', 'The 8th official grand cru climat'), ('Un premier cru de Fourchaume', 'A Fourchaume premier cru'), ('Une AOC à part entière', 'An AOC in its own right')],
  ('2,35 ha, ≈ 95 % Vaudésir + 5 % Preuses ; nom autorisé par l’INAO depuis 1952.', '2.35 ha, ≈ 95 % Vaudésir + 5 % Preuses; name allowed by the INAO since 1952.'), CLA + '#bourgogne', LK_CLA)
H('grande-rue', 3, 'classif', ('Quel est le plus récent grand cru de Bourgogne (1992) ?', 'Which is Burgundy’s most recent grand cru (1992)?'),
  same('La Grande Rue'), [same('Clos des Lambrays'), same('Clos de Tart'), same('La Romanée')], ('La Grande Rue, à Vosne-Romanée, promue en 1992.', 'La Grande Rue, in Vosne-Romanée, promoted in 1992.'), CLA + '#bourgogne', LK_CLA)
H('cb2025', 3, 'classif', ('Combien de châteaux compte le classement des Crus Bourgeois 2025 ?', 'How many châteaux are in the 2025 Crus Bourgeois classification?'),
  same('170'), [same('61'), same('249'), same('444')], ('170 crus, sur trois niveaux : Exceptionnels, Supérieurs et Crus Bourgeois.', '170 growths on three tiers: Exceptionnels, Supérieurs and Crus Bourgeois.'), CLA + '#crus-bourgeois', LK_CLA)
H('graves1959', 3, 'classif', ('Le classement des Graves date de…', 'The Graves classification dates from…'),
  same('1953 et 1959'), [same('1855'), same('1932'), same('2022')], ('Établi en 1953, complété en 1959 : 16 châteaux, rouges et/ou blancs.', 'Drawn up in 1953, completed in 1959: 16 châteaux, red and/or white.'), CLA + '#graves-1959', LK_CLA)

# quotations
H('q-musset', 2, 'quotes', ('Qui a écrit « Qu’importe le flacon, pourvu qu’on ait l’ivresse » ?', 'Who wrote “What matter the flask, so long as there is the intoxication”?'),
  same('Alfred de Musset'), [same('Charles Baudelaire'), same('Victor Hugo'), same('Paul Verlaine')], ('La Coupe et les Lèvres (1832).', 'La Coupe et les Lèvres (1832).'), QUO + '#s=Musset', LK_QUO)
H('q-baudelaire', 1, 'quotes', ('Qui a écrit « Il faut être toujours ivre […] De vin, de poésie ou de vertu » ?', 'Who wrote “One must always be drunk […] On wine, on poetry or on virtue”?'),
  same('Charles Baudelaire'), [same('François Rabelais'), same('Molière'), same('Voltaire')], ('« Enivrez-vous », Le Spleen de Paris.', '“Get Drunk”, Paris Spleen.'), QUO + '#s=Baudelaire', LK_QUO)
H('q-pasteur', 1, 'quotes', ('Quel savant a qualifié le vin de « plus saine, plus hygiénique des boissons » ?', 'Which scientist called wine “the most healthful, the most hygienic of beverages”?'),
  same('Louis Pasteur'), [same('Marie Curie'), same('Antoine Lavoisier'), same('Claude Bernard')], ('Études sur le vin (1866).', 'Studies on Wine (1866).'), QUO + '#s=Pasteur', LK_QUO)
H('q-pepys', 3, 'quotes', ('En 1663, Samuel Pepys note avoir bu un vin français appelé « Ho Bryan ». Lequel ?', 'In 1663, Samuel Pepys noted drinking a French wine called “Ho Bryan”. Which one?'),
  same('Haut-Brion'), [same('Yquem'), same('Romanée-Conti'), same('Hermitage')], ('Première mention écrite connue d’un cru bordelais nommé.', 'The first known written mention of a named Bordeaux growth.'), QUO + '#s=Pepys', LK_QUO)
H('q-perignon', 2, 'quotes', ('« Venez vite, je bois des étoiles ! », prêté à Dom Pérignon, est…', '“Come quickly, I am drinking the stars!”, credited to Dom Pérignon, is…'),
  ('Une invention publicitaire du XIX<sup>e</sup> siècle', 'A 19th-century advertising invention'),
  [('Une phrase de son journal', 'A line from his diary'), ('Une lettre au roi Louis XIV', 'A letter to Louis XIV'), ('Une devise de l’abbaye d’Hautvillers', 'The motto of Hautvillers abbey')],
  ('Dom Pérignon cherchait au contraire à éviter les bulles, alors considérées comme un défaut.', 'Dom Pérignon actually tried to avoid bubbles, then considered a fault.'), QUO + '#s=Perignon', LK_QUO)
H('q-stevenson', 2, 'quotes', ('Quel écrivain a dit du vin qu’il est « de la poésie en bouteille » ?', 'Which writer called wine “bottled poetry”?'),
  same('Robert Louis Stevenson'), [same('Oscar Wilde'), same('Ernest Hemingway'), same('Charles Dickens')], ('The Silverado Squatters (1883), à propos de la Napa Valley.', 'The Silverado Squatters (1883), about the Napa Valley.'), QUO + '#s=Stevenson', LK_QUO)
H('q-rabelais', 2, 'quotes', ('« Je bois pour la soif à venir » : de quel auteur ?', '“I drink for the thirst to come”: by which author?'),
  same('François Rabelais'), [same('Michel de Montaigne'), same('Molière'), same('Jean de La Fontaine')], ('Gargantua, chap. 5, « Les propos des bien ivres ».', 'Gargantua, ch. 5, “The talk of the drinkers”.'), QUO + '#s=Rabelais', LK_QUO)
H('q-veritas', 3, 'quotes', ('L’adage « in vino veritas » remonte au poète grec…', 'The saying “in vino veritas” goes back to the Greek poet…'),
  same('Alcée'), [same('Homère'), same('Sophocle'), same('Pindare')],
  ('« Le vin, cher enfant, et la vérité » (Alcée, v. 600 av. J.-C.), repris par Pline l’Ancien.', '“Wine, dear boy, and truth” (Alcaeus, c. 600 BC), taken up by Pliny the Elder.'), QUO + '#s=veritas', LK_QUO)
H('q-colette', 2, 'quotes', ('Qui a écrit que la vigne « nous rend intelligible ce qu’est la véritable saveur de la terre » ?', 'Who wrote that the vine “makes intelligible to us the true savour of the earth”?'),
  same('Colette'), [same('George Sand'), same('Marguerite Duras'), same('Simone de Beauvoir')], ('Prisons et paradis (1932).', 'Prisons et paradis (1932).'), QUO + '#s=Colette', LK_QUO)
H('q-virgil', 3, 'quotes', ('« Bacchus aime les collines ouvertes » : qui l’a écrit ?', '“Bacchus loves the open hills”: who wrote it?'),
  same('Virgile'), [same('Horace'), same('Ovide'), same('Catulle')], ('Géorgiques, II, 113.', 'Georgics, II, 113.'), QUO + '#s=Bacchus', LK_QUO)


# =================================================================================== Cognac & eaux-de-vie
# Sources: Cognac rulebook (AOC library, consolidated CDC of June 2026), « How brandy is made », Cognac crus map.
CDC_COG = '../AOC_Decree/decrees/charente_cognac_cognac_version_consolidee.pdf'
BRA = '../How%20it%27s%20made/How%20brandy%20is%20made.html'
MAPC = '../../Cognac.html'
LK_CDC_COG = ('Cahier des charges du Cognac', 'Cognac rulebook (in French)')
LK_BRA = ('Comment naît une eau-de-vie', 'How brandy is made')
LK_MAPC = ('Carte des crus de Cognac', 'Cognac crus map')


def C(id_, lv, q, a, d, x, href=CDC_COG, lk=LK_CDC_COG):
    add('cog-' + id_, lv, 'spirits', q, a, d, x, href, lk)


# ---- level 1
C('base', 1, ('Le Cognac est une eau-de-vie distillée à partir…', 'Cognac is a spirit distilled from…'),
  ('de vin blanc', 'white wine'), [('de cidre', 'cider'), ('de céréales', 'grain'), ('de jus de canne', 'sugar-cane juice')],
  ('« Eau-de-vie de vin issu de cépages blancs » (cahier des charges).', '“A wine spirit made from white grapes” (rulebook).'))
C('ugni', 1, ('Quel cépage représente près de 98 % du vignoble de Cognac ?', 'Which grape makes up nearly 98 % of the Cognac vineyard?'),
  same('Ugni blanc'), [same('Chardonnay'), same('Sauvignon blanc'), same('Merlot')],
  ('Productif, tardif, acide et peu sucré : l’idéal pour un vin de distillation.', 'Productive, late-ripening, acidic and low in sugar: ideal for a distilling wine.'))
C('alambic', 1, ('Comment s’appelle l’alambic du Cognac ?', 'What is the Cognac still called?'),
  ('L’alambic charentais', 'The alambic charentais (Charentais pot still)'),
  [('L’alambic armagnaçais', 'The alambic armagnaçais'), ('La colonne Coffey', 'The Coffey column still'), ('L’alambic à bain-marie', 'The bain-marie still')],
  ('Un alambic en cuivre chauffé à feu nu, travaillé par lots.', 'A copper pot still heated over a naked flame, worked in batches.'), BRA, LK_BRA)
C('twice', 1, ('Combien de fois le vin est-il distillé pour faire du Cognac ?', 'How many times is the wine distilled to make Cognac?'),
  same('2'), [same('1'), same('3'), same('4')],
  ('Double distillation « à repasse » : première chauffe (brouillis) puis bonne chauffe.', 'Double distillation “à repasse”: first heating (brouillis) then the bonne chauffe.'), BRA, LK_BRA)
C('anges', 1, ('Que désigne la « part des anges » ?', 'What is the “angels’ share”?'),
  ('L’eau-de-vie qui s’évapore à travers le fût', 'The spirit that evaporates through the cask'),
  [('La part réservée au maître de chai', 'The cellar master’s own share'), ('Le premier fût offert à l’église', 'The first cask given to the church'),
   ('La taxe payée sur chaque fût', 'The tax paid on each cask')],
  ('Chaque année, l’équivalent de plusieurs millions de bouteilles s’évapore des chais.', 'Each year the equivalent of several million bottles evaporates from the cellars.'))
C('vs', 1, ('Quel âge minimum a un cognac « VS » ?', 'What is the minimum age of a “VS” Cognac?'),
  same('2 ans'), [same('1 an'), same('3 ans'), same('4 ans')],
  ('Compte 2 : au moins deux ans sous bois de chêne (VS, ★★★, Sélection).', 'Count 2: at least two years in oak (VS, ★★★, Sélection).'))
C('xo', 1, ('Quel âge minimum a un cognac « XO » ?', 'What is the minimum age of an “XO” Cognac?'),
  same('10 ans'), [same('4 ans'), same('6 ans'), same('20 ans')],
  ('Compte 10 pour XO, Hors d’âge, Extra… ; 14 ans pour XXO.', 'Count 10 for XO, Hors d’âge, Extra…; 14 years for XXO.'))
C('oak', 1, ('Dans quel bois vieillit le Cognac ?', 'In which wood is Cognac aged?'),
  same('Le chêne'), [same('Le châtaignier'), same('L’acacia'), same('Le merisier')],
  ('Vieillissement exclusivement sous bois de chêne, sans interruption.', 'Ageing exclusively in oak, without interruption.'))
C('depts', 1, ('Dans quels départements se trouve l’essentiel du vignoble de Cognac ?', 'In which départements does most of the Cognac vineyard lie?'),
  ('Charente et Charente-Maritime', 'Charente and Charente-Maritime'),
  [('Gers et Landes', 'Gers and Landes'), ('Gironde et Lot-et-Garonne', 'Gironde and Lot-et-Garonne'), ('Vendée et Loire-Atlantique', 'Vendée and Loire-Atlantique')],
  ('Plus quelques communes de Dordogne et des Deux-Sèvres.', 'Plus a few communes in the Dordogne and Deux-Sèvres.'), MAPC, LK_MAPC)
C('armagnac', 1, ('Quelle eau-de-vie gasconne est le plus souvent distillée une seule fois, en continu ?', 'Which Gascon brandy is usually distilled only once, continuously?'),
  same('L’Armagnac'), [same('Le Calvados'), same('Le Cognac'), same('Le Kirsch')],
  ('L’alambic armagnaçais, à colonne, sort une eau-de-vie plus faible en alcool et plus rustique.', 'The column-type alambic armagnaçais yields a lower-strength, more rustic spirit.'), BRA, LK_BRA)
C('clear', 1, ('À la sortie de l’alambic, l’eau-de-vie de Cognac est…', 'Straight off the still, Cognac spirit is…'),
  ('Incolore', 'Colourless'), [('Ambrée', 'Amber'), ('Dorée', 'Golden'), ('Acajou', 'Mahogany')],
  ('C’est le chêne qui la colore : jaune pâle, or, ambre puis acajou pour les plus vieilles.', 'Oak gives the colour: pale yellow, gold, amber then mahogany for the oldest.'), BRA, LK_BRA)
C('bottle', 1, ('Un cognac continue-t-il de vieillir en bouteille ?', 'Does Cognac keep ageing in the bottle?'),
  ('Non, son âge est fixé à la sortie du fût', 'No, its age is fixed when it leaves the cask'),
  [('Oui, comme un grand vin', 'Yes, like a fine wine'), ('Oui, s’il est conservé couché', 'Yes, if stored lying down'), ('Seulement les XO', 'Only XOs do')],
  ('Contrairement au vin, une eau-de-vie ne vieillit plus en verre.', 'Unlike wine, a spirit no longer ages in glass.'), BRA, LK_BRA)
C('abroad', 1, ('Quelle part du Cognac est bue hors de France ?', 'How much Cognac is drunk outside France?'),
  ('Plus de 95 %', 'Over 95 %'), [('Environ 25 %', 'About 25 %'), ('Environ la moitié', 'About half'), ('Environ 75 %', 'About 75 %')],
  ('Exporté dans près de 160 pays.', 'Exported to nearly 160 countries.'))
C('abv', 1, ('Quel est le degré minimum d’un cognac mis en vente ?', 'What is the minimum strength of Cognac on sale?'),
  same('40 %'), [same('35 %'), same('45 %'), same('50 %')],
  ('40 % vol. minimum, obtenu par « réduction » avec de l’eau distillée ou des petites eaux.', '40 % ABV minimum, reached by “reduction” with distilled water or weak spirit.'))

# ---- level 2
C('vsop', 2, ('Quel âge minimum a un cognac « VSOP » ?', 'What is the minimum age of a “VSOP” Cognac?'),
  same('4 ans'), [same('2 ans'), same('6 ans'), same('10 ans')],
  ('Compte 4 : VSOP, Réserve, Vieux, Rare, Royal.', 'Count 4: VSOP, Réserve, Vieux, Rare, Royal.'))
C('vsop-name', 2, ('Que signifie le sigle « VSOP » ?', 'What does “VSOP” stand for?'),
  same('Very Superior Old Pale'), [same('Very Special Old Product'), same('Vintage Selected Old Pale'), same('Very Smooth Old Proof')],
  ('Mention anglaise héritée du commerce avec l’Angleterre, au compte 4.', 'An English term inherited from trade with Britain, count 4.'))
C('gc', 2, ('Quel cru de Cognac est le plus réputé ?', 'Which Cognac cru is the most prized?'),
  same('Grande Champagne'), [same('Fins Bois'), same('Bons Bois'), same('Borderies')],
  ('Grande finesse, bouquet floral, maturation lente : elle demande un long vieillissement.', 'Great finesse, floral bouquet, slow to mature: it needs long ageing.'))
C('fine', 2, ('Un cognac « Fine Champagne » est…', 'A “Fine Champagne” Cognac is…'),
  ('Un assemblage de Grande et Petite Champagne', 'A blend of Grande and Petite Champagne'),
  [('Un cognac élaboré dans la Marne', 'A Cognac made in the Marne'), ('Un cognac vieilli en fûts de champagne', 'A Cognac aged in Champagne casks'),
   ('Un assemblage de tous les crus', 'A blend of all the crus')],
  ('Au moins 50 % de Grande Champagne ; ce n’est pas un territoire mais un assemblage.', 'At least 50 % Grande Champagne; it is a blend, not a territory.'))
C('six', 2, ('Combien de crus (dénominations géographiques) compte le Cognac ?', 'How many crus (geographical names) does Cognac have?'),
  same('6'), [same('4'), same('5'), same('8')],
  ('Grande Champagne, Petite Champagne, Borderies, Fins Bois, Bons Bois, Bois ordinaires.', 'Grande Champagne, Petite Champagne, Borderies, Fins Bois, Bons Bois, Bois ordinaires.'), MAPC, LK_MAPC)
C('craie', 2, ('Sur quels sols poussent les vignes de Grande et Petite Champagne ?', 'What soils do the Grande and Petite Champagne vines grow on?'),
  ('Des sols crayeux', 'Chalky soils'), [('Des sables', 'Sands'), ('Du granite', 'Granite'), ('Des galets roulés', 'Rounded pebbles')],
  ('Argilo-calcaires peu profonds sur calcaire tendre et crayeux du Crétacé — d’où le nom « Champagne ».', 'Shallow clay-limestone over soft, chalky Cretaceous limestone — hence the name “Champagne”.'))
C('brouillis', 2, ('Comment s’appelle le produit trouble de la première distillation ?', 'What is the cloudy product of the first distillation called?'),
  same('Le brouillis'), [same('Le cœur'), same('Les queues'), same('Le rancio')],
  ('Environ 28–32 % vol., il est redistillé lors de la « bonne chauffe ».', 'About 28–32 % ABV, it is distilled again in the “bonne chauffe”.'), BRA, LK_BRA)
C('bonne', 2, ('Comment s’appelle la seconde distillation du Cognac ?', 'What is Cognac’s second distillation called?'),
  same('La bonne chauffe'), [same('La première chauffe'), same('La repasse froide'), same('La réduction')],
  ('C’est là que le distillateur fait la « coupe » et garde le cœur.', 'This is where the distiller makes the “cut” and keeps the heart.'), BRA, LK_BRA)
C('coupe', 2, ('Que fait le distillateur lors de la « coupe » ?', 'What does the distiller do at “the cut”?'),
  ('Il sépare têtes, cœur et queues', 'Separates heads, heart and tails'),
  [('Il ajoute de l’eau pour baisser le degré', 'Adds water to lower the strength'), ('Il assemble plusieurs crus', 'Blends several crus'),
   ('Il taille la vigne après les vendanges', 'Prunes the vines after harvest')],
  ('Seul le cœur va vieillir ; têtes et secondes sont recyclées dans les distillations suivantes.', 'Only the heart is aged; heads and seconds are recycled into later distillations.'), BRA, LK_BRA)
C('cuivre', 2, ('En quel métal est l’alambic charentais ?', 'What metal is the alambic charentais made of?'),
  same('Cuivre'), [same('Inox'), same('Fonte'), same('Laiton')],
  ('Chaudière, chapiteau, col-de-cygne et serpentin sont obligatoirement en cuivre, qui retient les composés soufrés.', 'Boiler, head, swan neck and coil must be copper, which removes sulphur compounds.'))
C('mars', 2, ('Avant quelle date la distillation doit-elle être achevée ?', 'By what date must distillation be finished?'),
  ('Le 31 mars suivant la récolte', '31 March after the harvest'),
  [('Le 31 décembre', '31 December'), ('Le 30 juin suivant la récolte', '30 June after the harvest'), ('Le 11 novembre', '11 November')],
  ('Pour ne pas laisser les vins, sans soufre, perdre leurs arômes.', 'So that the unsulphured wines do not lose their aromas.'))
C('wine', 2, ('Les vins destinés au Cognac sont plutôt…', 'The wines made for Cognac are rather…'),
  ('Peu alcoolisés et acides', 'Low in alcohol and acidic'),
  [('Riches et sucrés', 'Rich and sweet'), ('Tanniques et colorés', 'Tannic and deep-coloured'), ('Doux et peu acides', 'Soft and low in acid')],
  ('Entre 7 et 12 % vol. : l’acidité les conserve l’hiver, le faible degré concentre les arômes.', '7 to 12 % ABV: acidity keeps them over winter, low alcohol concentrates the aromas.'))
C('soufre', 2, ('Quel produit courant en vinification est interdit pendant la fermentation des vins de Cognac ?', 'Which common winemaking product is banned during fermentation of Cognac wines?'),
  ('Le soufre (SO₂)', 'Sulphur (SO₂)'), [('Les levures', 'Yeast'), ('Le pressoir pneumatique', 'The pneumatic press'), ('La cuve en inox', 'The stainless-steel tank')],
  ('Il augmenterait l’acétaldéhyde et passerait dans l’eau-de-vie.', 'It would raise acetaldehyde and carry through to the spirit.'))
C('brandwijn', 2, ('Le mot « brandy » vient du néerlandais « brandwijn », qui signifie…', 'The word “brandy” comes from the Dutch “brandwijn”, meaning…'),
  ('Vin brûlé', 'Burnt wine'), [('Vin de marque', 'Branded wine'), ('Vin du bord', 'Ship’s wine'), ('Vin de garde', 'Keeping wine')],
  ('Les Hollandais distillaient les vins charentais pour qu’ils supportent le voyage.', 'The Dutch distilled Charente wines so they would survive the voyage.'))
C('dutch', 2, ('Qui, au XVI<sup>e</sup> siècle, se met à distiller les vins de la Charente ?', 'Who began distilling Charente wines in the 16th century?'),
  same('Les Hollandais'), [same('Les Anglais'), same('Les Vénitiens'), same('Les moines de Cluny')],
  ('Venus chercher le sel de la côte, ils emportaient aussi les vins de Champagne et des Borderies.', 'Coming for salt from the coast, they also took the wines of Champagne and the Borderies.'))
C('trebbiano', 2, ('Sous quel nom l’ugni blanc est-il connu en Italie ?', 'Under which name is Ugni Blanc known in Italy?'),
  same('Trebbiano'), [same('Vermentino'), same('Malvasia'), same('Grechetto')],
  ('« Trebbiano Toscano » : en Charente, il est à la limite nord de sa maturité.', '“Trebbiano Toscano”: in the Charente it is at its northern ripening limit.'))
C('forets', 2, ('De quelles forêts vient traditionnellement le chêne des fûts de Cognac ?', 'Which forests traditionally supply the oak for Cognac casks?'),
  ('Limousin et Tronçais', 'Limousin and Tronçais'), [('Vosges et Jura', 'Vosges and Jura'), ('Landes et Gascogne', 'Landes and Gascony'), ('Ardennes et Argonne', 'Ardennes and Argonne')],
  ('Gros grain (Limousin) ou grain fin (Tronçais).', 'Wide grain (Limousin) or fine grain (Tronçais).'))
C('bnic', 2, ('Quel organisme interprofessionnel contrôle les comptes d’âge du Cognac ?', 'Which trade body controls Cognac’s age counts?'),
  same('Le BNIC'), [same('Le CIVC'), same('Le CIVB'), same('Le BIVB')],
  ('Bureau national interprofessionnel du Cognac, créé à la Libération en 1946.', 'Bureau National Interprofessionnel du Cognac, set up at the Liberation in 1946.'))
C('folle', 2, ('Lequel de ces cépages est autorisé pour le Cognac ?', 'Which of these grapes is allowed for Cognac?'),
  same('Folle blanche'), [same('Chardonnay'), same('Chenin'), same('Muscadelle')],
  ('Cépages principaux : colombard, folle blanche, montils, sémillon, ugni blanc.', 'Main grapes: Colombard, Folle Blanche, Montils, Sémillon, Ugni Blanc.'))
C('baco', 2, ('Quel cépage hybride caractérise l’Armagnac, mais pas le Cognac ?', 'Which hybrid grape is typical of Armagnac but not Cognac?'),
  same('Baco'), [same('Colombard'), same('Ugni blanc'), same('Folle blanche')],
  ('Le Baco donne à l’Armagnac son caractère plus rustique ; les trois autres servent aux deux.', 'Baco gives Armagnac its more rustic character; the other three are used for both.'), BRA, LK_BRA)
C('blanche', 2, ('Qu’est-ce que la « blanche d’Armagnac » ?', 'What is “blanche d’Armagnac”?'),
  ('Un armagnac non vieilli, incolore', 'An unaged, colourless Armagnac'),
  [('Un armagnac de raisins blancs', 'An Armagnac from white grapes'), ('Un armagnac coupé d’eau', 'An Armagnac cut with water'),
   ('Un vin blanc de Gascogne', 'A Gascon white wine')],
  ('Reposée en verre ou en inox, sans bois.', 'Rested in glass or steel, with no wood.'), BRA, LK_BRA)
C('marc', 2, ('À partir de quoi distille-t-on un marc ?', 'What is marc distilled from?'),
  ('Des peaux, pépins et rafles après pressurage', 'Skins, pips and stalks left after pressing'),
  [('De la lie des vins', 'Wine lees'), ('De raisins secs', 'Dried grapes'), ('Du vin blanc', 'White wine')],
  ('Marc de Bourgogne, de Champagne… La grappa italienne suit le même principe.', 'Marc de Bourgogne, de Champagne… Italian grappa is the same idea.'), BRA, LK_BRA)
C('pineau', 2, ('Quel vin de liqueur charentais est muté au cognac ?', 'Which Charente vin de liqueur is fortified with Cognac?'),
  same('Le Pineau des Charentes'), [same('Le Floc de Gascogne'), same('Le Macvin du Jura'), same('Le Pommeau de Normandie')],
  ('Moût de raisin muté avec du cognac rassis, dans la même aire.', 'Grape must fortified with matured Cognac, in the same area.'),
  cep_link('Pineau des Charentes'), LK_CEP)

# ---- level 3
C('fins', 3, ('Quel cru de Cognac représente le vignoble le plus vaste ?', 'Which Cognac cru is the largest vineyard?'),
  same('Fins Bois'), [same('Grande Champagne'), same('Borderies'), same('Petite Champagne')],
  ('Eaux-de-vie rondes et souples, au bouquet de raisin pressé, qui vieillissent assez vite.', 'Round, supple spirits with a pressed-grape bouquet that age fairly fast.'))
C('borderies', 3, ('Quel cru donne des eaux-de-vie rondes au parfum de violette ?', 'Which cru gives round spirits with a scent of violets?'),
  same('Borderies'), [same('Bons Bois'), same('Grande Champagne'), same('Fins Bois')],
  ('Le plus petit cru (6 communes), sur des sols argilo-siliceux à silex.', 'The smallest cru (6 communes), on flinty clay-silica soils.'))
C('cognac-ville', 3, ('La Charente partage la commune de Cognac entre deux crus. Lesquels ?', 'The Charente river splits the commune of Cognac between two crus. Which?'),
  ('Grande Champagne et Borderies', 'Grande Champagne and Borderies'),
  [('Petite Champagne et Fins Bois', 'Petite Champagne and Fins Bois'), ('Borderies et Fins Bois', 'Borderies and Fins Bois'),
   ('Grande et Petite Champagne', 'Grande and Petite Champagne')],
  ('Rive gauche en Grande Champagne, rive droite en Borderies.', 'Left bank in Grande Champagne, right bank in the Borderies.'), MAPC, LK_MAPC)
C('groies', 3, ('Comment appelle-t-on les sols rouges, caillouteux et argilo-calcaires des Fins Bois ?', 'What are the red, stony clay-limestone soils of the Fins Bois called?'),
  same('Les groies'), [same('Les aubues'), same('Les boulbènes'), same('Les terres blanches')],
  ('Sur un calcaire dur du Jurassique.', 'Over hard Jurassic limestone.'))
C('coquand', 3, ('Quel géologue a établi au XIX<sup>e</sup> siècle le classement des crus de Cognac ?', 'Which geologist drew up the Cognac crus classification in the 19th century?'),
  same('Henri Coquand'), [same('Jules Guyot'), same('Louis Pasteur'), same('Pierre Galet')],
  ('Avec un dégustateur, vers 1860 ; base du décret du 13 janvier 1938.', 'With a taster, around 1860; the basis for the decree of 13 January 1938.'))
C('1909', 3, ('En quelle année l’aire de production du Cognac a-t-elle été délimitée ?', 'In which year was the Cognac production area delimited?'),
  same('1909'), [same('1860'), same('1936'), same('1946')],
  ('1909 : l’aire ; 1936 : l’AOC ; 1938 : les crus.', '1909: the area; 1936: the AOC; 1938: the crus.'))
C('1938', 3, ('En quelle année les crus du Cognac ont-ils été délimités par décret ?', 'In which year were the Cognac crus delimited by decree?'),
  same('1938'), [same('1909'), same('1875'), same('1956')],
  ('Décret du 13 janvier 1938, d’après les travaux de Coquand.', 'Decree of 13 January 1938, based on Coquand’s work.'))
C('torula', 3, ('Quel champignon, nourri par la part des anges, noircit les murs des chais ?', 'Which fungus, fed by the angels’ share, blackens the cellar walls?'),
  same('Torula compniacensis'), [same('Botrytis cinerea'), same('Penicillium roqueforti'), same('Saccharomyces cerevisiae')],
  ('Il recouvre en les noircissant les pierres de la région.', 'It covers the local stone and turns it black.'))
C('napoleon', 3, ('La mention « Napoléon » impose un âge minimum de…', 'The term “Napoléon” requires a minimum age of…'),
  same('6 ans'), [same('4 ans'), same('10 ans'), same('20 ans')],
  ('Compte 6 : Napoléon, Très Vieille Réserve, Très Vieux, Héritage…', 'Count 6: Napoléon, Très Vieille Réserve, Très Vieux, Héritage…'))
C('xxo', 3, ('Quel âge minimum impose la mention « XXO » ?', 'What minimum age does “XXO” require?'),
  same('14 ans'), [same('10 ans'), same('12 ans'), same('20 ans')],
  ('XXO / Extra Extra Old : 14 ans au moins.', 'XXO / Extra Extra Old: at least 14 years.'))
C('esprit', 3, ('À quoi sert l’« Esprit de Cognac » ?', 'What is “Esprit de Cognac” used for?'),
  ('À préparer des vins mousseux', 'Making sparkling wines'),
  [('À compléter les fûts (ouillage)', 'Topping up the casks'), ('À nettoyer les alambics', 'Cleaning the stills'), ('À muter le Pineau', 'Fortifying Pineau')],
  ('Troisième distillation à 80–85 % vol., non vieillie, interdite à la consommation directe.', 'A third distillation at 80–85 % ABV, unaged, not for drinking as is.'))
C('737', 3, ('Quel degré maximum peut avoir l’eau-de-vie à la sortie de l’alambic ?', 'What is the maximum strength of the spirit off the still?'),
  same('73,7 %'), [same('60 %'), same('80 %'), same('96 %')],
  ('Ce faible degré garde les arômes du vin ; le cœur coule autour de 70 %.', 'This low strength keeps the wine’s aromas; the heart runs at about 70 %.'))
C('30hl', 3, ('Quelle capacité maximale a la chaudière d’un alambic charentais pour la bonne chauffe ?', 'What is the maximum boiler capacity of a Charentais still for the bonne chauffe?'),
  same('30 hl'), [same('10 hl'), same('60 hl'), same('140 hl')],
  ('30 hl pour une charge de 25 hl ; jusqu’à 140 hl admis seulement pour le brouillis.', '30 hl for a 25 hl charge; up to 140 hl allowed only for the brouillis.'))
C('feu', 3, ('Comment est chauffée la chaudière de l’alambic charentais ?', 'How is the boiler of the Charentais still heated?'),
  ('À feu nu', 'Over a naked flame'), [('À la vapeur', 'By steam'), ('Au bain-marie', 'In a bain-marie'), ('Par résistance électrique', 'By electric element')],
  ('Le contact du vin avec le fond chauffé crée des arômes supplémentaires.', 'Wine touching the heated base creates extra aromas.'))
C('rancio', 3, ('Comment appelle-t-on le bouquet des vieux cognacs (fruits confits, épices, tabac, fruits secs) ?', 'What is the bouquet of old Cognacs (candied fruit, spice, tobacco, dried fruit) called?'),
  ('Le rancio charentais', 'The rancio charentais'), [('La part des anges', 'The angels’ share'), ('Le brouillis', 'The brouillis'), ('La bonne chauffe', 'The bonne chauffe')],
  ('Terme repris par le cahier des charges (Flanzy, 1998).', 'A term used in the rulebook (Flanzy, 1998).'))
C('caramel', 3, ('Lequel de ces ajouts est autorisé pour la finition d’un cognac ?', 'Which of these additions is allowed when finishing a Cognac?'),
  ('Le caramel (E150a)', 'Caramel (E150a)'), [('Un arôme de vanille', 'Vanilla flavouring'), ('Du jus de raisin', 'Grape juice'), ('Du carmin de cochenille', 'Cochineal carmine')],
  ('Caramel, édulcoration et infusion de copeaux de chêne (« boisé ») sont admis, dans la limite de 4 % d’obscuration.', 'Caramel, sweetening and an oak-chip infusion (“boisé”) are allowed, up to 4 % obscuration.'))
C('semillon', 3, ('Lequel de ces cépages bordelais est autorisé pour le Cognac ?', 'Which of these Bordeaux grapes is allowed for Cognac?'),
  same('Sémillon'), [same('Sauvignon blanc'), same('Muscadelle'), same('Merlot')],
  ('Il figure parmi les cépages principaux, avec colombard, folle blanche, montils et ugni blanc.', 'It is one of the main grapes, with Colombard, Folle Blanche, Montils and Ugni Blanc.'))
C('phyllo', 3, ('Combien d’hectares comptait le vignoble charentais avant le phylloxéra ?', 'How large was the Charente vineyard before phylloxera?'),
  same('280 000 ha'), [same('75 000 ha'), same('150 000 ha'), same('500 000 ha')],
  ('Il n’en restait que 40 600 ha vers 1893 ; environ 75 000 ha aujourd’hui.', 'Only 40,600 ha remained around 1893; about 75,000 ha today.'))
C('martell', 3, ('Laquelle de ces maisons de Cognac est la plus ancienne ?', 'Which of these Cognac houses is the oldest?'),
  same('Martell'), [same('Hennessy'), same('Courvoisier'), same('Bisquit')],
  ('Martell 1715, Rémy Martin 1724, Hennessy 1765, Bisquit 1819, Courvoisier 1843.', 'Martell 1715, Rémy Martin 1724, Hennessy 1765, Bisquit 1819, Courvoisier 1843.'))
C('1860', 3, ('Quel événement de 1860 fait décoller les ventes de Cognac ?', 'Which 1860 event sent Cognac sales soaring?'),
  ('Le traité de commerce franco-anglais', 'The Anglo-French trade treaty'),
  [('L’arrivée du phylloxéra', 'The arrival of phylloxera'), ('L’invention de l’alambic charentais', 'The invention of the Charentais still'),
   ('Le premier classement des crus', 'The first classification of the crus')],
  ('Signé le 23 janvier 1860 sous Napoléon III ; apogée en 1879.', 'Signed on 23 January 1860 under Napoleon III; peak in 1879.'))
C('bois-ord', 3, ('Quel cru de Cognac est aussi appelé « Bois à terroirs » ?', 'Which Cognac cru is also called “Bois à terroirs”?'),
  same('Bois ordinaires'), [same('Bons Bois'), same('Fins Bois'), same('Borderies')],
  ('Sols surtout sableux, sur la côte et au sud du vignoble ; eaux-de-vie fruitées qui vieillissent vite.', 'Mostly sandy soils, on the coast and in the south; fruity spirits that age quickly.'))
C('petite', 3, ('Quel cru ressemble à la Grande Champagne mais mûrit plus vite ?', 'Which cru resembles Grande Champagne but matures faster?'),
  same('Petite Champagne'), [same('Fins Bois'), same('Bons Bois'), same('Borderies')],
  ('Mêmes caractères de finesse, qualité optimale après une maturation plus courte.', 'Same finesse, at its best after a shorter maturation.'))


def bank():
    return Q


if __name__ == '__main__':
    from collections import Counter
    print(len(Q), Counter(q['lv'] for q in Q))
    print(Counter((q['lv'], q['cat']) for q in Q))
