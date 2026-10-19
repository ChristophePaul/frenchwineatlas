#!/usr/bin/env python3
"""Build Infos/Vine_and_Vineyard/Vine_Canopy.html (chapter 6 — canopy & soil work).
Run:  python3 "WEB Site/Infos/Vine_and_Vineyard/_source/build_canopy.py"
Rules quoted from the INAO cahiers des charges in « Cahiers des Charges/ ».
"""
import random
from common import HERE, att, t, blk, base_css, pro_panel, chapter_nav, PRO_ICON

OUT = HERE.parent / 'Vine_Canopy.html'
INK = '#3b2a1e'
SERIF = 'Iowan Old Style,Palatino,Georgia,serif'
OLD = '#5f4b37'; SHOOT = '#6f8f34'; LEAF = '#7aa23c'; LEAF_D = '#4f7a2a'; GRAPE = '#4f1c47'; WIRE = '#8a8a8a'
CUT = '#a0283c'


def lbl(x, y, pair, anchor='middle', size=14, fill=INK, weight='400', extra=''):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'font-family="{SERIF}" paint-order="stroke" stroke="#fbf6ea" stroke-width="3" {extra}'
            f'data-fr="{att(pair[0])}" data-en="{att(pair[1])}">{pair[0]}</text>')


# ------------------------------------------------------------ canopy cross-section (end view)
def canopy_section():
    s = ['<svg class="diagram" viewBox="0 0 680 360" role="img" aria-label="Coupe transversale de rangs palissés / Cross-section of trellised rows">']
    s.append('<defs><marker id="ar" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M1 1L9 5L1 9" fill="none" stroke="#3b2a1e" stroke-width="1.6"/></marker></defs>')
    s.append('<rect x="0" y="0" width="680" height="300" fill="#e6f0f4"/><rect x="0" y="300" width="680" height="60" fill="#cdb48a"/>')
    s.append('<circle cx="620" cy="46" r="20" fill="#f2c14e"/>')
    rows = [150, 340, 530]
    rnd = random.Random(2)
    for i, x in enumerate(rows):
        s.append(f'<rect x="{x - 3}" y="80" width="6" height="222" fill="#9b7b52"/>')
        s.append(f'<path d="M{x} 300 L{x} 240" stroke="{OLD}" stroke-width="9" stroke-linecap="round"/>')
        # leaf wall
        s.append(f'<path d="M{x - 30} 236 C{x - 38} 190 {x - 34} 130 {x - 26} 96 L{x + 26} 96 C{x + 34} 130 {x + 38} 190 {x + 30} 236 Z" fill="{LEAF}" opacity=".92"/>')
        for _ in range(26):
            lx = x + rnd.uniform(-28, 28); ly = rnd.uniform(102, 230)
            s.append(f'<ellipse cx="{lx:.1f}" cy="{ly:.1f}" rx="9" ry="6" fill="{rnd.choice([LEAF, LEAF_D, "#8fb84a"])}" opacity=".9"/>')
        # bunch zone (leaves removed on the east side, right)
        s.append(f'<rect x="{x + 4}" y="236" width="34" height="34" fill="#e6f0f4"/>')
        s.append(f'<ellipse cx="{x - 14}" cy="252" rx="8" ry="13" fill="{GRAPE}"/><ellipse cx="{x + 14}" cy="254" rx="8" ry="13" fill="{GRAPE}"/>')
        for y in (236, 180, 130, 96):
            s.append(f'<line x1="{x - 34}" y1="{y}" x2="{x + 34}" y2="{y}" stroke="{WIRE}" stroke-width="1.2" opacity=".7"/>')
        # trimming line
        s.append(f'<line x1="{x - 40}" y1="92" x2="{x + 40}" y2="92" stroke="{CUT}" stroke-width="2" stroke-dasharray="6 4"/>')
        s.append(f'<path d="M{x + 36} 236 L{x + 36} 270" stroke="#d29a1e" stroke-width="0" />')
    # sun rays reaching walls and the ground
    for x0, y0, x1, y1 in ((600, 62, 378, 150), (604, 70, 562, 210), (606, 74, 470, 300)):
        s.append(f'<path d="M{x0} {y0} L{x1} {y1}" stroke="#d29a1e" stroke-width="1.8" stroke-dasharray="6 5"/>')
    # dimensions
    s.append(f'<path d="M{rows[0] + 52} 236 L{rows[0] + 52} 96" stroke="{INK}" stroke-width="1.4" marker-start="url(#ar)" marker-end="url(#ar)"/>')
    s.append(lbl(rows[0] + 60, 160, ('H', 'H'), anchor='start', size=18, weight='700'))
    s.append(lbl(rows[0] + 60, 178, ('hauteur de', 'trellised'), anchor='start', size=12.5))
    s.append(lbl(rows[0] + 60, 193, ('feuillage palissé', 'canopy height'), anchor='start', size=12.5))
    s.append(f'<path d="M{rows[1]} 326 L{rows[2]} 326" stroke="{INK}" stroke-width="1.4" marker-start="url(#ar)" marker-end="url(#ar)"/>')
    s.append(lbl((rows[1] + rows[2]) / 2, 320, ('E : écartement entre les rangs', 'E: row spacing'), size=13.5, weight='600'))
    s.append(f'<path d="M{rows[0] - 46} 300 L{rows[0] - 46} 236" stroke="{INK}" stroke-width="1.2" marker-start="url(#ar)" marker-end="url(#ar)"/>')
    s.append(lbl(rows[0] - 52, 262, ('≥ 30 cm', '≥ 30 cm'), anchor='end', size=12.5))
    s.append(lbl(rows[0] - 52, 278, ('du sol', 'off the ground'), anchor='end', size=12.5))
    s.append(lbl(rows[1], 76, ('rognage', 'trimming'), size=12.5, fill=CUT, weight='600'))
    s.append(lbl(rows[2] + 44, 262, ('grappes dégagées', 'bunches exposed'), anchor='start', size=12.5))
    s.append(lbl(rows[2] + 44, 278, ('côté soleil levant', 'on the morning-sun side'), anchor='start', size=12.5))
    s.append(lbl(340, 30, ('Règle courante des cahiers des charges : H ≥ 0,6 × E', 'Common specification rule: H ≥ 0.6 × E'), size=15, weight='600'))
    s.append('</svg>')
    return ''.join(s)


# ------------------------------------------------------------ mini operation diagrams (viewBox 160 × 100)
def mini(kind):
    s = ['<svg class="mini" viewBox="0 0 160 100" aria-hidden="true">']
    s.append('<line x1="6" y1="64" x2="154" y2="64" stroke="#8a8a8a" stroke-width="1.2"/>')
    trunk = f'<path d="M80 100 L80 66" stroke="{OLD}" stroke-width="7" stroke-linecap="round"/><path d="M80 66 L150 66" stroke="#7d5a2c" stroke-width="3.5"/>'

    def shoot(x, top=10, col=SHOOT, dash=''):
        d = f' stroke-dasharray="{dash}"' if dash else ''
        out = f'<path d="M{x} 66 C{x - 2} 46 {x + 2} 28 {x} {top}" stroke="{col}" stroke-width="2.4" fill="none"{d}/>'
        for ly in range(top + 8, 62, 14):
            out += f'<ellipse cx="{x + (6 if ly % 28 else -6)}" cy="{ly}" rx="7" ry="5" fill="{LEAF}" opacity="{.35 if dash else .95}"/>'
        return out

    def cross(x, y):
        return f'<path d="M{x - 6} {y - 6} L{x + 6} {y + 6} M{x + 6} {y - 6} L{x - 6} {y + 6}" stroke="{CUT}" stroke-width="2.6" stroke-linecap="round"/>'
    s.append(trunk)
    if kind == 'debud':
        for x in (92, 112, 132, 148):
            s.append(shoot(x))
        s.append(shoot(102, 30, dash='3 3') + cross(102, 48) + shoot(122, 34, dash='3 3') + cross(122, 50))
    elif kind == 'sucker':
        for x in (100, 125, 148):
            s.append(shoot(x))
        s.append(f'<path d="M80 92 C70 86 64 80 60 70" stroke="{SHOOT}" stroke-width="2.2" fill="none" stroke-dasharray="3 3"/>' + cross(64, 76))
        s.append(f'<path d="M80 84 C90 80 94 76 96 72" stroke="{SHOOT}" stroke-width="2.2" fill="none" stroke-dasharray="3 3"/>')
    elif kind == 'lift':
        s.append('<line x1="6" y1="40" x2="154" y2="40" stroke="#8a8a8a" stroke-width="1.2"/><line x1="6" y1="16" x2="154" y2="16" stroke="#8a8a8a" stroke-width="1.2"/>')
        for x in (96, 114, 132, 150):
            s.append(shoot(x, 6))
        s.append(f'<path d="M30 60 C26 46 30 30 44 22" stroke="{SHOOT}" stroke-width="2.4" fill="none" stroke-dasharray="3 3"/><path d="M44 30 l10 -6" stroke="{CUT}" stroke-width="0"/>')
        s.append('<path d="M40 44 C50 34 62 30 76 30" stroke="#d29a1e" stroke-width="2" fill="none" marker-end="url(#mk)"/>')
    elif kind == 'trim':
        for x in (92, 110, 128, 146):
            s.append(shoot(x, 4))
        s.append(f'<line x1="84" y1="20" x2="156" y2="20" stroke="{CUT}" stroke-width="2" stroke-dasharray="5 3"/>')
        s.append('<rect x="84" y="2" width="72" height="17" fill="#fbf6ea" opacity=".72"/>')
    elif kind == 'leaf':
        for x in (92, 110, 128, 146):
            s.append(shoot(x, 10))
        s.append('<rect x="86" y="44" width="70" height="20" fill="#fbf6ea"/>')
        for x in (98, 122, 140):
            s.append(f'<ellipse cx="{x}" cy="76" rx="6" ry="10" fill="{GRAPE}"/>')
        s.append(f'<path d="M86 44 L156 44 M86 64 L156 64" stroke="{CUT}" stroke-width="1.2" stroke-dasharray="4 3"/>')
    elif kind == 'green':
        for x in (92, 110, 128, 146):
            s.append(shoot(x, 10))
        for x in (98, 140):
            s.append(f'<ellipse cx="{x}" cy="76" rx="6" ry="10" fill="{GRAPE}"/>')
        s.append(f'<ellipse cx="122" cy="76" rx="6" ry="10" fill="#7aa23c" opacity=".5"/>' + cross(122, 76))
        s.append('<ellipse cx="40" cy="94" rx="7" ry="4" fill="#7aa23c"/><ellipse cx="54" cy="96" rx="7" ry="4" fill="#7aa23c"/>')
    s.insert(1, '<defs><marker id="mk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="#d29a1e" stroke-width="1.8"/></marker></defs>')
    s.append('</svg>')
    return ''.join(s)


OPS = [  # kind, name, when, what, why
  ('debud', ('Ébourgeonnage', 'Shoot thinning'), ('avril – mai', 'April – May'),
   ('Supprimer à la main les pousses en surnombre : doubles, mal placées, sans grappe.', 'Removing surplus shoots by hand: doubles, badly placed, fruitless.'),
   ('Régler la charge, aérer la future végétation.', 'Set the crop, open up the future canopy.')),
  ('sucker', ('Épamprage', 'Desuckering'), ('mai', 'May'),
   ('Retirer les « pampres », pousses nées sur le tronc ou au pied du cep.', 'Removing suckers growing on the trunk or at the foot of the vine.'),
   ('Elles consomment de la sève sans rien produire.', 'They use sap and produce nothing.')),
  ('lift', ('Relevage & palissage', 'Shoot positioning'), ('mai – juin', 'May – June'),
   ('Remonter les fils releveurs pour pincer les rameaux et les tenir verticaux.', 'Raising the catch wires to hold the shoots upright.'),
   ('Un mur de feuilles régulier, bien exposé, facile à traiter.', 'An even, well-exposed wall of leaves, easy to spray.')),
  ('trim', ('Rognage', 'Trimming'), ('juin – août', 'June – August'),
   ('Couper l’extrémité des rameaux au-dessus du dernier fil et sur les côtés, souvent en deux ou trois passages à la machine.', 'Cutting shoot tips above the top wire and on the sides, often in two or three machine passes.'),
   ('Limiter la vigueur, faciliter le passage, concentrer la sève vers les grappes.', 'Curb vigour, keep rows passable, send sap to the bunches.')),
  ('leaf', ('Effeuillage', 'Leaf removal'), ('juin – juillet', 'June – July'),
   ('Enlever les feuilles de la zone des grappes, souvent d’un seul côté, à la main ou à la machine.', 'Removing leaves in the bunch zone, often on one side only, by hand or machine.'),
   ('Aérer les grappes contre la pourriture, mieux les exposer au soleil.', 'Air the bunches against rot, expose them to sunlight.')),
  ('green', ('Vendange verte', 'Green harvest'), ('juillet – août', 'July – August'),
   ('Couper une partie des grappes avant maturité, en général à la véraison.', 'Cutting off some bunches before ripeness, usually at véraison.'),
   ('Réduire le rendement, homogénéiser la maturité.', 'Reduce yield, even out ripening.')),
]


def op_cards():
    return ''.join(
        f'<article class="op"><div class="op-fig">{mini(k)}</div><div class="op-b"><span class="op-w">{t(w)}</span><h3>{t(n)}</h3>'
        f'{blk(what)}<p class="op-y"><b>{t(("Pourquoi : ", "Why: "))}</b>{t(why)}</p></div></article>'
        for k, n, w, what, why in OPS)


CAL_ROWS = [  # name, months (index 0 = Jan) values 0/1/2
  (('Ébourgeonnage', 'Shoot thinning'), '#7aa23c', [0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0]),
  (('Épamprage', 'Desuckering'), '#6f8b1e', [0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 0]),
  (('Relevage, palissage', 'Shoot positioning'), '#4f7a2a', [0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0, 0]),
  (('Rognage', 'Trimming'), '#a0283c', [0, 0, 0, 0, 0, 2, 2, 1, 0, 0, 0, 0]),
  (('Effeuillage', 'Leaf removal'), '#c08a1a', [0, 0, 0, 0, 0, 1, 2, 1, 0, 0, 0, 0]),
  (('Vendange verte', 'Green harvest'), '#7d3f78', [0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0]),
  (('Débuttage, griffages', 'Unhilling, harrowing'), '#8a5a2b', [0, 0, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0]),
  (('Tonte de l’herbe', 'Mowing'), '#5f8a34', [0, 0, 0, 1, 2, 2, 1, 1, 0, 0, 0, 0]),
  (('Semis des couverts', 'Sowing cover crops'), '#4f8a6a', [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1, 0]),
  (('Buttage, fumure', 'Hilling up, manuring'), '#6f5a48', [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 1]),
]
MONTHS = [('J', 'J'), ('F', 'F'), ('M', 'M'), ('A', 'A'), ('M', 'M'), ('J', 'J'), ('J', 'J'), ('A', 'A'), ('S', 'S'), ('O', 'O'), ('N', 'N'), ('D', 'D')]


def calendar():
    head = '<div class="cal-row cal-head"><div class="cal-lbl"></div>' + ''.join(f'<div class="cal-m">{t(m)}</div>' for m in MONTHS) + '</div>'
    row = lambda n, c, vals: (f'<div class="cal-row" style="--c:{c}"><div class="cal-lbl"><i></i>{t(n)}</div>'
                              + ''.join(f'<div class="cell v{v}"></div>' for v in vals) + '</div>')
    rows = ''.join(row(*r) for r in CAL_ROWS[:6]) + '<div class="cal-sep"></div>' + ''.join(row(*r) for r in CAL_ROWS[6:])
    return head + rows


# ------------------------------------------------------------ soil management cross-sections
def soils():
    rnd = random.Random(9)
    s = ['<svg class="diagram" viewBox="0 0 680 250" role="img" aria-label="Quatre façons d’entretenir le sol / Four ways to manage the soil">']
    W = 170
    titles = [(('Désherbé', 'Herbicide-bare'), ('sol nu', 'bare soil')), (('Travaillé', 'Cultivated'), ('labour, griffage', 'ploughing, harrowing')),
              (('Enherbé', 'Grassed'), ('couvert permanent', 'permanent cover')), (('Mixte', 'Mixed'), ('herbe, rang travaillé', 'grass, row tilled'))]
    for i, (name, sub) in enumerate(titles):
        ox = i * W
        s.append(f'<rect x="{ox + 4}" y="4" width="{W - 8}" height="242" rx="10" fill="#eef4f6" stroke="#d8cfb8"/>')
        s.append(f'<rect x="{ox + 4}" y="150" width="{W - 8}" height="96" fill="#b58e5e"/>')
        for vx in (ox + 34, ox + W - 34):
            s.append(f'<path d="M{vx} 150 L{vx} 96" stroke="{OLD}" stroke-width="7" stroke-linecap="round"/>'
                     f'<path d="M{vx - 22} 96 C{vx - 26} 70 {vx - 20} 50 {vx - 12} 34 L{vx + 12} 34 C{vx + 20} 50 {vx + 26} 70 {vx + 22} 96 Z" fill="{LEAF}" opacity=".9"/>')
            for d in (-10, 0, 10):
                s.append(f'<path d="M{vx} 150 q{d} 30 {d * 2.2} 70" stroke="#7a5a3a" stroke-width="1.4" fill="none"/>')
        mid0, mid1 = ox + 50, ox + W - 50
        if i == 0:
            s.append(f'<rect x="{mid0}" y="146" width="{mid1 - mid0}" height="6" fill="#c9a87a"/>')
            for _ in range(5):
                x = rnd.uniform(mid0, mid1)
                s.append(f'<path d="M{x:.0f} 146 l-3 -7 M{x:.0f} 146 l3 -6" stroke="#b8a070" stroke-width="1.4"/>')
        elif i == 1:
            s.append(f'<path d="M{mid0} 150 ' + ''.join(f'q6 -8 12 0 ' for _ in range(int((mid1 - mid0) / 12))) + '" fill="#a07a4a" stroke="#7a5a3a"/>')
            for vx in (ox + 34, ox + W - 34):
                s.append(f'<path d="M{vx - 20} 150 Q{vx} 128 {vx + 20} 150 Z" fill="#a07a4a" stroke="#7a5a3a"/>')
        elif i in (2, 3):
            g0, x1 = (ox + 14, ox + W - 14) if i == 2 else (mid0, mid1)
            s.append(f'<rect x="{g0}" y="142" width="{x1 - g0}" height="9" fill="#6f9a3a"/>')
            for _ in range(int((x1 - g0) / 2.5)):
                x = rnd.uniform(g0, x1)
                s.append(f'<path d="M{x:.0f} 141 l{rnd.uniform(-3, 3):.1f} -{rnd.uniform(5, 10):.1f}" stroke="#4f7a2a" stroke-width="1.6"/>')
            if i == 2:
                for _ in range(10):
                    x = rnd.uniform(mid0, x1)
                    s.append(f'<path d="M{x:.0f} 152 l0 {rnd.uniform(10, 30):.0f}" stroke="#5f7a2a" stroke-width="1" opacity=".7"/>')
            else:
                for vx in (ox + 34, ox + W - 34):
                    s.append(f'<path d="M{vx - 16} 150 q4 -7 8 0 q4 -7 8 0 q4 -7 8 0 q4 -7 8 0" fill="#a07a4a" stroke="#7a5a3a"/>')
        s.append(lbl(ox + W / 2, 212, name, size=15, weight='600', fill='#fbf6ea', extra='stroke="#5a3e22" '))
        s.append(lbl(ox + W / 2, 232, sub, size=12, fill='#fbf6ea', extra='stroke="#5a3e22" '))
    s.append('</svg>')
    return ''.join(s).replace('stroke="#fbf6ea" stroke-width="3" stroke="#5a3e22"', 'stroke="#5a3e22" stroke-width="3"')


SOIL_TABLE = [
  (('Désherbage chimique', 'Herbicides'), ('Peu coûteux, rapide, aucune concurrence pour l’eau.', 'Cheap, fast, no competition for water.'),
   ('Sol nu qui s’érode et se tasse, perte de vie du sol ; fortement restreint aujourd’hui.', 'Bare soil that erodes and compacts, loss of soil life; heavily restricted today.')),
  (('Travail du sol', 'Cultivation'), ('Supprime l’herbe sans herbicide, aère le sol, oblige les racines à descendre.', 'Removes weeds without herbicides, aerates the soil, forces roots deeper.'),
   ('Passages nombreux, coût et carburant, érosion sur les pentes, risque de tassement.', 'Many passes, cost and fuel, erosion on slopes, risk of compaction.')),
  (('Enherbement', 'Cover crops'), ('Protège de l’érosion, porte les engins par temps humide, nourrit la vie du sol, freine la vigueur.', 'Prevents erosion, carries machinery in wet weather, feeds soil life, tempers vigour.'),
   ('Concurrence pour l’eau et l’azote, à maîtriser en climat sec.', 'Competes for water and nitrogen, must be managed in dry climates.')),
]


def soil_table():
    return ''.join(f'<tr><td>{t(n)}</td><td class="pro">{t(p)}</td><td class="con">{t(c)}</td></tr>' for n, p, c in SOIL_TABLE)


PRO_CANOPY = [
  (('Surface foliaire exposée', 'Exposed leaf area'),
   ('Les travaux d’Alain Carbonneau ont popularisé la notion de surface foliaire exposée (SFE) : c’est la face éclairée du feuillage qui mûrit les raisins. Un rapport hauteur de feuillage / écartement voisin de 0,6 à 1 évite que les rangs s’ombragent. D’où la règle H ≥ 0,6 × E des cahiers des charges de Chambertin ou de Champagne.',
    'Alain Carbonneau’s work popularised the notion of exposed leaf area: it is the sunlit face of the canopy that ripens the grapes. A canopy height to row spacing ratio of about 0.6–1 keeps rows from shading each other. Hence the H ≥ 0.6 × E rule in the Chambertin or Champagne specifications.')),
  (('Effeuillage : côté et moment', 'Leaf removal: side and timing'),
   ('On effeuille plutôt côté soleil levant, et tôt (de la nouaison à la fermeture de la grappe) pour que la pellicule s’endurcisse. Un effeuillage brutal en pleine chaleur provoque l’échaudage des baies ; dans le Midi, on le limite ou on l’évite.',
    'Leaves are usually removed on the morning-sun side, and early (from fruit set to bunch closure) so the skins can harden. Sudden leaf removal in a heatwave causes sunburn; in the South it is limited or avoided.')),
  (('Vendange verte : un débat', 'Green harvest: a debate'),
   ('Couper des grappes tard réduit le rendement, mais la vigne compense en partie en grossissant les baies restantes. Beaucoup préfèrent régler la charge plus tôt, par la taille et l’ébourgeonnage.',
    'Cutting bunches late lowers yield, but the vine partly compensates by enlarging the remaining berries. Many growers prefer to set the crop earlier, through pruning and shoot thinning.')),
  (('Hauteur de rognage', 'Trimming height'),
   ('Rogner trop bas réduit la surface foliaire en dessous du besoin (environ 1 m² de feuilles par kilo de raisin, chapitre 1) et retarde la maturité ; rogner trop tôt relance la pousse des entre-cœurs.',
    'Trimming too low cuts leaf area below what is needed (about 1 m² of leaves per kilo of grapes, chapter 1) and delays ripening; trimming too early triggers lateral shoot growth.')),
]

PRO_SOIL = [
  (('Règles des appellations', 'Appellation rules'),
   ('Les cahiers des charges encadrent de plus en plus l’entretien du sol : en Languedoc, un couvert végétal est obligatoire sur l’inter-rang dès qu’il dépasse 1,70 m ; en Champagne, l’enherbement permanent des tournières est obligatoire ; en Chambertin, l’herbe doit rester sous la moitié de la hauteur de palissage.',
    'Specifications increasingly regulate soil management: in Languedoc a cover crop is compulsory between rows wider than 1.70 m; in Champagne permanent grass on the headlands is compulsory; in Chambertin grass must stay below half the trellis height.')),
  (('Herbicides', 'Herbicides'),
   ('Depuis les restrictions de l’ANSES (2020-2021), le glyphosate n’est plus utilisable en vigne que sous le rang, sur une fraction de la parcelle et à dose réduite. Les vignes en bio n’utilisent aucun herbicide.',
    'Following ANSES restrictions (2020–21), glyphosate may only be used in vineyards under the row, on a fraction of the plot and at a reduced dose. Organic vineyards use no herbicides at all.')),
  (('Couverts végétaux', 'Cover crops'),
   ('Mélanges de céréales (seigle, orge, avoine) et de légumineuses (féverole, vesce, trèfle) semés à l’automne, roulés ou broyés au printemps : ils apportent de l’azote et de la matière organique, structurent le sol et nourrissent les auxiliaires.',
    'Mixes of cereals (rye, barley, oats) and legumes (faba bean, vetch, clover) sown in autumn, rolled or mulched in spring: they add nitrogen and organic matter, structure the soil and feed beneficial insects.')),
  (('Azote', 'Nitrogen'),
   ('La vigne a peu besoin d’azote : trop, elle pousse et pourrit ; trop peu, les fermentations peinent (azote assimilable des moûts) et les blancs perdent des arômes. Les apports se raisonnent après analyse de sol et observation de la vigueur.',
    'The vine needs little nitrogen: too much and it grows rampantly and rots; too little and fermentations struggle (yeast-assimilable nitrogen in the must) and whites lose aroma. Inputs are decided after soil analysis and vigour observation.')),
  (('Irrigation', 'Irrigation'),
   ('Le code rural encadre strictement l’irrigation des vignes AOC ; certains cahiers des charges l’interdisent (Chambertin, Champagne, Sancerre), d’autres l’autorisent dans les conditions fixées par la réglementation nationale (Pauillac, Languedoc, Châteauneuf-du-Pape), surtout face à la sécheresse.',
    'The French rural code strictly regulates irrigation of AOC vines; some specifications forbid it (Chambertin, Champagne, Sancerre), others allow it under the conditions set by national rules (Pauillac, Languedoc, Châteauneuf-du-Pape), mainly to cope with drought.')),
]

SOURCES = [
  ('INAO, cahiers des charges des AOC Chambertin, Champagne, Sancerre, Pauillac, Languedoc, Châteauneuf-du-Pape.', 'INAO, specifications of the Chambertin, Champagne, Sancerre, Pauillac, Languedoc and Châteauneuf-du-Pape AOCs.'),
  ('Carbonneau A. et al., <i>Traité de la vigne</i>, Dunod.', 'Carbonneau A. et al., <i>Traité de la vigne</i>, Dunod.'),
  ('IFV, fiches « entretien du sol » et « gestion du feuillage » ; ANSES, décisions sur le glyphosate, 2020.', 'IFV, “soil management” and “canopy management” sheets; ANSES, glyphosate decisions, 2020.'),
  ('Code rural et de la pêche maritime, article D. 645-5 (irrigation des vignes AOC).', 'French rural code, article D. 645-5 (irrigation of AOC vines).'),
]


def main():
    tpl = (HERE / 'canopy_template.html').read_text()
    rep = {
        '@@BASE_CSS@@': base_css(),
        '@@PRO_ICON@@': PRO_ICON,
        '@@CANOPY@@': canopy_section(),
        '@@OPS@@': op_cards(),
        '@@CALENDAR@@': calendar(),
        '@@SOILS@@': soils(),
        '@@SOIL_TABLE@@': soil_table(),
        '@@PRO_CANOPY@@': pro_panel(PRO_CANOPY),
        '@@PRO_SOIL@@': pro_panel(PRO_SOIL),
        '@@CHAPTERS@@': chapter_nav(6),
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
