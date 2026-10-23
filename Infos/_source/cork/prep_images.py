"""Turns the user's cork pictures (Infos/Corks/*.png) into web images for the Bottle Sizes page.
White backgrounds -> transparent (soft edge); the 4-closures picture is split into 4 tiles.
Run:  python3 Infos/_source/cork/prep_images.py
"""
from pathlib import Path
from PIL import Image, ImageFilter
import numpy as np

SITE = Path(__file__).resolve().parents[3]
SRC = SITE / 'Infos' / 'Corks'
OUT = SITE / 'Infos' / 'Bottle_Sizes_img'


def cut_white(im, lo=232, hi=250, holes=False):
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    m = a.min(axis=2)
    alpha = np.clip((hi - m) / (hi - lo), 0, 1)
    # keep only background connected to the border as transparent: flood from edges
    from scipy import ndimage
    bg = m >= lo
    lab, _ = ndimage.label(bg)
    edge = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    outside = np.isin(lab, list(edge))
    outside = ndimage.binary_dilation(outside, iterations=2)
    if holes:  # white gaps inside the shape (sky between leaves) too
        outside = outside | bg
    al = np.where(outside, alpha, 1.0)
    rgba = np.dstack([a, al * 255]).astype(np.uint8)
    out = Image.fromarray(rgba)
    return out.crop(out.getbbox())


def save(im, name, w):
    im = im.copy()
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    im.save(OUT / name, 'WEBP', quality=82, method=6)
    print(name, im.size)


save(Image.open(SRC / 'Cork Bark Stacks in Sunlit Grove.png').convert('RGB'), 'cork_stacks.webp', 1400)
save(cut_white(Image.open(SRC / 'Harvested Cork Oak Tree.png'), holes=True), 'cork_tree.webp', 1100)
for src, name in [('Detailed Cork Oak Cross-Section Slice.png', 'cork_slice.webp'),
                  ('Weathered Cork Bark Slab Macro.png', 'cork_slab.webp'), ('Cork Bark and Wine Cork Cross-Section.png', 'cork_punched.webp')]:
    save(cut_white(Image.open(SRC / src)), name, 1100)
four = Image.open(SRC / 'Four Wine Closure Types Compared.png').convert('RGB')
col = np.asarray(four).min(axis=2).min(axis=0) < 225          # columns holding an object
runs, start = [], None
for x, v in enumerate(col):
    if v and start is None:
        start = x
    if not v and start is not None:
        runs.append((start, x)); start = None
if start is not None:
    runs.append((start, len(col)))
runs = sorted(sorted(runs, key=lambda r: r[1] - r[0])[-4:])    # the 4 widest runs, left to right
for (x0, x1), key in zip(runs, ['agglo', 'natural', 'screwcap', 'glass']):
    tile = four.crop((max(0, x0 - 12), 0, min(four.width, x1 + 12), four.height))
    save(cut_white(tile), f'closure_{key}.webp', 500)


# ---- the user's own cork photos (Infos/Corks/Mycorks, 2026-10-23): pale blue-grey backdrop -> transparent
def cut_backdrop(im, lo=4, hi=16):
    """Cork is warm (red > blue), the backdrop and its shadows are cool (blue >= red):
    keep the largest warm blob, fill the holes left by the printing, soften the edge."""
    from scipy import ndimage
    a = np.asarray(im.convert('RGB')).astype(np.float32)
    warm = a[:, :, 0] - a[:, :, 2]
    mask = warm > (lo + hi) / 2
    mask = ndimage.binary_opening(mask, iterations=2)
    lab, n = ndimage.label(mask)
    if n:
        sizes = ndimage.sum(mask, lab, range(1, n + 1))
        mask = lab == (1 + int(np.argmax(sizes)))
    mask = ndimage.binary_fill_holes(ndimage.binary_closing(mask, iterations=4))
    alpha = ndimage.gaussian_filter(mask.astype(np.float32), 1.0)
    rgba = np.dstack([a, alpha * 255]).astype(np.uint8)
    out = Image.fromarray(rgba)
    return out.crop(out.getbbox())


MINE = SRC / 'Mycorks'
# 2026-10-23 (2nd batch, user): white-background / already-transparent photos
if (MINE / 'Natural_Cork.png').exists():
    save(cut_white(Image.open(MINE / 'Natural_Cork.png')), 'mycork_natural.webp', 420)
if (MINE / 'Bouchon_Agglomere.png').exists():
    im = Image.open(MINE / 'Bouchon_Agglomere.png').convert('RGBA')
    save(im.crop(im.getbbox()), 'mycork_agglo.webp', 420)
# 1st batch (blue backdrop), kept for the Diam / Nomacorc cards if the files come back
for src, name in [('Agglomerate_Cork.png', 'mycork_micro.webp'), ('Norma_Corks High Quality.png', 'mycork_synth.webp')]:
    if (MINE / src).exists():
        save(cut_backdrop(Image.open(MINE / src)), name, 340)

def trim_reflection(im):
    """Drop the rows under the cork where only its floor reflection is left (mask much narrower than the body)."""
    a = np.asarray(im)[:, :, 3] > 128
    width = a.sum(axis=1)
    body = np.median(width[width > 0])
    rows = np.where(width > 0.8 * body)[0]
    return im.crop((0, 0, im.width, int(rows.max()) + 2))


# 3rd batch (user, 2026-10-23): studio shots on a dark backdrop (warm/cool cut) + white-background Nomacorc
for src, name in [('Bouchon_Colmate.jpg', 'mycork_colmate.webp'), ('Bouchon_Technique.jpg', 'mycork_1plus1.webp'),
                  ('Bouchon de Champagne.jpg', 'mycork_champagne.webp')]:
    if (MINE / src).exists():
        save(trim_reflection(cut_backdrop(Image.open(MINE / src), lo=16, hi=30)), name, 420)
if (MINE / 'Norma_Cork.png').exists():
    save(cut_white(Image.open(MINE / 'Norma_Cork.png')), 'mycork_synth.webp', 420)

# 4th batch (user, 2026-10-23): Diam card -> Synthetic_Cork.png (user's choice); crown cap on white with a soft shadow
if (MINE / 'Synthetic_Cork.png').exists():
    save(cut_white(Image.open(MINE / 'Synthetic_Cork.png')), 'mycork_micro.webp', 420)
if (MINE / 'Crown_Cap.jpg').exists():
    save(cut_white(Image.open(MINE / 'Crown_Cap.jpg'), lo=212, hi=244), 'mycork_crown.webp', 520)

