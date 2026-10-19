"""Corrects the user's barrel-anatomy picture (2026-10-18, at the user's request) by splicing glyphs
taken from the picture itself, so the typeface stays the same:
  Bordeaux 228 L / Burgundy 225 L -> 225 / 228 (the two last digits are swapped)
  « Bildge » -> « Bilge », « BILDGE » -> « BILGE », « Emty » -> « Empty », « biding » -> « binding »
  « Chestnut, hazel or Willow Hoops » label moved down, its arrow now points at the wooden hoops at the base
  (it pointed at a steel hoop).
Usage: python3 fix_anatomy.py <original.webp|png> <out.webp>
"""
import sys
import numpy as np
from PIL import Image, ImageDraw

src, out = sys.argv[1], sys.argv[2]
a = np.asarray(Image.open(src).convert('RGB')).copy()
BG = np.median(a[1050:1100, 20:200].reshape(-1, 3), axis=0).astype(np.uint8)   # paper white


def shift(x0, x1, y0, y1, dx):
    """move columns x0..x1 (inclusive) by dx; the vacated strip becomes background"""
    blk = a[y0:y1, x0:x1 + 1].copy()
    a[y0:y1, x0:x1 + 1] = BG
    a[y0:y1, x0 + dx:x1 + 1 + dx] = blk


def ink_rows(x0, x1, y0, y1, thr=110):
    lum = a[y0:y1, x0:x1 + 1].mean(2)
    r = np.where((lum < thr).any(1))[0]
    return y0 + r[0], y0 + r[-1]


# 1. capacities: swap the third digit of « 228L » (Bordeaux) and « 225L » (Burgundy)
t1, _ = ink_rows(1052, 1061, 1226, 1254)
t2, _ = ink_rows(1052, 1061, 1255, 1282)
h = 20
d8 = a[t1:t1 + h, 1052:1062].copy()
d5 = a[t2:t2 + h, 1052:1062].copy()
a[t1:t1 + h, 1052:1062] = d5
a[t2:t2 + h, 1052:1062] = d8

# 2. « Bildge Hoop » -> « Bilge Hoop »: drop the d (x 76-88), close the gap
shift(89, 172, 346, 390, -13)
# 3. « BILDGE » -> « BILGE »: drop the D (x 91-105), close the gap, re-centre the word
y0, y1 = ink_rows(56, 134, 496, 523)
y0, y1 = y0 - 2, y1 + 3
shift(106, 134, y0, y1, -15)
shift(56, 120, y0, y1, 7)
# 4. « Emty » -> « Empty »: open a gap after the m, paste the p of « Capacity » (Bordeaux line)
ma = ink_rows(964, 975, 1180, 1200)[0]                     # top of m (x-height)
pa = ink_rows(1085, 1091, 1226, 1254)[0]                   # top of a, same line as the p
p = a[pa - 1:pa + 22, 1093:1102].copy()                    # p with its descender, 9 px wide
shift(977, 1100, 1180, 1208, 9)
a[ma - 1:ma + 22, 977:986] = np.minimum(a[ma - 1:ma + 22, 977:986], p)
# 5. « biding » -> « binding »: move « Wicker bi » left, paste a copy of the n before the d
n = a[1112:1150, 177:190].copy()
shift(66, 160, 1112, 1150, -12)
a[1112:1150, 147:160] = np.minimum(a[1112:1150, 147:160], n)

# 6. wooden-hoops label + arrow
lab = a[980:1046, 18:197].copy()
lab[:32, 157:] = BG                                      # first line: keep « hazel », drop the arrow's start
DY = 178
a[980:1046, 18:200] = BG                                   # old label + start of the old arrow
# old arrow: dark pixels in a band around the segment (182,1005)->(299,962), filled from below
mask = np.zeros(a.shape[:2], bool)
yy, xx = np.mgrid[940:1020, 170:310]
px, py, qx, qy = 182, 1005, 299, 962
t = np.clip(((xx - px) * (qx - px) + (yy - py) * (qy - py)) / ((qx - px) ** 2 + (qy - py) ** 2), 0, 1)
dist = np.hypot(xx - (px + t * (qx - px)), yy - (py + t * (qy - py)))
lum = a[940:1020, 170:310].mean(2)
sel = (xx < 280) & ((dist < 8.5) | ((dist < 11) & (lum < 200)))   # the arrow and its anti-aliased fringe, off the barrel
sel = sel | np.roll(sel, 1, 0) | np.roll(sel, -1, 0) | np.roll(sel, 1, 1) | np.roll(sel, -1, 1)
mask[940:1020, 170:310] = sel
for y in range(1019, 939, -1):
    for x in np.where(mask[y])[0]:
        k = 1
        while mask[y + k, x]:
            k += 1
        a[y, x] = a[y + k, x]
        mask[y, x] = False
# arrowhead over the barrel's edge (x 280-310): left of the edge -> paper, on the wood -> nearest wood to the right
for y in range(956, 978):
    edge = 284 + (y - 960) * 4 / 14
    for x in range(280, 311):
        sat = int(a[y, x].max()) - int(a[y, x].min())
        if np.hypot(x - 294, y - 965) > 14:
            continue
        if x < edge:
            a[y, x] = BG
        elif sat < 45 or (sat < 80 and a[y, x].mean() > 150 and x < 300):
            r = x + 1
            while r < 330 and int(a[y, r].max()) - int(a[y, r].min()) < 80:
                r += 1
            a[y, x] = a[y, r]
a[980 + DY:1046 + DY, 18:197] = np.minimum(a[980 + DY:1046 + DY, 18:197], lab)

img = Image.fromarray(a)
# new arrow, drawn 4x and scaled down (same weight as the picture's arrows)
S = 4
x0, y0, x1, y1 = 120, 1110, 360, 1200
ov = Image.new('L', ((x1 - x0) * S, (y1 - y0) * S), 0)
d = ImageDraw.Draw(ov)
tail, tip = (183, 1005 + DY), (333, 1141)
v = np.subtract(tip, tail)
u = v / np.hypot(*v)
nrm = np.array([-u[1], u[0]])
base = np.array(tip) - u * 15
P = lambda q: tuple(((np.array(q) - (x0, y0)) * S).tolist())
d.line([P(tail), P(base + u * 2)], fill=255, width=int(2.4 * S))
d.polygon([P(tip), P(base + nrm * 5.5), P(base - nrm * 5.5)], fill=255)
ov = ov.resize((x1 - x0, y1 - y0), Image.LANCZOS)
patch = img.crop((x0, y0, x1, y1))
patch.paste(Image.new('RGB', patch.size, (17, 17, 17)), (0, 0), ov)
img.paste(patch, (x0, y0))
img.save(out, 'WEBP', quality=90, method=6) if out.endswith('.webp') else img.save(out)
print('saved', out)
