"""Shared helpers for the « La vigne & le vignoble » chapter pages.
base.css holds the styles common to every chapter (theme vars, header, panels, plates,
lightbox, pro fold-outs); each chapter template adds its own CSS after @@BASE_CSS@@.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent

PRO_ICON = ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" '
            'stroke-linejoin="round"><path d="M9 3h6M10 3v6L4.5 18.5A1.6 1.6 0 0 0 5.9 21h12.2a1.6 1.6 0 0 0 '
            '1.4-2.5L14 9V3"/><path d="M7.5 15h9"/></svg>')
ZOOM_ICON = ('<span class="zoom-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="1.6" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/>'
             '<path d="M15.5 15.5 21 21M10.5 7.5v6M7.5 10.5h6"/></svg></span>')


def base_css():
    return (HERE / 'base.css').read_text()


def att(s):
    return s.replace('&', '&amp;').replace('"', '&quot;')


def t(pair, tag='span', cls=''):
    """Short bilingual text: one element swapped by data-fr / data-en."""
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c} data-fr="{att(pair[0])}" data-en="{att(pair[1])}">{pair[0]}</{tag}>'


def blk(pair, tag='p', cls=''):
    """Long bilingual text: two elements, CSS shows the active language."""
    c = f'{cls} ' if cls else ''
    return f'<{tag} class="{c}L fr">{pair[0]}</{tag}><{tag} class="{c}L en">{pair[1]}</{tag}>'


def plate(src, alt, w=900, h=1140, cls=''):
    """A zoomable illustration on a paper card."""
    c = f' {cls}' if cls else ''
    return (f'<figure class="plate{c}"><button type="button" class="zoom" data-full="{src}" aria-label="Agrandir / Enlarge">'
            f'<img src="{src}" alt="{att(alt)}" loading="lazy" decoding="async" width="{w}" height="{h}">{ZOOM_ICON}</button></figure>')


def pro_panel(items, open_=False):
    rows = ''.join(f'<div class="pro-item"><dt>{t(lbl)}</dt><dd>{blk(txt, "div")}</dd></div>' for lbl, txt in items)
    return (f'<details class="pro"{" open" if open_ else ""}><summary>{PRO_ICON}{t(("Pour les professionnels", "For professionals"))}'
            f'<span class="chev" aria-hidden="true">›</span></summary><dl>{rows}</dl></details>')


CHAPTERS = [
    (1, 'La plante vigne', 'The vine plant', 'Vine_Plant.html'),
    (2, 'Le cycle de la vigne', 'The vine’s year', 'Vine_Cycle.html'),
    (3, 'Terroir & site', 'Terroir & site', 'Vine_Terroir.html'),
    (4, 'Plantation & vie du vignoble', 'Planting & the life of a vineyard', 'Vine_Planting.html'),
    (5, 'Taille & modes de conduite', 'Training & pruning', 'Vine_Pruning.html'),
    (6, 'Travaux en vert & du sol', 'Canopy & soil work', 'Vine_Canopy.html'),
    (7, 'Les ennemis de la vigne', 'Threats to the vine', 'Vine_Threats.html'),
    (8, 'Philosophies culturales', 'Farming philosophies', 'Vine_Farming.html'),
    (9, 'Les vendanges', 'Harvest', 'Vine_Harvest.html'),
    (10, 'Glossaire', 'Glossary', 'Vine_Glossary.html'),
]


def chapter_nav(current):
    """Strip listing the 10 chapters; built ones are links, the others marked « à venir »."""
    out = []
    for n, fr, en, href in CHAPTERS:
        inner = f'<span class="ch-n">{n:02d}</span>{t((fr, en), "span", "ch-t")}'
        if n == current:
            out.append(f'<span class="ch cur" aria-current="page">{inner}</span>')
        elif href:
            out.append(f'<a class="ch" href="{href}">{inner}</a>')
        else:
            out.append(f'<span class="ch soon">{inner}{t(("à venir", "coming soon"), "small")}</span>')
    head = t(('La vigne &amp; le vignoble · les chapitres', 'The vine &amp; the vineyard · chapters'), 'h3')
    return f'<nav class="chapters" aria-label="Chapitres">{head}<div class="ch-grid">{"".join(out)}</div></nav>'
