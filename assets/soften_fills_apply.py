#!/usr/bin/env python3
"""Soften the dark appellation colours on region maps so elevation curves stay readable (2026-10-14).

Every colour with relative luminance < 0.12 found in the page's MD "communeFill" block is blended
toward the cream base (#efe7d4) and replaced in the communeFill / fillLegend / regionalLegend /
aocColors blocks (map + sidebar legend stay matched). Not touched: denomFull (selection colour),
wine-colour dots, grand-cru parcel fills. The two Rhône pages use the hand-tuned values below.
Côte-d'Or + Saône-et-Loire: the hard-coded "Village" legend swatch #7a1020 is softened too.

Usage (from WEB Site/):  python3 assets/soften_fills_apply.py <page.html> [...]
Safe to rerun: softened colours are no longer dark, so nothing changes the second time.
"""
import re, sys

CREAM = (0xef, 0xe7, 0xd4)
BLOCKS = [r'"communeFill"\s*:\s*\{.*?\}', r'"fillLegend"\s*:\s*\[.*?\]',
          r'"regionalLegend"\s*:\s*\[.*?\]', r'"aocColors"\s*:\s*\{.*?\}']
# Rhône pages were tuned by eye first (blend share per colour)
RHONE_T = {
    'Rhone-septentrional.html': {'#8f1d2e': .45, '#7b1d33': .42, '#6d3b8f': .45, '#5a1730': .40, '#a3324a': .42},
    'Rhone-meridional.html':    {'#6d1a2f': .42, '#8f1d2e': .45, '#a3324a': .42, '#6d3b8f': .45},
}
SWATCH = ('lg-sw" style="background:#7a1020"', 'lg-sw" style="background:#a96668"')


def lum(h):
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def mix(h, t):
    rgb = [int(h[i:i + 2], 16) for i in (1, 3, 5)]
    return '#' + ''.join('%02x' % round(c + (k - c) * t) for c, k in zip(rgb, CREAM))


def soft(h):
    L = lum(h)
    if L >= 0.12:
        return None
    return mix(h, 0.42 if L > 0.05 else 0.40 + (0.05 - L) * 0.5)


def apply(path):
    s = open(path, encoding='utf-8').read()
    name = path.replace('\\', '/').split('/')[-1]
    m = re.search(BLOCKS[0], s)
    if not m:
        print('skip (no communeFill)', path); return
    if name in RHONE_T:
        mp = {c: mix(c, t) for c, t in RHONE_T[name].items()}
    else:
        mp = {c.lower(): soft(c) for c in set(re.findall(r'#[0-9a-fA-F]{6}', m.group(0))) if soft(c)}
    n = 0
    for b in BLOCKS if mp else []:
        mm = re.search(b, s)
        if not mm:
            continue
        n += sum(1 for x in re.findall(r'#[0-9a-fA-F]{6}', mm.group(0)) if x.lower() in mp)
        new = re.sub(r'#[0-9a-fA-F]{6}', lambda x: mp.get(x.group(0).lower(), x.group(0)), mm.group(0))
        s = s[:mm.start()] + new + s[mm.end():]
    if name in ('Cote-d_Or.html', 'Saone-et-Loire.html') and SWATCH[0] in s:
        s = s.replace(SWATCH[0], SWATCH[1]); n += 1
    open(path, 'w', encoding='utf-8').write(s)
    print('ok' if n else 'unchanged', path, n)


if __name__ == '__main__':
    for p in sys.argv[1:]:
        apply(p)
