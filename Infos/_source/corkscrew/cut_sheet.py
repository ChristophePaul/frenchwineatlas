"""Cuts the user's corkscrew sheet (6 tools on white, labels underneath; 2026-10-18, stand-in until the user's
own photos) into Bottle_Sizes_img/corkscrew_<key>.webp with a transparent background.
Usage: python3 cut_sheet.py corkscrews_sheet_user.webp   (then rerun add_section.py)
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

KEYS = ['t', 'henshall', 'limonadier', 'ailes', 'bilame', 'screwpull']      # left to right
OUT = Path(__file__).resolve().parents[2] / 'Bottle_Sizes_img'

a = np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float)
a = a[:740]                                         # drop the printed labels
diff = (255 - a).max(2)
m = ndi.binary_closing(diff > 18, iterations=2)
lab, n = ndi.label(m)
sizes = ndi.sum(m, lab, range(1, n + 1))
comps = [i + 1 for i, s in enumerate(sizes) if s > 300]
comps.sort(key=lambda i: ndi.find_objects(lab == i)[0][1].start)
assert len(comps) == len(KEYS), len(comps)
for key, i in zip(KEYS, comps):
    region = ndi.binary_dilation(lab == i, iterations=3)
    alpha = np.clip((diff - 6) / 40, 0, 1) * region             # soft edges, white -> transparent
    al = np.maximum(alpha, 1e-3)[..., None]
    rgb = np.clip((a - (1 - al) * 255) / al, 0, 255)           # un-mix the white
    ys, xs = np.where(alpha > 0)
    y0, y1, x0, x1 = ys.min() - 4, ys.max() + 5, xs.min() - 4, xs.max() + 5
    rgba = np.dstack([rgb, alpha * 255])[y0:y1, x0:x1].astype(np.uint8)
    im = Image.fromarray(rgba)
    im.save(OUT / f'corkscrew_{key}.webp', 'WEBP', quality=88, method=6)
    print(key, im.size)
