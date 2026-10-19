# -*- coding: utf-8 -*-
"""One-off: freezes the Burgundy premier cru list into premiers_crus.json.
Source = INAO « délimitation parcellaire des AOC viticoles » (release 2026-06-15, data.gouv.fr), field `denom`
« <AOC> premier cru <climat> » for dt Dijon + Mâcon, communes from `nomcom`.
Chablis: the INAO file only carries 10 of its climats → list taken from the Chablis cahier des charges (II-3°),
with the climat principal of each group. Usage: python3 make_premiers_crus.py <inao_rows.json> <communes.geojson>"""
import json, sys, unicodedata, collections
rows = json.load(open(sys.argv[1]))
import re
for r in rows: r['denom'] = re.sub(r' premier cru ', ' premier cru ', r['denom'], flags=re.I)
geo = json.load(open(sys.argv[2]))
def key(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().upper().replace('’', "'")
NAMES = {key(f['properties']['nom']): f['properties']['nom'] for f in geo['features']
         if f['properties']['code'][:2] in ('21', '71', '89')}
COTE = {}
for a in ['Fixin', 'Gevrey-Chambertin', 'Morey-Saint-Denis', 'Chambolle-Musigny', 'Vougeot', 'Vosne-Romanée', 'Nuits-Saint-Georges']: COTE[a] = 'nuits'
for a in ['Ladoix', 'Aloxe-Corton', 'Pernand-Vergelesses', 'Savigny-lès-Beaune', 'Beaune', 'Pommard', 'Volnay', 'Monthélie',
          'Auxey-Duresses', 'Meursault', 'Blagny', 'Puligny-Montrachet', 'Chassagne-Montrachet', 'Saint-Aubin', 'Santenay', 'Maranges']: COTE[a] = 'beaune'
for a in ['Rully', 'Mercurey', 'Givry', 'Montagny']: COTE[a] = 'chalon'
for a in ['Pouilly-Fuissé', 'Pouilly-Loché', 'Pouilly-Vinzelles']: COTE[a] = 'macon'
d = collections.defaultdict(set)
for r in rows:
    if r['dt'] in ('Dijon', 'Mâcon') and ' premier cru ' in r['denom'] and r['app'] != 'Chablis':
        cl = r['denom'].split(' premier cru ', 1)[1]
        if cl == 'Les Chaillots blanc': cl = 'Les Chaillots (blanc)'
        d[(r['app'], cl)].add(NAMES.get(key(r['nomcom']), r['nomcom'].title()))
out = [[COTE[a], a, cl, sorted(c), ''] for (a, cl), c in d.items()]
chab_communes = collections.defaultdict(set)
for r in rows:
    if r['app'] == 'Chablis' and ' premier cru ' in r['denom']:
        chab_communes[r['denom'].split(' premier cru ', 1)[1]].add(NAMES.get(key(r['nomcom']), r['nomcom'].title()))
CHAB = [['Beauroy', 'Côte de Savant', 'Troesmes'], ['Berdiot'], ['Chaume de Talvat'], ['Côte de Jouan'], ['Côte de Léchet'],
        ['Côte de Vaubarousse'], ['Fourchaume', 'Côte de Fontenay', "L'Homme Mort", 'Vaulorent', 'Vaupulent'],
        ['Les Beauregards', 'Côte de Cuisy'], ['Les Fourneaux', 'Côte des Prés-Girots', 'Morein'], ['Mont de Milieu'],
        ['Montée de Tonnerre', 'Chapelot', 'Côte de Bréchain', "Pied d'Aloup"], ['Montmains', 'Butteaux', 'Forêts'],
        ['Vaillons', 'Beugnons', 'Chatains', 'Les Épinottes', 'Les Lys', 'Mélinots', 'Roncières', 'Sécher'],
        ['Vau de Vey', 'Vaux Ragons'], ['Vau Ligneau'], ['Vaucoupin'], ['Vosgros', 'Vaugiraut']]
for g in CHAB:
    for i, cl in enumerate(g):
        out.append(['chablis', 'Chablis', cl, sorted(chab_communes.get(cl, [])), '' if i == 0 else g[0]])
ORDER = ['chablis', 'nuits', 'beaune', 'chalon', 'macon']
APPS = ['Chablis', 'Fixin', 'Gevrey-Chambertin', 'Morey-Saint-Denis', 'Chambolle-Musigny', 'Vougeot', 'Vosne-Romanée',
        'Nuits-Saint-Georges', 'Ladoix', 'Aloxe-Corton', 'Pernand-Vergelesses', 'Savigny-lès-Beaune', 'Beaune', 'Pommard',
        'Volnay', 'Monthélie', 'Auxey-Duresses', 'Meursault', 'Blagny', 'Puligny-Montrachet', 'Chassagne-Montrachet',
        'Saint-Aubin', 'Santenay', 'Maranges', 'Rully', 'Mercurey', 'Givry', 'Montagny', 'Pouilly-Fuissé', 'Pouilly-Loché', 'Pouilly-Vinzelles']
def sk(s): return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
out.sort(key=lambda x: (APPS.index(x[1]), sk(x[2]) if x[1] != 'Chablis' else 0))
json.dump(out, open('premiers_crus.json', 'w'), ensure_ascii=False, indent=0)
print(len(out), collections.Counter(x[1] for x in out))
