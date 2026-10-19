"""French version of the barrel-anatomy picture (2026-10-18, user request): every English label is erased
and redrawn in French (Arial Narrow Bold, same cap height as the original lettering).
Pipeline (from this folder):
  python3 fix_anatomy.py barrel_anatomy_original.webp /tmp/en.png      # corrected English picture
  python3 make_fr.py /tmp/en.png ../../Barrel_Making/img/barrel_anatomy_fr.webp
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FONT = '/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf'
INK = (17, 17, 17)
S = 4                                            # supersampling

src, out = sys.argv[1], sys.argv[2]
img = Image.open(src).convert('RGB')
a = np.asarray(img).astype(int)
BG = tuple(int(v) for v in np.median(a[1050:1100, 20:200].reshape(-1, 3), axis=0))
lum, sat = a.mean(2), a.max(2) - a.min(2)

# (erase boxes may run past the old text to shorten an arrow's tail where the French text is longer)
# label: erase boxes, English reference ((x0, top, x1), text) = where it sat, French lines, alignment
#   align 'c' = centred on the old text, 'r' = right edge kept (arrow starts there), 'l' = left edge kept
L = [
    dict(erase=[(119, 56, 276, 83), (158, 85, 228, 116)], ref=((121, 58, 274), 'Head or Chime'),
         fr=['Cercle de tête'], align='c'),
    dict(erase=[(690, 53, 748, 83)], ref=((692, 55, 746), 'Croze'), fr=['Jable'], align='c'),
    dict(erase=[(797, 34, 860, 56)], ref=((799, 36, 858), 'Chime'), fr=['Chanfrein'], align='c'),
    dict(erase=[(973, 55, 1032, 82)], ref=((975, 57, 1030), 'Head'), fr=['Fond'], align='c'),
    dict(erase=[(56, 225, 196, 253)], ref=((58, 227, 194), 'Quarter Hoop'), fr=['Cercle de collet'], align='r'),
    dict(erase=[(51, 352, 192, 379)], ref=((53, 354, 157), 'Bilge Hoop'), fr=['Cercle de bouge'], align='r'),
    dict(erase=[(34, 501, 173, 556)], ref=((36, 503, 171), '(Widest part)'), fr=['BOUGE', '(le plus large)'], align='c'),
    dict(erase=[(967, 565, 1117, 619)], ref=((969, 567, 1115), '0.88m - 0.95m'), fr=['Hauteur', '0,88 m – 0,95 m'], align='c'),
    dict(erase=[(75, 607, 126, 634)], ref=((77, 609, 124), 'Bung'), fr=['Bonde'], align='r'),
    dict(erase=[(59, 699, 160, 727)], ref=((61, 701, 158), 'Bung Hole'), fr=['Trou de bonde'], align='r'),
    dict(erase=[(73, 798, 130, 820)], ref=((75, 800, 128), 'Stave'), fr=['Douelle'], align='r'),
    dict(erase=[(45, 883, 154, 905)], ref=((47, 885, 152), 'Stave Joint'), fr=['Joint de', 'douelles'], align='r', dy=-14),
    dict(erase=[(57, 1118, 202, 1145)], ref=((59, 1120, 200), 'Wicker binding'), fr=['Ligature en osier'], align='r'),
    dict(erase=[(24, 1162, 204, 1192), (24, 1192, 201, 1219)], ref=((26, 1164, 176), 'Chestnut, hazel'),
         fr=['Cercles en bois :', 'châtaignier, noisetier', 'ou saule'], align='l'),
    dict(erase=[(497, 1227, 701, 1250)], ref=((499, 1229, 699), 'Head  0.55m - 0.60m'), fr=['Fond  0,55 m – 0,60 m'], align='c', pad=8),
    dict(erase=[(499, 1273, 701, 1300)], ref=((501, 1275, 699), 'Bilge  0.70m - 0.72m'), fr=['Bouge  0,70 m – 0,72 m'], align='c', pad=8),
]


def ink_width(text, size):
    f = ImageFont.truetype(FONT, size * S)
    x0, _, x1, _ = f.getbbox(text)
    return (x1 - x0) / S


def size_for(text, width):
    lo, hi = 8.0, 60.0
    for _ in range(30):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if ink_width(text, mid) < width else (lo, mid)
    return lo


# sizes from the cap heights measured on the original (B of « Bung », H of « Head », E of « Empty »):
# labels and dimensions 19 px, weights block 14 px; Arial Narrow Bold cap height = 0.72 em
CAP = .72
SZ_LAB = SZ_DIM = 19 / CAP

draw = ImageDraw.Draw(img)


def write(lines, size, top, x_ref, align, pitch, underline=None):
    """lines of text, cap tops starting at `top`; x_ref = centre / right / left edge depending on align"""
    f = ImageFont.truetype(FONT, round(size * S))
    cap = -f.getbbox('H', anchor='ls')[1] / S
    widths = [ink_width(t, size) for t in lines]
    W = int(max(widths) + 20)
    H = int(pitch * (len(lines) - 1) + size * 1.6)
    if align == 'c':
        X0 = x_ref - W / 2
    elif align == 'r':
        X0 = max(x_ref, 8 + max(widths)) - W + 10      # keep the right edge, but never run off the left side
    else:
        X0 = x_ref - 10
    X0, Y0 = int(X0), int(top - size * .35)
    m = Image.new('L', (W * S, H * S), 0)
    d = ImageDraw.Draw(m)
    for i, (t, w) in enumerate(zip(lines, widths)):
        bx = {'c': (W - w) / 2, 'r': W - 10 - w, 'l': 10}[align]
        x_off = f.getbbox(t)[0] / S
        base = top - Y0 + cap + i * pitch
        d.text(((bx - x_off) * S, base * S), t, font=f, fill=255, anchor='ls')
        if underline and underline[i]:
            uw = ink_width(underline[i], size)
            d.line([(bx * S, (base + 3) * S), ((bx + uw) * S, (base + 3) * S)], fill=200, width=int(1.6 * S))
    m = m.resize((W, H), Image.LANCZOS)
    img.paste(Image.new('RGB', (W, H), INK), (X0, Y0), m)
    return X0, X0 + W


for d in L:
    (rx0, rtop, rx1), _ = d['ref']
    size = SZ_DIM if d in L[14:] else SZ_LAB
    if d in L[14:]:
        # dimension lines sit in a white gap of the arrow line: widen the gap to the French text
        w = ink_width(d['fr'][0], size) + 2 * d['pad']
        cx = (rx0 + rx1) / 2
        x0, y0, x1, y1 = d['erase'][0]
        draw.rectangle((min(x0, cx - w / 2), y0, max(x1, cx + w / 2), y1), fill=BG)
    else:
        for box in d['erase']:
            draw.rectangle(box, fill=BG)
    x_ref = {'c': (rx0 + rx1) / 2, 'r': rx1, 'l': rx0}[d['align']]
    write(d['fr'], size, rtop + d.get('dy', 0), x_ref, d['align'], pitch=28)

# weights & capacities block (smaller text), underlined region names as in the original
draw.rectangle((950, 1184, 1142, 1281), fill=BG)
sz_w = 14 / CAP
write(['Poids à vide : 45 kg', 'Poids plein : 270-273 kg', 'Bordeaux : 225 L', 'Bourgogne : 228 L'],
      sz_w, 1187, 954, 'l', pitch=24.5, underline=[None, None, 'Bordeaux', 'Bourgogne'])

img.save(out, 'WEBP', quality=90, method=6) if out.endswith('.webp') else img.save(out)
print('saved', out)
