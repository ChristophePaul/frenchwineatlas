# -*- coding: utf-8 -*-
"""Swap the Burgundy pyramid (HTML + CSS) in the live Crus_Classifications.html for the SVG version from pyr_svg.py.
The live page carries theme_apply CSS that gen_page.py does not reproduce, hence a patch rather than a rebuild."""
import re
from pathlib import Path
from pyr_svg import svg, CSS
P = Path(__file__).resolve().parents[2] / 'Crus_Classifications.html'
s = P.read_text()
s, n1 = re.subn(r'<div class="pyr">.*?</p></div>', lambda m: svg(), s, count=1, flags=re.S)
s, n2 = re.subn(r'  /\* burgundy pyramid.*?\n(?=\n  /\* chips)', lambda m: CSS, s, count=1, flags=re.S)
s, n3 = re.subn(r'html\[data-theme="cream"\] \.pyr \.shape\{[^}]*\}\n?', '', s)
P.write_text(s)
print('pyramid', n1, 'css', n2, 'old cream rule removed', n3)
