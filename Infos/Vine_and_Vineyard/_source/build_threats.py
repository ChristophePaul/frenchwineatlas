#!/usr/bin/env python3
"""Build Infos/Vine_and_Vineyard/Vine_Threats.html (chapter 7) from threats_content.py.
Run:  python3 "WEB Site/Infos/Vine_and_Vineyard/_source/build_threats.py"
"""
from pathlib import Path
from common import att, t, blk, base_css, chapter_nav
from threats_content import FAMILIES, THREATS, OTHERS, CALENDAR, STAGES, TIMELINE, SOURCES

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / 'Vine_Threats.html'
IMG = 'img/threats/'
MONTHS = [('J', 'J'), ('F', 'F'), ('M', 'M'), ('A', 'A'), ('M', 'M'), ('J', 'J'),
          ('J', 'J'), ('A', 'A'), ('S', 'S'), ('O', 'O'), ('N', 'N'), ('D', 'D')]
MONTHS_LONG = [('janvier', 'January'), ('février', 'February'), ('mars', 'March'), ('avril', 'April'),
               ('mai', 'May'), ('juin', 'June'), ('juillet', 'July'), ('août', 'August'),
               ('septembre', 'September'), ('octobre', 'October'), ('novembre', 'November'), ('décembre', 'December')]


def chip(fam):
    fr, en, col = FAMILIES[fam]
    return f'<span class="chip" style="--c:{col}">{t((fr, en))}</span>'


def threat_card(i, th):
    fam = th['fam']
    col = FAMILIES[fam][2]
    side = 'rev' if i % 2 else ''
    ess = ''.join(f'<div class="ess"><h4>{t(lbl)}</h4>{blk(txt)}</div>' for lbl, txt in th['ess'])
    pro = ''.join(f'<div class="pro-item"><dt>{t(lbl)}</dt><dd>{blk(txt, "div")}</dd></div>' for lbl, txt in th['pro'])
    links = ''
    if th.get('links'):
        a = ''.join(f'<a href="{u}">{n}</a>' if u else f'<span>{n}</span>' for n, u in th['links'])
        links = (f'<div class="where"><h4>{t(("Où la trouver", "Where to find it"))}</h4>'
                 f'<div class="aoc-links">{a}</div>'
                 f'<p class="hint">{t(("Chaque nom ouvre le plan cadastral de l’appellation.", "Each name opens the appellation’s cadastral plan."))}</p></div>')
    return f'''
  <section class="threat {side}" id="{th['id']}" style="--c:{col}">
    <figure class="plate">
      <button type="button" class="zoom" data-full="{IMG}{th['img']}.webp" aria-label="Agrandir / Enlarge">
        <img src="{IMG}{th['img']}.webp" alt="{att(th['name'][1])}" loading="lazy" decoding="async" width="900" height="1140">
        <span class="zoom-ico" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="10.5" cy="10.5" r="6.5"/><path d="M15.5 15.5 21 21M10.5 7.5v6M7.5 10.5h6"/></svg></span>
      </button>
    </figure>
    <div class="body">
      <div class="kicker">{chip(fam)}<span class="num">{i + 1:02d}</span></div>
      <h2>{t(th['name'])}</h2>
      <p class="latin">{th['latin']}</p>
      {blk(th['lead'], 'p', 'lead')}
      <div class="ess-grid">{ess}</div>
      {links}
      <details class="pro">
        <summary><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M9 3h6M10 3v6L4.5 18.5A1.6 1.6 0 0 0 5.9 21h12.2a1.6 1.6 0 0 0 1.4-2.5L14 9V3"/><path d="M7.5 15h9"/></svg>{t(("Pour les professionnels", "For professionals"))}<span class="chev" aria-hidden="true">›</span></summary>
        <dl>{pro}</dl>
      </details>
    </div>
  </section>'''


def index_grid():
    out = []
    for i, th in enumerate(THREATS):
        col = FAMILIES[th['fam']][2]
        out.append(f'<a class="idx" href="#{th["id"]}" style="--c:{col}"><span class="idx-img">'
                   f'<img src="{IMG}{th["img"]}_s.webp" alt="" loading="lazy" decoding="async"></span>'
                   f'<span class="idx-n">{i + 1:02d}</span>{t(th["name"], "b")}'
                   f'<small>{t(FAMILIES[th["fam"]][:2])}</small></a>')
    return ''.join(out)


def calendar():
    head = '<div class="cal-row cal-head"><div class="cal-lbl"></div>' + ''.join(
        f'<div class="cal-m" title="{m[0]}">{t(MONTHS[k])}</div>' for k, m in enumerate(MONTHS_LONG)) + '</div>'
    stages = '<div class="cal-row cal-stages"><div class="cal-lbl">' + t(('Stade de la vigne', 'Vine stage')) + '</div>'
    for a, b, fr, en in STAGES:
        stages += f'<div class="stage" style="grid-column:{a + 2}/{b + 3}">{t((fr, en))}</div>'
    stages += '</div>'
    rows = ''
    for anchor, fam, name, vals in CALENDAR:
        col = FAMILIES[fam][2]
        lbl = f'<a href="#{anchor}">{t(name)}</a>' if anchor else t(name)
        cells = ''.join(f'<div class="cell v{v}"></div>' for v in vals)
        rows += f'<div class="cal-row" style="--c:{col}"><div class="cal-lbl"><i></i>{lbl}</div>{cells}</div>'
    return head + stages + rows


def others():
    out = []
    for fam, name, what, how in OTHERS:
        col = FAMILIES[fam][2]
        out.append(f'<article class="other" style="--c:{col}">{chip(fam)}<h3>{t(name)}</h3>{blk(what)}'
                   f'<p class="how"><b>{t(("Parades : ", "Defences: "))}</b>{t(how)}</p></article>')
    return ''.join(out)


def timeline():
    return ''.join(f'<li style="--c:{FAMILIES[f][2]}"><span class="yr">{y}</span>{t(txt, "span", "ev")}</li>'
                   for y, txt, f in TIMELINE)


def legend():
    used = ['oomycete', 'fungus', 'noble', 'wood', 'phyto', 'insect', 'weather']
    return ''.join(chip(f) for f in used)


def main():
    tpl = (HERE / 'threats_template.html').read_text()
    html = (tpl.replace('@@BASE_CSS@@', base_css())
               .replace('@@CHAPTERS@@', chapter_nav(7))
               .replace('@@INDEX@@', index_grid())
               .replace('@@LEGEND@@', legend())
               .replace('@@CALENDAR@@', calendar())
               .replace('@@THREATS@@', ''.join(threat_card(i, th) for i, th in enumerate(THREATS)))
               .replace('@@OTHERS@@', others())
               .replace('@@TIMELINE@@', timeline())
               .replace('@@SOURCES@@', ''.join(f'<li>{t(s)}</li>' for s in SOURCES)))
    assert '@@' not in html
    OUT.write_text(html)
    print(f'{OUT.name}: {len(html) // 1024} KB')


if __name__ == '__main__':
    main()
