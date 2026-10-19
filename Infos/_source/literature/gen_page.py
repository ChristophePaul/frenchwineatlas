"""Builds Infos/Literature/Wine_Quotes.html — « Le vin en citations » / "Wine in quotations".

First page of the « Littérature & jeux » section: a bilingual search engine over quotes_data.py.
Shared look = Vine & Vineyard base.css. Run:  python3 gen_page.py
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INFOS = HERE.parent.parent
sys.path.insert(0, str(INFOS / 'Vine_and_Vineyard' / '_source'))
from common import base_css  # noqa: E402
import quotes_data as D  # noqa: E402

OUT = INFOS / 'Literature' / 'Wine_Quotes.html'


def slug(s):
    import unicodedata
    s = unicodedata.normalize('NFD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def data_json():
    quotes, seen = [], {}
    for x in D.Q:
        base = slug(x['a_en'])
        seen[base] = seen.get(base, 0) + 1
        quotes.append({
            'id': f"{base}-{seen[base]}",
            'a': x['a'], 'ae': x['a_en'], 'l': x['life'], 'le': x['life_en'],
            'nf': '' if x['nat'][0] in x['w'][0] else x['nat'][0], 'ne': '' if x['nat'][1] in x['w'][1] else x['nat'][1], 'era': x['era'], 'lang': x['lang'], 'o': x['o'],
            'fr': x['fr'], 'en': x['en'], 'wf': x['w'][0], 'we': x['w'][1], 'y': x['y'],
            'th': x['th'], 'st': x['st'],
            'nof': x.get('n', ('', ''))[0], 'noe': x.get('n', ('', ''))[1],
        })
    meta = {'themes': D.THEMES, 'eras': D.ERAS, 'langs': D.LANGS, 'status': D.STATUS}
    return json.dumps({'q': quotes, 'm': meta}, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def main():
    tpl = (HERE / 'page_template.html').read_text()
    html = tpl.replace('@@BASE_CSS@@', base_css()).replace('@@DATA@@', data_json())
    assert '@@' not in html, html[html.index('@@'):html.index('@@') + 40]
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html)
    print(f'{OUT.relative_to(INFOS.parent)}: {len(html) // 1024} KB, {len(D.Q)} quotes')


if __name__ == '__main__':
    main()
