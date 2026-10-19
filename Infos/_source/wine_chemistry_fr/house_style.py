"""Gives the two « Chimie du vin » pages the site's house header (← Retour, eyebrow, serif title with an italic
second half, rule, tagline) and links chem_house.css (2026-10-19, user). Idempotent; rerun after apply.py.
Run from WEB Site/Infos: python3 _source/wine_chemistry_fr/house_style.py
"""
import html, re
from pathlib import Path

D = Path('wine_chemistry_html')
PAGES = {
    'wine_chemistry_web.html': (('Les composés au fil de la vinification', 'Compounds through winemaking'),
                                ('Chimie <em>du vin</em>', 'Wine <em>chemistry</em>')),
    'wine_compound_count_web.html': (('La science du vin', 'Wine science'),
                                     ('Combien de composés <em>dans une bouteille&nbsp;?</em>', 'How many compounds <em>in a bottle?</em>')),
}


def bi(tag, fr, en, cls):
    return f'<{tag} class="{cls}" data-fr="{html.escape(fr, quote=True)}" data-en="{html.escape(en, quote=True)}">{fr}</{tag}>'


for name, ((efr, een), (tfr, ten)) in PAGES.items():
    p = D / name
    s = p.read_text()
    m = re.search(r'<header class="site-header"><div class="wrap">(.*?)</div></header>', s, re.S)
    inner = m.group(1)
    tag = re.search(r'<p (?:class="tagline" )?data-en="[^"]*" data-fr="[^"]*">.*?</p>', inner, re.S).group(0)   # the existing tagline
    if 'class="tagline"' not in tag:
        tag = tag.replace('<p ', '<p class="tagline" ', 1)
    new = ('<div class="topbar"><a class="back" href="../../index.html" data-fr="← Retour" data-en="← Back">← Retour</a></div>'
           + bi('p', efr, een, 'eyebrow') + bi('h1', tfr, ten, 'title') + '<div class="rule"></div>' + tag)
    s = s[:m.start(1)] + new + s[m.end(1):]
    link = '<link rel="stylesheet" href="chem_house.css?v=1">'
    if link not in s:
        s = s.replace('</head>', link + '\n</head>', 1)
    p.write_text(s)
    print(name, 'ok')
