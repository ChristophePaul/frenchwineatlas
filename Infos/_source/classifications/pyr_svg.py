# -*- coding: utf-8 -*-
"""Burgundy classification pyramid — one true triangle (inline SVG) cut into four bands.
Used by gen_page.py; pyr_patch.py swaps it into the live Crus_Classifications.html."""
import html

# (css class, fr, en, sub fr, sub en, share of production)
LEVELS = [('gc', 'Grands crus', 'Grands crus', '33 AOC', '33 AOCs', '1 %'),
          ('pc', 'Premiers crus', 'Premiers crus', '667 climats', '667 climats', '10 %'),
          ('vil', 'Appellations villages', 'Village appellations', '44 AOC', '44 AOCs', '37 %'),
          ('reg', 'Appellations régionales', 'Regional appellations', '7 AOC + dénominations', '7 AOCs + denominations', '52 %')]
# band limits as a fraction of the height (apex = 0): the small top band is given extra height so its label fits
CUTS = [0, .44, .63, .82, 1]
FILL = {'gc': ('#f3d98c', '#cfa04a'), 'pc': ('#c9933c', '#9c6a22'),
        'vil': ('#a3354a', '#7a1a2e'), 'reg': ('#621527', '#3f0a16')}
INK = {'gc': '#2b1a05', 'pc': '#fff', 'vil': '#fff', 'reg': '#fff'}

AX, TOP, BASE, HALF = 230, 14, 394, 222      # apex x, apex y, base y, half base width
GAP = 5                                      # white gap between bands
PX = 556                                     # right edge of the percentage column


def _t(fr, en):
    e = html.escape
    return f'<tspan data-fr="{e(fr)}" data-en="{e(en)}">{e(fr)}</tspan>'


def _hw(y):
    return HALF * (y - TOP) / (BASE - TOP)


def svg(caption_fr='Part de la production (BIVB)', caption_en='Share of production (BIVB)'):
    H = BASE - TOP
    g = ['<defs>'] + [f'<linearGradient id="pyr-{k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/>'
                      f'<stop offset="1" stop-color="{b}"/></linearGradient>' for k, (a, b) in FILL.items()] + ['</defs>']
    for i, (k, fr, en, sfr, sen, pct) in enumerate(LEVELS):
        y0 = TOP + CUTS[i] * H + (GAP / 2 if i else 0)
        y1 = TOP + CUTS[i + 1] * H - (GAP / 2 if i < 3 else 0)
        if i == 0:
            pts = f'{AX},{y0:.1f} {AX + _hw(y1):.1f},{y1:.1f} {AX - _hw(y1):.1f},{y1:.1f}'
            yl = y0 + (y1 - y0) * .74            # label low in the top band, where it is widest
        else:
            pts = (f'{AX - _hw(y0):.1f},{y0:.1f} {AX + _hw(y0):.1f},{y0:.1f} '
                   f'{AX + _hw(y1):.1f},{y1:.1f} {AX - _hw(y1):.1f},{y1:.1f}')
            yl = (y0 + y1) / 2
        g.append(f'<polygon class="band" points="{pts}" fill="url(#pyr-{k})"/>')
        g.append(f'<text class="nm{" top" if i == 0 else ""}" x="{AX}" y="{yl - 4:.1f}" fill="{INK[k]}">{_t(fr, en)}</text>')
        g.append(f'<text class="sb" x="{AX}" y="{yl + 17:.1f}" fill="{INK[k]}">{_t(sfr, sen)}</text>')
        xe = AX + _hw(yl) + 10
        g.append(f'<line class="ld" x1="{xe:.1f}" y1="{yl + 2:.1f}" x2="{PX - 52}" y2="{yl + 2:.1f}"/>')
        g.append(f'<text class="pc" x="{PX}" y="{yl + 9:.1f}">{pct}</text>')
    return ('<div class="pyr"><svg viewBox="0 0 560 404" role="img" aria-label="Pyramide des appellations de Bourgogne / '
            'Burgundy appellation pyramid">' + ''.join(g) + '</svg>'
            f'<p class="small"><span data-fr="{caption_fr}" data-en="{caption_en}">{caption_fr}</span></p></div>')


CSS = '''  /* burgundy pyramid: one SVG triangle, four bands (pyr_svg.py) */
  .pyr{padding:4px 0;}
  .pyr svg{display:block;width:100%;height:auto;overflow:visible;}
  .pyr .band{filter:drop-shadow(0 2px 3px rgba(40,10,15,.18));}
  .pyr text{text-anchor:middle;}
  .pyr .nm{font-family:var(--serif);font-weight:600;font-size:21px;}
  .pyr .nm.top{font-size:18px;}
  .pyr .sb{font-family:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Arial,sans-serif;font-size:15px;font-weight:500;opacity:.95;}
  .pyr .pc{text-anchor:end;font-family:var(--serif);font-size:25px;font-weight:600;fill:var(--gold);}
  .pyr .ld{stroke:var(--gold);stroke-width:1;stroke-dasharray:2 4;opacity:.6;}
  .pyr .small{text-align:center;margin-top:8px;}
  @media (max-width:620px){.pyr .nm{font-size:23px;} .pyr .nm.top{font-size:20px;} .pyr .sb{font-size:17px;} .pyr .pc{font-size:27px;}}
'''
