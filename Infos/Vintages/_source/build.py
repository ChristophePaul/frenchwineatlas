#!/usr/bin/env python3
"""Build the French vintage chart page.

Blends the user's own spreadsheet (Vintage Charts/Wine List vintage chart_05to25.xlsx)
with public charts saved in sources/ (BBR, iDealwine, Wine Scholar Guild, Wine
Enthusiast, Grains & Grapes). Each public chart is linearly calibrated onto the
spreadsheet's 5-star scale, then values are blended per region row and rounded
to the nearest half star.

Usage:  python3 build.py            (writes ../Vintage_Chart.html)
"""
import json, os, re, sys
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(HERE, '../../../../Vintage Charts/Wine List vintage chart_05to25.xlsx')
OUT = os.path.join(HERE, '../Vintage_Chart.html')
SRC = os.path.join(HERE, 'sources')

sys.path.insert(0, HERE)
from notes import YEAR_NOTES, ROW_NOTES  # noqa: E402

# ---------------------------------------------------------------- spreadsheet
def stars(v):
    if v is None or isinstance(v, (int, float)):
        return None
    s = str(v).replace('«', '*').strip()
    if not s or s.upper() in ('NA', 'N/A', '-'):
        return None
    vals = []
    for m in re.finditer(r'(\*+)\s*(½|1/2)?(\(\*\))?', s):
        x = len(m.group(1)) + (0.5 if m.group(2) else 0) + (0.5 if m.group(3) else 0)
        vals.append(min(x, 5))
    if not vals:
        return None
    x = sum(vals) / len(vals)
    if '+' in s:
        x += 0.25
    return x


def read_user():
    wb = openpyxl.load_workbook(XLSX, data_only=True)
    U = {}

    def put(fam, y, v, prio):
        if v is None or not isinstance(y, int):
            return
        cur = U.setdefault(fam, {}).get(y)
        if cur is None or cur[1] < prio:
            U[fam][y] = (v, prio)

    # newest sheet: 2005-2025, two blocks
    ws = wb['2003-2023']
    block = 0
    for r in ws.iter_rows(values_only=True):
        if r[0] == 'Languedoc':
            block = 1
        if not isinstance(r[0], int):
            continue
        if block == 0:
            put('Alsace', r[0], stars(r[1]), 4)
            md, lb = stars(r[3]), stars(r[4])
            if md is not None and lb is not None:
                put('BdxRed', r[2], (md + lb) / 2, 4)
            put('Sauternes', r[2], stars(r[5]), 4)
            put('Champagne', r[6], stars(r[7]), 4)
            put('BurgW', r[8], stars(r[9]), 4)
            put('BurgR', r[8], stars(r[10]), 4)
            put('Beaujolais', r[8], stars(r[11]), 4)
        else:
            put('LR', r[0], stars(r[1]), 4)
            put('RhN', r[2], stars(r[3]), 4)
            put('RhS', r[2], stars(r[4]), 4)
            put('Provence', r[2], stars(r[5]), 4)
            put('SJ', r[6], stars(r[7]), 4)
            put('LoireW', r[8], stars(r[9]), 4)
            put('LoireR', r[8], stars(r[10]), 4)
            put('LoireS', r[8], stars(r[11]), 4)

    # concise charts 1987-2011 (same layout)
    for name, prio in (('1991-2011', 3), ('1987-2007', 2)):
        ws = wb[name]
        block = 0
        for r in ws.iter_rows(values_only=True):
            if r[0] == 'White':
                block = 1
            fams = (['Alsace', 'BdxRed', 'BdxWS', 'Champagne', 'Loire'] if block == 0
                    else ['BurgW', 'BurgR', 'RhN', 'RhS', 'SJ'])
            for i, fam in enumerate(fams):
                yc, vc = 3 * i, 3 * i + 1
                if isinstance(r[yc], int):
                    put(fam, r[yc], stars(r[vc]), prio)

    # oldest sheet (1980-1998), titled blocks
    ws = wb['Sheet2']
    titles = {'Alsace': 'Alsace', 'Red Bordeaux': 'BdxRed', 'White Bordeaux': 'BdxWS',
              'Red Burgundy': 'BurgR', 'White Burgundy': 'BurgW',
              'Southern Rhône': 'RhS', 'Northern Rhône': 'RhN'}
    fam = None
    for r in ws.iter_rows(values_only=True):
        if isinstance(r[0], str):
            for k, f in titles.items():
                if r[0].strip().startswith(k):
                    fam = f
        elif isinstance(r[0], int) and fam:
            put(fam, r[0], stars(r[1]), 1)

    U = {f: {y: v for y, (v, p) in d.items()} for f, d in U.items()}
    # the old single Loire column feeds all three Loire families before 2005
    for f in ('LoireW', 'LoireR', 'LoireS'):
        for y, v in U.get('Loire', {}).items():
            U.setdefault(f, {}).setdefault(y, v)
    for y, v in U.get('BdxWS', {}).items():
        U.setdefault('Sauternes', {}).setdefault(y, v)
    return U

# ---------------------------------------------------------------- public charts
def load(name):
    with open(os.path.join(SRC, name), encoding='utf-8') as f:
        return json.load(f)


def raw_sources():
    S = {}
    for k, d in load('bbr.json').items():
        S['BBR:' + k] = {int(y): v for y, v in d.items()}
    ideal = load('ideal.json')
    cols = ['BdxR', 'BdxW', 'BdxS', 'BurgR', 'BurgW', 'Champagne', 'RhN', 'RhS',
            'Loire', 'Alsace', 'Beaujolais', 'Savoie', 'Corsica']
    for row in ideal[1:]:
        y = int(row[0])
        for c, v in zip(cols, row[1:]):
            v = v.replace('/20', '').strip()
            if v:
                S.setdefault('ID:' + c, {})[y] = int(v)
    for k, d in load('wsg.json').items():
        S['WSG:' + k.replace('&amp;', '&')] = {int(y): v for y, v in d.items() if v is not None}
    we = load('we.json')
    for k, vals in we['rows'].items():
        S['WE:' + k] = {y: int(v) for y, v in zip(we['years'], vals) if v.isdigit()}
    letter = {'O': 5, 'E': 4, 'G': 3, 'A': 2, 'P': 1}
    for k, d in load('gg.json').items():
        S['GG:' + k] = {int(y): letter[v] for y, v in d.items() if v in letter}
    return S


# which spreadsheet family each public series should agree with (for calibration)
CAL = {
    'BBR:Champagne': 'Champagne', 'BBR:Red Bordeaux': 'BdxRed', 'BBR:Red Burgundy': 'BurgR',
    'BBR:White Burgundy': 'BurgW', 'BBR:Rhône': 'RhS', 'BBR:Loire': 'LoireW', 'BBR:Alsace': 'Alsace',
    'ID:BdxR': 'BdxRed', 'ID:BdxS': 'Sauternes', 'ID:BurgR': 'BurgR', 'ID:BurgW': 'BurgW',
    'ID:Champagne': 'Champagne', 'ID:RhN': 'RhN', 'ID:RhS': 'RhS', 'ID:Loire': 'LoireW',
    'ID:Alsace': 'Alsace', 'ID:Beaujolais': 'Beaujolais',
    'WSG:Alsace': 'Alsace', 'WSG:Champagne': 'Champagne', 'WSG:Côte de Beaune whites': 'BurgW',
    'WSG:Côte de Beaune Côte de Nuits reds': 'BurgR', 'WSG:Beaujolais': 'Beaujolais',
    'WSG:Northern Rhône': 'RhN', 'WSG:Southern Rhône': 'RhS', 'WSG:Provence': 'Provence',
    'WSG:Languedoc-Roussillon': 'LR', 'WSG:Médoc Graves': 'BdxRed', 'WSG:Sauternes': 'Sauternes',
    'WE:Médoc': 'BdxRed', 'WE:Sauternes': 'Sauternes', 'WE:CdN red': 'BurgR', 'WE:CdB white': 'BurgW',
    'WE:N Rhône red': 'RhN', 'WE:S Rhône red': 'RhS', 'WE:Loire sweet': 'LoireS',
    'WE:Loire red': 'LoireR', 'WE:Loire dry white': 'LoireW', 'WE:Alsace': 'Alsace',
    'WE:Champagne': 'Champagne', 'WE:Languedoc-Roussillon': 'LR', 'WE:Provence red': 'Provence',
    'WE:Beaujolais': 'Beaujolais',
    'GG:Alsace': 'Alsace', 'GG:Burgundy (Red)': 'BurgR', 'GG:Burgundy (White)': 'BurgW',
    'GG:Champagne': 'Champagne', 'GG:Jura': 'SJ', 'GG:Languedoc-Roussillon': 'LR',
    'GG:Loire Valley': 'LoireW', 'GG:Northern Rhone': 'RhN', 'GG:Southern Rhone': 'RhS',
    'GG:Provence': 'Provence', 'GG:Bordeaux (Left Bank)': 'BdxRed', 'GG:Bordeaux (Right Bank)': 'BdxRed',
    'GG:Beaujolais': 'Beaujolais',
}


def calibrate(S, U):
    """Fit one linear map per source (BBR, ID, WSG, WE, GG) onto the user's stars."""
    fits = {}
    for pre in ('BBR', 'ID', 'WSG', 'WE', 'GG'):
        xs, ys = [], []
        for k, fam in CAL.items():
            if not k.startswith(pre + ':') or k not in S:
                continue
            for y, x in S[k].items():
                if y in U.get(fam, {}):
                    xs.append(x); ys.append(U[fam][y])
        n = len(xs)
        mx, my = sum(xs) / n, sum(ys) / n
        a = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
        # keep the spread of the source (a regression slope shrinks towards the mean)
        sx = (sum((x - mx) ** 2 for x in xs) / n) ** .5
        sy = (sum((y - my) ** 2 for y in ys) / n) ** .5
        a = sy / sx if a > 0 else a
        fits[pre] = (a, my - a * mx, n)
    C = {}
    for k, d in S.items():
        a, b, _ = fits[k.split(':')[0]]
        C[k] = {y: max(0.5, min(5.0, a * v + b)) for y, v in d.items()}
    return C, fits

# ---------------------------------------------------------------- region rows
# (source key, weight, generic?)  generic series receive the row's deltas
def U_(f, w=3, g=False): return ('U:' + f, w, g)
def X(k, w=1, g=False): return (k, w, g)

BDX_R = [U_('BdxRed'), X('BBR:Red Bordeaux'), X('ID:BdxR'), X('WSG:Médoc Graves'), X('WSG:Médoc Graves Red'),
         X('WSG:St.-Emilion Pomerol'), X('WE:Médoc', .5), X('WE:Bordeaux Pomerol/St-Em', .5),
         X('GG:Bordeaux (Left Bank)', .5), X('GG:Bordeaux (Right Bank)', .5)]
BDX_W = [U_('BdxWS', 1), X('BBR:White Bordeaux'), X('ID:BdxW'), X('WE:Graves white'), X('WSG:Médoc Graves White')]
SAUT = [U_('Sauternes'), X('ID:BdxS'), X('WE:Sauternes'), X('WSG:Sauternes')]
BURG_R = [U_('BurgR'), X('BBR:Red Burgundy'), X('ID:BurgR'), X('WSG:Côte de Beaune Côte de Nuits reds'),
          X('GG:Burgundy (Red)', .5)]
BURG_W = [U_('BurgW'), X('BBR:White Burgundy'), X('ID:BurgW'), X('WSG:Côte de Beaune whites'),
          X('WE:CdB white'), X('GG:Burgundy (White)', .5)]
BEAUJ = [U_('Beaujolais'), X('ID:Beaujolais'), X('WSG:Beaujolais'), X('WE:Beaujolais'), X('GG:Beaujolais', .5)]
LOIRE = [X('BBR:Loire'), X('ID:Loire'), X('GG:Loire Valley', .5)]
LR = [U_('LR'), X('WSG:Languedoc-Roussillon'), X('WE:Languedoc-Roussillon'), X('GG:Languedoc-Roussillon', .5)]
PROV = [U_('Provence'), X('WSG:Provence'), X('GG:Provence', .5), X('ID:Corsica', .5)]
RHN = [U_('RhN'), X('BBR:Rhône', .5), X('ID:RhN'), X('WSG:Northern Rhône'), X('GG:Northern Rhone', .5)]
RHS = [U_('RhS'), X('BBR:Rhône', .5), X('ID:RhS'), X('WSG:Southern Rhône'), X('GG:Southern Rhone', .5)]
SJ = [U_('SJ', 2, True), X('GG:Jura', .5, True)]


def gen(lst, w_scale=1.0):
    """Mark a source list as generic (row deltas apply) and optionally down-weight it."""
    return [(k, w * w_scale, True) for k, w, _ in lst]

A, B, Cc = 'A', 'B', 'C'
ROWS = [
    # id, group, EN, FR, type, first year, confidence, sources, deltas
    ('champagne', 'Champagne', 'Champagne', 'Champagne', 'sp', 1900, A,
     [U_('Champagne'), X('BBR:Champagne'), X('ID:Champagne'), X('WSG:Champagne'), X('WE:Champagne', .5),
      X('GG:Champagne', .5)], {}),

    ('alsace_w', 'Alsace', 'Alsace White', 'Alsace Blanc', 'w', 1919, A,
     [U_('Alsace'), X('BBR:Alsace'), X('ID:Alsace', .5), X('WSG:Alsace'), X('WE:Alsace', .5), X('GG:Alsace', .5)], {}),
    ('alsace_r', 'Alsace', 'Alsace Red', 'Alsace Rouge', 'r', 1990, B,
     gen([U_('Alsace'), X('BBR:Alsace'), X('WSG:Alsace'), X('GG:Alsace', .5)]),
     {2003: .5, 2009: .5, 2015: .5, 2018: .5, 2020: .5, 2022: .5, 2008: -.5, 2010: -.5, 2013: -.5,
      2014: -.5, 2021: -1, 2024: -.5}),

    ('jura_w', 'Jura', 'Jura White', 'Jura Blanc', 'w', 1987, B, SJ,
     {2021: -1, 2016: -.5, 2017: -.5, 2024: -.5, 2003: -.5}),
    ('jura_r', 'Jura', 'Jura Red', 'Jura Rouge', 'r', 1987, B, SJ,
     {2021: -1.5, 2016: -.5, 2017: -.5, 2024: -1, 2013: -.5, 2014: -.5, 2018: .5, 2020: .5, 2022: .5}),
    ('jura_s', 'Jura', 'Jura Sweet / Vin Jaune', 'Jura Vin de Paille / Vin Jaune', 'sw', 1987, B, SJ,
     {2021: -1, 2016: -.5, 2017: -.5, 2024: -.5, 2003: .5, 2018: .5}),

    ('savoie_w', 'Savoie', 'Savoie White', 'Savoie Blanc', 'w', 1987, B, SJ + [X('ID:Savoie')],
     {2003: -.5, 2022: -.5}),
    ('savoie_r', 'Savoie', 'Savoie Red', 'Savoie Rouge', 'r', 1987, B, SJ + [X('ID:Savoie')],
     {2013: -.5, 2014: -.5, 2021: -.5, 2024: -.5, 2018: .5, 2020: .5}),

    ('cdn_w', 'Bourgogne', 'Côte de Nuits White', 'Côte de Nuits Blanc', 'w', 1900, B, gen(BURG_W), {}),
    ('cdn_r', 'Bourgogne', 'Côte de Nuits Red', 'Côte de Nuits Rouge', 'r', 1900, A,
     gen(BURG_R) + [X('WE:CdN red', 1.5)], {1986: .5, 1988: .5}),
    ('cdb_w', 'Bourgogne', 'Côte de Beaune White', 'Côte de Beaune Blanc', 'w', 1900, A, BURG_W, {}),
    ('cdb_r', 'Bourgogne', 'Côte de Beaune Red', 'Côte de Beaune Rouge', 'r', 1900, A,
     gen(BURG_R) + [X('WE:CdB red', 1.5)], {1986: -.5, 2013: -.5}),
    ('chal_w', 'Bourgogne', 'Côte Chalonnaise White', 'Côte Chalonnaise Blanc', 'w', 1978, B,
     gen(BURG_W) + [X('WE:Chalonnaise white', 1.5)], {}),
    ('chal_r', 'Bourgogne', 'Côte Chalonnaise Red', 'Côte Chalonnaise Rouge', 'r', 1978, B,
     gen(BURG_R) + [X('WE:Chalonnaise red', 1.5)], {2021: -.5}),
    ('chal_rs', 'Bourgogne', 'Côte Chalonnaise Rosé', 'Côte Chalonnaise Rosé', 'rs', 2010, Cc,
     ('derive', ['chal_w', 'chal_r']), {2003: -.5}),
    ('mac_w', 'Bourgogne', 'Mâconnais White', 'Mâconnais Blanc', 'w', 1978, A,
     gen(BURG_W, .7) + [X('WSG:Mâconnais', 1.5), X('WE:Mâconnais', 1.5)], {}),
    ('mac_r', 'Bourgogne', 'Mâconnais Red', 'Mâconnais Rouge', 'r', 1978, B, gen(BEAUJ), {}),
    ('mac_rs', 'Bourgogne', 'Mâconnais Rosé', 'Mâconnais Rosé', 'rs', 2010, Cc,
     ('derive', ['mac_w', 'mac_r']), {}),

    ('rhn_w', 'Rhône', 'Northern Rhône White', 'Rhône Nord Blanc', 'w', 1978, A,
     gen(RHN, .6) + [X('WE:N Rhône white', 1.5), X('WSG:Northern Rhône White', 1.5)],
     {2003: -1, 2009: -.5, 2002: .5, 2008: 1, 2013: .5, 2014: 1, 2021: .5}),
    ('rhn_r', 'Rhône', 'Northern Rhône Red', 'Rhône Nord Rouge', 'r', 1900, A,
     RHN + [X('WE:N Rhône red'), X('WSG:Northern Rhône Red')], {}),
    ('rhs_w', 'Rhône', 'Southern Rhône White', 'Rhône Sud Blanc', 'w', 1978, A,
     gen(RHS, .6) + [X('WE:S Rhône white', 1.5), X('WSG:Southern Rhône White', 1.5)],
     {2003: -1, 2002: 1, 2008: 1, 2013: .5, 2014: .5, 2021: 1}),
    ('rhs_r', 'Rhône', 'Southern Rhône Red', 'Rhône Sud Rouge', 'r', 1900, A,
     RHS + [X('WE:S Rhône red'), X('WSG:Southern Rhône Red')], {}),
    ('rhs_rs', 'Rhône', 'Southern Rhône Rosé', 'Rhône Sud Rosé', 'rs', 2010, Cc,
     ('derive', ['rhs_w', 'rhs_r']), {}),

    ('prov_w', 'Provence & Corse', 'Provence & Corsica White', 'Provence & Corse Blanc', 'w', 1990, B,
     gen(PROV), {2003: -.5, 2017: -.5, 2022: -.5}),
    ('prov_r', 'Provence & Corse', 'Provence & Corsica Red', 'Provence & Corse Rouge', 'r', 1990, A,
     gen(PROV) + [X('WE:Provence red', 1.5)], {}),
    ('prov_rs', 'Provence & Corse', 'Provence & Corsica Rosé', 'Provence & Corse Rosé', 'rs', 2005, B,
     gen(PROV), {2003: -.5}),

    ('lang_w', 'Languedoc', 'Languedoc White', 'Languedoc Blanc', 'w', 1990, B, gen(LR),
     {2003: -1, 2019: -.5, 2022: -.5}),
    ('lang_r', 'Languedoc', 'Languedoc Red', 'Languedoc Rouge', 'r', 1990, A, LR, {}),
    ('lang_rs', 'Languedoc', 'Languedoc Rosé', 'Languedoc Rosé', 'rs', 2010, Cc,
     ('derive', ['lang_w', 'lang_r']), {}),
    ('lang_s', 'Languedoc', 'Languedoc Sweet (Muscats)', 'Languedoc Doux (Muscats)', 'sw', 1990, Cc, gen(LR),
     {2003: -.5}),

    ('rous_w', 'Roussillon', 'Roussillon White', 'Roussillon Blanc', 'w', 1990, B, gen(LR),
     {2003: -1, 2022: -1, 2023: -.5, 2024: -1}),
    ('rous_r', 'Roussillon', 'Roussillon Red', 'Roussillon Rouge', 'r', 1990, B, gen(LR),
     {2022: -.5, 2023: -.5, 2024: -1}),
    ('rous_rs', 'Roussillon', 'Roussillon Rosé', 'Roussillon Rosé', 'rs', 2010, Cc,
     ('derive', ['rous_w', 'rous_r']), {}),
    ('rous_s', 'Roussillon', 'Roussillon Sweet (Vins Doux Naturels)', 'Roussillon Vins Doux Naturels', 'sw', 1990, Cc,
     gen(LR), {2023: -.5, 2024: -1}),

    ('swb_w', 'Sud-Ouest', 'South West · Bergerac & Dordogne White', 'Sud-Ouest · Bergerac & Dordogne Blanc', 'w',
     1990, Cc, gen(BDX_W), {}),
    ('swb_r', 'Sud-Ouest', 'South West · Bergerac & Dordogne Red', 'Sud-Ouest · Bergerac & Dordogne Rouge', 'r',
     1990, Cc, gen(BDX_R), {2017: -.5}),
    ('swb_s', 'Sud-Ouest', 'South West · Bergerac Sweet (Monbazillac…)', 'Sud-Ouest · Bergerac Liquoreux (Monbazillac…)',
     'sw', 1990, Cc, gen(SAUT), {}),
    ('swp_w', 'Sud-Ouest', 'South West · Garonne & Pyrénées White', 'Sud-Ouest · Garonne & Pyrénées Blanc', 'w',
     1990, Cc, gen(BDX_W), {2017: -.5}),
    ('swp_r', 'Sud-Ouest', 'South West · Garonne & Pyrénées Red (Cahors, Madiran…)',
     'Sud-Ouest · Garonne & Pyrénées Rouge (Cahors, Madiran…)', 'r', 1990, Cc, gen(BDX_R),
     {2001: .5, 2013: -.5, 2017: -.5}),
    ('swp_s', 'Sud-Ouest', 'South West · Garonne & Pyrénées Sweet (Jurançon…)',
     'Sud-Ouest · Garonne & Pyrénées Moelleux (Jurançon…)', 'sw', 1990, Cc, gen(SAUT), {}),

    ('bdx_w', 'Bordeaux', 'Bordeaux White', 'Bordeaux Blanc', 'w', 1900, A, BDX_W, {}),
    ('bdx_r', 'Bordeaux', 'Bordeaux Red', 'Bordeaux Rouge', 'r', 1900, A, BDX_R, {}),
    ('bdx_rs', 'Bordeaux', 'Bordeaux Rosé', 'Bordeaux Rosé', 'rs', 2010, Cc,
     ('derive', ['bdx_w', 'bdx_r']), {}),
    ('sauternes', 'Bordeaux', 'Sauternes & Barsac', 'Sauternes & Barsac', 'sw', 1900, A, SAUT, {}),

    ('loire_w', 'Loire', 'Loire White', 'Loire Blanc', 'w', 1900, A,
     [U_('LoireW'), X('WE:Loire dry white'), X('WSG:Loire Dry whites & reds')] + LOIRE, {}),
    ('loire_r', 'Loire', 'Loire Red', 'Loire Rouge', 'r', 1900, A,
     [U_('LoireR'), X('WE:Loire red'), X('WSG:Loire Dry whites & reds')] + gen(LOIRE), {}),
    ('loire_rs', 'Loire', 'Loire Rosé', 'Loire Rosé', 'rs', 2010, Cc, ('derive', ['loire_w', 'loire_r']), {}),
    ('loire_s', 'Loire', 'Loire Sweet', 'Loire Liquoreux', 'sw', 1900, A,
     [U_('LoireS'), X('WE:Loire sweet', 1.5)] + gen(LOIRE, .6), {}),
]

# ---------------------------------------------------------------- historical anchors
# great older vintages quoted in the user's spreadsheet ("Older notable vintages")
USER_NOTABLE = {
    'alsace_w': [1945, 1949, 1953, 1959, 1976, 1986],
    'sauternes': [1929, 1945, 1947, 1949, 1955, 1959, 1967, 1970, 1971, 1975, 1976, 1979, 1988, 1990, 2001],
    'bdx_r': [1900, 1928, 1929, 1945, 1947, 1949, 1959, 1961, 1966, 1970, 1975, 1982, 1990, 1995, 2000],
    'champagne': [1945, 1947, 1954, 1964, 1975, 1985, 1988, 1990, 1996, 2002],
    'cdb_w': [1945, 1947, 1949, 1952, 1955, 1962, 1966, 1968, 1970, 1985, 1990, 2002],
    'cdn_w': [1945, 1947, 1949, 1952, 1955, 1962, 1966, 1968, 1970, 1985, 1990, 2002],
    'cdn_r': [1945, 1947, 1949, 1953, 1959, 1961, 1962, 1966, 1969, 1971, 1976, 1978, 1985, 1990, 1996],
    'cdb_r': [1945, 1947, 1949, 1953, 1959, 1961, 1962, 1966, 1969, 1971, 1976, 1978, 1985, 1990, 1996],
    'rhn_r': [1945, 1947, 1949, 1952, 1953, 1959, 1961, 1971, 1978, 1988, 1990, 1999],
    'rhs_r': [1945, 1947, 1949, 1952, 1959, 1961, 1970, 1971, 1978, 1989, 1990],
}
# "Older great vintages" box of the Wine Enthusiast chart (public PDF)
WE_NOTABLE = {
    'bdx_r': [1996, 1990, 1989, 1986, 1985, 1982, 1978, 1970, 1966, 1964, 1961, 1959, 1955, 1953, 1949, 1947, 1945],
    'bdx_w': [1996, 1990, 1989, 1982, 1978, 1970, 1964, 1959],
    'sauternes': [1996, 1990, 1989, 1988, 1986, 1983, 1976, 1975, 1967],
    'cdn_r': [1996, 1985, 1978, 1976, 1971, 1969, 1959, 1952, 1949, 1947, 1945],
    'cdb_r': [1996, 1985, 1978, 1976, 1971, 1969, 1959, 1952, 1949, 1947, 1945],
    'cdb_w': [1995, 1992, 1990, 1989, 1986, 1983, 1982], 'cdn_w': [1995, 1992, 1990, 1989, 1986, 1983, 1982],
    'rhn_r': [1995, 1991, 1990, 1989, 1988, 1985, 1983, 1978, 1970, 1961],
    'rhs_r': [1985, 1983, 1981, 1978, 1967],
    'loire_w': [1996, 1985, 1978, 1976, 1971, 1969, 1959, 1947],
    'loire_s': [1996, 1985, 1978, 1976, 1971, 1969, 1959, 1947],
    'alsace_w': [1985, 1983, 1975],
    'champagne': [1996, 1995, 1990, 1985, 1982, 1979, 1971, 1964],
}
# legendary vintages from before each row's continuous coverage (historical accounts:
# Broadbent, Vintage Wine; Coates, The Wines of Burgundy / Bordeaux; appellation histories)
LEGENDS = {
    'loire_s': {1921: 5, 1947: 5, 1959: 5, 1976: 5, 1989: 5, 1990: 5, 1997: 5},
    'sauternes': {1921: 5, 1929: 5, 1937: 5, 1945: 5, 1947: 4.5, 1959: 5, 1967: 5, 2001: 5},
    'jura_s': {1947: 5, 1959: 5},
    'rhs_r': {1978: 5, 1989: 5, 1990: 5},
}
# only the very best pre-1900 vintages
PRE1900 = {
    'bdx_r': {1802: 4.5, 1811: 5, 1815: 4.5, 1825: 4.5, 1831: 4.5, 1841: 4.5, 1844: 4.5, 1848: 4.5, 1858: 4.5,
              1864: 5, 1865: 5, 1870: 5, 1874: 4.5, 1875: 5, 1893: 4.5, 1896: 4.5, 1899: 5},
    'sauternes': {1811: 5, 1847: 5, 1858: 4.5, 1869: 4.5, 1874: 4.5, 1893: 4.5, 1899: 4.5},
    'cdn_r': {1846: 4.5, 1858: 4.5, 1865: 5, 1869: 4.5},
    'cdb_r': {1846: 4.5, 1858: 4.5, 1865: 5, 1869: 4.5},
    'champagne': {1874: 5, 1880: 4.5, 1892: 4.5, 1893: 4.5, 1899: 4.5},
}


def half(x):
    return max(0.5, min(5.0, round(x * 2) / 2))


def build():
    U = read_user()
    S = raw_sources()
    C, fits = calibrate(S, U)
    for f, d in U.items():
        C['U:' + f] = d
    missing = sorted({k for r in ROWS if isinstance(r[7], list) for k, _, _ in r[7] if k not in C})
    if missing:
        print('WARNING missing sources:', missing)

    vals = {}
    for rid, grp, en, fr, typ, start, conf, src, deltas in ROWS:
        out = {}
        if isinstance(src, tuple):  # derived rosé
            a, b = vals[src[1][0]], vals[src[1][1]]
            for y in set(a) & set(b):
                if y >= start:
                    out[y] = half((a[y] + b[y]) / 2 - 0.01 + deltas.get(y, 0))
        else:
            years = {y for k, _, _ in src for y in C.get(k, {})}
            for y in years:
                if y < start:
                    continue
                num = den = 0
                for k, w, g in src:
                    v = C.get(k, {}).get(y)
                    if v is None:
                        continue
                    if g:
                        v = v + deltas.get(y, 0)
                    num += w * v
                    den += w
                if den:
                    out[y] = half(num / den)
        for y in USER_NOTABLE.get(rid, []):
            if y in out or y < start:
                out[y] = max(out.get(y, 0), 4.5)
            else:
                out[y] = 4.5
        for y in WE_NOTABLE.get(rid, []):
            if y < 1997:
                out[y] = max(out.get(y, 0), 4)
        for y, v in LEGENDS.get(rid, {}).items():
            out[y] = max(out.get(y, 0), v) if y >= start else v
        for y, v in PRE1900.get(rid, {}).items():
            out[y] = v
        vals[rid] = out

    rows = []
    for rid, grp, en, fr, typ, start, conf, src, deltas in ROWS:
        d = vals[rid]
        rows.append({'id': rid, 'g': grp, 'en': en, 'fr': fr, 't': typ, 'c': conf, 'from': start,
                     'n': ROW_NOTES.get(rid), 'v': {str(y): int(d[y] * 2) for y in sorted(d, reverse=True)}})
    data = {'rows': rows, 'notes': {str(k): v for k, v in YEAR_NOTES.items()},
            'fits': {k: [round(a, 3), round(b, 3), n] for k, (a, b, n) in fits.items()}}

    with open(os.path.join(HERE, 'template.html'), encoding='utf-8') as f:
        html = f.read()
    html = html.replace('/*__DATA__*/null', json.dumps(data, ensure_ascii=False, separators=(',', ':')))
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html)
    print('fits', data['fits'])
    print('wrote', OUT, len(html) // 1024, 'KB;', sum(len(r['v']) for r in rows), 'ratings')
    return vals


if __name__ == '__main__':
    vals = build()
    if '-v' in sys.argv:
        for rid, d in vals.items():
            print(f'{rid:10}', ' '.join(f"{y % 100:02d}:{d[y]:g}" for y in sorted(d, reverse=True) if y >= 1985))
