#!/usr/bin/env python3
"""Build Infos/Vine_and_Vineyard/Vine_Glossary.html (chapter 10 — FR ↔ EN glossary).
Run:  python3 "WEB Site/Infos/Vine_and_Vineyard/_source/build_glossary.py"
Terms live in glossary_data.py; the page renders and filters them in the browser.
"""
import json
from common import HERE, base_css, chapter_nav
from glossary_data import TERMS, CATS

OUT = HERE.parent / 'Vine_Glossary.html'


def main():
    keys = set()
    for fr, en, cat, href, dfr, den in TERMS:
        assert cat in CATS, cat
        assert fr.lower() not in keys, f'duplicate: {fr}'
        keys.add(fr.lower())
    data = [{'fr': fr, 'en': en, 'c': cat, 'h': href, 'dfr': dfr, 'den': den} for fr, en, cat, href, dfr, den in TERMS]
    cats = {k: {'fr': v[0], 'en': v[1], 'col': v[2], 'n': v[3]} for k, v in CATS.items()}
    tpl = (HERE / 'glossary_template.html').read_text()
    html = (tpl.replace('@@BASE_CSS@@', base_css())
               .replace('@@CHAPTERS@@', chapter_nav(10))
               .replace('@@COUNT@@', str(len(TERMS)))
               .replace('@@DATA@@', json.dumps(data, ensure_ascii=False))
               .replace('@@CATS@@', json.dumps(cats, ensure_ascii=False)))
    assert '@@' not in html
    OUT.write_text(html)
    print(f'{OUT.name}: {len(html) // 1024} KB, {len(TERMS)} terms')


if __name__ == '__main__':
    main()
