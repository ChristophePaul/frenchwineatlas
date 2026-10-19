#!/usr/bin/env python3
"""Build Infos/Vine_and_Vineyard/Vine_Pruning.html (chapter 5 — training & pruning).
Run:  python3 "WEB Site/Infos/Vine_and_Vineyard/_source/build_pruning.py"
Pruning rules come from the INAO cahiers des charges in « Cahiers des Charges/ ».
"""
from common import HERE, att, t, blk, base_css, plate, pro_panel, chapter_nav, PRO_ICON

OUT = HERE.parent / 'Vine_Pruning.html'
INK = '#3b2a1e'
SERIF = 'Iowan Old Style,Palatino,Georgia,serif'
PLAN = '../../Plan%20Cadastraux/'
OLD = '#5f4b37'; CANE = '#a0703a'; BUDC = '#6f8f34'; WIRE = '#8a8a8a'; GONE = '#cdbfa6'


def lbl(x, y, pair, anchor='middle', size=14, fill=INK, weight='400', extra=''):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'font-family="{SERIF}" paint-order="stroke" stroke="#fbf6ea" stroke-width="3" {extra}'
            f'data-fr="{att(pair[0])}" data-en="{att(pair[1])}">{pair[0]}</text>')


def buds(pts, r=3.2):
    return ''.join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{BUDC}" stroke="#3f5f1a" stroke-width=".8"/>' for x, y in pts)


# ------------------------------------------------------------ before / after (single Guyot)
def before_after():
    s = ['<svg class="diagram" viewBox="0 0 680 330" role="img" aria-label="Un cep avant et après la taille Guyot simple / A vine before and after single-Guyot pruning">']
    for ox, title in ((0, ('Avant la taille (janvier)', 'Before pruning (January)')), (340, ('Après la taille', 'After pruning'))):
        s.append(f'<rect x="{ox + 8}" y="8" width="324" height="314" rx="12" fill="#f7f0e0" stroke="#e2d4b4"/>')
        s.append(lbl(ox + 170, 34, title, size=16, weight='600'))
        s.append(f'<rect x="{ox + 8}" y="276" width="324" height="46" rx="0" fill="#cdb48a"/><line x1="{ox + 20}" y1="200" x2="{ox + 320}" y2="200" stroke="{WIRE}" stroke-width="1.6"/>')
        s.append(f'<path d="M{ox + 120} 276 C{ox + 116} 250 {ox + 126} 225 {ox + 120} 205" stroke="{OLD}" stroke-width="11" fill="none" stroke-linecap="round"/>')
    # before: last year's cane on the wire (old, to be removed) + many canes growing up from it and the spur
    canes = [(130, 198, 150, 60), (150, 198, 180, 70), (176, 199, 215, 80), (204, 200, 250, 70), (232, 200, 280, 90), (262, 200, 305, 110),
             (114, 200, 92, 70), (126, 196, 116, 56)]
    s.append(f'<path d="M120 204 L300 200" stroke="{OLD}" stroke-width="6" stroke-linecap="round"/>')
    for x0, y0, x1, y1 in canes:
        s.append(f'<path d="M{x0} {y0} C{x0 + 4} {y0 - 50} {x1 - 6} {y1 + 40} {x1} {y1}" stroke="{CANE}" stroke-width="3.6" fill="none" stroke-linecap="round"/>')
    # after: removed wood ghosted, one new cane bent on the wire + one spur
    o = 340
    s.append(f'<path d="M{o + 120} 204 L{o + 300} 200" stroke="{GONE}" stroke-width="6" stroke-linecap="round" stroke-dasharray="2 5"/>')
    for x0, y0, x1, y1 in canes[2:6]:
        s.append(f'<path d="M{o + x0} {y0} C{o + x0 + 4} {y0 - 50} {o + x1 - 6} {y1 + 40} {o + x1} {y1}" stroke="{GONE}" stroke-width="3" fill="none" stroke-dasharray="2 5"/>')
    s.append(f'<path d="M{o + 122} 204 C{o + 130} 175 {o + 150} 196 {o + 165} 198 L{o + 300} 198" stroke="{CANE}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    s.append(buds([(o + 150 + k * 18.5, 192) for k in range(8)]))
    s.append(f'<path d="M{o + 116} 206 L{o + 104} 182" stroke="{CANE}" stroke-width="5" stroke-linecap="round"/>' + buds([(o + 110, 194), (o + 105, 184)]))
    s.append(f'<path d="M{o + 104} 182 l-5 -4 l9 0 Z" fill="{CANE}"/>')
    s.append(lbl(o + 230, 228, ('Baguette : 8 yeux', 'Cane: 8 buds'), size=14, weight='600'))
    s.append(lbl(o + 230, 246, ('les rameaux de l’année en naîtront', 'this year’s shoots will grow from them'), size=12.5, fill='#7a6650'))
    s.append(lbl(o + 80, 158, ('Courson : 2 yeux', 'Spur: 2 buds'), size=14, weight='600'))
    s.append(lbl(o + 80, 174, ('la baguette de l’an prochain', 'next year’s cane'), size=12.5, fill='#7a6650'))
    s.append(lbl(o + 250, 120, ('bois retiré (pointillés)', 'wood removed (dotted)'), size=12.5, fill='#9a8a6e', extra='font-style="italic" '))
    s.append(lbl(225, 228, ('Sarments de l’an dernier', 'Last year’s canes'), size=14, weight='600'))
    s.append(lbl(225, 246, ('il faut choisir lesquels garder', 'the grower must choose which to keep'), size=12.5, fill='#7a6650'))
    s.append('</svg>')
    return ''.join(s)


# ------------------------------------------------------------ mini system diagrams (viewBox 160 × 110)
def mini(kind):
    s = ['<svg class="mini" viewBox="0 0 160 93" aria-hidden="true">']
    trunk = lambda x, top: f'<path d="M{x} 92 L{x} {top}" stroke="{OLD}" stroke-width="7" stroke-linecap="round"/>'
    wire = lambda y: f'<line x1="6" y1="{y}" x2="154" y2="{y}" stroke="{WIRE}" stroke-width="1.2"/>'
    arm = lambda x0, y0, x1, y1, w=5: f'<path d="M{x0} {y0} L{x1} {y1}" stroke="{OLD}" stroke-width="{w}" stroke-linecap="round"/>'
    cane = lambda x0, y0, x1, y1: f'<path d="M{x0} {y0} L{x1} {y1}" stroke="{CANE}" stroke-width="3.4" stroke-linecap="round"/>'

    def spur(x, y, dx=0, n=2):
        return (f'<path d="M{x} {y} L{x + dx} {y - 12}" stroke="{CANE}" stroke-width="3.4" stroke-linecap="round"/>'
                + buds([(x + dx * (k + 1) / (n + .5), y - 12 * (k + 1) / (n + .5)) for k in range(n)], 2.6))

    def along(x0, y0, x1, y1, n):
        return buds([(x0 + (x1 - x0) * (k + .7) / n, y0 + (y1 - y0) * (k + .7) / n - 4) for k in range(n)], 2.6)

    if kind == 'gobelet':
        s.append(trunk(80, 62))
        for dx in (-34, -12, 12, 34):
            s.append(arm(80, 62, 80 + dx, 40) + spur(80 + dx, 40, dx * .15))
    elif kind == 'guyot1':
        s.append(wire(50) + trunk(70, 54) + cane(70, 50, 146, 50) + along(70, 50, 146, 50, 8) + spur(66, 54, -6))
    elif kind == 'guyot2':
        s.append(wire(50) + trunk(80, 54) + cane(80, 50, 150, 50) + cane(80, 50, 10, 50)
                 + along(80, 50, 150, 50, 6) + along(80, 50, 10, 50, 6) + spur(74, 54, -5) + spur(86, 54, 5))
    elif kind == 'royat':
        s.append(wire(50) + trunk(30, 52) + arm(30, 52, 150, 52, 6))
        s.append(''.join(spur(x, 50, 2) for x in (50, 78, 106, 134)))
    elif kind == 'chablis':
        s.append(trunk(80, 78))
        for ex, ey in ((30, 50), (60, 44), (100, 44), (130, 50)):
            s.append(arm(80, 78, ex, ey, 4) + cane(ex, ey, ex + (ex - 80) * .35, ey - 20) + along(ex, ey, ex + (ex - 80) * .35, ey - 20, 4))
        s.append(spur(82, 80, 3))
    elif kind == 'marne':
        s.append(wire(50) + trunk(40, 54) + arm(40, 52, 110, 52, 4))
        s.append(cane(110, 52, 152, 50) + along(110, 52, 152, 50, 5))
        s.append(cane(46, 54, 92, 34) + along(46, 54, 92, 34, 6) + spur(38, 56, -5, 3))
    elif kind == 'medoc':
        s.append(wire(56) + trunk(80, 70) + arm(80, 70, 50, 60, 5) + arm(80, 70, 110, 60, 5))
        s.append(cane(50, 58, 12, 56) + along(50, 58, 12, 56, 4) + cane(110, 58, 148, 56) + along(110, 58, 148, 56, 4))
        s.append(spur(56, 60, -2) + spur(104, 60, 2))
    elif kind == 'eventail':
        s.append(wire(40) + trunk(80, 80))
        for ex, ey in ((22, 46), (56, 36), (104, 36), (138, 46)):
            s.append(arm(80, 80, ex, ey, 4) + spur(ex, ey, (ex - 80) * .1))
    elif kind == 'echalas':
        s.append(f'<rect x="96" y="6" width="4" height="98" fill="#c9b07a"/>' + trunk(84, 60))
        for dx in (-14, 0, 14):
            s.append(arm(84, 60, 84 + dx, 44, 4) + spur(84 + dx, 44, dx * .2))
        s.append('<path d="M86 30 l12 0 M86 70 l12 0" stroke="#9aa04a" stroke-width="2.4"/>')
    s.append('</svg>')
    return ''.join(s)


SYSTEMS = [  # kind, name, family, desc, where, rule example
  ('gobelet', ('Gobelet', 'Bush vine (gobelet)'), 'courte',
   ('Sans fil ni piquet : 3 à 6 bras courts en couronne, chacun portant un courson. Le cep se tient seul, compact, bien adapté au vent et à la chaleur.', 'No wires or posts: 3–6 short arms in a crown, each carrying a spur. The vine stands on its own, compact, well suited to wind and heat.'),
   ('Beaujolais, Rhône méridional, Languedoc, Roussillon, Provence', 'Beaujolais, southern Rhône, Languedoc, Roussillon, Provence'),
   ('Châteauneuf-du-Pape : obligatoire pour Grenache et Mourvèdre, coursons à 2 yeux.', 'Châteauneuf-du-Pape: compulsory for Grenache and Mourvèdre, 2-bud spurs.')),
  ('guyot1', ('Guyot simple', 'Single Guyot'), 'longue',
   ('Une baguette de 6 à 10 yeux couchée sur le fil, et un courson de rappel à 2 yeux qui fournira la baguette de l’an prochain. Inventé par Jules Guyot au XIX<sup>e</sup> siècle.', 'One cane of 6–10 buds laid along the wire, plus a 2-bud renewal spur that provides next year’s cane. Devised by Jules Guyot in the 19th century.'),
   ('Bourgogne, Loire, Alsace, Jura, Savoie', 'Burgundy, Loire, Alsace, Jura, Savoie'),
   ('Sancerre : au plus 8 yeux sur le long bois, 10 par pied.', 'Sancerre: at most 8 buds on the cane, 10 per vine.')),
  ('guyot2', ('Guyot double', 'Double Guyot'), 'longue',
   ('Deux baguettes opposées, chacune avec son courson : plus de charge par pied, pour les vignes plus espacées.', 'Two opposite canes, each with its spur: more crop per vine, for wider-spaced vines.'),
   ('Bordelais, Sud-Ouest, Loire, Alsace', 'Bordeaux, South-West, Loire, Alsace'),
   ('Sancerre : deux baguettes de 4 yeux au plus, 12 yeux par pied.', 'Sancerre: two canes of at most 4 buds, 12 buds per vine.')),
  ('royat', ('Cordon de Royat', 'Royat cordon'), 'courte',
   ('Un bras permanent couché le long du fil, garni de coursons courts régulièrement espacés. Végétation bien répartie, taille rapide.', 'A permanent arm laid along the wire, set with short, evenly spaced spurs. Well-spread foliage, quick pruning.'),
   ('Bourgogne, Champagne, Languedoc', 'Burgundy, Champagne, Languedoc'),
   ('Champagne : coursons à 3 yeux au plus, espacés d’au moins 15 cm.', 'Champagne: spurs of at most 3 buds, at least 15 cm apart.')),
  ('chablis', ('Taille Chablis', 'Chablis pruning'), 'longue',
   ('Plusieurs charpentes en éventail, chacune terminée par un « prolongement » de quelques yeux, et un courson de rajeunissement (« rachet ») à la base.', 'Several fan-shaped arms, each ending in a short fruiting “extension”, plus a renewal spur (“rachet”) at the base.'),
   ('Chablis, Champagne (Côte des Blancs)', 'Chablis, Champagne (Côte des Blancs)'),
   ('Champagne : prolongements à 5 yeux au plus, une charpente par 30 cm.', 'Champagne: extensions of at most 5 buds, one arm per 30 cm.')),
  ('marne', ('Vallée de la Marne', 'Vallée de la Marne'), 'longue',
   ('Propre à la Champagne et surtout au Meunier : un courson, une baguette lancée sur le courson de l’an passé et un prolongement au bout de l’ancienne baguette.', 'Specific to Champagne and mainly Meunier: a spur, a cane grown from last year’s spur, and an extension at the end of the old cane.'),
   ('Champagne (vallée de la Marne)', 'Champagne (Marne valley)'),
   ('Champagne : courson 3 yeux, baguette 9 yeux, prolongement 6 yeux au plus.', 'Champagne: spur 3, cane 9, extension 6 buds at most.')),
  ('medoc', ('Médocaine à astes', 'Médoc pruning (astes)'), 'longue',
   ('Variante bordelaise du Guyot double : deux bras courts portent chacun une « aste » (baguette courte) et un « cot » (courson) de retour.', 'Bordeaux variant of double Guyot: two short arms each carry an “aste” (short cane) and a return “cot” (spur).'),
   ('Médoc, Graves', 'Médoc, Graves'),
   ('Pauillac : astes à 4 yeux au plus, cots à 2 yeux, 12 yeux par pied.', 'Pauillac: astes of at most 4 buds, 2-bud cots, 12 buds per vine.')),
  ('eventail', ('Éventail', 'Fan'), 'courte',
   ('Les bras s’étalent dans le plan du rang comme un éventail, chacun portant des coursons.', 'The arms spread along the row like a fan, each carrying spurs.'),
   ('Bourgogne, Beaujolais, Bordelais', 'Burgundy, Beaujolais, Bordeaux'),
   ('Pauillac : éventail à quatre bras autorisé.', 'Pauillac: four-armed fan permitted.')),
  ('echalas', ('Sur échalas', 'On stakes'), 'courte',
   ('Chaque cep est attaché à un ou deux piquets de bois (échalas), sans fil : la seule solution sur les terrasses les plus raides.', 'Each vine is tied to one or two wooden stakes, without wires: the only option on the steepest terraces.'),
   ('Côte-Rôtie, Condrieu, Hermitage, Moselle', 'Côte-Rôtie, Condrieu, Hermitage, Moselle'),
   ('Côte-Rôtie : sur échalas ou palissage relevé, 10 yeux par pied au plus.', 'Côte-Rôtie: on stakes or raised trellis, at most 10 buds per vine.')),
]


def system_cards():
    fam = {'courte': (('Taille courte', 'Short pruning'), '#6f8b1e'), 'longue': (('Taille longue', 'Long pruning'), '#a0283c')}
    out = []
    for kind, name, f, desc, where, rule in SYSTEMS:
        fl, col = fam[f]
        out.append(f'<article class="sys" style="--c:{col}"><div class="sys-fig">{mini(kind)}</div><div class="sys-b">'
                   f'<span class="chip" style="--c:{col}">{t(fl)}</span><h3>{t(name)}</h3>{blk(desc)}'
                   f'<p class="sys-w">{t(where)}</p><p class="sys-r"><b>{t(("Règle AOC : ", "AOC rule: "))}</b>{t(rule)}</p></div></article>')
    return ''.join(out)


# ------------------------------------------------------------ sap-flow pruning
def sapflow():
    s = ['<svg class="diagram" viewBox="0 0 680 280" role="img" aria-label="Taille respectueuse des flux de sève / Pruning that respects sap flow">']
    for ox, title, good in ((0, ('À éviter', 'Avoid'), False), (340, ('À privilégier', 'Prefer'), True)):
        col = '#2f7d4a' if good else '#a0283c'
        s.append(f'<rect x="{ox + 8}" y="8" width="324" height="264" rx="12" fill="#f7f0e0" stroke="{col}" stroke-width="1.5"/>')
        s.append(lbl(ox + 170, 34, title, size=16, weight='600', fill=col))
        s.append(f'<path d="M{ox + 60} 192 C{ox + 57} 175 {ox + 63} 162 {ox + 60} 150 L{ox + 300} 150" stroke="{OLD}" stroke-width="22" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        if not good:
            for x in (120, 190, 260):
                s.append(f'<ellipse cx="{ox + x}" cy="140" rx="10" ry="5" fill="#e9d9b8" stroke="#8a6a44"/>'
                         f'<path d="M{ox + x - 10} 141 L{ox + x} 166 L{ox + x + 10} 141 Z" fill="#c9a87a" opacity=".9"/>')
            for x in (155, 225):
                s.append(f'<ellipse cx="{ox + x}" cy="160" rx="10" ry="5" fill="#e9d9b8" stroke="#8a6a44"/>'
                         f'<path d="M{ox + x - 10} 159 L{ox + x} 134 L{ox + x + 10} 159 Z" fill="#c9a87a" opacity=".9"/>')
            s.append(f'<path d="M{ox + 70} 150 L{ox + 108} 150" stroke="#3f7fae" stroke-width="3" marker-end="url(#sf)"/>'
                     f'<path d="M{ox + 112} 150 l6 -3 M{ox + 112} 150 l6 3" stroke="#a0283c" stroke-width="2.4"/>')
            s.append(lbl(ox + 170, 214, ('Grosses plaies rases, des deux côtés :', 'Large flush cuts on both sides:'), size=13.5))
            s.append(lbl(ox + 170, 232, ('les cônes de bois mort coupent la sève', 'dead-wood cones cut off the sap'), size=13.5))
            s.append(lbl(ox + 170, 250, ('et ouvrent la porte à l’esca.', 'and let esca in.'), size=13.5))
        else:
            for x in (130, 200, 270):
                s.append(f'<path d="M{ox + x} 140 L{ox + x} 116" stroke="{OLD}" stroke-width="7" stroke-linecap="round"/>'
                         f'<ellipse cx="{ox + x}" cy="115" rx="4" ry="2" fill="#e9d9b8" stroke="#8a6a44"/>'
                         f'<path d="M{ox + x - 3} 117 L{ox + x} 130 L{ox + x + 3} 117 Z" fill="#c9a87a"/>')
            s.append(f'<path d="M{ox + 70} 156 L{ox + 290} 156" stroke="#3f7fae" stroke-width="3" stroke-dasharray="8 5" marker-end="url(#sf)"/>')
            s.append(lbl(ox + 170, 214, ('Petites plaies sur le dessus du bras,', 'Small cuts on top of the arm,'), size=13.5))
            s.append(lbl(ox + 170, 232, ('on laisse un chicot qui sèche seul :', 'leaving a stub that dries out on its own:'), size=13.5))
            s.append(lbl(ox + 170, 250, ('la sève circule sans obstacle.', 'sap flows without obstacles.'), size=13.5))
    s.insert(1, '<defs><marker id="sf" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="#3f7fae" stroke-width="1.8"/></marker></defs>')
    s.append('</svg>')
    return ''.join(s)


RULES = [  # AOC, link, systems fr/en, max
  ('Chambertin', '../../Bourgogne%20Regions/Bourgogne%20climats/Gevrey-Chambertin%20%E2%80%94%20Climats%201er%20Cru%2C%20relief%205%20m%20%26%20climats%20communaux%20%C2%B7%20Carte.html',
   ('Taille courte (cordon de Royat, cordon bilatéral, gobelet, éventail) ou Guyot simple', 'Short pruning (Royat cordon, bilateral cordon, gobelet, fan) or single Guyot'), ('8 yeux / pied', '8 buds / vine')),
  ('Chablis', '../../Bourgogne%20Regions/Chablis_et_de_l_Auxerrois.html',
   ('Cordon de Royat, Guyot simple ou double, taille Chablis', 'Royat cordon, single or double Guyot, Chablis pruning'), ('14 yeux / pied et 10 / m²', '14 buds / vine and 10 / m²')),
  ('Champagne', '../../Champagne.html',
   ('Chablis, cordon de Royat, Vallée de la Marne, Guyot simple ou double', 'Chablis, Royat cordon, Vallée de la Marne, single or double Guyot'), ('18 yeux / m²', '18 buds / m²')),
  ('Pauillac', PLAN + 'Bordeaux_LeftBank/Pauillac.html',
   ('Médocaine à astes, cots et astes, cordon à deux bras, éventail à quatre bras', 'Médoc pruning with astes, cots and astes, two-armed cordon, four-armed fan'), ('12 yeux / pied', '12 buds / vine')),
  ('Sancerre', PLAN + 'Loire_Centre/Sancerre.html',
   ('Guyot simple (10), Guyot double (12), cordon de Royat (14)', 'Single Guyot (10), double Guyot (12), Royat cordon (14)'), ('10 à 14 yeux / pied', '10–14 buds / vine')),
  ('Morgon', '../../Bourgogne%20Regions/Beaujolais.html',
   ('Taille courte : gobelet, éventail, cordon de Royat ; 3 à 5 coursons à 2 yeux ; taille achevée le 15 mai', 'Short pruning: gobelet, fan, Royat cordon; 3–5 two-bud spurs; pruning finished by 15 May'), ('10 yeux / pied', '10 buds / vine')),
  ('Côte-Rôtie', PLAN + 'Cotes_du_Rhone/Cote-Rotie.html',
   ('Gobelet (5 coursons au plus), cordon de Royat, Guyot simple ; sur échalas ou palissage', 'Gobelet (5 spurs at most), Royat cordon, single Guyot; on stakes or trellis'), ('10 yeux / pied', '10 buds / vine')),
  ('Condrieu', PLAN + 'Cotes_du_Rhone/Condrieu.html',
   ('Taille courte à coursons de 3 yeux au plus (gobelet, cordon de Royat) ou Guyot simple (8 yeux au plus sur le long bois)', 'Spur pruning with spurs of at most 3 buds (gobelet, Royat cordon) or single Guyot (at most 8 buds on the cane)'), ('10 yeux / pied', '10 buds / vine')),
  ('Châteauneuf-du-Pape', PLAN + 'Cotes_du_Rhone_Sud/Chateauneuf-du-Pape.html',
   ('Gobelet obligatoire pour Grenache et Mourvèdre ; cordon de Royat ou Guyot simple possibles pour d’autres cépages', 'Gobelet compulsory for Grenache and Mourvèdre; Royat cordon or single Guyot possible for other varieties'), ('12 yeux / pied (15 après 40 ans)', '12 buds / vine (15 after 40 years)')),
  ('Alsace', '../../Alsace.html',
   ('Guyot simple ou double', 'Single or double Guyot'), ('24 yeux / pied (20 pour VT et SGN)', '24 buds / vine (20 for VT and SGN)')),
]


def rules_rows():
    return ''.join(f'<tr><td><a href="{h}">{n}</a></td><td>{t(sy)}</td><td class="mx">{t(mx)}</td></tr>' for n, h, sy, mx in RULES)


WORDS = [
  (('Œil franc', 'Count bud'), ('Bourgeon bien formé sur le sarment, hors de la couronne de base : c’est lui qu’on compte.', 'A well-formed bud on the cane, away from the basal crown: the one that is counted.')),
  (('Courson (cot)', 'Spur'), ('Sarment taillé court, à 1–3 yeux.', 'A cane cut short, to 1–3 buds.')),
  (('Baguette (long bois, aste)', 'Cane'), ('Sarment gardé long, couché sur le fil.', 'A cane kept long and laid along the wire.')),
  (('Charpente, bras', 'Arm'), ('Bois permanent qui porte coursons ou baguettes.', 'Permanent wood carrying spurs or canes.')),
  (('Rachet, rappel', 'Renewal spur'), ('Courson laissé bas pour rajeunir le cep.', 'A low spur kept to rejuvenate the vine.')),
  (('Chicot', 'Stub'), ('Bout de bois laissé au-dessus de la coupe pour protéger le bois vivant.', 'A piece of wood left above the cut to protect living wood.')),
  (('Prétaille', 'Pre-pruning'), ('Passage d’une machine qui raccourcit les sarments avant la taille fine.', 'A machine pass that shortens canes before fine pruning.')),
  (('Tirage des bois', 'Brush pulling'), ('Arracher du fil les sarments coupés.', 'Pulling the cut canes out of the wires.')),
]


def words():
    return ''.join(f'<div class="word"><b>{t(a)}</b>{t(b, "span")}</div>' for a, b in WORDS)


PRO_WHY = [
  (('Équilibre', 'Balance'),
   ('La taille règle le rapport entre la vigueur (le bois et les feuilles) et la charge (les grappes). Trop d’yeux : une récolte abondante qui mûrit mal et épuise le cep. Trop peu : une vigne trop vigoureuse, des rameaux exubérants et des raisins à l’ombre.',
    'Pruning sets the ratio between vigour (wood and leaves) and crop (bunches). Too many buds: a large crop that ripens poorly and exhausts the vine. Too few: an over-vigorous vine, rampant shoots and shaded grapes.')),
  (('Taille courte ou longue ?', 'Short or long pruning?'),
   ('Les cépages dont les yeux de la base sont peu fertiles (Sauvignon, Cabernet Sauvignon dans certains terroirs) se taillent plutôt long ; ceux dont la base est fertile (Grenache, Gamay, Syrah) acceptent la taille courte, plus simple et plus pérenne.',
    'Varieties with poorly fruitful basal buds (Sauvignon, Cabernet Sauvignon in some sites) tend to be cane-pruned; those with fruitful basal buds (Grenache, Gamay, Syrah) accept spur pruning, which is simpler and longer-lasting.')),
  (('Date de la taille', 'Pruning date'),
   ('De la chute des feuilles à la fin de l’hiver. Une taille tardive retarde un peu le débourrement, ce qui peut aider à éviter les gelées de printemps. Les cahiers des charges fixent souvent une date ou un stade limite (Pauillac : stade « feuilles étalées » ; Champagne : 4 feuilles étalées ; Morgon : 15 mai).',
    'From leaf fall to the end of winter. Late pruning delays budburst slightly, which can help avoid spring frost. Specifications often set a deadline date or stage (Pauillac: “leaves unfolded”; Champagne: 4 leaves unfolded; Morgon: 15 May).')),
  (('Yeux supplémentaires', 'Extra buds'),
   ('Plusieurs AOC (Chambertin, Chablis) autorisent à laisser plus d’yeux à la taille, par sécurité contre le gel, à condition qu’au stade 11–12 feuilles le nombre de rameaux fructifères ne dépasse pas la limite.',
    'Several AOCs (Chambertin, Chablis) allow extra buds at pruning as frost insurance, provided that at the 11–12 leaf stage the number of fruiting shoots does not exceed the limit.')),
]

PRO_SAP = [
  (('La méthode', 'The method'),
   ('Popularisée en France par François Dal (Sicavac, Sancerre) et, en Italie, par Marco Simonit et Pierpaolo Sirch, d’après les travaux de Lafon (années 1920). Principes : garder une continuité du bois vivant entre les racines et les rameaux, regrouper les plaies sur une même face, éviter les grosses coupes sur le vieux bois, laisser des chicots.',
    'Popularised in France by François Dal (Sicavac, Sancerre) and in Italy by Marco Simonit and Pierpaolo Sirch, building on Lafon’s work (1920s). Principles: keep living wood continuous between roots and shoots, group wounds on the same side, avoid large cuts in old wood, leave stubs.')),
  (('Pourquoi', 'Why'),
   ('Chaque coupe provoque un « cône de dessèchement » de bois mort sous la plaie. Placées n’importe où, ces zones mortes finissent par isoler des parties du cep et favorisent l’installation des champignons de l’esca (chapitre 7).',
    'Every cut causes a “desiccation cone” of dead wood beneath the wound. Placed randomly, these dead zones end up isolating parts of the vine and help the esca fungi take hold (chapter 7).')),
]

SOURCES = [
  ('INAO, cahiers des charges des AOC Chambertin, Chablis, Champagne, Pauillac, Sancerre, Morgon, Côte-Rôtie, Condrieu, Châteauneuf-du-Pape, Alsace.', 'INAO, specifications of the Chambertin, Chablis, Champagne, Pauillac, Sancerre, Morgon, Côte-Rôtie, Condrieu, Châteauneuf-du-Pape and Alsace AOCs.'),
  ('Guyot J., <i>Culture de la vigne et vinification</i>, 1860.', 'Guyot J., <i>Culture de la vigne et vinification</i>, 1860.'),
  ('Simonit M., <i>Guide de la taille Guyot</i> ; Lafon R., <i>Modifications à apporter à la taille de la vigne…</i>, 1921.', 'Simonit M., <i>Guyot pruning manual</i>; Lafon R., <i>Modifications à apporter à la taille de la vigne…</i>, 1921.'),
  ('IFV et Plan national dépérissement du vignoble : fiches taille et maladies du bois.', 'IFV and the national vineyard-decline plan: pruning and trunk-disease sheets.'),
]


def main():
    tpl = (HERE / 'pruning_template.html').read_text()
    rep = {
        '@@BASE_CSS@@': base_css(),
        '@@PRO_ICON@@': PRO_ICON,
        '@@BEFORE_AFTER@@': before_after(),
        '@@PLATE_TRAINING@@': plate('img/botany/training_systems.webp', 'Modes de conduite de la vigne / Vine training systems', 1122, 1402, 'wide'),
        '@@SYSTEMS@@': system_cards(),
        '@@SAPFLOW@@': sapflow(),
        '@@RULES@@': rules_rows(),
        '@@WORDS@@': words(),
        '@@PRO_WHY@@': pro_panel(PRO_WHY),
        '@@PRO_SAP@@': pro_panel(PRO_SAP),
        '@@CHAPTERS@@': chapter_nav(5),
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
