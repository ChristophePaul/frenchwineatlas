#!/usr/bin/env python3
"""Build Infos/Vine_and_Vineyard/Vine_Cycle.html (chapter 2 — the vine's year).
Run:  python3 "WEB Site/Infos/Vine_and_Vineyard/_source/build_cycle.py"
Static text is in cycle_template.html; stage cards, wheel, charts, tables below.
"""
import math
from common import HERE, att, t, blk, base_css, plate, pro_panel, chapter_nav, PRO_ICON

OUT = HERE.parent / 'Vine_Cycle.html'
IMG = 'img/cycle/'
TH = 'Vine_Threats.html#'

# ---------------------------------------------------------------- stages
# (start, end) in months from 1 January (0.0 = 1 Jan, 2.5 = mid-March); end may exceed 12 (wraps)
STAGES = [
  dict(n=1, span=(10.9, 14.0), col='#6f5a48', name=('Dormance hivernale', 'Winter dormancy'),
       period=('décembre à février', 'December to February'), bbch='00', bag='A',
       what=('Les feuilles sont tombées, la sève est descendue : la vigne vit au ralenti sur les réserves d’amidon stockées dans ses racines et son bois. Le froid hivernal lève progressivement la dormance des bourgeons.',
             'The leaves have fallen and the sap has withdrawn: the vine idles on the starch reserves stored in its roots and wood. Winter cold gradually lifts the buds’ dormancy.'),
       work=('La taille, de décembre à mars : le vigneron choisit le bois qui portera la récolte. Sarments broyés ou brûlés, réparation des piquets et des fils.',
             'Pruning, from December to March: the grower chooses the wood that will carry the crop. Cuttings shredded or burned, posts and wires repaired.'),
       risks=[(('Gel d’hiver extrême', 'Extreme winter frost'), TH + 'autres'), (('Esca (plaies de taille)', 'Esca (pruning wounds)'), TH + 'esca')],
       pro=[(('Deux phases', 'Two phases'),
             ('Endodormance (le bourgeon ne peut pas débourrer, même au chaud), levée par une accumulation de froid ; puis écodormance : le bourgeon attend simplement la chaleur.',
              'Endodormancy (the bud cannot burst, even if warm), lifted by accumulated chilling; then ecodormancy: the bud simply waits for warmth.')),
            (('Résistance au froid', 'Cold hardiness'),
             ('Un œil bien aoûté de <i>vinifera</i> supporte souvent −15 à −20 °C. Le gel de février 1956 a détruit une grande partie des vignes de Saint-Émilion et de Pomerol.',
              'A well-hardened <i>vinifera</i> bud often withstands −15 to −20 °C. The February 1956 freeze destroyed much of the vineyard in Saint-Émilion and Pomerol.'))]),
  dict(n=2, span=(2.0, 3.8), col='#b07a8a', name=('Débourrement', 'Budburst'),
       period=('mars à avril', 'March to April'), bbch='01–09', bag='B–C',
       what=('Quand le sol se réchauffe, les racines se remettent à pomper : la sève coule des plaies de taille, ce sont les « pleurs ». Puis les bourgeons gonflent, s’ouvrent dans leur bourre cotonneuse et laissent apparaître une pointe verte.',
             'As the soil warms, the roots start pumping again: sap drips from the pruning cuts, the vine’s “weeping”. Then the buds swell, open in their cottony wool and show a green tip.'),
       work=('Fin de la taille, pliage et attachage des baguettes sur le fil, travail du sol (débuttage), surveillance du gel.',
             'Pruning finishes, canes are bent and tied to the wire, soil work (removing the winter earth mound), frost watch.'),
       risks=[(('Gel de printemps', 'Spring frost'), TH + 'autres')],
       pro=[(('Seuil thermique', 'Thermal threshold'),
             ('Le débourrement suit une température moyenne d’environ 10 °C, le « zéro de végétation » de la vigne. Chardonnay et Pinot débourrent tôt ; Cabernet Sauvignon, Grenache et Ugni blanc plus tard, ce qui les expose moins au gel.',
              'Budburst follows a mean temperature of about 10 °C, the vine’s “growth threshold”. Chardonnay and Pinot burst early; Cabernet Sauvignon, Grenache and Ugni Blanc later, which makes them less exposed to frost.')),
            (('Pleurs', 'Bleeding'),
             ('Les pleurs commencent quand le sol atteint environ 10 à 12 °C ; un cep peut perdre plusieurs litres de sève sans dommage.',
              'Bleeding starts when the soil reaches about 10–12 °C; a vine can lose several litres of sap without harm.'))]),
  dict(n=3, span=(3.8, 4.8), col='#7aa23c', name=('Croissance des rameaux', 'Shoot growth'),
       period=('avril à mai', 'April to May'), bbch='11–57', bag='D–H',
       what=('Les feuilles s’étalent une à une et les rameaux s’allongent vite, parfois de plusieurs centimètres par jour. Les futures grappes deviennent visibles, puis leurs boutons floraux se séparent.',
             'Leaves unfold one by one and the shoots lengthen fast, sometimes several centimetres a day. The future bunches become visible, then their flower buds separate.'),
       work=('Ébourgeonnage (supprimer les pousses inutiles), relevage des rameaux entre les fils, premiers traitements, travail du sol ou tonte de l’herbe.',
             'Shoot thinning (removing unwanted shoots), lifting shoots between the wires, first sprays, soil work or mowing.'),
       risks=[(('Mildiou', 'Downy mildew'), TH + 'mildiou'), (('Oïdium', 'Powdery mildew'), TH + 'oidium'), (('Black rot', 'Black rot'), TH + 'black-rot')],
       pro=[(('Réserves puis photosynthèse', 'Reserves, then photosynthesis'),
             ('Jusqu’au stade 6 à 8 feuilles environ, la pousse vit surtout sur les réserves ; ensuite les feuilles deviennent exportatrices de sucres.',
              'Until roughly the 6–8 leaf stage the shoot lives mainly on reserves; after that the leaves become net exporters of sugars.')),
            (('Premiers risques', 'First risks'),
             ('Les contaminations primaires de mildiou sont possibles dès que les rameaux atteignent environ 10 cm (règle des 3 × 10, voir chapitre 7).',
              'Primary downy-mildew infections are possible once shoots reach about 10 cm (the 3 × 10 rule, see chapter 7).'))]),
  dict(n=4, span=(4.8, 5.6), col='#c9b84a', name=('Floraison', 'Flowering'),
       period=('fin mai à juin', 'late May to June'), bbch='60–69', bag='I',
       what=('Les capuchons tombent et les minuscules fleurs libèrent leur pollen. Une parcelle fleurit en une à deux semaines ; le vignoble embaume d’un parfum discret, proche du réséda.',
             'The caps fall and the tiny flowers release their pollen. A plot flowers within one to two weeks; the vineyard gives off a faint scent, rather like mignonette.'),
       work=('Palissage, premiers rognages ; on évite de déranger la vigne. Les vignerons notent la date de mi-floraison : la vendange suit environ 100 jours plus tard.',
             'Trellising, first trimming; the vines are left in peace. Growers note the date of mid-flowering: harvest follows about 100 days later.'),
       risks=[(('Coulure, millerandage', 'Coulure, millerandage'), 'Vine_Plant.html#fleur'), (('Mildiou sur grappes', 'Downy mildew on bunches'), TH + 'mildiou')],
       pro=[(('Conditions', 'Conditions'),
             ('Au moins 15 °C, idéalement 20–25 °C, temps sec. Froid et pluie ralentissent la germination du pollen et provoquent la coulure.',
              'At least 15 °C, ideally 20–25 °C, dry weather. Cold and rain slow pollen germination and cause coulure.')),
            (('Repère', 'Benchmark'),
             ('BBCH 65 = pleine floraison (50 % des capuchons tombés), la date de référence des modèles de prévision de récolte.',
              'BBCH 65 = full bloom (50 % of caps fallen), the reference date for harvest-forecasting models.'))]),
  dict(n=5, span=(5.6, 6.6), col='#5f9a3a', name=('Nouaison', 'Fruit set'),
       period=('juin à juillet', 'June to July'), bbch='71–79', bag='J–L',
       what=('Les fleurs fécondées deviennent de petites baies vertes, dures et très acides. Elles grossissent jusqu’à se toucher : c’est la fermeture de la grappe.',
             'The fertilised flowers become small green berries, hard and very acidic. They swell until they touch: bunch closure.'),
       work=('Rognage (couper l’extrémité des rameaux), effeuillage de la zone des grappes, traitements, parfois vendange verte en juillet.',
             'Trimming (topping the shoots), leaf removal around the bunches, sprays, sometimes green harvesting in July.'),
       risks=[(('Oïdium', 'Powdery mildew'), TH + 'oidium'), (('Mildiou', 'Downy mildew'), TH + 'mildiou'), (('Grêle', 'Hail'), TH + 'autres')],
       pro=[(('Croissance de la baie', 'Berry growth'),
             ('Première phase : multiplication cellulaire puis grossissement ; les acides (malique surtout) s’accumulent. Un stress hydrique à ce stade réduit définitivement la taille des baies.',
              'First phase: cell division then expansion; acids (mainly malic) accumulate. Water stress at this stage permanently reduces berry size.')),
            (('Plateau', 'Lag phase'),
             ('Avant la véraison, la croissance marque une pause de 1 à 3 semaines pendant laquelle les pépins mûrissent.',
              'Before véraison, growth pauses for 1–3 weeks while the seeds mature.'))]),
  dict(n=6, span=(6.6, 7.6), col='#9b4f8a', name=('Véraison', 'Véraison'),
       period=('mi-juillet à mi-août', 'mid-July to mid-August'), bbch='81–85', bag='M',
       what=('Les baies s’assouplissent et changent de couleur : les raisins noirs rougissent puis bleuissent, les blancs deviennent translucides et dorés. Les sucres commencent à affluer, l’acidité à baisser. Les rameaux brunissent : c’est l’aoûtement.',
             'The berries soften and change colour: black grapes turn red then blue, white grapes become translucent and golden. Sugars start pouring in and acidity begins to fall. The shoots turn brown: they are ripening into wood.'),
       work=('Vendange verte pour éliminer les grappes en retard, filets contre les oiseaux, premiers prélèvements de baies.',
             'Green harvest to remove lagging bunches, nets against birds, first berry sampling.'),
       risks=[(('Pourriture grise', 'Grey rot'), TH + 'pourriture-grise'), (('Canicule, sécheresse', 'Heat, drought'), TH + 'autres')],
       pro=[(('Bascule physiologique', 'Physiological switch'),
             ('La baie passe de l’alimentation par le xylème à celle par le phloème : sucres, potassium et eau arrivent par la sève élaborée. Les anthocyanes s’accumulent dans la pellicule des cépages rouges.',
              'The berry switches from xylem to phloem supply: sugars, potassium and water arrive in the phloem sap. Anthocyanins build up in red varieties’ skins.')),
            (('Durée', 'Duration'),
             ('À l’échelle d’une grappe, quelques jours ; à l’échelle d’une parcelle, une à deux semaines. Une véraison étalée annonce une vendange hétérogène.',
              'A few days for one bunch, one to two weeks for a whole plot. A drawn-out véraison means an uneven harvest.'))]),
  dict(n=7, span=(7.6, 8.6), col='#4f2a6e', name=('Maturation', 'Ripening'),
       period=('août à septembre', 'August to September'), bbch='85–89', bag='M–N',
       what=('Pendant quarante à cinquante jours, les baies se gorgent de sucre, perdent de l’acidité, gagnent en arômes et en couleur ; les tanins des pépins et des peaux s’affinent.',
             'For forty to fifty days the berries fill with sugar, lose acidity and gain aroma and colour; the tannins in seeds and skins soften.'),
       work=('Contrôles de maturité : prélèvement de baies, mesure du sucre et de l’acidité, dégustation des baies. Préparation du matériel et des équipes.',
             'Ripeness checks: berry sampling, measuring sugar and acidity, tasting berries. Equipment and crews prepared.'),
       risks=[(('Pourriture grise', 'Grey rot'), TH + 'pourriture-grise'), (('Vers de la grappe', 'Grape moths'), TH + 'autres')],
       pro=[(('Évolution type', 'Typical evolution'),
             ('Les sucres passent d’environ 20 g/L à la véraison à 180–250 g/L ; l’acide malique est respiré, d’autant plus vite qu’il fait chaud ; l’acide tartrique reste stable.',
              'Sugars rise from about 20 g/L at véraison to 180–250 g/L; malic acid is respired, faster in hot weather; tartaric acid stays stable.')),
            (('Ban des vendanges', 'Official harvest start'),
             ('Pour les AOC, la date d’ouverture des vendanges est fixée chaque année par arrêté préfectoral, sur proposition de l’ODG et après avis de l’INAO, à partir des contrôles de maturité.',
              'For AOCs, the harvest opening date is set every year by prefectoral order, on the proposal of the growers’ body (ODG) and after INAO’s opinion, based on ripeness checks.'))]),
  dict(n=8, span=(8.6, 9.8), col='#a0283c', name=('Vendanges', 'Harvest'),
       period=('septembre à octobre', 'September to October'), bbch='89', bag='N',
       what=('Le raisin est cueilli au moment choisi par le vigneron, selon le style de vin voulu : plus tôt pour la fraîcheur des effervescents, plus tard pour la richesse ou les vins doux.',
             'The grapes are picked when the grower decides, according to the wine style: earlier for the freshness of sparkling wines, later for richness or sweet wines.'),
       work=('Vendange à la main ou à la machine, tri, transport rapide au chai. Chapitre 9 à venir.',
             'Hand or machine picking, sorting, quick transport to the winery. Chapter 9 to come.'),
       risks=[(('Pluie, pourriture', 'Rain, rot'), TH + 'pourriture-grise')],
       pro=[(('Avance des dates', 'Earlier dates'),
             ('Avec le réchauffement, les vendanges ont lieu en moyenne deux à trois semaines plus tôt qu’il y a quarante ans ; en Languedoc, elles commencent souvent dès la mi-août.',
              'With climate warming, harvests now take place on average two to three weeks earlier than forty years ago; in Languedoc they often start in mid-August.')),
            (('Après la récolte', 'After picking'),
             ('Les feuilles restent actives plusieurs semaines : c’est le moment où la vigne reconstitue ses réserves pour l’année suivante. Une défoliation précoce (maladie, gel d’automne) pénalise le millésime suivant.',
              'The leaves stay active for several weeks: this is when the vine rebuilds its reserves for the next year. Early defoliation (disease, autumn frost) hurts the following vintage.'))]),
  dict(n=9, span=(9.8, 10.9), col='#d39a2a', name=('Chute des feuilles', 'Leaf fall'),
       period=('octobre à novembre', 'October to November'), bbch='91–97', bag='—',
       what=('Les feuilles jaunissent ou rougissent, puis tombent aux premières gelées. La sève redescend, les sarments achèvent de s’aoûter et la vigne entre en dormance.',
             'Leaves turn yellow or red, then fall at the first frosts. The sap withdraws, the canes finish hardening and the vine goes dormant.'),
       work=('Buttage (remonter la terre au pied des ceps contre le froid), apport de fumure ou de compost, semis des couverts végétaux, plantations.',
             'Hilling up soil around the vine base against the cold, spreading manure or compost, sowing cover crops, planting.'),
       risks=[(('Couleurs anormales : virus, flavescence', 'Abnormal colours: virus, flavescence'), TH + 'flavescence-doree')],
       pro=[(('Mise en réserve', 'Storing reserves'),
             ('Amidon et azote migrent des feuilles vers le bois et les racines avant leur chute ; la qualité de cette mise en réserve conditionne le débourrement suivant.',
              'Starch and nitrogen move from the leaves into the wood and roots before leaf fall; how well this happens determines the next budburst.'))]),
]

MONTHS = [('Janv.', 'Jan'), ('Févr.', 'Feb'), ('Mars', 'Mar'), ('Avr.', 'Apr'), ('Mai', 'May'), ('Juin', 'Jun'),
          ('Juil.', 'Jul'), ('Août', 'Aug'), ('Sept.', 'Sep'), ('Oct.', 'Oct'), ('Nov.', 'Nov'), ('Déc.', 'Dec')]

INK = '#3b2a1e'


def svg_text(x, y, pair, size=14, anchor='middle', weight='400', fill=INK, extra=''):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'font-family="Iowan Old Style,Palatino,Georgia,serif" {extra}data-fr="{att(pair[0])}" data-en="{att(pair[1])}">{pair[0]}</text>')


def arc(cx, cy, r1, r2, m0, m1):
    """Ring sector between radii r1<r2 from month m0 to m1 (0 = 1 Jan at 12 o'clock, clockwise)."""
    a0 = math.radians(m0 * 30 - 90)
    a1 = math.radians(m1 * 30 - 90)
    large = 1 if (m1 - m0) * 30 > 180 else 0
    p = lambda r, a: (cx + r * math.cos(a), cy + r * math.sin(a))
    x0, y0 = p(r2, a0); x1, y1 = p(r2, a1); x2, y2 = p(r1, a1); x3, y3 = p(r1, a0)
    return (f'M{x0:.1f} {y0:.1f} A{r2} {r2} 0 {large} 1 {x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f} '
            f'A{r1} {r1} 0 {large} 0 {x3:.1f} {y3:.1f} Z')


def wheel():
    cx = cy = 330
    s = [f'<svg class="diagram wheel" viewBox="0 0 660 660" role="img" aria-label="Roue du cycle annuel de la vigne / The vine’s annual cycle wheel">']
    # month ring
    for i, m in enumerate(MONTHS):
        s.append(f'<path d="{arc(cx, cy, 262, 300, i, i + 1)}" fill="{"#efe5cf" if i % 2 else "#f6eedd"}" stroke="#d9c9a3" stroke-width="1"/>')
        a = math.radians((i + .5) * 30 - 90)
        s.append(svg_text(cx + 281 * math.cos(a), cy + 281 * math.sin(a) + 5, m, 14, weight='600', fill='#8a5a2b'))
    # stage ring
    for st in STAGES:
        m0, m1 = st['span']
        s.append(f'<a href="#stade-{st["n"]}" class="w-seg"><path d="{arc(cx, cy, 168, 258, m0, m1)}" fill="{st["col"]}" stroke="#fbf6ea" stroke-width="3"/>')
        a = math.radians(((m0 + m1) / 2) * 30 - 90)
        x, y = cx + 213 * math.cos(a), cy + 213 * math.sin(a)
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="17" fill="#fbf6ea" opacity=".95"/>'
                 f'<text x="{x:.1f}" y="{y + 6:.1f}" text-anchor="middle" font-size="17" font-weight="700" fill="{st["col"]}" font-family="Iowan Old Style,Palatino,Georgia,serif">{st["n"]}</text></a>')
    # seasons ring
    seasons = [((11, 14), ('Hiver', 'Winter'), '#c9d6e3'), ((2, 5), ('Printemps', 'Spring'), '#d8e6b8'),
               ((5, 8), ('Été', 'Summer'), '#f1dd9a'), ((8, 11), ('Automne', 'Autumn'), '#efc39a')]
    for (m0, m1), name, col in seasons:
        s.append(f'<path d="{arc(cx, cy, 120, 164, m0, m1)}" fill="{col}" stroke="#fbf6ea" stroke-width="3"/>')
        mid = math.radians(((m0 + m1) / 2) * 30 - 90)
        a0, a1 = math.radians(m0 * 30 - 90), math.radians(m1 * 30 - 90)
        pid = f'season{int(m0)}'
        if math.sin(mid) > 0.3:   # bottom of the wheel: run the path anticlockwise so the text is upright
            r = 148
            p0 = (cx + r * math.cos(a1), cy + r * math.sin(a1)); p1 = (cx + r * math.cos(a0), cy + r * math.sin(a0))
            d = f'M{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 0 0 {p1[0]:.1f} {p1[1]:.1f}'
        else:
            r = 137
            p0 = (cx + r * math.cos(a0), cy + r * math.sin(a0)); p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
            d = f'M{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}'
        s.append(f'<path id="{pid}" d="{d}" fill="none"/>'
                 f'<text font-size="15" font-weight="600" fill="#4b3a2a" font-family="Iowan Old Style,Palatino,Georgia,serif" letter-spacing="1">'
                 f'<textPath href="#{pid}" startOffset="50%" text-anchor="middle" data-fr="{att(name[0])}" data-en="{att(name[1])}">{name[0]}</textPath></text>')
    # centre
    s.append(f'<circle cx="{cx}" cy="{cy}" r="114" fill="#fbf6ea" stroke="#d9c9a3"/>')
    s.append(svg_text(cx, cy - 14, ('Le cycle', 'The vine’s'), 24))
    s.append(svg_text(cx, cy + 14, ('de la vigne', 'year'), 24))
    s.append(svg_text(cx, cy + 44, ('hémisphère nord', 'northern hemisphere'), 13, fill='#8a7a64'))
    s.append('</svg>')
    return ''.join(s)


def wheel_legend():
    return ''.join(f'<a class="wl" href="#stade-{st["n"]}" style="--c:{st["col"]}"><span class="wl-n">{st["n"]}</span>'
                   f'<span>{t(st["name"], "b")}{t(st["period"], "small")}</span></a>' for st in STAGES)


def stage_cards():
    out = []
    for st in STAGES:
        risks = ''.join(f'<a href="{h}">{t(lbl)}</a>' for lbl, h in st['risks'])
        note = ''
        out.append(f'''
    <article class="stage" id="stade-{st['n']}" style="--c:{st['col']}">
      <div class="st-side"><img src="{IMG}stage{st['n']}.webp" alt="" loading="lazy" decoding="async" width="180" height="180">
        <div class="codes"><span title="BBCH">BBCH {st['bbch']}</span><span title="Baggiolini">Baggiolini {st['bag']}</span></div></div>
      <div class="st-body">
        <div class="st-head"><span class="st-n">{st['n']}</span><div><h3>{t(st['name'])}</h3>{t(st['period'], 'p', 'st-period')}</div></div>
        <div class="st-grid">
          <div><h4>{t(("Dans la vigne", "In the vine"))}</h4>{blk(st['what'])}</div>
          <div><h4>{t(("Au vignoble", "In the vineyard"))}</h4>{blk(st['work'])}</div>
        </div>
        <div class="st-risks"><h4>{t(("À surveiller", "Watch out for"))}</h4>{risks}</div>
        {note}
        {pro_panel(st['pro'])}
      </div>
    </article>''')
    return ''.join(out)


def two_years():
    """Two-year timeline: the reproductive cycle spans two seasons."""
    x0, w = 180, 480 / 24
    X = lambda m: x0 + m * w
    s = ['<svg class="diagram" viewBox="0 0 680 330" role="img" aria-label="Le cycle reproducteur sur deux ans / The two-year reproductive cycle">']
    s.append(f'<rect x="{X(0)}" y="40" width="{12 * w}" height="250" fill="#f3ead6"/><rect x="{X(12)}" y="40" width="{12 * w}" height="250" fill="#eef1dc"/>')
    s.append(svg_text(X(6), 30, ('Année N − 1', 'Year N − 1'), 16, weight='600', fill='#8a5a2b'))
    s.append(svg_text(X(18), 30, ('Année N (millésime)', 'Year N (vintage)'), 16, weight='600', fill='#4f6e22'))
    for m in range(25):
        s.append(f'<line x1="{X(m):.1f}" y1="40" x2="{X(m):.1f}" y2="290" stroke="#ffffff" stroke-width="{1.5 if m % 12 else 2.5}"/>')
    for m in range(24):
        s.append(f'<text x="{X(m + .5):.1f}" y="306" text-anchor="middle" font-size="11" fill="#8a7a64" font-family="Iowan Old Style,Georgia,serif">{"JFMAMJJASOND"[m % 12]}</text>')

    def bar(y, m0, m1, col, pair, hatch=False):
        fill = 'url(#hatch)' if hatch else col
        r = f'<rect x="{X(m0):.1f}" y="{y}" width="{(m1 - m0) * w:.1f}" height="26" rx="6" fill="{fill}" stroke="{col}" stroke-width="1.2"/>'
        return r + svg_text(X((m0 + m1) / 2), y + 18, pair, 12.5, fill='#fff' if not hatch else INK, weight='600')
    s.append('<defs><pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="7" height="7" fill="#e8dcc0"/><line x1="0" y1="0" x2="0" y2="7" stroke="#b9a37a" stroke-width="2.5"/></pattern></defs>')
    rows = [  # label, bars, side note (text after/before the bars)
      (('Le rameau de l’an N−1', 'Shoot of year N−1'), [(3, 10.8, '#7aa23c', ('pousse et récolte N−1', 'growth, crop N−1'), False)], None),
      (('Ses bourgeons', 'Its buds'), [(5, 8, '#c08a1a', ('initiation', 'initiation'), False),
                                       (8, 14.5, '#b9a37a', ('dormance', 'dormancy'), True),
                                       (14.5, 15.8, '#9b4f8a', ('', ''), False)],
       ('after', 15.8, ('fleurs formées', 'flowers formed'))),
      (('Le sarment taillé', 'The pruned cane'), [(11.5, 14.2, '#8a5a2b', ('taille', 'pruning'), False)], None),
      (('Le rameau de l’an N', 'Shoot of year N'), [(15, 22.8, '#5f9a3a', ('débourrement → chute', 'budburst → leaf fall'), False)], None),
      (('Les grappes de l’an N', 'Bunches of year N'), [(17, 18, '#c9b84a', ('', ''), False), (18, 19.6, '#5f9a3a', ('', ''), False),
                                                       (19.6, 20.6, '#9b4f8a', ('', ''), False), (20.6, 21.8, '#a0283c', ('', ''), False)],
       ('before', 17, ('floraison → véraison → vendange', 'flowering → véraison → harvest'))),
    ]
    y = 56
    for lbl, bars, side in rows:
        s.append(svg_text(X(0) - 8, y + 18, lbl, 13, anchor='end', fill=INK))
        for m0, m1, col, pair, h in bars:
            s.append(bar(y, m0, m1, col, pair, h))
        if side:
            where, m, pair = side
            if where == 'after':
                s.append(svg_text(X(m) + 6, y + 18, pair, 12.5, anchor='start', fill=INK, extra='font-style="italic" '))
            else:
                s.append(svg_text(X(m) - 6, y + 18, pair, 12.5, anchor='end', fill=INK, extra='font-style="italic" '))
        y += 46
    s.append('</svg>')
    return ''.join(s)


EPOCHS = [
  (('Première époque', 'First period'), ('même date que le Chasselas', 'same time as Chasselas'), '#7aa23c',
   ['Chasselas', 'Pinot noir', 'Chardonnay', 'Gamay', 'Pinot gris', 'Sauvignon blanc', 'Gewurztraminer']),
  (('Deuxième époque', 'Second period'), ('≈ 12 à 15 jours après', '≈ 12–15 days later'), '#9b4f8a',
   ['Merlot', 'Syrah', 'Cabernet franc', 'Chenin', 'Riesling', 'Sémillon', ('Cabernet Sauvignon (tardif)', 'Cabernet Sauvignon (late)')]),
  (('Troisième époque', 'Third period'), ('≈ 3 à 4 semaines après', '≈ 3–4 weeks later'), '#a0283c',
   ['Grenache', 'Mourvèdre', 'Carignan', 'Ugni blanc', 'Clairette']),
]

HARVEST = [  # region, start, end (months from 1 Jan; 7.0 = 1 Aug), late tail end (sweet / late harvest) or None
  (('Languedoc-Roussillon', 'Languedoc-Roussillon'), 7.5, 8.9, None),
  (('Provence', 'Provence'), 7.7, 8.9, None),
  (('Beaujolais', 'Beaujolais'), 7.8, 8.6, None),
  (('Champagne', 'Champagne'), 7.8, 8.7, None),
  (('Bourgogne', 'Burgundy'), 7.9, 8.8, None),
  (('Vallée du Rhône sud', 'Southern Rhône'), 8.0, 9.2, None),
  (('Bordeaux', 'Bordeaux'), 7.9, 9.4, None),
  (('Alsace', 'Alsace'), 8.1, 9.4, 10.6),
  (('Loire', 'Loire'), 8.0, 9.5, 10.8),
  (('Sauternes', 'Sauternes'), 8.4, 10.5, None),
]


def harvest_chart():
    rows = []
    for name, a, b, tail in HARVEST:
        lft = (a - 7) / 5 * 100
        wid = (b - a) / 5 * 100
        tl = ''
        if tail:
            tl = f'<i class="tail" style="left:{(b - 7) / 5 * 100:.1f}%;width:{(tail - b) / 5 * 100:.1f}%"></i>'
        rows.append(f'<div class="hv-row"><span class="hv-l">{t(name)}</span><div class="hv-track">'
                    f'<i class="hv-bar" style="left:{lft:.1f}%;width:{wid:.1f}%"></i>{tl}</div></div>')
    head = ''.join(f'<span>{t(m)}</span>' for m in [('Août', 'Aug'), ('Sept.', 'Sep'), ('Oct.', 'Oct'), ('Nov.', 'Nov'), ('Déc.', 'Dec')])
    return f'<div class="hv"><div class="hv-row hv-head"><span class="hv-l"></span><div class="hv-months">{head}</div></div>{"".join(rows)}</div>'


def epochs():
    return ''.join(f'<div class="ep" style="--c:{c}"><h4>{t(n)}</h4>{t(d, "p", "ep-d")}<ul>{"".join(f"<li>{t(v) if isinstance(v, tuple) else v}</li>" for v in vs)}</ul></div>'
                   for n, d, c, vs in EPOCHS)


CAL = [
  (('Janvier', 'January'), ('Taille. Broyage des sarments.', 'Pruning. Shredding cuttings.')),
  (('Février', 'February'), ('Taille, réparation du palissage.', 'Pruning, trellis repairs.')),
  (('Mars', 'March'), ('Fin de la taille, pliage et attachage, débuttage. Les pleurs.', 'End of pruning, bending and tying canes, removing the winter mound. Bleeding.')),
  (('Avril', 'April'), ('Débourrement. Lutte contre le gel, plantations.', 'Budburst. Frost protection, planting.')),
  (('Mai', 'May'), ('Ébourgeonnage, relevage, premiers traitements, travail du sol.', 'Shoot thinning, shoot lifting, first sprays, soil work.')),
  (('Juin', 'June'), ('Floraison. Palissage, rognage, traitements.', 'Flowering. Trellising, trimming, sprays.')),
  (('Juillet', 'July'), ('Rognage, effeuillage, vendange verte.', 'Trimming, leaf removal, green harvest.')),
  (('Août', 'August'), ('Véraison. Contrôles de maturité, préparation des vendanges.', 'Véraison. Ripeness checks, harvest preparation.')),
  (('Septembre', 'September'), ('Vendanges.', 'Harvest.')),
  (('Octobre', 'October'), ('Fin des vendanges, nettoyage.', 'End of harvest, clean-up.')),
  (('Novembre', 'November'), ('Chute des feuilles. Buttage, fumure, semis des couverts, plantations.', 'Leaf fall. Hilling up, manuring, sowing cover crops, planting.')),
  (('Décembre', 'December'), ('Dormance. Début de la taille.', 'Dormancy. Pruning begins.')),
]


def grower_calendar():
    seas = ['#6f8fb0', '#6f8fb0', '#7aa23c', '#7aa23c', '#7aa23c', '#c9a227', '#c9a227', '#c9a227', '#c0703a', '#c0703a', '#c0703a', '#6f8fb0']
    return ''.join(f'<div class="mo" style="--c:{seas[i]}"><b>{t(m)}</b>{t(txt, "span")}</div>' for i, (m, txt) in enumerate(CAL))


BBCH = [  # code, baggiolini, fr, en
  ('00', 'A', 'Bourgeon d’hiver, dormance', 'Winter bud, dormancy'),
  ('01–03', 'B', 'Gonflement du bourgeon', 'Bud swelling'),
  ('05', 'B', 'Stade « dans le coton »', 'Woolly bud'),
  ('07–09', 'C', 'Pointe verte', 'Green tip'),
  ('11', 'D–E', 'Première feuille étalée', 'First leaf unfolded'),
  ('12–19', 'E', '2 à 9 feuilles étalées', '2 to 9 leaves unfolded'),
  ('53', 'F', 'Inflorescences visibles', 'Inflorescences visible'),
  ('55', 'G', 'Inflorescences séparées', 'Inflorescences swelling'),
  ('57', 'H', 'Boutons floraux séparés', 'Flowers separating'),
  ('61', 'I', 'Début floraison (10 % de capuchons tombés)', 'Beginning of flowering (10 % caps off)'),
  ('65', 'I', 'Pleine floraison (50 %)', 'Full flowering (50 %)'),
  ('69', 'I', 'Fin de floraison', 'End of flowering'),
  ('71', 'J', 'Nouaison', 'Fruit set'),
  ('73', 'K', 'Baies taille « plomb »', 'Berries groat-sized'),
  ('75', 'K', 'Baies taille « petit pois »', 'Berries pea-sized'),
  ('77–79', 'L', 'Fermeture de la grappe', 'Bunch closure'),
  ('81–83', 'M', 'Véraison : début de coloration', 'Véraison: colour change begins'),
  ('85', 'M', 'Ramollissement des baies', 'Berries softening'),
  ('89', 'N', 'Maturité de récolte', 'Ripe for harvest'),
  ('91', '—', 'Après vendange, fin de l’aoûtement', 'After harvest, end of wood ripening'),
  ('92–97', '—', 'Coloration puis chute des feuilles', 'Leaf discolouration, then leaf fall'),
]


def bbch_table():
    return ''.join(f'<tr><td class="code">{c}</td><td class="code">{b}</td><td>{t((fr, en))}</td></tr>' for c, b, fr, en in BBCH)


PRO_HEAT = [
  (('Degrés-jours', 'Degree-days'),
   ('On additionne chaque jour la température moyenne au-dessus de 10 °C (le zéro de végétation). Exemple : une journée à 22 °C de moyenne compte 12 degrés-jours. Un cépage précoce a besoin de moins de chaleur cumulée qu’un cépage tardif pour mûrir.',
    'Each day, the mean temperature above 10 °C (the growth threshold) is added up. Example: a day averaging 22 °C counts 12 degree-days. An early variety needs less accumulated heat to ripen than a late one.')),
  (('Indice de Winkler', 'Winkler index'),
   ('Somme des degrés-jours (base 10 °C) du 1<sup>er</sup> avril au 31 octobre, créée en Californie dans les années 1940 ; cinq régions climatiques de I (fraîche) à V (chaude).',
    'Sum of degree-days (base 10 °C) from 1 April to 31 October, devised in California in the 1940s; five climate regions from I (cool) to V (hot).')),
  (('Indice héliothermique de Huglin', 'Huglin heliothermal index'),
   ('Plus utilisé en Europe : il combine températures moyennes et maximales d’avril à septembre et corrige selon la latitude (longueur du jour). Classes : très frais ≤ 1 500, frais 1 500–1 800, tempéré 1 800–2 100, tempéré chaud 2 100–2 400, chaud 2 400–3 000. Historiquement, la Champagne et l’Alsace se situaient dans les classes fraîches, Bordeaux en tempéré, le Languedoc en chaud ; toutes ces valeurs augmentent avec le réchauffement.',
    'More widely used in Europe: it combines mean and maximum temperatures from April to September and adjusts for latitude (day length). Classes: very cool ≤ 1,500, cool 1,500–1,800, temperate 1,800–2,100, warm temperate 2,100–2,400, warm 2,400–3,000. Historically Champagne and Alsace fell in the cool classes, Bordeaux in temperate and Languedoc in warm; all these values are rising with climate warming.')),
  (('Échelle de Pulliat', 'Pulliat scale'),
   ('Classement de la précocité de maturité établi au XIX<sup>e</sup> siècle par Victor Pulliat, avec le Chasselas pour référence. Les écarts réels varient selon le climat et l’année.',
    'Ranking of ripening earliness drawn up in the 19th century by Victor Pulliat, using Chasselas as the reference. Actual gaps vary with climate and year.')),
]

SOURCES = [
  ('Lorenz D. H. et al., « Growth stages of the grapevine… (BBCH) », <i>Australian Journal of Grape and Wine Research</i>, 1995 ; Baggiolini M., 1952.', 'Lorenz D. H. et al., “Growth stages of the grapevine… (BBCH)”, <i>Australian Journal of Grape and Wine Research</i>, 1995; Baggiolini M., 1952.'),
  ('Huglin P., <i>Biologie et écologie de la vigne</i>, Payot, 1986 ; Tonietto J., Carbonneau A., « A multicriteria climatic classification system for grape-growing regions worldwide », <i>Agricultural and Forest Meteorology</i>, 2004.', 'Huglin P., <i>Biologie et écologie de la vigne</i>, Payot, 1986; Tonietto J., Carbonneau A., “A multicriteria climatic classification system for grape-growing regions worldwide”, <i>Agricultural and Forest Meteorology</i>, 2004.'),
  ('Reynier A., <i>Manuel de viticulture</i>, Lavoisier Tec & Doc.', 'Reynier A., <i>Manuel de viticulture</i>, Lavoisier Tec & Doc.'),
  ('IFV et chambres d’agriculture : bulletins de santé du végétal, stades phénologiques.', 'IFV and chambers of agriculture: plant-health bulletins, phenological stages.'),
]


def main():
    tpl = (HERE / 'cycle_template.html').read_text()
    rep = {
        '@@BASE_CSS@@': base_css(),
        '@@PRO_ICON@@': PRO_ICON,
        '@@PLATE_CYCLE@@': plate(IMG + 'cycle_infographic.webp', 'Le cycle de croissance de la vigne / Grapevine growth cycle', 1448, 1086, 'wide'),
        '@@WHEEL@@': wheel(),
        '@@WHEEL_LEGEND@@': wheel_legend(),
        '@@STAGES@@': stage_cards(),
        '@@TWO_YEARS@@': two_years(),
        '@@EPOCHS@@': epochs(),
        '@@HARVEST@@': harvest_chart(),
        '@@PRO_HEAT@@': pro_panel(PRO_HEAT),
        '@@CALENDAR@@': grower_calendar(),
        '@@BBCH@@': bbch_table(),
        '@@CHAPTERS@@': chapter_nav(2),
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
