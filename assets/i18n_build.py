#!/usr/bin/env python3
"""Build assets/i18n_maps.js (FR→EN layer for the region map pages) and wire it into the pages.

  python3 assets/i18n_build.py            # rebuild the JS and (re)insert the script tag + bilingual <title> in every page
  python3 assets/i18n_build.py --remove   # take it out of the pages again

Sources: assets/i18n_maps.src.js (engine) + assets/i18n_tech.json (phrase rules for yields/alcohol/decrees) + assets/i18n_maps_dict.json ({"D": {french: english}, "RIV": {river: english}}).
To fix or add a translation, edit the JSON (keys are the French text with whitespace collapsed) and rerun.
Cadastral plans (Plan Cadastraux/) and Alsace.html (own built-in translation) are not touched.
"""
import json, os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.dirname(HERE)
PAGES = sorted([p for p in glob.glob(os.path.join(SITE, '*.html')) if os.path.basename(p) not in ('index.html', 'Alsace.html')]
               + glob.glob(os.path.join(SITE, 'Bourgogne Regions', '*.html')))
MARK = re.compile(r'<!--fw-i18n:start-->.*?<!--fw-i18n:end-->\n?', re.S)

def build():
    d = json.load(open(os.path.join(HERE, 'i18n_maps_dict.json'), encoding='utf-8'))
    src = open(os.path.join(HERE, 'i18n_maps.src.js'), encoding='utf-8').read()
    tech = json.load(open(os.path.join(HERE, 'i18n_tech.json'), encoding='utf-8'))   # [[regex, replacement]] for yields / alcohol / decrees
    js = (src.replace('__DICT__', json.dumps(d['D'], ensure_ascii=False)).replace('__RIV__', json.dumps(d['RIV'], ensure_ascii=False))
             .replace('__TECH__', json.dumps(tech, ensure_ascii=False)))
    open(os.path.join(HERE, 'i18n_maps.js'), 'w', encoding='utf-8').write(js)
    print(f"i18n_maps.js: {len(d['D'])} entries, {len(js)//1024} KB")
    return d['D']

def wire(D, remove=False):
    for p in PAGES:
        s = open(p, encoding='utf-8').read(); s0 = s
        s = MARK.sub('', s)
        # bilingual <title> (nav.js only switches html[lang] on pages that carry data-fr/data-en)
        m = re.search(r'<title(?: data-fr="[^"]*" data-en="[^"]*")?>([^<]*)</title>', s)
        if m:
            fr = m.group(1); key = ' '.join(fr.replace('&amp;', '&').split())
            en = D.get(key)
            if remove or not en: tag = f'<title>{fr}</title>'
            else: tag = f'<title data-fr="{fr}" data-en="{en.replace("&", "&amp;")}">{fr}</title>'
            s = s[:m.start()] + tag + s[m.end():]
        if not remove:
            rel = os.path.relpath(os.path.join(HERE, 'i18n_maps.js'), os.path.dirname(p)).replace(os.sep, '/')
            tag = f'<!--fw-i18n:start--><script src="{rel}"></script><!--fw-i18n:end-->\n'
            k = s.rfind('</body>')
            if k < 0: k = s.rfind('</html>')
            s = s[:k] + tag + s[k:] if k >= 0 else s.rstrip('\n') + '\n' + tag
        if s != s0:
            open(p, 'w', encoding='utf-8').write(s); print('  ', os.path.relpath(p, SITE))

if __name__ == '__main__':
    rm = '--remove' in sys.argv
    D = build() if not rm else {}
    wire(D, rm)
