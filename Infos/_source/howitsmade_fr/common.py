"""Shared helpers to make the « How it's made » pages bilingual (2026-10-19, user).
French is the default text; English stays available through the site's FR/EN switch (assets/nav.js swaps
[data-fr][data-en] and sets <html lang>). The step data drawn by each page's script gets a French twin
(S_FR, GLOSS_FR) and the render code picks the set that matches <html lang>, redrawing when it changes.
"""
import html
import json
import re


def A(s):
    return html.escape(s, quote=True)


def js(obj):
    """JSON is valid JS; keep non-ASCII characters readable."""
    return json.dumps(obj, ensure_ascii=False, indent=1)


def sub1(s, old, new, label):
    """replace exactly one occurrence (fails loudly if the page changed)"""
    n = s.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 match, found {n}')
    return s.replace(old, new)


def bilingual(s, old_open, en_inner, close, fr_inner, label):
    """old_open + en_inner + close  →  old_open with data-fr/data-en, French inside"""
    old = old_open + en_inner + close
    new_open = old_open[:-1] + f' data-fr="{A(fr_inner)}" data-en="{A(en_inner)}">'
    return sub1(s, old, new_open + fr_inner + close, label)


def details(s, cls, sum_fr, body_fr, label):
    """<details class="acc CLS"><summary>EN</summary> <div class="body">EN</div> → bilingual summary + body"""
    m = re.search(r'(<details class="acc ' + cls + r'"><summary)>(.*?)(</summary>\s*<div class="body")>(.*?)(</div>\s*</details>)', s, re.S)
    if not m:
        raise SystemExit(label + ': details block not found')
    sum_en, body_en = m.group(2), m.group(4)
    new = (m.group(1) + f' data-fr="{A(sum_fr)}" data-en="{A(sum_en)}">' + sum_fr + m.group(3)
           + f' data-fr="{A(body_fr)}" data-en="{A(body_en)}">' + body_fr + m.group(5))
    return s[:m.start()] + new + s[m.end():]


LANG_JS = r'''
/* ---------- LANGUAGE (2026-10-19): French by default, English via the site menu ---------- */
const isEN = () => document.documentElement.lang === 'en';
const SS = () => (isEN() ? S : S_FR);
const GG = () => (isEN() ? GLOSS : GLOSS_FR);
const UI = k => ({optional: isEN() ? 'optional' : 'facultatif'})[k];
'''

LANG_INIT = r'''
/* redraw the script-built parts when the site menu switches FR/EN (it also swaps the static text) */
new MutationObserver(() => { renderFlows(); renderGloss(); setTimeout(() => wireGloss(document), 0); })
  .observe(document.documentElement, {attributes: true, attributeFilter: ['lang']});
'''
