# Print the lot number « L0001-01 » on the three imaginary labels, in each label's own small-text style.
import sys
from PIL import Image, ImageFont, ImageDraw, ImageFilter
SRC, OUT = sys.argv[1], sys.argv[2]          # folder of the pre-lot images, output folder
FS = '/System/Library/Fonts/Supplemental/'
TEXT = 'L0001-01'

def stamp(fn, font, cap, xscale, ink, anchor, x, y, blur=0.35):
    im = Image.open(f'{SRC}/{fn}').convert('RGB')
    k = 4                                              # supersample for clean anti-aliasing
    f = ImageFont.truetype(FS + font, 200)
    capb = f.getbbox('L')                               # cap height of the font at 200 px
    size = round(200 * cap * k / (capb[3] - capb[1]))
    f = ImageFont.truetype(FS + font, size)
    l, t, r, b = f.getbbox(TEXT)
    m = Image.new('L', (r - l + 8 * k, b - t + 8 * k), 0)
    ImageDraw.Draw(m).text((4 * k - l, 4 * k - t), TEXT, font=f, fill=255)
    w = round(m.width * xscale / k); h = round(m.height / k)
    m = m.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(blur))
    px = {'left': x - 4, 'right': x - w + 4, 'center': x - w // 2}[anchor]
    im.paste(Image.new('RGB', m.size, ink), (px, y - 4), m)
    im.save(f'{OUT}/{fn}', 'WEBP', quality=92)
    print(fn, 'x', px + 4, px + w - 4, 'y', y, y + cap)

# Blabla: left-aligned under « 14.5% Vol. », condensed serif like « 14.5% Vol. » / « 750 ml »
stamp('label_bordeaux_blabla.webp', 'Times New Roman.ttf', 17, 0.82, (62, 58, 49), 'left', 80, 1033)
# Coullenot: left-aligned under « 750 ml », narrow sans
stamp('label_bourgogne_coullenot.webp', 'Arial Narrow.ttf', 16, 1.0, (40, 40, 40), 'left', 106, 959)
# Bubulle: centre of the bottom strip, between « 12% Vol. » and « 750 ml », narrow sans
stamp('label_champagne_bubulle.webp', 'Arial Narrow.ttf', 20, 1.0, (42, 24, 0), 'center', 768, 964)
