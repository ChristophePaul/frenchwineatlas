#!/usr/bin/env python3
"""Add the licence names (Licence Ouverte 2.0 / ODbL) and a « Crédits » link to the source credits of the map pages.

Targets the source lines the map generators write:
  - <div class="src">Sources : INAO … · DGFiP / Etalab … · © contributeurs OpenStreetMap …</div>   (cadastral plans)
  - <div class="foot">Délimitation : <b>INAO</b> · … cadastre (Etalab) · Relief : <b>IGN …</b> …</div>  (Burgundy climats maps)
A <span class="fw-lic" data-fr data-en> is appended inside the element, so the existing text (and its entry in the
plans' FR→EN dictionary) is untouched; nav.js swaps the span's language like any other data-fr/data-en element.
Only the licences of the producers named in that line are listed; the link goes to Infos/Confidentialite.html#credits.

Idempotent: earlier spans are removed before adding. Rerun after rebuilding map pages:
    python3 assets/credits_apply.py            # whole site
    python3 assets/credits_apply.py <pages…>   # some pages
"""
import glob, html, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDITS_PAGE = 'Infos/Confidentialite.html'
LO = 'https://www.etalab.gouv.fr/licence-ouverte-open-licence/'
ODBL = 'https://opendatacommons.org/licenses/odbl/'

OLD = re.compile(r'(?:<br class="fw-lic-br">| )?<span class="fw-lic"[^>]*>.*?</span>(?=\s*</div>)', re.S)
BLOCK = re.compile(r'(<div class="(src|foot)">)(.*?)(\s*</div>)', re.S)


def a(href, text, ext=True):
    return '<a href="%s"%s>%s</a>' % (href, ' target="_blank" rel="noopener"' if ext else '', text)


def licence_span(text, credits_href, kind):
    text = text.rstrip()
    open_by = [n for n in ('INAO', 'DGFiP', 'IGN') if n in text or (n == 'DGFiP' and 'Etalab' in text)]
    osm = 'OpenStreetMap' in text
    if not open_by and not osm:
        return None
    parts = {'fr': [], 'en': []}
    if open_by:
        who = ', '.join(open_by)
        parts['fr'].append(a(LO, 'Licence Ouverte 2.0') + ' (' + who + ')')
        parts['en'].append(a(LO, 'Licence Ouverte 2.0') + ' (' + who + ')')
    if osm:
        parts['fr'].append(a(ODBL, 'ODbL') + ' (OpenStreetMap)')
        parts['en'].append(a(ODBL, 'ODbL') + ' (OpenStreetMap)')
    fr = 'Licences : ' + ' · '.join(parts['fr']) + ' · ' + a(credits_href, 'Crédits', False)
    en = 'Licences: ' + ' · '.join(parts['en']) + ' · ' + a(credits_href, 'Credits', False)
    if kind == 'src':
        # the « · » separator sits inside the span, so a rerun finds the generated text unchanged
        lead = ' '
        if not text.endswith('.'):
            fr, en = '· ' + fr, '· ' + en
    else:
        lead = '<br class="fw-lic-br">'
    return '%s<span class="fw-lic" data-fr="%s" data-en="%s">%s</span>' % (
        lead, html.escape(fr, quote=True), html.escape(en, quote=True), fr)


def apply(path):
    s = open(path, encoding='utf-8').read()
    s0 = s
    s = OLD.sub('', s)
    credits_href = os.path.relpath(os.path.join(ROOT, CREDITS_PAGE), os.path.dirname(path)).replace(os.sep, '/') + '#credits'

    def repl(m):
        head, kind, body, tail = m.groups()
        if kind == 'foot' and 'Délimitation' not in body:
            return m.group(0)
        if kind == 'src' and not re.search(r'Sources?\s*:', body):
            return m.group(0)
        span = licence_span(body, credits_href, kind)
        if not span:
            return m.group(0)
        return head + body.rstrip() + span + tail

    s = BLOCK.sub(repl, s)
    if s != s0:
        open(path, 'w', encoding='utf-8').write(s)
        return True
    return False


def main(args):
    if args:
        pages = args
    else:
        pages = [p for p in glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)
                 if '/_backups/' not in p and '/_source/' not in p]
    n = 0
    for p in pages:
        if apply(p):
            n += 1
    print('credits: %d page(s) updated' % n)


if __name__ == '__main__':
    main(sys.argv[1:])
