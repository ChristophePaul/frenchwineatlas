#!/usr/bin/env python3
"""Build Infos/Vine_and_Vineyard/Vine_Plant.html (chapter 1 — the vine plant).
Run:  python3 "WEB Site/Infos/Vine_and_Vineyard/_source/build_plant.py"
Text of the main sections lives in plant_template.html; fold-out panels, glossary and sources below.
"""
from common import HERE, t, base_css, plate, pro_panel, chapter_nav, PRO_ICON
import svg_ch1

OUT = HERE.parent / 'Vine_Plant.html'
IMG = 'img/botany/'

PRO_FAMILY = [
  (('Domestication', 'Domestication'),
   ('Une étude génomique de 2023 (Dong et al., <i>Science</i>) situe deux domestications simultanées il y a environ 11 000 ans, au Proche-Orient et dans le Caucase. La vigne sauvage <i>sylvestris</i> est dioïque (pieds mâles et femelles) ; la domestication a sélectionné des fleurs hermaphrodites, capables de s’autoféconder.',
    'A 2023 genomic study (Dong et al., <i>Science</i>) points to two simultaneous domestications about 11,000 years ago, in the Near East and the Caucasus. The wild <i>sylvestris</i> vine is dioecious (separate male and female plants); domestication selected hermaphrodite flowers able to self-pollinate.')),
  (('Génome', 'Genome'),
   ('Premier génome d’une plante fruitière séquencé, en 2007, par un consortium franco-italien, sur une lignée de Pinot noir presque homozygote (PN40024). 19 paires de chromosomes.',
    'The first fruit-crop genome to be sequenced, in 2007, by a French-Italian consortium, from a near-homozygous Pinot Noir line (PN40024). 19 pairs of chromosomes.')),
  (('Multiplication', 'Propagation'),
   ('Un cépage est un clone multiplié par bouture ou greffage : chaque pied de Chardonnay est génétiquement (presque) identique. Semer un pépin donne une plante nouvelle, différente de ses parents, d’où la création variétale par croisement.',
    'A grape variety is a clone propagated by cuttings or grafting: every Chardonnay vine is genetically (almost) identical. Planting a seed produces a new plant unlike its parents, which is how new varieties are bred by crossing.')),
  (('Parentés', 'Parentage'),
   ('Les analyses ADN ont révélé de grandes familles : le Gouais blanc et le Pinot sont les parents du Chardonnay, du Gamay, de l’Aligoté et du Melon ; le Cabernet Sauvignon est issu d’un croisement naturel entre Cabernet franc et Sauvignon blanc.',
    'DNA profiling has revealed large families: Gouais Blanc and Pinot are the parents of Chardonnay, Gamay, Aligoté and Melon; Cabernet Sauvignon comes from a natural cross between Cabernet Franc and Sauvignon Blanc.')),
]

PRO_VINE = [
  (('Organisation du rameau', 'Shoot structure'),
   ('Le rameau alterne nœuds et entre-nœuds. À chaque nœud : une feuille, un bourgeon latent à son aisselle et un bourgeon anticipé ; à l’opposé de la feuille, une vrille ou une inflorescence (ce sont des organes homologues). Chez <i>V. vinifera</i>, les vrilles sont discontinues : deux nœuds en portent, le troisième non.',
    'The shoot alternates nodes and internodes. At each node: a leaf, a latent bud in its axil and a prompt bud; opposite the leaf, a tendril or an inflorescence (they are homologous organs). In <i>V. vinifera</i> tendrils are discontinuous: two nodes carry one, the third does not.')),
  (('Réserves', 'Reserves'),
   ('L’amidon stocké dans les racines, le tronc et les bras alimente le débourrement et les premières semaines de pousse, avant que les feuilles ne deviennent exportatrices. Une vigne épuisée une année (surcharge, défoliation précoce) débourre mal l’année suivante.',
    'Starch stored in roots, trunk and arms fuels budburst and the first weeks of growth, before leaves become net exporters. A vine exhausted one year (overcropping, early defoliation) bursts poorly the next.')),
  (('Fertilité', 'Fruitfulness'),
   ('Chez la plupart des cépages, les yeux de la base du sarment sont moins fertiles que ceux du milieu : c’est pourquoi on taille long (Guyot) les cépages peu fertiles à la base, et court (cordon, coursons) les autres. Les « gourmands » nés du vieux bois sont en général stériles.',
    'In most varieties the buds at the base of the cane are less fruitful than those in the middle: hence long pruning (Guyot) for varieties with poor basal fruitfulness and short pruning (cordon, spurs) for the others. Water shoots growing from old wood are usually sterile.')),
  (('Longévité', 'Lifespan'),
   ('Un cep peut vivre plus de cent ans, mais la plupart sont remplacés entre 30 et 50 ans, quand les maladies du bois et la baisse de rendement s’installent. La mention « vieilles vignes » n’a pas de définition légale en France.',
    'A vine can live over a hundred years, but most are replaced at 30–50 years old, when trunk diseases and falling yields set in. “Vieilles vignes” (old vines) has no legal definition in France.')),
]

PRO_BUD = [
  (('Vocabulaire', 'Terms'),
   ('Bourgeon latent (œil) : complexe de trois bourgeons, dormant en hiver. Bourgeon anticipé : se développe l’année même et donne un entre-cœur (rameau secondaire). Bourillons et yeux de la couronne : à la base du sarment, peu fertiles. Bourgeons du vieux bois : peuvent dormir des années et donner des gourmands.',
    'Latent bud (“eye”): a complex of three buds, dormant over winter. Prompt bud: develops the same year into a lateral shoot. Base buds (“crown” buds): at the bottom of the cane, poorly fruitful. Old-wood buds: can stay dormant for years and produce water shoots.')),
  (('Initiation florale', 'Floral initiation'),
   ('Les ébauches d’inflorescences se forment dans le bourgeon principal autour de la floraison de l’année N−1, favorisées par la lumière et la chaleur sur les bourgeons. Leur différenciation en fleurs se termine au printemps de l’année N, juste avant le débourrement.',
    'Inflorescence primordia form in the primary bud around flowering in year N−1, favoured by light and warmth on the buds. Their differentiation into flowers is completed in spring of year N, just before budburst.')),
  (('Gel et bourgeons', 'Frost and buds'),
   ('Un œil dormant résiste à des températures très basses en hiver (souvent −15 à −20 °C pour <i>vinifera</i>), mais le bourgeon gonflé puis débourré ne supporte que −2 à −3 °C, et la jeune pousse à peine −1 °C.',
    'A dormant bud withstands very low winter temperatures (often −15 to −20 °C for <i>vinifera</i>), but once swollen and burst it tolerates only −2 to −3 °C, and the young shoot barely −1 °C.')),
  (('Compter les yeux', 'Counting buds'),
   ('La charge (nombre d’yeux laissés par pied ou par m²) est la première façon de régler le rendement ; de nombreux cahiers des charges d’AOC fixent un nombre maximal d’yeux par pied.',
    'Bud load (buds left per vine or per m²) is the first lever on yield; many AOC specifications set a maximum number of buds per vine.')),
]

PRO_LEAF = [
  (('Surface foliaire', 'Leaf area'),
   ('Il faut environ 0,8 à 1,2 m² de feuilles bien exposées pour mûrir 1 kg de raisin (Kliewer & Dokoozlian, 2005). C’est l’indicateur clé de l’équilibre feuilles/fruits, que l’on règle par la hauteur de rognage et la charge.',
    'About 0.8–1.2 m² of well-exposed leaf area is needed to ripen 1 kg of grapes (Kliewer & Dokoozlian, 2005). It is the key measure of leaf-to-fruit balance, adjusted through trimming height and crop load.')),
  (('Photosynthèse', 'Photosynthesis'),
   ('Optimum vers 25–30 °C ; elle chute au-delà de 35 °C et lorsque la contrainte hydrique ferme les stomates. Les stomates, de l’ordre de 100 à 200 par mm², sont presque tous à la face inférieure.',
    'Optimum around 25–30 °C; it drops above 35 °C and when water stress closes the stomata. Stomata, roughly 100–200 per mm², are almost all on the underside.')),
  (('Ampélographie', 'Ampelography'),
   ('Science de la description des cépages, refondée en France par Pierre Galet (1921–2019) : mesure des angles entre nervures, profondeur des sinus, forme du sinus pétiolaire, type et densité des poils (couchés ou dressés). La liste des descripteurs de l’OIV en codifie aujourd’hui les caractères ; l’ADN a pris le relais pour les identifications délicates.',
    'The science of describing grape varieties, rebuilt in France by Pierre Galet (1921–2019): angles between veins, sinus depth, shape of the petiolar sinus, type and density of hairs (prostrate or erect). The OIV descriptor list now codifies these traits; DNA has taken over for difficult identifications.')),
  (('Couleurs d’automne', 'Autumn colours'),
   ('Le rougissement de cépages blancs, ou un rougissement précoce en été entre des nervures restées vertes, peut signaler une virose (enroulement) ou une maladie (flavescence dorée, esca) : voir le chapitre 7.',
    'Reddening of white varieties, or early summer reddening between veins that stay green, can signal a virus (leafroll) or a disease (flavescence dorée, esca): see chapter 7.')),
]

PRO_FLOWER = [
  (('Structure', 'Structure'),
   ('Fleur pentamère : 5 sépales réduits, 5 pétales soudés en capuchon qui se détache par la base, 5 étamines, un ovaire à 2 carpelles contenant chacun 2 ovules, d’où au plus 4 pépins par baie.',
    'Five-part flower: 5 reduced sepals, 5 petals fused into a cap that detaches from the base, 5 stamens, an ovary of 2 carpels with 2 ovules each, hence at most 4 seeds per berry.')),
  (('Conditions', 'Conditions'),
   ('La floraison demande au moins 15 °C, idéalement 20–25 °C, et un temps sec. Stades repères : BBCH 65 (pleine floraison, 50 % des capuchons tombés), BBCH 71 (nouaison).',
    'Flowering needs at least 15 °C, ideally 20–25 °C, and dry weather. Reference stages: BBCH 65 (full bloom, 50 % of caps fallen), BBCH 71 (fruit set).')),
  (('Coulure et millerandage', 'Coulure and millerandage'),
   ('Coulure : chute des fleurs ou jeunes baies non fécondées (froid, pluie, carences, déséquilibre de vigueur) ; Grenache, Merlot et Côt y sont sensibles. Millerandage : baies petites et souvent sans pépins mêlées aux normales ; fréquent sur Chardonnay. Un millerandage modéré concentre parfois la qualité.',
    'Coulure: shedding of unfertilised flowers or young berries (cold, rain, deficiencies, vigour imbalance); Grenache, Merlot and Malbec are prone to it. Millerandage: small, often seedless berries mixed with normal ones; common in Chardonnay. Moderate millerandage can sometimes concentrate quality.')),
  (('Poids de grappe', 'Bunch weight'),
   ('De moins de 100 g (Pinot noir) à plus de 300 g (Grenache, Carignan). La rafle représente environ 3 à 6 % du poids de la grappe ; elle est conservée dans les vinifications en « vendange entière ».',
    'From under 100 g (Pinot Noir) to over 300 g (Grenache, Carignan). The stalk accounts for about 3–6 % of bunch weight; it is kept in whole-bunch fermentations.')),
]

PRO_BERRY = [
  (('Maturation', 'Ripening'),
   ('À la véraison, la baie change de couleur et s’assouplit ; les sucres arrivent alors par le phloème et s’accumulent. L’acide malique est respiré, d’autant plus vite qu’il fait chaud ; l’acide tartrique reste à peu près stable. La teneur en sucres atteint souvent 180 à 250 g/L à maturité.',
    'At véraison the berry changes colour and softens; sugars then arrive through the phloem and accumulate. Malic acid is respired, faster in hot weather; tartaric acid stays roughly stable. Sugar content often reaches 180–250 g/L at ripeness.')),
  (('Du sucre à l’alcool', 'From sugar to alcohol'),
   ('Il faut environ 16,8 à 17 g/L de sucres pour 1 % vol. d’alcool. Mesures courantes : réfractomètre (°Brix), degré Baumé, densité (°Oechsle).',
    'About 16.8–17 g/L of sugar make 1 % alcohol by volume. Common measures: refractometer (°Brix), Baumé degrees, density (°Oechsle).')),
  (('Taille des baies', 'Berry size'),
   ('Plus une baie est petite, plus la part de peau par rapport au jus est élevée : davantage de couleur, de tanins et d’arômes. C’est pourquoi les raisins de cuve (1 à 2 g) sont bien plus petits que les raisins de table (5 à 10 g).',
    'The smaller the berry, the higher the ratio of skin to juice: more colour, tannin and aroma. That is why wine grapes (1–2 g) are much smaller than table grapes (5–10 g).')),
  (('Maturité phénolique', 'Phenolic ripeness'),
   ('Au-delà du sucre, on suit la couleur et l’extractibilité des anthocyanes, la maturité des tanins et le brunissement des pépins (qui passent du vert au brun et deviennent croquants).',
    'Beyond sugar, growers track anthocyanin colour and extractability, tannin ripeness and seed browning (from green to brown and crunchy).')),
  (('Teinturiers', 'Teinturiers'),
   ('Rares cépages à pulpe colorée : Alicante Henri Bouschet, Grand noir de la Calmette, Gamay de Bouze et autres Gamays teinturiers.',
    'Rare varieties with coloured flesh: Alicante Henri Bouschet, Grand Noir de la Calmette, Gamay de Bouze and other teinturier Gamays.')),
]

GLOSSARY = [  # (fr, en, def_fr, def_en)
  ('Aoûtement', 'Lignification (cane ripening)', 'Transformation du rameau vert en bois, en fin d’été.', 'The green shoot turning into wood in late summer.'),
  ('Baguette', 'Cane (fruiting cane)', 'Sarment taillé long, porteur de la récolte.', 'Cane left long to carry the crop.'),
  ('Baie', 'Berry', 'Le grain de raisin.', 'An individual grape.'),
  ('Bourgeon, œil', 'Bud', 'Organe en dormance qui donnera un rameau.', 'Dormant organ that will grow into a shoot.'),
  ('Bourre', 'Bud wool', 'Duvet qui protège le bourgeon en hiver.', 'Hairs protecting the bud in winter.'),
  ('Bras', 'Arm', 'Ramification permanente du tronc.', 'Permanent branch of the trunk.'),
  ('Capuchon', 'Calyptra (cap)', 'Pétales soudés qui tombent à la floraison.', 'Fused petals shed at flowering.'),
  ('Cep', 'Vine (vinestock)', 'Le pied de vigne entier.', 'The whole vine plant.'),
  ('Coulure', 'Coulure (poor fruit set)', 'Chute des fleurs ou jeunes baies.', 'Shedding of flowers or young berries.'),
  ('Courson', 'Spur', 'Sarment taillé court (1–2 yeux).', 'Cane cut short (1–2 buds).'),
  ('Débourrement', 'Budburst', 'Ouverture des bourgeons au printemps.', 'Buds opening in spring.'),
  ('Entre-cœur', 'Lateral shoot', 'Rameau secondaire né d’un bourgeon anticipé.', 'Secondary shoot from a prompt bud.'),
  ('Entre-nœud', 'Internode', 'Portion de rameau entre deux nœuds.', 'Section of shoot between two nodes.'),
  ('Gourmand', 'Water shoot', 'Rameau né sur le vieux bois.', 'Shoot growing from old wood.'),
  ('Greffon', 'Scion', 'Partie greffée, le cépage.', 'The grafted part: the variety.'),
  ('Limbe', 'Leaf blade', 'Partie plane de la feuille.', 'The flat part of the leaf.'),
  ('Millerandage', 'Millerandage (hens and chicks)', 'Mélange de petites et grosses baies.', 'Mix of small and normal berries.'),
  ('Nœud', 'Node', 'Point du rameau où naissent feuille et bourgeon.', 'Point on the shoot bearing a leaf and bud.'),
  ('Nouaison', 'Fruit set', 'Passage de la fleur à la jeune baie.', 'Flower turning into a young berry.'),
  ('Pédicelle', 'Pedicel', 'Petite queue de chaque baie.', 'The tiny stalk of each berry.'),
  ('Pédoncule', 'Peduncle', 'Queue de la grappe, attachée au rameau.', 'Bunch stalk, attached to the shoot.'),
  ('Pellicule', 'Skin', 'Peau de la baie.', 'The berry’s skin.'),
  ('Pépin', 'Seed (pip)', 'Graine de la baie, 0 à 4.', 'The berry’s seed, 0 to 4.'),
  ('Pétiole', 'Petiole', 'Queue de la feuille.', 'Leaf stalk.'),
  ('Porte-greffe', 'Rootstock', 'Pied américain résistant au phylloxéra.', 'Phylloxera-resistant American base.'),
  ('Pruine', 'Bloom', 'Cire poudreuse sur la pellicule.', 'Powdery wax on the skin.'),
  ('Rafle', 'Stalk, rachis', 'Charpente ramifiée de la grappe.', 'Branched framework of the bunch.'),
  ('Rameau', 'Shoot', 'Pousse verte de l’année.', 'The season’s green growth.'),
  ('Sarment', 'Cane', 'Rameau aoûté, bois d’un an.', 'Ripened shoot, one-year-old wood.'),
  ('Sinus pétiolaire', 'Petiolar sinus', 'Échancrure où s’attache le pétiole.', 'Notch where the petiole joins.'),
  ('Véraison', 'Véraison', 'Changement de couleur et ramollissement de la baie.', 'Berry colour change and softening.'),
  ('Vrille', 'Tendril', 'Organe qui s’enroule pour accrocher la plante.', 'Coiling organ the plant climbs with.'),
]

SOURCES = [
  ('Galet P., <i>Dictionnaire encyclopédique des cépages et de leurs synonymes</i>, Libre & Solidaire, 2015.', 'Galet P., <i>Dictionnaire encyclopédique des cépages et de leurs synonymes</i>, Libre & Solidaire, 2015.'),
  ('Reynier A., <i>Manuel de viticulture</i>, Lavoisier Tec & Doc, 12<sup>e</sup> éd.', 'Reynier A., <i>Manuel de viticulture</i>, Lavoisier Tec & Doc, 12th ed.'),
  ('Robinson J., Harding J., Vouillamoz J., <i>Wine Grapes</i>, Allen Lane, 2012.', 'Robinson J., Harding J., Vouillamoz J., <i>Wine Grapes</i>, Allen Lane, 2012.'),
  ('Jaillon O. et al., « The grapevine genome sequence… », <i>Nature</i> 449, 2007 ; Dong Y. et al., « Dual domestications and origin of traits in grapevine evolution », <i>Science</i> 379, 2023.', 'Jaillon O. et al., “The grapevine genome sequence…”, <i>Nature</i> 449, 2007; Dong Y. et al., “Dual domestications and origin of traits in grapevine evolution”, <i>Science</i> 379, 2023.'),
  ('Kliewer W. M., Dokoozlian N. K., « Leaf area/crop weight ratios of grapevines », <i>AJEV</i> 56, 2005.', 'Kliewer W. M., Dokoozlian N. K., “Leaf area/crop weight ratios of grapevines”, <i>AJEV</i> 56, 2005.'),
  ('OIV, liste des descripteurs des variétés et espèces de <i>Vitis</i> ; IFV, fiches techniques.', 'OIV descriptor list for grape varieties and <i>Vitis</i> species; IFV technical sheets.'),
]


def glossary():
    return ''.join(f'<tr><td>{fr}</td><td>{en}</td><td>{t((dfr, den))}</td></tr>' for fr, en, dfr, den in GLOSSARY)


def main():
    tpl = (HERE / 'plant_template.html').read_text()
    rep = {
        '@@BASE_CSS@@': base_css(),
        '@@PRO_ICON@@': PRO_ICON,
        '@@PLATE_VINE@@': plate(IMG + 'vine_guyot.webp', 'Cep de vigne taillé en Guyot / Guyot-trained vine', 1122, 1387),
        '@@PLATE_LEAF_UPPER@@': plate(IMG + 'leaf_upper.webp', 'Feuille de vigne, face supérieure / Vine leaf, upper side', 1254, 1254, 'face-upper'),
        '@@PLATE_LEAF_UNDER@@': plate(IMG + 'leaf_under.webp', 'Feuille de vigne, face inférieure / Vine leaf, underside', 1254, 1254, 'face-under'),
        '@@PLATE_BERRY@@': plate(IMG + 'berry_section.webp', 'Coupe d’une baie de raisin / Cross-section of a grape berry', 1254, 1254, 'photo'),
        '@@PLATE_TRAINING@@': plate(IMG + 'training_systems.webp', 'Modes de conduite de la vigne / Vine training systems', 1122, 1402),
        '@@PLATE_BUD@@': plate(IMG + 'bud_section.webp', 'Coupe d’un bourgeon de vigne / Section of a grapevine bud', 1087, 1363),
        '@@PLATE_FLOWER@@': plate(IMG + 'flower_stages.webp', 'Fleur de vigne / Grapevine flower', 1290, 721),
        '@@PLATE_BUNCH@@': plate(IMG + 'bunch_anatomy.webp', 'Grappe de raisin / Grape bunch', 1449, 980),
        '@@PRO_FAMILY@@': pro_panel(PRO_FAMILY),
        '@@PRO_VINE@@': pro_panel(PRO_VINE),
        '@@PRO_BUD@@': pro_panel(PRO_BUD),
        '@@PRO_LEAF@@': pro_panel(PRO_LEAF),
        '@@PRO_FLOWER@@': pro_panel(PRO_FLOWER),
        '@@PRO_BERRY@@': pro_panel(PRO_BERRY),
        '@@GLOSSARY@@': glossary(),
        '@@CHAPTERS@@': chapter_nav(1),
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
