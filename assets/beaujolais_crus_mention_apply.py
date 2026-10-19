#!/usr/bin/env python3
"""Beaujolais map: correct the « mention » line of the ten crus' fiches (2026-10-14).

They all said « Primeur » / « Nouveau » autorisée, which the crus' cahiers des charges do not allow
(chapitre Ier, II lists the only complementary mention):
  - Saint-Amour, Juliénas, Chénas, Moulin-à-Vent, Fleurie, Chiroubles, Morgon, Côte de Brouilly
    (CDC version 2, 2010): « cru du Beaujolais » may complete the name;
  - Brouilly (CDC homologué par arrêté du 20 février 2024): « pas de disposition particulière »;
  - Régnié: no CDC in the local library — the line is removed rather than guessed.
Usage (from WEB Site/): python3 assets/beaujolais_crus_mention_apply.py "Bourgogne Regions/Beaujolais.html"
"""
import json, sys

CRU = "Mention « cru du Beaujolais » possible ; ni « primeur » ni « nouveau »"
FIX = {n: CRU for n in ['Saint-Amour', 'Juliénas', 'Chénas', 'Moulin-à-Vent', 'Fleurie', 'Chiroubles', 'Morgon', 'Côte de Brouilly']}
FIX['Brouilly'] = "Pas de mention complémentaire ; ni « primeur » ni « nouveau »"
FIX['Régnié'] = None

for path in sys.argv[1:]:
    s = open(path, encoding='utf-8').read()
    i = s.find('window.MAPDATA'); j = s.find('{', i); md, end = json.JSONDecoder().raw_decode(s[j:])
    n = 0
    for name, txt in FIX.items():
        m = md['meta'].get(name)
        if m is None: continue
        if txt is None:
            if 'mention' in m: del m['mention']; n += 1
        elif m.get('mention') != txt:
            m['mention'] = txt; n += 1
    if not n:
        print('skip (already corrected)', path); continue
    s = s[:j] + json.dumps(md, ensure_ascii=False, separators=(',', ':')) + s[j + end:]
    open(path, 'w', encoding='utf-8').write(s)
    print('ok', path, n, 'fiches')
