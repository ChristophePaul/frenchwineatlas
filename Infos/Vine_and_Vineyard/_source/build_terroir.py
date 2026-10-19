#!/usr/bin/env python3
"""Build Infos/Vine_and_Vineyard/Vine_Terroir.html (chapter 3 — terroir & site).
Run:  python3 "WEB Site/Infos/Vine_and_Vineyard/_source/build_terroir.py"
Static text is in terroir_template.html; diagrams, soil cards, panels below.
"""
import random
from urllib.parse import quote
from common import HERE, att, t, blk, base_css, plate, pro_panel, chapter_nav, PRO_ICON

OUT = HERE.parent / 'Vine_Terroir.html'
IMG = 'img/terroir/'
INK = '#3b2a1e'
SERIF = 'Iowan Old Style,Palatino,Georgia,serif'
CLIMATS = '../../Bourgogne%20Regions/Bourgogne%20climats/'
PLAN = '../../Plan%20Cadastraux/'


def climat(village):
    return CLIMATS + quote(f'{village} — Climats 1er Cru, relief 5 m & climats communaux · Carte.html')


def lbl(x, y, pair, anchor='start', size=14, px=None, py=None, sx=None, sy=None, fill=INK, weight='400'):
    line = ''
    if px is not None:
        x0 = sx if sx is not None else (x + 4 if anchor == 'end' else x - 4)
        y0 = sy if sy is not None else y - 4
        line = (f'<path d="M{x0} {y0} L{px} {py}" fill="none" stroke="#7a6650" stroke-width="1"/>'
                f'<circle cx="{px}" cy="{py}" r="2.4" fill="{INK}"/>')
    return (line + f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'font-family="{SERIF}" data-fr="{att(pair[0])}" data-en="{att(pair[1])}">{pair[0]}</text>')


# ------------------------------------------------------------ hillside microclimate diagram
def hillside():
    s = ['<svg class="diagram" viewBox="0 0 680 400" role="img" aria-label="Le coteau et son microclimat / The hillside and its microclimate">']
    s.append('<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#dcebf3"/><stop offset="1" stop-color="#f6f1e2"/></linearGradient>'
             '<marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="#3f7fae" stroke-width="1.8"/></marker>'
             '<marker id="as" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="#d29a1e" stroke-width="1.8"/></marker></defs>')
    s.append('<rect x="0" y="0" width="680" height="400" fill="url(#sky)"/>')
    slope = 'M0 118 L150 112 C232 116 262 160 332 220 C392 270 452 302 540 314 L680 318'
    s.append(f'<path d="{slope} L680 400 L0 400 Z" fill="#a9c46b"/>')
    s.append(f'<path d="{slope}" fill="none" stroke="#6f8f34" stroke-width="2"/>')
    # soil layers hint at the front
    s.append('<path d="M0 360 L680 360 L680 400 L0 400 Z" fill="#c8a978" opacity=".55"/>')
    # forest on the crest
    rnd = random.Random(3)
    for i in range(16):
        x = 8 + i * 10 + rnd.uniform(-3, 3); y = 112 - rnd.uniform(0, 4)
        h = rnd.uniform(16, 26)
        s.append(f'<path d="M{x:.1f} {y:.1f} l-7 0 l7 -{h:.1f} l7 {h:.1f} Z" fill="#3f6b2e"/>')
    # vine rows on the slope
    for k in range(26):
        tt = k / 25
        x = 165 + tt * 360; y = 116 + (tt ** 1.15) * 196
        s.append(f'<line x1="{x:.1f}" y1="{y + 4:.1f}" x2="{x:.1f}" y2="{y - 7:.1f}" stroke="#4f6e22" stroke-width="2.4" stroke-linecap="round"/>')
    # village & river on the plain
    s.append('<rect x="560" y="300" width="14" height="12" fill="#e8d8b8" stroke="#8a6a44"/><path d="M558 300 l9 -8 l9 8 Z" fill="#a0402e"/>'
             '<rect x="578" y="304" width="12" height="9" fill="#e8d8b8" stroke="#8a6a44"/><path d="M576 304 l8 -7 l8 7 Z" fill="#a0402e"/>')
    s.append('<path d="M612 319 C630 322 650 321 676 323" fill="none" stroke="#4f8fc9" stroke-width="5" stroke-linecap="round"/>')
    # sun + rays
    s.append('<circle cx="626" cy="58" r="22" fill="#f2c14e"/>' + ''.join(
        f'<line x1="{626 + 30 * c:.1f}" y1="{58 + 30 * d:.1f}" x2="{626 + 38 * c:.1f}" y2="{58 + 38 * d:.1f}" stroke="#f2c14e" stroke-width="2.4" stroke-linecap="round"/>'
        for c, d in [(1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7)]))
    s.append('<path d="M596 74 L360 230" stroke="#d29a1e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#as)"/>'
             '<path d="M604 84 L420 266" stroke="#d29a1e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#as)"/>'
             '<path d="M618 88 L648 306" stroke="#d29a1e" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#as)"/>')
    # cold air flowing down
    s.append('<path d="M190 100 C250 120 280 165 330 200" fill="none" stroke="#3f7fae" stroke-width="2.4" stroke-dasharray="7 5" marker-end="url(#ah)"/>'
             '<path d="M300 170 C360 220 420 262 500 286" fill="none" stroke="#3f7fae" stroke-width="2.4" stroke-dasharray="7 5" marker-end="url(#ah)"/>')
    s.append('<ellipse cx="600" cy="316" rx="78" ry="14" fill="#9cc6e6" opacity=".55"/>')
    # labels
    s.append(lbl(14, 40, ('Forêt sur le plateau :', 'Forest on the plateau:'), size=14, weight='600'))
    s.append(lbl(14, 58, ('elle abrite du vent d’ouest', 'shelter from westerly winds'), size=14, px=80, py=100, sx=60, sy=64))
    s.append(lbl(170, 300, ('Mi-coteau : sols drainés,', 'Mid-slope: well-drained soils,'), size=14, weight='600'))
    s.append(lbl(170, 318, ('soleil reçu presque de face', 'sun striking almost head-on'), size=14, px=350, py=236, sx=300, sy=304))
    s.append(lbl(250, 92, ('L’air froid, plus lourd,', 'Cold, heavy air'), size=14))
    s.append(lbl(250, 110, ('glisse vers le bas', 'drains downhill'), size=14, px=262, py=136, sx=262, sy=114))
    s.append(lbl(592, 30, ('Soleil du matin (est)', 'Morning sun (east)'), anchor='end', size=14, fill='#9a6a12', weight='600'))
    s.append(lbl(460, 354, ('Plaine : sols profonds, gelées', 'Plain: deep soils, frost pocket'), size=14, weight='600'))
    s.append(lbl(460, 372, ('et humidité ; rivière', 'and damp; river nearby'), size=14))
    s.append('</svg>')
    return ''.join(s)


# ------------------------------------------------------------ soil swatches
def swatch(kind, seed):
    rnd = random.Random(seed)
    W, H = 200, 120
    s = [f'<svg class="swatch" viewBox="0 0 {W} {H}" aria-hidden="true">']
    top = '<rect x="0" y="0" width="200" height="22" fill="#6b4a2b"/>' + ''.join(
        f'<circle cx="{rnd.uniform(0, 200):.1f}" cy="{rnd.uniform(3, 20):.1f}" r="{rnd.uniform(.8, 2):.1f}" fill="#4a321c"/>' for _ in range(40))
    top += ''.join(f'<path d="M{x} 0 q-3 -10 2 -14" stroke="#5f8a34" stroke-width="2" fill="none"/>' for x in range(10, 200, 24))
    body = ''
    if kind == 'limestone':
        body = '<rect y="22" width="200" height="98" fill="#e7dcc0"/>'
        for r, y in enumerate(range(22, 120, 16)):
            off = 0 if r % 2 else 20
            body += f'<line x1="0" y1="{y}" x2="200" y2="{y}" stroke="#b9a983" stroke-width="1.4"/>'
            body += ''.join(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y + 16}" stroke="#b9a983" stroke-width="1.4"/>' for x in range(off, 200, 40))
    elif kind == 'chalk':
        body = '<rect y="22" width="200" height="98" fill="#f6f3ea"/>' + ''.join(
            f'<circle cx="{rnd.uniform(0, 200):.1f}" cy="{rnd.uniform(24, 120):.1f}" r="{rnd.uniform(.6, 1.5):.1f}" fill="#cfc8b6"/>' for _ in range(90))
        body += ''.join(f'<ellipse cx="{rnd.uniform(10, 190):.1f}" cy="{rnd.uniform(40, 112):.1f}" rx="6" ry="4" fill="#5b5b62" opacity=".8"/>' for _ in range(3))
    elif kind == 'marl':
        cols = ['#cfc6b4', '#b8b3a8', '#d9cfb9', '#a9a49a']
        body = ''.join(f'<rect y="{22 + i * 14}" width="200" height="14" fill="{cols[i % 4]}"/>' for i in range(7))
        body += ''.join(f'<path d="M0 {22 + i * 14} q50 {rnd.uniform(-3, 3):.1f} 100 0 t100 0" stroke="#8f8a80" stroke-width=".8" fill="none"/>' for i in range(1, 7))
    elif kind == 'clay':
        body = '<rect y="22" width="200" height="98" fill="#9b6b48"/>'
        for _ in range(9):
            x = rnd.uniform(10, 190); y = rnd.uniform(30, 110)
            body += f'<path d="M{x:.1f} {y:.1f} l{rnd.uniform(-12, 12):.1f} {rnd.uniform(6, 14):.1f} l{rnd.uniform(-8, 8):.1f} {rnd.uniform(4, 10):.1f}" stroke="#6e4428" stroke-width="1.4" fill="none"/>'
        body += '<rect y="84" width="200" height="36" fill="#7c8aa0" opacity=".35"/>'
    elif kind == 'gravel':
        body = '<rect y="22" width="200" height="98" fill="#d9c49a"/>'
        for _ in range(55):
            x = rnd.uniform(0, 200); y = rnd.uniform(26, 118); r = rnd.uniform(4, 10)
            c = rnd.choice(['#f0ead8', '#cdbb94', '#e5d6b6', '#b9a37a', '#ece2c8'])
            body += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r:.1f}" ry="{r * .7:.1f}" fill="{c}" stroke="#8f7a52" stroke-width=".8"/>'
    elif kind == 'galets':
        body = '<rect y="22" width="200" height="98" fill="#b8664a"/>'
        for _ in range(16):
            x = rnd.uniform(0, 200); y = rnd.uniform(30, 116); r = rnd.uniform(10, 18)
            body += f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{r:.1f}" ry="{r * .65:.1f}" fill="#e9dcc4" stroke="#8a6a52" stroke-width="1"/>'
    elif kind == 'granite':
        body = '<rect y="22" width="200" height="98" fill="#d7a98f"/>' + ''.join(
            f'<rect x="{rnd.uniform(0, 196):.1f}" y="{rnd.uniform(24, 116):.1f}" width="{rnd.uniform(2, 5):.1f}" height="{rnd.uniform(2, 4):.1f}" fill="{rnd.choice(["#3a3330", "#f2e6dc", "#b27a62", "#efe8e0"])}" transform="rotate({rnd.uniform(0, 90):.0f} 100 70)"/>'
            for _ in range(220))
    elif kind == 'schist':
        body = '<rect y="22" width="200" height="98" fill="#4f4a52"/>' + ''.join(
            f'<line x1="{x}" y1="22" x2="{x + 60}" y2="120" stroke="{rnd.choice(["#6a6470", "#39353d", "#7a7280"])}" stroke-width="{rnd.uniform(2, 5):.1f}"/>' for x in range(-60, 200, 7))
    elif kind == 'sand':
        body = '<rect y="22" width="200" height="98" fill="#ead7a4"/>' + ''.join(
            f'<circle cx="{rnd.uniform(0, 200):.1f}" cy="{rnd.uniform(24, 120):.1f}" r=".9" fill="{rnd.choice(["#c7a868", "#f7ecc8", "#b99450"])}"/>' for _ in range(420))
    elif kind == 'flint':
        body = '<rect y="22" width="200" height="98" fill="#a8774f"/>'
        for _ in range(11):
            x = rnd.uniform(10, 190); y = rnd.uniform(34, 110)
            body += (f'<path d="M{x:.1f} {y:.1f} l9 -6 l11 3 l4 9 l-8 7 l-12 -1 Z" fill="#6f7178" stroke="#e9e6df" stroke-width="1.6" '
                     f'transform="rotate({rnd.uniform(0, 180):.0f} {x:.1f} {y:.1f})"/>')
    elif kind == 'volcanic':
        body = '<rect y="22" width="200" height="98" fill="#3b3434"/>'
        for row, y in enumerate(range(28, 124, 18)):
            for x in range(-10 if row % 2 else 0, 210, 20):
                body += f'<path d="M{x} {y} l10 -5 l10 5 l0 11 l-10 5 l-10 -5 Z" fill="#4a4242" stroke="#2a2424" stroke-width="1"/>'
    s.append(body + top + '</svg>')
    return ''.join(s)


SOILS = [  # kind, name, what, wine effect, examples [(label, href|None)]
  ('limestone', ('Calcaire', 'Limestone'),
   ('Roche sédimentaire formée de coquilles et squelettes marins. Sols filtrants mais retenant un peu d’eau dans les fissures.', 'Sedimentary rock formed from marine shells and skeletons. Free-draining soils that still hold some water in their cracks.'),
   ('Vins tendus, frais, élégants ; le grand terrain du Pinot noir et du Chardonnay.', 'Taut, fresh, elegant wines; the great ground of Pinot Noir and Chardonnay.'),
   [('Côte d’Or', '../../Bourgogne%20Regions/Cote-d_Or.html'), ('Saint-Émilion (plateau)', PLAN + 'Bordeaux_RightBank/Saint-Emilion.html'), ('Sancerre', PLAN + 'Loire_Centre/Sancerre.html')]),
  ('chalk', ('Craie', 'Chalk'),
   ('Calcaire tendre et très poreux : il emmagasine l’eau comme une éponge et la restitue en été.', 'Soft, very porous limestone: it soaks up water like a sponge and releases it in summer.'),
   ('Acidité, finesse et longévité : la base des grands Champagnes.', 'Acidity, finesse and longevity: the foundation of great Champagne.'),
   [('Champagne', '../../Champagne.html'), ('Côte des Blancs', PLAN + 'Champagne_Grands_Crus/Champagne-Grands-Crus.html')]),
  ('marl', ('Marnes', 'Marl'),
   ('Mélange de calcaire et d’argile, souvent en couches. Plus frais et plus riche en eau que le calcaire pur.', 'A mix of limestone and clay, often layered. Cooler and moister than pure limestone.'),
   ('Vins amples et structurés ; les marnes kimméridgiennes de Chablis donnent leur tension minérale aux Chardonnays.', 'Broad, structured wines; Chablis’s Kimmeridgian marls give its Chardonnays their mineral tension.'),
   [('Chablis', '../../Bourgogne%20Regions/Chablis_et_de_l_Auxerrois.html'), ('Jura', '../../Jura.html')]),
  ('clay', ('Argile', 'Clay'),
   ('Particules très fines qui retiennent l’eau et les éléments nutritifs ; sols frais, lourds, qui se réchauffent lentement.', 'Very fine particles that hold water and nutrients; cool, heavy soils that warm up slowly.'),
   ('Vins ronds, charnus, puissants ; le Merlot y excelle, comme sur la « boutonnière » d’argile bleue de Pomerol.', 'Round, fleshy, powerful wines; Merlot excels there, as on Pomerol’s “buttonhole” of blue clay.'),
   [('Pomerol', PLAN + 'Bordeaux_RightBank/Pomerol.html')]),
  ('gravel', ('Graves', 'Gravel'),
   ('Galets et graviers apportés par les fleuves, mêlés de sable. Très drainants, ils emmagasinent la chaleur du jour.', 'Pebbles and gravel carried down by rivers, mixed with sand. Very free-draining, they store the day’s heat.'),
   ('Le Cabernet Sauvignon, cépage tardif, y mûrit pleinement : les grands vins du Médoc et des Graves.', 'Late-ripening Cabernet Sauvignon ripens fully there: the great wines of the Médoc and Graves.'),
   [('Médoc', PLAN + 'Bordeaux_LeftBank/Medoc.html'), ('Pessac-Léognan', PLAN + 'Bordeaux_LeftBank/Pessac-Leognan.html')]),
  ('galets', ('Galets roulés', 'Rounded pebbles'),
   ('Gros galets de quartzite polis par le Rhône, sur argile rouge. Ils restituent la chaleur la nuit.', 'Large quartzite cobbles polished by the Rhône, over red clay. They give back heat at night.'),
   ('Grenache très mûr, vins chaleureux et généreux.', 'Very ripe Grenache, warm, generous wines.'),
   [('Châteauneuf-du-Pape', PLAN + 'Cotes_du_Rhone_Sud/Chateauneuf-du-Pape.html')]),
  ('granite', ('Granite', 'Granite'),
   ('Roche cristalline dure qui se désagrège en sable grossier (« arène ») : sols acides, pauvres, drainants.', 'Hard crystalline rock that weathers into coarse sand (“arène”): acidic, poor, free-draining soils.'),
   ('Vins fruités et floraux, à la structure fine : Gamay des crus du Beaujolais, Syrah de l’Hermitage.', 'Fruity, floral wines with fine structure: Gamay in the Beaujolais crus, Syrah on Hermitage.'),
   [('Beaujolais', '../../Bourgogne%20Regions/Beaujolais.html'), ('Hermitage', PLAN + 'Cotes_du_Rhone/Hermitage.html')]),
  ('schist', ('Schiste', 'Schist'),
   ('Roche feuilletée, souvent sombre, qui se débite en plaquettes ; sols maigres et chauds.', 'Flaky rock, often dark, that splits into plates; thin, warm soils.'),
   ('Vins concentrés, épicés ou très purs : Banyuls, Collioure, Faugères, Anjou « noir », Côte-Rôtie.', 'Concentrated, spicy or very pure wines: Banyuls, Collioure, Faugères, “black” Anjou, Côte-Rôtie.'),
   [('Banyuls', PLAN + 'Roussillon/Banyuls.html'), ('Côte-Rôtie', PLAN + 'Cotes_du_Rhone/Cote-Rotie.html')]),
  ('sand', ('Sable', 'Sand'),
   ('Grains grossiers qui ne retiennent presque rien ; le phylloxéra ne peut pas y vivre.', 'Coarse grains that hold almost nothing; phylloxera cannot live there.'),
   ('Vins légers, fruités, souvent de vignes franches de pied.', 'Light, fruity wines, often from ungrafted vines.'),
   [('Sables de Camargue', None)]),
  ('flint', ('Silex', 'Flint'),
   ('Rognons de silice pris dans l’argile, issus de la craie : sols froids qui chauffent vite au soleil.', 'Silica nodules set in clay, left from chalk: cold soils that heat quickly in the sun.'),
   ('Sauvignons et Chenins tendus, aux notes « pierre à fusil ».', 'Taut Sauvignons and Chenins with “gunflint” notes.'),
   [('Pouilly-Fumé', PLAN + 'Loire_Centre/Pouilly-Fume.html'), ('Vouvray', PLAN + 'Loire_Anjou_Touraine/Vouvray.html')]),
  ('volcanic', ('Volcanique', 'Volcanic'),
   ('Basaltes et cendres des anciens volcans : sols sombres, riches en minéraux.', 'Basalt and ash from old volcanoes: dark soils rich in minerals.'),
   ('Vins vifs et épicés, comme les Gamay et Pinot noir des Côtes d’Auvergne.', 'Lively, spicy wines, such as the Gamay and Pinot Noir of Côtes d’Auvergne.'),
   [('Auvergne', '../../Auvergne_et_du_Haut_Val_de_Loire.html')]),
]


PHOTOS = {  # soil kind -> (image, alt, style) replacing the drawn swatch; 'block' = cut-out soil profile, 'photo' = full-bleed picture
    'galets': ('galets_chateauneuf', 'Galets roulés à Châteauneuf-du-Pape / Rounded pebbles at Châteauneuf-du-Pape', 'photo'),
    'limestone': ('soil_limestone', 'Profil de sol calcaire / Limestone soil profile', 'block'),
    'chalk': ('soil_chalk', 'Profil de sol crayeux / Chalk soil profile', 'block'),
    'marl': ('soil_marl', 'Profil de sol marneux / Marl soil profile', 'block'),
    'clay': ('soil_clay', 'Profil de sol argileux / Clay soil profile', 'block'),
    'gravel': ('soil_gravel', 'Profil de sol de graves / Gravel soil profile', 'block'),
    'granite': ('soil_granite', 'Profil de sol granitique / Granite soil profile', 'block'),
    'schist': ('soil_schist', 'Profil de sol schisteux / Schist soil profile', 'block'),
    'sand': ('soil_sand', 'Profil de sol sableux / Sandy soil profile', 'block'),
    'flint': ('soil_flint', 'Profil de sol à silex / Flint soil profile', 'block'),
    'volcanic': ('soil_volcanic', 'Profil de sol volcanique / Volcanic soil profile', 'block'),
}


def soil_cards():
    out = []
    for i, (kind, name, what, wine, ex) in enumerate(SOILS):
        links = ''.join(f'<a href="{h}">{n}</a>' if h else f'<span>{n}</span>' for n, h in ex)
        if kind in PHOTOS:
            f, alt, style = PHOTOS[kind]
            wh = 'width="600" height="400"' if style == 'photo' else 'width="352" height="440"'
            top = (f'<button type="button" class="zoom soil-{style}" data-full="{IMG}{f}.webp" aria-label="Agrandir / Enlarge">'
                   f'<img src="{IMG}{f}_s.webp" alt="{att(alt)}" loading="lazy" decoding="async" {wh}></button>')
        else:
            top = swatch(kind, i + 7)
        out.append(f'<article class="soil">{top}<div class="soil-b"><h3>{t(name)}</h3>{blk(what)}'
                   f'<p class="soil-w"><b>{t(("Dans le verre : ", "In the glass: "))}</b>{t(wine)}</p><div class="soil-ex">{links}</div></div></article>')
    return ''.join(out)


CLIMATES = [
  ('#4f7fae', ('Océanique', 'Oceanic'), ('Hivers doux, étés tempérés, pluies réparties sur l’année ; le risque, c’est l’humidité et les maladies.', 'Mild winters, moderate summers, rain spread through the year; the risk is damp and disease.'),
   ('Bordeaux, Pays nantais, Anjou, Cognac, Sud-Ouest atlantique', 'Bordeaux, Pays Nantais, Anjou, Cognac, Atlantic South-West')),
  ('#7a5aa0', ('Semi-continental', 'Semi-continental'), ('Hivers froids, étés chauds, gel de printemps fréquent ; grandes variations d’une année à l’autre.', 'Cold winters, warm summers, frequent spring frost; big swings from one year to the next.'),
   ('Bourgogne, Champagne, Alsace, Centre-Loire, Jura', 'Burgundy, Champagne, Alsace, Centre-Loire, Jura')),
  ('#c0703a', ('Méditerranéen', 'Mediterranean'), ('Étés chauds et secs, pluies d’automne parfois violentes, vents puissants (mistral, tramontane) qui assèchent et assainissent.', 'Hot, dry summers, sometimes violent autumn rain, strong winds (mistral, tramontane) that dry the vines and keep disease away.'),
   ('Languedoc, Roussillon, Provence, Rhône méridional, Corse', 'Languedoc, Roussillon, Provence, southern Rhône, Corsica')),
  ('#4f8a6a', ('Montagnard', 'Mountain'), ('L’altitude rafraîchit (environ −0,6 °C par 100 m) ; les vignes cherchent les pentes bien exposées et l’abri des lacs.', 'Altitude cools (about −0.6 °C per 100 m); vines seek well-exposed slopes and the shelter of lakes.'),
   ('Savoie, Bugey, piémont pyrénéen (Jurançon, Irouléguy)', 'Savoie, Bugey, Pyrenean foothills (Jurançon, Irouléguy)')),
]


def climate_cards():
    return ''.join(f'<div class="clim" style="--c:{c}"><h3>{t(n)}</h3>{blk(d)}<p class="clim-r">{t(r)}</p></div>' for c, n, d, r in CLIMATES)


MATCH = [  # site, grape, why
  (('Graves du Médoc', 'Médoc gravel'), 'Cabernet Sauvignon', ('cépage tardif, il profite de la chaleur et du drainage des graves', 'a late variety, it benefits from the warmth and drainage of gravel')),
  (('Argiles de Pomerol', 'Pomerol clay'), 'Merlot', ('précoce, il aime les sols frais qui ne manquent jamais d’eau', 'early-ripening, it likes cool soils that never run dry')),
  (('Calcaires et marnes de Bourgogne', 'Burgundy limestone and marl'), 'Pinot noir, Chardonnay', ('précoces et délicats, ils traduisent les moindres nuances du sol', 'early and delicate, they reflect the subtlest differences in soil')),
  (('Craie de Champagne', 'Champagne chalk'), 'Chardonnay, Pinot noir, Meunier', ('la fraîcheur du sol garde l’acidité indispensable aux effervescents', 'the cool soil keeps the acidity sparkling wine needs')),
  (('Granite du Beaujolais', 'Beaujolais granite'), 'Gamay', ('sols pauvres et acides qui tempèrent sa vigueur', 'poor, acidic soils that calm its vigour')),
  (('Granite de l’Hermitage', 'Hermitage granite'), 'Syrah', ('coteau très pentu exposé plein sud, au nord de sa limite de culture', 'a steep, south-facing slope near the northern limit of its range')),
  (('Galets de Châteauneuf-du-Pape', 'Châteauneuf-du-Pape cobbles'), 'Grenache', ('tardif et amoureux de la chaleur', 'late-ripening and heat-loving')),
  (('Calcaires et silex du Centre-Loire', 'Centre-Loire limestone and flint'), 'Sauvignon blanc', ('climat frais qui préserve ses arômes', 'a cool climate that keeps its aromas')),
  (('Schistes d’Anjou', 'Anjou schist'), 'Chenin', ('coteaux chauds au-dessus du Layon, propices aux liquoreux', 'warm slopes above the Layon, ideal for sweet wines')),
]


def match_table():
    return ''.join(f'<tr><td>{t(s)}</td><td class="g">{g}</td><td>{t(w)}</td></tr>' for s, g, w in MATCH)


PRO_DEF = [
  (('Définition officielle', 'Official definition'),
   ('Selon l’OIV (résolution OIV/VITI 333/2010), le terroir vitivinicole est « un concept qui se réfère à un espace sur lequel se développe un savoir collectif des interactions entre un milieu physique et biologique identifiable et les pratiques vitivinicoles appliquées, qui confèrent des caractéristiques distinctives aux produits originaires de cet espace ».',
    'According to the OIV (resolution OIV/VITI 333/2010), vitivinicultural terroir is “a concept which refers to an area in which collective knowledge of the interactions between the identifiable physical and biological environment and applied vitivinicultural practices develops, providing distinctive characteristics for the products originating from this area”.')),
  (('Ce qui pèse le plus', 'What matters most'),
   ('Les travaux de Gérard Seguin puis de Cornelis van Leeuwen à Bordeaux ont montré que le sol agit d’abord par le <b>régime hydrique</b> qu’il impose à la vigne : une contrainte en eau modérée, à partir de la véraison, arrête la croissance des rameaux et favorise la maturité, la couleur et les tanins. Dans leurs essais à Saint-Émilion, l’effet du climat de l’année et celui du sol dépassaient celui du cépage.',
    'Work by Gérard Seguin and later Cornelis van Leeuwen in Bordeaux showed that soil acts first through the <b>water regime</b> it imposes on the vine: moderate water stress from véraison stops shoot growth and favours ripeness, colour and tannin. In their Saint-Émilion trials, the effects of vintage weather and of soil outweighed the effect of grape variety.')),
  (('La « minéralité »', '“Minerality”'),
   ('Les racines absorbent des ions minéraux dissous, pas le goût des roches : il n’y a pas de transfert direct du sol au verre. Ce que l’on appelle minéralité est plutôt lié à l’acidité, à certains composés soufrés ou à l’absence de fruit exubérant ; le sujet reste débattu.',
    'Roots take up dissolved mineral ions, not the taste of rocks: there is no direct transfer from soil to glass. What is called minerality is more likely linked to acidity, certain sulphur compounds or the absence of exuberant fruit; the subject is still debated.')),
]

PRO_SOIL = [
  (('Réserve utile', 'Available water capacity'),
   ('La quantité d’eau qu’un sol peut stocker et céder à la vigne (en mm) dépend de sa profondeur, de sa texture et de sa teneur en cailloux : quelques dizaines de mm sur un sol caillouteux superficiel, plus de 200 mm sur des limons profonds.',
    'The amount of water a soil can store and release to the vine (in mm) depends on its depth, texture and stone content: a few tens of mm on a shallow stony soil, over 200 mm on deep silts.')),
  (('Calcaire actif et chlorose', 'Active lime and chlorosis'),
   ('Un sol riche en calcaire actif bloque l’absorption du fer : les feuilles jaunissent (chlorose). On choisit alors un porte-greffe tolérant (41 B, Fercal, 333 EM) plutôt qu’un porte-greffe sensible comme le Riparia ; l’indice de pouvoir chlorosant (IPC) guide ce choix (chapitre 4).',
    'Soil rich in active lime blocks iron uptake: the leaves turn yellow (chlorosis). Growers then choose a tolerant rootstock (41 B, Fercal, 333 EM) rather than a sensitive one such as Riparia; the chlorosis potential index (IPC) guides the choice (chapter 4).')),
  (('Couleur et chaleur', 'Colour and warmth'),
   ('Les sols sombres (schiste, basalte) et caillouteux se réchauffent vite et avancent la maturité ; les sols clairs (craie, calcaire blanc) renvoient la lumière vers les grappes ; les argiles humides restent froides au printemps.',
    'Dark (schist, basalt) and stony soils warm up fast and advance ripening; pale soils (chalk, white limestone) reflect light onto the bunches; damp clays stay cold in spring.')),
]

PRO_SITE = [
  (('Altitude', 'Altitude'),
   ('La température baisse d’environ 0,6 °C tous les 100 m. Avec le réchauffement, les parcelles plus hautes, autrefois trop fraîches, deviennent recherchées (Hautes-Côtes de Bourgogne, piémonts du Languedoc).',
    'Temperature drops by about 0.6 °C every 100 m. With warming, higher plots once too cool are now sought after (Hautes-Côtes in Burgundy, Languedoc foothills).')),
  (('Exposition et pente', 'Aspect and slope'),
   ('Plus le soleil frappe la pente à angle droit, plus elle reçoit d’énergie : un coteau exposé au sud ou au sud-est gagne nettement sur la plaine, surtout au printemps et à l’automne quand le soleil est bas. Au sud de la France, des expositions nord ou plus fraîches préservent l’acidité.',
    'The closer the sun strikes a slope at a right angle, the more energy it receives: a south- or south-east-facing slope clearly gains over flat land, especially in spring and autumn when the sun is low. In southern France, north-facing or cooler sites help keep acidity.')),
  (('Air froid', 'Cold air'),
   ('Par nuit claire, l’air refroidi au sol s’écoule comme de l’eau vers les points bas : les gelées de printemps frappent d’abord les bas de pente et les cuvettes, rarement le mi-coteau.',
    'On clear nights, air chilled at ground level flows like water to low points: spring frosts hit the foot of slopes and hollows first, rarely the mid-slope.')),
  (('Eau et forêts', 'Water and forests'),
   ('Fleuves, estuaires et lacs adoucissent les extrêmes et favorisent les brumes (la Gironde au Médoc, le Ciron à Sauternes) ; la forêt des Landes abrite le Médoc des vents de l’océan, celle des plateaux bourguignons protège la Côte.',
    'Rivers, estuaries and lakes soften extremes and encourage mists (the Gironde in the Médoc, the Ciron at Sauternes); the Landes forest shelters the Médoc from ocean winds, and the plateau forests protect the Côte in Burgundy.')),
]

PRO_COTE = [
  (('Géologie', 'Geology'),
   ('La Côte est l’escarpement d’une grande faille apparue il y a environ 35 millions d’années, quand la plaine de la Saône (le fossé bressan) s’est effondrée. Elle met à nu des calcaires et marnes déposés au Jurassique, il y a 150 à 175 millions d’années, dans une mer chaude. La Côte de Nuits repose surtout sur des calcaires du Jurassique moyen ; la Côte de Beaune montre davantage de marnes du Jurassique supérieur, favorables aux grands blancs (Corton-Charlemagne, Meursault).',
    'The Côte is the escarpment of a great fault formed some 35 million years ago, when the Saône plain (the Bresse graben) subsided. It exposes limestones and marls laid down in a warm Jurassic sea 150–175 million years ago. The Côte de Nuits sits mainly on Middle Jurassic limestones; the Côte de Beaune shows more Upper Jurassic marls, which suit great whites (Corton-Charlemagne, Meursault).')),
  (('Les chiffres', 'Figures'),
   ('Une bande d’environ 50 km de Dijon aux Maranges, large de quelques centaines de mètres seulement, entre environ 220 et 400 m d’altitude ; la plupart des grands crus se situent entre 250 et 330 m.',
    'A strip about 50 km long from Dijon to the Maranges, only a few hundred metres wide, between roughly 220 and 400 m in altitude; most grands crus lie between 250 and 330 m.')),
  (('La route', 'The road'),
   ('L’ancienne route nationale 74 (aujourd’hui D974) marque grossièrement la limite entre les appellations villages, à l’ouest, et les appellations régionales Bourgogne, à l’est, dans la plaine.',
    'The old N74 road (now the D974) roughly marks the boundary between village appellations to the west and regional Bourgogne appellations to the east, on the plain.')),
]

SOURCES = [
  ('OIV, résolution OIV/VITI 333/2010, définition du terroir vitivinicole.', 'OIV, resolution OIV/VITI 333/2010, definition of vitivinicultural terroir.'),
  ('Van Leeuwen C. et al., « Influence of climate, soil, and cultivar on terroir », <i>AJEV</i> 55, 2004 ; Seguin G., « Terroirs and pedology of wine growing », <i>Experientia</i>, 1986.', 'Van Leeuwen C. et al., “Influence of climate, soil, and cultivar on terroir”, <i>AJEV</i> 55, 2004; Seguin G., “Terroirs and pedology of wine growing”, <i>Experientia</i>, 1986.'),
  ('Wilson J. E., <i>Terroir: the role of geology, climate and culture in the making of French wines</i>, 1998.', 'Wilson J. E., <i>Terroir: the role of geology, climate and culture in the making of French wines</i>, 1998.'),
  ('UNESCO, « Les Climats du vignoble de Bourgogne », inscription au patrimoine mondial, 2015.', 'UNESCO, “The Climats, terroirs of Burgundy”, World Heritage listing, 2015.'),
  ('INAO, cahiers des charges des appellations citées.', 'INAO, specifications of the appellations mentioned.'),
]


def main():
    tpl = (HERE / 'terroir_template.html').read_text()
    cote_links = ''.join(f'<a href="{climat(v)}">{v}</a>' for v in
                         ['Gevrey-Chambertin', 'Morey-Saint-Denis', 'Chambolle-Musigny', 'Vougeot', 'Vosne-Romanée', 'Nuits-Saint-Georges',
                          'Aloxe-Corton', 'Beaune', 'Pommard', 'Volnay', 'Meursault', 'Puligny-Montrachet', 'Chassagne-Montrachet'])
    rep = {
        '@@BASE_CSS@@': base_css(),
        '@@PRO_ICON@@': PRO_ICON,
        '@@PLATE_COTE@@': plate(IMG + 'cote_dor_section.webp', 'Coupe de la Côte d’Or / Côte d’Or cross-section', 1600, 1090, 'wide'),
        '@@COTE_LINKS@@': cote_links,
        '@@CLIMAT_VOUGEOT@@': climat('Vougeot'),
        '@@HILLSIDE@@': hillside(),
        '@@SOILS@@': soil_cards(),
        '@@CLIMATES@@': climate_cards(),
        '@@MATCH@@': match_table(),
        '@@PRO_DEF@@': pro_panel(PRO_DEF),
        '@@PRO_COTE@@': pro_panel(PRO_COTE),
        '@@PRO_SITE@@': pro_panel(PRO_SITE),
        '@@PRO_SOIL@@': pro_panel(PRO_SOIL),
        '@@CHAPTERS@@': chapter_nav(3),
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
