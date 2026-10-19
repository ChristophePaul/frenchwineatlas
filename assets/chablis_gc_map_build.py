#!/usr/bin/env python3
"""Build the « Chablis Grand Cru » climats map: a copy of the Chablis 1er Cru climats map
(Bourgogne Regions/Bourgogne climats/Chablis — …) renamed Grand Cru and opening zoomed on the 7 grands crus.
Rerun after the Chablis climats map changes, then assets/i18n_plans_build.py, assets/theme_apply.py,
assets/nav_build.py and plan_links_apply.py.
"""
import os, glob, unicodedata
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(SITE, 'Bourgogne Regions', 'Bourgogne climats')
nfc = lambda s: unicodedata.normalize('NFC', s)
SRC = next(p for p in glob.glob(os.path.join(D, '*.html')) if nfc(os.path.basename(p)).startswith('Chablis — '))
DST = os.path.join(D, 'Chablis Grand Cru — Climats Grands Crus, relief 5 m & climats communaux · Carte.html')

s = open(SRC, encoding='utf-8').read()
REPL = [
    ('<title data-fr="Chablis — Les climats du 1ᵉʳ Cru · Carte interactive" data-en="Chablis — The 1ᵉʳ Cru climats · Interactive map">Chablis — Les climats du 1ᵉʳ Cru · Carte interactive</title>',
     '<title data-fr="Chablis Grand Cru — Les climats du Grand Cru · Carte interactive" data-en="Chablis Grand Cru — The Grand Cru climats · Interactive map">Chablis Grand Cru — Les climats du Grand Cru · Carte interactive</title>'),
    ('<h1>Chablis<span class="sub">Les climats du Premier Cru</span></h1>',
     '<h1>Chablis Grand Cru<span class="sub">Les climats du Grand Cru</span></h1>'),
    # the lede keeps its counter ids out: the page script only fills them when present
    (s[s.find('<p class="lede">'):s.find('</p>', s.find('<p class="lede">')) + 4],
     '<p class="lede">Les <b>7</b> climats classés en <b>Grand Cru</b> de Chablis — Blanchot, Bougros, Les Clos, Grenouilles, '
     'Preuses, Valmur et Vaudésir, avec La Moutonne à cheval sur Vaudésir et Preuses — d’un seul tenant sur la rive droite du Serein, '
     'face à la ville. La carte s’ouvre sur les grands crus&nbsp;; dézoomez pour les premiers crus voisins, le relief au <b>5&nbsp;m</b> '
     'et les climats communaux nommés.</p>'),
    ('<div class="t">Chablis 1ᵉʳ Cru</div>', '<div class="t">Chablis Grand Cru</div>'),
    ('<div class="d">Climats, grands crus &amp; relief au 5&nbsp;m</div>', '<div class="d">Les 7 climats &amp; relief au 5&nbsp;m</div>'),
    # opening view: the grands crus only (the 1er Cru map frames every climat and commune label)
    ("function refit(){map.invalidateSize();if(!all.getLayers().length)return;\n  var b=all.getBounds();",
     "function refit(){map.invalidateSize();if(!all.getLayers().length)return;\n  var b=LAYERS['grand_cru'].getBounds();\n  if(b.isValid()){map.fitBounds(b.pad(0.03));return;}\n  b=all.getBounds();"),
]
for old, new in REPL:
    assert old and old in s, old[:80]
    s = s.replace(old, new, 1)
open(DST, 'w', encoding='utf-8').write(s)
print('wrote', os.path.relpath(DST, SITE), round(len(s) / 1e6, 2), 'MB')
