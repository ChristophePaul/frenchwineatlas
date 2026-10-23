"""Adds « Le bouchon de liège » (#bouchon) and « Les nouveaux bouchages » (#nouveaux-bouchages) to
Infos/Bottle_Sizes.html, right after the corkscrew section (2026-10-23).
Same method as Infos/_source/corkscrew/add_section.py: the block between <!--ck:start--> and <!--ck:end-->
is (re)written, plus two jump chips and CSS after /*<!--ck-css-->*/. Safe to rerun after editing the texts.
Pictures: Bottle_Sizes_img/cork_*.webp and closure_*.webp, made by prep_images.py from Infos/Corks.
"""
import html
import re
from pathlib import Path

PAGE = Path(__file__).resolve().parents[2] / 'Bottle_Sizes.html'
IMG = PAGE.parent / 'Bottle_Sizes_img'


def A(s):
    return html.escape(s, quote=True)


def bi(tag, fr, en, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c} data-fr="{A(fr)}" data-en="{A(en)}">{fr}</{tag}>'


def R(*n):
    return '<sup class="src">' + ','.join(f'<a href="#ck-src-{k}">{k}</a>' for k in n) + '</sup>'


def U(url, label):
    return f' <a class="u" href="{url}" target="_blank" rel="noopener">{label}</a>'


SOURCES = [
    ('APCOR (Association portugaise du liège), « Montado » : surfaces de chêne-liège par pays (2,12 millions d’ha), longévité moyenne de 200 ans.' + U('https://apcor.pt/en/montado', 'apcor.pt'),
     'APCOR (Portuguese Cork Association), “Montado”: cork oak area by country (2.12 million ha), average lifespan of 200 years.' + U('https://apcor.pt/en/montado', 'apcor.pt')),
    ('Corticeira Amorim, <i>About cork stoppers</i> (brochure du fabricant) : première levée à 25 ans, cycles de 9 ans entre mai et août, qualité « bouchon naturel » après la 3<sup>e</sup> levée (43 ans), repos de 6 mois, bouillage, tubage, ≈ 800 millions de cellules par bouchon.' + U('https://www.amorim.com/xms/files/v1/Documentacao/About_cork_stoppers_final_LR.pdf', 'pdf'),
     'Corticeira Amorim, <i>About cork stoppers</i> (manufacturer’s brochure): first stripping at 25 years, 9-year cycles between May and August, natural-stopper quality after the 3rd stripping (43 years), 6 months’ rest, boiling, punching, ≈ 800 million cells per stopper.' + U('https://www.amorim.com/xms/files/v1/Documentacao/About_cork_stoppers_final_LR.pdf', 'pdf')),
    ('APCOR, « Natural cork stoppers » : tubage, rectification, tri, lavage, colmatage, marquage, paraffine ou silicone, sachets sous SO<sub>2</sub>.' + U('https://apcor.pt/en/natural-cork-stoppers', 'apcor.pt'),
     'APCOR, “Natural cork stoppers”: punching, rectification, sorting, washing, colmating, branding, paraffin or silicone, bags under SO<sub>2</sub>.' + U('https://apcor.pt/en/natural-cork-stoppers', 'apcor.pt')),
    ('Wikipédia (en), « Quercus suber » : levée à la hachette, liège « mâle » ou vierge, <i>secundeira</i>, liège « femelle » des levées suivantes ; abattage interdit au Portugal (décret-loi n° 169/2001).' + U('https://en.wikipedia.org/wiki/Quercus_suber', 'wikipedia'),
     'Wikipedia, “Quercus suber”: stripping with a small axe, “male” or virgin cork, <i>secundeira</i>, “female” cork from later harvests; felling banned in Portugal (Decree-Law No 169/2001).' + U('https://en.wikipedia.org/wiki/Quercus_suber', 'wikipedia')),
    ('Wikipédia (en), « Cork (material) » : composition (≈ 40 % de subérine), liège <i>amadia</i> pour les bouchons, ≈ 60 % de la production de liège transformée en bouchons.' + U('https://en.wikipedia.org/wiki/Cork_(material)', 'wikipedia'),
     'Wikipedia, “Cork (material)”: composition (≈ 40% suberin), <i>amadia</i> cork for stoppers, ≈ 60% of cork output turned into stoppers.' + U('https://en.wikipedia.org/wiki/Cork_(material)', 'wikipedia')),
    ('APCOR, <i>Cork Yearbook 2018/19</i>, résumé par Amorim : le Portugal a 34 % des forêts de chêne-liège et fournit 49,6 % de la production mondiale.' + U('https://amorimcork.com/en/media-center/news/apcors-201819-yearbook-highlights-the-continuing-strong-export-growth-of-cork-stoppers/258', 'amorimcork.com'),
     'APCOR, <i>Cork Yearbook 2018/19</i>, summarised by Amorim: Portugal has 34% of the cork oak forests and supplies 49.6% of world production.' + U('https://amorimcork.com/en/media-center/news/apcors-201819-yearbook-highlights-the-continuing-strong-export-growth-of-cork-stoppers/258', 'amorimcork.com')),
    ('Amorim, fiche technique « NDtech Champagne » : corps en liège aggloméré moulé et 2 rondelles de liège naturel, 48 × 31 mm.' + U('https://www.amorimcork.com/xms/files/Certifications/Bouchons_Champagne_et_effervescents/Fiches_techniques_Bouchons_de_Champagne_et_Vins_effervescents/NDtech-Champagne2HD191008.pdf', 'pdf'),
     'Amorim, “NDtech Champagne” data sheet: moulded agglomerated cork body and 2 natural cork discs, 48 × 31 mm.' + U('https://www.amorimcork.com/xms/files/Certifications/Bouchons_Champagne_et_effervescents/Fiches_techniques_Bouchons_de_Champagne_et_Vins_effervescents/NDtech-Champagne2HD191008.pdf', 'pdf')),
    ('Cahier des charges de l’AOC « Champagne », homologué par l’arrêté du 31 juillet 2025 (JORF du 5 août 2025), chap. I, XII : bouchon portant le nom de l’appellation sur la partie contenue dans le col ; millésime sur le bouchon.',
     'Specification of the “Champagne” AOC, approved by the order of 31 July 2025 (JORF of 5 August 2025), ch. I, XII: stopper bearing the appellation’s name on the part inside the neck; vintage on the stopper.'),
    ('Wikipédia (en), « Cork taint » : TCA identifié par Buser, Zanier et Tanner (1982), précurseur 2,4,6-trichlorophénol, TCA « systémique » des chais (fûts, poutres, palettes), estimations de 1 à 5 % de bouteilles atteintes, baisse de 81 % en 8 ans selon le Cork Quality Council (2013).' + U('https://en.wikipedia.org/wiki/Cork_taint', 'wikipedia'),
     'Wikipedia, “Cork taint”: TCA identified by Buser, Zanier and Tanner (1982), 2,4,6-trichlorophenol precursor, “systemic” TCA in cellars (barrels, beams, pallets), estimates of 1–5% of bottles affected, an 81% fall in 8 years per the Cork Quality Council (2013).' + U('https://en.wikipedia.org/wiki/Cork_taint', 'wikipedia')),
    ('Cappellin L. <i>et al.</i> (2020). Thermal desorption–Vocus enables online nondestructive quantification of 2,4,6-trichloroanisole in cork stoppers. <i>Analytical Chemistry</i> (vin perçu comme bouchonné dès 1–2 ng/l ; < 0,5 ng/l négligeable).' + U('https://www.research.unipd.it/handle/11577/3357955', 'unipd'),
     'Cappellin L. <i>et al.</i> (2020). Thermal desorption–Vocus enables online nondestructive quantification of 2,4,6-trichloroanisole in cork stoppers. <i>Analytical Chemistry</i> (wine perceived as corked from 1–2 ng/L; < 0.5 ng/L negligible).' + U('https://www.research.unipd.it/handle/11577/3357955', 'unipd')),
    ('Wikipédia (en), « Screw cap (wine) » : demande de Peter Wall (Yalumba) en 1964, Stelvin du Bouchage Mécanique, essais suisses 1970–1971, Hammel 1972, marque déposée en 1975, Clare Valley 2000, Domaine Laroche 2001, joint en PVDC, risque de réduction, Nouvelle-Zélande de 1 % (2001) à 70 % (2004).' + U('https://en.wikipedia.org/wiki/Screw_cap_(wine)', 'wikipedia'),
     'Wikipedia, “Screw cap (wine)”: Peter Wall’s (Yalumba) request in 1964, Le Bouchage Mécanique’s Stelvin, Swiss trials 1970–1971, Hammel 1972, trademark registered 1975, Clare Valley 2000, Domaine Laroche 2001, PVDC liner, risk of reduction, New Zealand from 1% (2001) to 70% (2004).' + U('https://en.wikipedia.org/wiki/Screw_cap_(wine)', 'wikipedia')),
    ('J. Goode, « The New Zealand Screwcap Initiative », <i>Wine Anorak</i> (fondée en 2001, un an après les rieslings de Clare Valley).' + U('https://wineanorak.com/new_zealand_screwcap_initiative.htm', 'wineanorak.com'),
     'J. Goode, “The New Zealand Screwcap Initiative”, <i>Wine Anorak</i> (founded in 2001, a year after the Clare Valley rieslings).' + U('https://wineanorak.com/new_zealand_screwcap_initiative.htm', 'wineanorak.com')),
    ('Vinventions, « Celebrating 25 years of innovation: from Nomacorc to global wine &amp; spirit solutions » (premier bouchon synthétique sans goût de bouchon, 1999) ; Wikipédia (en), « Nomacorc » (Gert et Marc Noël, co-extrusion, Vinventions en 2015, gamme « Green Line » en polymères de canne à sucre).' + U('https://us.vinventions.com/en/articles/news/celebrating-25-years-of-innovation-vinventions-and-the-journey-from-nomacorc-to-global-wine-spirit-solutions', 'vinventions.com') + U('https://en.wikipedia.org/wiki/Nomacorc', 'wikipedia'),
     'Vinventions, “Celebrating 25 years of innovation: from Nomacorc to global wine &amp; spirit solutions” (the first taint-free synthetic closure, 1999); Wikipedia, “Nomacorc” (Gert and Marc Noël, co-extrusion, Vinventions in 2015, “Green Line” range in sugar-cane polymers).' + U('https://us.vinventions.com/en/articles/news/celebrating-25-years-of-innovation-vinventions-and-the-journey-from-nomacorc-to-global-wine-spirit-solutions', 'vinventions.com') + U('https://en.wikipedia.org/wiki/Nomacorc', 'wikipedia')),
    ('Vinventions, fiches « Nomacorc Classic Green » et « Nomacorc nolow » (données du fabricant : ≈ 1,7 et 0,6 mg d’oxygène par an après la 1<sup>re</sup> année).' + U('https://cms.us.vinventions.com/files/uploads/sites/3/2023/12/NOMACORC-Classic-Green.pdf', 'pdf') + U('https://eu.vinventions.com/en/solutions/nomacorc/nolow/', 'vinventions.com'),
     'Vinventions, “Nomacorc Classic Green” and “Nomacorc nolow” sheets (manufacturer data: ≈ 1.7 and 0.6 mg of oxygen per year after the 1st year).' + U('https://cms.us.vinventions.com/files/uploads/sites/3/2023/12/NOMACORC-Classic-Green.pdf', 'pdf') + U('https://eu.vinventions.com/en/solutions/nomacorc/nolow/', 'vinventions.com')),
    ('« Corking idea from Sabaté », <i>BeverageDaily</i>, 21 avril 2004 (procédé Diamant mis au point avec le CEA, production industrielle prévue en 2005) ; « DIAMANT®, an innovative solution to the smell of cork in wine », NetworkNature (CO<sub>2</sub> supercritique ; garantie fabricant ≤ 0,3 ng/l de TCA relargable).' + U('https://www.beveragedaily.com/Article/2004/04/21/Corking-idea-from-Sabate/', 'beveragedaily.com') + U('https://networknature.eu/node/20130', 'networknature.eu'),
     '“Corking idea from Sabaté”, <i>BeverageDaily</i>, 21 April 2004 (Diamant process developed with the CEA, industrial production planned for 2005); “DIAMANT®, an innovative solution to the smell of cork in wine”, NetworkNature (supercritical CO<sub>2</sub>; manufacturer’s guarantee ≤ 0.3 ng/L of releasable TCA).' + U('https://www.beveragedaily.com/Article/2004/04/21/Corking-idea-from-Sabate/', 'beveragedaily.com') + U('https://networknature.eu/node/20130', 'networknature.eu')),
    ('Wein-plus, glossaire « Vinolok » (mis au point par Alcoa à Worms, sur le marché européen en 2003, en série l’année suivante) ; Corticeira Amorim, communiqué du 25 juillet 2019 (Preciosa développe Vinolok depuis 2011 ; Amorim en achète 50 %).' + U('https://glossary.wein-plus.eu/vinolok', 'wein-plus.eu') + U('https://www.amorim.com/xms/files/v1/Investidores/7_Comunicados/20190725VinolokEN.pdf', 'pdf'),
     'Wein-plus glossary, “Vinolok” (developed by Alcoa in Worms, on the European market in 2003, in series production a year later); Corticeira Amorim, press release of 25 July 2019 (Preciosa has developed Vinolok since 2011; Amorim buys 50%).' + U('https://glossary.wein-plus.eu/vinolok', 'wein-plus.eu') + U('https://www.amorim.com/xms/files/v1/Investidores/7_Comunicados/20190725VinolokEN.pdf', 'pdf')),
    ('Wikipédia (en), « Crown cork » : capsule couronne brevetée par William Painter le 2 février 1892.' + U('https://en.wikipedia.org/wiki/Crown_cork', 'wikipedia'),
     'Wikipedia, “Crown cork”: crown cap patented by William Painter on 2 February 1892.' + U('https://en.wikipedia.org/wiki/Crown_cork', 'wikipedia')),
]

# ---------------------------------------------------------------- cork: key figures
KEYS = [('2,1 M ha', '2.1 M ha', 'de forêts de chêne-liège, autour de la Méditerranée occidentale', 'of cork oak forest around the western Mediterranean', (1,)),
        ('≈ 50 %', '≈ 50%', 'du liège mondial vient du Portugal', 'of the world’s cork comes from Portugal', (6,)),
        ('25 ans', '25 years', 'avant la première levée de l’écorce', 'before the bark is stripped for the first time', (2,)),
        ('9 ans', '9 years', 'entre deux levées, toujours de mai à août', 'between two strippings, always May to August', (2,)),
        ('43 ans', '43 years', 'pour un liège digne d’un bouchon naturel (3<sup>e</sup> levée)', 'for cork fit for a natural stopper (3rd stripping)', (2,)),
        ('200 ans', '200 years', 'de vie moyenne pour un chêne-liège', 'average life of a cork oak', (1,))]

AREA = [('Portugal', 'Portugal', 720), ('Espagne', 'Spain', 574), ('Maroc', 'Morocco', 383), ('Algérie', 'Algeria', 230),
        ('Tunisie', 'Tunisia', 86), ('France', 'France', 65), ('Italie', 'Italy', 65)]

# (img, title FR, title EN, text FR, text EN)
STEPS = [
    ('cork_tree', 'Le chêne-liège', 'The cork oak',
     '<i>Quercus suber</i> pousse au Portugal, en Espagne, au Maghreb, en France et en Italie. Son écorce épaisse, le liège, se reforme après chaque récolte : c’est le seul arbre que l’on « écorce » sans le tuer. Au Portugal, on ne peut l’abattre qu’avec une autorisation.' + R(1, 4),
     '<i>Quercus suber</i> grows in Portugal, Spain, North Africa, France and Italy. Its thick bark — cork — grows back after each harvest: it is the only tree stripped of its bark without being killed. In Portugal it may only be felled with official permission.' + R(1, 4)),
    ('cork_stacks', 'La levée', 'Stripping',
     'De mai à août, quand l’arbre est en pleine croissance, des ouvriers spécialisés détachent l’écorce à la hachette, sans machine. La 1<sup>re</sup> levée (liège « vierge », vers 25 ans) et la 2<sup>e</sup> donnent un liège irrégulier, destiné aux isolants ; le liège de qualité bouchon ne vient qu’à partir de la 3<sup>e</sup> levée, vers 43 ans.' + R(2, 4, 5),
     'From May to August, when the tree is growing fastest, skilled workers prise off the bark with a small axe, with no machinery. The 1st stripping (“virgin” cork, around 25 years) and the 2nd give irregular cork, used for insulation; stopper-grade cork only comes from the 3rd stripping, at about 43 years.' + R(2, 4, 5)),
    ('cork_slab', 'Repos et bouillage', 'Rest and boiling',
     'Les planches de liège reposent au moins six mois pour atteindre la bonne humidité, puis sont bouillies dans des cuves fermées : le liège s’assouplit, se nettoie et sa structure se détend.' + R(2),
     'The cork planks rest for at least six months to reach the right moisture, then are boiled in closed tanks: the cork softens, is cleaned and its structure relaxes.' + R(2)),
    ('cork_punched', 'Le tubage', 'Punching',
     'Les planches sont découpées en bandes de la hauteur d’un bouchon, puis percées à l’emporte-pièce (« tubées ») pour en sortir des cylindres. Les chutes ne sont pas perdues : broyées en granulés, elles serviront aux bouchons agglomérés.' + R(2, 3),
     'The planks are cut into strips as tall as a stopper, then punched to extract cylinders. Offcuts are not wasted: ground into granules, they make agglomerated stoppers.' + R(2, 3)),
    ('closure_natural', 'Finitions', 'Finishing',
     'Rectification aux cotes, tri en classes (souvent par caméra), lavage désinfectant, marquage à l’encre, au feu ou au laser, puis une fine couche de paraffine ou de silicone pour glisser dans le col. Les bouchons voyagent en sachets saturés de SO<sub>2</sub>.' + R(3),
     'Grinding to size, sorting into grades (often by camera), disinfecting wash, branding with ink, fire or laser, then a thin coat of paraffin or silicone so it slides into the neck. Stoppers travel in bags filled with SO<sub>2</sub>.' + R(3)),
]

# (img or None, title FR, title EN, kicker FR, kicker EN, text FR, text EN)
CORKS = [
    ('mycork_natural', 'Le bouchon naturel', 'Natural cork', 'D’une seule pièce', 'One piece',
     'Tubé directement dans l’écorce. Le plus noble et le plus cher, réservé aux vins de garde ; sa qualité varie d’un bouchon à l’autre selon les « lenticelles », ces pores qui traversent le liège.' + R(2, 3),
     'Punched straight from the bark. The finest and dearest, kept for wines meant to age; quality varies from cork to cork with the “lenticels”, the pores running through it.' + R(2, 3)),
    ('mycork_colmate', 'Le bouchon colmaté', 'Colmated cork', 'Naturel « rebouché »', 'Natural, pores filled',
     'Un bouchon naturel dont les pores de surface sont comblés avec de la poudre de liège et une colle : il a meilleure mine et ferme mieux.' + R(3),
     'A natural cork whose surface pores are filled with cork powder and glue: it looks better and seals better.' + R(3)),
    ('mycork_agglo', 'Le bouchon aggloméré', 'Agglomerated cork', 'Granulés de liège', 'Cork granules',
     'Des granulés de liège liés et moulés en cylindre. Régulier et bon marché, pour les vins à boire jeunes ; il naît des chutes du tubage.' + R(3),
     'Cork granules bound and moulded into a cylinder. Consistent and cheap, for wines to drink young; it is made from punching offcuts.' + R(3)),
    ('mycork_1plus1', 'Le bouchon technique « 1+1 »', 'The “1+1” technical cork', 'Aggloméré + rondelles', 'Agglomerated + discs',
     'Un corps aggloméré avec une rondelle de liège naturel collée à chaque bout : seul le liège naturel touche le vin.' + R(7),
     'An agglomerated body with a natural cork disc glued to each end: only natural cork touches the wine.' + R(7)),
    ('mycork_champagne', 'Le bouchon de champagne', 'The Champagne cork', '48 × 31 mm avant compression', '48 × 31 mm before compression',
     'Un gros corps aggloméré et deux rondelles de liège naturel côté vin, comprimé de force dans le col — d’où sa forme de champignon une fois sorti. En AOC Champagne, il doit porter le nom de l’appellation sur la partie logée dans le col, et le millésime s’il y en a un.' + R(7, 8),
     'A large agglomerated body and two natural cork discs on the wine side, forced into the neck — hence its mushroom shape once out. For AOC Champagne it must bear the appellation’s name on the part inside the neck, and the vintage if there is one.' + R(7, 8)),
]

# ---------------------------------------------------------------- new closures
TIMELINE = [
    ('1892', 'Baltimore', '1892', 'Baltimore', 'La capsule couronne', 'The crown cap',
     'William Painter brevète la capsule métallique sertie sur le goulot. Elle ferme aujourd’hui les bouteilles de champagne et de crémant pendant leur prise de mousse, avant le bouchon définitif.' + R(18),
     'William Painter patents the metal cap crimped onto the bottle lip. Today it seals Champagne and crémant bottles during their second fermentation, before the final cork.' + R(18)),
    ('1964', 'France · Australie', '1964', 'France · Australia', 'Naissance du Stelvin', 'Birth of the Stelvin',
     'Peter Wall, du domaine australien Yalumba, demande au français <b>Le Bouchage Mécanique</b> une capsule à vis pour le vin. Essayée en Suisse sur des chasselas en 1970–1971, elle est commercialisée en 1972 ; la marque « Stelvin » est déposée en 1975.' + R(11),
     'Peter Wall of the Australian winery Yalumba asks the French firm <b>Le Bouchage Mécanique</b> for a wine screw cap. Trialled in Switzerland on Chasselas in 1970–1971, it is sold from 1972; the “Stelvin” trademark is registered in 1975.' + R(11)),
    ('1999', 'Belgique · États-Unis', '1999', 'Belgium · United States', 'Nomacorc', 'Nomacorc',
     'Gert et Marc Noël lancent le premier bouchon synthétique co-extrudé sans goût de bouchon : un cœur en mousse et une peau souple soudée autour.' + R(13),
     'Gert and Marc Noël launch the first co-extruded, taint-free synthetic closure: a foam core with a flexible skin bonded around it.' + R(13)),
    ('2000', 'Clare Valley', '2000', 'Clare Valley', 'La révolution de la capsule', 'The screw-cap revolution',
     'En juillet, des producteurs de riesling de la Clare Valley, menés par Jeffrey Grosset, mettent ensemble leurs vins sous capsule à vis. L’année suivante naît la <i>New Zealand Screwcap Initiative</i> : la Nouvelle-Zélande passe de 1 % de capsules en 2001 à 70 % en 2004.' + R(11, 12),
     'In July, Clare Valley riesling growers led by Jeffrey Grosset bottle their wines under screw cap together. The next year the <i>New Zealand Screwcap Initiative</i> is born: New Zealand goes from 1% screw caps in 2001 to 70% in 2004.' + R(11, 12)),
    ('2001', 'Chablis', '2001', 'Chablis', 'Un pionnier français', 'A French pioneer',
     'Le Domaine Laroche adopte la capsule à vis à partir du millésime 2001, jusque sur ses chablis.' + R(11),
     'Domaine Laroche adopts the screw cap from the 2001 vintage, even for its Chablis.' + R(11)),
    ('2001 · 2005', 'Espagne · France', '2001 · 2005', 'Spain · France', 'Diam', 'Diam',
     'Le bouchonnier Sabaté et le Commissariat à l’énergie atomique (CEA) mettent au point le procédé « Diamant » : le liège en granulés est nettoyé au CO<sub>2</sub> supercritique, comme on décaféine le café. Brevet en 2001, production industrielle à partir de 2005.' + R(15),
     'The cork maker Sabaté and France’s Atomic Energy Commission (CEA) develop the “Diamant” process: granulated cork is cleaned with supercritical CO<sub>2</sub>, the way coffee is decaffeinated. Patent in 2001, industrial production from 2005.' + R(15)),
    ('2003', 'Worms', '2003', 'Worms', 'Le bouchon de verre', 'The glass stopper',
     'Alcoa lance en Allemagne le <b>Vino-Lok</b>, un bouchon de verre avec un joint torique. Le cristallier tchèque Preciosa le reprend en 2011 sous le nom <b>Vinolok</b> ; Amorim en rachète la moitié en 2019.' + R(16),
     'Alcoa launches the <b>Vino-Lok</b> in Germany, a glass stopper with an O-ring seal. The Czech crystal maker Preciosa takes it over in 2011 as <b>Vinolok</b>; Amorim buys half of it in 2019.' + R(16)),
]

NEW = [
    ('closure_screwcap', 'La capsule à vis (Stelvin)', 'The screw cap (Stelvin)', 'Aluminium + joint', 'Aluminium + liner',
     'Une jupe d’aluminium vissée sur un goulot fileté, avec un joint intérieur (souvent en PVDC) qui règle le passage de l’oxygène. Aucun goût de bouchon, ouverture sans outil ; le revers : un vin trop « réduit » peut sentir l’œuf ou l’allumette, faute d’oxygène.' + R(11),
     'An aluminium skirt screwed onto a threaded neck, with an inner liner (often PVDC) that controls oxygen. No cork taint, opens without a tool; the downside: a wine that is too “reduced” can smell of egg or struck match, for lack of oxygen.' + R(11)),
    ('mycork_synth', 'Le synthétique co-extrudé (Nomacorc)', 'Co-extruded synthetic (Nomacorc)', 'Polymères', 'Polymers',
     'Un cylindre de mousse gainé d’une peau souple. Chaque modèle laisse passer une quantité d’oxygène choisie, par exemple ≈ 0,6 ou 1,7 mg par an selon le fabricant ; certaines gammes sont faites de polymères issus de la canne à sucre.' + R(13, 14),
     'A foam cylinder sheathed in a flexible skin. Each model lets through a chosen amount of oxygen, e.g. ≈ 0.6 or 1.7 mg a year according to the maker; some ranges use polymers made from sugar cane.' + R(13, 14)),
    ('mycork_micro', 'Le bouchon technique traité (Diam)', 'Treated technical cork (Diam)', 'Liège nettoyé au CO<sub>2</sub>', 'CO<sub>2</sub>-cleaned cork',
     'Du vrai liège micro-aggloméré, débarrassé de ses molécules odorantes par le CO<sub>2</sub> supercritique. Le fabricant garantit chaque bouchon à moins de 0,3 ng/l de TCA relargable.' + R(15),
     'Real micro-agglomerated cork, stripped of its odorous molecules by supercritical CO<sub>2</sub>. The maker guarantees each stopper below 0.3 ng/L of releasable TCA.' + R(15)),
    ('closure_glass', 'Le bouchon de verre (Vinolok)', 'The glass stopper (Vinolok)', 'Verre + joint torique', 'Glass + O-ring',
     'Un bouchon de verre qui s’enfonce dans un col adapté et ferme grâce à un joint ; il se rebouche à volonté. Élégant mais cher, il demande des bouteilles spéciales.' + R(16),
     'A glass stopper pushed into a matching neck, sealed by an O-ring; it can be re-closed at will. Elegant but dear, it needs special bottles.' + R(16)),
    ('mycork_crown', 'La capsule couronne', 'The crown cap', 'Acier serti', 'Crimped steel',
     'La capsule des bières ferme aussi les vins effervescents pendant leur seconde fermentation en bouteille, et parfois quelques vins tranquilles ou pétillants naturels vendus tels quels.' + R(18),
     'The beer-bottle cap also seals sparkling wines during their second fermentation in bottle, and sometimes a few still or pét-nat wines sold as they are.' + R(18)),
]

COMPARE = [
    # name FR, name EN, material FR, EN, oxygen FR, EN, taint FR, EN
    ('Liège naturel', 'Natural cork', 'Écorce de chêne-liège', 'Cork oak bark', 'Faible, variable d’un bouchon à l’autre', 'Low, varies from cork to cork', 'Possible', 'Possible'),
    ('Aggloméré, 1+1', 'Agglomerated, 1+1', 'Granulés de liège liés', 'Bound cork granules', 'Régulier', 'Consistent', 'Possible (réduit si traité)', 'Possible (lower if treated)'),
    ('Diam', 'Diam', 'Liège micro-aggloméré traité au CO₂', 'CO₂-treated micro-agglomerated cork', 'Régulier, plusieurs niveaux', 'Consistent, several levels', 'Garanti ≤ 0,3 ng/l (fabricant)', 'Guaranteed ≤ 0.3 ng/L (maker)'),
    ('Synthétique (Nomacorc)', 'Synthetic (Nomacorc)', 'Polymères, parfois végétaux', 'Polymers, some plant-based', 'Fixé par modèle', 'Set by model', 'Aucun (pas de liège)', 'None (no cork)'),
    ('Capsule à vis (Stelvin)', 'Screw cap (Stelvin)', 'Aluminium + joint', 'Aluminium + liner', 'Très faible, selon le joint', 'Very low, depends on liner', 'Aucun ; risque de réduction', 'None; risk of reduction'),
    ('Verre (Vinolok)', 'Glass (Vinolok)', 'Verre + joint torique', 'Glass + O-ring', 'Très faible', 'Very low', 'Aucun', 'None'),
]

CSS = '''
  /* cork + new closures (ck) */
  .ck-keys{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:10px;margin:0 0 16px;}
  .ck-key{padding:12px 14px;border-radius:14px;border:1px solid var(--hair);background:var(--chip);}
  .ck-key b{display:block;font-family:var(--serif);font-weight:500;font-size:22px;color:var(--title);line-height:1.1;}
  .ck-key small{font-size:12px;line-height:1.4;color:var(--muted);}
  .ck-area{display:grid;gap:5px;margin-top:6px;}
  .ck-area div{display:grid;grid-template-columns:72px 1fr 54px;gap:8px;align-items:center;font-size:12.5px;color:var(--muted);}
  .ck-area .bar{height:9px;border-radius:5px;background:var(--hair);overflow:hidden;}
  .ck-area .bar span{display:block;height:100%;border-radius:5px;background:linear-gradient(90deg,#b07a4f,#d9a66b);}
  .ck-area b{color:var(--title);font-weight:600;text-align:right;}
  .ck-steps{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin-top:4px;counter-reset:ck;}
  .ck-steps .tv-card{position:relative;}
  .ck-steps .tv-card::before{counter-increment:ck;content:counter(ck);position:absolute;top:12px;left:14px;width:24px;height:24px;border-radius:50%;
    display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:var(--title);border:1px solid var(--hair-hi);background:var(--chip);z-index:2;}
  .ck-steps .tv-card .ph img.photo{border-radius:10px;object-fit:cover;width:100%;height:100%;}
  .ck-gal{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:12px;margin-top:4px;}
  .ck-gal .tv-card .meta{font-size:10.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-top:2px;}
  .ck-gal .tv-card.noimg h3{margin-top:2px;}
  .ck-two{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:16px;}
  .ck-taint{border-left:3px solid #b07a4f;}
  .ck-cmp{width:100%;border-collapse:collapse;font-size:13px;margin-top:6px;}
  .ck-cmp th,.ck-cmp td{padding:9px 10px;border-bottom:1px solid var(--hair);text-align:left;vertical-align:top;color:var(--muted);}
  .ck-cmp tr:first-child th{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);}
  .ck-cmp td:first-child{color:var(--title);font-family:var(--serif);font-size:15px;white-space:nowrap;}
  .ck-wrap{overflow-x:auto;}
  .ck-credit{text-align:right;}
  .hist-intro h3.ck-h{font-family:var(--sans);font-size:10.5px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);margin:14px 0 6px;}
  #bouchon p.note,#nouveaux-bouchages p.note{font-size:12px !important;color:var(--faint) !important;margin:8px 0 0 !important;}
  .ph-slice{margin-top:10px;text-align:center;} .ph-slice img{max-width:100%;max-height:150px;width:auto;filter:drop-shadow(0 10px 16px rgba(0,0,0,.35));}
  @media (max-width:1000px){ .ck-keys{grid-template-columns:repeat(3,minmax(0,1fr));} .ck-steps,.ck-gal{grid-template-columns:repeat(3,minmax(0,1fr));} }
  @media (max-width:760px){ .ck-two{grid-template-columns:1fr;} .ck-steps,.ck-gal{grid-template-columns:repeat(2,minmax(0,1fr));} }
  @media (max-width:480px){ .ck-keys{grid-template-columns:repeat(2,minmax(0,1fr));} .ck-steps,.ck-gal{grid-template-columns:1fr;} }
'''


def img(key, alt, photo=False):
    if not (IMG / f'{key}.webp').exists():
        return ''
    c = ' class="photo"' if photo else ''
    v = int((IMG / f'{key}.webp').stat().st_mtime)   # cache-buster: pictures get replaced under the same name
    return f'<img{c} src="Bottle_Sizes_img/{key}.webp?v={v}" alt="{A(alt)}" loading="lazy" draggable="false">'


def card(k, nf, ne, xf, xe, mf=None, me=None, photo=False):
    ph = img(k, nf + ' / ' + ne, photo) if k else ''
    meta = bi('div', mf, me, 'meta') if mf else ''
    cls = 'panel tv-card' + ('' if ph else ' noimg')
    return f'<article class="{cls}">' + (f'<div class="ph">{ph}</div>' if ph else '') + f'{bi("h3", nf, ne)}{meta}{bi("p", xf, xe)}</article>'


def section():
    keys = ''.join(f'<div class="ck-key">{bi("b", vf, ve)}{bi("small", lf + R(*s), le + R(*s))}</div>' for vf, ve, lf, le, s in KEYS)
    mx = max(v for *_, v in AREA)
    area = ''.join(f'<div>{bi("span", f, e)}<span class="bar"><span style="width:{v / mx * 100:.0f}%"></span></span><b>{v}&#8239;k</b></div>' for f, e, v in AREA)
    steps = ''.join(card(k, tf, te, xf, xe, photo=(k == 'cork_stacks')) for k, tf, te, xf, xe in STEPS)
    corks = ''.join(card(k, nf, ne, xf, xe, mf, me) for k, nf, ne, mf, me, xf, xe in CORKS)
    tl = ''.join(
        f'<li><div class="when" data-fr="{A(wf + "<small>" + pf + "</small>")}" data-en="{A(we + "<small>" + pe + "</small>")}">{wf}<small>{pf}</small></div>'
        f'<div class="what">{bi("h3", tf, te)}{bi("p", xf, xe)}</div></li>'
        for wf, pf, we, pe, tf, te, xf, xe in TIMELINE)
    new = ''.join(card(k, nf, ne, xf, xe, mf, me) for k, nf, ne, mf, me, xf, xe in NEW)
    head = ('<tr>' + ''.join(f'<th data-fr="{A(f)}" data-en="{A(e)}">{f}</th>' for f, e in
            [('Bouchage', 'Closure'), ('Matière', 'Material'), ('Oxygène', 'Oxygen'), ('Goût de bouchon', 'Cork taint')]) + '</tr>')
    rows = ''.join('<tr>' + ''.join(f'<td data-fr="{A(row[i])}" data-en="{A(row[i + 1])}">{row[i]}</td>' for i in (0, 2, 4, 6)) + '</tr>' for row in COMPARE)
    srcs = ''.join(f'<li id="ck-src-{i}" data-fr="{A(f)}" data-en="{A(e)}">{f}</li>' for i, (f, e) in enumerate(SOURCES, 1))

    intro_fr = ('Le liège ferme les bouteilles de vin depuis la fin du XVII<sup>e</sup> siècle, quand le verre anglais devient assez solide pour le recevoir. '
                'C’est l’écorce d’un seul arbre, le <b>chêne-liège</b>, qui pousse autour de la Méditerranée occidentale. '
                'Environ 60 % du liège récolté dans le monde devient des bouchons.' + R(5))
    intro_en = ('Cork has sealed wine bottles since the late 17th century, when English glass became strong enough to take it. '
                'It is the bark of a single tree, the <b>cork oak</b>, which grows around the western Mediterranean. '
                'About 60% of the cork harvested in the world becomes stoppers.' + R(5))
    why_fr = ('Léger, compressible, élastique, imperméable aux liquides : le liège est fait de cellules mortes remplies d’un gaz proche de l’air, '
              'dont les parois contiennent ≈ 40 % de <b>subérine</b>, une cire naturelle. Un bouchon en compte ≈ 800 millions : comprimé dans le col, il reprend sa forme et colle au verre.' + R(2, 5))
    why_en = ('Light, compressible, springy and liquid-tight: cork is made of dead cells filled with an air-like gas, '
              'whose walls hold ≈ 40% <b>suberin</b>, a natural wax. A stopper has ≈ 800 million of them: squeezed into the neck, it springs back and grips the glass.' + R(2, 5))
    taint_fr = [('Le goût de bouchon', 'Cork taint'),
                ('Un vin « bouchonné » sent le carton mouillé, la cave humide, le champignon, et perd son fruit. Le principal coupable est le <b>2,4,6-trichloroanisole (TCA)</b>, identifié en 1982 par Buser, Zanier et Tanner. Il naît quand des moisissures transforment des chlorophénols (anciens biocides, traitements au chlore) présents dans le bois ou le liège.' + R(9),
                 'A “corked” wine smells of wet cardboard, damp cellar or mushroom, and loses its fruit. The main culprit is <b>2,4,6-trichloroanisole (TCA)</b>, identified in 1982 by Buser, Zanier and Tanner. It forms when moulds transform chlorophenols (old biocides, chlorine treatments) present in wood or cork.' + R(9)),
                ('Il en faut très peu : un vin est perçu comme bouchonné dès <b>1 à 2 ng/l</b> — un milliardième de gramme par litre. On estimait autrefois qu’1 à 5 % des bouteilles étaient touchées ; les contrôles individuels des bouchons ont fait chuter les teneurs (−81 % en huit ans selon le Cork Quality Council, 2013). Le bouchon n’est pas toujours coupable : fûts, poutres ou palettes d’un chai contaminé peuvent gâter toute une cuvée.' + R(9, 10),
                 'It takes very little: a wine is perceived as corked from <b>1–2 ng/L</b> — a billionth of a gram per litre. It was once estimated that 1 to 5% of bottles were affected; individual cork screening has brought levels down (−81% in eight years per the Cork Quality Council, 2013). The cork is not always to blame: barrels, beams or pallets in a contaminated cellar can spoil a whole batch.' + R(9, 10))]
    keep = [('Pourquoi coucher les bouteilles ?', 'Why lay bottles down?'),
            ('Un bouchon de liège qui sèche se rétracte et laisse entrer l’air. On couche donc les bouteilles bouchées au liège, pour que le vin garde le bouchon humide, dans une cave fraîche, sombre et assez humide. Les capsules à vis et les bouchons synthétiques ou de verre n’ont pas ce souci : ces bouteilles peuvent rester debout.',
             'A cork that dries out shrinks and lets air in. So bottles sealed with cork are laid on their side, keeping the cork moist, in a cool, dark, fairly humid cellar. Screw caps and synthetic or glass stoppers have no such problem: those bottles can stand upright.')]

    return f'''<!--ck:start-->
  <!-- ===== cork + new closures (Infos/_source/cork/add_section.py) ===== -->
  <section class="sec" id="bouchon">
    <div class="sec-head"><div>
      {bi("h2", "Le <em>bouchon</em> de liège", "The <em>cork</em> stopper")}
      {bi("p", "De l’écorce du chêne-liège au col de la bouteille : l’arbre, la récolte, la fabrication, les types de bouchons et le goût de bouchon.", "From the cork oak’s bark to the bottle neck: the tree, the harvest, the making, the kinds of stoppers and cork taint.")}
    </div></div>
    <div class="panel hist-intro">
      <div>{bi("p", intro_fr, intro_en)}
        {bi("h3", "Où pousse le chêne-liège (milliers d’hectares)", "Where the cork oak grows (thousand hectares)", "ck-h")}
        <div class="ck-area">{area}</div>{bi("p", "Surfaces de chêne-liège par pays, total ≈ 2,12 millions d’ha." + R(1), "Cork oak area by country, total ≈ 2.12 million ha." + R(1), "note")}</div>
      <div class="who">{bi("h3", "Pourquoi le liège&nbsp;?", "Why cork?")}{bi("p", why_fr, why_en)}<div class="ph-slice">{img("cork_slice", "Coupe d’un tronc de chêne-liège / Cross-section of a cork oak trunk")}</div></div>
    </div>
    <div class="ck-keys">{keys}</div>
    <div class="sec-head" style="margin-top:22px"><div>{bi("h2", "Du chêne <em>au bouchon</em>", "From oak <em>to stopper</em>")}</div></div>
    <div class="ck-steps" id="bouchon-fabrication">{steps}</div>
    <div class="sec-head" style="margin-top:26px"><div>{bi("h2", "Les bouchons <em>de liège</em>", "Cork <em>stoppers</em>")}</div></div>
    <div class="ck-gal" id="bouchon-types">{corks}</div>
    {bi("p", "Photos des bouchons : © 2026 Christophe A. Paul.", "Cork photos: © 2026 Christophe A. Paul.", "note ck-credit")}
    <div class="ck-two">
      <div class="panel tv-box ck-taint" id="gout-de-bouchon">{bi("h3", *taint_fr[0])}{bi("p", *taint_fr[1])}{bi("p", *taint_fr[2])}</div>
      <div class="panel tv-box">{bi("h3", *keep[0])}{bi("p", *keep[1])}</div>
    </div>
  </section>

  <section class="sec" id="nouveaux-bouchages">
    <div class="sec-head"><div>
      {bi("h2", "Les <em>nouveaux</em> bouchages", "<em>New</em> closures")}
      {bi("p", "Capsule à vis Stelvin, synthétique Nomacorc, liège traité Diam, verre Vinolok : comment le goût de bouchon a ouvert la porte à d’autres solutions.", "Stelvin screw cap, Nomacorc synthetic, Diam treated cork, Vinolok glass: how cork taint opened the door to other solutions.")}
    </div></div>
    <div class="panel hist-intro">
      <div>{bi("p", "Dans les années 1980–1990, le goût de bouchon et l’irrégularité du liège poussent les vignerons à chercher autre chose. Deux idées guident les inventeurs : supprimer le risque de TCA, et maîtriser la quantité d’<b>oxygène</b> qui traverse le bouchage au fil des années — un peu pour un vin qui doit évoluer, presque rien pour un vin à boire sur le fruit." + R(9, 11, 14), "In the 1980s and 1990s, cork taint and the irregularity of cork pushed winemakers to look elsewhere. Two ideas guided the inventors: remove the risk of TCA, and control how much <b>oxygen</b> passes through the closure over the years — a little for a wine meant to evolve, almost none for a wine to drink on its fruit." + R(9, 11, 14))}</div>
      <div class="who">{bi("h3", "Et en France&nbsp;?", "And in France?")}{bi("p", "Le liège reste dominant, surtout pour les vins de garde, et il est même obligatoire en Champagne, où le bouchon doit porter le nom de l’appellation. Mais la capsule à vis a gagné des vins blancs et rosés à boire jeunes, et le Domaine Laroche l’a adoptée dès 2001 à Chablis." + R(8, 11), "Cork is still dominant, especially for wines meant to age, and it is even compulsory in Champagne, where the stopper must bear the appellation’s name. But the screw cap has won over whites and rosés to drink young, and Domaine Laroche adopted it as early as 2001 in Chablis." + R(8, 11))}</div>
    </div>
    <div class="panel"><ol class="tl">{tl}</ol></div>
    <div class="sec-head" style="margin-top:26px"><div>{bi("h2", "Les <em>alternatives</em> au liège", "The <em>alternatives</em> to cork")}</div></div>
    <div class="ck-gal" id="nouveaux-bouchages-types">{new}</div>
    {bi("p", "Photos des bouchons Diam, Nomacorc et de la capsule couronne : © 2026 Christophe A. Paul.", "Photos of the Diam, Nomacorc and crown-cap closures: © 2026 Christophe A. Paul.", "note ck-credit")}
    <div class="panel tv-box" style="margin-top:16px">{bi("h3", "En un coup d’œil", "At a glance")}<div class="ck-wrap"><table class="ck-cmp">{head}{rows}</table></div>
      {bi("p", "Comparaison simplifiée ; les valeurs d’oxygène dépendent du modèle exact et sont surtout fournies par les fabricants.", "Simplified comparison; oxygen values depend on the exact model and come mostly from the manufacturers.", "note")}</div>
    <div class="panel tv-box tv-sources" id="bouchon-sources">
      {bi("h3", "Sources", "Sources")}
      <ol>{srcs}</ol>
    </div>
  </section>
<!--ck:end-->'''


def main():
    s = PAGE.read_text()
    block = section()
    if '<!--ck:start-->' in s:
        s = re.sub(r'<!--ck:start-->.*?<!--ck:end-->', lambda m: block, s, flags=re.S)
    else:
        k = s.index('<!--cs:end-->') + len('<!--cs:end-->')
        s = s[:k] + '\n\n  ' + block + s[k:]
    nav = s.split('</nav>')[0]
    if 'href="#bouchon"' not in nav:
        k = s.index('    <a href="#tire-bouchon"')
        k = s.index('\n', k) + 1
        s = (s[:k] + '    <a href="#bouchon" data-fr="Le bouchon" data-en="The cork">Le bouchon</a>\n'
             '    <a href="#nouveaux-bouchages" data-fr="Nouveaux bouchages" data-en="New closures">Nouveaux bouchages</a>\n' + s[k:])
    if '<!--ck-css-->' in s:
        s = re.sub(r'/\*<!--ck-css-->\*/.*?/\*<!--ck-css:end-->\*/', lambda m: '/*<!--ck-css-->*/' + CSS + '/*<!--ck-css:end-->*/', s, flags=re.S)
    else:
        k = s.index('</style>')
        s = s[:k] + '/*<!--ck-css-->*/' + CSS + '/*<!--ck-css:end-->*/\n' + s[k:]
    PAGE.write_text(s)
    print(f'{PAGE.name}: #bouchon + #nouveaux-bouchages written ({len(STEPS)} steps, {len(CORKS)} corks, {len(TIMELINE)} dates, {len(NEW)} closures, {len(SOURCES)} sources)')


if __name__ == '__main__':
    main()
