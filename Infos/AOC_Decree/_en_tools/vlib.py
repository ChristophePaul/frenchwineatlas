"""Helpers for cloning 2010 Burgundy village drafts from the Morey-Saint-Denis EN source."""
import re, sys
class V:
    def __init__(s, name, src='bourgogne_cote_de_nuits_morey_saint_denis', srcname='Morey-Saint-Denis'):
        s.t = open(f'_en_src/{src}.txt').read()
        s.R(f'“{srcname}”', f'“{name}”', 0)
        s.R(f'“{srcname.upper()}”', f'“{name.upper()}”', 0)
        s.name = name
    def R(s, old, new, count=1):
        assert old in s.t, 'NOT FOUND: ' + old[:100]
        s.t = s.t.replace(old, new) if count == 0 else s.t.replace(old, new, count)
    def section(s, start, end, new):
        a = s.t.index(start); b = s.t.index(end, a)
        s.t = s.t[:a] + new + s.t[b:]
    def table(s, rows, extra=''):
        """rows: list of (commune, climat, lieudit); replaces the premier cru table (and Morey's c) clause)."""
        new = '| COMMUNE | NAME OF CLIMAT | LIEU-DIT |\n' + ''.join(f'| {a} | {b} | {c} |\n' for a, b, c in rows) + extra
        s.section('| COMMUNE | NAME OF CLIMAT', '### 3° – Immediate proximity area', new)
    @staticmethod
    def rows_fr(md):
        """parse '| a | b | c |' French rows (from extract_fr) into EN tuples, merging continuation lines."""
        out = []
        for l in md.strip().splitlines():
            c = [x.strip() for x in l.strip().strip('|').split('|')]
            if len(c) < 3 or c[0] == 'COMMUNE' or not any(c): continue
            c = [x.replace('(en partie)', '(in part)').replace("'", '’') for x in c[:3]]
            if not c[1] and not c[2]: continue
            out.append((c[0].upper() if c[0] else '', c[1], c[2]))
        return out
    def save(s, slug):
        open(f'_en_src/{slug}.txt', 'w').write(s.t)

def red_only(v):
    """convert the Morey (white+red) text to a red-only village."""
    v.R('is reserved for still white or red wines.', 'is reserved for still red wines.')
    v.section('### 1° – Grape varieties', '## VI. – Management', '''### 1° – Grape varieties
The wines come from the following varieties:
- main variety: pinot noir N;
- accessory varieties: chardonnay B, pinot blanc B, pinot gris G.
### 2° – Proportion rules on the holding
The accessory varieties are authorised only as mixed plantings within the vines. Their total proportion is limited to 15 % within each parcel.
''')
    v.R('The red wines come from vines pruned according to the following techniques:', 'The wines come from vines pruned according to the following techniques:')
    v.R('''The white wines come from vines pruned according to the following techniques:
- either short pruning (vines trained as Royat cordon and bilateral cordon), with a number of free eyes per plant less than or equal to 10;
- or single Guyot long pruning, with a number of free eyes per plant less than or equal to 8.
''', '')
    v.R('set at 9,000 kilograms per hectare for red wines and 10,500 kilograms per hectare for white wines.', 'set at 9,000 kilograms per hectare.')
    v.section('### 2° – Ripeness of the grapes', '## VIII.', '''### 2° – Ripeness of the grapes
a) – Sugar content of the grapes
Grapes with a sugar content of less than 180 grams per litre of must may not be considered to be at good ripeness.
Where the name of the appellation is supplemented by the name of a climat or by the expression “premier cru”, or by both, for wines from the climats classified as premier cru, grapes with a sugar content of less than 189 grams per litre of must may not be considered to be at good ripeness.
b) – Minimum natural alcoholic strength by volume
The wines have a minimum natural alcoholic strength by volume of 10.5 %.
Where the name of the appellation is supplemented by the name of the climat of origin, or by the term “premier cru”, or by both, for wines from the climats classified as premier cru, the wines have a minimum natural alcoholic strength by volume of 11 %.
''')
    v.R('is set at 50 hectolitres per hectare for red wines and 57 hectolitres per hectare for white wines.', 'is set at 50 hectolitres per hectare.')
    v.R('is set at 48 hectolitres per hectare for red wines and 55 hectolitres per hectare for white wines.', 'is set at 48 hectolitres per hectare.')
    n = v.name
    v.section(f'| AOC “{n}” for white wines | 64 |', '### 3° – Maximum production yield', f'''| AOC “{n}” | 58 |
| AOC “{n}” supplemented by the name of the climat of origin, or by the term “premier cru”, or by both, for wines from the climats classified as premier cru | 56 |
''')
    v.R('Red wines produced from parcels with mixed plantings', 'Wines produced from parcels with mixed plantings')
    v.R('At the packaging stage, red wines have', 'At the packaging stage, the wines have')
    v.R('''(glucose + fructose) of:
- for white wines, 3 grams per litre, or 4 grams per litre if the total acidity, expressed as H2SO4, is greater than or equal to 2.7 grams per litre;
- for red wines, 2 grams per litre.''', '(glucose + fructose) of 2 grams per litre.')
    v.R('''equivalent to at least:
- for white wines, the volume of wine vinified for the previous year’s harvest, as entered either on the harvest declaration, pro rata to the change in the holding’s area in production, or on the production declaration;
- for red wines, 150 % of the volume''', 'equivalent to at least 150 % of the volume')

def no_premier_cru(v, area_sentence, dates, climat=True):
    """remove premier cru provisions (II, IV 2°, ripeness/yields/enrichment, XII)."""
    if climat:
        v.R('may be supplemented by the name of the climat of origin, or by the term “premier cru”, or by both, for wines meeting',
            'may be supplemented by the name of the climat of origin for wines meeting')
    v.R('within the territory of the commune of Morey-Saint-Denis, in the Côte-d’Or department.', area_sentence)
    v.section('a) – The wines come exclusively from vines situated within the delimited parcel', '### 3° – Immediate proximity area',
        f'''The wines come exclusively from vines situated within the delimited parcel production area as approved by the National Institute of Origin and Quality at the sessions of the competent national committee of {dates}.
The National Institute of Origin and Quality lodges with the town hall of the commune referred to in 1° the graphic documents establishing the parcel boundaries of the production area thus approved.
''')
    v.section('Where the name of the appellation is supplemented by the name of the climat of origin, or by the term “premier cru”, or by both, for wines from the climats classified as premier cru, the sugar content', '## VIII.', '')
    v.R('''Where the name of the appellation is supplemented by the name of the climat of origin, or by the term “premier cru”, or by both, for wines from the climats classified as premier cru, the yield referred to in Article D. 644-25 of the Rural Code is set at 48 hectolitres per hectare for red wines and 55 hectolitres per hectare for white wines.
''', '')
    v.R(' Where the name of the appellation is supplemented by the name of the climat of origin, or by the term premier cru, or by both, for wines from the climats classified as premier cru, the wines do not exceed, after enrichment, a total alcoholic strength by volume of 14 %.', '')

def cdb_suffix(v, red_only_wines=True):
    """the 'Côte de Beaune' geographical denomination (II, III, XII)."""
    v.R('for wines meeting the production conditions set for these terms in the present specification.',
        'for wines meeting the production conditions set for these terms in the present specification.\nThe name of the appellation may be followed by the geographical denomination “Côte de Beaune”.')
    if red_only_wines:
        v.R('is reserved for still white or red wines.', 'is reserved for still white or red wines.\nThe geographical denomination “Côte de Beaune” is reserved for still red wines.')
    v.R('must not exceed half those of the appellation.\n# CHAPTER II',
        'must not exceed half those of the appellation.\n' + ('For red wines, where' if red_only_wines else 'Where') +
        ' the appellation is followed by the words “Côte de Beaune”, the appellation thus formed is inseparable and is printed in identical characters of the same form, size and colour.\n# CHAPTER II')

def gris_whites(v, accessory='pinot gris G', main='chardonnay B and pinot blanc B'):
    """white wines with main varieties + one accessory limited to 10 % / 30 %."""
    v.section('### 1° – Grape varieties', '## VI. – Management', f'''### 1° – Grape varieties
a) – The white wines come from the following varieties:
- main varieties: {main};
- accessory variety: {accessory}.
b) – The red wines come from the following varieties:
- main variety: pinot noir N;
- accessory varieties: chardonnay B, pinot blanc B, pinot gris G.
### 2° – Proportion rules on the holding
Compliance of the planting is assessed, for the colour concerned, over all the parcels of the holding producing the wine of the appellation.
a) – White wines
The proportion of the {accessory} variety is less than or equal to 10 % of the planting.
b) – Red wines
The accessory varieties are authorised only as mixed plantings within the vines. Their total proportion is limited to 15 % within each parcel.
''')
    v.R('Red wines produced from parcels with mixed plantings are vinified by blending the grapes.',
        f'The proportion of {accessory.rsplit(" ",1)[0]} {accessory.rsplit(" ",1)[1]} is less than or equal to 30 % in the blend of white wines.\nRed wines produced from parcels with mixed plantings are vinified by blending the grapes.')

def chapter1(v, text):
    """replace the whole of chapter I (keeping Morey's chapters II and III)."""
    v.section('# CHAPTER I\n', '# CHAPTER II\n', text)

MONTREUIL = ('51, rue d’Anjou, 75008 PARIS\nTel.: (33) (0)1.53.89.80.00 – Fax: (33) (0)1.42.25.57.97',
             'TSA 30003, 93555 MONTREUIL-SOUS-BOIS Cedex\nTel.: (33) (0)1.73.30.38.00 – Fax: (33) (0)1.73.30.38.04')
