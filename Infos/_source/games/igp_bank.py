"""Question bank for game 5 « Au pays des IGP » / "Lost in the Pays" (Infos/Literature/IGP_Game.html).

Sources:
  - the site's IGP map (« Vignobles de France — Carte des IGP.html »: DATA = name, category, commune count;
    DETAIL = colours, styles, dénominations, INAO rulebook link);
  - the IGP rulebooks in « IGP of France/Cahiers des Charges/Vins » (zone, grapes, history, « lien à l'origine »),
    read once and cached in igp_cdc_cache.json; grape and dénomination claims are re-checked against them on build;
  - FACTS below (wine region + départements of each IGP, taken from the rulebooks' « zone géographique »).

Question types (cat): name (finish the name), region, dept, denom, grape, history, lien (trivia), size, spirit, igpaoc, categ.
A question: dict(id, lv, cat, q=(fr,en), o=[(fr,en)×4], a=index, fix=bool, x=(fr,en), href, lk) — same as cep_bank.
"""
import json
import random
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = HERE.parents[2]
ROOT = SITE.parent
INFOS = SITE / 'Infos'
sys.path.insert(0, str(INFOS / 'Vine_and_Vineyard' / 'Cepages' / '_source'))
from parse import parse_all  # noqa: E402

RNG = random.Random(1968)
MAP = '../../Vignobles de France — Carte des IGP.html'
LK_MAP = ('Carte des IGP', 'IGP map')
LK_CDC = ('Cahier des charges de l’IGP (INAO)', 'IGP rulebook (INAO, in French)')
ALL = ('Toutes ces réponses', 'All of the above')
NONE = ('Aucune de ces réponses', 'None of the above')

# ------------------------------------------------------------------ site map data
_html = (SITE / 'Vignobles de France — Carte des IGP.html').read_text()
_dec = json.JSONDecoder()
DATA = {a['name']: a for a in _dec.raw_decode(_html[_html.index('[', _html.index('const DATA=')):])[0]}
DETAIL = _dec.raw_decode(_html[_html.index('{', _html.index('const DETAIL=')):])[0]
WINE = sorted(n for n, a in DATA.items() if a['cat'] != 'spir')
SPIRIT = sorted(n for n, a in DATA.items() if a['cat'] == 'spir')
REGIONAL = sorted(n for n in WINE if DATA[n]['cat'] == 'reg')


def cdc_url(n):
    c = DETAIL.get(n, {}).get('cdc') or []
    return c[0]['url'] if c else None


# ------------------------------------------------------------------ rulebook texts (cached)
CDC_DIR = ROOT / 'IGP of France' / 'Cahiers des Charges' / 'Vins'
CACHE = HERE / 'igp_cdc_cache.json'
FILE = {'Cathare': 'Le Pays Cathare'}


def norm(s):
    s = unicodedata.normalize('NFD', s.replace('’', "'").lower())
    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


def load_cdc():
    if CACHE.exists():
        return json.loads(CACHE.read_text())
    import fitz
    out = {}
    for n in WINE:
        f = CDC_DIR / f'IGP - {FILE.get(n, n)}.pdf'
        if not f.exists():
            g = [p for p in CDC_DIR.glob('*.pdf') if norm(p.stem) == norm(f'IGP - {FILE.get(n, n)}')]
            if not g:
                continue
            f = g[0]
        t = re.sub(r'\s+', ' ', ' '.join(p.get_text() for p in fitz.open(f)))
        ks = [m.start() for m in re.finditer('Encépagement', t)]
        k = next((k for k in ks if 'cépage' in t[k:k + 400]), ks[-1] if ks else 0)
        end = min([e for e in (t.find('Rendement', k + 50), t.find('6 –', k + 50), t.find('6 -', k + 50)) if e > 0] or [k + 6000])
        out[n] = {'full': norm(t), 'encep': norm(t[k:end])}
    CACHE.write_text(json.dumps(out, ensure_ascii=False))
    return out


CDC = load_cdc()


def in_encep(igp, grape):
    return (' ' + norm(grape) + ' ') in (' ' + CDC[igp]['encep'] + ' ')


def in_cdc(igp, text):
    return norm(text) in CDC[igp]['full']


# ------------------------------------------------------------------ facts: wine region + départements (from each rulebook's zone)
B = {'lr': ('Languedoc-Roussillon', 'Languedoc-Roussillon'), 'so': ('Sud-Ouest', 'South-West'), 'bx': ('Bordeaux', 'Bordeaux'),
     'ch': ('Charentes', 'Charentes'), 'rh': ('Vallée du Rhône', 'Rhône Valley'), 'pr': ('Provence', 'Provence'),
     'co': ('Corse', 'Corsica'), 'bo': ('Bourgogne', 'Burgundy'), 'lo': ('Val de Loire & Centre', 'Loire Valley & Centre'),
     'sa': ('Savoie, Bugey & Dauphiné', 'Savoie, Bugey & Dauphiné'), 'ju': ('Jura & Franche-Comté', 'Jura & Franche-Comté'),
     'es': ('Champagne & Lorraine', 'Champagne & Lorraine'), 'idf': ('Île-de-France', 'Île-de-France'), 'al': ('Alsace', 'Alsace')}
CLASH = {('rh', 'pr'), ('pr', 'rh'), ('sa', 'rh'), ('rh', 'sa'), ('bx', 'ch'), ('ch', 'bx'), ('bx', 'so'), ('so', 'bx'),
         ('lo', 'bo'), ('bo', 'lo'), ('ju', 'bo'), ('bo', 'ju'), ('ch', 'so'), ('so', 'ch')}
F = {  # name: (regions, départements, ambiguous-region flag)
    'Agenais': ('so', ['Lot-et-Garonne']), 'Alpes-Maritimes': ('pr', ['Alpes-Maritimes']),
    'Alpes-de-Haute-Provence': ('pr', ['Alpes-de-Haute-Provence']), 'Alpilles': ('pr', ['Bouches-du-Rhône']),
    'Ardèche': ('rh', ['Ardèche', 'Gard']), 'Ariège': ('so', ['Ariège']), 'Atlantique': ('bx ch so', None),
    'Aude': ('lr', ['Aude']), 'Aveyron': ('so', ['Aveyron']), 'Charentais': ('ch', ['Charente', 'Charente-Maritime']),
    'Cathare': ('lr so', ['Aude', 'Ariège']), 'Cité de Carcassonne': ('lr', ['Aude']), 'Collines Rhodaniennes': ('rh', None),
    'Comté Tolosan': ('so', None), 'Comtés Rhodaniens': ('rh sa', None), "Coteaux d'Ensérune": ('lr', ['Hérault']),
    'Coteaux de Béziers': ('lr', ['Hérault']), 'Coteaux de Coiffy': ('es', ['Haute-Marne']), 'Coteaux de Glanes': ('so', ['Lot']),
    'Coteaux de Narbonne': ('lr', ['Aude']), 'Coteaux de Peyriac': ('lr', ['Aude', 'Hérault']), 'Coteaux de Tannay': ('lo', ['Nièvre'], 1),
    "Coteaux de l'Ain": ('sa', ['Ain']), "Coteaux de l'Auxois": ('bo', ["Côte-d'Or"]), 'Coteaux des Baronnies': ('rh', ['Drôme']),
    "Coteaux du Cher et de l'Arnon": ('lo', ['Cher', 'Indre']), 'Coteaux du Pont du Gard': ('lr', ['Gard']), 'Cévennes': ('lr', None),
    'Côte Vermeille': ('lr', ['Pyrénées-Orientales']), 'Côtes Catalanes': ('lr', ['Pyrénées-Orientales']),
    'Côtes de Gascogne': ('so', None), 'Côtes de Meuse': ('es', ['Meuse']), 'Côtes de Thau': ('lr', ['Hérault']),
    'Côtes de Thongue': ('lr', ['Hérault']), 'Côtes de la Charité': ('lo', ['Nièvre'], 1), 'Côtes du Lot': ('so', ['Lot']),
    'Côtes du Tarn': ('so', ['Tarn']), 'Drôme': ('rh', ['Drôme']), 'Franche-Comté': ('ju', None), 'Gard': ('lr', ['Gard']),
    'Gers': ('so', ['Gers']), "Haute Vallée de l'Aude": ('lr', ['Aude']), "Haute Vallée de l'Orb": ('lr', ['Hérault']),
    'Haute-Marne': ('es', ['Haute-Marne']), 'Haute-Vienne': ('so', ['Haute-Vienne'], 1), 'Hautes-Alpes': ('pr', ['Hautes-Alpes']),
    'Ile de Beauté': ('co', ['Corse-du-Sud', 'Haute-Corse']), 'Isère': ('sa', ['Isère']), 'Landes': ('so', ['Landes']),
    'Lavilledieu': ('so', ['Tarn-et-Garonne']), 'Lorraine': ('es', ['Meurthe-et-Moselle', 'Meuse', 'Moselle']),
    'Maures': ('pr', ['Var']), 'Mont Caume': ('pr', ['Var']), 'Méditerranée': ('rh pr co', None), "Pays d'Hérault": ('lr', ['Hérault']),
    "Pays d'Oc": ('lr', None), 'Pays de Brive': ('so', ['Corrèze']), 'Pays des Bouches-du-Rhône': ('pr', ['Bouches-du-Rhône']),
    'Puy-de-Dôme': ('lo', ['Puy-de-Dôme'], 1), 'Périgord': ('so', ['Dordogne']), 'Saint-Guilhem-le-Désert': ('lr', ['Hérault', 'Gard']),
    'Sainte-Marie-la-Blanche': ('bo', ["Côte-d'Or", 'Saône-et-Loire']), 'Saône-et-Loire': ('bo', ['Saône-et-Loire']),
    'Terres du Midi': ('lr', None), 'Thézac-Perricard': ('so', ['Lot-et-Garonne']), 'Urfé': ('lo', ['Loire'], 1),
    'Val de Loire': ('lo', None), 'Vallée du Paradis': ('lr', ['Aude']), 'Vallée du Torgan': ('lr', ['Aude']), 'Var': ('pr', ['Var']),
    'Vaucluse': ('rh', ['Vaucluse']), "Vicomté d'Aumelas": ('lr', ['Hérault']), 'Vin des Allobroges': ('sa', ['Savoie', 'Haute-Savoie', 'Ain']),
    'Yonne': ('bo', ['Yonne']), 'Île-de-France': ('idf', None),
}
assert set(F) == set(WINE), set(F) ^ set(WINE)
REG = {n: set(v[0].split()) for n, v in F.items()}
DEPS = {n: v[1] for n, v in F.items()}
AMB = {n for n, v in F.items() if len(v) > 2}
FAMOUS = {"Pays d'Oc", 'Côtes de Gascogne', 'Val de Loire', 'Méditerranée', 'Ile de Beauté', 'Charentais', 'Var', 'Vaucluse', 'Gard',
          'Aude', 'Côtes Catalanes', 'Alpilles', 'Périgord', 'Vin des Allobroges', 'Yonne', 'Comté Tolosan', 'Atlantique',
          'Île-de-France', 'Franche-Comté', 'Ardèche', 'Drôme', 'Landes', 'Gers', "Pays d'Hérault", 'Saône-et-Loire', 'Cévennes',
          'Terres du Midi', 'Pays des Bouches-du-Rhône', 'Coteaux du Pont du Gard', 'Cité de Carcassonne'}
DEP_POOL = {'lr': ['Aude', 'Hérault', 'Gard', 'Pyrénées-Orientales', 'Lozère'],
            'so': ['Lot', 'Lot-et-Garonne', 'Tarn', 'Tarn-et-Garonne', 'Gers', 'Landes', 'Aveyron', 'Dordogne', 'Corrèze', 'Ariège', 'Haute-Garonne'],
            'pr': ['Var', 'Bouches-du-Rhône', 'Vaucluse', 'Alpes-Maritimes', 'Alpes-de-Haute-Provence'],
            'bo': ["Côte-d'Or", 'Saône-et-Loire', 'Yonne', 'Nièvre'], 'es': ['Haute-Marne', 'Meuse', 'Aube', 'Marne', 'Vosges'],
            'rh': ['Drôme', 'Ardèche', 'Vaucluse', 'Gard'], 'lo': ['Loire', 'Nièvre', 'Cher', 'Allier', 'Puy-de-Dôme']}

AOC_NAMES = sorted(a['name'] for a in parse_all())
AOC_FAMOUS = ['Bordeaux', 'Chablis', 'Champagne', 'Sancerre', 'Châteauneuf-du-Pape', 'Médoc', 'Muscadet', 'Bandol', 'Cahors',
              'Beaujolais', 'Côtes du Rhône', 'Saint-Émilion', 'Pomerol', 'Vouvray', 'Chinon', 'Côtes de Provence', 'Madiran']


def same(x):
    return (x, x)


def ell(x):
    return '…' + x


def wr(r):
    return ', '.join(B[k][0] for k in sorted(r)), ', '.join(B[k][1] for k in sorted(r))


Q = []
IDS = set()


def add(id_, lv, cat, q, o, a, fix, x, href=MAP, lk=LK_MAP):
    assert id_ not in IDS, id_
    assert len(o) == 4 and len({t[0] for t in o}) == 4, (id_, o)
    IDS.add(id_)
    Q.append(dict(id=id_, lv=lv, cat=cat, q=q, o=o, a=a, fix=fix, x=x, href=href, lk=lk))


def H(id_, lv, cat, q, right, wrongs, x, igp=None, special=None):
    """hand-written question: right answer + 3 wrongs; special='all'|'none' → 3 items + special (right ones flagged)."""
    href, lk = (cdc_url(igp), LK_CDC) if igp and cdc_url(igp) else (MAP, LK_MAP)
    to = lambda t: t if isinstance(t, tuple) else same(t)  # noqa: E731
    if special is None:
        add(id_, lv, cat, q, [to(right)] + [to(w) for w in wrongs], 0, False, x, href, lk)
    else:
        items = [to(t) for t in wrongs]  # here wrongs = the 3 displayed items
        add(id_, lv, cat, q, items + [ALL if special[0] == 'all' else NONE], special[1], True, x, href, lk)


# ===================================================================================== 1) finish the name (hand)
def Nm(id_, lv, clue, start, right, wrongs, x, igp, whole=None):
    """« clue … <start>…? » with answers « …ending »."""
    H(f'name-{id_}', lv, 'name', (clue[0] + f' <b>{start[0]}…</b> ?', clue[1] + f' <b>{start[1]}…</b>?'),
      ell(right) if isinstance(right, str) else (ell(right[0]), ell(right[1])),
      [ell(w) if isinstance(w, str) else (ell(w[0]), ell(w[1])) for w in wrongs], x, igp)
    full = whole or (start[0] + right if isinstance(right, str) else start[0] + right[0])
    assert full in WINE or any(full == d or full.lower() == d.lower() for v in DETAIL.values() for d in v.get('denoms', [])) or whole == '*', full


s = same
# ---- level 1: one real ending, three silly ones
Nm('smlb', 1, ('Près de Beaune, la petite IGP de zone de la Côte-d’Or porte le nom d’un village :',
               'Near Beaune, the small “IGP de zone” of the Côte-d’Or is named after a village:'), s('Sainte-'),
   'Marie-la-Blanche', ['Bonne Mère de Dieu', 'Estèphe', 'Nitouche'],
   ('Sainte-Marie-la-Blanche : 18 communes de Côte-d’Or (plus une partie de Saint-Loup-Géanges en Saône-et-Loire), à moins de 10 km de Beaune. '
    'C’est l’une des deux IGP de zone de la Côte-d’Or, avec les Coteaux de l’Auxois — quant à Saint-Estèphe, c’est une AOC du Médoc.',
    'Sainte-Marie-la-Blanche: 18 communes of the Côte-d’Or (plus part of Saint-Loup-Géanges in Saône-et-Loire), less than 10 km from Beaune. '
    'It is one of the Côte-d’Or’s two “IGP de zone”, with Coteaux de l’Auxois — as for Saint-Estèphe, it is a Médoc AOC.'),
   'Sainte-Marie-la-Blanche')
Nm('oc', 1, ('La grande IGP régionale du Languedoc-Roussillon, star des vins de cépage :', 'Languedoc-Roussillon’s big regional IGP, star of varietal wines:'),
   s('Pays d’'), 'Oc', ['Ocre', 'Ohé-du-Bateau', 'Octobre'],
   ('Pays d’Oc : Aude, Gard, Hérault, Pyrénées-Orientales et 6 communes de Lozère ; vin de pays depuis 1987.',
    'Pays d’Oc: Aude, Gard, Hérault, Pyrénées-Orientales and 6 communes of the Lozère; a vin de pays since 1987.'), "Pays d'Oc", "Pays d'Oc")
Nm('gascogne', 1, ('Dans le Gers, l’IGP des blancs vifs au colombard :', 'In the Gers, the IGP of zesty colombard whites:'), s('Côtes de '),
   'Gascogne', ['Gasoil', 'Grand-Mère', 'Gaston Lagaffe'],
   ('Côtes de Gascogne : tout le Gers et quelques communes des Landes et du Lot-et-Garonne.',
    'Côtes de Gascogne: the whole Gers plus a few communes of the Landes and Lot-et-Garonne.'), 'Côtes de Gascogne')
Nm('beaute', 1, ('L’IGP qui couvre toute la Corse :', 'The IGP covering all of Corsica:'), s('Ile de '), 'Beauté', ['Pâques', 'Bonté', 'Ré-création'],
   ('« Ile de Beauté » : toutes les communes de Haute-Corse et de Corse-du-Sud.', '“Ile de Beauté” (Isle of Beauty): every commune of Haute-Corse and Corse-du-Sud.'),
   'Ile de Beauté')
Nm('allobroges', 1, ('L’IGP de la Savoie et de la Haute-Savoie, du nom d’un peuple gaulois :', 'The IGP of Savoie and Haute-Savoie, named after a Gallic tribe:'),
   s('Vin des '), 'Allobroges', ['Alligators', 'Hallebardes', 'Allô Maman'],
   ('Vin des Allobroges : Savoie, Haute-Savoie et le canton de Seyssel (Ain). D’abord « vin de pays d’Allobrogie » (1981).',
    'Vin des Allobroges: Savoie, Haute-Savoie and the Seyssel area (Ain). First recognised as “vin de pays d’Allobrogie” (1981).'), 'Vin des Allobroges')
Nm('tolosan', 1, ('La grande IGP régionale du Sud-Ouest, du nom de l’ancien comté de Toulouse :', 'The big regional IGP of the South-West, named after the old county of Toulouse:'),
   s('Comté '), 'Tolosan', ['Tolérant', 'Toboggan', 'Totoche'],
   ('Comté Tolosan : 12 départements du Sud-Ouest, de l’Ariège aux Pyrénées-Atlantiques.', 'Comté Tolosan: 12 départements of the South-West, from the Ariège to the Pyrénées-Atlantiques.'),
   'Comté Tolosan')
Nm('medit', 1, ('L’IGP régionale du quart sud-est de la France, de la Drôme à la Corse :', 'The regional IGP of south-east France, from the Drôme to Corsica:'),
   s('Méditer'), 'ranée', ['sur la vie', 'en silence', 'avant de boire'],
   ('Méditerranée : Provence, Alpes, Drôme, Ardèche, Corse et quelques communes de l’Isère, de la Loire et du Rhône.',
    'Méditerranée: Provence, the southern Alps, Drôme, Ardèche, Corsica and a few communes of the Isère, Loire and Rhône.'), 'Méditerranée')
Nm('valdeloire', 1, ('La grande IGP régionale qui suit le plus long fleuve de France sur 14 départements :', 'The big regional IGP following France’s longest river across 14 départements:'),
   s('Val de '), 'Loire', ['Loisirs', 'Lessive', 'Larmes'],
   ('Val de Loire : 14 départements du bassin de la Loire, du Massif central au Pays nantais.', 'Val de Loire: 14 départements of the Loire basin, from the Massif Central to the Pays Nantais.'),
   'Val de Loire')
Nm('vermeille', 1, ('Sur la côte de Banyuls et Collioure, le vignoble le plus méridional de France :', 'On the Banyuls and Collioure coast, France’s southernmost vineyard:'),
   s('Côte Ver'), 'meille', ['glas', 'sailles', 'rouillée'],
   ('Côte Vermeille : 4 communes — Banyuls-sur-Mer, Collioure, Cerbère et Port-Vendres.', 'Côte Vermeille: 4 communes — Banyuls-sur-Mer, Collioure, Cerbère and Port-Vendres.'),
   'Côte Vermeille')
Nm('pontdugard', 1, ('L’IGP gardoise qui doit son nom à un aqueduc romain :', 'The Gard IGP named after a Roman aqueduct:'), s('Coteaux du Pont du '), 'Gard',
   ['Diable', 'Grand Large', 'Rhum'],
   ('C’est le pont du Gard, au cœur de la zone, qui a donné son nom à l’IGP Coteaux du Pont du Gard.', 'The Pont du Gard, in the middle of the area, gave the Coteaux du Pont du Gard IGP its name.'),
   'Coteaux du Pont du Gard')
Nm('carcassonne', 1, ('L’IGP du cœur de l’Aude, au pied des remparts médiévaux :', 'The IGP at the heart of the Aude, below the medieval ramparts:'), s('Cité de '),
   'Carcassonne', ['la Peur', 'Carcasse', 'Caravane'],
   ('Cité de Carcassonne : entre Malepère, Cabardès, Minervois et Corbières.', 'Cité de Carcassonne: between Malepère, Cabardès, Minervois and Corbières.'), 'Cité de Carcassonne')
Nm('caume', 1, ('Dans le Var, entre Toulon et Saint-Cyr-sur-Mer, une IGP de 12 communes :', 'In the Var, between Toulon and Saint-Cyr-sur-Mer, a 12-commune IGP:'),
   s('Mont '), 'Caume', ['Calme', 'Chauve', 'Blanc-Sec'],
   ('Mont Caume : 12 communes du sud-ouest du Var, un cirque ouvert sur la mer à Saint-Cyr.', 'Mont Caume: 12 communes in the south-west of the Var, an amphitheatre opening onto the sea at Saint-Cyr.'),
   'Mont Caume')
Nm('brive', 1, ('En Corrèze, l’IGP du bassin de Brive :', 'In the Corrèze, the IGP of the Brive basin:'), s('Pays de '), 'Brive', ['Brie', 'Bribes', 'Rêve'],
   ('Pays de Brive : d’abord « vin de pays de la Corrèze » (1968).', 'Pays de Brive: first recognised as “vin de pays de la Corrèze” (1968).'), 'Pays de Brive')
Nm('paradis', 1, ('Au cœur des Corbières, une IGP de 12 communes au nom céleste :', 'In the heart of the Corbières, a 12-commune IGP with a heavenly name:'), s('Vallée du '),
   'Paradis', ['Purgatoire', 'Pastis', 'Parapluie'],
   ('Vallée du Paradis : 12 communes des Corbières, traversées par la Berre.', 'Vallée du Paradis: 12 communes of the Corbières, crossed by the river Berre.'), 'Vallée du Paradis')
Nm('guilhem', 1, ('Dans le nord de l’Hérault, au pied du Larzac, l’IGP d’un village médiéval :', 'In the north of the Hérault, below the Larzac, the IGP of a medieval village:'),
   s('Saint-Guilhem-le-'), 'Désert', ['Dessert', 'Déserteur', 'Désiré'],
   ('Saint-Guilhem-le-Désert, dominée par le mont Baudile et le pic Saint-Loup.', 'Saint-Guilhem-le-Désert, overlooked by Mont Baudile and the Pic Saint-Loup.'), 'Saint-Guilhem-le-Désert')
Nm('rhodaniennes', 1, ('L’IGP des coteaux du Rhône septentrional (Ardèche, Drôme, Isère, Loire, Rhône) :', 'The IGP of the northern Rhône slopes (Ardèche, Drôme, Isère, Loire, Rhône):'),
   s('Collines '), 'Rhodaniennes', ['Rhodésiennes', 'Rondouillardes', 'Radiophoniques'],
   ('Collines Rhodaniennes : vin de pays depuis 1981, sur les deux rives du Rhône septentrional.', 'Collines Rhodaniennes: a vin de pays since 1981, on both banks of the northern Rhône.'),
   'Collines Rhodaniennes')
Nm('midi', 1, ('La plus jeune IGP régionale du Languedoc, sur le « vignoble du Midi » :', 'Languedoc’s youngest regional IGP, on the “vineyard of the Midi”:'), s('Terres du '),
   'Midi', ['Milieu', 'Minuit', 'Mildiou'],
   ('Terres du Midi : Gard, Hérault, Aude, Pyrénées-Orientales et quelques communes de Lozère.', 'Terres du Midi: Gard, Hérault, Aude, Pyrénées-Orientales and a few communes of the Lozère.'),
   'Terres du Midi')
Nm('perricard', 1, ('Au nord-est du Lot-et-Garonne, sur la rive gauche du Lot :', 'In the north-east of Lot-et-Garonne, on the left bank of the Lot:'), s('Thézac-'),
   'Perricard', ['Pernod', 'Picard', 'Pétanque'],
   ('Thézac-Perricard : 6 communes, un « coin du causse » entre Quercy et vallée de la Garonne.', 'Thézac-Perricard: 6 communes, a “corner of the causse” between Quercy and the Garonne valley.'),
   'Thézac-Perricard')
Nm('coiffy', 1, ('En Haute-Marne, l’IGP du nom de deux villages (le Haut et le Bas) :', 'In the Haute-Marne, the IGP named after two villages (the Upper and the Lower):'),
   s('Coteaux de '), 'Coiffy', ['Coiffeur', 'Confit', 'Café'],
   ('Coiffy-le-Haut et Coiffy-le-Bas ont donné leur nom aux Coteaux de Coiffy.', 'Coiffy-le-Haut and Coiffy-le-Bas gave their name to Coteaux de Coiffy.'), 'Coteaux de Coiffy')
Nm('aumelas', 1, ('Entre Montpellier et Béziers, au nord de Sète :', 'Between Montpellier and Béziers, north of Sète:'), s('Vicomté d’'), 'Aumelas',
   ['Omelette', 'Aumônier', 'Au-Mélange'],
   ('Vicomté d’Aumelas : collines adossées au plateau d’Aumelas, au-dessus du fleuve Hérault.', 'Vicomté d’Aumelas: hills backing onto the Aumelas plateau, above the river Hérault.'),
   "Vicomté d'Aumelas", "Vicomté d'Aumelas")
Nm('enserune', 1, ('Entre Béziers et l’Aude, une IGP du nom d’un oppidum antique :', 'Between Béziers and the Aude, an IGP named after an ancient hill fort:'), s('Coteaux d’'),
   'Ensérune', ['En-Sérum', 'Encre-Rouge', 'Ensemble'],
   ('Coteaux d’Ensérune : la plaine languedocienne entre Béziers et l’Aude.', 'Coteaux d’Ensérune: the Languedoc plain between Béziers and the Aude.'),
   "Coteaux d'Ensérune", "Coteaux d'Ensérune")
Nm('thau', 1, ('Six communes au bord d’un étang célèbre pour ses huîtres :', 'Six communes on the shore of a lagoon famous for its oysters:'), s('Côtes de '), 'Thau',
   ['Tôt', 'Taupe', 'Thé'],
   ('Côtes de Thau : 6 communes au nord-est de l’étang de Thau.', 'Côtes de Thau: 6 communes on the north-east shore of the Étang de Thau.'), 'Côtes de Thau')
Nm('catalanes', 1, ('L’IGP des Pyrénées-Orientales, qui porte le nom de la Catalogne :', 'The IGP of the Pyrénées-Orientales, named after Catalonia:'), s('Côtes Cata'), 'lanes',
   ['combes', 'strophiques', 'plasme'],
   ('Côtes Catalanes : vin de pays depuis 1981, dans les Pyrénées-Orientales.', 'Côtes Catalanes: a vin de pays since 1981, in the Pyrénées-Orientales.'), 'Côtes Catalanes')
Nm('vilaine', 1, ('Treize communes du Tarn-et-Garonne, entre Garonne et Tarn :', 'Thirteen communes of the Tarn-et-Garonne, between the Garonne and the Tarn:'),
   s('Lavillé'), 'dieu', ['lumière', 'gale', 'basse'],
   ('Lavilledieu : 13 communes du Tarn-et-Garonne, vins rouges et rosés uniquement.', 'Lavilledieu: 13 communes of the Tarn-et-Garonne, red and rosé wines only.'),
   'Lavilledieu', '*')
Nm('orb', 1, ('Dans l’Hérault, l’IGP de la haute vallée d’un fleuve qui passe à Béziers :', 'In the Hérault, the IGP of the upper valley of the river that flows through Béziers:'),
   s('Haute Vallée de l’'), 'Orb', ['Orbite', 'Or Blanc', 'Orchestre'],
   ('Haute Vallée de l’Orb : 32 communes de l’Hérault (ne pas confondre avec la Haute Vallée de l’Aude).', 'Haute Vallée de l’Orb: 32 communes of the Hérault (not to be confused with the Haute Vallée de l’Aude).'),
   "Haute Vallée de l'Orb", "Haute Vallée de l'Orb")

# ---- level 2: real names in the trap answers — read the clue!
Nm('glanes', 2, ('Dans le Lot, une IGP réservée à sept communes :', 'In the Lot, an IGP reserved for seven communes:'), s('Coteaux de '), 'Glanes',
   ['Béziers', 'Coiffy', 'Narbonne'],
   ('Coteaux de Glanes : 7 communes du nord-est du Lot. Béziers (Hérault), Coiffy (Haute-Marne) et Narbonne (Aude) ont aussi leurs « Coteaux », mais ailleurs.',
    'Coteaux de Glanes: 7 communes in the north-east of the Lot. Béziers (Hérault), Coiffy (Haute-Marne) and Narbonne (Aude) have “Coteaux” IGPs too, elsewhere.'), 'Coteaux de Glanes')
Nm('peyriac', 2, ('Au cœur du Minervois, entre Aude et Hérault :', 'In the heart of the Minervois, straddling the Aude and the Hérault:'), s('Coteaux de '), 'Peyriac',
   ['Narbonne', 'Glanes', 'Tannay'],
   ('Coteaux de Peyriac : une trentaine de communes du Minervois (Aude et Hérault).', 'Coteaux de Peyriac: some thirty communes of the Minervois (Aude and Hérault).'), 'Coteaux de Peyriac')
Nm('thongue', 2, ('Autour de 23 villages entre Faugères, Pézenas et Béziers, le long d’un affluent de l’Hérault :', 'Around 23 villages between Faugères, Pézenas and Béziers, along a tributary of the Hérault:'),
   s('Côtes de '), 'Thongue', ['Thau', 'Gascogne', 'Meuse'],
   ('Côtes de Thongue : le bassin versant de la Thongue. Les Côtes de Thau, elles, bordent l’étang de Thau.', 'Côtes de Thongue: the basin of the river Thongue. Côtes de Thau lies by the Thau lagoon.'),
   'Côtes de Thongue')
Nm('charite', 2, ('Dans la Nièvre, une IGP de zone voisine de Pouilly-sur-Loire :', 'In the Nièvre, an “IGP de zone” next to Pouilly-sur-Loire:'), s('Côtes de la '), 'Charité',
   ['Malepère', 'Montagne Noire', 'Bonne Mère'],
   ('Côtes de la Charité (La Charité-sur-Loire), d’abord « coteaux charitois » (1986). La Malepère est une AOC de l’Aude.',
    'Côtes de la Charité (La Charité-sur-Loire), first called “coteaux charitois” (1986). Malepère is an AOC in the Aude.'), 'Côtes de la Charité')
Nm('arnon', 2, ('En Champagne berrichonne, près de Quincy et Reuilly : Coteaux du Cher et de l’…', 'In the Champagne berrichonne, near Quincy and Reuilly: Coteaux du Cher et de l’…'),
   ('Coteaux du Cher et de l’', 'Coteaux du Cher et de l’'), 'Arnon', ['Indre', 'Allier', 'Yèvre'],
   ('Coteaux du Cher et de l’Arnon : Cher et Indre, le long du Cher et de ses affluents l’Arnon et la Théols.', 'Coteaux du Cher et de l’Arnon: Cher and Indre, along the Cher and its tributaries the Arnon and the Théols.'),
   "Coteaux du Cher et de l'Arnon", "Coteaux du Cher et de l'Arnon")
Nm('hvaude', 2, ('Près de Limoux, l’IGP des vins frais de la haute vallée :', 'Near Limoux, the IGP of cool wines from the upper valley:'), s('Haute Vallée de l’'), 'Aude',
   ['Orb', 'Agly', 'Hérault'],
   ('Haute Vallée de l’Aude : 56 communes de l’Aude, avec des cépages « du Nord » (pinot noir, chardonnay…). La Haute Vallée de l’Orb, elle, est dans l’Hérault.',
    'Haute Vallée de l’Aude: 56 communes of the Aude, with “northern” grapes (pinot noir, chardonnay…). Haute Vallée de l’Orb is in the Hérault.'),
   "Haute Vallée de l'Aude", "Haute Vallée de l'Aude")
Nm('baronnies', 2, ('Dans la Drôme provençale, pays des olives de Nyons :', 'In the Drôme provençale, land of the Nyons olives:'), s('Coteaux des '), 'Baronnies',
   ['Dentelles', 'Alpilles', 'Monts d’Or'],
   ('Coteaux des Baronnies : 65 communes de la Drôme. Les Alpilles sont une IGP des Bouches-du-Rhône ; les Dentelles de Montmirail, un massif du Vaucluse.',
    'Coteaux des Baronnies: 65 communes of the Drôme. Alpilles is an IGP in the Bouches-du-Rhône; the Dentelles de Montmirail are hills in the Vaucluse.'),
   'Coteaux des Baronnies')
Nm('torgan', 2, ('Deux communes seulement, Tuchan et Paziols, au pied du mont Tauch :', 'Only two communes, Tuchan and Paziols, below Mont Tauch:'), s('Vallée du '), 'Torgan',
   ['Paradis', 'Tarn', 'Tech'],
   ('Vallée du Torgan : la plus petite IGP de la carte (2 communes). La Vallée du Paradis, voisine, en compte 12.',
    'Vallée du Torgan: the smallest IGP on the map (2 communes). Its neighbour Vallée du Paradis has 12.'), 'Vallée du Torgan')
Nm('cathare', 2, ('Toute l’Aude et 60 communes de l’Ariège :', 'The whole Aude plus 60 communes of the Ariège:'), s('Le Pays '), 'Cathare', ['Basque', 'Catalan', 'Cévenol'],
   ('IGP « Le Pays Cathare » (Cathare sur la carte), vin de pays depuis 2001.', '“Le Pays Cathare” IGP (Cathare on the map), a vin de pays since 2001.'), 'Cathare', '*')
Nm('auxois', 2, ('En Côte-d’Or, autour de Semur et Montbard :', 'In the Côte-d’Or, around Semur and Montbard:'), s('Coteaux de l’'), 'Auxois', ['Auxerrois', 'Ain', 'Arnon'],
   ('Coteaux de l’Auxois : 8 cantons de Côte-d’Or. L’auxerrois est un cépage (et le pays d’Auxerre, dans l’Yonne).',
    'Coteaux de l’Auxois: 8 cantons of the Côte-d’Or. Auxerrois is a grape (and the area around Auxerre, in the Yonne).'), "Coteaux de l'Auxois", "Coteaux de l'Auxois")
Nm('tannay', 2, ('Dans la Nièvre, une IGP de zone autour d’un bourg du Clamecycois :', 'In the Nièvre, an “IGP de zone” around a small town near Clamecy:'), s('Coteaux de '),
   'Tannay', ['Tonnerre', 'Tain', 'Tavel'],
   ('Coteaux de Tannay : vin de pays depuis 2001. Tonnerre est dans l’Yonne, Tain l’Hermitage dans la Drôme, Tavel dans le Gard.',
    'Coteaux de Tannay: a vin de pays since 2001. Tonnerre is in the Yonne, Tain l’Hermitage in the Drôme, Tavel in the Gard.'), 'Coteaux de Tannay')
Nm('rhodaniens', 2, ('L’IGP régionale de l’ancienne région Rhône-Alpes :', 'The regional IGP of the former Rhône-Alpes region:'), s('Comtés '), 'Rhodaniens',
   ['Tolosans', 'Provençaux', 'Lyonnais'],
   ('Comtés Rhodaniens : vin de pays depuis 1989. Le Comté Tolosan (au singulier) est l’IGP régionale du Sud-Ouest.',
    'Comtés Rhodaniens: a vin de pays since 1989. Comté Tolosan (singular) is the South-West’s regional IGP.'), 'Comtés Rhodaniens')
Nm('maures', 2, ('Dans le Var, 42 communes autour d’un massif cristallin, entre Toulon et Fréjus :', 'In the Var, 42 communes around a crystalline massif, between Toulon and Fréjus:'),
   s('IGP '), 'Maures', ['Estérel', 'Sainte-Baume', 'Alpilles'],
   ('Maures : avec le Tanneron et l’Estérel, le massif des Maures forme la Provence cristalline. Seules les Maures ont leur IGP.',
    'Maures: with the Tanneron and the Estérel, the Maures massif forms crystalline Provence. Only the Maures have their own IGP.'), 'Maures', '*')

# ---- level 3: smaller geographical units (dénominations)
def Dn(id_, lv, igp, clue, start, right, wrongs, x):
    Nm(f'denom-{id_}', lv, clue, start, right, wrongs, x, igp, '*')
    full = igp + ' ' + (right if isinstance(right, str) else right[0])
    end = start[0].split(igp)[-1] + (right if isinstance(right, str) else right[0])
    assert any(norm(d).endswith(norm(end)) for d in DETAIL[igp]['denoms']) or (igp in CDC and in_cdc(igp, end)), full


Dn('caux', 3, "Pays d'Hérault", ('L’IGP Pays d’Hérault a une unité géographique au nom… très normand :', 'The Pays d’Hérault IGP has a geographical unit with a very… Norman name:'),
   s('Pays d’Hérault Pays de '), 'Caux', ['Bray', 'Auge', 'Retz'],
   ('Pays de Caux est bien l’une des 16 unités géographiques de l’IGP Pays d’Hérault — rien à voir avec la Normandie ! (Le Pays de Retz est une dénomination du Val de Loire.)',
    'Pays de Caux really is one of the 16 geographical units of the Pays d’Hérault IGP — nothing to do with Normandy! (Pays de Retz is a Val de Loire unit.)'))
Dn('reve', 3, 'Aude', ('Parmi les unités géographiques de l’IGP Aude, la plus poétique :', 'Among the Aude IGP’s geographical units, the most poetic:'), s('Aude La côte '),
   'rêvée', ['sauvage', 'd’Azur', 'vermeille'],
   ('« La côte rêvée » est l’une des 9 unités géographiques de l’IGP Aude. La Côte Vermeille est une IGP à part, dans les Pyrénées-Orientales.',
    '“La côte rêvée” (the dreamt-of coast) is one of the Aude IGP’s 9 geographical units. Côte Vermeille is a separate IGP in the Pyrénées-Orientales.'))
Dn('provins', 3, 'Île-de-France', ('Une unité géographique de l’IGP Île-de-France, cité médiévale des roses :', 'A geographical unit of the Île-de-France IGP, the medieval city of roses:'),
   s('Île-de-France Coteaux de '), 'Provins', ['Montmartre', 'Meudon', 'Argenteuil'],
   ('Unités de l’IGP Île-de-France : Coteaux de Blunay, Coteaux de Provins, Coteaux de Suresnes-Mont-Valérien, Guérard et… Paris.',
    'Île-de-France IGP units: Coteaux de Blunay, Coteaux de Provins, Coteaux de Suresnes-Mont-Valérien, Guérard and… Paris.'))
Dn('orange', 2, 'Vaucluse', ('L’IGP Vaucluse peut porter le nom d’une ancienne principauté :', 'The Vaucluse IGP may carry the name of a former principality:'),
   s('Vaucluse Principauté d’'), 'Orange', ['Monaco', 'Andorre', 'Avignon'],
   ('« Principauté d’Orange » et « Aigues » sont les deux unités géographiques de l’IGP Vaucluse.', '“Principauté d’Orange” and “Aigues” are the Vaucluse IGP’s two geographical units.'))
Dn('rocamadour', 2, 'Côtes du Lot', ('L’IGP Côtes du Lot a une unité géographique au nom d’un célèbre lieu de pèlerinage :', 'The Côtes du Lot IGP has a geographical unit named after a famous pilgrimage site:'),
   s('Côtes du Lot '), 'Rocamadour', ['Conques', 'Lourdes', 'Cahors'],
   ('Côtes du Lot Rocamadour. Cahors, lui, est une AOC.', 'Côtes du Lot Rocamadour. Cahors is an AOC.'))
Dn('camargue', 2, 'Pays des Bouches-du-Rhône', ('L’unité géographique de l’IGP Pays des Bouches-du-Rhône, pays des taureaux et des flamants :', 'The geographical unit of the Pays des Bouches-du-Rhône IGP, land of bulls and flamingos:'),
   s('Pays des Bouches-du-Rhône Terre de '), 'Camargue', ['Crau', 'Provence', 'Sel'],
   ('Pays des Bouches-du-Rhône Terre de Camargue.', 'Pays des Bouches-du-Rhône Terre de Camargue.'))
Dn('agde', 3, 'Côtes de Thau', ('L’unité géographique des Côtes de Thau, au bord de la Méditerranée :', 'The Côtes de Thau unit, on the Mediterranean shore:'), s('Côtes de Thau Cap d’'),
   'Agde', ['Antibes', 'Ail', 'Erquy'],
   ('Côtes de Thau Cap d’Agde.', 'Côtes de Thau Cap d’Agde.'))
Dn('oleron', 2, 'Charentais', ('Outre l’île de Ré, l’IGP Charentais a une autre île parmi ses unités géographiques :', 'Besides the Île de Ré, the Charentais IGP has another island among its units:'),
   s('Charentais Ile d’'), 'Oléron', ['Yeu', 'Ouessant', 'Aix'],
   ('Unités de l’IGP Charentais : Charente, Charente-Maritime, Ile d’Oléron, Ile de Ré et Saint-Sornin.', 'Charentais IGP units: Charente, Charente-Maritime, Ile d’Oléron, Ile de Ré and Saint-Sornin.'))
Dn('ocean', 3, 'Landes', ('Une des quatre unités géographiques de l’IGP Landes :', 'One of the Landes IGP’s four geographical units:'), s('Landes Sables de l’'), 'Océan',
   ['Estuaire', 'Adour', 'Olonne'],
   ('Unités de l’IGP Landes : Coteaux de Chalosse, Côtes de l’Adour, Sables de l’Océan et Sables fauves.', 'Landes IGP units: Coteaux de Chalosse, Côtes de l’Adour, Sables de l’Océan and Sables fauves.'))
Dn('gex', 3, "Coteaux de l'Ain", ('L’unité géographique des Coteaux de l’Ain voisine de Genève :', 'The Coteaux de l’Ain unit next to Geneva:'), s('Coteaux de l’Ain Pays de '), 'Gex',
   ['Vaud', 'Gruyère', 'Faucigny'],
   ('Unités des Coteaux de l’Ain : Pays de Gex, Revermont, Val de Saône et Valromey.', 'Coteaux de l’Ain units: Pays de Gex, Revermont, Val de Saône and Valromey.'))
Dn('balmes', 3, 'Isère', ('Une unité géographique de l’IGP Isère :', 'A geographical unit of the Isère IGP:'), s('Isère Balmes '), 'dauphinoises',
   ['savoyardes', 'lyonnaises', 'alpines'],
   ('Unités de l’IGP Isère : Balmes dauphinoises, Coteaux du Grésivaudan et Trièves.', 'Isère IGP units: Balmes dauphinoises, Coteaux du Grésivaudan and Trièves.'))
Dn('baume', 2, 'Var', ('L’IGP Var a une unité géographique au nom d’un massif provençal :', 'The Var IGP has a unit named after a Provençal mountain range:'), s('Var Sainte-'), 'Baume',
   ['Victoire', 'Maxime', 'Anne'],
   ('Unités de l’IGP Var : Argens, Correns, Coteaux du Verdon et Sainte-Baume. « Sainte-Victoire » est une dénomination de l’AOC Côtes de Provence.',
    'Var IGP units: Argens, Correns, Coteaux du Verdon and Sainte-Baume. “Sainte-Victoire” belongs to the Côtes de Provence AOC.'))
Dn('aniane', 3, 'Saint-Guilhem-le-Désert', ('Une unité géographique de Saint-Guilhem-le-Désert :', 'A geographical unit of Saint-Guilhem-le-Désert:'), s('Saint-Guilhem-le-Désert '),
   'Aniane', ['Aigues-Mortes', 'Agde', 'Alès'],
   ('Unités de Saint-Guilhem-le-Désert : Aniane (« Cité d’Aniane » sur la carte) et Val de Montferrand.', 'Saint-Guilhem-le-Désert units: Aniane (“Cité d’Aniane” on the map) and Val de Montferrand.'))
Dn('doree', 3, "Vicomté d'Aumelas", ('L’unique unité géographique de la Vicomté d’Aumelas :', 'The one geographical unit of Vicomté d’Aumelas:'), s('Vicomté d’Aumelas Vallée '),
   ('Dorée', 'Dorée'), ['Heureuse', 'Verte', 'Blanche'], ('Vicomté d’Aumelas Vallée Dorée.', 'Vicomté d’Aumelas Vallée Dorée (golden valley).'))
Dn('badens', 3, 'Coteaux de Peyriac', ('L’unité géographique des Coteaux de Peyriac :', 'The Coteaux de Peyriac geographical unit:'), s('Coteaux de Peyriac Hauts de '), 'Badens',
   ['Bages', 'Bize', 'Bram'], ('Coteaux de Peyriac Hauts de Badens (d’après le cahier des charges).', 'Coteaux de Peyriac Hauts de Badens (per the rulebook).'))
Dn('rochelle', 3, 'Charentais', ('L’unité géographique de l’IGP Charentais qui porte le nom d’une commune :', 'The Charentais IGP unit named after a single commune:'), s('Charentais Saint-'),
   'Sornin', ['Émilion', 'Tropez', 'Georges'], ('Charentais Saint-Sornin.', 'Charentais Saint-Sornin.'))
Dn('ambierle', 3, 'Urfé', ('L’IGP Urfé a une unité géographique réservée au rosé :', 'The Urfé IGP has a geographical unit reserved for rosé:'), s('Urfé '), 'Ambierle rosé',
   ['Roanne rosé', 'Forez rosé', 'Madeleine rosé'], ('Unités de l’IGP Urfé : Ambierle (rosé) et Trelins.', 'Urfé IGP units: Ambierle (rosé) and Trelins.'))
Dn('cucugnan', 2, 'Aude', ('Une unité géographique de l’IGP Aude, village rendu célèbre par le curé d’Alphonse Daudet :', 'An Aude IGP unit, the village made famous by Alphonse Daudet’s priest:'),
   s('Aude Pays de '), 'Cucugnan', ['Tarascon', 'Fontvieille', 'Maillane'],
   ('Aude Pays de Cucugnan. « Le Curé de Cucugnan » est un conte des Lettres de mon moulin.', 'Aude Pays de Cucugnan. “The Priest of Cucugnan” is one of Daudet’s Letters from my Windmill.'))
Dn('paris', 1, 'Île-de-France', ('L’IGP Île-de-France a même une unité géographique au nom de sa capitale :', 'The Île-de-France IGP even has a geographical unit named after the capital:'),
   s('Île-de-France '), 'Paris', ['Pigalle', 'Plage', 'Saint-Germain'],
   ('Oui : « Paris » est une unité géographique de l’IGP Île-de-France (vignes de Montmartre, Belleville…).', 'Yes: “Paris” is a geographical unit of the Île-de-France IGP (vines at Montmartre, Belleville…).'))

# ===================================================================================== 2) history (hand, from the rulebooks)
H('hist-1968', 2, 'history', ('Les premiers vins de pays départementaux (Aude, Gard, Var, Yonne…) datent du décret du 13 septembre…', 'The first departmental vins de pays (Aude, Gard, Var, Yonne…) date from the decree of 13 September…'),
  '1968', ['1936', '1973', '1990'],
  ('Décret n° 68-807 du 13 septembre 1968, cité par les cahiers des charges de l’Aude, de l’Ardèche, du Var, de la Drôme…',
   'Decree no. 68-807 of 13 September 1968, cited in the rulebooks of Aude, Ardèche, Var, Drôme…'), 'Aude')
H('hist-vdp', 1, 'history', ('Avant la réforme européenne de 2009, comment appelait-on les IGP ?', 'Before the 2009 EU reform, what were IGPs called?'),
  ('Vins de pays', 'Vins de pays'), [('Vins de table', 'Table wines'), ('VDQS', 'VDQS'), ('Vins de garde', 'Vins de garde')],
  ('Chaque cahier des charges d’IGP rappelle qu’elle a été « initialement reconnue vin de pays ».', 'Every IGP rulebook recalls that it was “initially recognised as a vin de pays”.'))
H('hist-libron', 3, 'history', ('L’IGP Coteaux de Béziers s’appelait d’abord « vin de pays des Coteaux du… » ?', 'The Coteaux de Béziers IGP was first called “vin de pays des Coteaux du…”?'),
  ell('Libron'), [ell('Lez'), ell('Vidourle'), ell('Salagou')],
  ('Reconnue en 1982 sous le nom de Coteaux du Libron (un petit fleuve côtier de Béziers).', 'Recognised in 1982 as Coteaux du Libron (a small coastal river near Béziers).'), 'Coteaux de Béziers')
H('hist-allobrogie', 2, 'history', ('En 1981, le Vin des Allobroges est né sous le nom de vin de pays d’… ?', 'In 1981, Vin des Allobroges was born as the vin de pays d’…?'),
  ell('Allobrogie'), [ell('Arpitanie'), ell('Helvétie'), ell('Aquitaine')],
  ('Vin de pays d’Allobrogie, décret du 16 janvier 1981.', 'Vin de pays d’Allobrogie, decree of 16 January 1981.'), 'Vin des Allobroges')
H('hist-charitois', 3, 'history', ('Les Côtes de la Charité ont été reconnues en 1986 sous le nom de « vins de pays des coteaux… » ?', 'Côtes de la Charité was recognised in 1986 as “vins de pays des coteaux…”?'),
  ell('charitois'), [ell('nivernais'), ell('ligériens'), ell('berrichons')],
  ('« Vins de pays des coteaux charitois », décret du 22 janvier 1986.', '“Vins de pays des coteaux charitois”, decree of 22 January 1986.'), 'Côtes de la Charité')
H('hist-vdqs', 3, 'history', ('Avant d’être une IGP, Lavilledieu était depuis 1954… ?', 'Before becoming an IGP, Lavilledieu had been, since 1954…?'),
  ('un VDQS', 'a VDQS'), [('une AOC', 'an AOC'), ('un vin de table', 'a table wine'), ('un vin de liqueur', 'a vin de liqueur')],
  ('Lavilledieu fut reconnu « appellation d’origine vin délimité de qualité supérieure » par l’arrêté du 22 janvier 1954.',
   'Lavilledieu was recognised as a VDQS (“vin délimité de qualité supérieure”) by the order of 22 January 1954.'), 'Lavilledieu')
H('hist-oc', 3, 'history', ('En quelle année le vin de pays d’Oc a-t-il été reconnu ?', 'In which year was the vin de pays d’Oc recognised?'),
  '1987', ['1968', '1999', '2009'], ('Décret du 15 octobre 1987.', 'Decree of 15 October 1987.'), "Pays d'Oc")
H('hist-vdl', 3, 'history', ('Le vin de pays du Val de Loire a été reconnu en… ?', 'The vin de pays du Val de Loire was recognised in…?'),
  '2007', ['1968', '1987', '1995'], ('Décret n° 2007-820 du 11 mai 2007.', 'Decree no. 2007-820 of 11 May 2007.'), 'Val de Loire')
H('hist-correze', 2, 'history', ('L’IGP Pays de Brive était d’abord le vin de pays de la… ?', 'The Pays de Brive IGP was first the vin de pays de la…?'),
  ell('Corrèze'), [ell('Dordogne'), ell('Vézère'), ell('Creuse')], ('Vin de pays de la Corrèze, décret de 1968.', 'Vin de pays de la Corrèze, 1968 decree.'), 'Pays de Brive')
H('hist-2006', 3, 'history', ('Alpilles et Atlantique ont été reconnus vins de pays par le même décret, le 18 octobre…', 'Alpilles and Atlantique were recognised as vins de pays by the same decree, on 18 October…'),
  '2006', ['1981', '1996', '2011'], ('Décret du 18 octobre 2006 pour les deux.', 'Decree of 18 October 2006 for both.'), 'Atlantique')
H('hist-medit', 3, 'history', ('Le vin de pays de Méditerranée a été reconnu en… ?', 'The vin de pays de Méditerranée was recognised in…?'),
  '1999', ['1968', '1987', '2006'], ('Décret du 22 octobre 1999.', 'Decree of 22 October 1999.'), 'Méditerranée')
H('hist-cathare', 3, 'history', ('Le vin de pays Cathare a été reconnu en… ?', 'The Cathare vin de pays was recognised in…?'), '2001', ['1968', '1982', '2015'],
  ('Décret du 25 avril 2001.', 'Decree of 25 April 2001.'), 'Cathare')
H('hist-landes', 3, 'history', ('Avant de fusionner dans l’IGP Landes, un vin de pays portait le nom de « terroirs… » ?', 'Before merging into the Landes IGP, one vin de pays was called “terroirs…”?'),
  ell('landais'), [ell('gascons'), ell('basques'), ell('girondins')],
  ('Vin de pays des terroirs landais (1986) et vin de pays des Landes (1968).', 'Vin de pays des terroirs landais (1986) and vin de pays des Landes (1968).'), 'Landes')

# ===================================================================================== 3) trivia from the « lien à l'origine »
H('lien-lorraine-name', 2, 'lien', ('D’après son cahier des charges, d’où vient le nom « Lorraine » ?', 'According to its rulebook, where does the name “Lorraine” come from?'),
  ('De Lothaire II, roi de Lotharingie', 'From Lothair II, king of Lotharingia'),
  [('De la quiche', 'From the quiche'), ('De Charlemagne', 'From Charlemagne'), ('De Louis XIV', 'From Louis XIV')],
  ('« Le nom Lorraine, hérité de Lothaire II de Lotharingie, son premier roi. »', '“The name Lorraine, inherited from Lothair II of Lotharingia, its first king.”'), 'Lorraine')
H('lien-lorraine-mousseux', 2, 'lien', ('L’IGP Lorraine (Meurthe-et-Moselle, Meuse, Moselle) est réservée aux… ?', 'The Lorraine IGP (Meurthe-et-Moselle, Meuse, Moselle) is reserved for…?'),
  ('Vins mousseux de qualité', 'Quality sparkling wines'), [('Vins gris', 'Vins gris'), ('Vins de paille', 'Straw wines'), ('Vins doux naturels', 'Vins doux naturels')],
  ('« L’IGP Lorraine est un vin mousseux de qualité. » Les gris de Toul relèvent de l’AOC Côtes de Toul.', '“The Lorraine IGP is a quality sparkling wine.” The famous Toul gris belongs to the Côtes de Toul AOC.'), 'Lorraine')
H('lien-urfe', 2, 'lien', ('L’IGP Urfé est le vignoble le plus en amont de quel fleuve ?', 'The Urfé IGP is the furthest-upstream vineyard of which river?'),
  'Loire', ['Rhône', 'Garonne', 'Seine'], ('« C’est le vignoble le plus en amont de ce fleuve », la Loire, dans le département du même nom.', '“It is the furthest-upstream vineyard of this river”, the Loire, in the département of the same name.'), 'Urfé')
H('lien-tolosan-12', 2, 'lien', ('Sur combien de départements s’étend l’IGP Comté Tolosan ?', 'How many départements does the Comté Tolosan IGP cover?'), '12', ['4', '7', '21'],
  ('Ariège, Aveyron, Cantal, Gers, Haute-Garonne, Hautes-Pyrénées, Landes, Lot, Lot-et-Garonne, Pyrénées-Atlantiques, Tarn et Tarn-et-Garonne.',
   'Ariège, Aveyron, Cantal, Gers, Haute-Garonne, Hautes-Pyrénées, Landes, Lot, Lot-et-Garonne, Pyrénées-Atlantiques, Tarn and Tarn-et-Garonne.'), 'Comté Tolosan')
H('lien-vdl-14', 2, 'lien', ('Sur combien de départements s’étend l’IGP Val de Loire ?', 'How many départements does the Val de Loire IGP cover?'), '14', ['5', '9', '27'],
  ('« La zone géographique de l’IGP Val de Loire s’étend sur 14 départements du bassin hydrographique de la Loire. »', '“The Val de Loire IGP area covers 14 départements of the Loire basin.”'), 'Val de Loire')
H('lien-oc-lozere', 3, 'lien', ('Pays d’Oc couvre l’Aude, le Gard, l’Hérault et les Pyrénées-Orientales… plus 6 communes de quel département ?', 'Pays d’Oc covers the Aude, Gard, Hérault and Pyrénées-Orientales… plus 6 communes of which département?'),
  'Lozère', ['Ardèche', 'Tarn', 'Aveyron'], ('Ispagnac, Montbrun, Quézac, Sainte-Enimie, La Malène et Les Vignes, en Lozère.', 'Ispagnac, Montbrun, Quézac, Sainte-Enimie, La Malène and Les Vignes, in the Lozère.'), "Pays d'Oc")
H('lien-cathare-ariege', 3, 'lien', ('L’IGP Le Pays Cathare couvre toute l’Aude et 60 communes de quel département ?', 'Le Pays Cathare IGP covers the whole Aude and 60 communes of which département?'),
  'Ariège', ['Hérault', 'Pyrénées-Orientales', 'Tarn'], ('« L’ensemble du département de l’Aude et 60 communes du département de l’Ariège. »', '“The whole Aude département and 60 communes of the Ariège.”'), 'Cathare')
H('lien-vermeille-odd', 2, 'lien', ('Laquelle de ces communes ne fait PAS partie de l’IGP Côte Vermeille ?', 'Which of these communes is NOT part of the Côte Vermeille IGP?'),
  'Perpignan', ['Banyuls-sur-Mer', 'Collioure', 'Port-Vendres'], ('Les 4 communes : Banyuls-sur-Mer, Collioure, Cerbère et Port-Vendres.', 'The 4 communes: Banyuls-sur-Mer, Collioure, Cerbère and Port-Vendres.'), 'Côte Vermeille')
H('lien-lido', 2, 'lien', ('Aux Côtes de Thau, l’étang est séparé de la mer par un cordon de sable cultivé en vignes, appelé… ?', 'At Côtes de Thau, the lagoon is cut off from the sea by a sand bar planted with vines, called…?'),
  ('le lido', 'the lido'), [('le polder', 'the polder'), ('la calanque', 'the calanque'), ('le fjord', 'the fjord')],
  ('« L’étang de Thau est protégé de la Méditerranée par un cordon lagunaire appelé lido et cultivé en vignes. »', '“The Thau lagoon is protected from the sea by a sand bar called the lido, planted with vines.”'), 'Côtes de Thau')
H('lien-baudile', 2, 'lien', ('Deux montagnes calcaires dominent Saint-Guilhem-le-Désert : le mont Baudile et… ?', 'Two limestone mountains overlook Saint-Guilhem-le-Désert: Mont Baudile and…?'),
  ('le pic Saint-Loup', 'the Pic Saint-Loup'), [('le mont Ventoux', 'Mont Ventoux'), ('le Canigou', 'the Canigou'), ('la Sainte-Victoire', 'the Sainte-Victoire')],
  ('Le mont Baudile à l’ouest, le pic Saint-Loup à l’est.', 'Mont Baudile to the west, the Pic Saint-Loup to the east.'), 'Saint-Guilhem-le-Désert')
H('lien-tauch', 3, 'lien', ('La Vallée du Torgan s’étend au pied de quelle montagne (917 m) ?', 'The Vallée du Torgan lies below which mountain (917 m)?'),
  ('la montagne du Tauch', 'the Montagne du Tauch'), [('le pic de Nore', 'the Pic de Nore'), ('le Canigou', 'the Canigou'), ('le mont Aigoual', 'Mont Aigoual')],
  ('Tuchan et Paziols, « au pied de la montagne du Tauch qui culmine à 917 mètres ».', 'Tuchan and Paziols, “below the Montagne du Tauch, 917 metres high”.'), 'Vallée du Torgan')
H('lien-berre', 3, 'lien', ('Quelle rivière traverse le vignoble de la Vallée du Paradis ?', 'Which river runs through the Vallée du Paradis vineyard?'), 'Berre', ['Orbieu', 'Agly', 'Aude'],
  ('« La Berre, rivière principale qui traverse ce vignoble. »', '“The Berre, the main river crossing this vineyard.”'), 'Vallée du Paradis')
H('lien-puechs', 3, 'lien', ('Aux Côtes de Thongue (et d’Ensérune), comment appelle-t-on localement les petites collines ?', 'In Côtes de Thongue (and Ensérune), what are the little hills called locally?'),
  ('des puechs', 'puechs'), [('des terrils', 'terrils'), ('des buttes-témoins', 'buttes'), ('des drumlins', 'drumlins')],
  ('« L’enchaînement de petites collines, appelées localement “puechs”. »', '“The succession of small hills, locally called ‘puechs’.”'), 'Côtes de Thongue')
H('lien-stremy', 2, 'lien', ('Quelle commune célèbre est au centre de l’IGP Alpilles ?', 'Which famous commune lies at the centre of the Alpilles IGP?'),
  'Saint-Rémy-de-Provence', ['Aix-en-Provence', 'Cassis', 'Gordes'],
  ('« Avec en son centre la commune de Saint-Rémy-de-Provence, à la renommée internationale. »', '“With at its centre the commune of Saint-Rémy-de-Provence, internationally renowned.”'), 'Alpilles')
H('lien-solenzara', 3, 'lien', ('En Corse, l’essentiel de l’IGP Ile de Beauté vient de la côte orientale, de Bastia jusqu’à… ?', 'In Corsica, most Ile de Beauté IGP wine comes from the east coast, from Bastia down to…?'),
  'Solenzara', ['Ajaccio', 'Calvi', 'Bonifacio'], ('« De Bastia jusqu’à Solenzara, sur toute la façade maritime orientale. »', '“From Bastia to Solenzara, along the whole eastern seaboard.”'), 'Ile de Beauté')
H('lien-esterel', 3, 'lien', ('Avec les Maures et le Tanneron, quel massif forme la « Provence cristalline » ?', 'Along with the Maures and the Tanneron, which range forms “crystalline Provence”?'),
  ('l’Estérel', 'the Estérel'), [('la Sainte-Baume', 'the Sainte-Baume'), ('le Luberon', 'the Luberon'), ('les Alpilles', 'the Alpilles')],
  ('« Le massif cristallin des Maures, composante essentielle, avec le Tanneron et l’Estérel, de la Provence cristalline. »', '“The crystalline Maures massif, with the Tanneron and the Estérel, the core of crystalline Provence.”'), 'Maures')
H('lien-atlantique', 2, 'lien', ('D’où vient le nom de l’IGP Atlantique ?', 'Where does the Atlantique IGP get its name?'),
  ('De l’océan qui longe la zone sur 250 km', 'From the ocean running along the area for 250 km'),
  [('D’un paquebot', 'From an ocean liner'), ('D’une ancienne province', 'From a former province'), ('D’un cépage', 'From a grape')],
  ('« Le nom est lié à la proximité de l’Océan Atlantique, qui longe l’aire à l’ouest sur 250 kilomètres. »', '“The name comes from the Atlantic Ocean, which runs along the area for 250 km.”'), 'Atlantique')
H('lien-alsace', 2, 'lien', ('Laquelle de ces régions viticoles n’a AUCUNE IGP de vin sur la carte ?', 'Which of these wine regions has NO wine IGP on the map?'),
  'Alsace', ['Provence', 'Bourgogne', 'Corse'],
  ('Aucune IGP de vin ne couvre le Bas-Rhin ni le Haut-Rhin ; l’Alsace n’a qu’une IGP de spiritueux, le Marc d’Alsace.',
   'No wine IGP covers the Bas-Rhin or Haut-Rhin; Alsace only has a spirit IGP, Marc d’Alsace.'))
H('lien-paris', 1, 'lien', ('Laquelle de ces villes est une unité géographique de l’IGP Île-de-France ?', 'Which of these cities is a geographical unit of the Île-de-France IGP?'),
  'Paris', ['Lyon', 'Marseille', 'Lille'], ('Oui, « Île-de-France Paris » existe !', 'Yes, “Île-de-France Paris” exists!'), 'Île-de-France')
H('lien-lavilledieu-col', 2, 'lien', ('L’IGP Lavilledieu ne produit que… ?', 'The Lavilledieu IGP only makes…?'),
  ('des rouges et des rosés', 'reds and rosés'), [('des blancs', 'whites'), ('des effervescents', 'sparkling wines'), ('des vins doux', 'sweet wines')],
  ('Lavilledieu : rouge et rosé uniquement (négrette, tannat, syrah, gamay, cabernet franc ; fer et milgranet en accessoires).',
   'Lavilledieu: red and rosé only (négrette, tannat, syrah, gamay, cabernet franc; fer and milgranet as accessory grapes).'), 'Lavilledieu')
H('lien-surlie', 3, 'lien', ('Quelle IGP peut porter la mention « sur lie » ?', 'Which IGP may carry the “sur lie” mention?'), "Pays d'Oc", ['Var', 'Yonne', 'Comté Tolosan'],
  ('Sur la carte des IGP, seule l’IGP Pays d’Oc mentionne le style « sur lie » (plus connu pour le Muscadet).', 'On the IGP map only Pays d’Oc lists the “sur lie” style (better known from Muscadet).'), "Pays d'Oc")
H('lien-1968-big', 1, 'lien', ('IGP, IGP… que signifient ces trois lettres ?', 'IGP, IGP… what do these three letters stand for?'),
  ('Indication géographique protégée', 'Protected geographical indication'),
  [('Interprofession des grands pinards', 'Interprofession of great plonk'), ('Inspection générale des pressoirs', 'General inspectorate of wine presses'),
   ('Institut du goût populaire', 'Institute of popular taste')],
  ('Indication géographique protégée (en anglais PGI) : un lien au terroir moins strict que l’AOP.', 'Indication géographique protégée (PGI in English): a looser link to place than the AOP/PDO.'))

# ===================================================================================== 4) grapes (hand, checked against the rulebook grape lists)
GR = []


def G(id_, lv, igp, q, right, wrongs, x, special=None, rights=()):
    for r in ([right] if right else []) + list(rights):
        assert in_encep(igp, r), (id_, igp, r)
    for w in (wrongs if special is None else []):
        assert not in_encep(igp, w), (id_, igp, w)
    GR.append(id_)
    H(f'grape-{id_}', lv, 'grape', q, right, wrongs, x, igp, special)


G('yonne-cesar', 2, 'Yonne', ('Quel vieux cépage bourguignon est autorisé dans l’IGP Yonne rouge ?', 'Which old Burgundy grape is allowed in red Yonne IGP?'), 'César',
  ['Mondeuse', 'Négrette', 'Tannat'], ('Yonne rouge : césar, gamay, pinot noir et tressot.', 'Red Yonne: césar, gamay, pinot noir and tressot.'))
G('yonne-tressot', 3, 'Yonne', ('L’IGP Yonne rouge autorise un cépage presque disparu :', 'Red Yonne IGP allows an almost-vanished grape:'), 'Tressot',
  ['Milgranet', 'Ségalin', 'Persan'], ('Yonne rouge : césar, gamay, pinot noir et tressot.', 'Red Yonne: césar, gamay, pinot noir and tressot.'))
G('lorraine-piwi', 2, 'Lorraine', ('Quel cépage résistant aux maladies entre dans l’IGP Lorraine ?', 'Which disease-resistant grape goes into the Lorraine IGP?'), 'Solaris',
  ['Mourvèdre', 'Grenache', 'Carignan'],
  ('Lorraine : notamment johanniter, muscaris, solaris, souvignier gris, cabernet cortis, pinotin — des variétés résistantes.',
   'Lorraine: among others johanniter, muscaris, solaris, souvignier gris, cabernet cortis, pinotin — disease-resistant varieties.'))
G('lavilledieu-negrette', 2, 'Lavilledieu', ('Quel cépage principal de Fronton se retrouve à Lavilledieu ?', 'Which main Fronton grape is also found at Lavilledieu?'), 'Négrette',
  ['Mondeuse', 'Poulsard', 'Nielluccio'], ('Principaux : cabernet franc, gamay, négrette, syrah, tannat.', 'Main grapes: cabernet franc, gamay, négrette, syrah, tannat.'))
G('lavilledieu-milgranet', 3, 'Lavilledieu', ('Quel cépage accessoire, très rare, est autorisé à Lavilledieu ?', 'Which very rare accessory grape is allowed at Lavilledieu?'), 'Milgranet',
  ['Persan', 'Biancu Gentile', 'Tressot'], ('Accessoires : fer et milgranet.', 'Accessory grapes: fer and milgranet.'))
G('isere-verdesse', 3, 'Isère', ('Quel vieux cépage blanc dauphinois est autorisé dans l’IGP Isère ?', 'Which old white Dauphiné grape is allowed in the Isère IGP?'), 'Verdesse',
  ['Carcajolo blanc', 'Codivarta', 'Ondenc'], ('Blancs : altesse, arvine, chardonnay, jacquère, verdesse, viognier… Rouges : étraire de la Dui, persan, servanin, joubertin…',
                                              'Whites: altesse, arvine, chardonnay, jacquère, verdesse, viognier… Reds: étraire de la Dui, persan, servanin, joubertin…'))
G('isere-etraire', 3, 'Isère', ('Quel cépage rouge au nom pittoresque est autorisé en IGP Isère ?', 'Which red grape with a picturesque name is allowed in the Isère IGP?'), 'Etraire de la Dui',
  ['Brun Fourca', 'Mérille', 'Valdiguié'], ('Rouges de l’Isère : étraire de la Dui, joubertin, mècle, persan, servanin, mondeuse…', 'Isère reds: étraire de la Dui, joubertin, mècle, persan, servanin, mondeuse…'))
G('beaute-biancu', 2, 'Ile de Beauté', ('Quel cépage blanc corse est autorisé en IGP Ile de Beauté ?', 'Which white Corsican grape is allowed in the Ile de Beauté IGP?'), 'Biancu gentile',
  ['Gringet', 'Tressot', 'Jacquère'], ('Ile de Beauté : biancu gentile, brustianu, carcajolo, codivarta, genovèse…', 'Ile de Beauté: biancu gentile, brustianu, carcajolo, codivarta, genovèse…'))
G('allobroges-gringet', 3, 'Vin des Allobroges', ('Quel cépage blanc, emblème d’Ayze, est autorisé en Vin des Allobroges ?', 'Which white grape, the emblem of Ayze, is allowed in Vin des Allobroges?'),
  'Gringet', ['Biancu gentile', 'Mauzac', 'Tourbat'], ('Blancs : altesse, chasselas, gringet, jacquère, molette, mondeuse blanche…', 'Whites: altesse, chasselas, gringet, jacquère, molette, mondeuse blanche…'))
G('idf-meslier', 3, 'Île-de-France', ('Quel ancien cépage blanc du Bassin parisien est autorisé en IGP Île-de-France ?', 'Which old white grape of the Paris basin is allowed in the Île-de-France IGP?'),
  'Meslier Saint-François', ['Biancu gentile', 'Codivarta', 'Rolle'], ('Notamment : arbane, meslier saint-François, petit meslier, goldriesling, knipperlé, muscat cendré…',
                                                                      'Including: arbane, meslier saint-François, petit meslier, goldriesling, knipperlé, muscat cendré…'))
G('glanes-segalin', 3, 'Coteaux de Glanes', ('Quel cépage rouge local est autorisé aux Coteaux de Glanes ?', 'Which local red grape is allowed in Coteaux de Glanes?'), 'Ségalin',
  ['Milgranet', 'Persan', 'César'], ('Rouges : abouriou, castets, fer, jurançon noir, mérille, ségalin, valdiguié, gamay, merlot…', 'Reds: abouriou, castets, fer, jurançon noir, mérille, ségalin, valdiguié, gamay, merlot…'))
G('gascogne-colombard', 1, 'Côtes de Gascogne', ('Quel cépage blanc fait la réputation des Côtes de Gascogne ?', 'Which white grape made Côtes de Gascogne famous?'), 'Colombard',
  ['Riesling', 'Savagnin', 'Jacquère'], ('Blancs : colombard, ugni blanc, gros et petit manseng, sauvignon… (et pas de riesling).', 'Whites: colombard, ugni blanc, gros and petit manseng, sauvignon… (and no riesling).'))
G('aveyron-fer', 2, 'Aveyron', ('Quel cépage, star de Marcillac, est un cépage principal de l’IGP Aveyron ?', 'Which grape, star of Marcillac, is a main grape of the Aveyron IGP?'), 'Fer servadou',
  ['Mondeuse', 'Poulsard', 'Nielluccio'], ('Principaux rouges : cabernet sauvignon, duras, fer servadou, merlot, syrah.', 'Main reds: cabernet sauvignon, duras, fer servadou, merlot, syrah.'))
G('fc-poulsard', 2, 'Franche-Comté', ('Quel cépage jurassien est autorisé en IGP Franche-Comté ?', 'Which Jura grape is allowed in the Franche-Comté IGP?'), 'Poulsard',
  ['Négrette', 'Tannat', 'Nielluccio'], ('Rouges : pinot noir, gamay, meunier, poulsard, trousseau, gamaret, merlot, syrah.', 'Reds: pinot noir, gamay, meunier, poulsard, trousseau, gamaret, merlot, syrah.'))
G('hva-pinot', 3, "Haute Vallée de l'Aude", ('Quel cépage « septentrional » est autorisé en Haute Vallée de l’Aude rouge… à la différence du carignan ?', 'Which “northern” grape is allowed in red Haute Vallée de l’Aude… unlike carignan?'),
  'Pinot noir', ['Carignan', 'Mourvèdre', 'Grenache'], ('Rouges : cabernets, cot, merlot, meunier, pinot gris, pinot noir, syrah — ni carignan, ni grenache, ni mourvèdre.',
                                                       'Reds: cabernets, cot, merlot, meunier, pinot gris, pinot noir, syrah — no carignan, grenache or mourvèdre.'))
G('smlb-melon', 3, 'Sainte-Marie-la-Blanche', ('Quel cépage, célèbre à Nantes, est autorisé en Sainte-Marie-la-Blanche blanc ?', 'Which grape, famous around Nantes, is allowed in white Sainte-Marie-la-Blanche?'),
  'Melon', ['Riesling', 'Sylvaner', 'Viognier'], ('Blancs : aligoté, auxerrois, chardonnay, melon, pinot blanc, pinot gris.', 'Whites: aligoté, auxerrois, chardonnay, melon, pinot blanc, pinot gris.'))
G('coiffy-meslier', 3, 'Coteaux de Coiffy', ('Quel cépage champenois rare est autorisé aux Coteaux de Coiffy ?', 'Which rare Champagne grape is allowed in Coteaux de Coiffy?'), 'Petit meslier',
  ['Tressot', 'Savagnin', 'Poulsard'], ('Coiffy : pinot noir, gamay, meunier, chardonnay, arbane, petit meslier, auxerrois…', 'Coiffy: pinot noir, gamay, meunier, chardonnay, arbane, petit meslier, auxerrois…'))
G('charite-sauv', 2, 'Côtes de la Charité', ('Comme à Pouilly voisin, quel cépage blanc est autorisé aux Côtes de la Charité ?', 'As in nearby Pouilly, which white grape is allowed in Côtes de la Charité?'),
  'Sauvignon', ['Chenin', 'Viognier', 'Riesling'], ('Blancs : sauvignon, chardonnay, pinot blanc, pinot gris.', 'Whites: sauvignon, chardonnay, pinot blanc, pinot gris.'))
G('oc-all', 1, "Pays d'Oc", ('Quel cépage est autorisé en IGP Pays d’Oc ?', 'Which grape is allowed in the Pays d’Oc IGP?'), None,
  ['Chardonnay', 'Merlot', 'Syrah'], ('Les trois — Pays d’Oc autorise plus de 50 cépages.', 'All three — Pays d’Oc allows more than 50 grapes.'), ('all', 3), rights=['Chardonnay', 'Merlot', 'Syrah'])
G('urfe-all', 3, 'Urfé', ('Quel cépage rouge est un cépage principal de l’IGP Urfé ?', 'Which red grape is a main grape of the Urfé IGP?'), None,
  ['Gamay', 'Syrah', 'Pinot noir'], ('Les trois : gamay, syrah et pinot noir.', 'All three: gamay, syrah and pinot noir.'), ('all', 3), rights=['Gamay', 'Syrah', 'Pinot noir'])
G('auxois-none', 2, "Coteaux de l'Auxois", ('Quel cépage est autorisé en Coteaux de l’Auxois rouge ?', 'Which grape is allowed in red Coteaux de l’Auxois?'), None,
  ['Mourvèdre', 'Tannat', 'Carignan'], ('Aucun : en rouge, césar, gamaret, gamay, merlot et pinot noir.', 'None: reds are césar, gamaret, gamay, merlot and pinot noir.'), ('none', 3))
for w in ['Mourvèdre', 'Tannat', 'Carignan']:
    assert not in_encep("Coteaux de l'Auxois", w)
G('tannay-none', 3, 'Coteaux de Tannay', ('Quel cépage est autorisé aux Coteaux de Tannay ?', 'Which grape is allowed in Coteaux de Tannay?'), None,
  ['Sauvignon', 'Syrah', 'Chenin'], ('Aucun : gamays, pinot noir, pinot gris, auxerrois, chardonnay, melon et pinot blanc.', 'None: gamays, pinot noir, pinot gris, auxerrois, chardonnay, melon and pinot blanc.'), ('none', 3))
for w in ['Sauvignon', 'Syrah', 'Chenin']:
    assert not in_encep('Coteaux de Tannay', w)
H('grape-ile-de-re', 2, 'grape', ('Dans l’IGP Charentais, le tannat n’est autorisé que sur… ?', 'In the Charentais IGP, tannat is only allowed on…?'),
  ('l’île de Ré', 'the Île de Ré'), [('l’île d’Oléron', 'the Île d’Oléron'), ('l’île d’Aix', 'the Île d’Aix'), ('l’île Madame', 'the Île Madame')],
  ('« Tannat N (pour l’île de Ré uniquement). »', '“Tannat N (for the Île de Ré only).”'), 'Charentais')
assert 'tannat n pour l ile de re uniquement' in CDC['Charentais']['encep']

# ===================================================================================== 5) spirits
H('spirit-fine', 1, 'spirit', ('Une « Fine » (Fine Bordeaux, Fine Faugères…) est une eau-de-vie distillée à partir… ?', 'A “Fine” (Fine Bordeaux, Fine Faugères…) is a brandy distilled from…?'),
  ('de vin', 'wine'), [('de marc de raisin', 'grape pomace'), ('de bière', 'beer'), ('de cidre', 'cider')],
  ('Fine = eau-de-vie de vin ; Marc = eau-de-vie de marc de raisin (les peaux et pépins après pressurage).', 'Fine = wine brandy; Marc = pomace brandy (skins and pips left after pressing).'))
H('spirit-marc', 1, 'spirit', ('Un « Marc » (Marc du Jura, Marc de Savoie…) est distillé à partir… ?', 'A “Marc” (Marc du Jura, Marc de Savoie…) is distilled from…?'),
  ('du marc de raisin', 'grape pomace'), [('du vin', 'wine'), ('des sarments', 'vine shoots'), ('du jus de raisin', 'grape juice')],
  ('Le marc : ce qui reste des raisins après pressurage, distillé.', 'Pomace: what is left of the grapes after pressing, distilled.'))
H('spirit-gewurz', 3, 'spirit', ('Le Marc d’Alsace peut être suivi du nom de quel cépage ?', 'Marc d’Alsace may be followed by the name of which grape?'), 'Gewurztraminer',
  ['Riesling', 'Sylvaner', 'Pinot noir'], ('IG « Marc d’Alsace » suivie de la dénomination « Gewurztraminer ».', '“Marc d’Alsace” followed by the denomination “Gewurztraminer”.'))
H('spirit-faugeres', 3, 'spirit', ('Quelle IGP de spiritueux porte le nom d’une AOC languedocienne de 7 communes ?', 'Which spirit IGP is named after a 7-commune Languedoc AOC?'), 'Fine Faugères',
  ['Fine Bordeaux', 'Marc d’Auvergne', 'Marc de Savoie'], ('Fine Faugères : l’eau-de-vie de vin du Faugères.', 'Fine Faugères: the wine brandy of Faugères.'))
H('spirit-both', 2, 'spirit', ('Laquelle de ces IGP existe à la fois en « Fine » et en « Marc » ?', 'Which of these IGPs exists both as “Fine” and as “Marc”?'), 'Bourgogne',
  ['Alsace', 'Jura', 'Savoie'],
  ('Fine de Bourgogne et Marc de Bourgogne. Pour l’Alsace, le Jura et la Savoie, la carte ne recense que le Marc.', 'Fine and Marc de Bourgogne. For Alsace, Jura and Savoie, the map only lists Marc.'))
H('spirit-auvergne', 2, 'spirit', ('Laquelle de ces régions a une IGP de marc ?', 'Which of these regions has a marc IGP?'), 'Auvergne', ['Bretagne', 'Normandie', 'Picardie'],
  ('Marc d’Auvergne (le Puy-de-Dôme a aussi son IGP de vin).', 'Marc d’Auvergne (the Puy-de-Dôme also has a wine IGP).'))
_sp_right = ['Marc du Jura', 'Marc de Savoie', 'Fine Bordeaux', "Marc d'Alsace", 'Fine Faugères', "Marc d'Auvergne"]
_sp_wrong = ['Franche-Comté', 'Vin des Allobroges', 'Atlantique', 'Coteaux de Coiffy', "Pays d'Hérault", 'Puy-de-Dôme', 'Isère', 'Charentais']
for i, r in enumerate(_sp_right):
    assert r in SPIRIT or r.replace("'", '’') in SPIRIT, r
    w = RNG.sample(_sp_wrong, 3)
    H(f'spirit-which-{i}', 1 if i < 2 else 2, 'spirit', ('Laquelle de ces IGP est une eau-de-vie (et non un vin) ?', 'Which of these IGPs is a brandy (not a wine)?'),
      r.replace("'", '’'), [x.replace("'", '’') for x in w],
      (f'{r} est une indication géographique de spiritueux ; les autres sont des IGP de vin.'.replace("'", '’'), f'{r} is a spirit geographical indication; the others are wine IGPs.'.replace("'", '’')))

# ===================================================================================== 6) generated from map + FACTS
def lv_of(n):
    # large « IGP de zone » (several départements or a big part of one: Franche-Comté, Lorraine, Agenais…) stay level 2
    return 1 if n in FAMOUS else 2 if DATA[n]['cat'] in ('reg', 'dep') or DATA[n]['n'] >= 150 else 3


def pick(pool, k):
    pool = sorted(set(pool))
    return RNG.sample(pool, k) if len(pool) >= k else None


def special():
    r = RNG.random()
    return None if r > 0.3 else ('all' if r < 0.12 else 'none')


# 6a) wine region of an IGP
for n in WINE:
    if n in AMB:
        continue
    rs = REG[n]
    pool = [k for k in B if k not in rs and not any((r, k) in CLASH for r in rs)]
    lv = lv_of(n)
    q = (f'Dans quelle région viticole se trouve l’IGP <b>{n}</b> ?'.replace("'", '’'), f'In which wine region is the <b>{n}</b> IGP?'.replace("'", '’'))
    names = wr(rs)
    sp = special()
    if len(rs) == 1 and sp != 'none':
        d = pick(pool, 3)
        add(f'region-{norm(n)}', lv, 'region', q, [B[next(iter(rs))]] + [B[k] for k in d], 0, False,
            (f'{n} : {names[0]}. Départements : ' .replace("'", '’') + (', '.join(DEPS[n]) if DEPS[n] else 'plusieurs') + '.',
             f'{n}: {names[1]}. Départements: '.replace("'", '’') + (', '.join(DEPS[n]) if DEPS[n] else 'several') + '.'),
            cdc_url(n) or MAP, LK_CDC if cdc_url(n) else LK_MAP)
    elif len(rs) > 1 and sp == 'all' and len(rs) >= 3:
        three = sorted(rs)[:3]
        add(f'region-{norm(n)}', lv, 'region', q, [B[k] for k in three] + [ALL], 3, True,
            (f'{n} s’étend sur les trois : {names[0]}.'.replace("'", '’'), f'{n} spans all three: {names[1]}.'.replace("'", '’')),
            cdc_url(n) or MAP, LK_CDC if cdc_url(n) else LK_MAP)
    elif sp == 'none':
        d = pick(pool, 3)
        add(f'region-{norm(n)}', lv, 'region', q, [B[k] for k in d] + [NONE], 3, True,
            (f'Aucune : {n} est en {names[0]}.'.replace("'", '’'), f'None: {n} is in {names[1]}.'.replace("'", '’')),
            cdc_url(n) or MAP, LK_CDC if cdc_url(n) else LK_MAP)
    elif len(rs) > 1:
        d = pick(pool, 3)
        r0 = sorted(rs)[0]
        add(f'region-{norm(n)}', lv, 'region', q, [B[r0]] + [B[k] for k in d], 0, False,
            (f'{n} : {names[0]}.'.replace("'", '’'), f'{n}: {names[1]}.'.replace("'", '’')), cdc_url(n) or MAP, LK_CDC if cdc_url(n) else LK_MAP)

# 6b) which IGP is in region X?
for k in ['lr', 'so', 'pr', 'bo', 'rh', 'lo', 'sa', 'es', 'co', 'ju', 'ch', 'idf']:
    mine = [n for n in WINE if n not in AMB and REG[n] == {k}]
    others = [n for n in WINE if n not in AMB and not (REG[n] & {k}) and not any((k, r) in CLASH for r in REG[n])]
    for j, n in enumerate(sorted(mine, key=lambda n: (lv_of(n), n))[:3 if len(mine) > 4 else 1]):
        lv = lv_of(n)
        d = pick([o for o in others if lv_of(o) <= max(lv, 2)], 3)
        q = (f'Laquelle de ces IGP se trouve dans la région viticole <b>{B[k][0]}</b> ?', f'Which of these IGPs is in the <b>{B[k][1]}</b> wine region?')
        o = [same(n.replace("'", '’'))] + [same(x.replace("'", '’')) for x in d]
        add(f'inreg-{k}-{j}', lv, 'region', q, o, 0, False,
            (f'{n} : {B[k][0]}. Les autres : '.replace("'", '’') + ', '.join(f'{x} ({wr(REG[x])[0]})' for x in d).replace("'", '’') + '.',
             f'{n}: {B[k][1]}. The others: '.replace("'", '’') + ', '.join(f'{x} ({wr(REG[x])[1]})' for x in d).replace("'", '’') + '.'))
    if len(mine) >= 3:  # « all of the above »
        three = sorted(mine, key=lambda n: (lv_of(n), n))[-3:]
        add(f'inreg-{k}-all', 3 if k == 'lr' else 2, 'region',
            (f'Laquelle de ces IGP se trouve dans la région viticole <b>{B[k][0]}</b> ?', f'Which of these IGPs is in the <b>{B[k][1]}</b> wine region?'),
            [same(x.replace("'", '’')) for x in three] + [ALL], 3, True,
            (f'Les trois sont en {B[k][0]}.', f'All three are in {B[k][1]}.'))

# 6c) département of a single-département IGP whose name does not give it away
for n in WINE:
    deps = DEPS[n]
    if not deps or len(deps) != 1 or norm(deps[0]) in norm(n) or n in ('Côtes du Lot', 'Côtes du Tarn'):
        continue
    dep, rk = deps[0], next(iter(REG[n]))
    pool = [x for x in DEP_POOL.get(rk, []) if x != dep]
    d = pick(pool, 3)
    if not d:
        continue
    sp = special() if lv_of(n) > 1 else None
    q = (f'Dans quel département se trouve l’IGP <b>{n}</b> ?'.replace("'", '’'), f'In which département is the <b>{n}</b> IGP?'.replace("'", '’'))
    x = (f'{n} : {dep}.'.replace("'", '’'), f'{n}: {dep}.'.replace("'", '’'))
    lv = max(2, lv_of(n))
    if sp == 'none':
        add(f'dept-{norm(n)}', lv, 'dept', q, [same(t) for t in d] + [NONE], 3, True, x, cdc_url(n) or MAP, LK_CDC if cdc_url(n) else LK_MAP)
    else:
        add(f'dept-{norm(n)}', lv, 'dept', q, [same(dep)] + [same(t) for t in d], 0, False, x, cdc_url(n) or MAP, LK_CDC if cdc_url(n) else LK_MAP)

# 6d) dénominations (smaller geographical units) → which IGP?
EASY_DEN = {'Allier', 'Cher', 'Indre', 'Indre-et-Loire', 'Loir-et-Cher', 'Loire-Atlantique', 'Loiret', 'Maine-et-Loire', 'Nièvre', 'Sarthe',
            'Vendée', 'Vienne', 'Charente', 'Charente-Maritime', 'Ile de Ré', 'Doubs', 'Haute-Saône', 'Haute-Garonne', 'Cantal', 'Tarn et Garonne',
            'Pyrénées Atlantiques', 'Dordogne', 'Bigorre', 'Coteaux du Verdon', 'Comté de Grignan', 'Coteaux de Montélimar', "Coteaux de l'Ardèche",
            'Condomois', 'Pays de Retz', 'Marches de Bretagne', 'Pyrénées Orientales', 'Vin de Domme', 'Coteaux de Chalosse'}
DEN = []
UNVERIFIED = []
for n, v in DETAIL.items():
    for d in v.get('denoms', []):
        base = n if norm(d).startswith(norm(n)) else ('Méditerranée' if n == 'Méditerranée' else n)
        suf = d[len(base):].strip() if norm(d[:len(base)]) == norm(base) else re.sub(r'^\S+\s+(tolosan\s+)?', '', d) if n != 'Méditerranée' else d.split(' ', 1)[1]
        suf = suf.replace('Côteaux', 'Coteaux').replace('Suresne-', 'Suresnes-')
        if n in CDC and not in_cdc(n, suf.split(' rosé')[0]):
            UNVERIFIED.append((n, suf))  # not in our (older) copy of the rulebook → left out
            continue
        DEN.append((n, suf))
used = {'Caux', 'La côte rêvée', 'Coteaux de Provins', "Principauté d'Orange", 'Rocamadour', 'Terre de Camargue', "Cap d'Agde", "Ile d'Oléron",
        "Sables de l'Océan", 'Pays de Gex', 'Balmes dauphinoises', 'Sainte Baume', "Cité d'Aniane", 'Vallée Dorée', 'Haut de Badens',
        'Saint-Sornin', 'Ambierle rosé', 'Pays de Cucugnan', 'Paris'}
DEN_IGPS = sorted({n for n, _ in DEN})
den_pick = [t for t in DEN if t[1] not in used and t[0] not in ('Comté Tolosan', 'Val de Loire', 'Charentais')]
den_pick += [t for t in DEN if t[0] in ('Comté Tolosan', 'Val de Loire') and t[1] in ('Bigorre', 'Coteaux et Terrasses de Montauban', 'Marches de Bretagne', 'Pays de Retz')]
for i, (n, suf) in enumerate(sorted(den_pick)):
    if i % 3 == 2 and n not in ("Pays d'Hérault", 'Aude', 'Franche-Comté'):
        continue  # keep the bank balanced
    others = [m for m in DEN_IGPS if m != n and not any(s2 == suf for m2, s2 in DEN if m2 == m)]
    near = [m for m in others if REG[m] & REG[n]]
    d = pick(near if len(near) >= 3 else others, 3)
    lv = 2 if suf in EASY_DEN else 3
    add(f'denom-{norm(n)}-{norm(suf)}', lv, 'denom',
        (f'« {suf} » est une unité géographique plus petite de quelle IGP ?'.replace("'", '’'), f'“{suf}” is a smaller geographical unit of which IGP?'.replace("'", '’')),
        [same(n.replace("'", '’'))] + [same(x.replace("'", '’')) for x in d], 0, False,
        (f'L’IGP {n} peut être complétée par « {suf} ».'.replace("'", '’'), f'The {n} IGP may be followed by “{suf}”.'.replace("'", '’')),
        cdc_url(n) or MAP, LK_CDC if cdc_url(n) else LK_MAP)
# « all / none » on dénominations of one IGP
for n, lv in (("Pays d'Hérault", 3), ('Aude', 3), ('Franche-Comté', 3), ('Landes', 2)):
    mine = [s2 for m, s2 in DEN if m == n]
    three = RNG.sample(mine, 3)
    add(f'denom-all-{norm(n)}', lv, 'denom', (f'Laquelle est une unité géographique de l’IGP <b>{n}</b> ?'.replace("'", '’'), f'Which is a geographical unit of the <b>{n}</b> IGP?'.replace("'", '’')),
        [same(t.replace("'", '’')) for t in three] + [ALL], 3, True,
        (f'Les trois. Unités de l’IGP {n} : '.replace("'", '’') + ', '.join(mine).replace("'", '’') + '.', f'All three. Units of the {n} IGP: '.replace("'", '’') + ', '.join(mine).replace("'", '’') + '.'),
        cdc_url(n) or MAP, LK_CDC if cdc_url(n) else LK_MAP)

# 6e) size (commune counts from the map; only clear-cut comparisons)
N_ = {n: DATA[n]['n'] for n in WINE}
small = sorted((n for n in WINE if DATA[n]['cat'] == 'zone'), key=lambda n: N_[n])
for i in range(6):
    tiny = small[i]
    cand = [n for n in WINE if N_[n] >= 3 * N_[tiny] and DATA[n]['cat'] == 'zone']
    d = pick(cand, 3)
    add(f'size-small-{i}', 3 if i > 1 else 2, 'size', ('Laquelle de ces IGP compte le MOINS de communes ?', 'Which of these IGPs has the FEWEST communes?'),
        [same(tiny.replace("'", '’'))] + [same(x.replace("'", '’')) for x in d], 0, False,
        (f'{tiny} : {N_[tiny]} commune(s). '.replace("'", '’') + ', '.join(f'{x} : {N_[x]}' for x in d).replace("'", '’') + ' (d’après la carte des IGP).',
         f'{tiny}: {N_[tiny]} commune(s). '.replace("'", '’') + ', '.join(f'{x}: {N_[x]}' for x in d).replace("'", '’') + ' (from the IGP map).'))
for i, big in enumerate(['Comté Tolosan', 'Val de Loire', 'Méditerranée', 'Atlantique']):
    cand = [n for n in WINE if N_[n] * 3 <= N_[big] and DATA[n]['cat'] != 'reg']
    d = pick(cand, 3)
    add(f'size-big-{i}', 2 if i < 2 else 3, 'size', ('Laquelle de ces IGP couvre le PLUS de communes ?', 'Which of these IGPs covers the MOST communes?'),
        [same(big)] + [same(x.replace("'", '’')) for x in d], 0, False,
        (f'{big} : environ {N_[big]} communes. '.replace("'", '’') + ', '.join(f'{x} : {N_[x]}' for x in d).replace("'", '’') + '.',
         f'{big}: about {N_[big]} communes. '.replace("'", '’') + ', '.join(f'{x}: {N_[x]}' for x in d).replace("'", '’') + '.'))
add('size-torgan', 2, 'size', ('Combien de communes compte la Vallée du Torgan, plus petite IGP de la carte ?', 'How many communes make up the Vallée du Torgan, the smallest IGP on the map?'),
    [same('2'), same('12'), same('25'), same('117')], 0, False,
    ('Deux : Tuchan et Paziols.', 'Two: Tuchan and Paziols.'), cdc_url('Vallée du Torgan'), LK_CDC)

# 6f) IGP or AOC?
IGP_NAMES = [n for n in WINE if n not in AOC_NAMES and not any(norm(a).startswith(norm(n)) or norm(n).startswith(norm(a)) for a in AOC_NAMES)]
AOC_POOL = [a for a in AOC_NAMES if not any(norm(i_) in norm(a) or norm(a) in norm(i_) for i_ in WINE)]
for i in range(26):
    lv = 1 if i < 9 else 2 if i < 18 else 3
    pool_i = [n for n in IGP_NAMES if (n in FAMOUS) == (lv == 1) or lv == 3]
    pool_a = [a for a in AOC_POOL if (a in AOC_FAMOUS) == (lv == 1) or lv == 3]
    kind = 'plain' if i % 4 else ('none' if i % 8 == 0 else 'all')
    if kind == 'plain':
        ig, aa = RNG.choice(pool_i), RNG.sample(pool_a, 3)
        add(f'igpaoc-{i}', lv, 'igpaoc', ('Lequel de ces noms est une <b>IGP</b> (et non une AOC) ?', 'Which of these names is an <b>IGP</b> (not an AOC)?'),
            [same(ig.replace("'", '’'))] + [same(a.replace("'", '’')) for a in aa], 0, False,
            (f'{ig} est une IGP ; '.replace("'", '’') + ', '.join(aa).replace("'", '’') + ' sont des AOC.', f'{ig} is an IGP; '.replace("'", '’') + ', '.join(aa).replace("'", '’') + ' are AOCs.'))
    elif kind == 'none':
        ii = RNG.sample(pool_i, 3)
        add(f'igpaoc-{i}', lv, 'igpaoc', ('Lequel de ces noms est une <b>AOC</b> ?', 'Which of these names is an <b>AOC</b>?'),
            [same(x.replace("'", '’')) for x in ii] + [NONE], 3, True,
            ('Aucun : ' + ', '.join(ii).replace("'", '’') + ' sont trois IGP.', 'None: ' + ', '.join(ii).replace("'", '’') + ' are three IGPs.'))
    else:
        ii = RNG.sample(pool_i, 3)
        add(f'igpaoc-{i}', lv, 'igpaoc', ('Lequel de ces noms est une <b>IGP</b> ?', 'Which of these names is an <b>IGP</b>?'),
            [same(x.replace("'", '’')) for x in ii] + [ALL], 3, True,
            ('Les trois sont des IGP : ' + ', '.join(ii).replace("'", '’') + '.', 'All three are IGPs: ' + ', '.join(ii).replace("'", '’') + '.'))

# 6g) regional IGPs — traps are only small, single-département « IGP de zone » (not Franche-Comté, Lorraine, Allobroges…)
SMALL_ZONE = [n for n in WINE if DATA[n]['cat'] == 'zone' and DATA[n]['n'] < 150 and F.get(n) and F[n][1] and len(F[n][1]) == 1]
for i, r in enumerate(REGIONAL):
    d = pick(SMALL_ZONE, 3)
    add(f'categ-reg-{i}', 1 if r in FAMOUS else 2, 'categ',
        ('Laquelle de ces IGP est une IGP <b>régionale</b>, à cheval sur plusieurs départements ?', 'Which of these is a <b>regional</b> IGP, spanning several départements?'),
        [same(r.replace("'", '’'))] + [same(x.replace("'", '’')) for x in d], 0, False,
        (f'{r} est une IGP régionale ; les trois autres sont de petites IGP de zone.'.replace("'", '’'), f'{r} is a regional IGP; the other three are small “IGP de zone”.'.replace("'", '’')))


def bank():
    return Q


if __name__ == '__main__':
    from collections import Counter
    print(len(Q), 'questions')
    print(Counter(q['lv'] for q in Q))
    print(Counter(q['cat'] for q in Q))
    print(Counter((q['lv'], q['cat']) for q in Q))
    print('special', sum(q['fix'] for q in Q))
    print('unverified denoms skipped:', UNVERIFIED)
