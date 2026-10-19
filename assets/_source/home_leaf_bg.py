"""Home page background trial (2026-10-18, user): the user's vine-leaf photo BEHIND the wall of AOC names.
The original wall (Web_Page_Background.png) is opaque, so the names are re-used as see-through layers made from
the letter mask already extracted for the cream theme (assets/page_bg_cream_wall.png alpha):
  assets/page_bg_leaf.webp         the photo, 1920 px, saturation x LEAF_SAT
  assets/page_bg_names_dark.png    rust-coloured letters (dark theme), alpha 0.8 x mask (x NAMES_GAIN)
  assets/page_bg_names_cream.png   brown letters (cream theme), alpha 0.24 x mask (x NAMES_GAIN)
Run from WEB Site: python3 assets/_source/home_leaf_bg.py   (also stamps the links in index.html with ?v=<time>)
"""
import numpy as np
from PIL import Image, ImageEnhance

LEAF_SAT = .7 * .7     # 2026-10-18 user: leaf colour intensity -30 %, applied twice
NAMES_GAIN = 1.2 ** 3     # 2026-10-18 user: AOC names intensity +20 %, applied three times

leaf = Image.open('assets/_source/vine_leaf_user_original.jpg').convert('RGB')
leaf.thumbnail((1920, 1920), Image.LANCZOS)
leaf = ImageEnhance.Color(leaf).enhance(LEAF_SAT)
leaf.save('assets/page_bg_leaf.webp', 'WEBP', quality=80, method=6)

mask = np.asarray(Image.open('assets/page_bg_cream_wall.png').convert('RGBA'))[..., 3].astype(float) / 255
for name, rgb, k in [('dark', (156, 52, 36), .8), ('cream', (104, 70, 38), .24)]:
    out = np.zeros(mask.shape + (4,), np.uint8)
    out[..., :3] = rgb
    out[..., 3] = np.clip(mask * k * NAMES_GAIN * 255, 0, 255)
    Image.fromarray(out).save(f'assets/page_bg_names_{name}.png', optimize=True)
# cache-busting: browsers keep the old picture when the file name does not change, so every run stamps
# the links in index.html (main CSS and the generated fw-theme-css) with a new ?v=
import re, time
from pathlib import Path
idx = Path('index.html')
v = time.strftime('%Y%m%d%H%M%S')
txt = re.sub(r'(assets/page_bg_(?:leaf\.webp|names_dark\.png|names_cream\.png))(\?v=\d+)?', rf'\1?v={v}', idx.read_text())
idx.write_text(txt)
print('done, links stamped ?v=' + v)
