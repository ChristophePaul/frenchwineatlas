"""Draws assets/sundial.svg — the « Histoire du vin » home-card watermark: a simple horizontal sundial
(hour lines computed for the latitude of Beaune, 47° N), Roman numerals, gnomon and its shadow on IV.
Simplified 2026-10-15 at the user's request (no motto, no vine, no quarter-hour ticks).
Run: python3 assets/_source/sundial_svg.py"""
import math, os
G = '#d9b36b'
cx, cy = 200, 196
lat = math.radians(47)
def ang(h): return math.atan(math.sin(lat) * math.tan(math.radians(15 * h)))
def pt(r, a): return (cx + r * math.sin(a), cy - r * math.cos(a))
o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 210"><g fill="none" stroke="{G}" stroke-linecap="round" stroke-linejoin="round">']
a = pt(180, -math.pi / 2); b = pt(180, math.pi / 2)
o.append(f'<path d="M{a[0]:.1f} {a[1]:.1f}A180 180 0 0 1 {b[0]:.1f} {b[1]:.1f}Z" stroke-width="3"/>')
for h in range(-6, 7):                       # hour lines, from the gnomon foot to the numerals
    a = ang(h); p1 = pt(24, a); p2 = pt(140, a)
    o.append(f'<path d="M{p1[0]:.1f} {p1[1]:.1f}L{p2[0]:.1f} {p2[1]:.1f}" stroke-width="1.3"/>')
o.append('</g>')
a = ang(4); s2 = pt(132, a - 0.02); s3 = pt(132, a + 0.05)    # shadow on IV
o.append(f'<path d="M{cx} {cy}L{s2[0]:.1f} {s2[1]:.1f}L{s3[0]:.1f} {s3[1]:.1f}Z" fill="{G}" fill-opacity=".4"/>')
o.append(f'<path d="M{cx} {cy}V{cy-120}L{cx+46} {cy}Z" fill="{G}" fill-opacity=".22" stroke="{G}" stroke-width="2.2" stroke-linejoin="round"/>')
R = ['VI', 'VII', 'VIII', 'IX', 'X', 'XI', 'XII', 'I', 'II', 'III', 'IV', 'V', 'VI']
for i, h in enumerate(range(-6, 7)):
    a = ang(h); x, y = pt(160, a)
    if abs(h) == 6: y -= 13
    o.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" dominant-baseline="middle" font-family="Georgia,serif" font-size="{17 if h == 0 else 14}" fill="{G}">{R[i]}</text>')
o.append('</svg>')
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'sundial.svg')
open(out, 'w').write(''.join(o)); print(out)
