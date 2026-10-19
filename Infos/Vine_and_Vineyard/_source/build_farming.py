#!/usr/bin/env python3
"""Build Infos/Vine_and_Vineyard/Vine_Farming.html (chapter 8 — farming philosophies).
Run:  python3 "WEB Site/Infos/Vine_and_Vineyard/_source/build_farming.py"
"""
import math
from common import HERE, att, t, blk, base_css, pro_panel, chapter_nav, PRO_ICON

OUT = HERE.parent / 'Vine_Farming.html'
INK = '#3b2a1e'
SERIF = 'Iowan Old Style,Palatino,Georgia,serif'


def lbl(x, y, pair, anchor='middle', size=14, fill=INK, weight='400', extra=''):
    return (f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'font-family="{SERIF}" {extra}data-fr="{att(pair[0])}" data-en="{att(pair[1])}">{pair[0]}</text>')


APPROACHES = [  # id, colour, short name, name, one-line
  ('conv', '#7a7a80', ('Conventionnelle', 'Conventional'), ('synthèse, préventif', 'synthetic, preventive')),
  ('raison', '#4f7fae', ('Raisonnée', 'Integrated (IPM)'), ('traiter si besoin', 'spray if needed')),
  ('hve', '#2f7d8c', ('HVE · Terra Vitis', 'HVE · Terra Vitis'), ('certifications', 'certifications')),
  ('bio', '#5f9a3a', ('Biologique', 'Organic'), ('sans synthèse', 'no synthetics')),
  ('bd', '#8a5aa0', ('Biodynamique', 'Biodynamic'), ('bio + préparations', 'organic + preparations')),
]


def spectrum():
    s = ['<svg class="diagram" viewBox="0 0 680 200" role="img" aria-label="Du conventionnel à la biodynamie / From conventional to biodynamic">']
    s.append('<defs><linearGradient id="sp" x1="0" x2="1"><stop offset="0" stop-color="#b9b9be"/><stop offset=".5" stop-color="#7fb0a0"/><stop offset="1" stop-color="#9a7ab8"/></linearGradient>'
             '<marker id="spa" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="#6b5a48" stroke-width="1.8"/></marker></defs>')
    s.append('<rect x="40" y="76" width="600" height="14" rx="7" fill="url(#sp)"/>')
    s.append('<path d="M40 112 L640 112" stroke="#6b5a48" stroke-width="1.4" marker-end="url(#spa)"/>')
    s.append(lbl(40, 132, ('moins de contraintes', 'fewer constraints'), anchor='start', size=12.5, fill='#7a6650'))
    s.append(lbl(640, 132, ('plus d’exigences sur les intrants', 'stricter limits on inputs'), anchor='end', size=12.5, fill='#7a6650'))
    for i, (aid, col, name, line) in enumerate(APPROACHES):
        x = 70 + i * 135
        s.append(f'<a href="#{aid}"><circle cx="{x}" cy="83" r="17" fill="{col}" stroke="#fbf6ea" stroke-width="3"/>'
                 f'<text x="{x}" y="89" text-anchor="middle" font-size="15" font-weight="700" fill="#fff" font-family="{SERIF}">{i + 1}</text></a>')
        s.append(lbl(x, 40, name, size=14.5, weight='600'))
        s.append(lbl(x, 58, line, size=11.5, fill='#7a6650'))
    s.append(lbl(340, 178, ('Le « vin nature » relève surtout de la vinification : raisins bio, intrants minimum au chai.',
                            '“Natural wine” is mainly a winemaking matter: organic grapes, minimal cellar inputs.'), size=12.5, fill='#7a6650', extra='font-style="italic" '))
    s.append('</svg>')
    return ''.join(s)


CARDS = [
  dict(id='conv', col='#7a7a80', name=('Viticulture conventionnelle', 'Conventional viticulture'),
       what=('Elle utilise les produits phytosanitaires et engrais de synthèse autorisés, souvent selon un calendrier préventif. Les plans Écophyto successifs, depuis 2008, visent à en réduire l’usage.',
             'It uses approved synthetic crop-protection products and fertilisers, often on a preventive schedule. Successive Écophyto plans, since 2008, aim to reduce their use.'),
       plus=('Protection efficace et régulière, coûts maîtrisés.', 'Effective, reliable protection, controlled costs.'),
       minus=('Résidus, impact sur la biodiversité et l’eau, image auprès des consommateurs.', 'Residues, impact on biodiversity and water, consumer image.')),
  dict(id='raison', col='#4f7fae', name=('Viticulture raisonnée, lutte intégrée', 'Integrated pest management'),
       what=('On observe la vigne, on suit les modèles de prévision et les bulletins de santé du végétal, et l’on ne traite qu’au-delà d’un seuil de risque. On privilégie les auxiliaires, la confusion sexuelle, l’enherbement.',
             'Growers monitor the vines, follow forecasting models and plant-health bulletins, and spray only above a risk threshold. Beneficial insects, mating disruption and cover crops are favoured.'),
       plus=('Moins de traitements sans renoncer aux produits de synthèse.', 'Fewer sprays without giving up synthetic products.'),
       minus=('Démarche peu encadrée en elle-même : c’est le rôle des certifications.', 'Loosely defined on its own: that is what certifications are for.')),
  dict(id='hve', col='#2f7d8c', name=('HVE, Terra Vitis, Vignerons Engagés', 'HVE, Terra Vitis, Vignerons Engagés'),
       what=('La <b>Haute Valeur Environnementale</b> est une certification de l’État (créée en 2012) qui évalue toute l’exploitation sur quatre thèmes : biodiversité, stratégie phytosanitaire, fertilisation et irrigation. <b>Terra Vitis</b> (depuis 1998) et <b>Vignerons Engagés</b> sont des démarches de la filière, plus larges (social, économie, environnement).',
             '<b>High Environmental Value</b> (HVE) is a state certification (created in 2012) that assesses the whole farm on four themes: biodiversity, crop-protection strategy, fertilisation and irrigation. <b>Terra Vitis</b> (since 1998) and <b>Vignerons Engagés</b> are industry schemes with a broader scope (social, economic, environmental).'),
       plus=('Contrôles par un organisme tiers ; la viticulture est de loin la première filière certifiée HVE.', 'Third-party audits; viticulture is by far the leading HVE-certified sector.'),
       minus=('Produits de synthèse autorisés ; exigences jugées trop faibles par certains, d’où un référentiel renforcé en 2023.', 'Synthetic products allowed; some consider the requirements too weak, hence a tougher standard in 2023.')),
  dict(id='bio', col='#5f9a3a', name=('Agriculture biologique', 'Organic farming'),
       what=('Aucun pesticide, herbicide ni engrais de synthèse ; protection par le cuivre, le soufre et des produits naturels ; travail du sol ou enherbement. Trois ans de conversion avant la certification. Le vin bio suit aussi des règles de vinification (depuis 2012), avec moins de sulfites autorisés.',
             'No synthetic pesticides, herbicides or fertilisers; protection with copper, sulphur and natural products; tillage or cover crops. Three years of conversion before certification. Organic wine also follows winemaking rules (since 2012), with lower permitted sulphites.'),
       plus=('Cadre européen précis et contrôlé ; environ un cinquième du vignoble français, conversion comprise.', 'Precise, audited EU framework; about one fifth of French vineyard area, including conversion.'),
       minus=('Plus de passages dans les années humides, accumulation de cuivre dans les sols, rendements parfois plus faibles.', 'More passes in wet years, copper build-up in soils, sometimes lower yields.')),
  dict(id='bd', col='#8a5aa0', name=('Biodynamie', 'Biodynamics'),
       what=('Issue des conférences de Rudolf Steiner (1924), elle ajoute au bio des préparations à base de bouse, de silice et de plantes, utilisées à doses infimes, et un calendrier tenant compte des rythmes lunaires et planétaires. Le domaine est pensé comme un organisme vivant.',
             'Born of Rudolf Steiner’s 1924 lectures, it adds to organic farming preparations made from manure, silica and plants, used in tiny doses, and a calendar based on lunar and planetary rhythms. The estate is seen as a living organism.'),
       plus=('Grande attention à la vigne et au sol ; adoptée par de grands domaines (Leroy, Coulée de Serrant…).', 'Close attention to vines and soil; adopted by leading estates (Leroy, Coulée de Serrant…).'),
       minus=('Les effets propres des préparations ne font pas consensus scientifique.', 'The specific effects of the preparations lack scientific consensus.')),
]


def cards():
    out = []
    for i, c in enumerate(CARDS):
        out.append(f'''<article class="ap" id="{c['id']}" style="--c:{c['col']}">
      <div class="ap-n">{i + 1}</div>
      <div class="ap-b"><h3>{t(c['name'])}</h3>{blk(c['what'])}
        <div class="pm"><p class="plus"><b>+</b> {t(c['plus'])}</p><p class="minus"><b>–</b> {t(c['minus'])}</p></div></div></article>''')
    return ''.join(out)


# comparison: rows × columns (conv, raison, hve, bio, bd); values: 'y' allowed, 'n' forbidden, 'l' limited
COMPARE = [
  (('Pesticides de synthèse', 'Synthetic pesticides'), 'yylnn'),
  (('Herbicides chimiques', 'Chemical herbicides'), 'yllnn'),
  (('Engrais de synthèse', 'Synthetic fertilisers'), 'yylnn'),
  (('Cuivre et soufre', 'Copper and sulphur'), 'yyyll'),
  (('Préparations biodynamiques', 'Biodynamic preparations'), '----y'),
  (('Certification et contrôle', 'Certification and audits'), 'nnyyy'),
  (('Règles de vinification propres', 'Own winemaking rules'), 'nnnyy'),
]


def compare_table():
    sym = {'y': ('ok', '✓', ('autorisé', 'allowed')), 'n': ('no', '✕', ('interdit / non', 'forbidden / no')), 'l': ('lim', '◐', ('limité', 'limited')), '-': ('na', '—', ('sans objet', 'n/a'))}
    head = '<tr><th></th>' + ''.join(f'<th style="--c:{col}"><span class="n">{i + 1}</span>{t(n)}</th>' for i, (_, col, n, _l) in enumerate(APPROACHES)) + '</tr>'
    rows = ''
    for name, vals in COMPARE:
        rows += f'<tr><td>{t(name)}</td>' + ''.join(f'<td class="{sym[v][0]}" title="{sym[v][2][0]}">{sym[v][1]}</td>' for v in vals) + '</tr>'
    return f'<thead>{head}</thead><tbody>{rows}</tbody>'


PREPS = [
  ('500', ('Bouse de corne', 'Horn manure'), ('sol, racines', 'soil, roots'), '#8a5a2b'),
  ('501', ('Silice de corne', 'Horn silica'), ('lumière, feuillage', 'light, foliage'), '#c9b84a'),
  ('502', ('Achillée', 'Yarrow'), ('compost', 'compost'), '#e8d9a0'),
  ('503', ('Camomille', 'Chamomile'), ('compost', 'compost'), '#f2e28a'),
  ('504', ('Ortie', 'Nettle'), ('compost', 'compost'), '#6f9a3a'),
  ('505', ('Écorce de chêne', 'Oak bark'), ('compost', 'compost'), '#9b7b52'),
  ('506', ('Pissenlit', 'Dandelion'), ('compost', 'compost'), '#e8b83a'),
  ('507', ('Valériane', 'Valerian'), ('compost', 'compost'), '#c9a0c0'),
]


def preps_wheel():
    cx, cy = 340, 210
    s = ['<svg class="diagram" viewBox="0 0 680 420" role="img" aria-label="Les préparations biodynamiques / Biodynamic preparations">']
    s.append(f'<circle cx="{cx}" cy="{cy}" r="160" fill="#f3ead6" stroke="#d9c9a3"/>')
    for i, (code, name, use, col) in enumerate(PREPS):
        a = math.radians(i * 45 - 90)
        x, y = cx + 112 * math.cos(a), cy + 112 * math.sin(a)
        s.append(f'<line x1="{cx + 54 * math.cos(a):.1f}" y1="{cy + 54 * math.sin(a):.1f}" x2="{cx + 84 * math.cos(a):.1f}" y2="{cy + 84 * math.sin(a):.1f}" stroke="#c9b48a" stroke-width="1.4"/>')
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="31" fill="{col}" stroke="#fbf6ea" stroke-width="3"/>')
        s.append(f'<text x="{x:.1f}" y="{y + 6:.1f}" text-anchor="middle" font-size="17" font-weight="700" fill="#2b2018" font-family="{SERIF}">{code}</text>')
        tx = cx + 178 * math.cos(a); ty = cy + 178 * math.sin(a)
        anc = 'start' if math.cos(a) > .3 else 'end' if math.cos(a) < -.3 else 'middle'
        dy = -6 if math.sin(a) < -.5 else 10 if math.sin(a) > .5 else 0
        s.append(lbl(tx, ty + dy, name, anchor=anc, size=14, weight='600'))
        s.append(lbl(tx, ty + dy + 16, use, anchor=anc, size=12, fill='#7a6650'))
    s.append(f'<circle cx="{cx}" cy="{cy}" r="52" fill="#fbf6ea" stroke="#d9c9a3"/>')
    s.append(lbl(cx, cy - 4, ('Les 8', 'The 8'), size=16, weight='600'))
    s.append(lbl(cx, cy + 16, ('préparations', 'preparations'), size=13))
    s.append('</svg>')
    return ''.join(s)


LABELS = [  # badge text, colour, name, what it guarantees
  ('HVE', '#2f7d8c', ('Haute Valeur Environnementale', 'High Environmental Value'),
   ('Exploitation certifiée niveau 3 par un organisme agréé. Mention possible sur l’étiquette : « issu d’une exploitation de Haute Valeur Environnementale ».', 'Farm certified at level 3 by an accredited body. Label wording: “from a High Environmental Value farm”.')),
  ('BIO', '#5f9a3a', ('Agriculture biologique (AB et logo européen)', 'Organic (AB and EU logo)'),
   ('Raisins et vinification conformes au règlement européen ; « en conversion » pendant les trois premières années.', 'Grapes and winemaking comply with the EU regulation; “in conversion” for the first three years.')),
  ('BD', '#8a5aa0', ('Demeter, Biodyvin', 'Demeter, Biodyvin'),
   ('Marques privées de biodynamie, qui exigent d’abord la certification bio. Biodyvin est propre au vin.', 'Private biodynamic brands, which first require organic certification. Biodyvin is specific to wine.')),
  ('TV', '#4f7fae', ('Terra Vitis', 'Terra Vitis'),
   ('Cahier des charges de viticulture durable porté par la filière, contrôlé par un organisme indépendant.', 'Industry-led sustainable-viticulture standard, audited by an independent body.')),
  ('VMN', '#a0283c', ('Vin méthode nature', 'Vin méthode nature'),
   ('Charte reconnue en 2020 : raisins bio vendangés à la main, levures indigènes, aucun intrant ; sulfites ajoutés au plus 30 mg/L, avec un logo distinct.', 'Charter recognised in 2020: organic, hand-picked grapes, native yeasts, no additives; at most 30 mg/L added sulphites, with a distinct logo.')),
]


def label_cards():
    return ''.join(f'<div class="lab" style="--c:{c}"><span class="badge">{b}</span><div><b>{t(n)}</b>{blk(d, "p")}</div></div>' for b, c, n, d in LABELS)


PRO_BIO = [
  (('Le règlement', 'The regulation'),
   ('Règlement (UE) 2018/848, en vigueur depuis 2022 (il remplace le 834/2007) ; règles de vinification bio depuis 2012. Contrôle annuel par un organisme certificateur agréé (Ecocert, Certipaq, Bureau Veritas…).',
    'Regulation (EU) 2018/848, in force since 2022 (replacing 834/2007); organic winemaking rules since 2012. Annual audit by an accredited certification body (Ecocert, Certipaq, Bureau Veritas…).')),
  (('Le cuivre', 'Copper'),
   ('Plafonné à 28 kg/ha sur 7 ans, soit 4 kg/ha/an en moyenne, lissable d’une année sur l’autre. Indispensable contre le mildiou en bio, il s’accumule dans les sols ; d’où la recherche de biocontrôle et de cépages résistants.',
    'Capped at 28 kg/ha over 7 years, i.e. 4 kg/ha/year on average, which can be averaged across years. Essential against downy mildew in organic farming, it builds up in soils; hence research into biocontrol and resistant varieties.')),
  (('Les sulfites', 'Sulphites'),
   ('Teneurs maximales en SO<sub>2</sub> total des vins secs : 100 mg/L pour un rouge bio contre 150 en conventionnel, 150 mg/L pour un blanc ou rosé bio contre 200. Certains additifs et techniques sont interdits (désalcoolisation partielle, électrodialyse…).',
    'Maximum total SO<sub>2</sub> in dry wines: 100 mg/L for an organic red versus 150 conventional, 150 mg/L for an organic white or rosé versus 200. Some additives and techniques are banned (partial dealcoholisation, electrodialysis…).')),
]

PRO_BD = [
  (('Les préparations', 'The preparations'),
   ('La 500 (bouse de vache fermentée l’hiver dans une corne enterrée) est pulvérisée sur le sol au printemps et à l’automne ; la 501 (quartz broyé, enterré l’été) sur le feuillage, tôt le matin. Les 502 à 507 sont ajoutées au compost. Doses de quelques grammes à quelques centaines de grammes par hectare, « dynamisées » dans l’eau.',
    'Preparation 500 (cow manure fermented over winter in a buried horn) is sprayed on the soil in spring and autumn; 501 (ground quartz, buried over summer) on the foliage, early in the morning. Preparations 502–507 are added to compost. Doses from a few grams to a few hundred grams per hectare, “dynamised” in water.')),
  (('Le calendrier', 'The calendar'),
   ('Les calendriers (Maria Thun et ses successeurs) classent les jours en jours fruit, fleur, feuille ou racine selon la position de la Lune devant les constellations ; les vignerons y calent traitements, taille ou mise en bouteille.',
    'The calendars (Maria Thun and her successors) classify days as fruit, flower, leaf or root days according to the Moon’s position against the constellations; growers time spraying, pruning or bottling by them.')),
  (('Ce que dit la science', 'What science says'),
   ('Les comparaisons montrent surtout les effets des pratiques bio qui sous-tendent la biodynamie (vie du sol, vigueur modérée) ; un effet spécifique des préparations n’est pas établi. Le soin accru porté aux vignes reste, pour beaucoup, l’explication la plus simple de la réputation des domaines biodynamiques.',
    'Comparisons mostly show the effects of the organic practices underlying biodynamics (soil life, moderate vigour); a specific effect of the preparations has not been established. The extra care given to the vines remains, for many, the simplest explanation of biodynamic estates’ reputation.')),
]

PRO_FUTURE = [
  (('Cépages résistants', 'Resistant varieties'),
   ('Les variétés résistantes au mildiou et à l’oïdium (programme ResDur de l’INRAE : Artaban, Vidoc, Floreal, Voltis…) permettent de réduire fortement les traitements fongicides, de l’ordre de 80 à 90 %. Leur entrée dans les AOC reste limitée, souvent sous le statut de « variétés d’intérêt à fin d’adaptation ».',
    'Varieties resistant to downy and powdery mildew (INRAE’s ResDur programme: Artaban, Vidoc, Floreal, Voltis…) can cut fungicide sprays sharply, by around 80–90 %. Their entry into AOCs is still limited, often under the status of “varieties of interest for adaptation”.')),
  (('Agroécologie', 'Agroecology'),
   ('Haies, arbres dans les vignes (agroforesterie), moutons en hiver pour tondre l’herbe, nichoirs à mésanges et chauves-souris contre les vers de la grappe : la biodiversité devient un outil de protection.',
    'Hedges, trees among the vines (agroforestry), sheep in winter to graze the grass, nest boxes for tits and bats against grape moths: biodiversity becomes a protection tool.')),
]

SOURCES = [
  ('Règlement (UE) 2018/848 relatif à la production biologique ; règlement d’exécution (UE) 203/2012 (vin biologique).', 'Regulation (EU) 2018/848 on organic production; Implementing Regulation (EU) 203/2012 (organic wine).'),
  ('Ministère de l’Agriculture, référentiel de la certification environnementale (HVE), version 2023.', 'French Ministry of Agriculture, environmental certification (HVE) standard, 2023 version.'),
  ('Agence Bio, chiffres de la viticulture biologique.', 'Agence Bio, organic viticulture figures.'),
  ('Steiner R., <i>Cours aux agriculteurs</i>, 1924 ; Demeter, Biodyvin (SIVCBD), cahiers des charges.', 'Steiner R., <i>Agriculture Course</i>, 1924; Demeter, Biodyvin (SIVCBD), standards.'),
  ('Syndicat de défense des vins nature’l, charte « Vin méthode nature », 2020 ; INRAE, programme ResDur.', 'Syndicat de défense des vins nature’l, “Vin méthode nature” charter, 2020; INRAE, ResDur programme.'),
]


def main():
    tpl = (HERE / 'farming_template.html').read_text()
    rep = {
        '@@BASE_CSS@@': base_css(),
        '@@PRO_ICON@@': PRO_ICON,
        '@@SPECTRUM@@': spectrum(),
        '@@CARDS@@': cards(),
        '@@COMPARE@@': compare_table(),
        '@@PREPS@@': preps_wheel(),
        '@@LABELS@@': label_cards(),
        '@@PRO_BIO@@': pro_panel(PRO_BIO),
        '@@PRO_BD@@': pro_panel(PRO_BD),
        '@@PRO_FUTURE@@': pro_panel(PRO_FUTURE),
        '@@CHAPTERS@@': chapter_nav(8),
        '@@SOURCES@@': ''.join(f'<li>{t(s)}</li>' for s in SOURCES),
    }
    html = tpl
    for k, v in rep.items():
        html = html.replace(k, v)
    assert '@@' not in html, html[html.index('@@'):html.index('@@') + 40]
    OUT.write_text(html)
    print(f'{OUT.name}: {len(html) // 1024} KB')


if __name__ == '__main__':
    main()
