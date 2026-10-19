#!/usr/bin/env python3
"""Build assets/i18n_plans.js (FR→EN layer for the cadastral plan pages) and wire it into the pages.

  python3 assets/i18n_plans_build.py            # rebuild the JS, (re)insert the script tag + bilingual <title> in every plan page
  python3 assets/i18n_plans_build.py --remove   # take it out of the pages again

Sources: assets/i18n_plans.src.js (engine) + assets/i18n_plans_dict.json:
  D     {french text node: english}            — sidebar, legends, popups, source credits…
  H     {french element textContent: english innerHTML} — AOC card rows (.row) and Burgundy intros (p.lede)
  P     [[regex, replacement]]                  — text assembled by the page scripts (counts, legend lines…)
  SUBS  [[french, english]]                     — pieces of the parcel hover line
plus assets/i18n_tech.json (yield / alcohol phrase rules shared with the region maps).
Keys are the French text with whitespace collapsed. To fix or add a translation, edit the JSON and rerun.
Rerun after rebuilding or adding any plan page (the plan build scripts rewrite the HTML).
"""
import json, os, re, sys, glob, html
HERE = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.dirname(HERE)
PAGES = sorted(glob.glob(os.path.join(SITE, 'Plan Cadastraux', '*', '*.html'))
               + glob.glob(os.path.join(SITE, 'Bourgogne Regions', 'Bourgogne climats', '*.html')))
MARK = re.compile(r'<!--fw-i18n:start-->.*?<!--fw-i18n:end-->\n?', re.S)

def build():
    d = json.load(open(os.path.join(HERE, 'i18n_plans_dict.json'), encoding='utf-8'))
    src = open(os.path.join(HERE, 'i18n_plans.src.js'), encoding='utf-8').read()
    tech = json.load(open(os.path.join(HERE, 'i18n_tech.json'), encoding='utf-8'))
    js = (src.replace('__DICT__', json.dumps(d['D'], ensure_ascii=False)).replace('__HTML__', json.dumps(d['H'], ensure_ascii=False))
             .replace('__PAT__', json.dumps(d['P'], ensure_ascii=False)).replace('__SUBS__', json.dumps(d['SUBS'], ensure_ascii=False))
             .replace('__TECH__', json.dumps(tech, ensure_ascii=False)))
    open(os.path.join(HERE, 'i18n_plans.js'), 'w', encoding='utf-8').write(js)
    print(f"i18n_plans.js: {len(d['D'])} strings, {len(d['H'])} blocks, {len(js)//1024} KB")
    return d

def title_en(fr, d):
    key = ' '.join(html.unescape(fr).split())
    if key in d['D']: return d['D'][key]
    for rx, rep in d['P']:
        if re.match(rx, key): return re.sub(rx, re.sub(r'\$(\d)', r'\\\1', rep), key)
    return None

def wire(d, remove=False):
    n = 0
    for p in PAGES:
        s = open(p, encoding='utf-8').read(); s0 = s
        s = MARK.sub('', s)
        # bilingual <title> (nav.js only switches html[lang] on pages that carry data-fr/data-en)
        m = re.search(r'<title(?: data-fr="[^"]*" data-en="[^"]*")?>([^<]*)</title>', s)
        if m:
            fr = m.group(1); en = None if remove else title_en(fr, d)
            tag = f'<title>{fr}</title>' if not en else f'<title data-fr="{fr}" data-en="{html.escape(en, quote=True)}">{fr}</title>'
            s = s[:m.start()] + tag + s[m.end():]
        if not remove:
            rel = os.path.relpath(os.path.join(HERE, 'i18n_plans.js'), os.path.dirname(p)).replace(os.sep, '/')
            rel = '/'.join(__import__('urllib.parse').parse.quote(x) for x in rel.split('/'))
            tag = f'<!--fw-i18n:start--><script src="{rel}"></script><!--fw-i18n:end-->\n'
            k = s.rfind('</body>')
            if k < 0: k = s.rfind('</html>')
            s = s[:k] + tag + s[k:] if k >= 0 else s.rstrip('\n') + '\n' + tag
        if s != s0:
            open(p, 'w', encoding='utf-8').write(s); n += 1
    print(f'{n} pages updated of {len(PAGES)}')

if __name__ == '__main__':
    rm = '--remove' in sys.argv
    d = build() if not rm else {'D': {}, 'P': []}
    wire(d, rm)
