# -*- coding: utf-8 -*-
"""Removes the old « ↗ other map » chips (.side-link) from the top of the region maps' sidebars: the site menu
(top-right, assets/nav.js) replaces them and they squeezed the AOC list. Idempotent; the .side-link CSS is left
(harmless). Rerun after rebuilding any region map. Usage: python3 assets/side_links_remove.py"""
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
n = 0
for f in sorted(ROOT.glob('*.html')):
    s = f.read_text()
    t = re.sub(r'\n?[ \t]*<a class="side-link"[^>]*>.*?</a>', '', s, flags=re.S)
    t = re.sub(r'\n?[ \t]*<span class="side-link side-link-active">.*?</span>', '', t, flags=re.S)
    if t != s:
        f.write_text(t); n += 1
        print('cleaned', f.name)
print(n, 'pages')
