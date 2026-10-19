#!/usr/bin/env python3
"""Build Infos/Vine_and_Vineyard/Vine_Planting.html (chapter 4 — planting & the life of a vineyard).
Run:  python3 "WEB Site/Infos/Vine_and_Vineyard/_source/build_planting.py"
Static text is in planting_template.html; diagrams, tables and panels below.
Density figures come from the INAO cahiers des charges in « Cahiers des Charges/ ».
"""
from common import HERE, att, t, blk, base_css, pro_panel, chapter_nav, PRO_ICON, plate

OUT = HERE.parent / 'Vine_Planting.html'
INK = '#3b2a1e'
SERIF = 'Iowan Old Style,Palatino,Georgia,serif'
PLAN = '../../Plan%20Cadastraux/'


def lbl(x, y, pair, anchor='middle', size=14, fill=INK, weight='400', extra=''):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'font-family="{SERIF}" {extra}data-fr="{att(pair[0])}" data-en="{att(pair[1])}">{pair[0]}</text>')


# ------------------------------------------------------------ grafting techniques
STOCK = '#8a7258'; STOCK_D = '#5f4b37'; SCION = '#b98d4f'; SCION_D = '#7d5a2c'; BUD = '#6f8f34'


def bud(x, y, side=1):
    return (f'<path d="M{x} {y} q{7 * side} -5 {9 * side} -14 q{-8 * side} 2 {-9 * side} 14 Z" fill="{BUD}" stroke="#3f5f1a" stroke-width="1"/>')


def roots(x, y):
    return ''.join(f'<path d="M{x} {y} q{dx * .4} 12 {dx} 26" stroke="{STOCK_D}" stroke-width="1.6" fill="none"/>' for dx in (-18, -8, 0, 9, 19))


def grafting():
    s = ['<svg class="diagram" viewBox="0 0 680 330" role="img" aria-label="Techniques de greffage / Grafting techniques">']
    W = 170
    for i in range(4):
        s.append(f'<rect x="{i * W + 6}" y="6" width="{W - 12}" height="318" rx="12" fill="#f7f0e0" stroke="#e2d4b4"/>')
    # 1 omega
    cx = W // 2
    s.append(f'<rect x="{cx - 9}" y="40" width="18" height="96" rx="4" fill="{SCION}" stroke="{SCION_D}"/>' + bud(cx + 9, 70) + bud(cx - 9, 104, -1))
    s.append(f'<path d="M{cx - 9} 136 L{cx - 9} 240 L{cx + 9} 240 L{cx + 9} 136 L{cx + 4} 136 C{cx + 4} 146 {cx + 11} 150 {cx + 2} 158 C{cx - 4} 164 {cx - 12} 150 {cx - 4} 136 Z" fill="{STOCK}" stroke="{STOCK_D}"/>')
    s.append(f'<path d="M{cx - 4} 136 C{cx - 12} 150 {cx - 4} 164 {cx + 2} 158 C{cx + 11} 150 {cx + 4} 146 {cx + 4} 136" fill="{SCION}" stroke="{SCION_D}"/>')
    s.append(f'<rect x="{cx - 13}" y="120" width="26" height="52" rx="6" fill="#b5262e" opacity=".35"/>' + roots(cx, 240))
    # 2 whip and tongue
    cx = W + W // 2
    s.append(f'<path d="M{cx - 9} 40 L{cx + 9} 40 L{cx + 9} 120 L{cx - 9} 160 Z" fill="{SCION}" stroke="{SCION_D}"/>' + bud(cx + 9, 74))
    s.append(f'<path d="M{cx - 9} 160 L{cx + 9} 120 L{cx + 9} 240 L{cx - 9} 240 Z" fill="{STOCK}" stroke="{STOCK_D}"/>')
    s.append(f'<path d="M{cx - 9} 160 L{cx + 9} 120 M{cx - 3} 146 L{cx + 3} 138" stroke="#fff6e0" stroke-width="2"/>')
    s.append(f'<path d="M{cx - 12} 116 l24 -6 M{cx - 12} 126 l24 -6 M{cx - 12} 136 l24 -6 M{cx - 12} 146 l24 -6 M{cx - 12} 156 l24 -6 M{cx - 12} 166 l24 -6" stroke="#9aa04a" stroke-width="2.4"/>' + roots(cx, 240))
    # 3 cleft graft
    cx = 2 * W + W // 2
    s.append(f'<rect x="{cx - 22}" y="128" width="44" height="112" rx="6" fill="{STOCK}" stroke="{STOCK_D}"/>'
             f'<path d="M{cx} 128 L{cx} 170" stroke="{STOCK_D}" stroke-width="2"/>')
    s.append(f'<path d="M{cx - 7} 50 L{cx + 7} 50 L{cx + 7} 128 L{cx} 166 L{cx - 7} 128 Z" fill="{SCION}" stroke="{SCION_D}"/>' + bud(cx + 7, 82) + bud(cx - 7, 108, -1))
    s.append(f'<path d="M{cx - 22} 128 q22 -10 44 0" fill="#d9c58a" stroke="#a88f4f"/>' + roots(cx, 240))
    # 4 chip budding
    cx = 3 * W + W // 2
    s.append(f'<rect x="{cx - 12}" y="40" width="24" height="200" rx="5" fill="{STOCK}" stroke="{STOCK_D}"/>')
    s.append(f'<path d="M{cx + 12} 120 L{cx + 2} 128 L{cx + 2} 156 L{cx + 12} 164 Z" fill="{SCION}" stroke="{SCION_D}"/>' + bud(cx + 12, 146))
    s.append(f'<path d="M{cx - 14} 118 l28 0 M{cx - 14} 126 l28 0 M{cx - 14} 158 l28 0 M{cx - 14} 166 l28 0" stroke="#9aa04a" stroke-width="2.4"/>')
    s.append(f'<path d="M{cx - 12} 70 l24 0" stroke="#5f4b37" stroke-width="1.5" stroke-dasharray="3 3"/>' + roots(cx, 240))
    names = [(('Greffe oméga', 'Omega graft'), ('en pépinière, à la machine', 'nursery bench, by machine')),
             (('Greffe anglaise', 'Whip-and-tongue'), ('à la main, sur table', 'by hand, on the bench')),
             (('Greffe en fente', 'Cleft graft'), ('au champ, sur vieux pied', 'in the field, on an old vine')),
             (('Écussonnage', 'Chip budding'), ('au champ, pour surgreffer', 'in the field, to top-work'))]
    for i, (n, d) in enumerate(names):
        s.append(lbl(i * W + W // 2, 292, n, size=15, weight='600'))
        s.append(lbl(i * W + W // 2, 311, d, size=12.5, fill='#7a6650'))
    s.append(lbl(W // 2 + 30, 30, ('greffon', 'scion'), size=12.5, fill=SCION_D, anchor='start'))
    s.append(lbl(W // 2 + 30, 214, ('porte-greffe', 'rootstock'), size=12.5, fill=STOCK_D, anchor='start'))
    s.append(lbl(W // 2 + 22, 186, ('cire', 'wax'), size=12, fill='#8a2a2a', anchor='start'))
    s.append('</svg>')
    return ''.join(s)


# ------------------------------------------------------------ rootstocks
ROOTSTOCKS = [  # name, parentage, vigour 1-5, lime % active, drought 1-5, note fr/en
  ('Riparia Gloire de Montpellier', 'V. riparia', 1, 6, 1, ('Avance la maturité ; sols profonds et frais.', 'Advances ripening; deep, cool soils.')),
  ('101-14 MGt', 'riparia × rupestris', 2, 9, 2, ('Précoce, faible vigueur ; sols argileux et frais.', 'Early, low vigour; cool clay soils.')),
  ('3309 C', 'riparia × rupestris', 2, 11, 2, ('Très répandu, qualitatif ; craint la sécheresse.', 'Very widespread, quality-oriented; dislikes drought.')),
  ('420 A MGt', 'berlandieri × riparia', 2, 20, 2, ('Faible vigueur, maturité régulière ; Bordelais, Bourgogne.', 'Low vigour, steady ripening; Bordeaux, Burgundy.')),
  ('SO4', 'berlandieri × riparia', 4, 17, 3, ('Longtemps le plus planté ; vigoureux, risque de coulure.', 'Long the most planted; vigorous, coulure risk.')),
  ('161-49 C', 'riparia × berlandieri', 3, 25, 3, ('Sols calcaires de Bourgogne et Champagne.', 'Limestone soils of Burgundy and Champagne.')),
  ('41 B MGt', 'Chasselas × berlandieri', 3, 40, 3, ('Champion des sols très calcaires : Champagne, Cognac.', 'Champion of very limy soils: Champagne, Cognac.')),
  ('Fercal', 'berlandieri × hybride', 3, 40, 3, ('Tolérance au calcaire parmi les plus élevées.', 'Among the highest lime tolerances.')),
  ('110 R', 'berlandieri × rupestris', 4, 17, 4, ('Résiste bien à la sécheresse ; Midi.', 'Copes well with drought; the South.')),
  ('1103 P', 'berlandieri × rupestris', 4, 17, 4, ('Vigoureux et résistant au sec.', 'Vigorous and drought-tolerant.')),
  ('140 Ru', 'berlandieri × rupestris', 5, 20, 5, ('Très vigoureux, le plus résistant au sec.', 'Very vigorous, the most drought-tolerant.')),
]


def dots(n, col):
    return ''.join(f'<i class="pip{" on" if k < n else ""}" style="--c:{col}"></i>' for k in range(5))


def rootstock_rows():
    out = []
    for name, par, vig, lime, dry, note in ROOTSTOCKS:
        out.append(f'<tr><td class="rs-n">{name}</td><td class="rs-p"><i>{par}</i></td>'
                   f'<td>{dots(vig, "#7aa23c")}</td>'
                   f'<td><span class="lime"><b style="width:{lime / 40 * 100:.0f}%"></b></span><span class="lime-v">{lime} %</span></td>'
                   f'<td>{dots(dry, "#c0703a")}</td><td class="rs-note">{t(note)}</td></tr>')
    return ''.join(out)


# ------------------------------------------------------------ densities
DENSITY = [  # AOC, min vines/ha, link
  ('Chambertin, Gevrey-Chambertin', 9000, '../../Bourgogne%20Regions/Bourgogne%20climats/Gevrey-Chambertin%20%E2%80%94%20Climats%201er%20Cru%2C%20relief%205%20m%20%26%20climats%20communaux%20%C2%B7%20Carte.html'),
  ('Pauillac', 7000, PLAN + 'Bordeaux_LeftBank/Pauillac.html'),
  ('Muscadet', 6500, PLAN + 'Loire_Pays_Nantais/Muscadet.html'),
  ('Sancerre', 6100, PLAN + 'Loire_Centre/Sancerre.html'),
  ('Bordeaux', 4000, '../../Bordeaux.html'),
  ('Alsace', 4000, '../../Alsace.html'),
  ('Languedoc', 4000, '../../Languedoc.html'),
  ('Châteauneuf-du-Pape', 3000, PLAN + 'Cotes_du_Rhone_Sud/Chateauneuf-du-Pape.html'),
]


def density_bars():
    out = []
    for name, d, href in DENSITY:
        out.append(f'<div class="db-row"><a class="db-l" href="{href}">{name}</a><div class="db-track"><i style="width:{d / 10000 * 100:.0f}%"></i></div>'
                   f'<span class="db-v">{d:,}'.replace(',', ' ') + '</span></div>')
    return ''.join(out)


def plots():
    """Four 10 m × 10 m squares seen from above."""
    cases = [(('Bourgogne, grand cru', 'Burgundy grand cru'), 1.10, 1.00, '≈ 9 100'),
             (('Médoc, Pauillac', 'Médoc, Pauillac'), 1.40, 1.00, '≈ 7 100'),
             (('Bordeaux, Alsace, Languedoc', 'Bordeaux, Alsace, Languedoc'), 2.50, 1.00, '4 000'),
             (('Gobelet du Midi', 'Southern bush vines'), 1.80, 1.80, '≈ 3 100')]
    s = ['<svg class="diagram" viewBox="0 0 680 250" role="img" aria-label="Densités de plantation vues du dessus / Planting densities from above">']
    size = 140
    for i, (name, row, vine, dens) in enumerate(cases):
        x0 = 14 + i * 168; y0 = 16
        s.append(f'<rect x="{x0}" y="{y0}" width="{size}" height="{size}" rx="6" fill="#d9c49a" stroke="#a88f5f"/>')
        nr = int(10 / row); nv = int(10 / vine)
        for r in range(nr):
            y = y0 + (r + .5) * row / 10 * size
            if vine < 1.5:
                s.append(f'<line x1="{x0 + 3}" y1="{y:.1f}" x2="{x0 + size - 3}" y2="{y:.1f}" stroke="#8a7258" stroke-width="1"/>')
            for v in range(nv):
                x = x0 + (v + .5) * vine / 10 * size
                s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{3.6 if vine < 1.5 else 5}" fill="#5f8a34" stroke="#3f5f1a" stroke-width=".8"/>')
        s.append(lbl(x0 + size / 2, y0 + size + 24, name, size=13.5, weight='600'))
        s.append(f'<text x="{x0 + size / 2}" y="{y0 + size + 44}" text-anchor="middle" font-size="13" fill="#7a6650" font-family="{SERIF}">'
                 f'{str(row).replace(".", ",")} × {str(vine).replace(".", ",")} m · {dens}</text>')
    s.append(lbl(340, 244, ('Chaque carré représente 100 m² (10 × 10 m) ; chaque point, un pied de vigne. Valeurs en pieds par hectare.',
                            'Each square is 100 m² (10 × 10 m); each dot is one vine. Figures in vines per hectare.'), size=12, fill='#7a6650'))
    s.append('</svg>')
    return ''.join(s)


# ------------------------------------------------------------ trellis
def trellis():
    """User plate; the EN copy is relabelled from the FR original."""
    return (plate('img/planting/trellis_fr.webp', 'Anatomie d’un rang palissé', 1600, 900, 'wide L fr')
            + plate('img/planting/trellis_en.webp', 'Anatomy of a trellised row', 1600, 900, 'wide L en'))


# ------------------------------------------------------------ life curve
def life_curve():
    X = lambda a: 70 + (a * 20 if a <= 10 else 200 + (a - 10) * 360 / 70)   # first 10 years stretched
    Y = lambda v: 250 - v * 2.0  # value 0..100
    s = ['<svg class="diagram" viewBox="0 0 680 300" role="img" aria-label="La vie d’une vigne : rendement et concentration / A vine’s life: yield and concentration">']
    zones = [(0, 3, '#efe5cf', ('Jeune vigne', 'Young vine')), (3, 10, '#e7efd4', ('Montée en production', 'Coming into bearing')),
             (10, 35, '#dfeac8', ('Pleine production', 'Full production')), (35, 80, '#ece2d2', ('Vieilles vignes', 'Old vines'))]
    for a0, a1, col, name in zones:
        s.append(f'<rect x="{X(a0)}" y="30" width="{X(a1) - X(a0)}" height="220" fill="{col}"/>')
        s.append(lbl((X(a0) + X(a1)) / 2, 46, name, size=12.5 if a0 >= 3 else 11, weight='600', fill='#6b5a48'))
    s.append(f'<line x1="{X(0)}" y1="250" x2="{X(80)}" y2="250" stroke="#7a6650"/><line x1="{X(0)}" y1="30" x2="{X(0)}" y2="250" stroke="#7a6650"/>')
    for a in (0, 3, 5, 10, 20, 35, 50, 65, 80):
        s.append(f'<text x="{X(a)}" y="268" text-anchor="middle" font-size="12" fill="#7a6650" font-family="{SERIF}">{a}</text>')
    s.append(lbl(X(40), 290, ('âge de la vigne (années ; les dix premières sont dilatées)', 'vine age (years; the first ten are stretched)'), size=12.5, fill='#7a6650'))
    yld = [(0, 0), (2, 5), (3, 25), (5, 65), (8, 90), (12, 100), (25, 100), (35, 90), (50, 65), (65, 45), (80, 30)]
    qual = [(0, 10), (3, 25), (6, 45), (10, 60), (20, 75), (30, 85), (40, 92), (55, 96), (80, 98)]
    path = lambda pts: 'M' + ' L'.join(f'{X(a):.1f} {Y(v):.1f}' for a, v in pts)
    s.append(f'<path d="{path(yld)}" fill="none" stroke="#5f8a34" stroke-width="3.5" stroke-linejoin="round"/>')
    s.append(f'<path d="{path(qual)}" fill="none" stroke="#7d3f78" stroke-width="3.5" stroke-dasharray="9 6" stroke-linejoin="round"/>')
    s.append(f'<line x1="{X(40)}" y1="206" x2="{X(45)}" y2="206" stroke="#5f8a34" stroke-width="3.5"/>' + lbl(X(46), 211, ('Rendement', 'Yield'), anchor='start', size=13.5, fill='#4f6e22', weight='600'))
    s.append(f'<line x1="{X(40)}" y1="228" x2="{X(45)}" y2="228" stroke="#7d3f78" stroke-width="3.5" stroke-dasharray="9 6"/>' + lbl(X(46), 233, ('Concentration des raisins', 'Grape concentration'), anchor='start', size=13.5, fill='#5e2a5a', weight='600'))
    s.append(lbl(X(3) + 4, 240, ('← vin d’AOC possible', '← AOC wine allowed'), anchor='start', size=11.5, fill='#8a5a2b', extra='font-style="italic" '))
    s.append('</svg>')
    return ''.join(s)


# ------------------------------------------------------------ clone vs massal
def selection():
    """User plates: identical clonal vines vs varied massal-selection vines."""
    img = lambda f, alt: f'<img class="selimg" src="img/planting/{f}.webp" alt="{att(alt)}" loading="lazy" decoding="async" width="1072" height="459">'
    return (img('clone', 'Parcelle clonale : 40 pieds identiques / Clonal plot: 40 identical vines'),
            img('massal', 'Parcelle en sélection massale : pieds variés / Massal-selection plot: varied vines'))


PRO_GRAFT = [
  (('En pépinière', 'In the nursery'),
   ('Les bois de greffe et de porte-greffe sont récoltés en hiver. Greffage en mars-avril (à la machine, en oméga), trempage dans la paraffine, puis « stratification » 2 à 3 semaines à chaud et humide (≈ 25–30 °C) pour souder le greffon. Les plants passent l’été en pépinière, sont arrachés en hiver, triés et vendus comme « greffés-soudés ». Le traitement à l’eau chaude (50 °C, 45 min) protège contre la flavescence dorée.',
    'Scion and rootstock wood is harvested in winter. Grafting in March–April (by machine, omega cut), dipping in paraffin, then “callusing” for 2–3 weeks in warm, humid conditions (≈ 25–30 °C) to knit the union. Plants spend the summer in nursery rows, are lifted in winter, sorted and sold as “bench grafts”. Hot-water treatment (50 °C, 45 min) protects against flavescence dorée.')),
  (('Surgreffage', 'Top-working'),
   ('Greffer un nouveau cépage sur une vigne en place (fente, chip-bud, T-bud) permet de changer de variété sans arracher, en ne perdant qu’une à deux récoltes ; le système racinaire reste intact.',
    'Grafting a new variety onto an established vine (cleft, chip-bud, T-bud) changes the variety without uprooting, losing only one or two crops; the root system stays intact.')),
  (('Vignes franches de pied', 'Own-rooted vines'),
   ('Sans porte-greffe, la vigne n’est possible que là où le phylloxéra ne peut vivre : sables, sols inondables, quelques parcelles isolées. Voir le chapitre 7.',
    'Without a rootstock, vines can only grow where phylloxera cannot live: sand, floodable soils, a few isolated plots. See chapter 7.')),
]

PRO_ROOT = [
  (('Lire le tableau', 'Reading the table'),
   ('Vigueur conférée au greffon, tolérance au calcaire actif (en % du sol, valeurs indicatives) et résistance à la sécheresse. Le choix se fait après analyse de sol : taux de calcaire actif, indice de pouvoir chlorosant (IPC), profondeur, réserve en eau.',
    'Vigour given to the scion, tolerance of active lime (% in soil, indicative values) and drought tolerance. The choice follows a soil analysis: active lime, chlorosis potential index (IPC), depth, water reserve.')),
  (('Vigueur et qualité', 'Vigour and quality'),
   ('Un porte-greffe peu vigoureux (Riparia, 101-14, 3309) limite la végétation et avance la maturité : il convient aux sols profonds et fertiles. Un porte-greffe vigoureux (110 R, 140 Ru) compense un sol pauvre et sec.',
    'A low-vigour rootstock (Riparia, 101-14, 3309) limits growth and advances ripening: it suits deep, fertile soils. A vigorous rootstock (110 R, 140 Ru) compensates for a poor, dry soil.')),
  (('Les noms', 'The names'),
   ('Les codes désignent l’obtenteur et le numéro de semis : C = Couderc, MGt = Millardet et de Grasset, R = Richter, P = Paulsen, Ru = Ruggeri ; SO4 = « Selektion Oppenheim 4 ».',
    'The codes refer to the breeder and seedling number: C = Couderc, MGt = Millardet & de Grasset, R = Richter, P = Paulsen, Ru = Ruggeri; SO4 = “Selektion Oppenheim 4”.')),
]

PRO_MATERIAL = [
  (('Clones agréés', 'Certified clones'),
   ('En France, les clones sont sélectionnés et agréés (IFV, INRAE, ENTAV) puis numérotés : par exemple 115, 667 ou 777 pour le Pinot noir, 76, 95 ou 548 pour le Chardonnay. Ils garantissent un état sanitaire contrôlé, notamment l’absence des principaux virus.',
    'In France, clones are selected, certified (IFV, INRAE, ENTAV) and numbered: for example 115, 667 or 777 for Pinot Noir, 76, 95 or 548 for Chardonnay. They guarantee controlled health, in particular freedom from the main viruses.')),
  (('Virus et repos du sol', 'Viruses and soil rest'),
   ('Le court-noué, virus transmis par un nématode du sol (<i>Xiphinema index</i>), et l’enroulement sont les viroses majeures. Après arrachage, on laisse souvent le sol au repos plusieurs années, parfois avec des couverts végétaux, pour faire disparaître les racines et réduire les nématodes avant de replanter.',
    'Fanleaf, a virus spread by a soil nematode (<i>Xiphinema index</i>), and leafroll are the major virus diseases. After uprooting, the soil is often rested for several years, sometimes under cover crops, to clear old roots and reduce nematodes before replanting.')),
  (('Conservatoires', 'Collections'),
   ('Les interprofessions et les domaines entretiennent des conservatoires de vieilles vignes pour préserver la diversité génétique de chaque cépage, base des sélections massales de demain.',
    'Trade bodies and estates maintain collections of old vines to preserve each variety’s genetic diversity, the basis for future massal selections.')),
]

PRO_RULES = [
  (('Densité et écartements', 'Density and spacing'),
   ('Chaque cahier des charges fixe une densité minimale et des écartements maximaux : par exemple 9 000 pieds/ha et 1,25 m entre rangs en Chambertin, 7 000 pieds/ha et 1,50 m à Pauillac. En Champagne, les rangs ne dépassent pas 2 m, les pieds sont espacés de 0,70 à 1,50 m et la somme des deux écartements ne dépasse pas 3 m.',
    'Each specification sets a minimum density and maximum spacing: for example 9,000 vines/ha and 1.25 m between rows in Chambertin, 7,000 vines/ha and 1.50 m in Pauillac. In Champagne, rows are no more than 2 m apart, vines 0.70–1.50 m apart, and the two spacings may not add up to more than 3 m.')),
  (('Jeunes vignes', 'Young vines'),
   ('Dans la plupart des AOC, une vigne plantée avant le 31 juillet peut produire du vin d’appellation à partir de la 2<sup>e</sup> année suivant celle de sa plantation, soit sa 3<sup>e</sup> feuille. Certaines appellations sont plus strictes ou limitent le rendement des jeunes vignes.',
    'In most AOCs, a vine planted before 31 July may produce appellation wine from the 2nd year after its planting year, i.e. its 3rd leaf. Some appellations are stricter or cap young-vine yields.')),
  (('Pieds manquants', 'Missing vines'),
   ('Si plus de 20 % des pieds d’une parcelle sont morts ou manquants, son rendement autorisé est réduit en proportion : d’où l’importance de remplacer les ceps morts (complantation).',
    'If more than 20 % of a plot’s vines are dead or missing, its permitted yield is reduced accordingly: hence the importance of replacing dead vines (interplanting).')),
  (('Autorisations de plantation', 'Planting authorisations'),
   ('Depuis 2016, toute plantation nouvelle en Europe exige une autorisation ; la surface nouvelle est plafonnée chaque année à 1 % du vignoble national au plus. En France, les demandes passent par FranceAgriMer ; les replantations après arrachage sont autorisées sur la même surface.',
    'Since 2016, any new planting in Europe needs an authorisation; new area is capped each year at no more than 1 % of the national vineyard. In France, requests go through FranceAgriMer; replanting after uprooting is allowed on the same area.')),
]

SOURCES = [
  ('INAO, cahiers des charges des AOC Chambertin, Gevrey-Chambertin, Pauillac, Bordeaux, Champagne, Muscadet, Sancerre, Alsace, Languedoc, Châteauneuf-du-Pape.', 'INAO, specifications of the Chambertin, Gevrey-Chambertin, Pauillac, Bordeaux, Champagne, Muscadet, Sancerre, Alsace, Languedoc and Châteauneuf-du-Pape AOCs.'),
  ('IFV, <i>Catalogue des variétés et clones de vigne cultivés en France</i> ; fiches porte-greffes.', 'IFV, <i>Catalogue of grape varieties and clones grown in France</i>; rootstock sheets.'),
  ('Galet P., <i>Précis de viticulture</i> ; Reynier A., <i>Manuel de viticulture</i>.', 'Galet P., <i>Précis de viticulture</i>; Reynier A., <i>Manuel de viticulture</i>.'),
  ('Règlement (UE) n° 1308/2013, régime des autorisations de plantation de vigne ; FranceAgriMer.', 'Regulation (EU) No 1308/2013, vine planting authorisation scheme; FranceAgriMer.'),
]


def main():
    tpl = (HERE / 'planting_template.html').read_text()
    clone, massal = selection()
    rep = {
        '@@BASE_CSS@@': base_css(),
        '@@PRO_ICON@@': PRO_ICON,
        '@@GRAFTING@@': grafting(),
        '@@ROOTSTOCKS@@': rootstock_rows(),
        '@@CLONE@@': clone,
        '@@MASSAL@@': massal,
        '@@PLOTS@@': plots(),
        '@@DENSITY@@': density_bars(),
        '@@TRELLIS@@': trellis(),
        '@@LIFE@@': life_curve(),
        '@@PRO_GRAFT@@': pro_panel(PRO_GRAFT),
        '@@PRO_ROOT@@': pro_panel(PRO_ROOT),
        '@@PRO_MATERIAL@@': pro_panel(PRO_MATERIAL),
        '@@PRO_RULES@@': pro_panel(PRO_RULES),
        '@@CHAPTERS@@': chapter_nav(4),
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
