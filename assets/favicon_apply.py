#!/usr/bin/env python3
"""Add favicon <link> tags right after the theme.js <script> block on every page.
Idempotent (tags live between <!--fw-favicon:start/end--> markers).
Usage: python3 assets/favicon_apply.py [page.html ...]   (no args = whole site)
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# after theme_apply's end marker (theme_apply rewrites everything between its markers)
TAG = re.compile(r'<script src="((?:\.\./)*)assets/theme\.js"></script>(?:<!--fw-theme:end-->)?')
OLD = re.compile(r'\n?<!--fw-favicon:start-->.*?<!--fw-favicon:end-->', re.S)

def block(pre):
    return ('\n<!--fw-favicon:start-->'
            f'<link rel="icon" href="{pre}favicon.ico" sizes="48x48">'
            f'<link rel="icon" type="image/png" href="{pre}assets/favicon.png" sizes="192x192">'
            f'<link rel="apple-touch-icon" href="{pre}apple-touch-icon.png">'
            '<!--fw-favicon:end-->')

def apply(p):
    s = p.read_text(encoding='utf-8')
    s2 = OLD.sub('', s)
    m = TAG.search(s2)
    if not m:
        return 'no theme.js'
    s2 = s2[:m.end()] + block(m.group(1)) + s2[m.end():]
    if s2 != s:
        p.write_text(s2, encoding='utf-8')
        return 'updated'
    return 'unchanged'

pages = [Path(a) for a in sys.argv[1:]] or [
    p for p in ROOT.rglob('*.html')
    if '.git' not in p.parts and '_backups' not in p.parts]
stats = {}
for p in pages:
    r = apply(p)
    stats[r] = stats.get(r, 0) + 1
    if r == 'no theme.js':
        print('skipped:', p.relative_to(ROOT))
print(stats)
