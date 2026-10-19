# -*- coding: utf-8 -*-
"""Extra blocks for gen_page.py: Pomerol note, Burgundy premier cru search engine, sources & official bodies."""
import json
from pathlib import Path
from urllib.parse import quote

HERE = Path(__file__).parent


def build(T, L, esc, plan, sec_head, BGC):
    out = {}

    # ---------------- Pomerol ----------------
    out['pomerol'] = sec_head('pomerol', 'Bordeaux · Rive droite', 'Bordeaux · Right Bank',
                              'Pomerol — l’exception sans classement', 'Pomerol — the unclassified exception',
                              plan('Bordeaux_RightBank/Pomerol.html', 'Pomerol', 'Pomerol')) + '''
  <div class="panel prose pomerol">''' + L(
        '''<p>Voisine de Saint-Émilion, l’AOC <b>Pomerol</b> (reconnue en 1936, environ 800 ha sur une seule commune) n’a
  <b>jamais eu de classement</b> — et ne l’a jamais demandé. Elle abrite pourtant certains des vins les plus chers du monde :
  <b>Petrus</b>, <b>Le Pin</b>, Lafleur, Vieux Château Certan, Trotanoy, L’Église-Clinet, L’Évangile, La Conseillante…
  dont les prix dépassent souvent ceux des premiers crus de 1855.</p>
  <p>Pourquoi ? En 1855, Pomerol était un vignoble modeste, ignoré des courtiers du Médoc ; sa gloire ne date que du XX<sup>e</sup>
  siècle, portée par le négoce libournais (Jean-Pierre Moueix) et le marché anglo-saxon. Ses domaines, souvent petits
  (Le Pin compte à peine 2,8 ha), n’ont jamais vu l’intérêt d’une hiérarchie officielle : <b>c’est le marché qui classe Pomerol</b>.
  Sur l’étiquette, on ne lira donc que « Pomerol », sans aucune mention de cru.</p>''',
        '''<p>Next door to Saint-Émilion, the <b>Pomerol</b> AOC (recognised in 1936, about 800 ha in a single commune) has
  <b>never had a classification</b> — and has never asked for one. Yet it is home to some of the world’s most expensive wines:
  <b>Petrus</b>, <b>Le Pin</b>, Lafleur, Vieux Château Certan, Trotanoy, L’Église-Clinet, L’Évangile, La Conseillante…
  often priced above the 1855 first growths.</p>
  <p>Why? In 1855 Pomerol was a modest vineyard the Médoc brokers ignored; its fame dates only from the 20th century, built by the
  Libourne merchants (Jean-Pierre Moueix) and the British and American markets. Its estates, often tiny (Le Pin barely 2.8 ha),
  never saw the point of an official ranking: <b>in Pomerol, the market does the classifying</b>. The label simply reads
  “Pomerol”, with no cru term at all.</p>''') + '</div></section>'

    # ---------------- Burgundy premier cru search ----------------
    pc = json.load(open(HERE / 'premiers_crus.json'))
    gc = []
    COTE_GC = {'Chablis': 'chablis', 'Côte de Nuits': 'nuits', 'Côte de Beaune': 'beaune'}
    for fr, en, rows in BGC:
        for n, c, col in rows:
            if n == 'Chablis Grand Cru':
                for cl in c.split(' · '):
                    gc.append(['chablis', 'Chablis Grand Cru', cl, ['Chablis'], '', 'gc'])
            else:
                gc.append([COTE_GC[fr], n, n, [x.strip() for x in c.split('·') if not x.strip().isdigit()], '', 'gc'])
    data = [x + ['pc'] for x in pc] + gc
    maps = {}
    for a in sorted(set(x[1] for x in pc)):
        page = {'Ladoix': 'Ladoix-Serrigny'}.get(a, a)
        tail = ' — Climats 1er Cru, Grands Crus, relief 5 m & climats communaux · Carte.html' if a == 'Chablis' \
            else ' — Climats 1er Cru, relief 5 m & climats communaux · Carte.html'
        f = HERE.parents[2] / 'Bourgogne Regions' / 'Bourgogne climats' / (page + tail)
        if f.exists():
            maps[a] = '../Bourgogne%20Regions/Bourgogne%20climats/' + quote(page + tail)
    # ---- per-climat deep links into the climats maps (#climat=<name>, see climat_link_apply.py) ----
    import re, unicodedata
    def nz(x): return re.sub(r'[()]', '', unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode().lower().replace('\u2019', "'")).strip()
    cdir = HERE.parents[2] / 'Bourgogne Regions' / 'Bourgogne climats'
    feat = {}   # (tier, name) -> list of (page_url, app)
    for f in sorted(cdir.glob('*.html')):
        url = '../Bourgogne%20Regions/Bourgogne%20climats/' + quote(f.name)
        pg = f.name.split(' — ')[0]
        for pr in re.findall(r'"properties":(\{[^{}]*\})', f.read_text()):
            pr = json.loads(pr)
            if pr.get('tier') not in ('premier_cru', 'grand_cru'): continue
            ap = pr.get('app') or {'Ladoix-Serrigny': 'Ladoix'}.get(pg, pg)   # Maranges page: no app field
            feat.setdefault((pr['tier'], nz(pr['name'])), []).append((url, nz(ap), pg, pr['name']))
    maps['Blagny'] = maps.get('Meursault')
    # La Moutonne — monopole, not an official climat: approximate marker on the Chablis plan (moutonne_apply.py)
    data.append(['chablis', 'Monopole · nom d’usage', 'La Moutonne', ['Chablis'], '', 'gc'])
    precise = 0
    for r in data:
        if r[2] == 'La Moutonne':
            r += [maps['Chablis'] + '#climat=La%20Moutonne', 1]; precise += 1; continue
        tier = 'grand_cru' if r[5] == 'gc' else 'premier_cru'
        nm = {'clos de vougeot': 'clos de vougeot ou clos vougeot'}.get(nz(r[2]), nz(r[2]))
        cands = feat.get((tier, nm), [])
        if not cands and r[4]:   # Chablis climat sold under its principal climat → that polygon
            cands = feat.get((tier, nz(r[4])), [])
        if r[1] == 'Chablis Grand Cru':   # keep the 7 GC on the main Chablis plan (with La Moutonne), not the GC-only page
            cands = [c for c in cands if c[2] == 'Chablis'] or cands
        if r[1] == 'Blagny':     # Blagny climats are drawn on the Meursault / Puligny pages
            cands = [(u, 'blagny', pg, o) for u, ap, pg, o in cands if pg.startswith(('Meursault', 'Puligny'))]
        best = [c for c in cands if r[5] == 'pc' and c[1] == nz(r[1]) and nz(c[2]) == nz(r[1])] or \
               [c for c in cands if c[1] == nz(r[1]) and nz(c[2]).startswith(nz(r[1])[:6])] or \
               [c for c in cands if c[1] == nz(r[1])] or (cands if r[5] == 'gc' else [])
        if best:
            r += [best[0][0] + '#climat=' + quote(best[0][3]), 1]; precise += 1
        elif r[5] == 'pc' and maps.get(r[1]):
            r += [maps[r[1]], 0]
        else:
            r += ['', 0]
    out['gc_links'] = {r[2]: r[6] for r in data if r[5] == 'gc' and r[6] and r[2] != 'La Moutonne'}
    out['moutonne'] = maps['Chablis'] + '#climat=La%20Moutonne'
    print('climat links: %d precise, %d to the village map, %d none' % (precise,
          sum(1 for r in data if r[6] and not r[7]), sum(1 for r in data if not r[6])))
    n_pc = len(pc)
    apps = []
    for x in pc:
        if x[1] not in apps: apps.append(x[1])
    opts = ''.join(f'<option value="{esc(a)}">{esc(a)}</option>' for a in apps)
    out['pc_search'] = f'''
  <div class="panel pcs" id="premiers-crus">
    <div class="pcs-head">
      <div><h3 class="sub-h">{T('Rechercher un climat', 'Find a climat')}</h3>
      {L(f'<p class="pcs-intro">Les <b>{n_pc} climats premiers crus</b> de Bourgogne (et les 33 grands crus), d’après la délimitation officielle de l’INAO. Tapez un nom de climat, de commune ou d’appellation.</p>',
         f'<p class="pcs-intro">All <b>{n_pc} premier cru climats</b> of Burgundy (and the 33 grands crus), from the INAO’s official delimitation. Type a climat, commune or appellation name.</p>')}</div>
    </div>
    <div class="pcs-ctrl">
      <input id="pcq" type="search" autocomplete="off" data-ph-fr="ex. Clos Saint-Jacques, Perrières, Meursault…" data-ph-en="e.g. Clos Saint-Jacques, Perrières, Meursault…" placeholder="ex. Clos Saint-Jacques, Perrières, Meursault…">
      <select id="pccote">
        <option value="" data-fr="Toutes les régions" data-en="All regions">Toutes les régions</option>
        <option value="chablis">Chablis</option>
        <option value="nuits">Côte de Nuits</option>
        <option value="beaune">Côte de Beaune</option>
        <option value="chalon" data-fr="Côte chalonnaise" data-en="Côte Chalonnaise">Côte chalonnaise</option>
        <option value="macon" data-fr="Mâconnais" data-en="Mâconnais">Mâconnais</option>
      </select>
      <select id="pcapp"><option value="" data-fr="Toutes les appellations" data-en="All appellations">Toutes les appellations</option>{opts}</select>
      <label class="pcs-chk"><input type="checkbox" id="pcgc" checked> {T('Grands crus', 'Grands crus')}</label>
    </div>
    <p class="pcs-legend">{T('⌖ cliquez sur un climat pour le voir sur son plan cadastral · ↗ climat non tracé individuellement : carte du village', '⌖ click a climat to see it on its parcel map · ↗ climat not drawn individually: village map')}</p>
    <p class="pcs-count" id="pccount"></p>
    <div id="pcres" class="pcs-res"></div>
  </div>
<script>window.PC_DATA={json.dumps(data, ensure_ascii=False, separators=(',', ':'))};window.PC_MAPS={json.dumps(maps, ensure_ascii=False)};</script>'''

    # ---------------- sources & official bodies ----------------
    def org(name, fr, en, url=''):
        n = f'<a href="{url}" target="_blank" rel="noopener">{name}</a>' if url else name
        return f'<li><b>{n}</b>{L("<span> — " + fr + "</span>", "<span> — " + en + "</span>")}</li>'
    G = [
      ('État & Union européenne', 'State & European Union', [
        org('INAO — Institut national de l’origine et de la qualité', 'établissement public sous tutelle du ministère de l’Agriculture : reconnaît les AOC, rédige les cahiers des charges, délimite les aires et les climats ; son Comité national des appellations d’origine relatives aux vins (CNAOV) a approuvé le classement de Saint-Émilion (8 sept. 2022) et le cadre des premiers crus d’Alsace (juin 2025).',
            'public body under the Ministry of Agriculture: recognises AOCs, writes the specifications, delimits areas and climats; its national wine committee (CNAOV) approved the Saint-Émilion classification (8 Sept 2022) and the Alsace premier cru framework (June 2025).', 'https://www.inao.gouv.fr'),
        org('Ministère de l’Agriculture et de la Souveraineté alimentaire', 'homologue par arrêté les cahiers des charges et les classements (Graves 1953/1959, Mouton 1973, Saint-Émilion, Crus Bourgeois — arrêté du 29 déc. 2017, Crus Artisans — arrêté du 21 oct. 2022).',
            'ratifies specifications and classifications by decree (Graves 1953/1959, Mouton 1973, Saint-Émilion, Crus Bourgeois — decree of 29 Dec 2017, Crus Artisans — decree of 21 Oct 2022).', 'https://agriculture.gouv.fr'),
        org('Ministère de l’Économie et des Finances', 'cosigne l’homologation du classement de Saint-Émilion ; la DGCCRF contrôle l’étiquetage des mentions (cru classé, grand cru, premier cru…).',
            'co-signs the ratification of the Saint-Émilion classification; the DGCCRF enforces labelling of the terms (cru classé, grand cru, premier cru…).', 'https://www.economie.gouv.fr/dgccrf'),
        org('Journal officiel / Légifrance', 'publication des décrets d’AOC (dès 1936-1938) et des arrêtés de classement.',
            'publication of AOC decrees (from 1936-1938) and classification decrees.', 'https://www.legifrance.gouv.fr'),
        org('data.gouv.fr — délimitation parcellaire des AOC viticoles', 'jeu de données ouvert de l’INAO (version du 15 juin 2026) d’où proviennent les climats premiers crus de la recherche ci-dessus.',
            'the INAO open dataset (15 June 2026 release) that supplies the premier cru climats in the search above.', 'https://www.data.gouv.fr'),
        org('Union européenne — eAmbrosia & règlement (UE) n° 1308/2013', 'registre européen des AOP ; protège les mentions traditionnelles « cru bourgeois » (1979), « cru artisan » (1994), « grand cru », « premier cru », « cru classé ».',
            'EU register of PDOs; protects the traditional terms “cru bourgeois” (1979), “cru artisan” (1994), “grand cru”, “premier cru”, “cru classé”.', 'https://ec.europa.eu/agriculture/eambrosia/'),
        org('Cour administrative d’appel & tribunal administratif de Bordeaux', 'annulation du classement des Crus Bourgeois de 2003 (2007) et suspension puis annulation du classement de Saint-Émilion de 2006.',
            'struck down the 2003 Crus Bourgeois classification (2007) and suspended, then annulled, the 2006 Saint-Émilion classification.'),
        org('UNESCO', 'inscription des « Climats du vignoble de Bourgogne » (2015) et des « Coteaux, maisons et caves de Champagne » (2015) au patrimoine mondial.',
            'World Heritage listing of the “Climats of the Burgundy vineyard” (2015) and the “Champagne hillsides, houses and cellars” (2015).', 'https://whc.unesco.org'),
      ]),
      ('Organismes historiques & de contrôle', 'Historical & certification bodies', [
        org('Chambre de commerce et d’industrie de Bordeaux', 'commanditaire du classement de 1855 (liste des courtiers du 18 avril 1855) ; relevé des prix des crus dès 1740 ; liste des 444 crus bourgeois de 1932 avec la Chambre d’agriculture de la Gironde.',
            'commissioned the 1855 Classification (brokers’ list of 18 April 1855); recorded cru prices from 1740; 1932 list of 444 crus bourgeois with the Gironde Chamber of Agriculture.'),
        org('Comité d’agriculture de Beaune', 'classement des climats de la Côte d’Or de 1861, d’après le Dr Jules Lavalle (1855).', '1861 ranking of the Côte d’Or climats, after Dr Jules Lavalle (1855).'),
        org('Bureau Veritas Certification', 'organisme tiers indépendant chargé d’instruire le classement de Saint-Émilion 2022.', 'independent third party that assessed the 2022 Saint-Émilion classification.'),
        org('Qualisud', 'organisme certificateur du classement des Crus Artisans du Médoc (2023).', 'certification body for the Crus Artisans du Médoc classification (2023).', 'https://www.qualisud.fr'),
      ]),
      ('Interprofessions & syndicats', 'Trade bodies & growers’ associations', [
        org('CIVB — Conseil interprofessionnel du vin de Bordeaux', 'interprofession bordelaise.', 'Bordeaux trade council.', 'https://www.bordeaux.com'),
        org('Conseil des Grands Crus Classés en 1855', 'regroupe les crus classés du Médoc et de Sauternes-Barsac.', 'association of the 1855 classified growths of the Médoc and Sauternes-Barsac.'),
        org('Syndicat des Crus Classés de Graves', 'les 16 crus classés de 1959.', 'the 16 classified growths of 1959.'),
        org('Association des Grands Crus Classés de Saint-Émilion', 'dossier de presse du classement 2022.', '2022 classification press kit.', 'https://agccse.fr'),
        org('Alliance des Crus Bourgeois du Médoc', 'liste officielle et dossier de presse du classement 2025.', 'official list and press kit of the 2025 classification.', 'https://www.crus-bourgeois.com'),
        org('Syndicat des Crus Artisans du Médoc', 'organisateur du classement quinquennal des crus artisans.', 'runs the five-yearly crus artisans classification.'),
        org('BIVB — Bureau interprofessionnel des vins de Bourgogne', 'chiffres de la hiérarchie bourguignonne (part de production par niveau).', 'figures for the Burgundy hierarchy (share of production per level).', 'https://www.bourgogne-wines.com'),
        org('CIVA — Conseil interprofessionnel des vins d’Alsace & AVA (Association des viticulteurs d’Alsace)', 'grands crus, dénominations communales et projet de premiers crus.', 'grands crus, communal denominations and the premier cru project.', 'https://www.vinsalsace.com'),
        org('Comité Champagne (CIVC)', 'interprofession créée par la loi de 1941 ; échelle des crus et villages grands et premiers crus.', 'trade body created by the 1941 law; the échelle des crus and grand & premier cru villages.', 'https://www.champagne.fr'),
        org('Association des Crus Classés de Côtes de Provence', 'les 18 crus classés de 1955.', 'the 18 crus classés of 1955.'),
        org('Inter Rhône, InterLoire, CIVL (Languedoc), Inter Beaujolais', 'hiérarchies régionales : crus du Rhône, crus communaux du Muscadet, crus du Languedoc, projets de premiers crus du Beaujolais.',
            'regional hierarchies: Rhône crus, Muscadet crus communaux, crus du Languedoc, Beaujolais premier cru projects.'),
      ]),
      ('Documents', 'Documents', [
        org('Cahiers des charges des AOC', 'Chablis, Alsace grand cru (arrêté du 4 juillet 2025), Champagne (arrêté du 31 juillet 2025), Saint-Émilion grand cru, Pouilly-Fuissé… — voir la bibliothèque des décrets du site.',
            'Chablis, Alsace grand cru (decree of 4 July 2025), Champagne (decree of 31 July 2025), Saint-Émilion grand cru, Pouilly-Fuissé… — see the site’s decree library.', 'AOC_Decree/AOC_Library.html'),
        org('« All Classification Liste_2026 » & « Cru Bourgeois Classification_2025 »', 'documents de travail d’origine, vérifiés et corrigés d’après les sources ci-dessus.',
            'the original working documents, checked and corrected against the sources above.'),
      ]),
    ]
    blocks = ''.join(f'<div class="srcg"><h3>{T(fr, en)}</h3><ul>{"".join(items)}</ul></div>' for fr, en, items in G)
    out['sources'] = sec_head('sources', 'Références', 'References', 'Sources & organismes officiels', 'Sources & official bodies') + \
        f'<div class="panel srcs">{blocks}</div></section>'
    return out
