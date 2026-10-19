"""Watermark for « Anatomie d'un décret AOC » (2026-10-18, user trial): the user's black-and-white photo of a foggy
winter vineyard turned into see-through ink layers — the darker the photo, the more opaque the ink; the fog disappears.
  img/wm_vineyard_dark.webp   faint gold ink, for the burgundy (dark) theme (near-black was invisible)
  img/wm_vineyard_cream.webp  warm brown ink, for the cream theme
Strength: K_DARK / K_CREAM. Run from AOC_Decree/: python3 _wm_src/make_watermark.py   (then bump ?v= in decree_watermark.css link)
"""
import numpy as np
from PIL import Image

K_DARK, K_CREAM = .42, .22
src = Image.open('_wm_src/vineyard_fog_user_original.jpg').convert('L')
src.thumbnail((1920, 1920), Image.LANCZOS)
lum = np.asarray(src).astype(float) / 255
ink = np.clip((0.86 - lum) / 0.72, 0, 1) ** 1.1          # fog ≈ 0, vine stocks ≈ 1
for name, rgb, k in [('dark', (217, 179, 107), K_DARK), ('cream', (92, 58, 30), K_CREAM)]:
    out = np.zeros(lum.shape + (4,), np.uint8)
    out[..., :3] = rgb
    out[..., 3] = np.clip(ink * k * 255, 0, 255)
    Image.fromarray(out).save(f'img/wm_vineyard_{name}.webp', 'WEBP', quality=82, method=6)
print('done')
