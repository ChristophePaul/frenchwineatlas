"""Stage 08 drawing: how the heads are held and how the barrel is made watertight (2026-10-18, user request).
Three panels on a paper card: (A) section through the end of the barrel — head in the croze, hoops squeezing;
(B) the head seen from above — boards, dowels / tongue-and-groove; (C) two staves in section under a hoop.
Numbered markers ① … ⑤ match the explanations printed under the drawing (gen_page.SEAL_NOTES).
"""

INK = '#3a2414'
OAK, OAK2, OAK3 = '#d8b07a', '#c99c62', '#e6c896'
HOOP = '#3b3430'
RED = '#9b2235'
WINE = '#7a1f2e'
PAPER = '#fbf5e8'


def att(s):
    return s.replace('&', '&amp;').replace('"', '&quot;')


def T(x, y, fr, en, cls='t', anchor='middle'):
    return (f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}" data-fr="{att(fr)}" '
            f'data-en="{att(en)}">{fr}</text>')


def num(x, y, n):
    return (f'<circle cx="{x}" cy="{y}" r="11" fill="{RED}"/>'
            f'<text x="{x}" y="{y + 4.2}" text-anchor="middle" class="n">{n}</text>')


def arrow(x1, y1, x2, y2, col=RED, w=2.4):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 10 * math.cos(a), y2 - 10 * math.sin(a)
    px, py = 5 * math.sin(a), -5 * math.cos(a)
    return (f'<line x1="{x1}" y1="{y1}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="{col}" stroke-width="{w}"/>'
            f'<path d="M{x2},{y2} L{hx + px:.1f},{hy + py:.1f} L{hx - px:.1f},{hy - py:.1f} Z" fill="{col}"/>')


def panel_a():
    """section through the end of the barrel, standing upright; outside left and right"""
    o = []
    L0, L1, R0, R1 = 80, 112, 368, 400          # stave faces (outer, inner)
    top, bot = 92, 452
    hy0, hy1 = 150, 176                         # head thickness
    # wine
    o.append(f'<rect x="{L1}" y="{hy1}" width="{R0 - L1}" height="{bot - hy1}" fill="{WINE}" opacity=".16"/>')
    o.append(T((L1 + R0) / 2, 330, 'le vin', 'the wine', 'tw'))
    for (x0, x1, inner, side) in [(L0, L1, L1, 1), (R1, R0, R0, -1)]:   # (outer face, inner face, inner, direction)
        g = 13 * side                           # croze depth, cut into the inner face
        c = 20 * side                           # chamfer width at the top of the inner face
        pts = (f'M{x0},{top} L{inner - c},{top} L{inner},{top + 32} L{inner},{hy0 - 2} '
               f'L{inner - g},{hy0 + 6} L{inner - g},{hy1 - 6} L{inner},{hy1 + 2} L{inner},{bot} L{x0},{bot} Z')
        o.append(f'<path d="{pts}" fill="url(#sgOak)" stroke="{INK}" stroke-width="1.6"/>')
        # grain lines along the stave
        for k in (1, 2):
            xx = x0 + (x1 - x0) * k / 3
            o.append(f'<line x1="{xx}" y1="{top + 40}" x2="{xx}" y2="{bot - 4}" stroke="{OAK2}" stroke-width="1"/>')
    # head with bevelled edges reaching into both crozes
    o.append(f'<path d="M{L1},{hy0 - 2} L{R0},{hy0 - 2} L{R0 + 12},{hy0 + 7} L{R0 + 12},{hy1 - 7} L{R0},{hy1 + 2} '
             f'L{L1},{hy1 + 2} L{L1 - 12},{hy1 - 7} L{L1 - 12},{hy0 + 7} Z" fill="{OAK3}" stroke="{INK}" stroke-width="1.6"/>')
    for xx in (180, 256, 316):                  # board joints seen in section
        o.append(f'<line x1="{xx}" y1="{hy0 - 2}" x2="{xx}" y2="{hy1 + 2}" stroke="{INK}" stroke-width=".9" stroke-dasharray="3 2"/>')
    # hoops on the outer faces + squeeze arrows
    for (y0, y1) in [(112, 136), (214, 238)]:
        o.append(f'<rect x="{L0 - 9}" y="{y0}" width="9" height="{y1 - y0}" fill="{HOOP}"/>')
        o.append(f'<rect x="{R1}" y="{y0}" width="9" height="{y1 - y0}" fill="{HOOP}"/>')
        ym = (y0 + y1) / 2
        o.append(arrow(L0 - 56, ym, L0 - 14, ym))
        o.append(arrow(R1 + 56, ym, R1 + 14, ym))
    # torn bottom edge
    o.append(f'<path d="M{L0 - 6},{bot} l12,-6 l12,8 l12,-6 l12,6" fill="none" stroke="{PAPER}" stroke-width="5"/>')
    o.append(f'<path d="M{R0 - 6},{bot} l12,-6 l12,8 l12,-6 l12,6" fill="none" stroke="{PAPER}" stroke-width="5"/>')
    # labels
    o.append(T(240, 54, 'Coupe au bout du fût', 'Section at the end of the cask', 'h'))
    o.append(T(240, 74, 'debout, l’extérieur à gauche et à droite', 'standing upright, outside left and right', 'st'))
    o.append(T(L0 - 34, 108, 'cercle', 'hoop', 'tl'))
    o.append(T((L1 + R0) / 2, hy0 - 12, 'le fond', 'the head', 'tl'))
    o.append(T(L0 + 16, bot + 22, 'douelle', 'stave', 'tl'))
    o.append(T(R0 + 16, bot + 22, 'douelle', 'stave', 'tl'))
    o.append(num(L1 + 22, hy1 + 22, 1))
    o.append(f'<line x1="{L1 + 13}" y1="{hy1 + 15}" x2="{L1 - 4}" y2="{hy1 - 4}" stroke="{RED}" stroke-width="1.4"/>')
    o.append(num(L0 - 64, 176, 2))
    o.append(num(300, hy0 - 22, 4))
    return '<g>' + ''.join(o) + '</g>'


def panel_b():
    """the head seen from above: boards, dowels across the joints, bevelled rim"""
    cx, cy, r = 600, 262, 118
    o = [T(cx, 54, 'Le fond vu de dessus', 'The head seen from above', 'h'),
         T(cx, 74, 'des planches assemblées', 'boards joined together', 'st'),
         f'<clipPath id="sgDisc"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>',
         '<g clip-path="url(#sgDisc)">']
    xs = [cx - r, cx - 76, cx - 30, cx + 18, cx + 64, cx + r]
    for i in range(len(xs) - 1):
        o.append(f'<rect x="{xs[i]}" y="{cy - r}" width="{xs[i + 1] - xs[i]}" height="{2 * r}" fill="{OAK3 if i % 2 else OAK}"/>')
        for k in range(3):
            gx = xs[i] + (xs[i + 1] - xs[i]) * (k + 1) / 4
            o.append(f'<line x1="{gx}" y1="{cy - r}" x2="{gx + 3}" y2="{cy + r}" stroke="{OAK2}" stroke-width=".8"/>')
    for x in xs[1:-1]:
        o.append(f'<line x1="{x}" y1="{cy - r}" x2="{x}" y2="{cy + r}" stroke="{INK}" stroke-width="1.3"/>')
        for dy in (-62, 0, 62):                 # dowels across each joint (hidden in the wood, shown dashed)
            o.append(f'<rect x="{x - 13}" y="{cy + dy - 3}" width="26" height="6" rx="3" fill="none" stroke="{RED}" stroke-width="1.3" stroke-dasharray="3 2"/>')
    o.append('</g>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r - 12}" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="5 4"/>')
    o.append(T(cx, cy + r + 22, 'biseau du bord (entre dans le jable)', 'bevelled rim (fits into the croze)', 'tl'))
    o.append(num(xs[2] + 22, cy - 92, 4))
    # tongue-and-groove inset
    ix, iy = cx - 70, cy + r + 44
    o.append(f'<rect x="{ix}" y="{iy}" width="66" height="22" fill="{OAK}" stroke="{INK}" stroke-width="1.2"/>')
    o.append(f'<path d="M{ix + 74},{iy} L{ix + 140},{iy} L{ix + 140},{iy + 22} L{ix + 74},{iy + 22} L{ix + 74},{iy + 15} '
             f'L{ix + 66},{iy + 15} L{ix + 66},{iy + 7} L{ix + 74},{iy + 7} Z" fill="{OAK3}" stroke="{INK}" stroke-width="1.2"/>')
    o.append(f'<path d="M{ix + 66},{iy + 7} L{ix + 58},{iy + 7} L{ix + 58},{iy + 15} L{ix + 66},{iy + 15}" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="2 2"/>')
    o.append(arrow(ix + 104, iy + 11, ix + 80, iy + 11, INK, 1.4))
    o.append(T(cx, iy + 42, 'rainure et languette', 'tongue and groove', 'st'))
    return '<g>' + ''.join(o) + '</g>'


def panel_c():
    """two staves in section (seen from the end) under a hoop: the bevelled edges meet"""
    import math
    cx, cy = 870, 560                           # centre of the barrel's circle, far below
    R1, R0 = 400, 362                           # outer / inner radius of the staves
    o = [T(870, 54, 'Deux douelles en coupe', 'Two staves in section', 'h'),
         T(870, 74, 'vues par le bout, sous un cercle', 'seen end-on, under a hoop', 'st')]

    def P(r, deg):
        a = math.radians(deg)
        return cx + r * math.sin(a), cy - r * math.cos(a)
    edges = [-15, -5, 5, 15]
    for i in range(3):
        a0, a1 = edges[i], edges[i + 1]
        p = [P(R1, a0), P(R1, a1), P(R0, a1), P(R0, a0)]
        o.append('<path d="M{:.1f},{:.1f} A{R1},{R1} 0 0 1 {:.1f},{:.1f} L{:.1f},{:.1f} A{R0},{R0} 0 0 0 {:.1f},{:.1f} Z" '
                 .format(*p[0], *p[1], *p[2], *p[3], R1=R1, R0=R0)
                 + f'fill="{OAK3 if i == 1 else OAK}" stroke="{INK}" stroke-width="1.4"/>')
    # hoop around the outside
    hp0, hp1 = P(R1 + 9, -16.5), P(R1 + 9, 16.5)
    o.append(f'<path d="M{hp0[0]:.1f},{hp0[1]:.1f} A{R1 + 9},{R1 + 9} 0 0 1 {hp1[0]:.1f},{hp1[1]:.1f}" fill="none" stroke="{HOOP}" stroke-width="9"/>')
    for d in (-10, 0, 10):
        q0, q1 = P(R1 + 44, d), P(R1 + 16, d)
        o.append(arrow(q0[0], q0[1], q1[0], q1[1]))
    # the joints: bevelled edges pressed together
    for e in (-5, 5):
        q = P(R0 - 18, e)
        o.append(f'<line x1="{q[0]:.1f}" y1="{q[1]:.1f}" x2="{P(R0 + 4, e)[0]:.1f}" y2="{P(R0 + 4, e)[1]:.1f}" stroke="{RED}" stroke-width="1.4"/>')
    o.append(num(*P(R0 - 30, 5), 3))
    o.append(T(870, 262, 'chants en biais', 'bevelled edges', 'tl'))
    o.append(T(870, 280, 'plaqués l’un contre l’autre', 'pressed against each other', 'tl'))
    o.append(T(870, 320, 'intérieur', 'inside', 'st'))
    o.append(num(*P(R1 + 50, -14), 2))
    return '<g>' + ''.join(o) + '</g>'


DEFS = (f'<defs><linearGradient id="sgOak" x1="0" x2="1"><stop offset="0" stop-color="{OAK2}"/>'
        f'<stop offset=".5" stop-color="{OAK3}"/><stop offset="1" stop-color="{OAK}"/></linearGradient></defs>')
STYLE = ('<style>.seal-svg .h{font:600 17px var(--serif,Georgia),serif;fill:#2e1419}'
         '.seal-svg .st{font:italic 12.5px var(--sans,sans-serif);fill:#6b4a2a}'
         '.seal-svg .tl{font:600 12.5px var(--sans,sans-serif);fill:#3a2414}'
         '.seal-svg .tw{font:italic 600 14px var(--sans,sans-serif);fill:#7a1f2e;opacity:.8}'
         '.seal-svg .n{font:700 12px var(--sans,sans-serif);fill:#fff}</style>')


def seal_svg():
    """panels A and C (the head seen from above now sits beside the stage-08 photos: head_svg())"""
    return ('<svg class="seal-svg" viewBox="0 0 760 520" role="img" '
            'aria-label="Comment le fond est tenu et comment la barrique devient étanche / How the head is held and how the barrel is made watertight">'
            + DEFS + STYLE + panel_a() + '<g transform="translate(-260,0)">' + panel_c() + '</g></svg>')


def head_svg():
    """panel B alone, as a tile in the stage-08 photo grid (user request, 2026-10-18)"""
    return ('<svg class="seal-svg head-svg" viewBox="435 32 330 448" role="img" '
            'aria-label="Le fond vu de dessus / The head seen from above">'
            + STYLE + panel_b() + '</svg>')
