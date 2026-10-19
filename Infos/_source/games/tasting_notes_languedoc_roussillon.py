"""Languedoc & Roussillon batch for « Goûtez votre savoir » (see tasting_notes.py for the field list).
Descriptors and most clues from the CDCs; the Limoux, Banyuls, Maury and Muscat de Rivesaltes rulebooks have no usable
lien section → established facts, flagged in the review sheet.
"""

ZONES_LR = {
    'lang_aude': ('Languedoc · Aude (Corbières, Minervois, Limoux…)', 'Languedoc · Aude (Corbières, Minervois, Limoux…)'),
    'lang_herault': ('Languedoc · Hérault (et appellation régionale)', 'Languedoc · Hérault (and the regional appellation)'),
    'lang_gard': ('Languedoc · Gard & Camargue', 'Languedoc · Gard & Camargue'),
    'rouss_sec': ('Roussillon · vins secs', 'Roussillon · dry wines'),
    'rouss_vdn': ('Roussillon · vins doux naturels', 'Roussillon · vins doux naturels'),
}
_Z = {'lang_aude': ['Corbières', 'Boutenac', 'Fitou', 'Minervois', 'La Livinière', 'Cabardès', 'Malepère', 'Limoux',
                    'Blanquette de Limoux', 'Blanquette méthode ancestrale', 'Crémant de Limoux', 'La Clape',
                    'Muscat de Saint-Jean-de-Minervois'],
      'lang_herault': ['Languedoc', 'Pic Saint-Loup', 'Terrasses du Larzac', 'Faugères', 'Saint-Chinian', 'Picpoul de Pinet',
                       'Clairette du Languedoc', 'Muscat de Frontignan', 'Muscat de Lunel', 'Muscat de Mireval'],
      'lang_gard': ['Costières de Nîmes', 'Clairette de Bellegarde', 'Duché d\'Uzès', 'Sable de Camargue'],
      'rouss_sec': ['Côtes du Roussillon', 'Côtes du Roussillon Villages', 'Collioure'],
      'rouss_vdn': ['Banyuls', 'Banyuls Grand Cru', 'Maury', 'Rivesaltes', 'Muscat de Rivesaltes', 'Grand Roussillon']}
AOC_ZONE_LR = {a: z for z, names in _Z.items() for a in names}

RED = ('Rouge tranquille sec', 'Still dry red')
WHITE = ('Blanc sec', 'Dry white')
GSMC = ('Grenache, syrah, mourvèdre, carignan', 'Grenache, Syrah, Mourvèdre, Carignan')

NOTES_LR = [
    # ------------------------------------------------------------------ Hérault
    dict(id='picpoul-b', aoc='Picpoul de Pinet', alias=['Picpoul', 'Pinet'], zone='lang_herault', col=WHITE, grapes=('Piquepoul blanc', 'Piquepoul Blanc'),
         fr='Robe or pâle aux reflets verts. Tilleul, aubépine, pamplemousse, citron, une pointe minérale. Bouche fine et fraîche avec une '
            '« arête acide » qu’on reconnaît entre tous les blancs de la région. Un seul cépage, sur les bords d’une lagune où l’on élève '
            'huîtres et moules, de part et d’autre d’une voie romaine.',
         en='Pale gold with green tints. Linden, hawthorn, grapefruit, lemon, a mineral hint. Fine, fresh palate with an “acid backbone” '
            'recognisable among all the region’s whites. A single grape, on the shores of a lagoon where oysters and mussels are farmed, '
            'on either side of a Roman road.',
         why=('Piquepoul seul, « arête acide typique », étang de Thau et via Domitia, 600 mm de pluie (cahier des charges).',
              'Piquepoul alone, “typical acid backbone”, the Thau lagoon and the Via Domitia, 600 mm of rain (rulebook).')),
    dict(id='pic-st-loup-r', aoc='Pic Saint-Loup', alias=['Pic St Loup', 'Pic-Saint-Loup'], zone='lang_herault', col=RED,
         grapes=('Syrah, grenache, mourvèdre', 'Syrah, Grenache, Mourvèdre'),
         fr='Robe grenat. Fruits rouges et réglisse, au nez comme en bouche ; garrigue. Bouche élégante, fraîche, tanins fins. Dix-sept communes '
            'au pied d’un sommet calcaire en forme de dent au nord de Montpellier ; le vin ne peut être vendu qu’à partir du 1<sup>er</sup> '
            'septembre suivant la récolte.',
         en='Garnet. Red fruit and liquorice, on the nose and palate; garrigue. Elegant, fresh palate, fine tannins. Seventeen communes below a '
            'tooth-shaped limestone peak north of Montpellier; the wine may only be sold from 1 September after the harvest.',
         why=('17 communes, massif du Pic Saint-Loup, mise en marché « au plus tôt le 1er septembre » (cahier des charges).',
              '17 communes, the Pic Saint-Loup massif, release “no earlier than 1 September” (rulebook).')),
    dict(id='larzac-r', aoc='Terrasses du Larzac', alias=[], zone='lang_herault', col=RED, grapes=('Au moins trois cépages : grenache, syrah, mourvèdre, carignan', 'At least three grapes: Grenache, Syrah, Mourvèdre, Carignan'),
         fr='Robe pourpre à reflets noirs. Fruits noirs, réglisse, olive noire, violette, garrigue ; puis cuir, foin, tabac, truffe. Gras, structure '
            'tannique et une fraîcheur rare dans le Midi, grâce aux nuits froides. Sous les falaises d’un causse à 800 m qui l’abrite du vent du '
            'nord ; certains ne se révèlent qu’après quinze ans.',
         en='Purple with black tints. Black fruit, liquorice, black olive, violet, garrigue; then leather, hay, tobacco, truffle. Rich, tannic '
            'structure and a freshness rare in the south, thanks to cold nights. Below the cliffs of an 800 m causse that shelters it from the '
            'north wind; some only open up after fifteen years.',
         why=('Causse du Larzac à 800 m, « au moins 3 cépages », « olive noire, violette… certains se révélant après plus de 15 ans » (cahier des charges).',
              'The Larzac causse at 800 m, “at least 3 grapes”, “black olive, violet… some revealing themselves after over 15 years” (rulebook).')),
    dict(id='faugeres-r', aoc='Faugères', alias=['Faugeres'], zone='lang_herault', col=RED, grapes=GSMC,
         fr='Robe sombre. Fruits mûrs, épices, finale réglissée. Faible acidité, tanins soyeux avec une légère amertume ; garde de cinq à dix ans. '
            'Un petit massif de schiste de dix kilomètres sur quatre, aux pentes fortes, au nord de Béziers.',
         en='Dark. Ripe fruit, spice, a liquorice finish. Low acidity, silky tannins with a slight bitterness; five to ten years’ ageing. A small '
            'schist massif ten kilometres by four, with steep slopes, north of Béziers.',
         why=('« 10 kilomètres de long… 4 kilomètres de large », « finale réglissée… légère impression d’amertume » (cahier des charges) ; schistes.',
              '“10 kilometres long… 4 kilometres wide”, “liquorice finish… slight bitterness” (rulebook); schist.')),
    dict(id='st-chinian-r', aoc='Saint-Chinian', alias=['Saint Chinian', 'Saint-Chinian Roquebrun', 'Saint-Chinian Berlou'], zone='lang_herault', col=RED,
         grapes=GSMC,
         fr='Robe sombre. Arômes complexes avec une nette note fumée ; faible acidité, belle structure tannique. Il vient du secteur de schistes '
            'de part et d’autre de l’Orb, d’une appellation qui distingue deux types de rouges selon le sol, et dont deux villages, Berlou et '
            'Roquebrun, ont leur propre nom.',
         en='Dark. Complex aromas with a clear smoky note; low acidity, fine tannic structure. It comes from the schist sector on both sides of the '
            'Orb, in an appellation that distinguishes two kinds of red by soil, and whose villages Berlou and Roquebrun have their own names.',
         why=('« Secteur des schistes… notes fumées », dénominations Berlou et Roquebrun (cahier des charges).', '“Schist sector… smoky notes”, Berlou and Roquebrun denominations (rulebook).')),
    dict(id='clairette-lang', aoc='Clairette du Languedoc', alias=['Clairette du Languedoc rancio'], zone='lang_herault', col=('Blanc « rancio »', 'White “rancio”'),
         grapes=('Clairette', 'Clairette'),
         fr='Robe brune, ambrée. Noix fraîche, fruits secs, épices, une note de cire. Bouche sèche, longue, oxydative. Plus de trois ans d’élevage '
            'oxydatif maîtrisé, pour une mention rare et recherchée ; ailleurs, la même appellation fait des blancs secs à l’amertume '
            'caractéristique.',
         en='Brown, amber. Fresh walnut, dried fruit, spice, a wax note. Dry, long, oxidative palate. More than three years of controlled oxidative '
            'ageing, for a rare and sought-after mention; otherwise the same appellation makes dry whites with a characteristic bitterness.',
         why=('Mention « Rancio » : « élevage long de 3 ans au moins… arôme caractéristique de noix fraîche » (cahier des charges).',
              'The “Rancio” mention: “long ageing of at least 3 years… characteristic fresh-walnut aroma” (rulebook).')),
    dict(id='muscat-frontignan', aoc='Muscat de Frontignan', alias=['Frontignan'], zone='lang_herault', col=('Vin doux naturel (blanc)', 'Vin doux naturel (white)'),
         grapes=('Muscat à petits grains (« muscat doré de Frontignan »)', 'Muscat à Petits Grains (“muscat doré de Frontignan”)'),
         fr='Robe or. Fruits exotiques, menthe, citron, puis miel et agrumes confits. Bouche douce et fraîche. Vignes tournées vers la mer sur les '
            'pentes douces d’un petit massif entre les étangs, et une bouteille célèbre pour sa forme torsadée.',
         en='Gold. Exotic fruit, mint, lemon, then honey and candied citrus. Sweet, fresh palate. Vines facing the sea on the gentle slopes of a small '
            'massif between the lagoons, and a bottle famous for its twisted shape.',
         why=('« Muscat doré de Frontignan », « fruits exotiques, menthe, citron », massif de la Gardiole (cahier des charges) ; bouteille torsadée.',
              '“Muscat doré de Frontignan”, “exotic fruit, mint, lemon”, the Gardiole massif (rulebook); twisted bottle.')),
    # ------------------------------------------------------------------ Aude
    dict(id='la-clape-b', aoc='La Clape', alias=['Languedoc La Clape'], zone='lang_aude', col=WHITE, grapes=('Bourboulenc (malvoisie), grenache blanc', 'Bourboulenc (Malvoisie), Grenache Blanc'),
         fr='Robe or pâle. Fleurs, agrumes, une note iodée et saline. Bouche ample et fraîche. Un massif calcaire entre Narbonne et la mer, qui '
            'était une île à l’époque romaine ; le cépage blanc local y est appelé malvoisie.',
         en='Pale gold. Flowers, citrus, an iodine and saline note. Ample, fresh palate. A limestone massif between Narbonne and the sea that was an '
            'island in Roman times; the local white grape is called Malvoisie here.',
         why=('La Clape, ancienne île au large de Narbonne ; le bourboulenc dit « malvoisie » ; AOC depuis 2015.',
              'La Clape, a former island off Narbonne; Bourboulenc known as “Malvoisie”; AOC since 2015.')),
    dict(id='corbieres-r', aoc='Corbières', alias=['Corbieres'], zone='lang_aude', col=RED, grapes=('Carignan, grenache, syrah, mourvèdre', 'Carignan, Grenache, Syrah, Mourvèdre'),
         fr='Robe sombre. Fruits rouges intenses, épices, garrigue. Bouche équilibrée, charpentée, puissante. Un vaste massif à l’extrémité nord-est '
            'des Pyrénées, aux paysages de garrigue dominés par des châteaux cathares ; le carignan y apporte la structure.',
         en='Dark. Intense red fruit, spice, garrigue. Balanced, structured, powerful palate. A vast massif at the north-eastern tip of the Pyrenees, '
            'a garrigue landscape dominated by Cathar castles; Carignan gives the structure.',
         why=('Massif des Corbières, « extrémité nord-orientale des Pyrénées », carignan « contribue à la structure » (cahier des charges).',
              'The Corbières massif, “north-eastern end of the Pyrenees”, Carignan “gives structure” (rulebook).')),
    dict(id='boutenac-r', aoc='Boutenac', alias=['Corbières-Boutenac', 'Corbieres Boutenac'], zone='lang_aude', col=RED,
         grapes=('Carignan, grenache, mourvèdre (au moins 70 %)', 'Carignan, Grenache, Mourvèdre (at least 70 %)'),
         fr='Robe profonde à reflets violets. Fruits mûrs, épices, puis moka et caramel. Bouche puissante, généreuse, tanins enrobés. Un « cru » au '
            'cœur d’un grand massif, autour d’une petite pinède à 273 m entre trois rivières ; élevé au moins jusqu’à la fin de l’année suivante.',
         en='Deep with violet tints. Ripe fruit, spice, then mocha and caramel. Powerful, generous palate, coated tannins. A “cru” in the heart of a '
            'great massif, around a small pine wood at 273 m between three rivers; aged at least until the end of the following year.',
         why=('« Pinada de Boutenac (273 m) », carignan-grenache-mourvèdre ≥ 70 %, « moka, épices et caramel » (cahier des charges).',
              '“Pinada de Boutenac (273 m)”, Carignan-Grenache-Mourvèdre ≥ 70 %, “mocha, spice and caramel” (rulebook).')),
    dict(id='fitou-r', aoc='Fitou', alias=[], zone='lang_aude', col=RED, grapes=('Carignan, grenache, mourvèdre, syrah', 'Carignan, Grenache, Mourvèdre, Syrah'),
         fr='Robe sombre. Fruits rouges et poivre, puis fruits noirs, truffe, grillé, cuir. Bouche riche en tanins, puissante. Une appellation en '
            'deux morceaux séparés par un plateau : l’un au bord des étangs et de la mer, l’autre au pied du mont Tauch ; la plus ancienne AOC '
            'de vin rouge du Languedoc.',
         en='Dark. Red fruit and pepper, then black fruit, truffle, toast, leather. Tannin-rich, powerful palate. An appellation in two pieces '
            'separated by a plateau: one by the lagoons and the sea, the other below Mont Tauch; the oldest red-wine AOC of the Languedoc.',
         why=('« Deux entités distinctes… distantes d’une quinzaine de kilomètres », mont Tauch (cahier des charges) ; AOC dès 1948.',
              '“Two distinct areas… some fifteen kilometres apart”, Mont Tauch (rulebook); AOC since 1948.')),
    dict(id='minervois-r', aoc='Minervois', alias=[], zone='lang_aude', col=RED, grapes=('Grenache, mourvèdre, syrah (au moins 60 %)', 'Grenache, Mourvèdre, Syrah (at least 60 %)'),
         fr='Robe pourpre aux reflets violets. Fruits rouges, épices, réglisse. Bouche chaleureuse et puissante. Un vaste amphithéâtre plein sud, de la '
            'Montagne Noire jusqu’à l’Aude, qui porte le nom d’un village perché, assiégé pendant la croisade contre les cathares.',
         en='Purple with violet tints. Red fruit, spice, liquorice. Warm, powerful palate. A vast south-facing amphitheatre, from the Montagne Noire '
            'down to the Aude, named after a perched village besieged during the crusade against the Cathars.',
         why=('Amphithéâtre adossé à la Montagne Noire (Pic de Nore), « totalement exposé au sud » (cahier des charges) ; Minerve, siège de 1210.',
              'An amphitheatre backing onto the Montagne Noire (Pic de Nore), “entirely south-facing” (rulebook); Minerve, besieged in 1210.')),
    dict(id='liviniere-r', aoc='La Livinière', alias=['Minervois-La Livinière', 'Minervois La Liviniere'], zone='lang_aude', col=RED,
         grapes=('Grenache, mourvèdre, syrah majoritaires', 'Mostly Grenache, Mourvèdre, Syrah'),
         fr='Robe pourpre soutenue aux reflets tuilés. Épices, fruits cuits, vanille ou cacao si élevé en fût. Matière riche et dense, puissante, '
            'chaleureuse, très persistante. Un « cru » sur le « Petit Causse » au pied de la Montagne Noire, au cœur d’une appellation plus vaste.',
         en='Deep purple with brick tints. Spice, cooked fruit, vanilla or cocoa if oak-aged. Rich, dense, powerful, warm, very persistent. A “cru” on '
            'the “Petit Causse” below the Montagne Noire, in the heart of a larger appellation.',
         why=('« Petit Causse », au cœur du Minervois ; « matière riche et dense… chaleureux, très persistants » (cahier des charges).',
              '“Petit Causse”, in the heart of the Minervois; “rich, dense… warm, very persistent” (rulebook).')),
    dict(id='cabardes-r', aoc='Cabardès', alias=['Cabardes'], zone='lang_aude', col=RED,
         grapes=('Cabernets et merlot avec grenache et syrah', 'Cabernets and Merlot with Grenache and Syrah'),
         fr='Robe profonde. Fruits noirs ou confits, réglisse, puis cuir. Tanins ronds. Un balcon incliné au nord de Carcassonne, face aux Pyrénées : '
            'une appellation qui marie à parts égales les cépages de Bordeaux et ceux de la Méditerranée.',
         en='Deep. Black or candied fruit, liquorice, then leather. Round tannins. A sloping balcony north of Carcassonne, facing the Pyrenees: an '
            'appellation that marries Bordeaux and Mediterranean grapes in equal measure.',
         why=('« Assemblage équilibré entre cépages atlantiques et méditerranéens », balcon face aux Pyrénées (cahier des charges).',
              '“A balanced blend of Atlantic and Mediterranean grapes”, a balcony facing the Pyrenees (rulebook).')),
    dict(id='malepere-r', aoc='Malepère', alias=['Malepere'], zone='lang_aude', col=RED, grapes=('Merlot surtout, avec cabernet franc et cot', 'Mostly Merlot, with Cabernet Franc and Cot'),
         fr='Robe rubis vive. Petits fruits rouges, puis fruits noirs, truffe, épices, cuir. Attaque franche et ample, une pointe de vivacité. Un '
            'petit massif à l’ouest de l’Aude, sur la ligne de partage entre versant océanique et versant méditerranéen ; le merlot y est roi.',
         en='Bright ruby. Small red fruit, then black fruit, truffle, spice, leather. Frank, ample attack, a touch of liveliness. A small massif west of '
            'the Aude, on the watershed between the Atlantic and Mediterranean slopes; Merlot is king here.',
         why=('Merlot « cépage principal », limite entre bassin océanique et méditerranéen (cahier des charges).', 'Merlot “main grape”, on the Atlantic/Mediterranean watershed (rulebook).')),
    dict(id='blanquette', aoc='Blanquette de Limoux', alias=['Blanquette'], zone='lang_aude', col=('Blanc effervescent', 'Sparkling white'),
         grapes=('Mauzac surtout', 'Mostly Mauzac'),
         fr='Robe pâle, bulles fines. Pomme verte, poire, une note de fleur et d’herbe. Bouche vive, fruitée. Un cépage local dont la peau se couvre '
            'd’une pruine blanche, autour d’une abbaye où des moines auraient fait mousser du vin dès 1531 — bien avant la Champagne, disent '
            'les Limouxins.',
         en='Pale, fine bubbles. Green apple, pear, a floral and grassy note. Lively, fruity palate. A local grape whose skin is covered with a white '
            'bloom, around an abbey where monks are said to have made sparkling wine as early as 1531 — long before Champagne, as locals say.',
         why=('Mauzac (« blanquette » : la pruine blanche) ; abbaye de Saint-Hilaire, 1531 (tradition).', 'Mauzac (“blanquette”: the white bloom); Saint-Hilaire abbey, 1531 (tradition).')),
    dict(id='cremant-limoux', aoc='Crémant de Limoux', alias=['Cremant de Limoux'], zone='lang_aude', col=('Blanc effervescent', 'Sparkling white'),
         grapes=('Chardonnay, chenin, mauzac, pinot noir — au moins trois', 'Chardonnay, Chenin, Mauzac, Pinot Noir — at least three'),
         fr='Robe or pâle, cordon de bulles fines et persistantes. Fleurs blanches, agrumes, pain grillé. Bouche savoureuse, longue et volumineuse. '
            'Un assemblage d’au moins trois cépages, au pied des Pyrénées audoises — le crémant du Midi.',
         en='Pale gold, a fine, persistent bead. White flowers, citrus, toasted bread. Tasty, long, voluminous palate. A blend of at least three grapes, '
            'at the foot of the Aude Pyrenees — the crémant of the south.',
         why=('« Au moins trois cépages », « fleurs blanches… agrumes et pain grillé » (cahier des charges).', '“At least three grapes”, “white flowers… citrus and toasted bread” (rulebook).')),
    # ------------------------------------------------------------------ Gard & Camargue
    dict(id='costieres-r', aoc='Costières de Nîmes', alias=['Costieres de Nimes'], zone='lang_gard', col=RED, grapes=('Grenache, mourvèdre, syrah', 'Grenache, Mourvèdre, Syrah'),
         fr='Robe intense. Fruits noirs, épices, garrigue, réglisse. Bouche ronde et généreuse. Un plateau de galets roulés long d’une quarantaine '
            'de kilomètres entre une ville aux arènes romaines et la Camargue — un terroir de Rhône rattaché au Languedoc.',
         en='Intense colour. Black fruit, spice, garrigue, liquorice. Round, generous palate. A plateau of rolled pebbles some forty kilometres long '
            'between a city with Roman arenas and the Camargue — Rhône-style terroir attached to the Languedoc.',
         why=('« Costière » : plateau caillouteux de 40 km entre la Vistrenque, le Rhône et la Camargue (cahier des charges).',
              '“Costière”: a 40 km stony plateau between the Vistrenque, the Rhône and the Camargue (rulebook).')),
    dict(id='sable-camargue', aoc='Sable de Camargue', alias=['Sables de Camargue'], zone='lang_gard', col=('Vin gris de gris', 'Gris de gris'),
         grapes=('Grenache gris', 'Grenache Gris'),
         fr='Robe saumonée très pâle. Agrumes, fruits blancs, une note iodée et minérale. Bouche souple, ronde, fraîche, sans tanin. Des vignes '
            'plantées dans le sable du delta — au moins 80 % de sable, sur lequel le phylloxéra ne peut vivre — sur quatorze communes littorales.',
         en='Very pale salmon. Citrus, white fruit, an iodine and mineral note. Supple, round, fresh palate, no tannin. Vines planted in the sand of the '
            'delta — at least 80 % sand, in which phylloxera cannot live — across fourteen coastal communes.',
         why=('Sols sableux « supérieure ou égale à 80 % », « gris de gris… du seul cépage grenache gris », notes iodées (cahier des charges).',
              'Sandy soils “80 % or more”, “gris de gris… from Grenache Gris alone”, iodine notes (rulebook).')),
    dict(id='uzes-r', aoc='Duché d\'Uzès', alias=['Duche d Uzes', 'Duché d’Uzès'], zone='lang_gard', col=RED, grapes=('Syrah et grenache (au moins 60 %)', 'Syrah and Grenache (at least 60 %)'),
         fr='Robe rubis à grenat, intense. Fruits mûrs ou confits, avec une nette note de réglisse. Tanins ronds. Entre Nîmes et Alès, autour '
            'd’une ville qui fut le premier duché de France.',
         en='Ruby to garnet, intense. Ripe or candied fruit, with a clear liquorice note. Round tannins. Between Nîmes and Alès, around a town that was '
            'France’s first duchy.',
         why=('Syrah et grenache ≥ 60 %, « notes de réglisse, reflet de la syrah sur ce terroir », entre Nîmes et Alès (cahier des charges) ; Uzès, « premier duché de France ».',
              'Syrah and Grenache ≥ 60 %, “liquorice notes, the expression of Syrah here”, between Nîmes and Alès (rulebook); Uzès, “first duchy of France”.')),
    # ------------------------------------------------------------------ Roussillon
    dict(id='collioure-r', aoc='Collioure', alias=[], zone='rouss_sec', col=RED, grapes=('Grenache, mourvèdre, syrah, carignan', 'Grenache, Mourvèdre, Syrah, Carignan'),
         fr='Robe colorée. Fruits mûrs, épices. Bouche généreuse, riche, tannique. Le vignoble le plus méridional de France, « entre mer et montagne », '
            'où les Pyrénées plongent dans la Méditerranée ; même aire qu’un célèbre vin doux, mais ici le vin est sec.',
         en='Deep colour. Ripe fruit, spice. Generous, rich, tannic palate. The southernmost vineyard in France, “between sea and mountain”, where the '
            'Pyrenees plunge into the Mediterranean; same area as a famous sweet wine, but here the wine is dry.',
         why=('« Le vignoble le plus méridional de France… mar i mont » (cahier des charges) ; même aire que Banyuls.',
              '“The southernmost vineyard in France… mar i mont” (rulebook); same area as Banyuls.')),
    dict(id='cdr-villages-caramany', aoc='Côtes du Roussillon Villages', alias=['Côtes du Roussillon Villages Caramany', 'Caramany', 'Cotes du Roussillon Villages'],
         zone='rouss_sec', col=RED, grapes=('Carignan, grenache, syrah', 'Carignan, Grenache, Syrah'),
         fr='Robe rouge. Fruits rouges croquants, épices. Bouche souple, fraîche, gourmande. Ici, au nord de la Têt, le carignan doit obligatoirement '
            'être vinifié en macération carbonique — une règle unique pour l’une des dénominations de cette appellation de villages.',
         en='Red. Crunchy red fruit, spice. Supple, fresh, tempting palate. Here, north of the Têt, Carignan must be made by carbonic maceration — a '
            'unique rule for one of the denominations of this village appellation.',
         why=('Dénomination Caramany : « macération carbonique imposée pour le cépage carignan » (cahier des charges).', 'The Caramany denomination: “carbonic maceration required for Carignan” (rulebook).')),
    dict(id='cdroussillon-r', aoc='Côtes du Roussillon', alias=['Cotes du Roussillon'], zone='rouss_sec', col=RED, grapes=GSMC,
         fr='Robe sombre. Fruits noirs, épices, garrigue. Trame tannique, charpente, mais un vin velouté, souvent reconnaissable à sa fraîcheur et sa '
            'minéralité. Un amphithéâtre ouvert sur la mer, fermé par le Canigou, les Albères et les Corbières, traversé par trois fleuves.',
         en='Dark. Black fruit, spice, garrigue. Tannic frame, structure, yet velvety, often recognisable by its freshness and minerality. An '
            'amphitheatre open to the sea, closed by the Canigou, the Albères and the Corbières, crossed by three rivers.',
         why=('Amphithéâtre Canigou (2 780 m) – Albères – Corbières, « veloutés… fraîcheur et minéralité » (cahier des charges).',
              'The Canigou (2,780 m) – Albères – Corbières amphitheatre, “velvety… freshness and minerality” (rulebook).')),
    dict(id='banyuls-trad', aoc='Banyuls', alias=['Banyuls traditionnel', 'Banyuls rancio'], zone='rouss_vdn', col=('Vin doux naturel (rouge, oxydatif)', 'Vin doux naturel (red, oxidative)'),
         grapes=('Grenache noir surtout', 'Mostly Grenache Noir'),
         fr='Robe tuilée. Pruneau, figue sèche, cacao, café, noix, une note de rancio. Bouche douce, ample, longue. Un vin muté élevé longtemps au '
            'contact de l’air, parfois en bonbonnes de verre laissées au soleil, sur les terrasses de schiste qui dévalent vers la mer à la frontière '
            'espagnole.',
         en='Brick-coloured. Prune, dried fig, cocoa, coffee, walnut, a rancio note. Sweet, ample, long palate. A fortified wine aged for a long time in '
            'contact with air, sometimes in glass demijohns left in the sun, on schist terraces tumbling down to the sea at the Spanish border.',
         why=('Banyuls traditionnel : élevage oxydatif, dames-jeannes au soleil (voir la page Formats de bouteilles) ; terrasses de schiste de la Côte Vermeille.',
              'Traditional Banyuls: oxidative ageing, demijohns in the sun (see the Bottle sizes page); schist terraces of the Côte Vermeille.')),
    dict(id='maury-vdn', aoc='Maury', alias=['Maury grenat'], zone='rouss_vdn', col=('Vin doux naturel (grenat)', 'Vin doux naturel (grenat)'),
         grapes=('Grenache noir', 'Grenache Noir'),
         fr='Robe grenat profond. Cerise noire, mûre, kirsch, cacao. Bouche douce et fruitée, tanins présents. Un vin muté jeune, sans oxydation, d’une '
            'vallée encaissée de schistes noirs au nord du Roussillon, dominée par les ruines d’un château cathare.',
         en='Deep garnet. Black cherry, blackberry, kirsch, cocoa. Sweet, fruity palate, present tannins. A young fortified wine, protected from '
            'oxidation, from a steep valley of black schist in the north of the Roussillon, overlooked by the ruins of a Cathar castle.',
         why=('Maury grenat (VDN de grenache noir) ; schistes noirs de Maury, château de Quéribus.', 'Maury grenat (a Grenache Noir VDN); the black schists of Maury, Quéribus castle.')),
    dict(id='rivesaltes-ambre', aoc='Rivesaltes', alias=['Rivesaltes ambré'], zone='rouss_vdn', col=('Vin doux naturel (ambré)', 'Vin doux naturel (amber)'),
         grapes=('Grenache blanc et gris, macabeu', 'Grenache Blanc and Gris, Macabeu'),
         fr='Robe ambrée. Orange confite, abricot sec, amande, noix, miel. Bouche douce et longue. Raisins d’au moins 252 g de sucre par litre, mutage '
            'à l’alcool neutre pour atteindre 15 % ; la plus vaste appellation de vin doux naturel de France.',
         en='Amber. Candied orange, dried apricot, almond, walnut, honey. Sweet, long palate. Grapes of at least 252 g of sugar per litre, fortified '
            'with neutral spirit to reach 15 %; France’s largest vin doux naturel appellation.',
         why=('« 252 grammes par litre… 15 % après mutage » (cahier des charges) ; mention « ambré » (élevage oxydatif).',
              '“252 grams per litre… 15 % after fortification” (rulebook); the “ambré” mention (oxidative ageing).')),
    dict(id='muscat-rivesaltes', aoc='Muscat de Rivesaltes', alias=[], zone='rouss_vdn', col=('Vin doux naturel (blanc)', 'Vin doux naturel (white)'),
         grapes=('Muscat à petits grains et muscat d’Alexandrie', 'Muscat à Petits Grains and Muscat of Alexandria'),
         fr='Robe or pâle. Raisin frais, agrumes, menthe, fleurs, fruits exotiques. Bouche douce, fraîche, à boire jeune. Le seul muscat français '
            'qui assemble deux variétés de muscat, l’une à petits grains, l’autre venue d’Égypte, à en croire son nom.',
         en='Pale gold. Fresh grape, citrus, mint, flowers, exotic fruit. Sweet, fresh palate, to drink young. The only French Muscat that blends two '
            'Muscat varieties, one small-berried, the other said by its name to come from Egypt.',
         why=('Muscat à petits grains + muscat d’Alexandrie (fiche cépages du site).', 'Muscat à Petits Grains + Muscat of Alexandria (the site’s grape card).')),
]
