"""Hand-drawn SVG diagrams for chapter 1 (bud, flower, bunch). Drawn for a cream paper card,
so colours are fixed (no theme switching). Labels are bilingual via data-fr / data-en."""
from common import att

INK = '#3b2a1e'
LINE = '#7a6650'


def lbl(x, y, pair, anchor='start', px=None, py=None, sx=None):
    """Label text, plus an optional leader line from (sx|x, y-4) to the point (px, py)."""
    line = ''
    if px is not None:
        x0 = sx if sx is not None else (x + 4 if anchor == 'end' else x - 4)
        line = f'<path d="M{x0} {y - 4} L{px} {py}" fill="none" stroke="{LINE}" stroke-width="1"/><circle cx="{px}" cy="{py}" r="2.4" fill="{INK}"/>'
    return (line + f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="16" fill="{INK}" '
            f'font-family="Iowan Old Style,Palatino,Georgia,serif" data-fr="{att(pair[0])}" data-en="{att(pair[1])}">{pair[0]}</text>')


def bud():
    s = ['<svg class="diagram" viewBox="0 0 680 444" role="img" aria-label="Coupe d’un bourgeon de vigne / Section of a grapevine bud">']
    # cane
    s.append('<rect x="70" y="330" width="540" height="46" rx="23" fill="#a77d52" stroke="#6b4f2a" stroke-width="1.5"/>')
    s.append(''.join(f'<path d="M{x} 338 q30 6 60 0" fill="none" stroke="#8a6440" stroke-width="1"/>' for x in range(95, 560, 75)))
    s.append(''.join(f'<path d="M{x} 366 q30 -5 60 0" fill="none" stroke="#8a6440" stroke-width="1"/>' for x in range(120, 560, 90)))
    # petiole scar
    s.append('<ellipse cx="470" cy="332" rx="20" ry="7" fill="#7d5a36" stroke="#5a3e22"/>')
    # prompt bud (lateral shoot)
    s.append('<path d="M150 332 C148 305 162 287 172 280 C182 287 196 305 194 332 Z" fill="#8bb34a" stroke="#4f6e22" stroke-width="1.2"/>')
    s.append('<path d="M172 282 C160 266 150 262 140 264 C146 274 158 280 172 282 Z" fill="#9cc25a" stroke="#4f6e22"/>')
    # scales, wool, buds
    s.append('<path d="M238 332 C226 240 292 128 340 96 C388 128 454 240 442 332 Z" fill="#8a5a2b" stroke="#5a3a1a" stroke-width="1.6"/>')
    s.append('<path d="M250 320 C246 250 298 150 340 116" fill="none" stroke="#6e4520" stroke-width="1.2"/><path d="M430 320 C434 250 382 150 340 116" fill="none" stroke="#6e4520" stroke-width="1.2"/>')
    s.append('<path d="M262 332 C255 250 300 165 340 135 C380 165 425 250 418 332 Z" fill="#efe3c6" stroke="#cdb98d"/>')
    s.append(''.join(f'<circle cx="{x}" cy="{y}" r="1.6" fill="#cdb98d"/>' for x, y in
                     [(285, 230), (300, 200), (318, 172), (392, 225), (380, 195), (365, 170), (276, 270), (404, 268), (296, 300), (388, 305), (340, 150)]))
    s.append('<path d="M266 332 C266 286 278 258 287 248 C298 260 308 290 306 332 Z" fill="#a9c76a" stroke="#5a7a2a" stroke-width="1.2"/>')
    s.append('<path d="M378 332 C378 292 388 270 395 262 C404 274 414 300 412 332 Z" fill="#b8d27e" stroke="#5a7a2a" stroke-width="1.2"/>')
    s.append('<path d="M300 332 C298 252 320 192 340 160 C360 192 382 252 380 332 Z" fill="#7aa23c" stroke="#3f5f1a" stroke-width="1.4"/>')
    s.append('<path d="M340 166 C330 186 326 200 328 214 M340 166 C350 186 354 200 352 214 M340 190 C334 204 334 220 340 232 M340 190 C346 204 346 220 340 232" fill="none" stroke="#c7df95" stroke-width="1.4"/>')
    s.append(''.join(f'<circle cx="{x}" cy="{y}" r="4.2" fill="#7d3f78" stroke="#4e2149" stroke-width=".8"/>' for x, y in
                     [(318, 262), (324, 252), (314, 272), (322, 280), (362, 262), (356, 252), (366, 272), (358, 280), (320, 300), (328, 292), (360, 300), (352, 292)]))
    # labels
    s.append(lbl(225, 150, ('Écailles protectrices', 'Protective scales'), 'end', 268, 196))
    s.append(lbl(225, 230, ('Bourgeon secondaire', 'Secondary bud'), 'end', 284, 290))
    s.append(lbl(30, 408, ('Bourgeon anticipé', 'Prompt bud'), 'start', 168, 318, sx=100))
    s.append(lbl(30, 428, ('(donnera un entre-cœur)', '(grows a lateral shoot)'), 'start'))
    s.append(lbl(470, 116, ('Bourre (duvet)', 'Bud wool'), 'start', 392, 205))
    s.append(lbl(470, 166, ('Bourgeon principal', 'Primary bud'), 'start', 350, 215))
    s.append(lbl(470, 216, ('Ébauches de grappes', 'Bunch primordia'), 'start', 364, 268))
    s.append(lbl(470, 266, ('Bourgeon tertiaire', 'Tertiary bud'), 'start', 400, 300))
    s.append(lbl(500, 318, ('Cicatrice du pétiole', 'Leaf scar'), 'start', 478, 330, sx=496))
    s.append(lbl(640, 408, ('Sarment (bois d’un an)', 'Cane (one-year-old wood)'), 'end'))
    s.append('</svg>')
    return ''.join(s)


def flower():
    s = ['<svg class="diagram" viewBox="0 0 680 360" role="img" aria-label="Fleur de vigne / Grapevine flower">']
    s.append('<path d="M340 340 L340 252" stroke="#6e8f34" stroke-width="7" stroke-linecap="round"/>')
    stam = [(258, 192), (292, 146), (388, 146), (422, 192), (352, 120)]
    for x, y in stam:
        s.append(f'<path d="M{340 + (x - 340) * .12} 242 Q{(x + 340) / 2 + (x - 340) * .1} {y + 60} {x} {y + 6}" fill="none" stroke="#b9cf72" stroke-width="3" stroke-linecap="round"/>')
    s.append('<ellipse cx="340" cy="248" rx="26" ry="9" fill="#86a845" stroke="#4f6e22"/>')
    s.append('<ellipse cx="340" cy="222" rx="21" ry="28" fill="#8fb24a" stroke="#4f6e22" stroke-width="1.4"/>')
    s.append('<path d="M330 222 Q340 206 350 222 Q340 238 330 222Z" fill="#a9c76a" stroke="#5a7a2a" stroke-width=".8"/>')
    s.append('<rect x="336" y="186" width="8" height="12" fill="#9cbc55" stroke="#4f6e22" stroke-width=".8"/>')
    s.append('<ellipse cx="340" cy="185" rx="11" ry="5" fill="#d6e48c" stroke="#7e9a32"/>')
    for x, y in stam:
        s.append(f'<ellipse cx="{x}" cy="{y}" rx="10" ry="7" fill="#e8c547" stroke="#a8831f" stroke-width="1.2"/>')
    # calyptra flying off
    s.append('<path d="M392 132 C410 118 426 108 446 104" fill="none" stroke="#9b8a6e" stroke-width="1.3" stroke-dasharray="4 4"/>')
    s.append('<g transform="rotate(-18 482 96)"><path d="M452 112 C450 72 514 72 512 112 L503 120 L493 112 L482 121 L471 112 L461 120 Z" fill="#9cc04f" stroke="#4f6e22" stroke-width="1.4"/>'
             '<path d="M466 90 C476 80 490 80 500 90" fill="none" stroke="#c7df95" stroke-width="1.4"/></g>')
    s.append(lbl(522, 66, ('Capuchon : pétales', 'Calyptra: fused'), 'start'))
    s.append(lbl(522, 88, ('soudés, qui tombent', 'petals, then shed'), 'start', 510, 100, sx=518))
    s.append(lbl(220, 130, ('Anthère (pollen)', 'Anther (pollen)'), 'end', 286, 146))
    s.append(lbl(220, 236, ('Filet de l’étamine', 'Stamen filament'), 'end', 286, 222))
    s.append(lbl(470, 182, ('Stigmate', 'Stigma'), 'start', 352, 185))
    s.append(lbl(470, 230, ('Ovaire (4 ovules)', 'Ovary (4 ovules)'), 'start', 360, 226))
    s.append(lbl(470, 300, ('Pédicelle', 'Pedicel'), 'start', 344, 300))
    s.append(lbl(220, 300, ('5 étamines', '5 stamens'), 'end'))
    s.append('</svg>')
    return ''.join(s)


def bunch():
    """The bunch drawn earlier in the conversation, scaled into a labelled diagram."""
    B = '''<defs><g id="bb"><circle r="22" fill="#2e1028"/><ellipse cx="-7" cy="-8" rx="5" ry="3" fill="#fff" opacity=".12"/></g>
<g id="bf"><circle r="22" fill="#4f1c47"/><circle r="22" fill="none" stroke="#2a0d24"/><ellipse cx="-7" cy="-9" rx="6" ry="3.5" fill="#c9b6d6" opacity=".45"/><circle cx="9" cy="10" r="9" fill="#3a1236" opacity=".6"/></g>
<g id="bw"><circle r="19" fill="#5a2252"/><circle r="19" fill="none" stroke="#2a0d24"/><ellipse cx="-6" cy="-8" rx="5" ry="3" fill="#c9b6d6" opacity=".45"/></g></defs>
<g transform="translate(90 20) scale(.8)">
<path d="M372 40 C368 80 352 115 345 152" fill="none" stroke="#6b4f2a" stroke-width="8" stroke-linecap="round"/>
<path d="M366 85 C395 80 410 60 400 48 C392 40 382 52 392 58 C398 62 404 54 400 50" fill="none" stroke="#7a9a3a" stroke-width="2.5" stroke-linecap="round"/>
<path d="M380 95 C400 60 430 40 455 45 C450 25 475 15 490 30 C505 10 535 20 530 45 C560 45 575 70 555 90 C580 105 570 135 545 130 C550 160 520 170 505 150 C495 170 465 170 465 145 C440 150 420 135 430 115 C405 115 385 105 380 95 Z" fill="#5f8a3a" stroke="#3f6324" stroke-width="1.5"/>
<path d="M382 95 L490 32 M382 95 L548 88 M382 95 L505 148 M382 95 L432 115 M382 95 L455 48 M455 70 L470 50 M480 92 L520 60 M470 110 L500 130" fill="none" stroke="#3f6324" stroke-width="1.5" stroke-linecap="round"/>
<path d="M340 150 C300 170 250 190 222 228" fill="none" stroke="#6b4f2a" stroke-width="4" stroke-linecap="round"/>'''
    back = [(283, 162), (325, 158), (367, 160), (409, 166), (244, 200), (450, 204), (242, 262), (446, 262), (306, 296), (390, 296), (306, 360), (388, 362), (346, 424)]
    front = [(262, 182), (304, 180), (346, 178), (388, 180), (430, 184), (283, 216), (325, 214), (367, 214), (409, 218), (262, 248), (304, 248), (346, 248), (388, 248), (426, 250),
             (285, 282), (327, 280), (369, 280), (408, 284), (303, 314), (345, 312), (387, 316), (287, 346), (326, 344), (366, 346), (402, 348), (310, 378), (350, 378), (386, 382),
             (328, 410), (366, 410), (347, 442)]
    wing = [(215, 240), (196, 270), (232, 272), (214, 302)]
    B += ''.join(f'<use href="#bw" x="{x}" y="{y}"/>' for x, y in wing)
    B += ''.join(f'<use href="#bb" x="{x}" y="{y}"/>' for x, y in back)
    B += ''.join(f'<use href="#bf" x="{x}" y="{y}"/>' for x, y in front)
    B += '</g>'
    s = ['<svg class="diagram" viewBox="0 0 680 420" role="img" aria-label="Grappe de raisin / Grape bunch">', B]
    s.append(lbl(225, 34, ('Vrille', 'Tendril'), 'end', 402, 60))
    s.append(lbl(225, 80, ('Pédoncule', 'Peduncle'), 'end', 383, 82))
    s.append(lbl(225, 142, ('Rafle (rachis)', 'Stalk (rachis)'), 'end', 318, 160))
    s.append(lbl(170, 226, ('Aile ou épaule', 'Wing (shoulder)'), 'end', 240, 232))
    s.append(lbl(470, 384, ('Baies', 'Berries'), 'start', 390, 372))
    s.append(lbl(572, 118, ('Feuille', 'Leaf'), 'start', 540, 104))
    s.append('</svg>')
    return ''.join(s)
