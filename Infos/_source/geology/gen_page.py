"""Builds « La géologie des vignobles » / "The geology of the vineyards" — Infos/Geology/Geology_Map.html.
Map data (geology_data.js) comes from GeoJson Files/Geology/build_geology.py; texts from content.py.
Run:  python3 gen_page.py   then   python3 ../../../assets/theme_apply.py Infos/Geology/Geology_Map.html  (from WEB Site)
"""
import json
import sys
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
INFOS = HERE.parent.parent
OUT = INFOS / 'Geology' / 'Geology_Map.html'
sys.path.insert(0, str(INFOS / 'Vine_and_Vineyard' / '_source'))
from common import base_css, att  # noqa: E402
import content as C  # noqa: E402

GAMES = HERE.parent / 'games'
PAGES = {  # same keys as build_geology.py
    'champagne': 'Champagne.html', 'lorraine': 'Lorraine.html', 'alsace': 'Alsace.html',
    'chablis': 'Bourgogne Regions/Chablis_et_de_l_Auxerrois.html', 'cotedor': 'Bourgogne Regions/Cote-d_Or.html',
    'saoneloire': 'Bourgogne Regions/Saone-et-Loire.html', 'beaujolais': 'Bourgogne Regions/Beaujolais.html',
    'jura': 'Jura.html', 'savoie': 'Savoie_et_du_Bugey.html', 'rhonen': 'Rhone-septentrional.html',
    'rhones': 'Rhone-meridional.html', 'provence': 'Provence-Cote-d-Azur.html', 'corse': 'Corse.html',
    'languedoc': 'Languedoc.html', 'limoux': 'Malepere-et-Limoux.html', 'roussillon': 'Roussillon.html',
    'swtoulouse': 'South-West Toulouse.html', 'pyrenees': 'Landes_et_Pyrenees_Occidentales.html',
    'swbergerac': 'South West Bergerac.html', 'bordeaux': 'Bordeaux.html', 'cognac': 'Cognac.html',
    'nantais': 'Pays_Nantais.html', 'anjou': 'Anjou_et_de_Touraine.html', 'centre': 'Centre-Loire.html',
    'auvergne': 'Auvergne_et_du_Haut_Val_de_Loire.html',
}


def bi(pair, tag='span', cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c} data-fr="{att(pair[0])}" data-en="{att(pair[1])}">{pair[0]}</{tag}>'


def families():
    out = []
    for f in C.FAMILIES:
        out.append(f'<article class="panel fam" style="--c:{f["color"]}">'
                   f'{bi(f["name"], "h3")}{bi(f["age"], "div", "age")}{bi(f["what"], "p")}{bi(f["wine"], "p", "w")}'
                   f'<div class="ex"><b data-fr="Exemples :" data-en="Examples:">Exemples :</b> {bi(f["ex"])}</div>'
                   f'<button type="button" class="show" data-fam="{f["key"]}" data-fr="Voir sur la carte" data-en="Show on the map">Voir sur la carte</button></article>')
    q = C.QUATERNARY
    out.append(f'<article class="panel fam quat">{bi(q["name"], "h3")}{bi(q["age"], "div", "age")}{bi(q["text"], "p")}</article>')
    return ''.join(out)


EVENTS = [
    ('Une haute chaîne de montagnes, la chaîne hercynienne, traverse la France. Ses racines usées forment aujourd’hui le Massif armoricain, le Massif central, les Vosges et la Corse.',
     'A great mountain range, the Variscan chain, crosses France. Its worn-down roots now form the Armorican Massif, the Massif Central, the Vosges and Corsica.'),
    ('Des fleuves étalent des sables rouges, puis la mer revient : marnes du Jura et de Lorraine.',
     'Rivers spread red sands, then the sea returns: marls of the Jura and Lorraine.'),
    ('Mer tropicale peu profonde : naissance des calcaires de Bourgogne, Chablis et Sancerre.',
     'Shallow tropical sea: the limestones of Burgundy, Chablis and Sancerre are born.'),
    ('Mer de craie au nord (Champagne, Cognac, Touraine), calcaires blancs au sud.',
     'Chalk sea in the north (Champagne, Cognac, Touraine), white limestones in the south.'),
    ('Pyrénées et Alpes se dressent ; leurs débris remplissent les bassins. La Saône et le Rhin s’effondrent, des volcans s’allument en Auvergne.',
     'The Pyrenees and Alps rise; their debris fills the basins. The Saône and Rhine valleys sink, volcanoes flare up in Auvergne.'),
    ('Glaciations : les fleuves étalent graves et galets en terrasses.',
     'Ice ages: rivers spread gravel and pebbles in terraces.'),
]


def time_strip():
    col = {f['key']: f['color'] for f in C.FAMILIES}
    cells = []
    for e in C.ERAS:
        style = 'class="q-sw"' if e['fam'] == 'quaternary' else f'style="background:{col[e["fam"]]}"'
        cells.append(f'<div {style}>{bi(e["name"], "b")}{bi(e["sub"], "small")}</div>')
    ev = ''.join(bi(p, 'p') for p in EVENTS)
    return f'<div class="strip">{"".join(cells)}</div><div class="events">{ev}</div>'


ICONS = [
    '<svg class="ic" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M16 4c4 6 7 10 7 14a7 7 0 0 1-14 0c0-4 3-8 7-14Z"/><path d="M8 28h16M11 24.5l-1 3.5M21 24.5l1 3.5"/></svg>',
    '<svg class="ic" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M4 12c4-2 8 2 12 0s8-2 12 0M4 18c4-2 8 2 12 0s8-2 12 0M4 24c4-2 8 2 12 0s8-2 12 0"/></svg>',
    '<svg class="ic" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="16" cy="13" r="5"/><path d="M16 3v3M16 20v3M6 13H3M29 13h-3M8.9 5.9l2.1 2.1M21 18l2.1 2.1M8.9 20.1 11 18M21 8l2.1-2.1M6 28h20"/></svg>',
    '<svg class="ic" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><path d="M6 24 16 6l10 18Z"/><path d="M11 18h10"/></svg>',
]


def ideas():
    return ''.join(f'<article class="panel idea">{ICONS[i]}{bi(t, "h3")}{bi(p, "p")}</article>' for i, (t, p) in enumerate(C.IDEAS))


def sources():
    li = []
    for fr, en, url in C.SOURCES:
        txt = bi((fr, en))
        link = f' — <a href="{url}" target="_blank" rel="noopener">{url.split("/")[2]}</a>' if url else ''
        li.append(f'<li>{txt}{link}</li>')
    more = ('<p class="more" data-fr="Pour aller plus loin : <a href=&quot;../Vine_and_Vineyard/Vine_Terroir.html&quot;>La vigne &amp; le vignoble — chapitre Terroir</a>." '
            'data-en="Further reading: <a href=&quot;../Vine_and_Vineyard/Vine_Terroir.html&quot;>Vine &amp; Vineyard — Terroir chapter</a>.">'
            'Pour aller plus loin : <a href="../Vine_and_Vineyard/Vine_Terroir.html">La vigne &amp; le vignoble — chapitre Terroir</a>.</p>')
    note = ('<p class="more" data-fr="La carte montre la roche du sous-sol à l’échelle de la France (1/5 000 000) : à l’échelle d’une parcelle, la réalité est toujours plus fine. Les aires des régions sont la réunion des aires AOC de chaque carte régionale du site." '
            'data-en="The map shows bedrock at the scale of France (1:5,000,000): at the scale of a vineyard plot, reality is always more detailed. Region areas are the union of the AOC areas of each regional map on this site.">'
            'La carte montre la roche du sous-sol à l’échelle de la France (1/5 000 000) : à l’échelle d’une parcelle, la réalité est toujours plus fine. Les aires des régions sont la réunion des aires AOC de chaque carte régionale du site.</p>')
    return f'<h3 data-fr="Sources" data-en="Sources">Sources</h3><ol>{"".join(li)}</ol>{note}{more}'


def main():
    regions = []
    for r in C.REGIONS:
        d = dict(r)
        d['href'] = '../../' + urllib.parse.quote(PAGES[r['key']])
        d.setdefault('q', False)
        regions.append(d)
    assert [r['key'] for r in regions] == list(PAGES), 'region order/keys differ from PAGES'
    content = dict(families=C.FAMILIES, regions=regions, groups=C.GROUPS)
    html = ((HERE / 'template.html').read_text()
            .replace('@@BASE_CSS@@', base_css())
            .replace('@@LEAFLET_CSS@@', (GAMES / 'leaflet_css.txt').read_text())
            .replace('@@LEAFLET_JS@@', (GAMES / 'leaflet_js.txt').read_text())
            .replace('@@FAMILIES@@', families())
            .replace('@@TIME@@', time_strip())
            .replace('@@IDEAS@@', ideas())
            .replace('@@SOURCES@@', sources())
            .replace('@@CONTENT@@', json.dumps(content, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')))
    assert '@@' not in html.replace('@preserve', ''), html[html.index('@@'):html.index('@@') + 40]
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html)
    print(f'{OUT}: {len(html) / 1e3:.0f} kB, {len(regions)} regions, {len(C.FAMILIES)} families')


if __name__ == '__main__':
    main()
