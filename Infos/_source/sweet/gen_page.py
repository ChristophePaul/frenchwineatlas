"""Builds Infos/Sweet_Wines/Douce_France.html — « Douce France… » / "Sweet France…".

The sweet, fortified and oxidative wines of France, method by method, with every AOC/AOP, its key legal
figures (taken from the cahiers des charges in force) and its grape varieties (read from the Cépages data,
Infos/Vine_and_Vineyard/Cepages/_source/data). Vin jaune closes the page.
Bilingual FR/EN like the other Infos pages; shared look = Vine & Vineyard base.css.
Run:  python3 gen_page.py
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INFOS = HERE.parent.parent
sys.path.insert(0, str(INFOS / 'Vine_and_Vineyard' / '_source'))
sys.path.insert(0, str(INFOS / 'Vine_and_Vineyard' / 'Cepages' / '_source'))
from common import base_css, t, blk, att  # noqa: E402
import parse as cep  # noqa: E402

OUT = INFOS / 'Sweet_Wines' / 'Douce_France.html'


def L(url, label='lien'):
    return f' <a href="{url}" target="_blank" rel="noopener">{label}</a>'


LF = 'https://www.legifrance.gouv.fr/jorf/id/'

# ------------------------------------------------------------------ sources (key, FR, EN)
SOURCES = [
    ('inao', 'INAO, cahiers des charges des appellations d’origine (versions en vigueur, homologuées par décret ou arrêté et publiées au <i>Bulletin officiel</i> du ministère de l’Agriculture). Chiffres de cette page : chapitre I, points VII (maturité), VIII et IX (élaboration, normes analytiques, élevage, mise en marché).' + L('https://www.inao.gouv.fr/', 'inao.gouv.fr'),
             'INAO, product specifications (<i>cahiers des charges</i>) of the appellations of origin (versions in force, approved by decree or order and published in the Ministry of Agriculture’s <i>Bulletin officiel</i>). Figures on this page: chapter I, points VII (ripeness), VIII and IX (production, analytical standards, ageing, release).' + L('https://www.inao.gouv.fr/', 'inao.gouv.fr')),
    ('ue1308', 'Règlement (UE) n° 1308/2013 portant organisation commune des marchés (OCM), annexe VII, partie II : catégories de produits de la vigne (« vin de liqueur » : TAV acquis 15–22 %, TAV total ≥ 17,5 %).' + L('https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32013R1308', 'eur-lex'),
               'Regulation (EU) No 1308/2013 establishing a common organisation of the markets (CMO), Annex VII, Part II: categories of grapevine products (“liqueur wine”: actual alcohol 15–22%, total ≥ 17.5%).' + L('https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32013R1308', 'eur-lex')),
    ('ue2019', 'Règlement délégué (UE) 2019/33 de la Commission : annexe III (mentions de teneur en sucre : sec, demi-sec, moelleux, doux ; brut… doux pour les mousseux), article 56 et annexe VII point 3 (bouteille « Clavelin »).' + L('https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32019R0033', 'eur-lex'),
               'Commission Delegated Regulation (EU) 2019/33: Annex III (sugar-content terms: sec, demi-sec, moelleux, doux; brut… doux for sparkling wines), Article 56 and Annex VII point 3 (the “Clavelin” bottle).' + L('https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32019R0033', 'eur-lex')),
    ('dir2007', 'Directive 2007/45/CE fixant les quantités nominales des produits en préemballages : le vin jaune n’est autorisé qu’en 62 cl.' + L('https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32007L0045', 'eur-lex'),
                'Directive 2007/45/EC on nominal quantities for prepacked products: vin jaune is allowed in 62 cl only.' + L('https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32007L0045', 'eur-lex')),
    ('sauternes', 'Cahiers des charges des AOC « Sauternes » et « Barsac » (raisins à surmaturité avec pourriture noble, tries successives manuelles, ≥ 221 g/l, ≥ 45 g/l de sucres ; traitements anti-botrytis interdits).',
                  'Specifications of the “Sauternes” and “Barsac” AOCs (over-ripe grapes with noble rot, successive hand-picked passes, ≥ 221 g/l, ≥ 45 g/l of sugar; anti-botrytis sprays banned).'),
    ('bdx_sweet', 'Cahiers des charges des AOC « Cérons » (arrêté du 17 novembre 2023), « Loupiac », « Sainte-Croix-du-Mont », « Cadillac », « Premières Côtes de Bordeaux », « Côtes de Bordeaux-Saint-Macaire », « Graves supérieures », « Côtes de Bordeaux » (arrêté du 29 décembre 2025) et « Bordeaux supérieur ».',
                  'Specifications of the “Cérons” (order of 17 November 2023), “Loupiac”, “Sainte-Croix-du-Mont”, “Cadillac”, “Premières Côtes de Bordeaux”, “Côtes de Bordeaux-Saint-Macaire”, “Graves supérieures”, “Côtes de Bordeaux” (order of 29 December 2025) and “Bordeaux supérieur” AOCs.'),
    ('so_sweet', 'Cahiers des charges des AOC « Monbazillac », « Saussignac » (décret n° 2011-1183 modifié), « Haut-Montravel », « Côtes de Montravel », « Rosette » (décret n° 2011-1401 modifié), « Côtes de Bergerac », « Côtes de Duras », « Jurançon », « Pacherenc du Vic-Bilh » et « Gaillac » (2025).',
                 'Specifications of the “Monbazillac”, “Saussignac” (decree No 2011-1183 as amended), “Haut-Montravel”, “Côtes de Montravel”, “Rosette” (decree No 2011-1401 as amended), “Côtes de Bergerac”, “Côtes de Duras”, “Jurançon”, “Pacherenc du Vic-Bilh” and “Gaillac” (2025) AOCs.'),
    ('loire_sweet', 'Cahiers des charges des AOC « Coteaux du Layon », « Quarts de Chaume », « Coteaux de Saumur » (arrêtés du 10 octobre 2019), « Bonnezeaux » (arrêté du 7 octobre 2022), « Coteaux de l’Aubance » (décret n° 2011-1353 modifié), « Anjou-Coteaux de la Loire » (décret n° 2011-1544 modifié), « Vouvray », « Montlouis-sur-Loire », « Jasnières », « Coteaux du Loir », « Savennières ».',
                    'Specifications of the “Coteaux du Layon”, “Quarts de Chaume”, “Coteaux de Saumur” (orders of 10 October 2019), “Bonnezeaux” (order of 7 October 2022), “Coteaux de l’Aubance” (decree No 2011-1353 as amended), “Anjou-Coteaux de la Loire” (decree No 2011-1544 as amended), “Vouvray”, “Montlouis-sur-Loire”, “Jasnières”, “Coteaux du Loir”, “Savennières” AOCs.'),
    ('alsace', 'Cahiers des charges des AOC « Alsace » et « Alsace grand cru » (décret n° 2011-1373 du 25 octobre 2011, modifié) : mentions « vendanges tardives » et « sélection de grains nobles ».',
               'Specifications of the “Alsace” and “Alsace grand cru” AOCs (decree No 2011-1373 of 25 October 2011, as amended): “vendanges tardives” and “sélection de grains nobles”.'),
    ('paille', 'Cahiers des charges des AOC « Arbois », « Côtes du Jura », « L’Étoile » (mention « vin de paille »), « Hermitage » (mention « vin de paille ») et « Corrèze » (arrêté du 28 septembre 2017).',
               'Specifications of the “Arbois”, “Côtes du Jura”, “L’Étoile” (“vin de paille”), “Hermitage” (“vin de paille”) and “Corrèze” (order of 28 September 2017) AOCs.'),
    ('rivesaltes', 'Arrêté du 14 juin 2023 relatif au cahier des charges de l’AOC « Rivesaltes », JORF du 18 juin 2023 (mentions ambré, grenat, rosé, tuilé, hors d’âge, rancio ; élevage oxydatif jusqu’au 31 août de la 2<sup>e</sup> année).' + L(LF + 'JORFTEXT000047693738', 'légifrance'),
                   'Order of 14 June 2023 on the specification of the “Rivesaltes” AOC, JORF of 18 June 2023 (mentions ambré, grenat, rosé, tuilé, hors d’âge, rancio; oxidative ageing until 31 August of the 2nd year).' + L(LF + 'JORFTEXT000047693738', 'légifrance')),
    ('banyuls', 'Cahiers des charges des AOC « Banyuls » et « Banyuls grand cru » (décret n° 2011-1828 du 7 décembre 2011 ; AOC grand cru reconnue en 1962).',
                'Specifications of the “Banyuls” and “Banyuls grand cru” AOCs (decree No 2011-1828 of 7 December 2011; grand cru AOC recognised in 1962).'),
    ('vdn_other', 'Cahiers des charges des AOC « Maury », « Grand Roussillon », « Rasteau » (vins doux naturels).',
                  'Specifications of the “Maury”, “Grand Roussillon”, “Rasteau” (vins doux naturels) AOCs.'),
    ('muscats', 'Cahiers des charges des AOC « Muscat de Rivesaltes » (décret n° 2011-1720), « Muscat de Frontignan », « Muscat de Lunel » (décret n° 2011-1744 modifié), « Muscat de Mireval » (décret n° 2011-1199), « Muscat de Saint-Jean-de-Minervois », « Muscat de Beaumes-de-Venise », « Muscat du Cap Corse » (décret n° 2011-781).',
                'Specifications of the “Muscat de Rivesaltes” (decree No 2011-1720), “Muscat de Frontignan”, “Muscat de Lunel” (decree No 2011-1744 as amended), “Muscat de Mireval” (decree No 2011-1199), “Muscat de Saint-Jean-de-Minervois”, “Muscat de Beaumes-de-Venise”, “Muscat du Cap Corse” (decree No 2011-781) AOCs.'),
    ('vdl', 'Cahiers des charges des AOC « Pineau des Charentes » (décret n° 2011-1453 modifié), « Floc de Gascogne » (décret n° 2011-1620), « Macvin du Jura » (arrêté du 1<sup>er</sup> décembre 2025) et « Clairette du Languedoc » (décret n° 2011-1389).',
            'Specifications of the “Pineau des Charentes” (decree No 2011-1453 as amended), “Floc de Gascogne” (decree No 2011-1620), “Macvin du Jura” (order of 1 December 2025) and “Clairette du Languedoc” (decree No 2011-1389) AOCs.'),
    ('bulles', 'Cahiers des charges des AOC « Clairette de Die » (arrêté du 27 février 2024), « Gaillac », « Limoux » (Blanquette méthode ancestrale), « Bugey » (Cerdon) et « Champagne ».',
               'Specifications of the “Clairette de Die” (order of 27 February 2024), “Gaillac”, “Limoux” (Blanquette méthode ancestrale), “Bugey” (Cerdon) and “Champagne” AOCs.'),
    ('jura_decrees', 'Décrets n° 2011-1187 (« Château-Chalon »), n° 2011-1188 (« Arbois »), n° 2011-1189 (« Côtes du Jura ») du 23 septembre 2011, JORF du 27 septembre 2011 ; décret n° 2011-1096 du 9 septembre 2011 modifié par le décret n° 2013-143 (« L’Étoile »).' + L(LF + 'JORFTEXT000024592005', 'légifrance'),
                     'Decrees No 2011-1187 (“Château-Chalon”), No 2011-1188 (“Arbois”), No 2011-1189 (“Côtes du Jura”) of 23 September 2011, JORF of 27 September 2011; decree No 2011-1096 of 9 September 2011 as amended by decree No 2013-143 (“L’Étoile”).' + L(LF + 'JORFTEXT000024592005', 'légifrance')),
    ('pasteur', 'Pasteur L. (1866). <i>Études sur le vin, ses maladies, causes qui les provoquent, procédés nouveaux pour le conserver et pour le vieillir</i>. Paris, Imprimerie impériale.',
                'Pasteur L. (1866). <i>Études sur le vin, ses maladies, causes qui les provoquent, procédés nouveaux pour le conserver et pour le vieillir</i>. Paris, Imprimerie impériale (in French).'),
    ('enology', 'Ribéreau-Gayon P., Dubourdieu D., Donèche B., Lonvaud A. (2006). <i>Handbook of Enology</i>, vol. 1 : <i>The Microbiology of Wine and Vinifications</i>, 2<sup>e</sup> éd. Wiley (chap. « Botrytized sweet wines » et « Conditions of yeast development » : pression osmotique, éthanol, carence en thiamine et en azote, botryticine).',
                'Ribéreau-Gayon P., Dubourdieu D., Donèche B., Lonvaud A. (2006). <i>Handbook of Enology</i>, vol. 1: <i>The Microbiology of Wine and Vinifications</i>, 2nd ed. Wiley (chapters “Botrytized sweet wines” and “Conditions of yeast development”: osmotic pressure, ethanol, thiamine and nitrogen deficiency, botryticine).'),
    ('oiv_ice', 'OIV, <i>Code international des pratiques œnologiques</i>, fiche I.4.7 « Vins de glace – Icewine – Eiswein » (résolution OENO 6/03) : raisins gelés au vignoble et pressés gelés, ≤ −7 °C recommandé, TAV potentiel ≥ 15 % non augmentable, TAV acquis ≥ 5,5 %.' + L('https://www.oiv.int/public/medias/3970/f-code-i-47.pdf', 'pdf'),
                'OIV, <i>International Code of Oenological Practices</i>, sheet I.4.7 “Icewine – Eiswein” (resolution OENO 6/03): grapes frozen in the vineyard and pressed frozen, ≤ −7 °C recommended, potential alcohol ≥ 15% not to be increased, actual alcohol ≥ 5.5%.' + L('https://www.oiv.int/public/medias/3970/f-code-i-47.pdf', 'pdf')),
    ('ue934', 'Règlement délégué (UE) 2019/934 de la Commission (pratiques œnologiques) : « Eiswein » y figure parmi les mentions traditionnelles d’autres États membres (Allemagne, Autriche).' + L('https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32019R0934', 'eur-lex'),
              'Commission Delegated Regulation (EU) 2019/934 (oenological practices): “Eiswein” appears among the traditional terms of other Member States (Germany, Austria).' + L('https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32019R0934', 'eur-lex')),
    ('plaimont', 'Plaimont, « Les vendanges de la Saint-Sylvestre » (Viella, Gers) : tradition née après le gel de 1991 ; Pacherenc issu des 4<sup>e</sup> et 5<sup>e</sup> tries, raisins passerillés, ≈ 5 hl/ha.' + L('https://www.plaimont.com/en', 'plaimont.com'),
                 'Plaimont, “The Saint-Sylvestre harvest” (Viella, Gers): a tradition born after the 1991 frost; Pacherenc from the 4th and 5th passes, shrivelled grapes, ≈ 5 hl/ha.' + L('https://www.plaimont.com/en', 'plaimont.com')),
    ('clav_gce', 'Grand Cru & Étiquette, « Qu’est-ce que le vin jaune du Jura ? Les secrets de Château-Chalon » (équivalence 1 l → 62 cl classée parmi les traditions orales par Claude Royer ; chauveau ; bouteille anglaise de ≈ 65 cl ; dérogation européenne).' + L('https://www.grandcruandetiquette.com/journal/vin-jaune-jura-chateau-chalon', 'grandcruandetiquette.com'),
                 'Grand Cru & Étiquette, “What is Jura vin jaune? The secrets of Château-Chalon” (the 1 l → 62 cl equivalence filed among oral traditions by Claude Royer; chauveau; ≈ 65 cl English bottle; EU exemption).' + L('https://www.grandcruandetiquette.com/journal/vin-jaune-jura-chateau-chalon', 'grandcruandetiquette.com')),
    ('clav_jw', 'Jura Wine (W. Stevens), « Vin Jaune » : bouteille « dite anglaise », commande des vignerons de Château-Chalon à La Vieille-Loye au XVIII<sup>e</sup> siècle, 30 bouteilles au sceau de l’abbé Clavelin en 1914.' + L('https://jurawine.co.uk/the-wines/vin-jaune/', 'jurawine.co.uk'),
                'Jura Wine (W. Stevens), “Vin Jaune”: the “so-called English” bottle, Château-Chalon growers’ 18th-century order from La Vieille-Loye, 30 bottles with abbot Clavelin’s seal in 1914.' + L('https://jurawine.co.uk/the-wines/vin-jaune/', 'jurawine.co.uk')),
    ('clav_blog', 'Le Blog du Sommelier, « Pourquoi 62 cl pour la bouteille de vin jaune ? » (2012) : l’explication par l’évaporation, « invention commode » ; clavelin d’usage au début du XX<sup>e</sup> siècle selon un vigneron jurassien.' + L('https://www.sommelier-vins.com/2012/11/pourquoi-62-cl-pour-la-bouteille-de-vin-jaune/', 'sommelier-vins.com'),
                  'Le Blog du Sommelier, “Why 62 cl for the vin jaune bottle?” (2012): the evaporation story as a “convenient invention”; clavelin in use from the early 20th century according to a Jura grower (in French).' + L('https://www.sommelier-vins.com/2012/11/pourquoi-62-cl-pour-la-bouteille-de-vin-jaune/', 'sommelier-vins.com')),
    ('sotolon', 'Pham T.T., Guichard E., Schlich P., Charpentier C. (1995). Optimal conditions for the formation of sotolon from α-ketobutyric acid in the French “Vin Jaune”. <i>Journal of Agricultural and Food Chemistry</i> 43 : 2616–2619.' + L('https://hal.inrae.fr/hal-02709893', 'hal'),
                'Pham T.T., Guichard E., Schlich P., Charpentier C. (1995). Optimal conditions for the formation of sotolon from α-ketobutyric acid in the French “Vin Jaune”. <i>Journal of Agricultural and Food Chemistry</i> 43: 2616–2619.' + L('https://hal.inrae.fr/hal-02709893', 'hal')),
    ('savagnin', 'Ramos-Madrigal J. <i>et al.</i> (2019). Palaeogenomic insights into the origins of French grapevine diversity. <i>Nature Plants</i> 5 : 595–603 (pépin médiéval d’Orléans = Savagnin).' + L('https://doi.org/10.1038/s41477-019-0437-5', 'doi'),
                 'Ramos-Madrigal J. <i>et al.</i> (2019). Palaeogenomic insights into the origins of French grapevine diversity. <i>Nature Plants</i> 5: 595–603 (medieval Orléans seed = Savagnin).' + L('https://doi.org/10.1038/s41477-019-0437-5', 'doi')),
    ('percee', 'Comité interprofessionnel des vins du Jura (CIVJ) et Gîtes de France, « Château-Chalon » : la Percée du vin jaune, fête annuelle de la mise en perce du nouveau millésime, organisée depuis 1997 dans un village différent chaque premier week-end de février.' + L('https://www.gites-de-france.com/fr/chateau-chalon', 'gites-de-france.com'),
               'Jura Wine Interprofessional Committee (CIVJ) and Gîtes de France, “Château-Chalon”: the Percée du vin jaune, the yearly broaching of the new vintage, held since 1997 in a different village on the first weekend of February.' + L('https://www.gites-de-france.com/en/chateau-chalon', 'gites-de-france.com')),
]
NUM = {k: i + 1 for i, (k, _, _) in enumerate(SOURCES)}


def r(*keys):
    return '<sup class="ref">' + ','.join(f'<a href="#src-{NUM[k]}">{NUM[k]}</a>' for k in keys) + '</sup>'


# ------------------------------------------------------------------ grapes from the Cépages data
_AOCS = {a['name']: a for a in cep.parse_all()}
EN_COLOUR = {'Blanc': 'Blanc', 'Noir': 'Noir'}


def grapes_of(dsl, labels=None):
    """Grape list for an AOC from the Cépages DSL; `labels` = substrings selecting the wine lines."""
    a = _AOCS[dsl]
    seen, out = set(), []
    for w in a['wines']:
        if labels and not any(s.lower() in w['label'].lower() for s in labels):
            continue
        for g in w['grapes']:
            if g['id'] in seen:
                continue
            seen.add(g['id'])
            out.append((cep.display(g['key'], g['code']), g['role'], g['adapt'], g['key'], g['code']))
    assert out, (dsl, labels)
    order = {'P': 0, '': 0, 'C': 1, 'A': 2}
    out.sort(key=lambda x: (order.get(x[1], 0), x[2]))
    return out


def grapes_html(gs):
    chips = []
    for name, role, adapt, _, _ in gs:
        cls = {'C': 'c', 'A': 'a'}.get(role, 'p')
        if adapt:
            cls = 'a ad'
        chips.append(f'<span class="gr {cls}">{name}</span>')
    return '<div class="grs">' + ''.join(chips) + '</div>'


# ------------------------------------------------------------------ families
# key: (FR, EN, colour token)
FAM = {
    'bot': ('Pourriture noble', 'Noble rot', 'bot'),
    'pas': ('Passerillage sur souche', 'Dried on the vine', 'pas'),
    'vt': ('Vendanges tardives · SGN', 'Late harvest · SGN', 'vt'),
    'pai': ('Vin de paille', 'Straw wine', 'pai'),
    'vdn': ('Vin doux naturel', 'Vin doux naturel', 'vdn'),
    'vdl': ('Vin de liqueur', 'Liqueur wine', 'vdl'),
    'ran': ('Rancio', 'Rancio', 'ran'),
    'bul': ('Bulles douces', 'Sweet bubbles', 'bul'),
    'jau': ('Vin jaune', 'Vin jaune', 'jau'),
}

# ------------------------------------------------------------------ the AOCs
# Each entry: slug, name, region (FR, EN), families, dsl (name, labels), numbers [(FR label, EN label, value FR, value EN)],
#             note (FR, EN), rs = minimum residual sugar used by the chart (g/l) or None, src keys
R = lambda fr, en=None: (fr, en or fr)  # noqa: E731
MUST = ('Raisins à la vendange', 'Grapes at harvest')
RS = ('Sucres du vin fini', 'Sugar in the finished wine')
TAV = ('Alcool', 'Alcohol')


def n(lab, fr, en=None):
    return (lab[0], lab[1], fr, en or fr)


AOC = []


def aoc(slug, name, region, fams, dsl, nums, note, rs=None, src=('inao',), sec=None):
    AOC.append(dict(slug=slug, name=name, region=region, fams=fams, dsl=dsl, nums=nums, note=note, rs=rs, src=src, sec=sec or fams[0]))


BX, SO, LO, AL, JU, RH, RO, LA, CO, CH = (R('Bordeaux'), R('Sud-Ouest', 'South-West'), R('Val de Loire', 'Loire Valley'), R('Alsace'),
                                          R('Jura'), R('Vallée du Rhône', 'Rhône Valley'), R('Roussillon'), R('Languedoc'), R('Corse', 'Corsica'),
                                          R('Charentes'))

# --- 1. noble rot & over-ripeness on the vine — Bordeaux
aoc('sauternes', 'Sauternes', BX, ['bot'], ('Sauternes', None),
    [n(MUST, '≥ 221 g/l'), n(RS, '≥ 45 g/l')],
    ('Pourriture noble obligatoire, vendange manuelle par tries successives ; tout traitement anti-botrytis est interdit dans les vignes.',
     'Noble rot required, hand-picked in successive passes (<i>tries</i>); anti-botrytis sprays are banned in the vineyard.'), 45, ('sauternes',))
aoc('barsac', 'Barsac', BX, ['bot'], ('Barsac', None),
    [n(MUST, '≥ 221 g/l'), n(RS, '≥ 45 g/l')],
    ('Mêmes règles que Sauternes ; les vins de Barsac peuvent aussi être vendus sous le nom « Sauternes ».',
     'Same rules as Sauternes; Barsac wines may also be sold under the Sauternes name.'), 45, ('sauternes',))
aoc('cerons', 'Cérons', BX, ['bot', 'pas'], ('Cérons', None),
    [n(MUST, '≥ 221 g/l'), n(RS, '≥ 45 g/l')],
    ('Raisins botrytisés et/ou passerillés sur souche, tries successives manuelles.', 'Botrytised and/or vine-dried grapes, successive hand-picked passes.'), 45, ('bdx_sweet',))
aoc('loupiac', 'Loupiac', BX, ['bot', 'pas'], ('Loupiac', None),
    [n(MUST, '≥ 238 g/l (sémillon)', '≥ 238 g/l (Sémillon)'), n(RS, '≥ 45 g/l')],
    ('Rive droite de la Garonne, face à Barsac ; botrytis et/ou passerillage, tries manuelles.', 'Right bank of the Garonne, opposite Barsac; botrytis and/or vine-drying, hand-picked passes.'), 45, ('bdx_sweet',))
aoc('sainte-croix', 'Sainte-Croix-du-Mont', BX, ['bot', 'pas'], ('Sainte-Croix-du-Mont', None),
    [n(MUST, '≥ 238 g/l (sémillon), 229 (autres)', '≥ 238 g/l (Sémillon), 229 (others)'), n(RS, '≥ 45 g/l')],
    ('Coteaux calcaires au-dessus de la Garonne ; tries successives manuelles.', 'Limestone slopes above the Garonne; successive hand-picked passes.'), 45, ('bdx_sweet',))
aoc('cadillac', 'Cadillac', BX, ['bot', 'pas'], ('Cadillac', None),
    [n(MUST, '≥ 255 g/l'), n(RS, '≥ 51 g/l'), n(TAV, '≥ 12 %')],
    ('Le plus exigeant des liquoreux de la rive droite : pourriture noble et/ou passerillage, tries manuelles.', 'The most demanding sweet wine of the right bank: noble rot and/or vine-drying, hand-picked passes.'), 51, ('bdx_sweet',))
aoc('premieres-cotes', 'Premières Côtes de Bordeaux', BX, ['bot'], ('Premières Côtes de Bordeaux', None),
    [n(MUST, '≥ 221 g/l'), n(RS, '≥ 34 g/l'), n(TAV, '≥ 11,5 %', '≥ 11.5%')],
    ('Blancs moelleux uniquement (les rouges relèvent désormais des Côtes de Bordeaux).', 'Sweet whites only (the reds now belong to Côtes de Bordeaux).'), 34, ('bdx_sweet',))
aoc('saint-macaire', 'Côtes de Bordeaux-Saint-Macaire', BX, ['bot'], ('Côtes de Bordeaux Saint-Macaire', None),
    [n(RS, 'moelleux 34–45 g/l · liquoreux > 45 g/l', 'moelleux 34–45 g/l · liquoreux > 45 g/l')],
    ('Secs, moelleux ou liquoreux ; les liquoreux viennent de raisins à pourriture noble récoltés à la main par tries.', 'Dry, medium-sweet or sweet; the sweet ones come from nobly rotten grapes picked by hand in passes.'), 34, ('bdx_sweet',))
aoc('graves-sup', 'Graves supérieures', BX, ['bot', 'pas'], ('Graves Supérieures', None),
    [n(MUST, '≥ 221 g/l')],
    ('Blancs avec sucres résiduels, raisins surmûris (pourriture noble et/ou passerillage), tries manuelles ; autour du sémillon.', 'Whites with residual sugar from over-ripe grapes (noble rot and/or vine-drying), hand-picked passes; built on Sémillon.'), None, ('bdx_sweet',))
aoc('cdb-sweet', 'Côtes de Bordeaux (Francs, Sainte-Foy)', BX, ['bot', 'pas'], ('Côtes de Bordeaux', ['Blanc']),
    [n(MUST, 'Sainte-Foy : moelleux 221, liquoreux 255 g/l', 'Sainte-Foy: moelleux 221, liquoreux 255 g/l')],
    ('Seules les dénominations Francs (liquoreux) et Sainte-Foy (moelleux et liquoreux) produisent des blancs doux ; tries manuelles.', 'Only the Francs (sweet) and Sainte-Foy (medium-sweet and sweet) denominations make sweet whites; hand-picked passes.'), None, ('bdx_sweet',))
aoc('bdx-sup', 'Bordeaux supérieur (blanc)', BX, ['bot'], ('Bordeaux Supérieur', ['Blanc']),
    [n(MUST, '≥ 195 g/l'), n(RS, '> 17 g/l')],
    ('Le Bordeaux supérieur blanc est toujours un vin avec sucres résiduels (moelleux).', 'White Bordeaux supérieur is always a wine with residual sugar (medium-sweet).'), 17, ('bdx_sweet',))

# --- South-West
aoc('monbazillac', 'Monbazillac', SO, ['bot', 'vt'], ('Monbazillac', None),
    [n(MUST, '≥ 221 g/l · SGN ≥ 255'), n(RS, '> 45 g/l · SGN > 85')],
    ('Surmaturité avec ou sans pourriture noble, tries manuelles. Mention « sélection de grains nobles » : élevage jusqu’au 1<sup>er</sup> juin de la 2<sup>e</sup> année.',
     'Over-ripeness with or without noble rot, hand-picked passes. “Sélection de grains nobles”: aged until 1 June of the 2nd year.'), 45, ('so_sweet',))
aoc('saussignac', 'Saussignac', SO, ['bot', 'pas'], ('Saussignac', None),
    [n(MUST, '≥ 272 g/l'), n(RS, '> 68 g/l')],
    ('Pourriture noble ou passerillage naturel, tries manuelles : l’un des seuils les plus élevés de France.', 'Noble rot or natural vine-drying, hand-picked passes: one of the highest thresholds in France.'), 68, ('so_sweet',))
aoc('haut-montravel', 'Haut-Montravel', SO, ['bot'], ('Haut-Montravel', None),
    [n(RS, '> 85 g/l')],
    ('Tries manuelles ; la cryoextraction (sous −5 °C) et les tunnels de passerillage sont interdits.', 'Hand-picked passes; cryo-extraction (below −5 °C) and drying tunnels are banned.'), 85, ('so_sweet',))
aoc('cotes-montravel', 'Côtes de Montravel', SO, ['bot'], ('Côtes de Montravel', None),
    [n(RS, '25–54 g/l')], ('Moelleux.', 'Medium-sweet.'), 25, ('so_sweet',))
aoc('rosette', 'Rosette', SO, ['bot'], ('Rosette', None),
    [n(RS, '25–51 g/l')], ('Petit moelleux des coteaux au nord de Bergerac.', 'A small medium-sweet appellation on the slopes north of Bergerac.'), 25, ('so_sweet',))
aoc('cotes-bergerac', 'Côtes de Bergerac (blanc)', SO, ['bot'], ('Côtes de Bergerac', ['Blanc']),
    [n(RS, '> 4 g/l')], ('Blancs moelleux ; au-delà de 54 g/l, aucun enrichissement n’est permis.', 'Medium-sweet whites; above 54 g/l no enrichment is allowed.'), None, ('so_sweet',))
aoc('cotes-duras', 'Côtes de Duras (blanc moelleux)', SO, ['bot'], ('Côtes de Duras', ['Blanc']),
    [n(RS, '> 12 g/l')], ('À côté des blancs secs, l’AOC produit des blancs moelleux.', 'Besides dry whites, the AOC makes medium-sweet whites.'), None, ('so_sweet',))
aoc('jurancon', 'Jurançon', SO, ['pas', 'vt'], ('Jurançon', None),
    [n(MUST, '≥ 247 g/l (petit manseng) · VT ≥ 281', '≥ 247 g/l (Petit Manseng) · VT ≥ 281'), n(RS, '> 40 g/l · VT > 55')],
    ('Passerillage sur souche des mansengs, tries successives. « Vendanges tardives » : petit et gros manseng seuls, récoltés à partir du 2 novembre.',
     'The Mansengs shrivel on the vine, picked in successive passes. “Vendanges tardives”: Petit and Gros Manseng only, picked from 2 November.'), 40, ('so_sweet',))
aoc('pacherenc', 'Pacherenc du Vic-Bilh', SO, ['pas'], ('Pacherenc du Vic-Bilh', ['moelleux']),
    [n(MUST, '≥ 238 g/l (petit manseng)', '≥ 238 g/l (Petit Manseng)'), n(RS, '≥ 45 g/l')],
    ('Même aire que Madiran ; vendange manuelle, petit manseng récolté par tries successives.', 'Same area as Madiran; hand harvest, Petit Manseng picked in successive passes.'), 45, ('so_sweet',))
aoc('gaillac', 'Gaillac (doux, vendanges tardives)', SO, ['pas', 'vt'], ('Gaillac', ['Blanc', 'Vendanges']),
    [n(MUST, 'doux ≥ 204 g/l · VT ≥ 280', 'doux ≥ 204 g/l · VT ≥ 280'), n(RS, 'doux ≥ 45 · VT ≥ 100 g/l')],
    ('Passerillage naturel sous le vent d’Autan ou pourriture noble ; les vendanges tardives (len de l’el, ondenc) sont récoltées par tries manuelles.',
     'Natural drying in the Autan wind or noble rot; late-harvest wines (Len de l’El, Ondenc) are picked by hand in passes.'), 45, ('so_sweet',))

# --- Loire
aoc('layon', 'Coteaux du Layon', LO, ['bot', 'pas', 'vt'], ('Coteaux du Layon', None),
    [n(MUST, 'Chaume 1<sup>er</sup> cru ≥ 272 · SGN ≥ 323 g/l', 'Chaume premier cru ≥ 272 · SGN ≥ 323 g/l'), n(RS, '≥ 34 g/l')],
    ('Chenin surmûri sur pied, avec ou sans pourriture noble, tries manuelles. Noms de commune possibles, « premier cru Chaume », mention « sélection de grains nobles ».',
     'Chenin over-ripened on the vine, with or without noble rot, hand-picked passes. Commune names allowed, “premier cru Chaume”, “sélection de grains nobles”.'), 34, ('loire_sweet',))
aoc('quarts', 'Quarts de Chaume grand cru', LO, ['bot', 'pas'], ('Quarts de Chaume', None),
    [n(MUST, '≥ 298 g/l'), n(RS, '> 85 g/l')],
    ('Seul « grand cru » de la Loire ; tries successives manuelles.', 'The Loire’s only “grand cru”; successive hand-picked passes.'), 85, ('loire_sweet',))
aoc('bonnezeaux', 'Bonnezeaux', LO, ['bot', 'pas'], ('Bonnezeaux', None),
    [n(RS, '≥ 51 g/l')], ('Chenin, tries successives manuelles.', 'Chenin, successive hand-picked passes.'), 51, ('loire_sweet',))
aoc('aubance', 'Coteaux de l’Aubance', LO, ['bot', 'pas', 'vt'], ('Coteaux de l\'Aubance', None),
    [n(MUST, 'SGN ≥ 323 g/l'), n(RS, '≥ 34 g/l')],
    ('Tries manuelles ; mention « sélection de grains nobles » (pourriture noble sur souche, élevage jusqu’au 1<sup>er</sup> juin de la 2<sup>e</sup> année).',
     'Hand-picked passes; “sélection de grains nobles” (noble rot on the vine, aged until 1 June of the 2nd year).'), 34, ('loire_sweet',))
aoc('saumur-coteaux', 'Coteaux de Saumur', LO, ['bot', 'pas'], ('Coteaux de Saumur', None),
    [n(RS, '≥ 34 g/l')], ('Chenin du tuffeau saumurois, tries successives manuelles.', 'Chenin from Saumur’s tuffeau, successive hand-picked passes.'), 34, ('loire_sweet',))
aoc('anjou-cdl', 'Anjou-Coteaux de la Loire', LO, ['bot', 'pas'], ('Anjou Coteaux de la Loire', None),
    [n(RS, '≥ 34 g/l')], ('Rive gauche de la Loire, brumes matinales favorables à la pourriture noble ; tries manuelles.', 'Left bank of the Loire, morning mists that favour noble rot; hand-picked passes.'), 34, ('loire_sweet',))
aoc('vouvray', 'Vouvray · Montlouis · Jasnières · Coteaux du Loir · Savennières', LO, ['bot', 'pas'], ('Vouvray', None),
    [n(RS, 'sec ≤ 8 g/l… jusqu’au doux selon le millésime', 'dry ≤ 8 g/l… up to doux depending on the vintage')],
    ('Ces chenins sont secs les années fraîches et demi-secs, moelleux ou doux les grandes années : la mention de sucre figure sur l’étiquette. Aucun enrichissement au-delà de 8–12 g/l.',
     'These Chenins are dry in cool years and demi-sec, moelleux or doux in great years: the sugar term is on the label. No enrichment above 8–12 g/l.'), None, ('loire_sweet',))

# --- Alsace
aoc('alsace-vt', 'Alsace · Alsace grand cru — VT et SGN', AL, ['vt', 'bot'], ('Alsace', ['Vendanges']),
    [n(('VT', 'VT'), 'gewurztraminer, pinot gris ≥ 270 g/l · riesling, muscats ≥ 244', 'Gewurztraminer, Pinot Gris ≥ 270 g/l · Riesling, Muscats ≥ 244'),
     n(('SGN', 'SGN'), '≥ 306 g/l · ≥ 276', '≥ 306 g/l · ≥ 276')],
    ('Quatre cépages seulement, aucun enrichissement, élevage jusqu’au 1<sup>er</sup> juin de la 2<sup>e</sup> année. La SGN exige des grains atteints de pourriture noble.',
     'Four grape varieties only, no enrichment, aged until 1 June of the 2nd year. SGN requires nobly rotten berries.'), None, ('alsace',), sec='vt')

# --- straw wines
aoc('jura-paille', 'Arbois · Côtes du Jura · L’Étoile — vin de paille', JU, ['pai'], ('Arbois', ['paille']),
    [n(('Séchage', 'Drying'), '≥ 6 semaines, sans chauffage', '≥ 6 weeks, no heating'), n(MUST, '320–420 g/l au pressurage', '320–420 g/l at pressing'),
     n(('Élevage', 'Ageing'), 'jusqu’au 15 nov. de la 3<sup>e</sup> année, dont 18 mois sous bois', 'until 15 Nov. of the 3rd year, incl. 18 months in wood')],
    ('Grappes séchées sur lits de paille, sur claies ou suspendues dans un local aéré ; mise en marché à partir du 1<sup>er</sup> décembre de la 3<sup>e</sup> année. L’Étoile n’utilise pas le trousseau.',
     'Bunches dried on straw, on racks or hanging in an airy room; released from 1 December of the 3rd year. L’Étoile does not use Trousseau.'), None, ('paille',))
aoc('hermitage-paille', 'Hermitage — vin de paille', RH, ['pai'], ('Hermitage', ['paille']),
    [n(('Séchage', 'Drying'), '≥ 45 jours', '≥ 45 days'), n(MUST, '> 350 g/l au pressurage', '> 350 g/l at pressing'), n(('Rendement', 'Yield'), '15 hl/ha')],
    ('Marsanne et roussanne passerillées hors souche, sur paille ou claies.', 'Marsanne and Roussanne dried off the vine, on straw or racks.'), None, ('paille',))
aoc('correze-paille', 'Corrèze — vin de paille', SO, ['pai'], ('Corrèze', ['paille']),
    [n(('Rendement', 'Yield'), '20 hl/ha')],
    ('Raisins récoltés à la main puis passerillés hors souche ; rouges et blancs.', 'Grapes picked by hand then dried off the vine; red and white.'), None, ('paille',))

# --- VDN
VDN_RULE = ('Mutage', 'Fortification')
aoc('rivesaltes', 'Rivesaltes', RO, ['vdn', 'ran'], ('Rivesaltes', None),
    [n(MUST, '≥ 252 g/l'), n(RS, '≥ 45 g/l'), n(TAV, '≥ 15 % acquis', '≥ 15% actual')],
    ('Ambré, grenat, rosé ou tuilé (obligatoire), hors d’âge et rancio (facultatifs). La plus vaste AOC de vins doux naturels, Aude et Pyrénées-Orientales.',
     'Ambré, grenat, rosé or tuilé (compulsory), hors d’âge and rancio (optional). The largest vin doux naturel AOC, in the Aude and Pyrénées-Orientales.'), 45, ('rivesaltes',))
aoc('banyuls', 'Banyuls', RO, ['vdn', 'ran'], ('Banyuls', None),
    [n(MUST, '≥ 252 g/l'), n(RS, '≥ 45 g/l')],
    ('Terrasses de schiste de la Côte Vermeille. Blanc, rosé, rimage (muté sur grains), ambré ou traditionnel ; hors d’âge, rancio.',
     'Schist terraces of the Côte Vermeille. Blanc, rosé, rimage (fortified on the skins), ambré or traditionnel; hors d’âge, rancio.'), 45, ('banyuls',))
aoc('banyuls-gc', 'Banyuls grand cru', RO, ['vdn', 'ran'], ('Banyuls Grand Cru', None),
    [n(('Grenache noir', 'Grenache Noir'), '≥ 75 %', '≥ 75%'), n(('Élevage', 'Ageing'), 'en bois jusqu’au 1<sup>er</sup> juin de la 3<sup>e</sup> année', 'in wood until 1 June of the 3rd year')],
    ('Rouge uniquement, vendange égrappée macérée au moins 5 jours.', 'Red only, destemmed grapes macerated for at least 5 days.'), 45, ('banyuls',))
aoc('maury', 'Maury', RO, ['vdn', 'ran'], ('Maury', ['VDN']),
    [n(MUST, '≥ 252 g/l'), n(RS, '≥ 45 g/l')],
    ('Ambré, blanc, grenat ou tuilé ; hors d’âge, rancio. L’AOC produit aussi des rouges secs.', 'Ambré, blanc, grenat or tuilé; hors d’âge, rancio. The AOC also makes dry reds.'), 45, ('vdn_other',))
aoc('grand-roussillon', 'Grand Roussillon', RO, ['vdn', 'ran'], ('Grand Roussillon', None),
    [n(MUST, '≥ 252 g/l'), n(RS, '≥ 45 g/l')],
    ('Aire commune aux VDN du Roussillon ; mention rancio possible. Devenu très rare.', 'Area shared by the Roussillon VDNs; rancio allowed. Now very rare.'), 45, ('vdn_other',))
aoc('rasteau', 'Rasteau (vin doux naturel)', RH, ['vdn', 'ran'], ('Rasteau', ['VDN']),
    [n(MUST, '≥ 252 g/l'), n(RS, '≥ 45 g/l')],
    ('Le grand VDN de grenache du Rhône : ambré, blanc, grenat, rosé, tuilé ; hors d’âge, rancio.', 'The Rhône’s great Grenache VDN: ambré, blanc, grenat, rosé, tuilé; hors d’âge, rancio.'), 45, ('vdn_other',))
aoc('muscat-rivesaltes', 'Muscat de Rivesaltes', RO, ['vdn'], ('Muscat de Rivesaltes', None),
    [n(MUST, '≥ 252 g/l'), n(RS, '≥ 100 g/l')], ('Muscat à petits grains et muscat d’Alexandrie.', 'Muscat à Petits Grains and Muscat of Alexandria.'), 100, ('muscats',))
aoc('frontignan', 'Muscat de Frontignan', LA, ['vdn', 'vdl'], ('Muscat de Frontignan', None),
    [n(MUST, 'VDN ≥ 252 · VDL ≥ 234 g/l'), n(RS, 'VDN ≥ 110 · VDL ≥ 185 g/l')],
    ('Aussi appelé « Frontignan » ou « vin de Frontignan » ; seule AOC à produire à la fois un VDN et un vin de liqueur (muté avant toute fermentation). Muscat blanc ou rouge, jamais assemblés.',
     'Also called “Frontignan” or “vin de Frontignan”; the only AOC making both a VDN and a liqueur wine (fortified before any fermentation). White or red Muscat, never blended.'), 110, ('muscats',))
aoc('lunel', 'Muscat de Lunel', LA, ['vdn'], ('Muscat de Lunel', None),
    [n(MUST, '≥ 252 g/l'), n(RS, '≥ 110 g/l')], ('Mention « Muscat de Noël » pour le vin de l’année, mis en bouteille par le producteur.', '“Muscat de Noël” for the new wine of the year, bottled by the grower.'), 110, ('muscats',))
aoc('mireval', 'Muscat de Mireval', LA, ['vdn'], ('Muscat de Mireval', None),
    [n(MUST, '≥ 252 g/l'), n(RS, '≥ 110 g/l')], ('Entre étang de Thau et massif de la Gardiole.', 'Between the Thau lagoon and the Gardiole hills.'), 110, ('muscats',))
aoc('st-jean', 'Muscat de Saint-Jean-de-Minervois', LA, ['vdn'], ('Muscat de Saint-Jean-de-Minervois', None),
    [n(MUST, '≥ 252 g/l'), n(RS, '≥ 125 g/l')], ('Plateau calcaire à ≈ 250 m d’altitude ; le plus sucré des muscats ; mention « Muscat de Noël ».', 'Limestone plateau at ≈ 250 m; the sweetest of the Muscats; “Muscat de Noël” allowed.'), 125, ('muscats',))
aoc('beaumes', 'Muscat de Beaumes-de-Venise', RH, ['vdn'], ('Muscat de Beaumes-de-Venise', None),
    [n(MUST, '≥ 252 g/l'), n(RS, '≥ 100 g/l')], ('Muscat blanc et muscat rouge peuvent être plantés et assemblés ensemble.', 'White and red Muscat may be planted and blended together.'), 100, ('muscats',))
aoc('cap-corse', 'Muscat du Cap Corse', CO, ['vdn'], ('Muscat du Cap Corse', None),
    [n(MUST, '≥ 252 g/l'), n(RS, '≥ 90 g/l')], ('Muscat à petits grains seul, au nord de la Corse.', 'Muscat à Petits Grains only, in northern Corsica.'), 90, ('muscats',))

# --- VDL
aoc('pineau', 'Pineau des Charentes', CH, ['vdl'], ('Pineau des Charentes', None),
    [n(('Mutage', 'Fortified with'), 'Cognac de la même exploitation', 'Cognac from the same estate'), n(MUST, '> 170 g/l'), n(TAV, '16–22 %', '16–22%'),
     n(('Élevage', 'Ageing'), 'blanc 18 mois (12 en chêne) · vieux > 7 ans · très vieux > 12 ans', 'white 18 months (12 in oak) · vieux > 7 yrs · très vieux > 12 yrs')],
    ('Blanc, rosé (8 mois) ou rouge (12 mois). Bouteille de verre obligatoire avec timbre de garantie.', 'White, rosé (8 months) or red (12 months). Glass bottle with guarantee stamp compulsory.'), None, ('vdl',))
aoc('floc', 'Floc de Gascogne', SO, ['vdl'], ('Floc de Gascogne', None),
    [n(('Mutage', 'Fortified with'), 'Armagnac de la même exploitation (≥ 52 %)', 'Armagnac from the same estate (≥ 52%)'), n(MUST, '≥ 170 g/l'), n(TAV, '16–18 %', '16–18%')],
    ('Blanc (assemblage obligatoire) ou rosé ; élevage jusqu’au 1<sup>er</sup> mars, vente à partir du 15 mars.', 'White (always a blend) or rosé; aged until 1 March, on sale from 15 March.'), None, ('vdl',))
aoc('macvin', 'Macvin du Jura', JU, ['vdl'], ('Macvin du Jura', None),
    [n(('Mutage', 'Fortified with'), 'Marc du Jura ≥ 52 %, vieilli ≥ 14 mois en chêne', 'Marc du Jura ≥ 52%, aged ≥ 14 months in oak'), n(MUST, '≥ 153 g/l au mutage', '≥ 153 g/l at fortification'), n(TAV, '16–22 %', '16–22%')],
    ('Moûts mutés pendant les vendanges, puis au moins 10 mois en chêne ; vente à partir du 1<sup>er</sup> septembre.', 'Musts fortified during the harvest, then at least 10 months in oak; on sale from 1 September.'), None, ('vdl',))
aoc('clairette-lang', 'Clairette du Languedoc (vin de liqueur, rancio)', LA, ['vdl', 'ran'], ('Clairette du Languedoc', None),
    [n(TAV, '≥ 17 %', '≥ 17%'), n(RS, '9–40 g/l'), n(('Rancio', 'Rancio'), 'élevage jusqu’au 15 oct. de la 3<sup>e</sup> année', 'aged until 15 Oct. of the 3rd year')],
    ('Clairette seule, mutée en cours de fermentation ; la mention « Rancio » vient de raisins surmûris.', 'Clairette alone, fortified during fermentation; “Rancio” comes from over-ripe grapes.'), None, ('vdl',))

# --- sweet bubbles
aoc('die', 'Clairette de Die méthode ancestrale', RH, ['bul'], ('Clairette de Die', ['ancestrale']),
    [n(('Muscat', 'Muscat'), '≥ 75 %', '≥ 75%'), n(RS, '≥ 35 g/l'), n(('Pression', 'Pressure'), '≥ 3 bars', '≥ 3 bar')],
    ('Une seule fermentation, arrêtée en bouteille : le sucre du raisin reste dans le vin.', 'A single fermentation, finished in the bottle: the grape’s own sugar stays in the wine.'), 35, ('bulles',))
aoc('gaillac-anc', 'Gaillac méthode ancestrale', SO, ['bul'], ('Gaillac', ['ancestrale']),
    [n(RS, 'mention « doux » ≥ 50 g/l', '“doux” ≥ 50 g/l')], ('Mauzac blanc et rose, fermentation unique en bouteille.', 'White and pink Mauzac, single fermentation in bottle.'), None, ('bulles',))
aoc('blanquette-anc', 'Blanquette méthode ancestrale', LA, ['bul'], ('Blanquette méthode ancestrale', None),
    [], ('Mauzac de Limoux, la plus ancienne méthode de bulles du pays.', 'Mauzac from Limoux, the country’s oldest sparkling method.'), None, ('bulles',))
aoc('cerdon', 'Bugey Cerdon', R('Savoie-Bugey'), ['bul'], ('Bugey', ['Cerdon']),
    [], ('Rosé demi-sec de méthode ancestrale, gamay et poulsard.', 'Medium-dry rosé by the ancestral method, Gamay and Poulsard.'), None, ('bulles',))
aoc('champagne-doux', 'Champagne doux', R('Champagne'), ['bul'], ('Champagne', None),
    [n(RS, '> 50 g/l')], ('Le plus sucré des dosages, rare aujourd’hui ; le « demi-sec » (32–50 g/l) est plus courant.', 'The sweetest dosage, rare today; “demi-sec” (32–50 g/l) is more common.'), 50, ('bulles', 'ue2019'))

# --- vin jaune (AOCs listed in the bottom section)
JAUNE = [
    ('Château-Chalon', 'Décret n° 2011-1187', 'Decree No 2011-1187', '29 mai 1936', '29 May 1936', ('Uniquement du vin jaune ; 4 communes ; 30 hl/ha ; certaines années sont refusées (1974, 1980, 1984, 2001).', 'Vin jaune only; 4 communes; 30 hl/ha; some vintages are declined (1974, 1980, 1984, 2001).')),
    ('Arbois (et Arbois-Pupillin)', 'Décret n° 2011-1188', 'Decree No 2011-1188', '15 mai 1936', '15 May 1936', ('Mention « vin jaune » ; Pupillin est une dénomination complémentaire d’Arbois.', '“Vin jaune” mention; Pupillin is an additional denomination of Arbois.')),
    ('Côtes du Jura', 'Décret n° 2011-1189', 'Decree No 2011-1189', '31 juillet 1937', '31 July 1937', ('Mention « vin jaune » ; la plus vaste aire jurassienne.', '“Vin jaune” mention; the largest Jura area.')),
    ('L’Étoile', 'Décret n° 2011-1096, modifié 2013-143', 'Decree No 2011-1096, amended 2013-143', '31 juillet 1937', '31 July 1937', ('Mention « vin jaune » ; petite aire au nord de Lons-le-Saunier.', '“Vin jaune” mention; small area north of Lons-le-Saunier.')),
]

# ------------------------------------------------------------------ rendering helpers
def chips(fams):
    return ''.join(f'<span class="fam f-{FAM[f][2]}">{t((FAM[f][0], FAM[f][1]))}</span>' for f in fams)


def card(a):
    gs = grapes_of(*a['dsl'])
    nums = ''.join(f'<div><dt>{t((fr, en))}</dt><dd>{t((vf, ve))}</dd></div>' for fr, en, vf, ve in a['nums'])
    nums = f'<dl class="nums">{nums}</dl>' if nums else ''
    return (f'<article class="aoc" id="aoc-{a["slug"]}" data-fam="{" ".join(a["fams"])}">'
            f'<div class="aoc-top"><h4>{a["name"]}</h4>{t(a["region"], "span", "reg")}</div>'
            f'<div class="fams">{chips(a["fams"])}</div>{nums}'
            f'{blk((a["note"][0] + r(*a["src"]), a["note"][1] + r(*a["src"])), "p", "aoc-note")}'
            f'{grapes_html(gs)}</article>')


def cards(sec):
    return '<div class="aocs">' + ''.join(card(a) for a in AOC if a['sec'] == sec) + '</div>'


YEAST_BOX = (
    '<div class="panel yeast" id="levures">' + t(('Pourquoi les levures s’arrêtent-elles d’elles-mêmes ?', 'Why do the yeasts stop on their own?'), 'h3')
    + blk(('Dans un moût botrytisé, les levures travaillent dans des conditions de plus en plus hostiles. Plusieurs freins s’additionnent' + r('enology') + ' :',
           'In a botrytised must, yeasts work in increasingly hostile conditions. Several brakes add up' + r('enology') + ':'))
    + '<div class="ys">' + ''.join(
        f'<div class="y"><b>{t(h)}</b>{t(b, "p")}</div>' for h, b in [
            (('1 · Trop de sucre', '1 · Too much sugar'),
             ('Un moût à 300–400 g/l de sucre exerce une forte pression osmotique : il « aspire » l’eau des cellules de levure, qui se déshydratent et se multiplient mal. La fermentation démarre lentement et peut durer des semaines, voire des mois.',
              'A must with 300–400 g/l of sugar exerts strong osmotic pressure: it draws water out of the yeast cells, which dehydrate and multiply poorly. Fermentation starts slowly and can last weeks or even months.')),
            (('2 · L’alcool devient toxique', '2 · Alcohol becomes toxic'),
             ('L’alcool que les levures produisent abîme leurs propres membranes. Plus il monte, plus elles ralentissent ; vers 13–15 %, la plupart cessent de fermenter alors qu’il reste encore beaucoup de sucre.',
              'The alcohol the yeasts produce damages their own membranes. The higher it climbs, the slower they work; around 13–15%, most stop fermenting while plenty of sugar remains.')),
            (('3 · Le botrytis a tout mangé', '3 · The botrytis ate everything'),
             ('Le champignon a consommé une grande partie de l’azote et des vitamines du raisin, surtout la <b>thiamine</b> (vitamine B1), dont les levures ont besoin pour vivre. Elles manquent de nourriture.',
              'The fungus has used up much of the grape’s nitrogen and vitamins, above all <b>thiamine</b> (vitamin B1), which yeasts need to live. They run short of food.')),
            (('4 · Un frein chimique', '4 · A chemical brake'),
             ('Le botrytis sécrète aussi une substance qui gêne la fermentation, appelée <b>botryticine</b> par les œnologues bordelais.',
              'Botrytis also secretes a substance that hinders fermentation, named <b>botryticine</b> by Bordeaux oenologists.')),
        ]) + '</div>'
    + blk(('<b>Le vigneron arrête la course.</b> En pratique, la fermentation ne s’arrête pas toujours pile au bon équilibre. Quand le rapport alcool/sucre recherché est atteint, le vigneron la bloque lui-même : il refroidit le vin, ajoute du dioxyde de soufre (SO<sub>2</sub>), puis le soutire ou le filtre pour éliminer les levures. C’est pourquoi les liquoreux contiennent plus de SO<sub>2</sub> que les vins secs : il empêche le sucre restant de refermenter en bouteille' + r('enology') + '.',
           '<b>The grower ends the race.</b> In practice, fermentation does not always stop exactly at the right balance. When the desired alcohol/sugar ratio is reached, the grower stops it: chilling the wine, adding sulphur dioxide (SO<sub>2</sub>), then racking or filtering out the yeasts. That is why sweet wines contain more SO<sub>2</sub> than dry ones: it keeps the remaining sugar from re-fermenting in the bottle' + r('enology') + '.'), 'p', 'y-end')
    + '</div>')


def method(id_, kick, title, lead, steps, sec, extra=''):
    st = ''.join(f'<li><b>{t(h)}</b> {t(b)}</li>' for h, b in steps)
    return (f'<section class="sec" id="{id_}"><div class="sec-head">{t(kick, "p", "kick")}{t(title, "h2")}</div>'
            f'<div class="method"><div class="panel lede">{blk(lead)}</div>'
            f'<ol class="steps">{st}</ol></div>{extra}{cards(sec) if sec else ""}</section>')


# ------------------------------------------------------------------ static blocks
SUGAR_TERMS = [
    ('sec', '≤ 4 g/l', '(≤ 9 g/l si l’acidité suit)', '(≤ 9 g/l if acidity follows)'),
    ('demi-sec', '≤ 12 g/l', '(≤ 18 g/l si l’acidité suit)', '(≤ 18 g/l if acidity follows)'),
    ('moelleux', '≤ 45 g/l', '', ''),
    ('doux', '≥ 45 g/l', '', ''),
]


def sugar_terms_html():
    rows = ''.join(f'<div class="st"><b>{w}</b><span>{v}</span><small>{t((nf, ne))}</small></div>' for w, v, nf, ne in SUGAR_TERMS)
    return f'<div class="sts">{rows}</div>'


def paths_svg():
    """Diagram: the two ways to keep sugar in a wine."""
    fr = dict(t1='Concentrer le sucre dans le raisin', t2='Arrêter la fermentation : le mutage', g='Raisin',
              m=[('Pourriture noble', 'Botrytis cinerea perce la peau'), ('Passerillage sur souche', 'le raisin sèche au vent'),
                 ('Passerillage hors souche', 'sur paille ou sur claies'), ('Alcool neutre ≥ 96 %', 'ajouté au moût qui fermente'),
                 ('Eau-de-vie de la région', 'Cognac, Armagnac, marc')],
              o=[('Liquoreux, moelleux', 'les levures s’épuisent'), ('Vin de paille', ''), ('Vin doux naturel', 'VDN'), ('Vin de liqueur', 'VDL')])
    en = dict(t1='Concentrate the sugar in the grape', t2='Stop the fermentation: fortification', g='Grape',
              m=[('Noble rot', 'Botrytis cinerea pierces the skin'), ('Drying on the vine', 'the grape shrivels in the wind'),
                 ('Drying off the vine', 'on straw or racks'), ('Neutral spirit ≥ 96%', 'added to the fermenting must'),
                 ('Local brandy', 'Cognac, Armagnac, marc')],
              o=[('Sweet wine', 'the yeasts give up'), ('Straw wine', ''), ('Vin doux naturel', 'VDN'), ('Liqueur wine', 'VDL')])
    MY = [40, 98, 156, 262, 320]
    MC = ['bot', 'pas', 'pai', 'vdn', 'vdl']
    OY = [(69, 'h'), (156, 'pai'), (262, 'vdn'), (320, 'vdl')]
    LINK = [(0, 0), (1, 0), (2, 1), (3, 2), (4, 3)]

    def box(x, y, w, h, cls, l1, l2=''):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" class="nd {cls}"/>'
                f'<text x="{x + w / 2}" y="{y + (h / 2 - 3 if l2 else h / 2 + 5)}" class="tb">{l1}</text>'
                + (f'<text x="{x + w / 2}" y="{y + h / 2 + 14}" class="ts">{l2}</text>' if l2 else ''))

    def svg(s):
        out = [f'<svg viewBox="0 0 760 390" class="paths" role="img" aria-label="{s["t1"]} / {s["t2"]}">',
               '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 10 5 0 10z" class="ahf"/></marker></defs>',
               f'<text x="320" y="26" class="tt">{s["t1"]}</text><text x="320" y="248" class="tt">{s["t2"]}</text>',
               '<line x1="190" y1="226" x2="740" y2="226" class="sep"/>',
               box(20, 170, 110, 56, 'g', s['g'])]
        for i, (y, c) in enumerate(zip(MY, MC)):
            out.append(f'<path d="M130 198 C160 198 165 {y + 24} 195 {y + 24}" class="ar"/>')
            out.append(box(200, y, 240, 48, c, *s['m'][i]))
        out.append(box(520, 40, 220, 106, 'h', *s['o'][0]))
        for j in (1, 2, 3):
            out.append(box(520, OY[j][0], 220, 48, OY[j][1], *s['o'][j]))
        for mi, oj in LINK:
            y1 = MY[mi] + 24
            y2 = (MY[mi] + 24) if oj == 0 else OY[oj][0] + 24
            out.append(f'<path d="M440 {y1} L515 {y2}" class="ar"/>')
        out.append('</svg>')
        return ''.join(out)
    return f'<figure class="fig"><div class="L fr">{svg(fr)}</div><div class="L en">{svg(en)}</div></figure>'


def when_html():
    """Explains the two sugar figures found in the specs: grape must at harvest vs. finished wine."""
    def side(cls, step, title, body, ex):
        return (f'<div class="wh {cls}"><span class="wh-step">{t(step)}</span>{t(title, "b")}{t(body, "p")}{t(ex, "small")}</div>')
    a = side('wh-must', ('Avant · à la vendange', 'Before · at harvest'), ('Richesse en sucre des raisins', 'Sugar in the grapes'),
             ('Mesurée dans le jus (moût) des raisins cueillis, en grammes par litre de moût. Elle dit si le raisin est assez mûr, concentré ou passerillé pour avoir droit à l’AOC.',
              'Measured in the juice (must) of the picked grapes, in grams per litre of must. It tells whether the grapes are ripe, concentrated or dried enough to qualify for the AOC.'),
             ('Ex. : Sauternes ≥ 221 g/l · vins doux naturels ≥ 252 g/l · Quarts de Chaume ≥ 298 g/l', 'E.g. Sauternes ≥ 221 g/l · vins doux naturels ≥ 252 g/l · Quarts de Chaume ≥ 298 g/l'))
    b = side('wh-wine', ('Après · dans le vin fini', 'After · in the finished wine'), ('Sucres résiduels', 'Residual sugar'),
             ('Le sucre qui reste une fois la fermentation terminée (ou arrêtée par le mutage), contrôlé après fermentation, à la vente en vrac ou à la mise en bouteille. C’est lui qui fait le goût sucré — et c’est lui que montre le graphique.',
              'The sugar left once fermentation is over (or stopped by fortification), checked after fermentation, at bulk sale or at bottling. It is what makes the wine taste sweet — and it is what the chart shows.'),
             ('Ex. : Sauternes ≥ 45 g/l · vins doux naturels ≥ 45 g/l · Quarts de Chaume > 85 g/l', 'E.g. Sauternes ≥ 45 g/l · vins doux naturels ≥ 45 g/l · Quarts de Chaume > 85 g/l'))
    mid = ('<div class="wh-arrow" aria-hidden="true"><svg viewBox="0 0 60 24"><path d="M2 12h50M44 4l10 8-10 8" /></svg>'
           + t(('fermentation', 'fermentation'), 'small') + '</div>')
    foot = blk(('Entre les deux, les levures transforment le sucre en alcool (≈ 17 g/l de sucre pour 1 % d’alcool). Un Sauternes cueilli à ≈ 340 g/l dont la fermentation s’arrête vers 14 % (≈ 238 g/l transformés) garde ainsi ≈ 100 g/l de sucre. Les cartes des AOC donnent les deux chiffres quand le cahier des charges les fixe : « Raisins à la vendange » et « Sucres du vin fini ».',
                'In between, yeasts turn sugar into alcohol (≈ 17 g/l of sugar per 1% of alcohol). A Sauternes picked at ≈ 340 g/l whose fermentation stops around 14% (≈ 238 g/l converted) therefore keeps ≈ 100 g/l of sugar. The AOC cards give both figures when the specification sets them: “Grapes at harvest” and “Sugar in the finished wine”.'), 'p', 'note')
    return f'<div class="when">{a}{mid}{b}</div>{foot}'


def ladder_html():
    """Minimum residual sugar by AOC (g/l), from the specs."""
    rows = sorted([a for a in AOC if a['rs']], key=lambda a: (-a['rs'], a['name']))
    mx = 140
    out = []
    for a in rows:
        w = min(a['rs'], mx) / mx * 100
        fam = a['fams'][0]
        out.append(f'<a class="ld f-{FAM[fam][2]}" href="#aoc-{a["slug"]}"><span class="ld-n">{a["name"]}</span>'
                   f'<span class="ld-t"><span class="ld-b" style="width:{w:.1f}%"></span><span class="ld-v">{a["rs"]}</span></span></a>')
    ticks = ''.join(f'<span style="left:{v / mx * 100:.1f}%">{v}</span>' for v in (0, 25, 45, 75, 100, 125))
    return (f'<div class="ladder">{"".join(out)}<div class="ld axis"><span class="ld-n"></span><span class="ld-t ld-ticks">{ticks}</span></div></div>'
            + t(('Minimum légal de sucres résiduels (glucose + fructose, en grammes par litre de vin) mesuré dans le vin fini — après la fermentation, au stade de la vente en vrac ou de la mise en bouteille, selon le cahier des charges. Ce n’est pas le sucre du raisin à la vendange. Les grands millésimes vont souvent bien au-delà : un Sauternes dépasse couramment 100 g/l.',
                 'Legal minimum residual sugar (glucose + fructose, in grams per litre of wine) measured in the finished wine — after fermentation, at bulk sale or bottling, depending on the specification. It is not the sugar in the grape at harvest. Great vintages often go far beyond: a Sauternes commonly exceeds 100 g/l.'), 'p', 'note'))


def index_html():
    btns = '<button type="button" class="fb on" data-f="all">' + t(('Toutes', 'All')) + '</button>' + ''.join(
        f'<button type="button" class="fb f-{FAM[k][2]}" data-f="{k}">{t((FAM[k][0], FAM[k][1]))}</button>' for k in FAM if k != 'jau')
    items = ''.join(f'<a class="ix" data-fam="{" ".join(a["fams"])}" href="#aoc-{a["slug"]}">{a["name"]}{t(a["region"], "small")}</a>' for a in sorted(AOC, key=lambda a: a['name']))
    items += ''.join(f'<a class="ix" data-fam="jau" href="#jaune-aoc">{nm} {t(("— vin jaune", "— vin jaune"), "small")}</a>' for nm, *_ in JAUNE)
    ph = att('Chercher une AOC…')
    return (f'<div class="panel ixp"><div class="ix-bar"><input type="search" id="ixq" placeholder="{ph}" data-ph-fr="{ph}" data-ph-en="{att("Search an AOC…")}" aria-label="AOC">'
            f'<div class="fbs">{btns}</div></div><div class="ixs" id="ixs">{items}</div></div>')


VDN_MENTIONS = [
    # mention FR, EN explanation FR, EN, AOCs having it
    ('Blanc', 'Blanc', 'Moût séparé des peaux, élevage réducteur (à l’abri de l’air) au moins jusqu’au 1<sup>er</sup> mai suivant, dont 3 mois en bouteille.', 'Must separated from the skins, reductive ageing (away from air) until at least 1 May of the next year, incl. 3 months in bottle.', {'Banyuls', 'Maury', 'Rasteau'}),
    ('Rosé', 'Rosé', 'Couleur légère, mis en bouteille au plus tard le 31 décembre de l’année suivante.', 'Pale colour, bottled by 31 December of the following year.', {'Rivesaltes', 'Banyuls', 'Rasteau'}),
    ('Grenat', 'Grenat', 'Rouge jeune, élevage réducteur jusqu’au 30 avril/1<sup>er</sup> mai suivant, dont 3 mois en bouteille ; fruit rouge et noir.', 'Young red, reductive ageing until 30 April/1 May of the next year, incl. 3 months in bottle; red and black fruit.', {'Rivesaltes', 'Maury', 'Rasteau'}),
    ('Rimage', 'Rimage', 'Équivalent du grenat à Banyuls : grenache noir muté sur grains, élevage réducteur.', 'Banyuls’ equivalent of grenat: Grenache Noir fortified on the skins, reductive ageing.', {'Banyuls'}),
    ('Ambré', 'Ambré', 'Blanc élevé au contact de l’air : il prend une couleur ambrée et des notes de fruits secs.', 'White aged in contact with air: it turns amber and develops dried-fruit notes.', {'Rivesaltes', 'Banyuls', 'Maury', 'Rasteau'}),
    ('Tuilé', 'Tuilé', 'Rouge élevé au contact de l’air : sa couleur vire à la tuile (orangé-brun).', 'Red aged in contact with air: its colour turns brick (orange-brown).', {'Rivesaltes', 'Maury', 'Rasteau'}),
    ('Traditionnel', 'Traditionnel', 'Équivalent du tuilé à Banyuls (grenache noir ≥ 50 %, macération, élevage oxydatif).', 'Banyuls’ equivalent of tuilé (Grenache Noir ≥ 50%, maceration, oxidative ageing).', {'Banyuls'}),
    ('Hors d’âge', 'Hors d’âge', 'Ambré, tuilé ou traditionnel élevé jusqu’au 31 août/1<sup>er</sup> septembre de la 5<sup>e</sup> année suivant la récolte.', 'Ambré, tuilé or traditionnel aged until 31 August/1 September of the 5th year after the harvest.', {'Rivesaltes', 'Banyuls', 'Banyuls GC', 'Maury', 'Rasteau'}),
    ('Rancio', 'Rancio', 'Réservée aux vins qui ont acquis le « goût de rancio » au cours de l’élevage — aucune durée minimale n’est fixée.', 'Reserved for wines that have acquired the “rancio taste” during ageing — no minimum duration is set.', {'Rivesaltes', 'Banyuls', 'Banyuls GC', 'Maury', 'Rasteau', 'Grand Roussillon'}),
]
VDN_COLS = ['Rivesaltes', 'Banyuls', 'Banyuls GC', 'Maury', 'Rasteau', 'Grand Roussillon']


def vdn_matrix():
    head = '<tr><th></th>' + ''.join(f'<th>{c}</th>' for c in VDN_COLS) + '</tr>'
    rows = ''
    for mf, me, ef, ee, has in VDN_MENTIONS:
        cells = ''.join(f'<td class="{"y" if c in has else ""}">{"●" if c in has else ""}</td>' for c in VDN_COLS)
        rows += f'<tr><th>{t((mf, me), "b")}{t((ef, ee), "small")}</th>{cells}</tr>'
    return f'<div class="mx-wrap"><table class="mx">{head}{rows}</table></div>'


def grape_index():
    idx = {}
    for a in AOC:
        for name, role, adapt, key, code in grapes_of(*a['dsl']):
            if adapt:
                continue
            idx.setdefault(name, []).append(a)
    for nm, *_ in JAUNE:
        idx.setdefault('Savagnin Blanc', [])
    order = sorted(idx.items(), key=lambda kv: (-len(kv[1]), cep.strip_acc(kv[0])))
    out = []
    for g, aocs in order:
        links = ''.join(f'<a href="#aoc-{a["slug"]}">{a["name"]}</a>' for a in aocs)
        if g == 'Savagnin Blanc':
            links += '<a href="#jaune">' + t(('Vin jaune (4 AOC)', 'Vin jaune (4 AOCs)')) + '</a>'
        cnt = len(aocs) + (1 if g == 'Savagnin Blanc' else 0)
        out.append(f'<div class="gi"><div class="gi-h"><b>{g}</b><span>{cnt}</span></div><div class="gi-l">{links}</div></div>')
    return '<div class="gis">' + ''.join(out) + '</div>'


def clavelin_svg():
    # Reg. (EU) 2019/33, Annex VII: height ≈ 2.75 × base diameter, cylindrical part = half the height.
    d, H = 80, 220
    x0, y0 = 60, 20
    cyl = H / 2
    body_top = y0 + H - cyl
    neck_w, neck_h = 26, 46
    cx = x0 + d / 2
    path = (f'M{x0} {y0 + H} L{x0} {body_top} C{x0} {body_top - 34} {cx - neck_w / 2} {y0 + neck_h + 30} {cx - neck_w / 2} {y0 + neck_h} '
            f'L{cx - neck_w / 2} {y0 + 8} L{cx + neck_w / 2} {y0 + 8} L{cx + neck_w / 2} {y0 + neck_h} '
            f'C{cx + neck_w / 2} {y0 + neck_h + 30} {x0 + d} {body_top - 34} {x0 + d} {body_top} L{x0 + d} {y0 + H} Z')
    fill_y = body_top + 6
    return (f'<svg viewBox="40 0 220 275" class="clav" role="img" aria-label="Clavelin 62 cl">'
            f'<defs><clipPath id="cb"><path d="{path}"/></clipPath></defs>'
            f'<rect x="{x0 - 2}" y="{fill_y}" width="{d + 4}" height="{y0 + H - fill_y}" class="wine" clip-path="url(#cb)"/>'
            f'<path d="{path}" class="glass"/><rect x="{cx - neck_w / 2 - 2}" y="{y0}" width="{neck_w + 4}" height="12" rx="3" class="cap"/>'
            f'<line x1="{x0 + d + 18}" y1="{y0 + 8}" x2="{x0 + d + 18}" y2="{y0 + H}" class="dim"/>'
            f'<line x1="{x0 + d + 12}" y1="{body_top}" x2="{x0 + d + 24}" y2="{body_top}" class="dim"/>'
            f'<line x1="{x0}" y1="{y0 + H + 14}" x2="{x0 + d}" y2="{y0 + H + 14}" class="dim"/>'
            f'<text x="{x0 + d + 28}" y="{y0 + H / 2 - 30}" class="dt">≈ 2,75 × Ø</text>'
            f'<text x="{x0 + d + 28}" y="{body_top + cyl / 2}" class="dt">½</text>'
            f'<text x="{cx}" y="{y0 + H + 32}" class="dt c">Ø</text>'
            f'<text x="{cx}" y="{body_top + cyl / 2 + 6}" class="lbl">62 cl</text></svg>')


def angels_html():
    return ('<div class="angels"><div class="an-bar"><span class="an-fill" style="width:62%"></span><span class="an-gone" style="width:38%"></span></div>'
            '<div class="an-leg">' + t(('1 litre mis en fût', '1 litre put in the cask'), 'span') + t(('62 cl « restent » après ≈ 6 ans — selon la légende', '62 cl “remain” after ≈ 6 years — so the legend goes'), 'b')
            + t(('38 cl : la « part des anges »', '38 cl: the “angels’ share”'), 'span') + '</div></div>')


def timeline_html():
    pts = [('Vendange (année N)', 'Harvest (year N)', 0), ('Fermentation complète, soutirage', 'Full fermentation, racking', 8),
           ('≥ 60 mois sous voile, sans ouillage', '≥ 60 months under the veil, no topping up', 40),
           ('Fin d’élevage : 15 déc. N+6', 'End of ageing: 15 Dec. N+6', 86), ('Vente : 1<sup>er</sup> janv. N+7', 'On sale: 1 Jan. N+7', 100)]
    dots = ''.join(f'<div class="tl-p{" up" if i % 2 else ""}" style="left:{p}%"><span class="tl-d"></span>{t((fr, en), "small")}</div>' for i, (fr, en, p) in enumerate(pts))
    return f'<div class="tl"><div class="tl-bar"><span class="tl-veil" style="left:8%;width:78%"></span></div>{dots}</div>'


def jaune_table():
    rows = ''.join(f'<tr><th>{nm}</th><td>{t((df, de))}</td><td>{t((rf, re_))}</td><td>{t(note, "small")}</td></tr>' for nm, df, de, rf, re_, note in JAUNE)
    head = '<tr><th>AOC</th><th>' + t(('Texte en vigueur', 'Text in force')) + '</th><th>' + t(('Première reconnaissance', 'First recognised')) + '</th><th>' + t(('Particularités', 'Notes')) + '</th></tr>'
    return f'<div class="mx-wrap"><table class="jt">{head}{rows}</table></div>'


# ------------------------------------------------------------------ page sections
SECTIONS = []

SECTIONS.append(f'''<section class="sec" id="sucre">
  <div class="sec-head">{t(("01 · Comprendre le doux", "01 · Understanding sweetness"), "p", "kick")}{t(("D’où vient <em>le sucre ?</em>", "Where does <em>the sugar come from?</em>"), "h2")}</div>
  <div class="two">
    <div class="panel lede">{blk(("Un vin est doux quand une partie du sucre du raisin n’a pas été transformée en alcool. Il n’y a que <b>deux façons</b> d’y arriver : <b>concentrer</b> le sucre dans le raisin avant de le presser, pour que les levures s’épuisent avant la fin (pourriture noble, passerillage, vendanges tardives), ou <b>arrêter</b> la fermentation en ajoutant de l’alcool — c’est le <b>mutage</b>. Avec un alcool neutre de raisin, on obtient un <b>vin doux naturel</b> ; avec une eau-de-vie (Cognac, Armagnac, marc), un <b>vin de liqueur</b>" + r("ue1308", "inao") + ". L’ajout de sucre (chaptalisation) est interdit dans tous les vins doux d’AOC présentés ici.",
                                         "A wine is sweet when part of the grape’s sugar has not been turned into alcohol. There are only <b>two ways</b> to get there: <b>concentrate</b> the sugar in the grape before pressing, so the yeasts give up before the end (noble rot, drying, late harvest), or <b>stop</b> the fermentation by adding alcohol — <b>fortification</b> (<i>mutage</i>). With neutral grape spirit you get a <b>vin doux naturel</b>; with a brandy (Cognac, Armagnac, marc), a <b>liqueur wine</b>" + r("ue1308", "inao") + ". Adding sugar (chaptalisation) is banned in every sweet AOC wine on this page."))}</div>
    <div class="panel lede">{t(("Ce que dit l’étiquette (vins tranquilles)", "What the label says (still wines)"), "h3")}{sugar_terms_html()}{blk(("Mentions européennes de teneur en sucres" + r("ue2019") + ". Les mousseux ont leur propre échelle, du « brut nature » au « doux » (plus de 50 g/l).", "EU sugar-content terms" + r("ue2019") + ". Sparkling wines have their own scale, from “brut nature” to “doux” (over 50 g/l)."), "p", "note")}</div>
  </div>
  {paths_svg()}
</section>''')

SECTIONS.append(f'''<section class="sec" id="index">
  <div class="sec-head">{t(("02 · Toutes les AOC", "02 · Every AOC"), "p", "kick")}{t((f"Les <em>{len(AOC) + len(JAUNE)} appellations</em> du doux et de l’oxydatif", f"The <em>{len(AOC) + len(JAUNE)} appellations</em> of sweet and oxidative wine"), "h2")}</div>
  {index_html()}
  <div class="panel ladp">{t(("Combien de sucre au minimum dans le vin fini ?", "How much sugar, at least, in the finished wine?"), "h3")}{when_html()}{ladder_html()}</div>
</section>''')

SECTIONS.append(method('botrytis', ('03 · Pourriture noble', '03 · Noble rot'), ('Le champignon <em>magicien</em>', 'The <em>magician</em> fungus'),
    ('Quand les matins d’automne sont brumeux et les après-midi chauds et ventés — au confluent du Ciron et de la Garonne, sur les bords du Layon ou de la Dordogne — le champignon <i>Botrytis cinerea</i> perce la peau des raisins mûrs sans les abîmer. L’eau s’évapore, le sucre, l’acidité et les arômes se concentrent : c’est la <b>pourriture noble</b>. Les grains « rôtis » sont cueillis un à un, en plusieurs passages : les <b>tries successives</b>' + r('sauternes') + '.',
     'When autumn mornings are misty and afternoons warm and windy — where the Ciron meets the Garonne, along the Layon or the Dordogne — the fungus <i>Botrytis cinerea</i> pierces the skin of ripe grapes without spoiling them. Water evaporates; sugar, acidity and aromas concentrate: this is <b>noble rot</b>. The “roasted” berries are picked one by one, in several passes: the <b>successive tries</b>' + r('sauternes') + '.'),
    [(('Brume puis soleil', 'Mist, then sun'), ('L’humidité du matin installe le champignon, le vent de l’après-midi l’empêche de tourner à la pourriture grise.', 'Morning damp lets the fungus settle; the afternoon wind stops it turning into grey rot.')),
     (('Grains rôtis', 'Roasted berries'), ('Le grain flétrit et brunit ; il peut perdre la moitié de son eau.', 'The berry shrivels and browns; it can lose half its water.')),
     (('Tries', 'Passes'), ('Les vendangeurs repassent plusieurs fois dans la même vigne, parfois pendant des semaines.', 'Pickers go through the same vines several times, sometimes for weeks.')),
     (('Fermentation lente', 'Slow fermentation'), ('Les levures peinent puis s’arrêtent vers 13–14 % d’alcool : le sucre restant fait le liquoreux (voir ci-dessous pourquoi).', 'The yeasts struggle, then stop around 13–14% alcohol: the remaining sugar makes the wine sweet (see below why).'))],
    'bot', YEAST_BOX))

SECTIONS.append(method('passerillage', ('04 · Passerillage sur souche', '04 · Drying on the vine'), ('Le raisin <em>sèche au vent</em>', 'The grape <em>dries in the wind</em>'),
    ('Sans botrytis, le raisin laissé sur la vigne après la maturité se flétrit sous l’effet du soleil et des vents secs — le foehn au pied des Pyrénées, le vent d’Autan à Gaillac. Il perd son eau et devient raisin sec : c’est le <b>passerillage</b>. Les vins gardent une acidité vive, signature du Jurançon et du Pacherenc. Beaucoup d’AOC autorisent les deux voies : pourriture noble <i>et/ou</i> passerillage' + r('so_sweet', 'bdx_sweet') + '.',
     'Without botrytis, grapes left on the vine after ripeness shrivel in the sun and dry winds — the foehn at the foot of the Pyrenees, the Autan wind in Gaillac. They lose water and turn into raisins: this is <b>passerillage</b>. The wines keep a bright acidity, the signature of Jurançon and Pacherenc. Many AOCs allow both routes: noble rot <i>and/or</i> drying' + r('so_sweet', 'bdx_sweet') + '.'),
    [(('Vendange différée', 'Delayed harvest'), ('Le raisin reste sur pied plusieurs semaines après la maturité.', 'Grapes stay on the vine for weeks after ripeness.')),
     (('Peaux épaisses', 'Thick skins'), ('Petit manseng, gros manseng, chenin résistent à la pourriture et sèchent bien.', 'Petit Manseng, Gros Manseng and Chenin resist rot and dry well.')),
     (('Acidité préservée', 'Acidity kept'), ('Le sucre monte sans que l’acidité ne s’effondre.', 'Sugar rises without acidity collapsing.'))],
    'pas'))

SECTIONS.append(method('vt-sgn', ('05 · Vendanges tardives & SGN', '05 · Late harvest & SGN'), ('Deux mentions <em>réglementées</em>', 'Two <em>regulated</em> terms'),
    ('« Vendanges tardives » et « sélection de grains nobles » ne sont pas de simples mots de marketing : chaque cahier des charges qui les autorise fixe une richesse minimale du raisin, interdit tout enrichissement et impose souvent un élevage plus long. Nées en Alsace (réglementées en 1984), elles existent aujourd’hui aussi en Loire (SGN du Layon et de l’Aubance), dans le Bergeracois (SGN de Monbazillac) et dans le Sud-Ouest (VT de Jurançon et de Gaillac)' + r('alsace', 'loire_sweet', 'so_sweet') + '.',
     '“Vendanges tardives” (late harvest) and “sélection de grains nobles” (selection of noble berries) are not mere marketing words: every specification that allows them sets a minimum grape sugar level, bans enrichment and often requires longer ageing. Born in Alsace (regulated in 1984), they now also exist in the Loire (Layon and Aubance SGN), around Bergerac (Monbazillac SGN) and in the South-West (Jurançon and Gaillac VT)' + r('alsace', 'loire_sweet', 'so_sweet') + '.'),
    [(('VT', 'VT'), ('Raisins surmûris, souvent passerillés, cueillis tard.', 'Over-ripe, often shrivelled grapes, picked late.')),
     (('SGN', 'SGN'), ('Grains atteints de pourriture noble, triés un à un ; seuils de sucre les plus hauts de France.', 'Nobly rotten berries sorted one by one; the highest sugar thresholds in France.'))],
    'vt'))

SECTIONS.append(method('paille', ('06 · Passerillage hors souche', '06 · Drying off the vine'), ('Le <em>vin de paille</em>', '<em>Straw wine</em>'),
    ('Ici, le raisin est cueilli puis séché à l’abri, sur des lits de paille, des claies ou suspendu dans un grenier aéré, pendant au moins six semaines (45 jours à l’Hermitage). Tout chauffage de l’air est interdit. Les rendements sont minuscules (15 hl/ha à l’Hermitage, 20 hl/ha en Corrèze) et le moût atteint 320 à 420 g/l de sucre dans le Jura' + r('paille') + '.',
     'Here grapes are picked, then dried indoors on straw beds, on racks or hung in an airy loft, for at least six weeks (45 days at Hermitage). Heating the air is banned. Yields are tiny (15 hl/ha at Hermitage, 20 hl/ha in Corrèze) and in the Jura the must reaches 320 to 420 g/l of sugar' + r('paille') + '.'),
    [(('Cueillette', 'Picking'), ('Grappes saines, à la main.', 'Healthy bunches, by hand.')),
     (('Séchage', 'Drying'), ('Paille, claies ou suspension, local ventilé.', 'Straw, racks or hanging, in a ventilated room.')),
     (('Pressurage', 'Pressing'), ('En hiver, quelques gouttes de moût très sucré.', 'In winter: a few drops of very sweet must.')),
     (('Élevage', 'Ageing'), ('3 ans dans le Jura, dont 18 mois sous bois ; demi-bouteille de 37,5 cl d’usage.', '3 years in the Jura, incl. 18 months in wood; customarily sold in 37.5 cl half-bottles.'))],
    'pai'))

SECTIONS.append(method('vdn', ('07 · Mutage à l’alcool neutre', '07 · Fortified with neutral spirit'), ('Les <em>vins doux naturels</em>', '<em>Vins doux naturels</em>'),
    ('Un vin doux naturel (VDN) est un vin dont on arrête la fermentation en ajoutant de l’<b>alcool neutre d’origine viticole titrant au moins 96 %</b>, à raison de 5 à 10 % (en alcool pur) du volume du moût, avant le 31 décembre de l’année de récolte. Le moût doit contenir au moins <b>252 g/l</b> de sucre naturel ; le vin titre au moins 15 % et garde au moins 45 g/l de sucre (100 à 125 g/l pour les muscats). Toute chaptalisation est interdite. Le procédé est attribué à Arnau de Vilanova, médecin à Montpellier au XIII<sup>e</sup> siècle' + r('rivesaltes', 'banyuls', 'muscats', 'ue1308') + '.',
     'A vin doux naturel (VDN) is a wine whose fermentation is stopped by adding <b>neutral grape spirit of at least 96%</b>, at 5 to 10% (pure alcohol) of the must volume, before 31 December of the harvest year. The must needs at least <b>252 g/l</b> of natural sugar; the wine reaches at least 15% and keeps at least 45 g/l of sugar (100 to 125 g/l for the Muscats). Chaptalisation is banned. The process is credited to Arnau de Vilanova, a physician in Montpellier in the 13th century' + r('rivesaltes', 'banyuls', 'muscats', 'ue1308') + '.'),
    [(('Mutage sur jus', 'Fortified on the juice'), ('Blancs, ambrés, rosés et muscats : le jus est séparé des peaux avant de fermenter.', 'Whites, ambrés, rosés and Muscats: the juice is separated from the skins before fermenting.')),
     (('Mutage sur grains', 'Fortified on the skins'), ('Grenats et rimages : l’alcool est versé sur la vendange, la macération continue après, pour la couleur et le fruit.', 'Grenats and rimages: spirit is poured on the crushed grapes and maceration continues, for colour and fruit.')),
     (('Deux élevages', 'Two kinds of ageing'), ('Réducteur (à l’abri de l’air, fruit) ou oxydatif (fût, bonbonnes au soleil, fruits secs).', 'Reductive (away from air, fruit) or oxidative (casks, glass demijohns in the sun, dried fruit).'))],
    'vdn'))

SECTIONS.append(f'''<section class="sec" id="rivesaltes">
  <div class="sec-head">{t(("08 · Roussillon", "08 · Roussillon"), "p", "kick")}{t(("Rivesaltes, Grand Cru <em>et rancio</em>", "Rivesaltes, Grand Cru <em>and rancio</em>"), "h2")}</div>
  <div class="two">
    <div class="panel lede answer">{t(("Y a-t-il un « Rivesaltes Grand Cru » ?", "Is there a “Rivesaltes Grand Cru”?"), "h3")}{blk(("<b>Non.</b> Le cahier des charges de Rivesaltes (arrêté du 14 juin 2023) ne connaît que des <b>mentions</b> : obligatoirement <b>ambré, grenat, rosé ou tuilé</b>, puis facultativement <b>hors d’âge</b> et <b>rancio</b>" + r("rivesaltes") + ". La seule appellation de vin doux naturel à porter le titre de grand cru est sa voisine, <b>Banyuls grand cru</b> (AOC depuis 1962) : un rouge seulement, au moins 75 % de grenache noir, vendange égrappée et macérée au moins 5 jours, puis élevé en bois au moins jusqu’au 1<sup>er</sup> juin de la 3<sup>e</sup> année — soit ≈ 30 mois" + r("banyuls") + ".",
                                                                                                                                  "<b>No.</b> The Rivesaltes specification (order of 14 June 2023) only knows <b>mentions</b>: compulsorily <b>ambré, grenat, rosé or tuilé</b>, then optionally <b>hors d’âge</b> and <b>rancio</b>" + r("rivesaltes") + ". The only vin doux naturel appellation to bear the grand cru title is its neighbour, <b>Banyuls grand cru</b> (AOC since 1962): red only, at least 75% Grenache Noir, destemmed and macerated for at least 5 days, then aged in wood until at least 1 June of the 3rd year — ≈ 30 months" + r("banyuls") + "."))}
      {blk(("Depuis 2023, un Rivesaltes ambré ou tuilé peut être vendu dès le <b>1<sup>er</sup> septembre de la 2<sup>e</sup> année</b> (élevage oxydatif jusqu’au 31 août), un hors d’âge à partir du 1<sup>er</sup> septembre de la <b>5<sup>e</sup> année</b>. À Banyuls, Maury et Rasteau, l’ambré et le tuilé restent au moins jusqu’au 1<sup>er</sup> mars de la 3<sup>e</sup> année" + r("rivesaltes", "banyuls", "vdn_other") + ".",
             "Since 2023, a Rivesaltes ambré or tuilé may be sold from <b>1 September of the 2nd year</b> (oxidative ageing until 31 August), a hors d’âge from 1 September of the <b>5th year</b>. At Banyuls, Maury and Rasteau, ambré and tuilé stay at least until 1 March of the 3rd year" + r("rivesaltes", "banyuls", "vdn_other") + "."))}
    </div>
    <div class="panel lede ran-box">{t(("Le rancio, goût du temps", "Rancio, the taste of time"), "h3")}{blk(("Le <b>rancio</b> naît d’un long élevage oxydatif : fûts en vidange, parfois <b>bonbonnes de verre laissées dehors</b> au soleil et au froid. Le vin s’oxyde lentement et prend des notes de noix, de cacao, de café, de pruneau, de curry. La loi ne fixe aucune durée : la mention est réservée aux vins qui « ont acquis le goût de rancio », vérifié à la dégustation" + r("rivesaltes", "banyuls") + ".",
                                                                                                      "<b>Rancio</b> comes from long oxidative ageing: casks left partly empty, sometimes <b>glass demijohns left outdoors</b> in sun and cold. The wine oxidises slowly and develops notes of walnut, cocoa, coffee, prune and curry. The law sets no duration: the term is reserved for wines that “have acquired the rancio taste”, checked by tasting" + r("rivesaltes", "banyuls") + "."))}
      {blk(("AOC qui autorisent la mention : Rivesaltes, Banyuls, Banyuls grand cru, Maury, Grand Roussillon, Rasteau (VDN) et Clairette du Languedoc (raisins surmûris, élevage jusqu’au 15 octobre de la 3<sup>e</sup> année)" + r("vdn_other", "vdl") + ".",
             "AOCs allowing the term: Rivesaltes, Banyuls, Banyuls grand cru, Maury, Grand Roussillon, Rasteau (VDN) and Clairette du Languedoc (over-ripe grapes, aged until 15 October of the 3rd year)" + r("vdn_other", "vdl") + "."), "p", "note")}
    </div>
  </div>
  <div class="panel mxp">{t(("Les mentions des vins doux naturels de grenache", "The terms used for Grenache vins doux naturels"), "h3")}{vdn_matrix()}</div>
  {cards("vdn")}
</section>''')

SECTIONS.append(method('vdl', ('09 · Mutage à l’eau-de-vie', '09 · Fortified with brandy'), ('Les <em>vins de liqueur</em>', '<em>Liqueur wines</em>'),
    ('Pour un vin de liqueur d’AOC, le moût de raisin — à peine ou pas du tout fermenté — est muté avec une <b>eau-de-vie de la région</b>, produite <b>sur la même exploitation</b> : Cognac pour le Pineau des Charentes, Armagnac pour le Floc de Gascogne, marc du Jura pour le Macvin. Ces vins titrent 16 à 22 %. Ce sont les cousins des « mistelles » et de la carthagène languedocienne, qui ne sont pas des AOC' + r('vdl', 'ue1308') + '.',
     'For an AOC liqueur wine, grape must — barely or not at all fermented — is fortified with a <b>local brandy</b> made <b>on the same estate</b>: Cognac for Pineau des Charentes, Armagnac for Floc de Gascogne, Marc du Jura for Macvin. These wines reach 16 to 22%. They are cousins of the “mistelles” and of Languedoc carthagène, which are not AOCs' + r('vdl', 'ue1308') + '.'),
    [(('Moût', 'Must'), ('Au moins 153 à 170 g/l de sucre au moment du mutage.', 'At least 153 to 170 g/l of sugar at fortification.')),
     (('Eau-de-vie maison', 'Home brandy'), ('Même exploitation, déjà vieillie (Cognac rassis, Armagnac ≥ 52 %, marc ≥ 14 mois de chêne).', 'Same estate, already aged (settled Cognac, Armagnac ≥ 52%, marc ≥ 14 months in oak).')),
     (('Élevage', 'Ageing'), ('De quelques mois (Floc) à plus de 12 ans (Pineau « très vieux »).', 'From a few months (Floc) to over 12 years (“très vieux” Pineau).'))],
    'vdl'))

SECTIONS.append(method('bulles', ('10 · Bulles douces', '10 · Sweet bubbles'), ('Le doux <em>qui pétille</em>', 'Sweetness <em>that sparkles</em>'),
    ('La <b>méthode ancestrale</b> n’a qu’une seule fermentation, commencée en cuve et achevée en bouteille, où elle est arrêtée avant d’avoir consommé tout le sucre du raisin. Elle donne des vins légers en alcool et naturellement doux, sans liqueur ajoutée. À l’inverse, un Champagne doux ou demi-sec doit son sucre à la <b>liqueur d’expédition</b> ajoutée au dégorgement' + r('bulles', 'ue2019') + '.',
     'The <b>ancestral method</b> has a single fermentation, started in tank and finished in bottle, where it stops before using up all the grape sugar. It gives light, naturally sweet wines with no added liqueur. A doux or demi-sec Champagne, by contrast, owes its sugar to the <b>dosage liqueur</b> added at disgorging' + r('bulles', 'ue2019') + '.'),
    [], 'bul'))

SECTIONS.append(f'''<section class="sec" id="cepages">
  <div class="sec-head">{t(("11 · Les cépages", "11 · The grapes"), "p", "kick")}{t(("Les cépages <em>du doux</em>", "The grapes <em>of sweet wine</em>"), "h2")}</div>
  <div class="panel lede">{blk(("Chaque fiche ci-dessus donne la liste officielle des cépages de l’AOC, lue dans les cahiers des charges : <b>gras</b> = cépage principal, <i>italique</i> = accessoire, souligné en pointillé = complémentaire, grisé = variété d’adaptation (expérimentale, ≤ 5–10 %). Voici l’index inverse : pour chaque cépage, les AOC du doux où il est autorisé.",
                                       "Every card above gives the official list of the AOC’s grapes, read from the specifications: <b>bold</b> = main variety, <i>italic</i> = accessory, dotted underline = complementary, greyed = adaptation variety (experimental, ≤ 5–10%). Here is the reverse index: for each grape, the sweet AOCs where it is allowed."))}</div>
  {grape_index()}
</section>''')

SECTIONS.append(f'''<section class="sec" id="glace">
  <div class="sec-head">{t(("12 · Hors AOC", "12 · Outside the AOCs"), "p", "kick")}{t(("Le <em>vin de glace</em>", "<em>Ice wine</em>"), "h2")}</div>
  <div class="method">
    <div class="panel lede ice">{blk(("Le vin de glace (<i>Eiswein</i> en Allemagne et en Autriche, <i>icewine</i> au Canada) est fait de raisins laissés sur la vigne jusqu’aux grands froids de l’hiver, <b>cueillis gelés et pressés gelés</b>. L’eau reste dans le pressoir sous forme de glace : il ne coule qu’un jus très concentré en sucre et en acidité. L’OIV recommande une récolte et un pressurage à <b>−7 °C ou moins</b>, un moût d’au moins 15 % d’alcool potentiel, sans aucun enrichissement" + r("oiv_ice") + ".",
                                                    "Ice wine (<i>Eiswein</i> in Germany and Austria, <i>icewine</i> in Canada) is made from grapes left on the vine until the hard frosts of winter, <b>picked frozen and pressed frozen</b>. The water stays in the press as ice: only a juice very concentrated in sugar and acidity runs out. The OIV recommends picking and pressing at <b>−7 °C or below</b>, a must of at least 15% potential alcohol, with no enrichment" + r("oiv_ice") + "."))}
      {blk(("<b>Ce n’est pas une AOC.</b> Aucun cahier des charges d’appellation française ne prévoit de vin de glace, et le terme n’est défini par aucun texte français — contrairement à « Eiswein », mention traditionnelle protégée de l’Allemagne et de l’Autriche" + r("ue934") + ". Les rares vins de glace français sont donc vendus hors appellation (IGP ou Vin de France). Il en naît de loin en loin en Alsace et dans le Sud-Ouest, les hivers où le thermomètre descend assez bas avant que les oiseaux, la pourriture ou la pluie n’aient eu raison des raisins.",
             "<b>It is not an AOC.</b> No French appellation specification provides for ice wine, and the term is defined by no French text — unlike “Eiswein”, a protected traditional term of Germany and Austria" + r("ue934") + ". The rare French ice wines are therefore sold outside the appellations (IGP or Vin de France). A few are made now and then in Alsace and in the South-West, in winters when the thermometer drops low enough before birds, rot or rain have taken the grapes."))}
    </div>
    <ol class="steps">
      <li><b>{t(("Attendre l’hiver", "Wait for winter"))}</b> {t(("Grappes saines laissées sur pied, souvent protégées par des filets, jusqu’en décembre ou janvier.", "Healthy bunches left on the vine, often under nets, until December or January."))}</li>
      <li><b>{t(("Vendange de nuit", "Night harvest"))}</b> {t(("On cueille à l’aube ou de nuit, quand le raisin est dur comme une bille (≤ −7 °C).", "Picking at dawn or at night, when the grapes are as hard as marbles (≤ −7 °C)."))}</li>
      <li><b>{t(("Pressurage gelé", "Frozen pressing"))}</b> {t(("La glace reste dans le pressoir ; quelques gouttes de jus sirupeux s’écoulent.", "The ice stays in the press; a few drops of syrupy juice run out."))}</li>
      <li><b>{t(("Fermentation lente", "Slow fermentation"))}</b> {t(("Elle s’arrête souvent vers 8–12 % d’alcool, en gardant beaucoup de sucre et une acidité vive.", "It often stops around 8–12% alcohol, keeping lots of sugar and a bright acidity."))}</li>
    </ol>
  </div>
  <div class="two ice-two">
    <div class="panel lede">{t(("Le froid naturel… et le froid artificiel", "Natural cold… and artificial cold"), "h3")}{blk(("On peut aussi geler les raisins en chambre froide puis les presser : c’est la <b>cryoextraction</b>. Le procédé est autorisé en œnologie, mais il ne donne pas un vin de glace au sens de l’OIV, qui exige un gel « dans le vignoble, sans recours à des procédés physiques »" + r("oiv_ice") + ". Certaines AOC l’interdisent : à Haut-Montravel, tout traitement de la vendange sous −5 °C est prohibé ; en Corrèze, la cryoconcentration est exclue pour le vin de paille" + r("so_sweet", "paille") + ".",
                                                                                                                          "Grapes can also be frozen in a cold room and then pressed: this is <b>cryo-extraction</b>. The process is allowed in winemaking, but it does not make an ice wine in the OIV sense, which requires freezing “in the vineyard, without physical processes”" + r("oiv_ice") + ". Some AOCs ban it: at Haut-Montravel any treatment of the grapes below −5 °C is prohibited; in Corrèze, cryo-concentration is excluded for straw wine" + r("so_sweet", "paille") + "."))}</div>
    <div class="panel lede">{t(("Un cousin d’AOC : la Saint-Sylvestre", "An AOC cousin: Saint-Sylvestre"), "h3")}{blk(("Dans le Gers, les vignerons de Plaimont vendangent chaque <b>31 décembre</b>, à Viella, les dernières grappes de Pacherenc du Vic-Bilh — une tradition née après le gel de 1991. Ce n’est pas un vin de glace : ces 4<sup>e</sup> et 5<sup>e</sup> tries donnent des raisins <b>passerillés</b> sur souche, à ≈ 5 hl/ha, vendus sous l’AOC" + r("plaimont") + ".",
                                                                                                                  "In the Gers, the Plaimont growers pick the last Pacherenc du Vic-Bilh bunches every <b>31 December</b> at Viella — a tradition born after the 1991 frost. It is not an ice wine: these 4th and 5th passes give grapes <b>shrivelled</b> on the vine, at ≈ 5 hl/ha, sold under the AOC" + r("plaimont") + "."))}</div>
  </div>
</section>''')

JAUNE_SEC = f'''<section class="sec jaune" id="jaune">
  <div class="sec-head">{t(("13 · Le joyau du Jura", "13 · The jewel of the Jura"), "p", "kick")}{t(("Le <em>vin jaune</em>", "<em>Vin jaune</em>"), "h2")}</div>
  <div class="panel lede jy-lede">{blk(("Le vin jaune n’est <b>pas un vin doux</b> : il est sec (au plus 3 g/l de sucre). Mais, comme le rancio, c’est un vin <b>oxydatif</b> né d’un très long élevage, et il partage avec les vins de paille et le Macvin le même vignoble jurassien. Issu du seul <b>savagnin</b>, il vieillit plus de six ans en fût <b>sans jamais être complété</b> : un voile de levures se forme à sa surface et lui donne le « <b>goût de jaune</b> » — noix, pomme mûre, curry" + r("jura_decrees") + ".",
                                                  "Vin jaune is <b>not a sweet wine</b>: it is dry (3 g/l of sugar at most). But, like rancio, it is an <b>oxidative</b> wine born of very long ageing, and it shares the Jura vineyard with straw wine and Macvin. Made from <b>Savagnin</b> alone, it ages for more than six years in cask <b>without ever being topped up</b>: a veil of yeast forms on its surface and gives it the “<b>goût de jaune</b>” — walnut, ripe apple, curry" + r("jura_decrees") + "."))}</div>

  <div class="jgrid">
    <div class="panel jc"><h3>{t(("Histoire", "History"))}</h3>
      {blk(("Le vin de Château-Chalon, autrefois appelé « vin de garde », est lié à l’<b>abbaye de dames nobles</b> fondée avant le X<sup>e</sup> siècle sur le promontoire du village ; son prestige le fait connaître des cours d’Europe. L’origine exacte de la méthode reste inconnue. <b>Louis Pasteur</b>, né à Dole et élevé à Arbois, l’étudie longuement dans ses <i>Études sur le vin</i> (1866)" + r("jura_decrees", "pasteur") + ".",
             "Château-Chalon wine, once called “vin de garde” (wine for keeping), is tied to the <b>abbey of noble ladies</b> founded before the 10th century on the village’s promontory; its prestige made it known at Europe’s courts. The exact origin of the method is unknown. <b>Louis Pasteur</b>, born in Dole and raised in Arbois, studied it at length in his <i>Études sur le vin</i> (1866)" + r("jura_decrees", "pasteur") + "."))}
      {blk(("Le syndicat de Château-Chalon naît le 14 mai 1933 ; l’AOC est reconnue en 1936. Une commission visite chaque parcelle avant les vendanges et peut renoncer à l’appellation : il n’y eut pas de Château-Chalon en 1974, 1980, 1984 et 2001. Depuis 1997, la <b>Percée du vin jaune</b> fête chaque premier week-end de février, dans un village différent, la mise en perce du millésime qui sort" + r("jura_decrees", "percee") + ".",
             "The Château-Chalon growers’ union was founded on 14 May 1933; the AOC was recognised in 1936. A committee inspects every plot before harvest and may forgo the appellation: there was no Château-Chalon in 1974, 1980, 1984 and 2001. Since 1997, the <b>Percée du vin jaune</b> has celebrated, each first weekend of February in a different village, the broaching of the vintage being released" + r("jura_decrees", "percee") + "."))}
    </div>
    <div class="panel jc"><h3>{t(("Le cépage : savagnin", "The grape: Savagnin"))}</h3>
      {blk(("Le <b>savagnin blanc</b> (appelé « naturé » dans le Jura) est le <b>seul cépage autorisé</b> pour le vin jaune dans les quatre AOC. Variété tardive à peau épaisse, il garde une forte acidité, indispensable pour un si long élevage. C’est l’un des plus anciens cépages d’Europe : un pépin médiéval trouvé à Orléans est génétiquement identique au savagnin actuel" + r("jura_decrees", "savagnin") + ".",
             "<b>Savagnin Blanc</b> (called “naturé” in the Jura) is the <b>only grape allowed</b> for vin jaune in all four AOCs. A late, thick-skinned variety, it keeps a high acidity, essential for such long ageing. It is one of Europe’s oldest grapes: a medieval seed found in Orléans is genetically identical to today’s Savagnin" + r("jura_decrees", "savagnin") + "."))}
      {blk(("Raisins récoltés à maturité physiologique, ≥ 204 g/l de sucre et ≥ 12 % naturel à Château-Chalon ; pas plus de 14 % avant l’élevage ; copeaux de bois interdits" + r("jura_decrees") + ".",
             "Grapes picked at physiological ripeness, ≥ 204 g/l of sugar and ≥ 12% natural alcohol at Château-Chalon; no more than 14% before ageing; oak chips banned" + r("jura_decrees") + "."), "p", "note")}
    </div>
  </div>

  <div class="panel jc"><h3>{t(("La méthode : élevage sous voile", "The method: ageing under the veil"))}</h3>
    {timeline_html()}
    <ol class="steps jsteps">
      <li><b>{t(("Fermentation complète", "Full fermentation"))}</b> {t(("Le savagnin est vinifié en blanc sec, fermentation menée jusqu’au bout, puis soutiré.", "Savagnin is made as a dry white, fermented right through, then racked."))}</li>
      <li><b>{t(("Fût en vidange", "Cask left ullaged"))}</b> {t(("Le vin est mis en fûts de chêne (souvent 228 l) qu’on ne remplit pas complètement et qu’on ne complète <b>jamais</b> (pas d’ouillage).", "The wine goes into oak casks (often 228 l) that are not filled to the top and are <b>never</b> topped up (no <i>ouillage</i>)."))}</li>
      <li><b>{t(("Le voile", "The veil"))}</b> {t(("Des levures forment naturellement un voile à la surface. Il protège le vin tout en permettant une oxydation ménagée ; les grands écarts de température entre hiver et été du grenier le renforcent.", "Yeasts naturally form a veil on the surface. It protects the wine while allowing gentle oxidation; the large winter-summer temperature swings of the loft strengthen it."))}</li>
      <li><b>{t(("Le goût de jaune", "The goût de jaune"))}</b> {t(("L’éthanal et surtout le <b>sotolon</b> (noix, curry) se forment pendant ces années sous voile" + r("sotolon") + ".", "Acetaldehyde and above all <b>sotolon</b> (walnut, curry) form during these years under the veil" + r("sotolon") + "."))}</li>
      <li><b>{t(("Six ans et trois mois", "Six years and three months"))}</b> {t(("Élevage minimal en fût jusqu’au <b>15 décembre de la 6<sup>e</sup> année</b> après la récolte, dont <b>60 mois au moins sous voile</b> ; mise en marché à partir du <b>1<sup>er</sup> janvier de la 7<sup>e</sup> année</b>" + r("jura_decrees") + ".", "Minimum cask ageing until <b>15 December of the 6th year</b> after harvest, including <b>at least 60 months under the veil</b>; released from <b>1 January of the 7th year</b>" + r("jura_decrees") + "."))}</li>
    </ol>
  </div>

  <div class="jgrid">
    <div class="panel jc clav-p"><h3>{t(("La bouteille : le clavelin", "The bottle: the clavelin"))}</h3>
      <div class="clav-row">{clavelin_svg()}<div>
        {blk(("Le <b>clavelin</b> est une bouteille trapue à col court de <b>62 cl</b>, dont la hauteur fait ≈ 2,75 fois le diamètre de la base. C’est la seule bouteille autorisée pour le vin jaune, et elle lui est réservée" + r("jura_decrees", "ue2019") + ".",
               "The <b>clavelin</b> is a squat, short-necked <b>62 cl</b> bottle whose height is ≈ 2.75 times its base diameter. It is the only bottle allowed for vin jaune, and is reserved for it" + r("jura_decrees", "ue2019") + "."))}
      </div></div>
      <div class="legend-box">{t(("Un litre devenu 62 cl : fait ou légende ?", "One litre turned into 62 cl: fact or legend?"), "h4")}
        {blk(("On raconte que 62 cl, c’est ce qui reste d’<b>un litre</b> de vin après six ans et trois mois en fût sans ouillage, les 38 cl manquants étant la « <b>part des anges</b> ». Le cahier des charges de Château-Chalon reprend lui-même cette explication" + r("jura_decrees") + ". Mais c’est une <b>tradition orale plutôt qu’un fait établi</b> : l’historien du vin jaune Claude Royer la range parmi les légendes, et une perte de 38 % en six ans dépasse de loin l’évaporation habituelle, de quelques pour cent par an" + r("clav_gce", "clav_blog") + ". Le vin s’évapore bel et bien sous voile ; c’est la coïncidence exacte avec 62 cl qui relève du conte.",
               "The story goes that 62 cl is what remains of <b>one litre</b> of wine after six years and three months in cask without topping up, the missing 38 cl being the “<b>angels’ share</b>”. The Château-Chalon specification itself repeats this explanation" + r("jura_decrees") + ". But it is <b>an oral tradition rather than an established fact</b>: the vin jaune historian Claude Royer files it among the legends, and a 38% loss in six years far exceeds normal evaporation of a few per cent a year" + r("clav_gce", "clav_blog") + ". Wine really does evaporate under the veil; it is the exact match with 62 cl that belongs to folklore."))}
      </div>
      {angels_html()}
    </div>
    <div class="panel jc"><h3>{t(("Ce que dit la loi", "What the law says"))}</h3>
      <ul class="law">
        <li>{t(("<b>Cahiers des charges</b> : décrets n° 2011-1187 (Château-Chalon), 2011-1188 (Arbois), 2011-1189 (Côtes du Jura) du 23 septembre 2011 ; décret n° 2011-1096 du 9 septembre 2011 modifié par le décret n° 2013-143 (L’Étoile)" + r("jura_decrees") + ".", "<b>Specifications</b>: decrees No 2011-1187 (Château-Chalon), 2011-1188 (Arbois), 2011-1189 (Côtes du Jura) of 23 September 2011; decree No 2011-1096 of 9 September 2011 as amended by decree No 2013-143 (L’Étoile)" + r("jura_decrees") + "."))}</li>
        <li>{t(("<b>Chapitre I, IX-2°</b> : « élevage minimum, en fût de chêne, sans ouillage, jusqu’au 15 décembre de la 6<sup>e</sup> année […] dont 60 mois au moins sous voile ».", "<b>Chapter I, IX-2°</b>: minimum ageing “in oak cask, without topping up, until 15 December of the 6th year […] of which at least 60 months under the veil”."))}</li>
        <li>{t(("<b>Chapitre I, IX-3° b</b> : le clavelin « d’une contenance de 62 centilitres environ » est réservé aux vins jaunes de l’AOC ; à Château-Chalon il porte en plus le <b>cachet moulé</b> au nom de l’appellation.", "<b>Chapter I, IX-3° b</b>: the clavelin “of about 62 centilitres” is reserved for the AOC’s vins jaunes; at Château-Chalon it also bears the <b>moulded seal</b> with the appellation’s name."))}</li>
        <li>{t(("<b>Règlement délégué (UE) 2019/33</b>, article 56 et annexe VII point 3 : le clavelin (0,62 l) est réservé aux AOP Côtes du Jura, Arbois, L’Étoile et Château-Chalon" + r("ue2019") + ".", "<b>Delegated Regulation (EU) 2019/33</b>, Article 56 and Annex VII point 3: the clavelin (0.62 l) is reserved for the Côtes du Jura, Arbois, L’Étoile and Château-Chalon PDOs" + r("ue2019") + "."))}</li>
        <li>{t(("<b>Directive 2007/45/CE</b> : la seule quantité nominale autorisée pour le vin jaune est 62 cl" + r("dir2007") + ".", "<b>Directive 2007/45/EC</b>: the only nominal quantity allowed for vin jaune is 62 cl" + r("dir2007") + "."))}</li>
        <li>{t(("<b>Normes</b> : sucres ≤ 3 g/l au conditionnement (≤ 3 g/l pour tous les vins non « paille » du Jura).", "<b>Standards</b>: sugar ≤ 3 g/l at bottling (≤ 3 g/l for all Jura wines other than straw wine)."))}</li>
      </ul>
    </div>
  </div>

      <div class="panel jc clav-hist"><h3>{t(("Histoire du clavelin", "History of the clavelin"))}</h3><div class="hist-cols">
        {blk(("<b>Le modèle anglais.</b> Sa forme dérive de la bouteille de verre noir épais mise au point en Angleterre au XVII<sup>e</sup> siècle — associée à Sir Kenelm Digby —, qui contenait alors ≈ 65 cl ; le clavelin est d’ailleurs souvent décrit comme une « bouteille dite anglaise »" + r("clav_gce", "clav_jw") + ".",
               "<b>The English model.</b> Its shape derives from the thick black-glass bottle developed in England in the 17th century — associated with Sir Kenelm Digby — which then held ≈ 65 cl; the clavelin is in fact often described as a “so-called English bottle”" + r("clav_gce", "clav_jw") + "."))}
        {blk(("<b>La Vieille-Loye.</b> Selon la tradition, des vignerons de Château-Chalon commandent au XVIII<sup>e</sup> siècle une bouteille spéciale, à leur nom, à la verrerie de La Vieille-Loye, près de Dole, privilégiée depuis une concession de Marguerite de Bourgogne en 1506 ; les clavelins y sont soufflés à la bouche" + r("jura_decrees", "clav_jw") + ".",
               "<b>La Vieille-Loye.</b> According to tradition, Château-Chalon growers ordered a special bottle bearing their name from the La Vieille-Loye glassworks near Dole in the 18th century — a works privileged since a grant by Margaret of Burgundy in 1506; clavelins were mouth-blown there" + r("jura_decrees", "clav_jw") + "."))}
        {blk(("<b>Le nom.</b> Son origine reste incertaine. La version la plus répandue évoque un abbé (ou chanoine) Clavelin qui aurait commandé en 1914 une trentaine de bouteilles marquées de son sceau ; d’autres y voient simplement un nom de famille courant dans le Jura. L’usage du clavelin pour le vin jaune ne se généralise qu’au début du XX<sup>e</sup> siècle" + r("clav_jw", "clav_blog") + ".",
               "<b>The name.</b> Its origin is uncertain. The most common version tells of an abbot (or canon) Clavelin who ordered some thirty bottles stamped with his seal in 1914; others see simply a family name common in the Jura. Using the clavelin for vin jaune only became widespread in the early 20th century" + r("clav_jw", "clav_blog") + "."))}
        {blk(("<b>Pourquoi 62 cl ?</b> Plutôt que l’évaporation, certains rapprochent ce volume du <b>chauveau</b>, ancienne mesure de liquide du Jura et de la Bourgogne proche de 62 cl, ou de la bouteille anglaise d’origine" + r("clav_gce") + ". <b>Sauvé par l’Europe.</b> Quand l’Europe a harmonisé les contenances des bouteilles, le 62 cl n’y figurait pas : le clavelin a obtenu une exception, aujourd’hui inscrite dans la directive 2007/45/CE et protégée par le règlement (UE) 2019/33" + r("clav_gce", "dir2007", "ue2019") + ".",
               "<b>Why 62 cl?</b> Rather than evaporation, some link this volume to the <b>chauveau</b>, an old liquid measure of the Jura and Burgundy close to 62 cl, or to the original English bottle" + r("clav_gce") + ". <b>Saved by Europe.</b> When Europe harmonised bottle sizes, 62 cl was not among them: the clavelin won an exception, now written into Directive 2007/45/EC and protected by Regulation (EU) 2019/33" + r("clav_gce", "dir2007", "ue2019") + "."))}
      </div></div>
  <div class="panel jc" id="jaune-aoc"><h3>{t(("Les quatre AOC autorisées", "The four AOCs allowed"))}</h3>{jaune_table()}</div>
</section>'''


TOC = [('sucre', 'Le sucre', 'Sugar'), ('index', 'Toutes les AOC', 'Every AOC'), ('botrytis', 'Pourriture noble', 'Noble rot'),
       ('passerillage', 'Passerillage', 'Vine-drying'), ('vt-sgn', 'VT & SGN', 'VT & SGN'), ('paille', 'Vin de paille', 'Straw wine'),
       ('vdn', 'Vins doux naturels', 'Vins doux naturels'), ('rivesaltes', 'Rivesaltes, Grand Cru & rancio', 'Rivesaltes, Grand Cru & rancio'),
       ('vdl', 'Vins de liqueur', 'Liqueur wines'), ('bulles', 'Bulles douces', 'Sweet bubbles'), ('cepages', 'Cépages', 'Grapes'),
       ('glace', 'Vin de glace', 'Ice wine'), ('jaune', 'Vin jaune', 'Vin jaune')]


def keys_html():
    nvdn = sum(1 for a in AOC if 'vdn' in a['fams'])
    ks = [(f'{len(AOC) + len(JAUNE)}', ('appellations décrites sur cette page', 'appellations described on this page')),
          ('252 g/l', ('de sucre naturel minimum dans le moût d’un vin doux naturel', 'minimum natural sugar in a vin doux naturel must')),
          (f'{nvdn}', ('AOC de vins doux naturels', 'vin doux naturel AOCs')),
          ('62 cl', ('le clavelin, seule bouteille du vin jaune', 'the clavelin, vin jaune’s only bottle'))]
    return ''.join(f'<div class="key"><b>{v}</b>{t(l, "small")}</div>' for v, l in ks)


def sources_html():
    return ''.join(f'<li id="src-{i + 1}">{t((fr, en))}</li>' for i, (k, fr, en) in enumerate(SOURCES))


CSS = r'''
  sup.ref{font-size:.68em;line-height:0;margin-left:1px;}
  sup.ref a{color:var(--gold);text-decoration:none;font-weight:700;}
  sup.ref a:hover{text-decoration:underline;}
  :root{--c-bot:#d4a437;--c-pas:#d98a3a;--c-vt:#e2c35a;--c-pai:#c9b27a;--c-vdn:#d9566b;--c-vdl:#b48ad6;--c-ran:#b07a4f;--c-bul:#7fb2d6;--c-jau:#f0c419;}
  html[data-theme="cream"]{--c-bot:#a8770f;--c-pas:#b4611a;--c-vt:#9a7d12;--c-pai:#8c7440;--c-vdn:#9b2235;--c-vdl:#6d3f99;--c-ran:#7d4a26;--c-bul:#2f6f9c;--c-jau:#a47f00;}
  .f-bot{--k:var(--c-bot);} .f-pas{--k:var(--c-pas);} .f-vt{--k:var(--c-vt);} .f-pai{--k:var(--c-pai);} .f-vdn{--k:var(--c-vdn);}
  .f-vdl{--k:var(--c-vdl);} .f-ran{--k:var(--c-ran);} .f-bul{--k:var(--c-bul);} .f-jau{--k:var(--c-jau);}
  .lede{padding:clamp(18px,3vw,28px);}
  .lede p{margin:0 0 10px;font-size:15.2px;line-height:1.72;} .lede p:last-child{margin-bottom:0;}
  .lede h3,.panel h3{margin:0 0 12px;font-family:var(--serif);font-weight:500;font-size:22px;color:var(--title);line-height:1.2;}
  .lede a{color:var(--gold-soft);}
  .sec-head .kick{font-size:10.5px;letter-spacing:.3em;text-transform:uppercase;color:var(--gold);font-weight:700;margin:0 0 8px;}
  .sec-head h2 em{font-style:italic;color:var(--gold-soft);}
  .note{font-size:12.5px;color:var(--faint);margin:12px 0 0;line-height:1.55;}
  .keys{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:24px;}
  .key{padding:14px 16px;border-radius:16px;border:1px solid var(--hair);background:var(--glass);text-align:left;}
  .key b{display:block;font-family:var(--serif);font-weight:500;font-size:24px;color:var(--title);line-height:1.1;}
  .key small{font-size:12.5px;color:var(--muted);line-height:1.4;}
  .two{display:grid;grid-template-columns:1.25fr 1fr;gap:12px;}
  .sts{display:grid;gap:6px;}
  .st{display:grid;grid-template-columns:90px 80px 1fr;gap:10px;align-items:baseline;padding:8px 12px;border-radius:10px;background:var(--track);}
  .st b{font-family:var(--serif);font-size:17px;color:var(--title);font-weight:500;font-style:italic;}
  .st span{font-weight:700;color:var(--gold-soft);font-size:14px;} .st small{font-size:12px;color:var(--faint);}
  .fig{margin:14px 0 0;padding:14px;border-radius:18px;border:1px solid var(--hair);background:var(--glass);}
  .paths{width:100%;height:auto;display:block;}
  .paths .nd{stroke-width:1.5;fill:color-mix(in srgb,var(--k) 16%,transparent);stroke:var(--k);}
  .paths .nd.g{--k:#6b8f4e;} .paths .nd.h{--k:var(--gold);} .paths .nd.bot{--k:var(--c-bot);} .paths .nd.pas{--k:var(--c-pas);}
  .paths .nd.pai{--k:var(--c-pai);} .paths .nd.vdn{--k:var(--c-vdn);} .paths .nd.vdl{--k:var(--c-vdl);}
  .paths .tb{fill:var(--title);font:600 13.5px var(--sans);text-anchor:middle;}
  .paths .ts{fill:var(--muted);font:12px var(--sans);text-anchor:middle;}
  .paths .tt{fill:var(--gold);font:700 11px var(--sans);letter-spacing:.18em;text-transform:uppercase;text-anchor:middle;}
  .paths .ar{fill:none;stroke:var(--faint);stroke-width:1.4;marker-end:url(#ah);} .paths .ar.dash{stroke-dasharray:4 4;marker-end:none;}
  .paths .ahf{fill:var(--faint);} .paths .sep{stroke:var(--hair-hi);stroke-dasharray:3 5;}
  .method{display:grid;grid-template-columns:1.5fr 1fr;gap:12px;}
  .steps{margin:0;padding:16px 18px 16px 40px;border-radius:16px;border:1px solid var(--hair);background:var(--glass);font-size:14px;line-height:1.55;}
  .steps:empty{display:none;} .method:has(.steps:empty){grid-template-columns:1fr;}
  .steps li{margin-bottom:8px;} .steps li::marker{color:var(--gold);font-weight:700;} .steps b{color:var(--title);}
  .yeast{margin-top:12px;padding:18px 20px;border-left:3px solid var(--c-bot);}
  .yeast > p{font-size:14.4px;line-height:1.65;margin:0 0 10px;}
  .ys{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin:4px 0 12px;}
  .y{padding:12px 14px;border-radius:12px;background:var(--track);}
  .y > b{display:block;font-family:var(--serif);font-weight:500;font-size:16px;color:var(--title);margin-bottom:4px;}
  .y p{margin:0;font-size:13.2px;line-height:1.55;color:var(--muted);}
  .yeast .y-end{font-size:14px;line-height:1.65;margin:0;}
  .ice{border-left:3px solid #8fc3e0;}
  .ice-two{margin-top:12px;grid-template-columns:1fr 1fr;}
  .legend-box{margin-top:14px;padding:14px 16px;border-radius:12px;background:var(--track);border-left:3px solid var(--c-jau);}
  .legend-box h4{margin:0 0 6px;font-family:var(--serif);font-weight:500;font-size:17px;color:var(--title);}
  .legend-box p{font-size:13.6px;line-height:1.6;margin:0 0 8px;} .legend-box p:last-child{margin-bottom:0;}
  .clav-hist{border-left:3px solid var(--gold);}
  .hist-cols{column-count:2;column-gap:28px;} .hist-cols p{break-inside:avoid;font-size:14px;line-height:1.62;margin:0 0 10px;}
  @media (max-width:900px){ .hist-cols{column-count:1;} }
  .aocs{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:12px;margin-top:14px;}
  .aoc{padding:16px 18px 16px;border-radius:16px;background:var(--glass);border:1px solid var(--hair);border-top:3px solid var(--k,var(--gold));}
  .aoc[data-fam^="bot"]{--k:var(--c-bot);} .aoc[data-fam^="pas"]{--k:var(--c-pas);} .aoc[data-fam^="vt"]{--k:var(--c-vt);} .aoc[data-fam^="pai"]{--k:var(--c-pai);}
  .aoc[data-fam^="vdn"]{--k:var(--c-vdn);} .aoc[data-fam^="vdl"]{--k:var(--c-vdl);} .aoc[data-fam^="bul"]{--k:var(--c-bul);}
  .aoc:target{box-shadow:0 0 0 2px var(--k);}
  .aoc-top{display:flex;justify-content:space-between;gap:10px;align-items:baseline;}
  .aoc h4{margin:0;font-family:var(--serif);font-weight:500;font-size:19px;line-height:1.2;color:var(--title);}
  .reg{font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);font-weight:700;white-space:nowrap;}
  .fams{display:flex;flex-wrap:wrap;gap:5px;margin:8px 0;}
  .fam{font-size:10.5px;padding:2px 8px;border-radius:999px;border:1px solid color-mix(in srgb,var(--k) 55%,transparent);color:var(--k);background:color-mix(in srgb,var(--k) 10%,transparent);font-weight:600;}
  .nums{display:grid;gap:4px;margin:6px 0 8px;}
  .nums div{display:grid;grid-template-columns:130px 1fr;gap:8px;font-size:13px;}
  .nums dt{color:var(--faint);} .nums dd{margin:0;color:var(--title);font-weight:600;}
  .aoc-note{margin:0 0 10px;font-size:13.4px;line-height:1.55;color:var(--muted);}
  .grs{display:flex;flex-wrap:wrap;gap:4px;padding-top:8px;border-top:1px dashed var(--hair);}
  .gr{font-size:11.6px;padding:2px 7px;border-radius:6px;background:var(--track);color:var(--parchment);}
  .gr.p{font-weight:700;color:var(--title);} .gr.a{font-style:italic;color:var(--muted);} .gr.c{text-decoration:underline dotted;text-underline-offset:3px;}
  .gr.ad{opacity:.55;}
  .ixp{padding:16px 18px;} .ix-bar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:12px;}
  #ixq{flex:1 1 220px;min-width:0;padding:9px 14px;border-radius:999px;border:1px solid var(--hair-hi);background:var(--track);color:var(--title);font:14px var(--sans);}
  .fbs{display:flex;flex-wrap:wrap;gap:6px;}
  .fb{font:600 11.5px var(--sans);padding:6px 11px;border-radius:999px;border:1px solid var(--hair);background:transparent;color:var(--k,var(--gold-soft));cursor:pointer;}
  .fb.on{background:color-mix(in srgb,var(--k,var(--gold)) 20%,transparent);border-color:var(--k,var(--gold));}
  .ixs{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:4px 14px;}
  .ix{display:flex;justify-content:space-between;gap:8px;padding:5px 8px;border-radius:8px;text-decoration:none;font-size:13.5px;color:var(--title);}
  .ix:hover{background:var(--track);} .ix small{color:var(--faint);font-size:11px;white-space:nowrap;} .ix.hide{display:none;}
  .ladp{margin-top:12px;padding:18px 20px;}
  .when{display:grid;grid-template-columns:1fr 70px 1fr;gap:10px;align-items:stretch;margin:4px 0 6px;}
  .wh{padding:14px 16px;border-radius:14px;background:var(--track);border-left:3px solid var(--k);}
  .wh-must{--k:#6b8f4e;} .wh-wine{--k:var(--gold);}
  .wh-step{display:block;font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--k);font-weight:700;margin-bottom:4px;}
  .wh b{display:block;font-family:var(--serif);font-weight:500;font-size:17px;color:var(--title);margin-bottom:4px;}
  .wh p{margin:0 0 6px;font-size:13.4px;line-height:1.55;color:var(--muted);}
  .wh small{font-size:12px;color:var(--title);font-weight:600;}
  .wh-arrow{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px;}
  .wh-arrow svg{width:56px;height:22px;fill:none;stroke:var(--gold);stroke-width:2;stroke-linecap:round;stroke-linejoin:round;}
  .wh-arrow small{font-size:10.5px;color:var(--faint);}
  .ladp .note{margin-bottom:14px;}
  .ladder{display:grid;gap:3px;}
  .ld{display:grid;grid-template-columns:minmax(150px,250px) 1fr;gap:12px;align-items:center;text-decoration:none;}
  .ld-n{font-size:12.5px;color:var(--title);text-align:right;line-height:1.2;}
  .ld-t{position:relative;height:16px;border-radius:5px;background:var(--track);}
  .ld-b{position:absolute;left:0;top:0;bottom:0;border-radius:5px;background:var(--k);opacity:.85;}
  .ld-v{position:absolute;right:6px;top:0;font-size:11px;line-height:16px;color:var(--muted);font-weight:700;}
  .ld:hover .ld-b{opacity:1;}
  .ld.axis .ld-t{background:none;height:16px;border-top:1px solid var(--hair-hi);border-radius:0;}
  .ld-ticks span{position:absolute;top:2px;transform:translateX(-50%);font-size:10.5px;color:var(--faint);}
  .answer{border-color:var(--hair-hi);}
  .ran-box{border-left:3px solid var(--c-ran);}
  .mxp{margin-top:12px;padding:18px 20px;}
  .mx-wrap{overflow-x:auto;}
  .mx,.jt{width:100%;border-collapse:collapse;font-size:13px;}
  .mx th,.mx td,.jt th,.jt td{padding:8px 10px;border-bottom:1px solid var(--hair);text-align:left;vertical-align:top;}
  .mx tr:first-child th{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--gold);text-align:center;}
  .mx th b{display:block;color:var(--title);font-family:var(--serif);font-size:16px;font-weight:500;}
  .mx th small{display:block;color:var(--muted);font-weight:400;font-size:12px;line-height:1.45;max-width:440px;}
  .mx td{text-align:center;color:var(--c-vdn);font-size:16px;} .mx td.y{background:color-mix(in srgb,var(--c-vdn) 7%,transparent);}
  .gis{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px;margin-top:14px;}
  .gi{padding:12px 14px;border-radius:14px;border:1px solid var(--hair);background:var(--glass);}
  .gi-h{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px;}
  .gi-h b{font-family:var(--serif);font-weight:500;font-size:16.5px;color:var(--title);}
  .gi-h span{font-size:11px;font-weight:700;color:var(--gold);}
  .gi-l{display:flex;flex-wrap:wrap;gap:4px;} .gi-l a{font-size:11.5px;padding:2px 7px;border-radius:6px;background:var(--track);text-decoration:none;color:var(--muted);}
  .gi-l a:hover{color:var(--title);}
  .jaune .sec-head h2 em{color:var(--c-jau);}
  .jy-lede{border-left:3px solid var(--c-jau);}
  .jgrid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px;}
  .jc{padding:18px 20px;margin-top:12px;} .jgrid .jc{margin-top:0;}
  .jc p{font-size:14.4px;line-height:1.66;margin:0 0 10px;}
  .jsteps{border:none;background:none;padding:6px 0 0 22px;}
  .tl{position:relative;height:130px;margin:6px 8px 4px;}
  .tl-bar{position:absolute;left:0;right:0;top:56px;height:6px;border-radius:3px;background:var(--track);}
  .tl-veil{position:absolute;top:0;bottom:0;border-radius:3px;background:linear-gradient(90deg,color-mix(in srgb,var(--c-jau) 40%,transparent),var(--c-jau));}
  .tl-p{position:absolute;top:50px;transform:translateX(-50%);width:120px;text-align:center;}
  .tl-p.up{top:0;display:flex;flex-direction:column-reverse;}
  .tl-p.up .tl-d{margin:8px auto 2px;}
  .tl-p:nth-child(2){transform:none;text-align:left;} .tl-p:last-child{transform:translateX(-100%);text-align:right;}
  .tl-d{display:block;width:14px;height:14px;margin:2px auto 8px;border-radius:50%;background:var(--c-jau);box-shadow:0 0 0 3px color-mix(in srgb,var(--c-jau) 30%,transparent);}
  .tl-p:nth-child(2) .tl-d{margin-left:0;} .tl-p:last-child .tl-d{margin-right:0;}
  .tl-p small{font-size:11.5px;line-height:1.3;color:var(--muted);display:block;}
  .clav-row{display:grid;grid-template-columns:170px 1fr;gap:14px;align-items:center;}
  .clav{width:100%;height:auto;}
  .clav .glass{fill:color-mix(in srgb,var(--c-jau) 8%,transparent);stroke:var(--title);stroke-width:1.6;}
  .clav .wine{fill:var(--c-jau);opacity:.75;} .clav .cap{fill:var(--gold);}
  .clav .dim{stroke:var(--faint);stroke-width:1;} .clav .dt{fill:var(--muted);font:12px var(--sans);} .clav .dt.c{text-anchor:middle;}
  .clav .lbl{fill:#2a1a00;font:700 15px var(--sans);text-anchor:middle;}
  .angels{margin-top:10px;} .an-bar{display:flex;height:14px;border-radius:7px;overflow:hidden;border:1px solid var(--hair);}
  .an-fill{background:var(--c-jau);} .an-gone{background:repeating-linear-gradient(45deg,var(--track) 0 6px,transparent 6px 12px);}
  .an-leg{display:flex;justify-content:space-between;gap:8px;font-size:11.5px;color:var(--muted);margin-top:5px;} .an-leg b{color:var(--title);}
  .law{margin:0;padding-left:18px;font-size:13.8px;line-height:1.6;} .law li{margin-bottom:8px;} .law b{color:var(--title);}
  .jt th{color:var(--title);font-family:var(--serif);font-weight:500;font-size:15px;white-space:nowrap;}
  .jt tr:first-child th{font-family:var(--sans);font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--gold);}
  .jt small{font-size:12.5px;color:var(--muted);}
  .sources-list{margin:0;padding-left:26px;font-size:13px;line-height:1.6;color:var(--muted);columns:2;column-gap:34px;}
  .sources-list li{break-inside:avoid;margin-bottom:6px;}
  .sources-list li:target{color:var(--title);background:color-mix(in srgb,var(--gold) 14%,transparent);border-radius:6px;}
  .sources-list a{color:var(--gold);}
  .method-note{font-size:12.5px;color:var(--faint);line-height:1.6;margin:14px 0 0;}
  @media (max-width:900px){
    .keys{grid-template-columns:repeat(2,minmax(0,1fr));} .sources-list{columns:1;}
    .two,.method,.jgrid{grid-template-columns:1fr;} .ys{grid-template-columns:1fr 1fr;}
  }
  @media (max-width:620px){
    .when{grid-template-columns:1fr;} .wh-arrow svg{transform:rotate(90deg);}
    .ld{grid-template-columns:1fr;gap:2px;} .ld-n{text-align:left;} .ld.axis .ld-n{display:none;}
    .clav-row{grid-template-columns:1fr;} .clav{max-width:220px;margin:0 auto;}
    .st{grid-template-columns:80px 1fr;} .st small{grid-column:1/-1;}
    .tl{height:auto;display:grid;gap:8px;} .tl-bar{display:none;} .tl-p,.tl-p:nth-child(2),.tl-p:last-child{position:static;transform:none;width:auto;text-align:left;display:flex;gap:8px;align-items:center;}
    .tl-d{margin:0!important;flex:none;} .tl-p.up{flex-direction:row;}
    .aocs{grid-template-columns:1fr;} .ys{grid-template-columns:1fr;}
  }
  @media (max-width:420px){ .keys{grid-template-columns:1fr;} .nums div{grid-template-columns:1fr;gap:0;} }
'''

TEMPLATE = '''<!DOCTYPE html>
<html lang="fr">
<head>
<!--fw-theme:start--><script src="../../assets/theme.js"></script><!--fw-theme:end-->
<!--fw-favicon:start--><link rel="icon" href="../../favicon.ico" sizes="48x48"><link rel="icon" type="image/png" href="../../assets/favicon.png" sizes="192x192"><link rel="apple-touch-icon" href="../../apple-touch-icon.png"><!--fw-favicon:end-->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Douce France…</title>
<meta name="description" content="Les vins doux, mutés et oxydatifs de France : pourriture noble, passerillage, vendanges tardives, vin de paille, vins doux naturels, vins de liqueur, rancio, et le vin jaune. Toutes les AOC, leurs règles et leurs cépages.">
<style>
@@BASE_CSS@@
@@CSS@@
</style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <a class="back" href="../../index.html" data-fr="← Retour" data-en="← Back">← Retour</a>
    <button class="lang" id="langbtn" type="button" aria-label="Language">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 3.8 5.8 3.8 9S14.5 18.5 12 21C9.5 18.5 8.2 15.2 8.2 12S9.5 5.5 12 3Z"/></svg>
      <span id="langlbl">English</span>
    </button>
  </div>

  <header>
    <p class="eyebrow" data-fr="Vins doux, mutés et oxydatifs" data-en="Sweet, fortified and oxidative wines">Vins doux, mutés et oxydatifs</p>
    <h1 data-fr="Douce <em>France…</em>" data-en="Sweet <em>France…</em>">Douce <em>France…</em></h1>
    <div class="rule"></div>
    @@TAGLINE@@
    <div class="keys">@@KEYS@@</div>
    <nav class="toc">@@TOC@@</nav>
  </header>

@@SECTIONS@@

@@JAUNE@@

  <footer id="sources">
    <h3 data-fr="Sources" data-en="Sources">Sources</h3>
    <ol class="sources-list">@@SOURCES@@</ol>
    @@METHOD@@
  </footer>
</div>
<script>
(function(){
  var LANG = 'fr';
  try{ var s = localStorage.getItem('fw_lang'); if(s==='fr'||s==='en') LANG = s; }catch(e){}
  var $ = function(id){ return document.getElementById(id); };
  function applyLang(){
    document.documentElement.lang = LANG;
    document.title = LANG==='fr' ? 'Douce France…' : 'Sweet France…';
    var nodes = document.querySelectorAll('[data-fr]');
    for(var i=0;i<nodes.length;i++){ var v = nodes[i].getAttribute('data-'+LANG); if(v!==null) nodes[i].innerHTML = v; }
    var q = $('ixq'); if(q) q.placeholder = q.getAttribute('data-ph-'+LANG);
    $('langlbl').textContent = LANG==='fr' ? 'English' : 'Français';
  }
  $('langbtn').addEventListener('click', function(){
    LANG = LANG==='fr' ? 'en' : 'fr';
    try{ localStorage.setItem('fw_lang', LANG); }catch(e){}
    applyLang();
  });
  document.addEventListener('fw:lang', function(e){
    var l = (e.detail && e.detail.lang) || document.documentElement.lang;
    if((l==='fr'||l==='en') && l!==LANG){ LANG = l; applyLang(); }
  });
  applyLang();
  // AOC index: family buttons + text search
  var fam = 'all', q = $('ixq'), items = document.querySelectorAll('#ixs .ix'), btns = document.querySelectorAll('.fb');
  function norm(s){ return s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').toLowerCase(); }
  function filter(){
    var w = norm(q.value.trim());
    for(var i=0;i<items.length;i++){
      var it = items[i], okF = fam==='all' || (' '+it.getAttribute('data-fam')+' ').indexOf(' '+fam+' ')>=0;
      var okQ = !w || norm(it.textContent).indexOf(w)>=0;
      it.classList.toggle('hide', !(okF && okQ));
    }
  }
  for(var b=0;b<btns.length;b++) btns[b].addEventListener('click', function(){
    fam = this.getAttribute('data-f');
    for(var j=0;j<btns.length;j++) btns[j].classList.toggle('on', btns[j]===this);
    filter();
  });
  q.addEventListener('input', filter);
  if(location.hash){
    var tgt = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if(tgt) setTimeout(function(){ tgt.scrollIntoView({block:'start'}); }, 0);
  }
})();
</script>
</body>
</html>
'''


def main():
    toc = ''.join(f'<a href="#{i}">{t((fr, en))}</a>' for i, fr, en in TOC)
    rep = {
        '@@BASE_CSS@@': base_css(),
        '@@CSS@@': CSS,
        '@@TAGLINE@@': t(('Liquoreux botrytisés, raisins passerillés, vendanges tardives, vins de paille, vins doux naturels, vins de liqueur, rancios… et, pour finir, le vin jaune. Méthode par méthode, toutes les appellations françaises, leurs règles et leurs cépages, tirés des cahiers des charges en vigueur (survolez ou touchez les petits numéros pour la source).',
                          'Botrytised sweet wines, dried grapes, late harvests, straw wines, vins doux naturels, liqueur wines, rancios… and, to finish, vin jaune. Method by method, every French appellation, its rules and its grapes, taken from the specifications in force (hover over or tap the small numbers for the source).'), 'p', 'tagline'),
        '@@KEYS@@': keys_html(),
        '@@TOC@@': toc,
        '@@SECTIONS@@': '\n'.join(SECTIONS),
        '@@JAUNE@@': JAUNE_SEC,
        '@@SOURCES@@': sources_html(),
        '@@METHOD@@': t(('Méthode : chiffres relevés dans les cahiers des charges (versions locales et publiées au BO Agri jusqu’en 2026) ; seuils = minimums légaux. Les cépages viennent des mêmes textes, via la base « Cépages & Appellations » du site. Page rédigée en 2026 · ©&nbsp;2026 Christophe A. Paul.',
                         'Method: figures taken from the product specifications (versions published in the BO Agri up to 2026); thresholds = legal minimums. Grapes come from the same texts, via the site’s “Grapes & Appellations” database. Page written in 2026 · ©&nbsp;2026 Christophe A. Paul.'), 'p', 'method-note'),
    }
    html = TEMPLATE
    for k, v in rep.items():
        html = html.replace(k, v)
    assert '@@' not in html, html[html.index('@@'):html.index('@@') + 40]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html)
    used = {int(m.group(1)) for m in re.finditer(r'href="#src-(\d+)"', html)}
    unused = [k for k, n_ in NUM.items() if n_ not in used]
    print(f'{OUT.relative_to(INFOS.parent)}: {len(html) // 1024} KB, {len(AOC)} AOC cards + {len(JAUNE)} vin jaune, {len(SOURCES)} sources, unused: {unused}')


if __name__ == '__main__':
    main()
