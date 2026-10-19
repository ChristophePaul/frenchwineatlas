#!/usr/bin/env python3
"""Build Infos/Vine_and_Vineyard/Vine_Harvest.html (chapter 9 — harvest).
Run:  python3 "WEB Site/Infos/Vine_and_Vineyard/_source/build_harvest.py"
Ripeness, yield and harvest rules come from the INAO cahiers des charges in « Cahiers des Charges/ ».
"""
from common import HERE, att, t, blk, base_css, pro_panel, chapter_nav, PRO_ICON, plate

OUT = HERE.parent / 'Vine_Harvest.html'
INK = '#3b2a1e'
SERIF = 'Iowan Old Style,Palatino,Georgia,serif'
PLAN = '../../Plan%20Cadastraux/'


def lbl(x, y, pair, anchor='middle', size=14, fill=INK, weight='400', extra=''):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'font-family="{SERIF}" paint-order="stroke" stroke="#fbf6ea" stroke-width="3" {extra}'
            f'data-fr="{att(pair[0])}" data-en="{att(pair[1])}">{pair[0]}</text>')


# ------------------------------------------------------------ ripening chart
def ripening():
    X = lambda w: 70 + w * 52      # weeks after véraison 0..10
    YS = lambda g: 300 - g * 0.9    # sugar g/L 0..260 → y 300..66
    YA = lambda a: 300 - a * 9.0    # total acidity g/L 0..28 → y 300..48
    s = ['<svg class="diagram" viewBox="0 0 680 360" role="img" aria-label="Évolution des raisins après la véraison / How grapes change after véraison">']
    windows = [(4.2, 5.4, '#e8e0f2', ('Effervescents', 'Sparkling')), (5.6, 6.8, '#eef3d6', ('Blancs secs', 'Dry whites')),
               (6.8, 8.6, '#f5dde0', ('Rouges', 'Reds')), (9.0, 10.0, '#f6ead0', ('Vendanges tardives', 'Late harvest'))]
    for k, (w0, w1, col, name) in enumerate(windows):
        s.append(f'<rect x="{X(w0):.1f}" y="40" width="{X(w1) - X(w0):.1f}" height="260" fill="{col}"/>')
        s.append(lbl((X(w0) + X(w1)) / 2, 72 if k % 2 == 0 else 54, name, size=12.5, weight='600', fill='#6b5a48'))
    s.append(f'<line x1="{X(0)}" y1="300" x2="{X(10)}" y2="300" stroke="#7a6650"/><line x1="{X(0)}" y1="40" x2="{X(0)}" y2="300" stroke="#7a6650"/>')
    for w in range(0, 11, 2):
        s.append(f'<text x="{X(w)}" y="318" text-anchor="middle" font-size="12" fill="#7a6650" font-family="{SERIF}">{w}</text>')
    s.append(lbl(X(5), 340, ('semaines après la véraison', 'weeks after véraison'), size=12.5, fill='#7a6650'))
    sugar = [(0, 25), (1, 70), (2, 115), (3, 150), (4, 175), (5, 195), (6, 210), (7, 222), (8, 232), (9, 240), (10, 250)]
    acid = [(0, 26), (1, 20), (2, 15), (3, 12), (4, 9.5), (5, 8), (6, 7), (7, 6.2), (8, 5.6), (9, 5.2), (10, 5)]
    phen = [(0, 20), (2, 30), (4, 60), (6, 110), (7, 150), (8, 185), (9, 205), (10, 215)]
    path = lambda pts, Y: 'M' + ' L'.join(f'{X(w):.1f} {Y(v):.1f}' for w, v in pts)
    s.append(f'<path d="{path(sugar, YS)}" fill="none" stroke="#c08a1a" stroke-width="3.5" stroke-linejoin="round"/>')
    s.append(f'<path d="{path(acid, YA)}" fill="none" stroke="#2f7d8c" stroke-width="3.5" stroke-linejoin="round"/>')
    s.append(f'<path d="{path(phen, YS)}" fill="none" stroke="#7d3f78" stroke-width="3" stroke-dasharray="8 5" stroke-linejoin="round"/>')
    s.append(lbl(X(1.15), YS(70) - 10, ('Sucres', 'Sugars'), anchor='end', size=13.5, fill='#9a6a12', weight='600'))
    s.append(lbl(X(1.3), YA(20) - 8, ('Acidité', 'Acidity'), anchor='start', size=13.5, fill='#2f6f7c', weight='600'))
    s.append(lbl(X(10), 162, ('Maturité des tanins', 'Tannin and colour'), anchor='end', size=13, fill='#5e2a5a', weight='600'))
    s.append(lbl(X(10), 178, ('et de la couleur', 'ripeness'), anchor='end', size=13, fill='#5e2a5a', weight='600'))
    s.append('</svg>')
    return ''.join(s)


# ------------------------------------------------------------ harvester (end view)
def harvester():
    """User plate with bilingual labels."""
    return plate('img/harvest/harvester.webp', 'Machine à vendanger et ses organes / Grape harvester and its parts', 1469, 982, 'wide')


RIPENESS = [  # AOC, link, sugar g/L, natural % vol
  ('Champagne', '../../Champagne.html', '143', '9 %'),
  ('Chablis', '../../Bourgogne%20Regions/Chablis_et_de_l_Auxerrois.html', '161 (1er cru : 170)', '10 % (10,5 %)'),
  ('Morgon', '../../Bourgogne%20Regions/Beaujolais.html', '180', '10,5 %'),
  ('Pauillac', PLAN + 'Bordeaux_LeftBank/Pauillac.html', '189 (Merlot) · 180', '—'),
  ('Sauternes', PLAN + 'Bordeaux_LeftBank/Sauternes.html', '221', '15 %'),
  ('Alsace VT · Riesling, Muscat', '../../Alsace.html', '244', '14,5 %'),
  ('Alsace VT · Gewurztraminer, Pinot gris', '../../Alsace.html', '270', '16 %'),
  ('Alsace SGN · Riesling, Muscat', '../../Alsace.html', '276', '16,4 %'),
  ('Alsace SGN · Gewurztraminer, Pinot gris', '../../Alsace.html', '306', '18,2 %'),
]

YIELDS = [  # AOC, link, rendement, butoir
  ('Chablis', '../../Bourgogne%20Regions/Chablis_et_de_l_Auxerrois.html', '60', '75'),
  ('Chablis premier cru', '../../Bourgogne%20Regions/Chablis_et_de_l_Auxerrois.html', '58', '73'),
  ('Pauillac', PLAN + 'Bordeaux_LeftBank/Pauillac.html', '57', '63'),
  ('Châteauneuf-du-Pape', PLAN + 'Cotes_du_Rhone_Sud/Chateauneuf-du-Pape.html', '35', '35'),
  ('Sauternes', PLAN + 'Bordeaux_LeftBank/Sauternes.html', '25', '—'),
]


def ripeness_rows():
    m1, m2 = t(('Sucre minimal : ', 'Minimum sugar: '), 'span', 'mh'), t(('Titre naturel : ', 'Natural alcohol: '), 'span', 'mh')
    return ''.join(f'<tr><td><a href="{h}">{n}</a></td><td class="num">{m1}{g}</td><td class="num">{m2}{a}</td></tr>' for n, h, g, a in RIPENESS)


def yield_rows():
    out = []
    for n, h, r, b in YIELDS:
        w = int(r) / 80 * 100
        m1, m2 = t(('Rendement : ', 'Base yield: '), 'span', 'mh'), t(('Butoir : ', 'Cap: '), 'span', 'mh')
        out.append(f'<tr><td><a href="{h}">{n}</a></td><td class="num">{m1}{r}</td><td class="num">{m2}{b}</td>'
                   f'<td class="bar"><span><i style="width:{w:.0f}%"></i></span></td></tr>')
    return ''.join(out)


HAND_MACHINE = [
  (('Rythme', 'Pace'), ('environ 1 ha par jour pour une équipe de 15 à 20 personnes', 'about 1 ha a day for a crew of 15–20'), ('1 ha en 2 à 3 heures', '1 ha in 2–3 hours')),
  (('Vendange', 'Crop'), ('grappes entières, intactes', 'whole, intact bunches'), ('baies détachées, un peu de jus', 'loose berries, some juice')),
  (('Tri', 'Sorting'), ('dès la vigne, grappe par grappe', 'in the vineyard, bunch by bunch'), ('au chai, ou par tri optique embarqué', 'at the winery, or by on-board optical sorting')),
  (('Souplesse', 'Flexibility'), ('pentes, terrasses, tries successives', 'slopes, terraces, successive passes'), ('nuit, fraîcheur, réactivité face à la pluie', 'at night, in the cool, quick response to rain')),
  (('Coût', 'Cost'), ('élevé : main-d’œuvre, hébergement', 'high: labour, accommodation'), ('investissement, mais coût à l’hectare bas', 'capital outlay, but low cost per hectare')),
  (('Obligatoire', 'Compulsory'), ('Châteauneuf-du-Pape, Sauternes, crémants, lieux-dits d’Alsace en Pinot gris et noir ; de fait en Champagne et dans les crus du Beaujolais', 'Châteauneuf-du-Pape, Sauternes, crémants, Alsace lieu-dit Pinot Gris and Noir; in practice in Champagne and the Beaujolais crus'), ('—', '—')),
]


def hand_machine():
    return ''.join(f'<tr><td>{t(a)}</td><td>{t(h)}</td><td>{t(m)}</td></tr>' for a, h, m in HAND_MACHINE)


PRO_RIPE = [
  (('Le contrôle de maturité', 'Ripeness sampling'),
   ('Chaque semaine après la véraison, on prélève environ 200 baies par parcelle, prises au hasard sur les deux faces du rang, à différentes hauteurs des grappes. On les presse et on mesure le sucre (réfractomètre), l’acidité totale, le pH et parfois l’acide malique et l’azote.',
    'Every week after véraison, about 200 berries per plot are sampled at random from both sides of the row and different parts of the bunches. They are pressed and sugar (refractometer), total acidity, pH and sometimes malic acid and nitrogen are measured.')),
  (('Au-delà du sucre', 'Beyond sugar'),
   ('La maturité phénolique (couleur, tanins) se suit par analyses d’extractibilité des anthocyanes et, surtout, en goûtant les baies : peau qui se déchire facilement, pulpe qui se détache, pépins bruns et croquants, tanins non asséchants.',
    'Phenolic ripeness (colour, tannins) is tracked by anthocyanin extractability tests and, above all, by tasting berries: skin that tears easily, pulp that comes away, brown crunchy seeds, tannins that no longer dry the mouth.')),
  (('Les minimums des AOC', 'AOC minimums'),
   ('Chaque cahier des charges fixe une richesse minimale en sucre des raisins et un titre alcoométrique naturel minimum ; le tableau ci-dessous en donne des exemples, tirés des cahiers des charges.',
    'Each specification sets a minimum grape sugar content and a minimum natural alcohol; the table below gives examples, taken from the specifications.')),
]

PRO_YIELD = [
  (('Rendement et rendement butoir', 'Base yield and cap'),
   ('Le « rendement » est le volume de vin d’appellation autorisé par hectare ; l’INAO peut l’ajuster chaque année, sur demande de l’ODG, sans dépasser le « rendement butoir ». Au-delà, la récolte perd le droit à l’appellation et doit être distillée ou détruite.',
    'The “rendement” is the volume of appellation wine permitted per hectare; INAO can adjust it each year, at the growers’ body’s request, without exceeding the “rendement butoir” (cap). Beyond that, the crop loses appellation status and must be distilled or destroyed.')),
  (('Volume complémentaire individuel', 'Individual reserve'),
   ('Dans certaines appellations, le VCI permet de mettre de côté, les bonnes années, un petit volume au-delà du rendement, pour compenser une récolte future déficitaire (gel, grêle).',
    'In some appellations, the VCI lets growers set aside, in good years, a small volume above the base yield, to make up for a future short crop (frost, hail).')),
  (('Champagne', 'Champagne'),
   ('Le rendement y est exprimé en kilos de raisin par hectare et fixé chaque année par l’interprofession, dans la limite d’une charge maximale de 19 700 kg/ha prévue par le cahier des charges ; 160 kg de raisins donnent au plus 102 litres de moût.',
    'There the yield is expressed in kilos of grapes per hectare and set every year by the trade body, within a maximum load of 19,700 kg/ha in the specification; 160 kg of grapes give at most 102 litres of must.')),
]

SOURCES = [
  ('INAO, cahiers des charges des AOC Champagne, Chablis, Morgon, Pauillac, Sauternes, Alsace, Crémant d’Alsace, Châteauneuf-du-Pape.', 'INAO, specifications of the Champagne, Chablis, Morgon, Pauillac, Sauternes, Alsace, Crémant d’Alsace and Châteauneuf-du-Pape AOCs.'),
  ('Code rural et de la pêche maritime, articles D. 644-25 et D. 645-7 (rendements), date de début des vendanges.', 'French rural code, articles D. 644-25 and D. 645-7 (yields), harvest start date.'),
  ('IFV, guide des contrôles de maturité ; Ribéreau-Gayon P. et al., <i>Traité d’œnologie</i>, Dunod.', 'IFV, ripeness-monitoring guide; Ribéreau-Gayon P. et al., <i>Handbook of Enology</i>, Dunod/Wiley.'),
]


def main():
    tpl = (HERE / 'harvest_template.html').read_text()
    rep = {
        '@@BASE_CSS@@': base_css(),
        '@@PRO_ICON@@': PRO_ICON,
        '@@RIPENING@@': ripening(),
        '@@HARVESTER@@': harvester(),
        '@@RIPENESS@@': ripeness_rows(),
        '@@YIELDS@@': yield_rows(),
        '@@HAND_MACHINE@@': hand_machine(),
        '@@PRO_RIPE@@': pro_panel(PRO_RIPE),
        '@@PRO_YIELD@@': pro_panel(PRO_YIELD),
        '@@CHAPTERS@@': chapter_nav(9),
        '@@SOURCES@@': ''.join(f'<li>{t(s)}</li>' for s in SOURCES),
    }
    html = tpl
    for k, v in rep.items():
        html = html.replace(k, v)
    assert '@@' not in html, html[html.index('@@'):html.index('@@') + 40]
    OUT.write_text(html)
    print(f'{OUT.name}: {len(html) // 1024} KB')


if __name__ == '__main__':
    main()
