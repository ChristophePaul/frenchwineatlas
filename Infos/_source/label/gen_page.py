"""Builds Infos/Wine_Label/Wine_Label.html — « Apprendre à lire… une étiquette » / "Learning to read… a wine label".

Source: the user's « How to Read a French Wine Label.pdf » (2010, A quick Glance at French Wine/): two annotated labels
(Château Figeac 1988 = Bordeaux & most French labels — replaced 2026-10-15 by the user's imaginary « Château Blabla 1989 » label, img/label_bordeaux_blabla.webp, to avoid rights issues; Aloxe-Corton likewise replaced by « Domaine Coullenot, Beaune 1er Cru Les Grèves 2019 », img/label_bourgogne_coullenot.webp; Aloxe-Corton 1er Cru Les Vercots = Burgundy & the rest).
Kept: the two labels and their call-outs (now numbered hotspots). Added: what a label must / may carry today,
the 85 % rules, sweetness terms, Champagne producer codes and a small glossary — each with its source.
Shared look = Vine & Vineyard base.css. Run:  python3 gen_page.py   (then assets/theme_apply.py on the output)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INFOS = HERE.parent.parent
sys.path.insert(0, str(INFOS / 'Vine_and_Vineyard' / '_source'))
from common import base_css  # noqa: E402

OUT = INFOS / 'Wine_Label' / 'Wine_Label.html'


def att(s):
    return s.replace('&', '&amp;').replace('"', '&quot;')


def dl(fr, en, tag='span', cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c} data-fr="{att(fr)}" data-en="{att(en)}">{fr}</{tag}>'


def LL(fr, en, tag='p', cls=''):
    """long text: both languages in the page, CSS shows the right one"""
    c = (' ' + cls) if cls else ''
    return f'<{tag} class="L fr{c}">{fr}</{tag}><{tag} class="L en{c}">{en}</{tag}>'


# ------------------------------------------------------------------ sources
SOURCES = [
    ('r1308', 'Règlement (UE) n° 1308/2013 portant organisation commune des marchés, art. 119 et 120 (mentions obligatoires et facultatives des vins). <a href="https://eur-lex.europa.eu/eli/reg/2013/1308/oj" target="_blank" rel="noopener">EUR-Lex</a>',
              'Regulation (EU) No 1308/2013 establishing a common organisation of the markets, Art. 119 and 120 (compulsory and optional particulars for wine). <a href="https://eur-lex.europa.eu/eli/reg/2013/1308/oj" target="_blank" rel="noopener">EUR-Lex</a>'),
    ('r2019', 'Règlement délégué (UE) 2019/33 de la Commission : présentation et étiquetage des vins (même champ visuel, tolérance de ±0,5 % vol, millésime et cépage à 85 %, teneur en sucre). <a href="https://eur-lex.europa.eu/eli/reg_del/2019/33/oj" target="_blank" rel="noopener">EUR-Lex</a>',
              'Commission Delegated Regulation (EU) 2019/33: presentation and labelling of wine (same field of vision, ±0.5 % vol tolerance, 85 % vintage and variety rules, sugar content). <a href="https://eur-lex.europa.eu/eli/reg_del/2019/33/oj" target="_blank" rel="noopener">EUR-Lex</a>'),
    ('r2117', 'Règlement (UE) 2021/2117 : liste des ingrédients et déclaration nutritionnelle des vins produits à partir du 8 décembre 2023 (valeur énergétique sur l’étiquette, le reste possible par voie électronique). <a href="https://eur-lex.europa.eu/eli/reg/2021/2117/oj" target="_blank" rel="noopener">EUR-Lex</a>',
              'Regulation (EU) 2021/2117: list of ingredients and nutrition declaration for wines produced from 8 December 2023 (energy value on the label, the rest may be given electronically). <a href="https://eur-lex.europa.eu/eli/reg/2021/2117/oj" target="_blank" rel="noopener">EUR-Lex</a>'),
    ('r1169', 'Règlement (UE) n° 1169/2011 (information des consommateurs), annexe II : allergènes, dont l’anhydride sulfureux et les sulfites au-delà de 10 mg/L — mention « contient des sulfites » obligatoire sur les vins depuis 2005 (directive 2003/89/CE).',
              'Regulation (EU) No 1169/2011 (food information to consumers), Annex II: allergens, including sulphur dioxide and sulphites above 10 mg/L — “contains sulphites” compulsory on wine since 2005 (Directive 2003/89/EC).'),
    ('d2011', 'Directive 2011/91/UE relative aux mentions permettant d’identifier le lot auquel appartient une denrée alimentaire.',
              'Directive 2011/91/EU on indications or marks identifying the lot to which a foodstuff belongs.'),
    ('csp', 'Code de la santé publique, art. L. 3322-2, et arrêté du 2 octobre 2006 : message sanitaire à destination des femmes enceintes (pictogramme), obligatoire depuis octobre 2007.',
            'French Public Health Code, Art. L. 3322-2, and order of 2 October 2006: health warning for pregnant women (pictogram), compulsory since October 2007.'),
    ('decret', 'Décret n° 2012-655 du 4 mai 2012 relatif à l’étiquetage et à la traçabilité des produits vitivinicoles (termes « château », « clos », « cru » ; mise en bouteille à la propriété), codifié au code rural et de la pêche maritime.',
               'French Decree No. 2012-655 of 4 May 2012 on the labelling and traceability of wine products (the terms “château”, “clos”, “cru”; estate bottling), codified in the Rural and Maritime Fishing Code.'),
    ('bio', 'Règlement (UE) 2018/848 relatif à la production biologique, art. 30 à 33 : termes « bio », logo de production biologique de l’Union européenne, numéro de code de l’organisme certificateur et lieu de production des matières premières.',
            'Regulation (EU) 2018/848 on organic production, Art. 30 to 33: the “organic” terms, the EU organic production logo, the code number of the control body and the place where the raw materials were farmed.'),
    ('stemi', 'INAO, classement des vins de l’appellation « Saint-Émilion Grand Cru » (1955, révisé ; classement 2022, homologué le 7 septembre 2022). Voir aussi la page « Les classements » du site.',
              'INAO, classification of the wines of the “Saint-Émilion Grand Cru” appellation (1955, revised; 2022 classification, approved on 7 September 2022). See also this site’s “Classifications” page.'),
    ('pomerol', 'Cahier des charges de l’AOC « Pomerol », homologué par l’arrêté du 12 octobre 2021, chapitre I, XII b (unité géographique plus grande « Vin de Bordeaux » / « Grand Vin de Bordeaux »). Voir la bibliothèque des décrets du site.',
                'Specification of the “Pomerol” AOC, approved by order of 12 October 2021, chapter I, XII b (larger geographical unit “Vin de Bordeaux” / “Grand Vin de Bordeaux”). See this site’s decree library.'),
    ('champ', 'Cahier des charges de l’AOC « Champagne », homologué par l’arrêté du 31 juillet 2025 : couleurs et blanc de blancs, mise en marché après 15 mois (36 mois pour les millésimés), millésime sur le bouchon, élaborateur en toutes lettres, immatriculations du Comité Champagne. Voir la bibliothèque des décrets du site.',
              'Specification of the “Champagne” AOC, approved by order of 31 July 2025: colours and blanc de blancs, release after 15 months (36 months for vintage wines), vintage on the cork, producer named in full, Comité Champagne registration codes. See this site’s decree library.'),
    ('bivb', 'Bureau interprofessionnel des vins de Bourgogne (BIVB), la hiérarchie des appellations (régionales, villages, premiers crus, grands crus) ; UNESCO (2015), « Les Climats du vignoble de Bourgogne », patrimoine mondial.',
             'Bourgogne Wine Board (BIVB), the hierarchy of appellations (regional, village, premier cru, grand cru); UNESCO (2015), “The Climats, terroirs of Burgundy”, World Heritage.'),
    ('tt', 'Règlement (UE) n° 1308/2013, art. 112 et 113 : les mentions traditionnelles, termes protégés réservés aux vins AOP et IGP ; registre européen eAmbrosia. <a href="https://ec.europa.eu/agriculture/eambrosia/" target="_blank" rel="noopener">eAmbrosia</a>',
           'Regulation (EU) No 1308/2013, Art. 112 and 113: traditional terms, protected terms reserved for PDO and PGI wines; EU eAmbrosia register. <a href="https://ec.europa.eu/agriculture/eambrosia/" target="_blank" rel="noopener">eAmbrosia</a>'),
    ('cdcmt', 'Cahiers des charges des AOC « Muscadet », « Muscadet Sèvre et Maine », « Muscadet Côtes de Grandlieu » et « Gros Plant du Pays nantais » (sur lie) ; « Beaujolais », « Touraine », « Mâcon » (primeur) ; « Alsace », « Alsace grand cru », « Jurançon », « Gaillac » (vendanges tardives) ; « Coteaux du Layon », « Coteaux de l’Aubance », « Monbazillac » (sélection de grains nobles) ; « Bordeaux » (version 2025) et « Bourgogne » (clairet). Voir la bibliothèque des décrets du site.',
              'Specifications of the “Muscadet”, “Muscadet Sèvre et Maine”, “Muscadet Côtes de Grandlieu” and “Gros Plant du Pays nantais” AOCs (sur lie); “Beaujolais”, “Touraine”, “Mâcon” (primeur); “Alsace”, “Alsace grand cru”, “Jurançon”, “Gaillac” (vendanges tardives); “Coteaux du Layon”, “Coteaux de l’Aubance”, “Monbazillac” (sélection de grains nobles); “Bordeaux” (2025 version) and “Bourgogne” (clairet). See this site’s decree library.'),
    ('bio2', 'Règlement (UE) 2018/848, annexe II, partie VI (règles de production du vin biologique : pratiques interdites ou limitées, teneurs maximales en anhydride sulfureux) ; règlement d’exécution (UE) 2021/1165 (produits et substances autorisés). Le « vin biologique » existe depuis le millésime 2012 (règlement d’exécution (UE) n° 203/2012) ; auparavant, on ne pouvait écrire que « vin issu de raisins de l’agriculture biologique ».',
             'Regulation (EU) 2018/848, Annex II, Part VI (production rules for organic wine: prohibited or restricted practices, maximum sulphur dioxide levels); Implementing Regulation (EU) 2021/1165 (authorised products and substances). “Organic wine” has existed since the 2012 vintage (Implementing Regulation (EU) No 203/2012); before that, labels could only say “wine made from organically grown grapes”.'),
    ('ab', 'Ministère de l’Agriculture et Agence Bio : la marque « AB – Agriculture biologique », propriété de l’État, d’usage facultatif, soumise aux mêmes règles que le logo européen. <a href="https://www.agencebio.org" target="_blank" rel="noopener">Agence Bio</a>',
           'French Ministry of Agriculture and Agence Bio: the “AB – Agriculture biologique” mark, owned by the State, optional, subject to the same rules as the EU logo. <a href="https://www.agencebio.org" target="_blank" rel="noopener">Agence Bio</a>'),
    ('nature', 'Syndicat de défense des vins nature’l, charte « Vin méthode nature » (2020) ; certification environnementale des exploitations « Haute Valeur Environnementale » (HVE), ministère de l’Agriculture ; Demeter et Biodyvin, cahiers des charges privés de la biodynamie.',
               'Syndicat de défense des vins nature’l, “Vin méthode nature” charter (2020); “Haute Valeur Environnementale” (HVE) farm environmental certification, French Ministry of Agriculture; Demeter and Biodyvin, private biodynamic standards.'),
    ('civc', 'Comité Champagne : immatriculation professionnelle portée sur l’étiquette (NM, RM, CM, RC, SR, ND, MA).',
             'Comité Champagne: the professional registration code printed on the label (NM, RM, CM, RC, SR, ND, MA).'),
]
SIDX = {k: i + 1 for i, (k, _, _) in enumerate(SOURCES)}


def r(*keys):
    return '<sup class="ref">' + ','.join(f'<a href="#src-{k}">{SIDX[k]}</a>' for k in keys) + '</sup>'


# ------------------------------------------------------------------ the two labels
# call-out = (tip x %, tip y %, side L/R/B (optionally '@y' = preferred box height in %), short FR, short EN, long FR, long EN, mandatory?)
# the tip is a point in blank space right next to the text (measured on a grid), never on the writing
def lot_spot(x, y, side, fr_here, en_here):
    """The lot number call-out, the same « L0001-01 » on the three labels; fr_here/en_here = where it sits on that bottle."""
    return (x, y, side, 'Numéro de lot', 'Lot number',
            '« L0001-01 » : le numéro de lot, obligatoire. Il désigne l’ensemble des bouteilles produites et mises en bouteille dans les mêmes conditions — souvent la même cuve, le même jour de tirage. '
            'Sa raison d’être est la traçabilité : en cas de défaut ou de rappel, on retrouve et retire exactement les bouteilles concernées, et le producteur remonte jusqu’à la cuve et à la date de mise en bouteille. '
            'Il est en général précédé d’un « L » ; le reste du code est libre (année, jour, cuve…). '
            'Où le trouver : sur l’étiquette ou la contre-étiquette, mais très souvent aussi imprimé ou gravé directement sur le verre, en bas de la bouteille ou près du col. Il n’a pas à figurer dans le même champ visuel que les autres mentions. ' + fr_here + r('d2011'),
            '“L0001-01”: the lot number, compulsory. It identifies all the bottles produced and bottled under the same conditions — often the same vat, the same bottling day. '
            'Its purpose is traceability: if there is a fault or a recall, exactly the bottles concerned can be found and withdrawn, and the producer can trace them back to the vat and the bottling date. '
            'It usually starts with an “L”; the rest of the code is up to the producer (year, day, vat…). '
            'Where to find it: on the label or the back label, but very often printed or etched straight onto the glass, at the bottom of the bottle or near the neck. It need not be in the same field of vision as the other statements. ' + en_here + r('d2011'), 1)


BX = [
    (86.5, 5.9, 'R', 'Unité géographique plus grande', 'Larger geographical unit',
     '« Grand Vin de Bordeaux » : beaucoup de cahiers des charges bordelais (celui de Pomerol, par exemple) autorisent « Vin de Bordeaux » ou « Grand Vin de Bordeaux », en caractères pas plus grands que les deux tiers de ceux du nom de l’appellation — c’est le cas ici. Malgré le mot « grand », ce n’est pas un gage de qualité.' + r('pomerol'),
     '“Grand Vin de Bordeaux”: many Bordeaux specifications (Pomerol’s, for example) allow “Vin de Bordeaux” or “Grand Vin de Bordeaux”, in letters no larger than two thirds of those of the appellation name — as here. Despite the word “grand”, it is no guarantee of quality.' + r('pomerol'), 0),
    (84, 30, 'R', 'Illustration', 'Illustration',
     'La gravure du château, des armoiries, un sceau… : purement décoratif, et entièrement libre.',
     'An engraving of the château, a coat of arms, a seal…: purely decorative, and entirely up to the producer.', 0),
    (25, 52.5, 'L', 'Nom de la propriété (château, domaine ou clos)', 'Name of the property (château, domaine or clos)',
     'Le nom de l’exploitation, ici le château. En France, le mot « château » est réservé aux vins d’appellation issus d’une exploitation qui existe réellement sous ce nom, de raisins récoltés dans ses vignes et vinifiés sur place. Selon la région, on lit aussi « domaine » (en Bourgogne notamment) ou « clos », une vigne close, à l’origine entourée de murs.' + r('decret'),
     'The name of the estate, here the château. In France the word “château” is reserved for appellation wines from a holding that really exists under that name, made from grapes harvested in its vineyards and vinified there. Depending on the region, you will also read “domaine” (in Burgundy especially) or “clos”, an enclosed vineyard, originally walled.' + r('decret'), 0),
    (14.5, 65.3, 'L', 'Classement (s’il existe)', 'Classification (if any)',
     '« Premier Grand Cru Classé » renvoie au classement des vins de Saint-Émilion, créé en 1955 et révisé environ tous les dix ans (le dernier date de 2022). Le classement porte sur le château, pas sur l’appellation, et il est réservé aux vins de l’AOC « Saint-Émilion Grand Cru » — celle qu’indique la petite ligne de l’étiquette.' + r('stemi'),
     '“Premier Grand Cru Classé” refers to the Saint-Émilion classification, created in 1955 and revised roughly every ten years (the latest dates from 2022). The classification applies to the château, not to the appellation, and it is reserved for wines of the “Saint-Émilion Grand Cru” AOC — the one named on the label’s small line.' + r('stemi'), 0),
    (70, 72.7, 'R@68', 'Appellation', 'Appellation',
     'Le nom du lieu, en grand. Attention : « Saint-Émilion » est écrit en gros, mais l’appellation exacte est celle de la petite ligne en dessous : Saint-Émilion Grand Cru, une AOC distincte de Saint-Émilion, aux règles plus strictes.',
     'The name of the place, in large letters. Careful: “Saint-Émilion” is printed large, but the exact appellation is the one on the small line below: Saint-Émilion Grand Cru, a separate AOC from Saint-Émilion, with stricter rules.', 1),
    (82.4, 77, 'R@77', 'Nom officiel de l’appellation', 'Official name of the appellation',
     '« Appellation Saint-Émilion Grand Cru Contrôlée » : la mention légale, qui donne le nom exact de l’AOC. Aujourd’hui on peut écrire « Appellation d’Origine Contrôlée » ou « Appellation d’Origine Protégée ».' + r('r1308'),
     '“Appellation Saint-Émilion Grand Cru Contrôlée”: the legal statement, giving the exact name of the AOC. Today the label may say “Appellation d’Origine Contrôlée” or “Appellation d’Origine Protégée”.' + r('r1308'), 1),
    (57, 81.5, 'R@85.5', 'Millésime', 'Vintage',
     'L’année de la récolte. Facultatif, mais s’il est indiqué, au moins 85 % des raisins doivent provenir de cette année-là.' + r('r2019'),
     'The year of the harvest. Optional, but when it is shown at least 85 % of the grapes must come from that year.' + r('r2019'), 0),
    (27.5, 88.3, 'L@84', 'Lieu de mise en bouteille', 'Place of bottling',
     '« Mis en bouteille au château » : le vin a été mis en bouteille sur la propriété qui a produit les raisins et fait le vin. C’est une mention facultative — ce qui est obligatoire, c’est le nom de l’embouteilleur.' + r('decret'),
     '“Mis en bouteille au château” (estate bottled): the wine was bottled at the property that grew the grapes and made the wine. This statement is optional — what is compulsory is the name of the bottler.' + r('decret'), 0),
    (66, 94.3, 'B', 'Nom du propriétaire', 'Owner’s name',
     '« A. Califourchon, Propriétaire à Saint-Émilion, France » : le nom et la commune de l’embouteilleur, mention obligatoire. « Propriétaire » précise son statut : le vin vient de ses propres vignes (un négociant, lui, achète raisins ou vins).' + r('r2019'),
     '“A. Califourchon, Propriétaire à Saint-Émilion, France”: the name and town of the bottler, a compulsory statement. “Propriétaire” (owner) gives his status: the wine comes from his own vines (a négociant, by contrast, buys grapes or wines).' + r('r2019'), 1),
    (38.8, 94.6, 'B', 'Pays d’origine', 'Country of origin',
     '« Produce of France » : la provenance est obligatoire (« Produit de France » ; pour l’export, souvent en anglais).' + r('r1308'),
     '“Produce of France”: the provenance is compulsory (“Produit de France”; often in English for export).' + r('r1308'), 1),
    (9, 89.6, 'L@92', 'Teneur en alcool', 'Alcohol content',
     'Le titre alcoométrique en « % vol ». Obligatoire, à ±0,5 % vol près.' + r('r2019'),
     'The alcoholic strength, in “% vol”. Compulsory, accurate to within ±0.5 % vol.' + r('r2019'), 1),
    (91.8, 95.5, 'B', 'Contenance', 'Bottle size',
     'Le volume nominal (750 ml = 75 cl, la bouteille standard). Obligatoire.' + r('r1308'),
     'The nominal volume (750 ml = 75 cl, the standard bottle). Compulsory.' + r('r1308'), 1),
    lot_spot(12.2, 94.6, 'B', 'Ici, il est imprimé sous le degré d’alcool. Sur une vraie bouteille de 1989, il n’y serait sans doute pas : il n’est devenu obligatoire qu’au début des années 1990 (directive 89/396/CEE).',
             'Here it is printed under the alcohol content. A real 1989 bottle would probably not have one: it only became compulsory in the early 1990s (Directive 89/396/EEC).'),
]
BG = [
    (67, 22, 'R', 'Illustration', 'Illustration',
     'Des armoiries — ici fantaisistes : un verre, un tire-bouchon et un bouffon. Purement décoratif, et entièrement libre.',
     'A coat of arms — a whimsical one here: a glass, a corkscrew and a jester. Purely decorative, and entirely up to the producer.', 0),
    (14.5, 73.3, 'L', 'Nom du domaine', 'Name of the domaine',
     '« Domaine Coullenot » : en Bourgogne on parle de domaine plutôt que de château — l’ensemble des vignes d’un même producteur, souvent au nom de la famille. Il est placé ici sous l’appellation : en Bourgogne, l’étiquette met volontiers le lieu en avant.',
     '“Domaine Coullenot”: in Burgundy one speaks of a domaine rather than a château — all the vines of a single producer, often under the family name. Here it sits below the appellation: Burgundy labels like to put the place first.', 0),
    (18, 49, 'L', 'Nom de l’appellation', 'Name of the appellation',
     'En Bourgogne, c’est souvent le village qui donne son nom au vin : ici Beaune. La hiérarchie va des appellations régionales (Bourgogne) aux villages, puis aux premiers crus et aux grands crus.' + r('bivb'),
     'In Burgundy the village often gives the wine its name: here Beaune. The hierarchy runs from regional appellations (Bourgogne) to villages, then premiers crus and grands crus.' + r('bivb'), 1),
    (57.3, 43.8, 'R@41', 'Classement', 'Classification',
     '« 1er Cru » : le vin vient d’un climat classé premier cru de Beaune ; l’appellation complète est « Beaune Premier Cru ». Beaune n’a pas de grand cru : le premier cru est le sommet de la commune.' + r('bivb'),
     '“1er Cru”: the wine comes from a climat classified as a Beaune premier cru; the full appellation is “Beaune Premier Cru”. Beaune has no grand cru: premier cru is the top of the commune.' + r('bivb'), 0),
    (64.5, 57.4, 'R@50', 'Nom du « climat »', 'Name of the “climat”',
     '« Les Grèves » est un climat — une parcelle nommée, délimitée depuis des siècles — classé premier cru de Beaune. Les Climats de Bourgogne sont inscrits au patrimoine mondial de l’UNESCO depuis 2015.' + r('bivb'),
     '“Les Grèves” is a climat — a named plot, mapped for centuries — classified as a Beaune premier cru. The Climats of Burgundy have been on UNESCO’s World Heritage list since 2015.' + r('bivb'), 0),
    (81.5, 62.2, 'R@59', 'Mention d’appellation', 'Appellation statement',
     '« Appellation Beaune 1er Cru Contrôlée » : la mention légale, qui donne le nom exact de l’AOC. Aujourd’hui on peut aussi écrire « Appellation d’Origine Protégée ».' + r('r1308'),
     '“Appellation Beaune 1er Cru Contrôlée”: the legal statement, giving the exact name of the AOC. Today the label may also say “Appellation d’Origine Protégée”.' + r('r1308'), 1),
    (57, 82, 'R@79', 'Millésime', 'Vintage',
     'L’année de la récolte : facultatif, mais au moins 85 % des raisins de cette année-là. En Bourgogne, il figure souvent sur la collerette, la petite étiquette du col ; ici, il est sur l’étiquette principale.' + r('r2019'),
     'The year of the harvest: optional, but at least 85 % of the grapes from that year. In Burgundy it is often printed on the neck label; here it is on the main label.' + r('r2019'), 0),
    (27, 87, 'L@76', 'Lieu de mise en bouteille', 'Place of bottling',
     '« Mis en bouteille au Domaine » : la version bourguignonne de « mis en bouteille au château » — le vin a été mis en bouteille par le domaine qui a fait le vin.' + r('decret'),
     '“Mis en bouteille au Domaine” (domaine bottled): the Burgundy version of “mis en bouteille au château” — the wine was bottled by the domaine that made it.' + r('decret'), 0),
    (17.5, 90.8, 'B', 'Nom et statut du producteur', 'Producer’s name and status',
     '« N. Coullenot, Propriétaire » : le nom de l’exploitant, suivi de son statut. « Propriétaire » : le vin vient des vignes du signataire. Un « négociant-éleveur » achète raisins, moûts ou vins pour les élever et les vendre sous son nom.',
     '“N. Coullenot, Propriétaire”: the grower’s name, followed by their status. “Propriétaire” (owner): the wine comes from the signatory’s own vines. A “négociant-éleveur” buys grapes, musts or wines to age and sell them under its own name.', 0),
    (82.4, 90.8, 'R@88', 'Adresse de l’embouteilleur', 'Bottler’s address',
     '« à Beaune “La Montagne” » : la commune (et ici le lieu-dit) de l’embouteilleur. Avec le nom « N. Coullenot », elle identifie l’embouteilleur : mention obligatoire.' + r('r2019'),
     '“à Beaune ‘La Montagne’”: the bottler’s town (and here its locality). Together with the name “N. Coullenot”, it identifies the bottler: compulsory.' + r('r2019'), 1),
    (34.5, 94.5, 'B', 'Pays d’origine', 'Country of origin',
     '« Produce of France » : la provenance est obligatoire (« Produit de France » ; pour l’export, souvent en anglais).' + r('r1308'),
     '“Produce of France”: the provenance is compulsory (“Produit de France”; often in English for export).' + r('r1308'), 1),
    (5.5, 91.4, 'B', 'Contenance', 'Bottle size',
     'Le volume nominal (750 ml = 75 cl, la bouteille standard). Obligatoire.' + r('r1308'),
     'The nominal volume (750 ml = 75 cl, the standard bottle). Compulsory.' + r('r1308'), 1),
    (89, 95.2, 'B', 'Teneur en alcool', 'Alcohol content',
     'Le titre alcoométrique en « % vol ». Obligatoire, à ±0,5 % vol près.' + r('r2019'),
     'The alcoholic strength, in “% vol”. Compulsory, accurate to within ±0.5 % vol.' + r('r2019'), 1),
    lot_spot(12.8, 94.4, 'B', 'Ici, il est imprimé sous la contenance.', 'Here it is printed under the bottle size.'),
]

CH = [
    (67, 22, 'R', 'Illustration', 'Illustration',
     'Les mêmes armoiries fantaisistes, cette fois avec une flûte de champagne. Purement décoratif.',
     'The same whimsical coat of arms, this time with a champagne flute. Purely decorative.', 0),
    (25, 45.5, 'L', 'Nom de l’appellation', 'Name of the appellation',
     '« Champagne » : le nom de l’appellation. Particularité, une exception propre au champagne : le seul mot « Champagne » suffit, sans la mention « Appellation d’Origine Contrôlée ».' + r('champ'),
     '“Champagne”: the name of the appellation. A peculiarity, an exception specific to champagne: the word “Champagne” alone is enough, without the words “Appellation d’Origine Contrôlée”.' + r('champ'), 1),
    (84.5, 57, 'R', 'Marque', 'Brand',
     '« Bubulle » : la marque de la maison. En Champagne, on achète souvent une marque plutôt qu’un lieu : la plupart des champagnes assemblent des raisins de nombreuses communes.' + r('champ'),
     '“Bubulle”: the house’s brand. In Champagne you often buy a brand rather than a place: most champagnes blend grapes from many villages.' + r('champ'), 0),
    (22.5, 72.7, 'L', 'Teneur en sucre', 'Sugar content',
     '« Brut » : moins de 12 g de sucre par litre. Pour un vin mousseux, cette mention est obligatoire (voir le tableau du sucre plus bas).' + r('r2019'),
     '“Brut”: less than 12 g of sugar per litre. For a sparkling wine this statement is compulsory (see the sugar table below).' + r('r2019'), 1),
    (77.5, 72.7, 'R', 'Blanc de blancs', 'Blanc de blancs',
     'Élaboré uniquement à partir de raisins blancs — en Champagne, essentiellement le chardonnay. À l’inverse, un « blanc de noirs » vient seulement de raisins noirs (pinot noir, meunier).' + r('champ'),
     'Made only from white grapes — in Champagne, essentially chardonnay. Conversely, a “blanc de noirs” comes only from black grapes (pinot noir, meunier).' + r('champ'), 0),
    (58.5, 79.3, 'R', 'Millésime', 'Vintage',
     'Un champagne millésimé : il ne peut être mis en vente qu’au moins 36 mois après le tirage en bouteille (15 mois pour un champagne sans millésime), et l’année doit aussi figurer sur le bouchon. La plupart des champagnes sont sans millésime, assemblés avec des vins de réserve.' + r('champ'),
     'A vintage champagne: it may be sold no earlier than 36 months after bottling (15 months for a non-vintage champagne), and the year must also appear on the cork. Most champagnes are non-vintage, blended with reserve wines.' + r('champ'), 0),
    (5.6, 89, 'L', 'Propriétaire : nom et adresse', 'Owner: name and address',
     '« Élaboré par S.A. Champagne Bubulle, Reims, France » : le nom de l’élaborateur, en toutes lettres, et sa commune. Pour un vin mousseux, c’est le producteur (ou le vendeur) qui doit figurer. Mention obligatoire.' + r('r2019', 'champ'),
     '“Élaboré par S.A. Champagne Bubulle, Reims, France” (made by): the producer’s name, in full, and its town. For a sparkling wine, it is the producer (or the vendor) that must be shown. Compulsory.' + r('r2019', 'champ'), 1),
    (94.5, 89, 'R', 'Code du producteur', 'Producer code',
     '« NM 312-00300 » : le numéro d’immatriculation du Comité Champagne, exigé par le cahier des charges. Les deux lettres disent qui a élaboré le vin : NM = négociant-manipulant, une maison qui achète raisins ou vins (voir les codes plus bas).' + r('champ', 'civc'),
     '“NM 312-00300”: the Comité Champagne registration number, required by the specification. The two letters tell you who made the wine: NM = négociant-manipulant, a house that buys grapes or wines (see the codes below).' + r('champ', 'civc'), 1),
    (10.5, 95.2, 'B', 'Teneur en alcool', 'Alcohol content',
     'Le titre alcoométrique en « % vol ». Obligatoire, à ±0,5 % vol près.' + r('r2019'),
     'The alcoholic strength, in “% vol”. Compulsory, accurate to within ±0.5 % vol.' + r('r2019'), 1),
    (90.5, 95.2, 'B', 'Contenance', 'Bottle size',
     'Le volume nominal (750 ml = 75 cl, la bouteille standard). Obligatoire.' + r('r1308'),
     'The nominal volume (750 ml = 75 cl, the standard bottle). Compulsory.' + r('r1308'), 1),
    lot_spot(54.2, 95.1, 'B', 'Ici, il est imprimé au bas de l’étiquette ; en Champagne, on le trouve aussi souvent sur la contre-étiquette ou sur le verre, près du col.',
             'Here it is printed at the foot of the label; in Champagne it is also often found on the back label or on the glass, near the neck.'),
]


def label_block(key, img, w, h, spots, alt):
    """One picture: the label in the middle, the call-out boxes around it (side L/R/B), leader lines drawn by JS
    from each box to its tip. Under it, the full explanations. Narrow screens: numbered dots on the tips + the list."""
    tips, boxes, keys = [], [], []
    for i, (x, y, side, sfr, sen, lfr, len_, must) in enumerate(spots, 1):
        col = '#9b2235' if must else '#3a6b8f'   # inline: the cream-theme converter would recolour a stylesheet rule
        tag = (dl('obligatoire', 'compulsory', 'span', 'tag must') if must else dl('facultatif', 'optional', 'span', 'tag opt'))
        tips.append(f'<span class="tip-dot" style="left:{x}%;top:{y}%;background:{col}" data-k="{key}{i}" data-x="{x}" data-y="{y}">'
                    f'<em style="background:{col}">{i}</em></span>')
        sd, _, by = side.partition('@')
        boxes.append(f'<button type="button" class="co" data-k="{key}{i}" data-side="{sd}" data-x="{x}" data-y="{y}"'
                     f'{f" data-by={by!r}" if by else ""} style="--c:{col}">'
                     f'<span class="kn" style="background:{col};color:#fff">{i}</span>{dl(sfr, sen)}</button>')
        keys.append(f'<li data-k="{key}{i}" tabindex="0"><span class="kn" style="background:{col};color:#fff">{i}</span><div>'
                    f'<b>{dl(sfr, sen)}</b> {tag}{LL(lfr, len_)}</div></li>')
    return (f'<figure class="dg" data-ratio="{h / w:.4f}">'
            f'<svg class="dg-lines" aria-hidden="true"></svg>'
            f'<div class="dg-img"><img src="img/{img}" width="{w}" height="{h}" alt="{alt}">{"".join(tips)}</div>'
            + ''.join(boxes)
            + f'</figure><p class="dg-cap">{dl("Survolez ou touchez une étiquette pour lire l’explication ci-dessous.", "Hover over or tap a call-out to read the explanation below.")}</p>'
            + f'<ol class="keys">{"".join(keys)}</ol>')


# ------------------------------------------------------------------ compulsory / optional
MUST = [
    ('La dénomination', 'The designation',
     'Le nom de l’appellation avec « Appellation d’Origine Protégée » ou la mention traditionnelle « Appellation … Contrôlée » ; pour une IGP, « Indication Géographique Protégée » (ou « Vin de Pays ») ; sinon « Vin de France ».' + r('r1308'),
     'The name of the appellation with “Appellation d’Origine Protégée” or the traditional “Appellation … Contrôlée”; for a PGI, “Indication Géographique Protégée” (or “Vin de Pays”); otherwise “Vin de France”.' + r('r1308')),
    ('Le titre alcoométrique', 'The alcoholic strength',
     'En « % vol », à ±0,5 % vol près.' + r('r2019'), 'In “% vol”, accurate to within ±0.5 % vol.' + r('r2019')),
    ('Le volume nominal', 'The nominal volume',
     'En litres, centilitres ou millilitres : 75 cl, 150 cl…' + r('r1308'), 'In litres, centilitres or millilitres: 75 cl, 150 cl…' + r('r1308')),
    ('La provenance', 'The provenance',
     '« Produit de France », ou le pays de production.' + r('r1308'), '“Produit de France” (Product of France), or the country of production.' + r('r1308')),
    ('L’embouteilleur', 'The bottler',
     'Son nom et sa commune (« mis en bouteille par… »). Pour les vins mousseux, le producteur ou le vendeur ; pour un vin importé, l’importateur.' + r('r2019'),
     'Its name and town (“bottled by…”). For sparkling wines, the producer or vendor; for an imported wine, the importer.' + r('r2019')),
    ('Les allergènes', 'Allergens',
     '« Contient des sulfites » dès 10 mg/L — c’est-à-dire presque toujours — et, le cas échéant, les protéines d’œuf ou de lait utilisées pour le collage.' + r('r1169'),
     '“Contains sulphites” from 10 mg/L — that is, almost always — and, where relevant, egg or milk proteins used for fining.' + r('r1169')),
    ('Le numéro de lot', 'The lot number',
     'Souvent une courte référence précédée de « L », parfois gravée sur le verre — comme « L0001-01 » sur les trois étiquettes ci-dessus. Il sert à retrouver les bouteilles d’un même lot en cas de rappel.' + r('d2011'),
     'Often a short code starting with “L”, sometimes etched on the glass — like “L0001-01” on the three labels above. It is used to trace the bottles of one batch in case of a recall.' + r('d2011')),
    ('Le logo « femme enceinte »', 'The pregnancy logo',
     'Obligatoire en France depuis 2007 (ou la phrase équivalente).' + r('csp'), 'Compulsory in France since 2007 (or the equivalent sentence).' + r('csp')),
    ('La valeur énergétique', 'The energy value',
     'Pour les vins produits depuis le 8 décembre 2023 : les calories figurent sur l’étiquette (parfois sous la forme « E = … kcal/100 ml ») ; la liste des ingrédients et la déclaration nutritionnelle complète peuvent être consultées via un QR code.' + r('r2117'),
     'For wines produced since 8 December 2023: the calories are on the label (sometimes as “E = … kcal/100 ml”); the list of ingredients and the full nutrition declaration may be given through a QR code.' + r('r2117')),
    ('La teneur en sucre (mousseux)', 'Sugar content (sparkling)',
     'Pour les vins mousseux uniquement : brut nature, extra brut, brut, extra dry, sec, demi-sec ou doux (voir le tableau plus bas).' + r('r2019'),
     'For sparkling wines only: brut nature, extra brut, brut, extra dry, sec, demi-sec or doux (see the table below).' + r('r2019')),
]
MAY = [
    ('Le millésime', 'The vintage', 'Au moins 85 % des raisins de l’année indiquée.' + r('r2019'), 'At least 85 % of the grapes from the year shown.' + r('r2019')),
    ('Le cépage', 'The grape variety',
     'Un seul cépage nommé : au moins 85 % de ce cépage. Deux cépages ou plus : ils doivent faire 100 % du vin et être cités par ordre d’importance. Beaucoup d’AOC ne le mentionnent pas : c’est le lieu qui compte.' + r('r2019'),
     'One variety named: at least 85 % of that variety. Two or more: they must make up 100 % of the wine and be listed in order of importance. Many AOCs leave it out: the place is what matters.' + r('r2019')),
    ('Le nom de l’exploitation', 'The estate name',
     '« Château », « Clos », « Domaine »… Les termes « château », « clos » et « cru » sont réservés aux vins d’appellation.' + r('decret'),
     '“Château”, “Clos”, “Domaine”… The terms “château”, “clos” and “cru” are reserved for appellation wines.' + r('decret')),
    ('Un classement', 'A classification',
     '« Grand Cru Classé en 1855 », « Premier Grand Cru Classé », « Cru Bourgeois », « Premier Cru », « Grand Cru »… seulement s’il est officiellement reconnu.',
     '“Grand Cru Classé en 1855”, “Premier Grand Cru Classé”, “Cru Bourgeois”, “Premier Cru”, “Grand Cru”… only if officially recognised.'),
    ('Une unité géographique', 'A geographical unit',
     'Plus petite (un climat, un lieu-dit) ou plus grande (« Vin de Bordeaux »), dans les limites fixées par le cahier des charges.',
     'Smaller (a climat, a lieu-dit) or larger (“Vin de Bordeaux”), within the limits set by the specification.'),
    ('La mise à la propriété', 'Estate bottling',
     '« Mis en bouteille au château / au domaine / à la propriété ».' + r('decret'), '“Mis en bouteille au château / au domaine / à la propriété”.' + r('decret')),
    ('Les mentions traditionnelles', 'Traditional terms',
     '« Sur lie » (Muscadet), « Vendanges tardives », « Sélection de grains nobles », « Primeur », « Clairet »… chacune encadrée par les textes. <a href="#mentions-trad">Le détail plus bas&nbsp;→</a>' + r('tt'),
     '“Sur lie” (Muscadet), “Vendanges tardives”, “Sélection de grains nobles”, “Primeur”, “Clairet”… each one regulated. <a href="#mentions-trad">Details below&nbsp;→</a>' + r('tt')),
    ('Le bio', 'Organic',
     'Si le vin est certifié biologique et l’indique, le logo bio européen est obligatoire ; le logo français AB est facultatif. <a href="#bio">Le détail plus bas&nbsp;→</a>' + r('bio'),
     'If the wine is certified organic and says so, the EU organic logo is compulsory; the French AB logo is optional. <a href="#bio">Details below&nbsp;→</a>' + r('bio')),
    ('Les mots sans définition légale', 'Words with no legal definition',
     '« Vieilles vignes », « Grand vin », « Réserve », « Cuvée prestige »… n’engagent que le producteur.',
     '“Vieilles vignes” (old vines), “Grand vin”, “Réserve”, “Cuvée prestige”… commit no one but the producer.'),
]

STILL = [('Sec', 'Dry', '≤ 4 g/L (jusqu’à 9 g/L si l’acidité est élevée)', '≤ 4 g/L (up to 9 g/L if acidity is high)'),
         ('Demi-sec', 'Medium dry', '≤ 12 g/L (jusqu’à 18 g/L si l’acidité est élevée)', '≤ 12 g/L (up to 18 g/L if acidity is high)'),
         ('Moelleux', 'Medium sweet', '≤ 45 g/L', '≤ 45 g/L'),
         ('Doux', 'Sweet', '≥ 45 g/L', '≥ 45 g/L')]
SPARK = [('Brut nature', 'Brut nature', '< 3 g/L, sans sucre ajouté', '< 3 g/L, no added sugar'),
         ('Extra brut', 'Extra brut', '0 à 6 g/L', '0 to 6 g/L'),
         ('Brut', 'Brut', '< 12 g/L', '< 12 g/L'),
         ('Extra dry', 'Extra dry', '12 à 17 g/L', '12 to 17 g/L'),
         ('Sec', 'Sec (dry)', '17 à 32 g/L', '17 to 32 g/L'),
         ('Demi-sec', 'Demi-sec', '32 à 50 g/L', '32 to 50 g/L'),
         ('Doux', 'Doux (sweet)', '> 50 g/L', '> 50 g/L')]
CHAMP = [('NM', 'Négociant-manipulant', 'une maison qui achète raisins ou vins et élabore le champagne sous sa marque', 'a house that buys grapes or wines and makes the champagne under its brand'),
         ('RM', 'Récoltant-manipulant', 'un vigneron qui élabore le champagne de ses propres raisins', 'a grower who makes champagne from his or her own grapes'),
         ('CM', 'Coopérative de manipulation', 'une coopérative qui élabore le champagne de ses adhérents', 'a co-operative making champagne from its members’ grapes'),
         ('RC', 'Récoltant-coopérateur', 'un vigneron qui vend sous son nom un champagne élaboré par sa coopérative', 'a grower selling under his or her own name a champagne made by the co-operative'),
         ('SR', 'Société de récoltants', 'une société de vignerons d’une même famille qui élaborent ensemble', 'a company of related growers making champagne together'),
         ('ND', 'Négociant distributeur', 'un distributeur qui achète des champagnes finis et les vend sous son étiquette', 'a distributor buying finished champagnes and selling them under its label'),
         ('MA', 'Marque auxiliaire / d’acheteur', 'une marque appartenant à l’acheteur (enseigne, restaurant…)', 'a brand owned by the buyer (retailer, restaurant…)')]

# traditional terms: (name FR, name EN, where FR, where EN, [(bullet FR, bullet EN)…], source keys)
TRAD = [
    ('« Sur lie »', '“Sur lie”',
     'Muscadet, Muscadet Sèvre et Maine, Muscadet Côtes de Grandlieu, Gros Plant du Pays nantais — vins blancs.',
     'Muscadet, Muscadet Sèvre et Maine, Muscadet Côtes de Grandlieu, Gros Plant du Pays nantais — white wines.',
     [('Les lies fines sont le dépôt de levures qui tombe au fond de la cuve après la fermentation. Le vin « sur lie » reste au contact de ces lies, sans soutirage, jusqu’à la mise en bouteille.',
       'The fine lees are the deposit of yeasts that settles at the bottom of the vat after fermentation. A “sur lie” wine stays on these lees, without racking, until bottling.'),
      ('Il ne passe qu’un hiver en cuve ou en fût et se trouve encore sur ses lies au moment du conditionnement.',
       'It spends only one winter in vat or cask and is still on its lees when it is bottled.'),
      ('Il est mis en bouteille dans le chai où il a été vinifié, entre le 1er mars et le 30 novembre de l’année qui suit la récolte.',
       'It is bottled in the cellar where it was made, between 1 March and 30 November of the year after the harvest.'),
      ('Les vignes sont moins chargées : 10 000 kg de raisin par hectare au plus, contre 12 000 pour le Muscadet sans mention.',
       'The vines carry less fruit: at most 10,000 kg of grapes per hectare, against 12,000 for Muscadet without the term.'),
      ('Dans le verre : plus de gras et d’arômes, et souvent un léger perlant dû au gaz carbonique naturel du vin.',
       'In the glass: more texture and aroma, and often a slight prickle from the wine’s natural carbon dioxide.')],
     ('cdcmt',)),
    ('« Primeur » ou « Nouveau »', '“Primeur” or “Nouveau”',
     'Beaujolais et Beaujolais-Villages surtout, mais aussi Mâcon, Touraine, Gaillac, Muscadet, Côtes du Rhône et d’autres AOC dont le cahier des charges le prévoit.',
     'Beaujolais and Beaujolais-Villages above all, but also Mâcon, Touraine, Gaillac, Muscadet, Côtes du Rhône and other AOCs whose specification provides for it.',
     [('Les deux mots sont synonymes : un vin de l’année, mis en vente quelques semaines après les vendanges.',
       'The two words mean the same thing: a wine of the year, released a few weeks after the harvest.'),
      ('Il est vendu au consommateur à partir du troisième jeudi de novembre de l’année de la récolte — la date du « Beaujolais nouveau » depuis 1985.',
       'It goes on sale to consumers from the third Thursday of November of the harvest year — the “Beaujolais nouveau” date since 1985.'),
      ('En Beaujolais : vins rouges ou rosés uniquement, raisins de l’année seulement, cuvaison de 10 jours au plus.',
       'In Beaujolais: red or rosé wines only, grapes of that year only, at most 10 days on the skins.'),
      ('Un vin frais et fruité, fait pour être bu dans les mois qui suivent.',
       'A fresh, fruity wine, made to be drunk within the following months.')],
     ('cdcmt',)),
    ('« Vendanges tardives »', '“Vendanges tardives” (late harvest)',
     'Alsace et Alsace grand cru, Jurançon, Gaillac — vins blancs.',
     'Alsace and Alsace grand cru, Jurançon, Gaillac — white wines.',
     [('Les raisins sont cueillis tard, en surmaturité, à la main : ils se sont concentrés sur la souche, par passerillage (ils se dessèchent) ou sous l’effet de la pourriture noble.',
       'The grapes are picked late, overripe, by hand: they have concentrated on the vine, by passerillage (drying out) or through noble rot.'),
      ('En Alsace, seulement quatre cépages, dont le nom doit figurer sur l’étiquette : gewurztraminer et pinot gris (270 g de sucre par litre de moût au minimum), riesling et muscat (244 g/L).',
       'In Alsace, only four varieties, whose name must be on the label: gewurztraminer and pinot gris (at least 270 g of sugar per litre of must), riesling and muscat (244 g/L).'),
      ('Aucun enrichissement : tout le sucre vient du raisin, la chaptalisation est interdite.',
       'No enrichment: all the sugar comes from the grape; chaptalisation is forbidden.'),
      ('Les parcelles sont déclarées avant le 1er mars de l’année de la récolte, et le vin est élevé au moins jusqu’au 1er juin de la deuxième année qui suit (Alsace, Jurançon).',
       'The plots are declared before 1 March of the harvest year, and the wine is aged at least until 1 June of the second year after it (Alsace, Jurançon).'),
      ('À Jurançon : petit et gros manseng seulement, 281 g/L de sucre dans le moût et plus de 55 g/L de sucre restant dans le vin.',
       'In Jurançon: petit and gros manseng only, 281 g/L of sugar in the must and more than 55 g/L of sugar left in the wine.')],
     ('cdcmt',)),
    ('« Sélection de grains nobles »', '“Sélection de grains nobles”',
     'Alsace et Alsace grand cru, Coteaux du Layon, Coteaux de l’Aubance, Monbazillac — vins blancs liquoreux.',
     'Alsace and Alsace grand cru, Coteaux du Layon, Coteaux de l’Aubance, Monbazillac — sweet white wines.',
     [('Le degré au-dessus des vendanges tardives : les raisins sont atteints de pourriture noble (le champignon Botrytis cinerea), qui les dessèche et en concentre le sucre et l’acidité.',
       'One step above vendanges tardives: the grapes are touched by noble rot (the fungus Botrytis cinerea), which dries them and concentrates their sugar and acidity.'),
      ('On les récolte à la main par tries successives : les vendangeurs passent plusieurs fois dans la même vigne pour ne cueillir que les grains « rôtis ».',
       'They are picked by hand in successive passes: the pickers go through the same vineyard several times, taking only the “roasted” berries.'),
      ('En Alsace : 306 g de sucre par litre de moût pour le gewurztraminer et le pinot gris, 276 g/L pour le riesling et le muscat.',
       'In Alsace: 306 g of sugar per litre of must for gewurztraminer and pinot gris, 276 g/L for riesling and muscat.'),
      ('À Monbazillac : 255 g/L dans le moût et au moins 85 g/L de sucre restant dans le vin (45 g/L sans la mention).',
       'In Monbazillac: 255 g/L in the must and at least 85 g/L of sugar left in the wine (45 g/L without the term).'),
      ('Aucun enrichissement. Ces vins ne se font que les années où la pourriture noble s’est bien installée.',
       'No enrichment. These wines are made only in years when noble rot has set in well.')],
     ('cdcmt',)),
    ('« Clairet »', '“Clairet”',
     'Bordeaux, Bourgogne.',
     'Bordeaux, Bourgogne.',
     [('Un rosé foncé, entre le rosé et le rouge : le cahier des charges de Bordeaux réserve la mention aux « vins rosés foncés ».',
       'A dark rosé, between rosé and red: the Bordeaux specification reserves the term for “dark rosé wines”.'),
      ('Il naît de raisins rouges laissés en macération un peu plus longtemps qu’un rosé ordinaire, mais bien moins qu’un rouge.',
       'It comes from red grapes left to macerate a little longer than for an ordinary rosé, but much less than for a red.'),
      ('Robe framboise intense, bouche plus vineuse que les autres rosés ; à boire dans les un à trois ans.',
       'Intense raspberry colour, a winier palate than other rosés; to drink within one to three years.'),
      ('C’est l’ancêtre du mot anglais « claret ». Depuis 2025, le cahier des charges de Bordeaux admet aussi la mention « claret », réservée aux vins rouge clair.',
       'It is the ancestor of the English word “claret”. Since 2025 the Bordeaux specification also allows the term “claret”, reserved for light red wines.')],
     ('cdcmt',)),
]

GLOSS = [
    ('Château', 'Château', 'Une exploitation viticole d’appellation, surtout dans le Bordelais — il n’y a pas toujours de château au sens du bâtiment.', 'An appellation wine estate, mostly in Bordeaux — there is not always a castle-like building.'),
    ('Domaine', 'Domaine', 'L’équivalent bourguignon (et général) : l’ensemble des vignes d’un même producteur.', 'The Burgundian (and general) equivalent: all the vines of a single producer.'),
    ('Clos', 'Clos', 'Une vigne close, à l’origine entourée de murs (Clos de Vougeot, Clos des Mouches…).', 'An enclosed vineyard, originally walled (Clos de Vougeot, Clos des Mouches…).'),
    ('Climat', 'Climat', 'En Bourgogne, une parcelle nommée et délimitée depuis des siècles, avec son sol et son exposition propres.', 'In Burgundy, a named plot mapped for centuries, with its own soil and exposure.'),
    ('Lieu-dit', 'Lieu-dit', 'Un nom de lieu cadastral, qui peut figurer sur l’étiquette si le cahier des charges le permet.', 'A cadastral place name, which may appear on the label when the specification allows it.'),
    ('Cru', 'Cru', 'Littéralement « ce qui a poussé » : un terroir réputé. Le sens exact change d’une région à l’autre.', 'Literally “what has grown”: a renowned terroir. Its exact meaning changes from one region to another.'),
    ('Grand cru / Premier cru', 'Grand cru / Premier cru', 'En Bourgogne, des climats classés (le grand cru est au sommet) ; en Alsace et en Champagne, d’autres systèmes ; dans le Bordelais, des châteaux classés.', 'In Burgundy, classified climats (grand cru at the top); in Alsace and Champagne, other systems; in Bordeaux, classified châteaux.'),
    ('Négociant-éleveur', 'Négociant-éleveur', 'Achète raisins, moûts ou vins, les élève et les met en bouteille sous son nom.', 'Buys grapes, musts or wines, ages them and bottles them under its own name.'),
    ('Cave coopérative', 'Co-operative cellar', 'Les vignerons adhérents apportent leurs raisins ; le vin est fait et vendu en commun (« Les Vignerons de… »).', 'Member growers bring in their grapes; the wine is made and sold jointly (“Les Vignerons de…”).'),
    ('Élevé en fût de chêne', 'Aged in oak barrels', 'Le vin a séjourné en barriques ou en foudres avant la mise en bouteille.', 'The wine spent time in barrels or large casks before bottling.'),
]


def trad_cards():
    out = []
    for nfr, nen, wfr, wen, bullets, refs in TRAD:
        lis_fr = ''.join(f'<li>{a}</li>' for a, _ in bullets)
        lis_en = ''.join(f'<li>{b}</li>' for _, b in bullets)
        out.append(f'<div class="mt"><h4>{dl(nfr, nen)}{r(*refs)}</h4>'
                   f'<p class="where"><b>{dl("Où ?", "Where?")}</b> {dl(wfr, wen)}</p>'
                   f'{LL(lis_fr, lis_en, "ul")}</div>')
    return ''.join(out)


BIO = [
    ('Le logo européen', 'The EU logo', 'obligatoire', 'compulsory', 'must',
     'Une feuille dessinée par des étoiles blanches sur fond vert. Dès qu’un vin se dit « bio » ou « biologique », il doit le porter. À côté figurent le numéro de l’organisme certificateur (par exemple « FR-BIO-01 ») et l’origine des raisins : « Agriculture UE », « Agriculture non UE », ou le nom du pays, comme « Agriculture France ».' + r('bio'),
     'A leaf drawn with white stars on a green background. As soon as a wine calls itself “bio” or “biologique” (organic), it must carry it. Next to it come the code number of the control body (for example “FR-BIO-01”) and the origin of the grapes: “Agriculture UE”, “Agriculture non UE”, or the country name, such as “Agriculture France”.' + r('bio')),
    ('Le logo AB', 'The AB logo', 'facultatif', 'optional', 'opt',
     'Les lettres « AB » (Agriculture biologique) en blanc sur fond vert : une marque française, propriété de l’État. Elle s’ajoute au logo européen, ne le remplace jamais, et suit les mêmes règles.' + r('ab'),
     'The letters “AB” (Agriculture biologique) in white on a green background: a French mark owned by the State. It is added to the EU logo, never replaces it, and follows the same rules.' + r('ab')),
    ('Dans la vigne', 'In the vineyard', '', '', '',
     'Les raisins viennent de vignes certifiées : pas d’herbicides ni d’engrais ou de pesticides de synthèse (le cuivre et le soufre restent permis). Il faut trois ans de conversion avant de pouvoir écrire « bio » ; un organisme agréé contrôle l’exploitation chaque année.' + r('bio2'),
     'The grapes come from certified vineyards: no herbicides and no synthetic fertilisers or pesticides (copper and sulphur remain allowed). Three years of conversion are needed before “organic” may be written; an approved body inspects the estate every year.' + r('bio2')),
    ('Dans le chai', 'In the cellar', '', '', '',
     'Depuis le millésime 2012, la vinification est encadrée elle aussi. Certaines pratiques sont interdites (désalcoolisation partielle, électrodialyse, concentration par le froid, désulfitation), d’autres limitées (chauffage à 70 °C au plus, filtration à 0,2 µm au minimum), et les sulfites sont plafonnés plus bas, comme le montre le tableau ci-dessous.' + r('bio2'),
     'Since the 2012 vintage, winemaking is regulated too. Some practices are forbidden (partial dealcoholisation, electrodialysis, concentration by cooling, desulphiting), others restricted (heating to 70 °C at most, filtration at 0.2 µm minimum), and sulphites are capped lower, as shown in the table below.' + r('bio2')),
]
# (wine FR, EN, conventional, organic) — a cell is (FR, EN); the % in brackets = share of the wine (mg/L ÷ 10 000)
SO2 = [('Vin rouge sec', 'Dry red wine', ('150 mg/L (0,015 %)', '150 mg/L (0.015 %)'), ('100 mg/L (0,01 %)', '100 mg/L (0.01 %)')),
       ('Vin blanc ou rosé sec', 'Dry white or rosé wine', ('200 mg/L (0,02 %)', '200 mg/L (0.02 %)'), ('150 mg/L (0,015 %)', '150 mg/L (0.015 %)')),
       ('Vins plus sucrés', 'Sweeter wines', ('200 à 400 mg/L (0,02 à 0,04 %) selon le type de vin', '200 to 400 mg/L (0.02 to 0.04 %) depending on the type of wine'),
        ('30 mg/L (0,003 %) de moins', '30 mg/L (0.003 %) less'))]
NOTBIO = [
    ('Biodynamie', 'Biodynamics',
     'Une agriculture bio qui ajoute des préparations à base de plantes et de minéraux et suit un calendrier lunaire. Pas de définition légale : on la reconnaît aux logos privés Demeter ou Biodyvin, qui supposent d’abord la certification bio.',
     'Organic farming with added plant- and mineral-based preparations and a lunar calendar. No legal definition: it is recognised by the private Demeter or Biodyvin logos, which require organic certification first.'),
    ('Vin nature', 'Natural wine',
     '« Vin naturel » n’a pas de définition légale. Depuis 2020, la charte privée « Vin méthode nature » impose des raisins bio vendangés à la main, des levures indigènes, aucun intrant, et pas de sulfites ajoutés (ou 30 mg/L au plus, avec un logo distinct).',
     '“Natural wine” has no legal definition. Since 2020 the private “Vin méthode nature” charter requires organic hand-picked grapes, indigenous yeasts, no additives, and no added sulphites (or 30 mg/L at most, with a separate logo).'),
    ('HVE', 'HVE',
     '« Haute Valeur Environnementale » : une certification de l’exploitation par l’État (biodiversité, produits phytosanitaires, fertilisation, eau). Ce n’est pas du bio : les produits de synthèse ne sont pas interdits.',
     '“Haute Valeur Environnementale” (High Environmental Value): a State certification of the farm (biodiversity, plant-protection products, fertilisation, water). It is not organic: synthetic products are not banned.'),
]


def bio_block():
    cards = []
    for hfr, hen, tfr, ten, cls, pfr, pen in BIO:
        tag = dl(tfr, ten, 'span', f'tag {cls}') if tfr else ''
        cards.append(f'<div class="mt"><h4>{dl(hfr, hen)} {tag}</h4>{LL(pfr, pen)}</div>')
    heads = (('Vin', 'Wine'), ('Conventionnel', 'Conventional'), ('Bio', 'Organic'))
    th = ''.join(f'<th>{dl(a, b)}</th>' for a, b in heads)
    lbl = [dl(a, b, 'span', 'lbl') for a, b in heads[1:]]   # column name repeated in the cell, shown only when rows stack
    rows = [f'<tr><td><b>{dl(a, b)}</b></td><td>{lbl[0]}{dl(*c)}</td><td>{lbl[1]}{dl(*d)}</td></tr>'
            for a, b, c, d in SO2]
    so2 = (f'<div class="so2wrap"><table class="tbl so2"><thead><tr>{th}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>'
           f'<p class="credit" style="margin-top:6px">{dl("Teneur maximale en sulfites (anhydride sulfureux total). « Sec » : moins de 2 g/L de sucre pour le bio. Entre parenthèses, la part dans le vin : 150 mg/L = 0,15 g par litre, soit 0,015 %.", "Maximum sulphite content (total sulphur dioxide). “Dry”: less than 2 g/L of sugar for organic wine. In brackets, the share of the wine: 150 mg/L = 0.15 g per litre, i.e. 0.015 %.")}{r("bio2")}</p>')
    nb = ''.join(f'<div class="gcard"><h4>{dl(a, b)}</h4>{LL(c, d)}</div>' for a, b, c, d in NOTBIO)
    return (f'<div class="mtgrid">{"".join(cards)}</div>{so2}'
            f'<h4 class="sub">{dl("À ne pas confondre avec le bio", "Not to be confused with organic")}{r("nature")}</h4>'
            f'<div class="ggrid">{nb}</div>')


def card_grid(items, cls):
    return ''.join(f'<div class="{cls}"><h4>{dl(a, b)}</h4>{LL(c, d)}</div>' for a, b, c, d in items)


def table(rows, head):
    th = ''.join(f'<th>{dl(a, b)}</th>' for a, b in head)
    tr = ''.join(f'<tr><td><b>{dl(a, b)}</b></td><td>{dl(c, d)}</td></tr>' for a, b, c, d in rows)
    return f'<table class="tbl"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table>'


def champ_table():
    tr = ''.join(f'<tr><td class="code">{c}</td><td><b>{n}</b><br>{dl(a, b, "span", "dim")}</td></tr>' for c, n, a, b in CHAMP)
    return f'<table class="tbl"><tbody>{tr}</tbody></table>'


def sources_html():
    return ''.join(f'<li id="src-{k}">{dl(fr, en)}</li>' for k, fr, en in SOURCES)


CSS = r'''
  sup.ref{font-size:.68em;line-height:0;margin-left:1px;}
  sup.ref a{color:var(--gold);text-decoration:none;font-weight:700;}
  .lede{padding:clamp(20px,3vw,32px);}
  .lede p{margin:0 0 12px;font-size:15.5px;line-height:1.72;}
  .steps{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin-top:22px;}
  .step{display:flex;flex-direction:column;gap:3px;padding:14px 16px;border-radius:16px;border:1px solid var(--hair);background:var(--glass);text-decoration:none;transition:border-color .2s,transform .2s;}
  .step:hover{border-color:var(--hair-hi);transform:translateY(-2px);}
  .step .sn{font-family:var(--serif);font-size:26px;color:var(--gold);line-height:1;}
  .step b{font-family:var(--serif);font-weight:500;font-size:19px;color:var(--title);}
  .step small{font-size:12.5px;color:var(--muted);line-height:1.45;}

  /* annotated labels: one picture, call-outs around, leader lines */
  .dg{position:relative;margin:0 auto;max-width:1180px;}
  .dg-img{position:absolute;}
  .dg-img img{display:block;width:100%;height:auto;border-radius:6px;box-shadow:0 18px 44px rgba(20,4,8,.4);}
  .dg-lines{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;overflow:visible;z-index:2;}
  .dg-lines line{stroke:var(--gold);stroke-width:1.3;opacity:.85;}
  .dg-lines circle{fill:var(--gold);}
  .dg-lines .on{stroke-width:2.4;opacity:1;}
  .tip-dot{position:absolute;width:9px;height:9px;margin:-4.5px 0 0 -4.5px;border-radius:50%;border:1.5px solid #fff;
           box-shadow:0 1px 4px rgba(0,0,0,.45);z-index:3;pointer-events:none;}
  .tip-dot em{display:none;}
  .tip-dot.on{transform:scale(1.6);}
  .co{all:unset;box-sizing:border-box;position:absolute;z-index:4;cursor:pointer;display:flex;align-items:center;gap:8px;
      width:var(--cw,176px);padding:6px 9px;border-radius:10px;background:var(--solid,#2a0a12);border:1px solid var(--hair-hi);
      border-left:4px solid var(--c);font-size:12px;line-height:1.25;color:var(--title);box-shadow:0 6px 18px rgba(0,0,0,.18);
      transition:transform .15s,border-color .15s;}
  .co .kn{width:20px;height:20px;font-size:11px;margin:0;}
  .co:hover,.co:focus-visible,.co.on{transform:scale(1.04);border-color:var(--gold);outline:none;}
  .dg-cap{font-size:12px;color:var(--faint);margin:10px 0 18px;text-align:center;}
  .keys{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;}
  .keys li{display:flex;gap:12px;padding:11px 14px;border-radius:14px;background:var(--glass);border:1px solid var(--hair);transition:border-color .18s,background .18s;outline:none;}
  .keys li.on,.keys li:focus-visible{border-color:var(--hair-hi);background:var(--glass-hi);}
  .keys li > div{min-width:0;}
  .keys b{font-family:var(--serif);font-weight:500;font-size:17px;color:var(--title);}
  .keys p{margin:3px 0 0;font-size:13.6px;line-height:1.55;}
  .kn{flex:none;width:24px;height:24px;border-radius:50%;display:grid;place-items:center;font:700 12px/1 var(--sans);color:#fff;background:#3a6b8f;margin-top:2px;}
  .kn.must{background:#9b2235;}
  .tag{display:inline-block;margin-left:6px;font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;font-weight:700;padding:2px 7px;border-radius:999px;vertical-align:2px;}
  .tag.must{color:#e48a9a;border:1px solid rgba(228,138,154,.5);}
  .tag.opt{color:#8fb6d3;border:1px solid rgba(143,182,211,.5);}
  html[data-theme="cream"] .tag.must{color:#9b2235;border-color:rgba(155,34,53,.45);}
  html[data-theme="cream"] .tag.opt{color:#2f5f82;border-color:rgba(47,95,130,.45);}
  .legend{display:flex;gap:16px;flex-wrap:wrap;font-size:12.5px;color:var(--muted);margin:0 0 14px;}
  .legend span{display:inline-flex;align-items:center;gap:6px;}
  .legend i{width:12px;height:12px;border-radius:50%;display:inline-block;}

  .note{margin-top:14px;padding:13px 16px;border-radius:14px;border:1px solid color-mix(in srgb,#c08a1a 50%,transparent);background:color-mix(in srgb,#c08a1a 10%,transparent);font-size:14px;line-height:1.6;}
  .note p{margin:0;}
  .cols{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:clamp(16px,2.6vw,28px);}
  .cols h3{font-family:var(--serif);font-weight:500;font-size:22px;color:var(--title);margin:0 0 10px;display:flex;align-items:center;gap:10px;}
  .cols h3 i{width:12px;height:12px;border-radius:50%;}
  .fgrid{display:grid;gap:10px;}
  .fcard{padding:13px 16px;border-radius:14px;background:var(--glass);border:1px solid var(--hair);border-left:4px solid var(--c);}
  .fcard h4{margin:0 0 4px;font-family:var(--serif);font-weight:500;font-size:18px;color:var(--title);}
  .fcard p{margin:0;font-size:13.8px;line-height:1.58;}
  .ggrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:10px;}
  .gcard{padding:13px 16px;border-radius:14px;background:var(--glass);border:1px solid var(--hair);}
  .gcard h4{margin:0 0 4px;font-family:var(--serif);font-weight:500;font-size:18px;color:var(--gold-soft);}
  html[data-theme="cream"] .gcard h4{color:#8a5d17;}
  .gcard p{margin:0;font-size:13.6px;line-height:1.55;}
  .mtgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px;margin-top:12px;}
  .mt{padding:14px 16px;border-radius:14px;background:var(--glass);border:1px solid var(--hair);}
  .mt h4{margin:0 0 6px;font-family:var(--serif);font-weight:500;font-size:19px;color:var(--gold-soft);}
  html[data-theme="cream"] .mt h4{color:#8a5d17;}
  .mt .where{margin:0 0 8px;font-size:13px;line-height:1.5;color:var(--muted);}
  .mt .where b{color:var(--title);font-weight:600;}
  .mt ul{margin:0;padding-left:18px;font-size:13.6px;line-height:1.55;}
  .mt li{margin-bottom:5px;}
  .mt p{margin:0;font-size:13.6px;line-height:1.58;}
  .tpanel > p.L{margin:0 0 4px;font-size:14.5px;line-height:1.65;}
  .tpanel .sub{font-family:var(--serif);font-weight:500;font-size:19px;color:var(--title);margin:20px 0 10px;}
  .so2wrap{margin-top:14px;max-width:780px;overflow-x:auto;}
  .so2 .lbl{display:none;}
  @media (max-width:560px){
    .tbl.so2,.tbl.so2 tbody{display:block;}
    .tbl.so2 thead{display:none;}
    .tbl.so2 tr{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:12px;padding:10px 0;border-bottom:1px solid var(--hair);}
    .tbl.so2 td,html[data-theme="cream"] .tbl.so2 td{border:0;padding:2px 0;min-width:0;}
    .tbl.so2 td:first-child{grid-column:1 / -1;margin-bottom:4px;}
    .tbl.so2 .lbl{display:block;font-size:9px;letter-spacing:.04em;text-transform:uppercase;color:var(--muted);font-weight:700;}
  }
  .tbl{width:100%;border-collapse:collapse;font-size:14px;}
  .tbl th{text-align:left;font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);padding:8px 10px;border-bottom:1px solid var(--hair-hi);}
  .tbl td{padding:8px 10px;border-bottom:1px solid var(--hair);vertical-align:top;line-height:1.5;}
  .tbl td b{color:var(--title);font-weight:600;}
  .tbl .code{font-family:var(--serif);font-size:22px;color:var(--gold-soft);width:60px;}
  html[data-theme="cream"] .tbl .code{color:#8a5d17;}
  .tbl .dim{color:var(--muted);font-size:13px;}
  .tpanel{padding:clamp(16px,2.4vw,24px);}
  .tpanel h3{font-family:var(--serif);font-weight:500;font-size:21px;color:var(--title);margin:0 0 10px;}
  .sources-list{margin:0;padding-left:26px;font-size:13px;line-height:1.6;color:var(--muted);columns:2;column-gap:34px;}
  .sources-list li{break-inside:avoid;margin-bottom:6px;}
  .sources-list li:target{color:var(--title);background:color-mix(in srgb,var(--gold) 14%,transparent);border-radius:6px;}
  .sources-list a{color:var(--gold);}
  .credit{font-size:12px;color:var(--faint);margin-top:16px;line-height:1.6;}
  @media (max-width:900px){
    .cols,.keys{grid-template-columns:minmax(0,1fr);}
    .steps{grid-template-columns:repeat(2,minmax(0,1fr));}
    .sources-list{columns:1;}
  }
  /* narrow: no call-out boxes, numbered dots on the tips instead */
  .dg.narrow .co{width:22px;padding:0;border:0;background:none;box-shadow:none;justify-content:center;}
  .dg.narrow .co > span:not(.kn){display:none;}
  .dg.narrow .co .kn{width:20px;height:20px;font-size:10px;}
  .dg.narrow .tip-dot{width:6px;height:6px;margin:-3px 0 0 -3px;border-width:1px;}
  .dg.narrow .dg-lines line{stroke-width:1;}
'''

PAGE = r'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title data-fr="Apprendre à lire… une étiquette" data-en="Learning to read… a wine label">Apprendre à lire… une étiquette</title>
<meta name="description" content="Comment lire une étiquette de vin français : deux étiquettes commentées (Bordeaux et Bourgogne), mentions obligatoires et facultatives, sucre, codes de Champagne et vocabulaire.">
<style>
@@BASE_CSS@@
@@CSS@@
</style>
</head>
<body>
<div class="wrap">

  <div class="topbar">
    <a class="back" href="../../index.html" data-fr="← Retour" data-en="← Back">← Retour</a>
  </div>

  <header>
    <p class="eyebrow" data-fr="Le vin en bouteille" data-en="Wine in the bottle">Le vin en bouteille</p>
    <h1 data-fr="Apprendre à lire… <em>une étiquette</em>" data-en="Learning to read… <em>a wine label</em>">Apprendre à lire… <em>une étiquette</em></h1>
    <div class="rule"></div>
    <p class="tagline" data-fr="Une étiquette française dit d’abord d’où vient le vin, avant de dire ce qu’il contient. Trois étiquettes commentées — Bordeaux, Bourgogne, Champagne — pour apprendre à la déchiffrer, puis ce que la loi impose aujourd’hui, ce qu’elle permet, et le vocabulaire à connaître."
       data-en="A French label first tells you where the wine comes from, before what is inside the bottle. Three annotated labels — Bordeaux, Burgundy, Champagne — to learn how to decipher one, then what the law requires today, what it allows, and the words worth knowing.">Une étiquette française dit d’abord d’où vient le vin, avant de dire ce qu’il contient. Trois étiquettes commentées — Bordeaux, Bourgogne, Champagne — pour apprendre à la déchiffrer, puis ce que la loi impose aujourd’hui, ce qu’elle permet, et le vocabulaire à connaître.</p>
    <nav class="steps">
      <a class="step" href="#bordeaux"><span class="sn">01</span><b data-fr="Bordeaux" data-en="Bordeaux">Bordeaux</b><small data-fr="et la plupart des étiquettes françaises" data-en="and most French labels">et la plupart des étiquettes françaises</small></a>
      <a class="step" href="#bourgogne"><span class="sn">02</span><b data-fr="Bourgogne" data-en="Burgundy">Bourgogne</b><small data-fr="et les autres" data-en="and the rest">et les autres</small></a>
      <a class="step" href="#champagne"><span class="sn">03</span><b data-fr="Champagne" data-en="Champagne">Champagne</b><small data-fr="une étiquette à part" data-en="a label of its own">une étiquette à part</small></a>
      <a class="step" href="#mentions"><span class="sn">04</span><b data-fr="Obligatoire ou facultatif" data-en="Compulsory or optional">Obligatoire ou facultatif</b><small data-fr="ce que dit la loi en 2026" data-en="what the law says in 2026">ce que dit la loi en 2026</small></a>
      <a class="step" href="#vocabulaire"><span class="sn">05</span><b data-fr="Le vocabulaire" data-en="The vocabulary">Le vocabulaire</b><small data-fr="sucre, Champagne, mentions, bio" data-en="sugar, Champagne, terms, organic">sucre, Champagne, mentions, bio</small></a>
    </nav>
  </header>

  <section class="sec" id="bordeaux">
    <div class="sec-head">
      <p class="kick" data-fr="01 · Bordeaux" data-en="01 · Bordeaux">01 · Bordeaux</p>
      <h2 data-fr="Bordeaux <em>et la plupart des étiquettes françaises</em>" data-en="Bordeaux <em>and most French labels</em>">Bordeaux <em>et la plupart des étiquettes françaises</em></h2>
      <p data-fr="Ici, la vedette est le château : son nom domine, l’appellation vient ensuite. Château Blabla, Saint-Émilion, millésime 1989 — une étiquette imaginaire, créée pour ce site."
         data-en="Here the star is the château: its name dominates, the appellation comes next. Château Blabla, Saint-Émilion, 1989 vintage — an imaginary label, created for this site.">Ici, la vedette est le château : son nom domine, l’appellation vient ensuite. Château Blabla, Saint-Émilion, millésime 1989 — une étiquette imaginaire, créée pour ce site.</p>
    </div>
    <div class="legend"><span><i style="background:#9b2235"></i>@@MUST@@</span><span><i style="background:#3a6b8f"></i>@@OPT@@</span></div>
    @@FIGEAC@@
    <div class="note">@@NOTE88@@</div>
  </section>

  <section class="sec" id="bourgogne">
    <div class="sec-head">
      <p class="kick" data-fr="02 · Bourgogne" data-en="02 · Burgundy">02 · Bourgogne</p>
      <h2 data-fr="La Bourgogne <em>et les autres</em>" data-en="Burgundy <em>and the rest</em>">La Bourgogne <em>et les autres</em></h2>
      <p data-fr="Ici, l’étiquette met en avant le lieu : le village, son classement, puis le climat — le nom du domaine est souvent bien en vue lui aussi. Domaine Coullenot, Beaune Premier Cru « Les Grèves », millésime 2019 — une étiquette imaginaire, créée pour ce site."
         data-en="Here the label puts the place first: the village, its classification, then the climat — the domaine name is often prominent too. Domaine Coullenot, Beaune Premier Cru “Les Grèves”, 2019 vintage — an imaginary label, created for this site.">Ici, l’étiquette met en avant le lieu : le village, son classement, puis le climat — le nom du domaine est souvent bien en vue lui aussi. Domaine Coullenot, Beaune Premier Cru « Les Grèves », millésime 2019 — une étiquette imaginaire, créée pour ce site.</p>
    </div>
    <div class="legend"><span><i style="background:#9b2235"></i>@@MUST@@</span><span><i style="background:#3a6b8f"></i>@@OPT@@</span></div>
    @@ALOXE@@
    <div class="note">@@NOTENECK@@</div>
  </section>

  <section class="sec" id="champagne">
    <div class="sec-head">
      <p class="kick" data-fr="03 · Champagne" data-en="03 · Champagne">03 · Champagne</p>
      <h2 data-fr="Le champagne <em>, une étiquette à part</em>" data-en="Champagne <em>, a label of its own</em>">Le champagne <em>, une étiquette à part</em></h2>
      <p data-fr="Ici, la vedette est la marque : on achète une maison plus qu’un lieu. Et un vin mousseux doit dire sa teneur en sucre. Champagne Bubulle, Brut Blanc de Blancs 2002 — une étiquette imaginaire, créée pour ce site."
         data-en="Here the star is the brand: you buy a house more than a place. And a sparkling wine must state its sugar content. Champagne Bubulle, Brut Blanc de Blancs 2002 — an imaginary label, created for this site.">Ici, la vedette est la marque : on achète une maison plus qu’un lieu. Et un vin mousseux doit dire sa teneur en sucre. Champagne Bubulle, Brut Blanc de Blancs 2002 — une étiquette imaginaire, créée pour ce site.</p>
    </div>
    <div class="legend"><span><i style="background:#9b2235"></i>@@MUST@@</span><span><i style="background:#3a6b8f"></i>@@OPT@@</span></div>
    @@CHAMPLABEL@@
    <div class="note">@@NOTECH@@</div>
  </section>

  <section class="sec" id="mentions">
    <div class="sec-head">
      <p class="kick" data-fr="04 · La règle" data-en="04 · The rules">04 · La règle</p>
      <h2 data-fr="Obligatoire <em>ou facultatif&nbsp;?</em>" data-en="Compulsory <em>or optional?</em>">Obligatoire <em>ou facultatif&nbsp;?</em></h2>
      <p data-fr="Ce qu’une bouteille vendue en France doit porter en 2026, et ce qu’elle peut ajouter. La plupart des mentions obligatoires doivent se lire dans le même champ visuel, sans tourner la bouteille — sauf notamment le numéro de lot, les allergènes et l’importateur."
         data-en="What a bottle sold in France must carry in 2026, and what it may add. Most compulsory statements must be readable in the same field of vision, without turning the bottle — except, notably, the lot number, allergens and importer.">Ce qu’une bouteille vendue en France doit porter en 2026, et ce qu’elle peut ajouter. La plupart des mentions obligatoires doivent se lire dans le même champ visuel, sans tourner la bouteille — sauf notamment le numéro de lot, les allergènes et l’importateur.</p>
    </div>
    <div class="cols">
      <div><h3><i style="background:#9b2235"></i>@@MUST_H@@</h3><div class="fgrid">@@MUSTCARDS@@</div></div>
      <div><h3><i style="background:#3a6b8f"></i>@@MAY_H@@</h3><div class="fgrid">@@MAYCARDS@@</div></div>
    </div>
  </section>

  <section class="sec" id="vocabulaire">
    <div class="sec-head">
      <p class="kick" data-fr="05 · Le vocabulaire" data-en="05 · The vocabulary">05 · Le vocabulaire</p>
      <h2 data-fr="Les mots <em>de l’étiquette</em>" data-en="The words <em>on the label</em>">Les mots <em>de l’étiquette</em></h2>
    </div>
    <div class="cols">
      <div class="panel tpanel"><h3 data-fr="Le sucre : vins tranquilles" data-en="Sugar: still wines">Le sucre : vins tranquilles</h3>@@STILL@@</div>
      <div class="panel tpanel"><h3 data-fr="Le sucre : vins mousseux" data-en="Sugar: sparkling wines">Le sucre : vins mousseux</h3>@@SPARK@@</div>
    </div>
    <p class="credit">@@SUGARREF@@</p>
    <div class="panel tpanel" style="margin-top:16px">
      <h3 data-fr="Champagne : le code du producteur" data-en="Champagne: the producer code">Champagne : le code du producteur</h3>
      @@CHAMPNOTE@@
      @@CHAMP@@
    </div>
    <div class="panel tpanel" id="mentions-trad" style="margin-top:16px">
      <h3 data-fr="Les mentions traditionnelles" data-en="Traditional terms">Les mentions traditionnelles</h3>
      @@TRADINTRO@@
      <div class="mtgrid">@@TRAD@@</div>
    </div>
    <div class="panel tpanel" id="bio" style="margin-top:16px">
      <h3 data-fr="Le bio" data-en="Organic wine">Le bio</h3>
      @@BIOINTRO@@
      @@BIO@@
    </div>
    <div class="ggrid" style="margin-top:16px">@@GLOSS@@</div>
  </section>

  <section class="sec" id="sources">
    <div class="sec-head"><h2 data-fr="Sources" data-en="Sources">Sources</h2></div>
    <ol class="sources-list">@@SOURCES@@</ol>
    <p class="credit">@@CREDIT@@</p>
  </section>

</div>
<script>
(function(){
  /* ---------- labels: call-out boxes around the picture, leader lines to the tips ---------- */
  var NS = 'http://www.w3.org/2000/svg';
  function layout(dg){
    var W = dg.clientWidth, ratio = +dg.getAttribute('data-ratio');
    var img = dg.querySelector('.dg-img'), svg = dg.querySelector('.dg-lines');
    var boxes = [].slice.call(dg.querySelectorAll('.co'));
    var narrow = W < 760;
    dg.classList.toggle('narrow', narrow);
    while(svg.firstChild) svg.removeChild(svg.firstChild);
    /* narrow screens: same picture, the call-outs shrink to numbered markers in the margins */
    var cw = narrow ? 22 : Math.max(150, Math.min(200, W*0.175)), g = narrow ? 8 : 34, sp = narrow ? 3 : 8;
    dg.style.setProperty('--cw', cw+'px');
    var side = function(sd){ return boxes.filter(function(b){ return b.getAttribute('data-side')===sd; }); };
    var L = side('L'), R = side('R'), B = side('B');
    var iL = cw+g, iW = W - 2*(cw+g), iH = iW*ratio;
    img.style.cssText = 'left:'+iL+'px;top:0;width:'+iW+'px';
    var tip = function(b){ return [iL + b.getAttribute('data-x')/100*iW, b.getAttribute('data-y')/100*iH]; };
    var bottom = iH;
    [[L, 0], [R, W-cw]].forEach(function(col){
      var list = col[0].slice().sort(function(a,b){ return tip(a)[1]-tip(b)[1]; });
      var want = function(b){ var by = b.getAttribute('data-by'); return by ? by/100*iH : tip(b)[1]; };
      list.sort(function(a,b){ return want(a)-want(b); });
      var pos = list.map(function(b){ return {b:b, h:b.offsetHeight, y:want(b)-b.offsetHeight/2}; });
      for(var i=0;i<pos.length;i++){ if(i) pos[i].y = Math.max(pos[i].y, pos[i-1].y+pos[i-1].h+sp); pos[i].y = Math.max(pos[i].y, 0); }
      for(i=pos.length-1;i>=0;i--){ var lim = i===pos.length-1 ? iH+20-pos[i].h : pos[i+1].y-sp-pos[i].h; if(pos[i].y>lim) pos[i].y = Math.max(0, lim); }
      pos.forEach(function(p){ p.b.style.left = col[1]+'px'; p.b.style.top = p.y+'px'; bottom = Math.max(bottom, p.y+p.h); });
    });
    var by = iH + (narrow ? 16 : 40);
    var bl = B.slice().sort(function(a,b){ return tip(a)[0]-tip(b)[0]; });
    var bp = bl.map(function(b){ return {b:b, x:tip(b)[0]-cw/2}; });
    for(var j=0;j<bp.length;j++){ if(j) bp[j].x = Math.max(bp[j].x, bp[j-1].x+cw+sp+4); bp[j].x = Math.max(bp[j].x, 0); }
    for(j=bp.length-1;j>=0;j--){ var lim2 = j===bp.length-1 ? W-cw : bp[j+1].x-sp-4-cw; if(bp[j].x>lim2) bp[j].x = lim2; }
    bp.forEach(function(p){ p.b.style.left = p.x+'px'; p.b.style.top = by+'px'; bottom = Math.max(bottom, by+p.b.offsetHeight); });
    dg.style.height = (bottom+6)+'px';
    boxes.forEach(function(b){
      var t = tip(b), sd = b.getAttribute('data-side');
      var x = parseFloat(b.style.left), y = parseFloat(b.style.top), h = b.offsetHeight;
      var a = sd==='L' ? [x+cw, y+h/2] : sd==='R' ? [x, y+h/2] : [x+cw/2, y];
      var ln = document.createElementNS(NS, 'line');
      ln.setAttribute('x1', a[0]); ln.setAttribute('y1', a[1]); ln.setAttribute('x2', t[0]); ln.setAttribute('y2', t[1]);
      ln.setAttribute('data-k', b.getAttribute('data-k')); svg.appendChild(ln);
    });
  }
  var dgs = document.querySelectorAll('.dg');
  function layoutAll(){ for(var i=0;i<dgs.length;i++) layout(dgs[i]); }
  layoutAll();
  window.addEventListener('resize', layoutAll);
  if(document.fonts && document.fonts.ready) document.fonts.ready.then(layoutAll);

  /* hover / focus / tap: box, dot, line and explanation light up together */
  function set(k, on){
    var els = document.querySelectorAll('[data-k="'+k+'"]');
    for(var i=0;i<els.length;i++){ if(on) els[i].classList.add('on'); else els[i].classList.remove('on'); }
  }
  function clear(){ var on = document.querySelectorAll('[data-k].on'); for(var j=0;j<on.length;j++) on[j].classList.remove('on'); }
  var all = document.querySelectorAll('.co,.tip-dot,.keys li');
  for(var i=0;i<all.length;i++){
    (function(el){
      var k = el.getAttribute('data-k');
      el.addEventListener('pointerenter', function(){ set(k, true); });
      el.addEventListener('pointerleave', function(){ if(!el.classList.contains('pin')) set(k, false); });
      el.addEventListener('focus', function(){ set(k, true); });
      el.addEventListener('blur', function(){ set(k, false); });
      if(!el.matches('li')) el.addEventListener('click', function(){
        clear(); set(k, true);
        var li = document.querySelector('li[data-k="'+k+'"]');
        if(li){ var r = li.getBoundingClientRect(); if(r.top<0 || r.bottom>innerHeight) li.scrollIntoView({block:'center', behavior:'smooth'}); }
      });
    })(all[i]);
  }
  /* language: the site menu sets <html lang>; data-fr/data-en nodes follow, .L blocks switch by CSS */
  function apply(){
    var l = document.documentElement.lang === 'en' ? 'en' : 'fr';
    var n = document.querySelectorAll('[data-fr][data-en]');
    for(var i=0;i<n.length;i++) n[i].innerHTML = n[i].getAttribute('data-'+l);
    var t = document.querySelector('title[data-en]'); if(t) document.title = t.getAttribute('data-'+l);
    layoutAll();   /* call-out heights change with the language */
  }
  new MutationObserver(apply).observe(document.documentElement, {attributes:true, attributeFilter:['lang']});
})();
</script>
</body>
</html>
'''


def main():
    rep = {
        '@@BASE_CSS@@': base_css(), '@@CSS@@': CSS,
        '@@MUST@@': dl('mention obligatoire', 'compulsory statement'), '@@OPT@@': dl('mention facultative', 'optional statement'),
        '@@FIGEAC@@': label_block('f', 'label_bordeaux_blabla.webp?v=20261024b', 1430, 1100, BX, 'Étiquette imaginaire Château Blabla 1989 / Imaginary Château Blabla 1989 label'),
        '@@ALOXE@@': label_block('a', 'label_bourgogne_coullenot.webp?v=20261024', 1536, 1024, BG, 'Étiquette imaginaire Domaine Coullenot, Beaune 1er Cru Les Grèves 2019 / Imaginary Domaine Coullenot, Beaune 1er Cru Les Grèves 2019 label'),
        '@@NOTE88@@': LL('<b>Une étiquette « millésime 1989 ».</b> Comme une vraie étiquette de l’époque, il lui manque ce qu’exige une étiquette d’aujourd’hui : « contient des sulfites » (depuis 2005), le logo femme enceinte (2007) et, pour les vins produits depuis décembre 2023, la valeur énergétique et le QR code des ingrédients. Le numéro de lot a été ajouté pour l’exemple.' + r('r1169', 'csp', 'd2011', 'r2117'),
                         '<b>A “1989 vintage” label.</b> Like a real label of the time, it lacks what a label needs today: “contains sulphites” (since 2005), the pregnancy logo (2007) and, for wines produced since December 2023, the energy value and the ingredients QR code. The lot number has been added for the example.' + r('r1169', 'csp', 'd2011', 'r2117')),
        '@@NOTENECK@@': LL('<b>Et le reste&nbsp;?</b> « Contient des sulfites » et le logo femme enceinte figurent le plus souvent sur la contre-étiquette, au dos de la bouteille ; le numéro de lot aussi, quand il n’est pas sur l’étiquette ou sur le verre. Un millésime 2019 n’a pas à porter de valeur énergétique : elle n’est obligatoire que pour les vins produits depuis le 8 décembre 2023.' + r('r1169', 'csp', 'd2011', 'r2117'),
                           '<b>And the rest?</b> “Contains sulphites” and the pregnancy logo usually appear on the back label; so does the lot number, when it is not on the label or on the glass. A 2019 vintage need not show an energy value: it is only compulsory for wines produced since 8 December 2023.' + r('r1169', 'csp', 'd2011', 'r2117')),
        '@@CHAMPLABEL@@': label_block('c', 'label_champagne_bubulle.webp?v=20261024', 1536, 1024, CH, 'Étiquette imaginaire Champagne Bubulle Brut Blanc de Blancs 2002 / Imaginary Champagne Bubulle Brut Blanc de Blancs 2002 label'),
        '@@NOTECH@@': LL('<b>Regardez aussi le bouchon.</b> Il porte le nom de l’appellation et, pour un champagne millésimé, l’année. Comme ailleurs, « contient des sulfites » et le logo femme enceinte sont le plus souvent sur la contre-étiquette.' + r('champ', 'r1169', 'csp', 'd2011'),
                         '<b>Look at the cork too.</b> It bears the name of the appellation and, for a vintage champagne, the year. As elsewhere, “contains sulphites” and the pregnancy logo are usually on the back label.' + r('champ', 'r1169', 'csp', 'd2011')),
        '@@MUST_H@@': dl('Obligatoire', 'Compulsory'), '@@MAY_H@@': dl('Facultatif', 'Optional'),
        '@@MUSTCARDS@@': card_grid(MUST, 'fcard" style="--c:#9b2235'), '@@MAYCARDS@@': card_grid(MAY, 'fcard" style="--c:#3a6b8f'),
        '@@STILL@@': table(STILL, [('Mention', 'Term'), ('Sucres', 'Sugar')]),
        '@@SPARK@@': table(SPARK, [('Mention', 'Term'), ('Sucres', 'Sugar')]),
        '@@SUGARREF@@': dl('Sucres résiduels, en grammes par litre.', 'Residual sugar, in grams per litre.') + r('r2019'),
        '@@CHAMPNOTE@@': LL('Deux lettres et un numéro, en petits caractères : ils disent qui a élaboré le champagne.' + r('civc'),
                            'Two letters and a number, in small print: they tell you who made the champagne.' + r('civc'), 'p', 'dimp'),
        '@@CHAMP@@': champ_table(),
        '@@GLOSS@@': card_grid(GLOSS, 'gcard'),
        '@@TRADINTRO@@': LL('Une mention traditionnelle est un terme protégé par l’Union européenne, utilisé de longue date pour désigner une méthode de production ou d’élevage, une qualité, une couleur ou un type de vin. Elle est réservée aux vins AOP et IGP, et seulement si le cahier des charges de l’appellation l’autorise, aux conditions qu’il fixe. « Appellation d’origine contrôlée » est elle-même une mention traditionnelle, comme « château », « clos », « cru classé », « vin jaune » ou « rancio ». Voici les plus courantes sur une étiquette.' + r('tt'),
                            'A traditional term is a term protected by the European Union, long used to describe a method of production or ageing, a quality, a colour or a type of wine. It is reserved for PDO and PGI wines, and only when the appellation’s specification allows it, under the conditions it sets. “Appellation d’origine contrôlée” is itself a traditional term, like “château”, “clos”, “cru classé”, “vin jaune” or “rancio”. Here are the most common ones on a label.' + r('tt')),
        '@@TRAD@@': trad_cards(),
        '@@BIOINTRO@@': LL('Écrire « bio » sur une étiquette n’est jamais obligatoire : c’est le choix du producteur. Mais s’il l’écrit, tout le vin doit être certifié, de la vigne à la bouteille, et l’étiquette doit alors porter certaines mentions.',
                           'Writing “organic” on a label is never compulsory: it is the producer’s choice. But if they write it, the whole wine must be certified, from vine to bottle, and the label must then carry certain statements.'),
        '@@BIO@@': bio_block(),
        '@@SOURCES@@': sources_html(),
        '@@CREDIT@@': dl('D’après la fiche « How to Read a French Wine Label » de Christophe A. Paul (2010), mise à jour et augmentée. Étiquettes imaginaires créées pour ce site : Château Blabla 1989 ; Domaine Coullenot, Beaune 1er Cru « Les Grèves » 2019 ; Champagne Bubulle, Brut Blanc de Blancs 2002.',
                         'Based on the “How to Read a French Wine Label” sheet by Christophe A. Paul (2010), updated and expanded. Imaginary labels created for this site: Château Blabla 1989; Domaine Coullenot, Beaune 1er Cru “Les Grèves” 2019; Champagne Bubulle, Brut Blanc de Blancs 2002.'),
    }
    html = PAGE
    for k, v in rep.items():
        html = html.replace(k, v)
    assert '@@' not in html, html[html.index('@@'):html.index('@@') + 40]
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html)
    print(f'{OUT.relative_to(INFOS.parent)}: {len(html) // 1024} KB, {len(SOURCES)} sources, {len(BX)}+{len(BG)}+{len(CH)} call-outs')


if __name__ == '__main__':
    main()
