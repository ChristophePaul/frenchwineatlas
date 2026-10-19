"""Loire batch for « Goûtez votre savoir » (see tasting_notes.py for the field list).

Most Loire rulebooks have a filled-in « lien à l'origine »: descriptors and many clues come from it.
Facts from outside the CDC are flagged in the review sheet.
"""

ZONES_LOI = {
    'nantais': ('Val de Loire · Pays nantais & Vendée', 'Loire Valley · Pays Nantais & Vendée'),
    'anjou': ('Val de Loire · Anjou & Saumur', 'Loire Valley · Anjou & Saumur'),
    'touraine': ('Val de Loire · Touraine, Blésois & Loir', 'Loire Valley · Touraine, Blois & the Loir'),
    'centre': ('Val de Loire · Centre-Loire (Sancerrois, Berry, Orléanais)', 'Loire Valley · Centre-Loire (Sancerre, Berry, Orléans)'),
    'auvergne': ('Val de Loire · Auvergne & haute Loire', 'Loire Valley · Auvergne & upper Loire'),
}
_Z = {'nantais': ['Muscadet', 'Muscadet Sèvre et Maine', 'Muscadet Côtes de Grandlieu', 'Muscadet Coteaux de la Loire',
                  'Gros Plant du Pays Nantais', 'Coteaux d\'Ancenis', 'Fiefs Vendéens', 'Haut-Poitou'],
      'anjou': ['Anjou', 'Cabernet d\'Anjou', 'Rosé d\'Anjou', 'Anjou Villages', 'Anjou Brissac', 'Anjou Coteaux de la Loire',
                'Savennières', 'Coulée de Serrant', 'Savennières Roche aux Moines', 'Coteaux du Layon', 'Quarts de Chaume',
                'Bonnezeaux', 'Coteaux de l\'Aubance', 'Saumur', 'Saumur-Champigny', 'Coteaux de Saumur', 'Crémant de Loire', 'Rosé de Loire'],
      'touraine': ['Touraine', 'Touraine Noble Joué', 'Chinon', 'Bourgueil', 'Saint-Nicolas-de-Bourgueil', 'Vouvray', 'Montlouis-sur-Loire',
                   'Jasnières', 'Coteaux du Loir', 'Coteaux du Vendômois', 'Cheverny', 'Cour-Cheverny', 'Valençay'],
      'centre': ['Sancerre', 'Pouilly-Fumé', 'Pouilly-sur-Loire', 'Menetou-Salon', 'Quincy', 'Reuilly', 'Coteaux du Giennois',
                 'Orléans', 'Orléans-Cléry', 'Châteaumeillant'],
      'auvergne': ['Saint-Pourçain', 'Côtes d\'Auvergne', 'Côtes du Forez', 'Côte Roannaise']}
AOC_ZONE_LOI = {a: z for z, names in _Z.items() for a in names}

RED = ('Rouge tranquille sec', 'Still dry red')
WHITE = ('Blanc sec', 'Dry white')
CF = ('Cabernet franc', 'Cabernet Franc')
CHE = ('Chenin', 'Chenin Blanc')
SAU = ('Sauvignon', 'Sauvignon Blanc')
SWEET = ('Blanc liquoreux', 'Sweet white (liquoreux)')

NOTES_LOI = [
    # ------------------------------------------------------------------ Nantais
    dict(id='muscadet-sm-b', aoc='Muscadet Sèvre et Maine', alias=['Muscadet Sevre et Maine', 'Muscadet Sèvre-et-Maine sur lie', 'Muscadet'],
         zone='nantais', col=WHITE, grapes=('Melon de Bourgogne', 'Melon de Bourgogne'),
         fr='Robe très pâle aux reflets verts. Citron, pomme verte, fleurs blanches et une note iodée. Bouche fraîche, légère, avec un '
            'imperceptible perlant : le vin est resté tout l’hiver sur ses lies avant d’être mis en bouteille directement. '
            'Coteaux à l’est de Nantes, sur les versants de deux rivières dont il porte le nom.',
         en='Very pale with green tints. Lemon, green apple, white flowers and an iodine note. Fresh, light palate with a barely '
            'perceptible prickle: the wine spent the winter on its lees before being bottled straight off them. Slopes east of Nantes, '
            'along two rivers whose names it bears.',
         why=('« Sur lie », « léger perlant dû au gaz carbonique résiduel », versants de la Sèvre et de la Maine (cahier des charges).',
              '“Sur lie”, “a slight prickle from residual CO2”, slopes of the Sèvre and the Maine (rulebook).')),
    dict(id='gros-plant-b', aoc='Gros Plant du Pays Nantais', alias=['Gros Plant', 'Gros-Plant'], zone='nantais', col=WHITE,
         grapes=('Folle blanche', 'Folle Blanche'),
         fr='Robe jaune très pâle. Arômes discrets d’agrumes et de fleurs, et une senteur iodée. Bouche acidulée, vive, légère : '
            'le compagnon tranchant des huîtres. Autour d’un grand lac au sud de Nantes, d’un cépage que les Charentais distillaient '
            'autrefois.',
         en='Very pale yellow. Discreet citrus and floral aromas, and an iodine scent. Tart, lively, light palate: the sharp companion '
            'to oysters. Around a large lake south of Nantes, from a grape the Charente once distilled.',
         why=('Folle blanche (« gros plant » en pays nantais), « équilibre acidulé… senteur iodée », autour du lac de Grandlieu (cahier des charges).',
              'Folle Blanche (“gros plant” locally), “tart balance… iodine scent”, around Lake Grandlieu (rulebook).')),
    dict(id='fiefs-r', aoc='Fiefs Vendéens', alias=['Fiefs Vendeens'], zone='nantais', col=RED,
         grapes=('Pinot noir, cabernets, gamay, négrette…', 'Pinot Noir, the Cabernets, Gamay, Négrette…'),
         fr='Robe rubis à grenat. Fruits puissants, épices douces, cuir ou réglisse. Bouche ronde et fine. Un vignoble entre bocage et '
            'plaine, qui s’étire depuis la côte atlantique des Sables-d’Olonne jusqu’à Fontenay-le-Comte, en cinq dénominations '
            'dont Brem, Mareuil et Pissotte.',
         en='Ruby to garnet. Powerful fruit, sweet spice, leather or liquorice. Round, fine palate. A vineyard between bocage and plain, '
            'stretching from the Atlantic coast at Les Sables-d’Olonne to Fontenay-le-Comte, in five denominations including Brem, '
            'Mareuil and Pissotte.',
         why=('Des Sables-d’Olonne à Fontenay-le-Comte ; dénominations Brem, Mareuil, Pissotte, Vix, Chantonnay (cahier des charges).',
              'From Les Sables-d’Olonne to Fontenay-le-Comte; denominations Brem, Mareuil, Pissotte, Vix, Chantonnay (rulebook).')),
    # ------------------------------------------------------------------ Anjou & Saumur
    dict(id='savennieres-b', aoc='Savennières', alias=['Savennieres'], zone='anjou', col=WHITE, grapes=CHE,
         fr='Robe jaune pâle à doré. Acacia, tilleul, poire, coing, amande grillée, miel, une touche minérale. Attaque ample et grasse, '
            'finale fraîche marquée d’une pointe d’amertume ; il ne s’épanouit qu’après plusieurs années. Coteaux de schiste de la rive '
            'droite, près d’Angers, sur six ou sept kilomètres ; il abrite deux minuscules appellations, dont un monopole célèbre pour '
            'la biodynamie.',
         en='Pale to golden yellow. Acacia, linden, pear, quince, toasted almond, honey, a mineral touch. Ample, rich attack, a fresh '
            'finish with a hint of bitterness; it only blossoms after several years. Right-bank schist slopes near Angers, over six '
            'or seven kilometres; it encloses two tiny appellations, one a monopole famous for biodynamics.',
         why=('« Pointe d’amertume », coteaux de 6-7 km rive droite (cahier des charges) ; Coulée de Serrant (monopole) et Roche aux Moines.',
              '“A hint of bitterness”, 6–7 km of right-bank slopes (rulebook); Coulée de Serrant (monopole) and Roche aux Moines.')),
    dict(id='layon', aoc='Coteaux du Layon', alias=['Coteaux du Layon'], zone='anjou', col=('Blanc moelleux ou liquoreux', 'Medium-sweet or sweet white'),
         grapes=CHE,
         fr='Robe dorée. Coing, abricot, miel, agrumes confits, notes de pourriture noble. Bouche suave et fraîche à la fois, puissante '
            'et fine, de longue garde. Coteaux qui suivent une petite rivière jusqu’à la Loire, sur treize communes ; certaines peuvent '
            'ajouter leur nom à l’appellation, comme Beaulieu, Faye ou Saint-Aubin-de-Luigné.',
         en='Golden. Quince, apricot, honey, candied citrus, noble-rot notes. Both luscious and fresh, powerful and fine, for long ageing. '
            'Slopes following a small river to the Loire, over thirteen communes; some may add their name to the appellation, such as '
            'Beaulieu, Faye or Saint-Aubin-de-Luigné.',
         why=('Le Layon, 13 communes, nom de commune possible sur l’étiquette (cahier des charges).',
              'The Layon river, 13 communes, commune name allowed on the label (rulebook).')),
    dict(id='quarts-chaume', aoc='Quarts de Chaume', alias=['Quarts-de-Chaume'], zone='anjou', col=SWEET, grapes=CHE,
         fr='Robe or. Fruits confits, miel, abricot sec, une pointe d’amertume. Bouche puissante et délicate, harmonie parfaite entre '
            'douceur et nervosité. Une quarantaine d’hectares au pied d’un coteau abrupt, dans un méandre au-dessus du Layon ; '
            'le seigneur du lieu se réservait, dit-on, le meilleur quart de la récolte — et c’est le premier « grand cru » du Val de Loire.',
         en='Gold. Candied fruit, honey, dried apricot, a hint of bitterness. Powerful yet delicate, a perfect harmony of sweetness and '
            'nerve. About forty hectares at the foot of a steep slope, in a meander above the Layon; the local lord is said to have kept '
            'the best quarter of the harvest — and it is the Loire Valley’s first “grand cru”.',
         why=('Une quarantaine d’hectares à Rochefort-sur-Loire (cahier des charges) ; mention « Grand Cru » depuis 2011.',
              'About forty hectares at Rochefort-sur-Loire (rulebook); “Grand Cru” mention since 2011.')),
    dict(id='bonnezeaux', aoc='Bonnezeaux', alias=[], zone='anjou', col=SWEET, grapes=CHE,
         fr='Robe dorée aux reflets verts. Fruits secs, fruits exotiques, fleurs blanches. Grande douceur, puissance, équilibre entre '
            'acidité et onctuosité. Trois coteaux exposés au sud-ouest sous un hameau perché sur un coteau abrupt, dont le nom '
            'viendrait de sources ferrugineuses.',
         en='Golden with green tints. Dried fruit, exotic fruit, white flowers. Great sweetness and power, a balance of acidity and '
            'unctuousness. Three south-west-facing slopes below a hamlet perched on a steep slope, whose name is said to come from '
            'iron-rich springs.',
         why=('Hameau de Bonnezeaux, « sources d’eau ferrugineuse », trois coteaux sur Thouarcé (cahier des charges).',
              'The hamlet of Bonnezeaux, “iron-rich springs”, three slopes at Thouarcé (rulebook).')),
    dict(id='cabernet-anjou', aoc='Cabernet d\'Anjou', alias=['Cabernet d’Anjou', 'Cabernet dAnjou'], zone='anjou',
         col=('Rosé demi-sec', 'Medium-dry rosé'), grapes=('Cabernet franc et cabernet-sauvignon', 'Cabernet Franc and Cabernet Sauvignon'),
         fr='Robe rose soutenu aux reflets framboise. Fraise, framboise, groseille, bonbon. Bouche tendre et sucrée, rafraîchie par '
            'l’acidité. Un rosé demi-sec issu des deux cabernets, sur les schistes de « l’Anjou noir » comme sur la craie de « l’Anjou blanc ».',
         en='Deep pink with raspberry tints. Strawberry, raspberry, redcurrant, sweets. Tender, sweet palate refreshed by acidity. '
            'A medium-dry rosé from the two Cabernets, on the schists of “black Anjou” as well as the chalk of “white Anjou”.',
         why=('Rosé avec sucres fermentescibles issu des cabernets ; Anjou noir (schiste) / Anjou blanc (craie) (cahier des charges).',
              'A rosé with residual sugar from the Cabernets; black Anjou (schist) / white Anjou (chalk) (rulebook).')),
    dict(id='rose-anjou', aoc='Rosé d\'Anjou', alias=['Rosé d’Anjou', 'Rose d Anjou'], zone='anjou', col=('Rosé tendre', 'Off-dry rosé'),
         grapes=('Grolleau surtout', 'Mostly Grolleau'),
         fr='Robe rose pâle, saumonée. Fruits rouges légers, bonbon. Bouche ronde, légèrement sucrée, facile. Un rosé tendre à base d’un '
            'cépage local peu connu ailleurs.',
         en='Pale, salmon pink. Light red fruit, sweets. Round, slightly sweet, easy. A tender rosé made mostly from a local grape little '
            'known elsewhere.',
         why=('Le grolleau, cépage angevin, et une légère sucrosité : Rosé d’Anjou.', 'Grolleau, an Anjou grape, and gentle sweetness: Rosé d’Anjou.')),
    dict(id='brissac-r', aoc='Anjou Brissac', alias=['Anjou Villages Brissac', 'Anjou-Villages-Brissac', 'Brissac'], zone='anjou', col=RED,
         grapes=('Cabernet franc et cabernet-sauvignon', 'Cabernet Franc and Cabernet Sauvignon'),
         fr='Robe soutenue. Fruits rouges et noirs, épices, venaison, boisé. Bouche ample et onctueuse, tanins très présents mais fondus : '
            'il faut l’oublier cinq ou six ans. Plateau de schiste au sud-ouest d’Angers, autour d’un château surnommé « le géant du '
            'Val de Loire » pour ses sept étages.',
         en='Deep colour. Red and black fruit, spice, venison, oak. Ample, unctuous palate, very present but rounded tannins: forget it '
            'for five or six years. A schist plateau south-west of Angers, around a castle nicknamed “the giant of the Loire Valley” for '
            'its seven storeys.',
         why=('« Il faut savoir l’oublier cinq ou six années » (cahier des charges) ; château de Brissac, le plus haut château de France.',
              '“One must forget it for five or six years” (rulebook); Brissac castle, the tallest château in France.')),
    dict(id='saumur-champigny-r', aoc='Saumur-Champigny', alias=['Saumur Champigny'], zone='anjou', col=RED, grapes=CF,
         fr='Robe rubis foncé. Fruits rouges croquants, violette. Bouche fraîche, ronde, souple, charmeuse dès la jeunesse. Sur la craie '
            'blanche — le tuffeau — de « l’Anjou blanc », au bord de la Loire, près d’une ville connue pour son École de cavalerie.',
         en='Dark ruby. Crunchy red fruit, violet. Fresh, round, supple, charming from youth. On the white chalk — tuffeau — of “white '
            'Anjou”, by the Loire, near a town known for its cavalry school.',
         why=('« Fruits rouges ou violette… frais, ronds et souples » ; craie tuffeau de l’Anjou blanc (cahier des charges) ; Cadre noir de Saumur.',
              '“Red fruit or violet… fresh, round, supple”; tuffeau chalk of white Anjou (rulebook); the Cadre Noir of Saumur.')),
    dict(id='saumur-mousseux', aoc='Saumur', alias=['Saumur brut', 'Saumur mousseux'], zone='anjou',
         col=('Blanc mousseux', 'Sparkling white'), grapes=('Chenin, chardonnay, cabernet franc…', 'Chenin, Chardonnay, Cabernet Franc…'),
         fr='Robe pâle, bulles fines. Pomme, poire, coing, une note briochée. Bouche fraîche et vive. Élevé dans des kilomètres de galeries '
            'creusées dans le tuffeau ; les maisons de la ville font mousser leurs vins depuis le début du XIX<sup>e</sup> siècle, '
            'ce qui en fait l’un des plus anciens pôles d’effervescents de France.',
         en='Pale, fine bubbles. Apple, pear, quince, a brioche note. Fresh, lively palate. Aged in kilometres of galleries dug into the '
            'tuffeau; the town’s houses have been making sparkling wine since the early 19th century, one of France’s oldest sparkling '
            'centres.',
         why=('Saumur mousseux (Ackerman, 1811) et les caves de tuffeau ; mention « mousseux » de l’AOC Saumur.',
              'Sparkling Saumur (Ackerman, 1811) and the tuffeau cellars; the “mousseux” mention of the Saumur AOC.')),
    dict(id='cremant-loire', aoc='Crémant de Loire', alias=['Cremant de Loire'], zone='anjou', col=('Blanc effervescent', 'Sparkling white'),
         grapes=('Chenin, chardonnay, cabernet franc…', 'Chenin, Chardonnay, Cabernet Franc…'),
         fr='Robe pâle, chapelets de bulles fines et persistantes. Fleurs blanches, pêche, abricot. Bouche fine et harmonieuse qui marie '
            'fraîcheur et douceur. Une aire qui longe le fleuve et ses affluents sur environ 200 km, à travers des centaines de communes '
            '« dont certaines sont célèbres par leur château ».',
         en='Pale, strings of fine, persistent bubbles. White flowers, peach, apricot. Fine, harmonious palate that blends freshness and '
            'softness. An area following the river and its tributaries for about 200 km, across hundreds of communes “some of them '
            'famous for their château”.',
         why=('« Environ 200 kilomètres… communes célèbres par leur château » ; « fleurs blanches, pêche, abricot » (cahier des charges).',
              '“About 200 kilometres… communes famous for their château”; “white flowers, peach, apricot” (rulebook).')),
    # ------------------------------------------------------------------ Touraine
    dict(id='chinon-r', aoc='Chinon', alias=[], zone='touraine', col=RED, grapes=CF,
         fr='Robe rubis sombre à grenat. Fruits rouges et noirs, violette, une note de poivron et de mine de crayon. Tanins présents mais '
            'fondus, élégance. Coteaux de la Vienne au pied d’une forteresse où Jeanne d’Arc rencontra le dauphin, tout près de la maison '
            'natale de Rabelais.',
         en='Dark ruby to garnet. Red and black fruit, violet, a hint of bell pepper and pencil lead. Present but rounded tannins, elegance. '
            'Slopes of the Vienne below a fortress where Joan of Arc met the Dauphin, close to Rabelais’s birthplace.',
         why=('Vallée de la Vienne, 26 communes (cahier des charges) ; forteresse de Chinon, La Devinière de Rabelais.',
              'The Vienne valley, 26 communes (rulebook); Chinon fortress, Rabelais’s La Devinière.')),
    dict(id='bourgueil-r', aoc='Bourgueil', alias=[], zone='touraine', col=RED, grapes=CF,
         fr='Robe rubis sombre à grenat profond. Fruits rouges et noirs ; avec l’âge, cacao, fumé, épices. Structure tannique présente '
            'mais fondue. Sur la rive nord de la Loire, un coteau coiffé par la forêt et des croupes de graviers que l’on appelle ici '
            'des « montilles ».',
         en='Dark ruby to deep garnet. Red and black fruit; with age, cocoa, smoke, spice. Present but rounded tannins. On the north bank '
            'of the Loire, a forest-capped slope and gravel rises known here as “montilles”.',
         why=('Rive nord, forêt de Gâtine, croupes appelées « montilles » ; notes « cacaotées, fumées » (cahier des charges).',
              'North bank, Gâtine forest, rises called “montilles”; “cocoa, smoky” notes (rulebook).')),
    dict(id='st-nicolas-r', aoc='Saint-Nicolas-de-Bourgueil', alias=['Saint Nicolas de Bourgueil', 'St-Nicolas-de-Bourgueil'], zone='touraine',
         col=RED, grapes=CF,
         fr='Robe rubis. Fruits rouges, framboise, cassis. Bouche élégante et souple, à boire jeune pour la plupart. Une seule commune, '
            'sur une ancienne terrasse de la Loire, à côté d’une voisine plus vaste dont elle reprend le nom.',
         en='Ruby. Red fruit, raspberry, blackcurrant. Elegant, supple palate, mostly to drink young. A single commune on an old Loire '
            'terrace, next to a larger neighbour whose name it takes up.',
         why=('Une seule commune, « ancienne terrasse de la Loire » ; vins « élégants, souples » (cahier des charges).',
              'A single commune, “an old Loire terrace”; “elegant, supple” wines (rulebook).')),
    dict(id='vouvray-b', aoc='Vouvray', alias=[], zone='touraine', col=('Blanc demi-sec', 'Medium-dry white'), grapes=CHE,
         fr='Robe or pâle. Coing, miel, tilleul, pomme cuite, fruits exotiques. Bouche tendre, une douceur légère portée par une acidité '
            'vibrante, très longue garde. Plateau au-dessus de Tours dont les falaises de tuffeau jaune sont creusées de caves et de '
            'maisons troglodytiques ; ici, le même cépage se fait sec, demi-sec, moelleux ou effervescent.',
         en='Pale gold. Quince, honey, linden, baked apple, exotic fruit. Tender palate, gentle sweetness carried by vibrant acidity, very '
            'long ageing. A plateau above Tours whose yellow tuffeau cliffs are dug with troglodyte cellars and homes; here the same grape '
            'is made dry, medium-dry, sweet or sparkling.',
         why=('« Caves et maisons troglodytiques creusées dans les falaises de tuffeau jaune », chenin sec à moelleux et mousseux (cahier des charges).',
              '“Troglodyte cellars and homes dug into the yellow tuffeau cliffs”, Chenin dry to sweet and sparkling (rulebook).')),
    dict(id='montlouis-b', aoc='Montlouis-sur-Loire', alias=['Montlouis'], zone='touraine', col=WHITE, grapes=CHE,
         fr='Robe or pâle. Fruits blancs, fleurs, puis miel et coing. Bouche vive et tendue. Trois communes sur un plateau calcaire en '
            'triangle entre deux rivières et une forêt royale, face à un voisin plus célèbre de l’autre côté de la Loire ; on y fait '
            'aussi un « pétillant originel » à fermentation unique.',
         en='Pale gold. White fruit, flowers, then honey and quince. Lively, taut palate. Three communes on a limestone triangle between '
            'two rivers and a royal forest, facing a more famous neighbour across the Loire; a single-fermentation “pétillant originel” '
            'is made here too.',
         why=('Triangle Loire–Cher–forêt d’Amboise, 3 communes ; « vins mousseux à fermentation unique » (cahier des charges).',
              'Loire–Cher–Amboise forest triangle, 3 communes; “single-fermentation sparkling wines” (rulebook).')),
    dict(id='jasnieres-b', aoc='Jasnières', alias=['Jasnieres'], zone='touraine', col=WHITE, grapes=CHE,
         fr='Robe or pâle. Fruits et fleurs, puis miel et rose fanée avec l’âge. Bouche tranchante, très fraîche. Un seul coteau très pentu '
            'de cinq kilomètres sur 300 mètres de large, exposé plein sud, dans la vallée d’un affluent qu’il ne faut pas confondre '
            'avec le grand fleuve.',
         en='Pale gold. Fruit and flowers, then honey and faded rose with age. Cutting, very fresh palate. A single, very steep '
            'south-facing slope five kilometres long and 300 metres wide, in the valley of a tributary not to be confused with the great river.',
         why=('Un coteau de 5 km sur la rive droite du Loir, entre Ruillé et Lhomme ; « miel, rose fanée » (cahier des charges).',
              'One 5 km slope on the right bank of the Loir, between Ruillé and Lhomme; “honey, faded rose” (rulebook).')),
    dict(id='vendomois-gris', aoc='Coteaux du Vendômois', alias=['Coteaux du Vendomois'], zone='touraine', col=('Vin gris', 'Vin gris'),
         grapes=('Pineau d’Aunis', 'Pineau d’Aunis'),
         fr='Robe pâle aux reflets saumonés. Nez généreux dominé par le poivre. Bouche légère, délicate, rafraîchissante. Un rouge pressé '
            'directement comme un blanc, issu d’un vieux cépage local — la spécialité de six boucles serrées d’une rivière à l’ouest '
            'de Vendôme.',
         en='Pale with salmon tints. A generous nose dominated by pepper. Light, delicate, refreshing palate. A red grape pressed straight '
            'away like a white, from an old local variety — the speciality of six tight meanders of a river west of Vendôme.',
         why=('Vins gris « issus uniquement du cépage pineau d’Aunis par pressurage direct », « senteur poivrée » ; méandres du Loir (cahier des charges).',
              'Gris wines “made only from Pineau d’Aunis by direct pressing”, “peppery scent”; meanders of the Loir (rulebook).')),
    dict(id='noble-joue-rs', aoc='Touraine Noble Joué', alias=['Noble Joué', 'Touraine Noble Joue'], zone='touraine', col=('Rosé (gris)', 'Rosé (gris)'),
         grapes=('Pinot meunier, pinot gris, pinot noir', 'Pinot Meunier, Pinot Gris, Pinot Noir'),
         fr='Robe pâle. Pivoine, groseille, griotte, pamplemousse. Bouche fraîche et grasse à la fois. Un « gris » de trois pinots, '
            'sur quelques îlots de vigne de plateau aux portes mêmes de Tours, entre l’Indre et le Cher.',
         en='Pale. Peony, redcurrant, morello cherry, grapefruit. Fresh yet rich palate. A “gris” from three Pinots, on a few plateau vine '
            'islands right at the gates of Tours, between the Indre and the Cher.',
         why=('« Pivoine, groseille, griotte, pamplemousse », 5 communes au sud de Tours en contexte périurbain (cahier des charges).',
              '“Peony, redcurrant, morello, grapefruit”, 5 communes south of Tours in a peri-urban setting (rulebook).')),
    dict(id='cour-cheverny-b', aoc='Cour-Cheverny', alias=['Cour Cheverny'], zone='touraine', col=WHITE, grapes=('Romorantin', 'Romorantin'),
         fr='Robe or pâle. Agrumes, fleurs blanches, parfois rhubarbe ou menthol ; avec les années, miel, cire, citron confit et une légère '
            'oxydation. Bouche très vive. Clairières viticoles entre la forêt de Chambord et la Sologne, dédiées à un cépage rare que '
            'François I<sup>er</sup> aurait fait venir de Bourgogne.',
         en='Pale gold. Citrus, white flowers, sometimes rhubarb or menthol; with years, honey, wax, candied lemon and a light oxidative '
            'note. Very lively palate. Vineyard clearings between the Chambord forest and the Sologne, devoted to a rare grape that '
            'François I is said to have brought from Burgundy.',
         why=('« Miel, citron, cire… caractéristiques du cépage romorantin » (cahier des charges) ; seule AOC du romorantin.',
              '“Honey, lemon, wax… typical of the Romorantin grape” (rulebook); the only Romorantin AOC.')),
    dict(id='cheverny-b', aoc='Cheverny', alias=[], zone='touraine', col=WHITE, grapes=('Sauvignon et chardonnay', 'Sauvignon and Chardonnay'),
         fr='Robe pâle. Agrumes, fruits exotiques, fleurs blanches, une touche de buis. Bouche vive équilibrée par de la rondeur. Un '
            'assemblage, chose rare en Loire, né dans des clairières face à Blois, autour d’un château qui a inspiré à Hergé celui '
            'du capitaine Haddock.',
         en='Pale. Citrus, exotic fruit, white flowers, a touch of boxwood. Lively palate balanced by roundness. A blend — rare in the '
            'Loire — born in clearings facing Blois, around a château that inspired Hergé’s Marlinspike Hall for Captain Haddock.',
         why=('Assemblage sauvignon-chardonnay ; château de Cheverny = Moulinsart ; « touche de buis » (cahier des charges).',
              'A Sauvignon–Chardonnay blend; Château de Cheverny = Marlinspike; “a touch of boxwood” (rulebook).')),
    dict(id='valencay-b', aoc='Valençay', alias=['Valencay'], zone='touraine', col=WHITE, grapes=('Sauvignon avec chardonnay', 'Sauvignon with Chardonnay'),
         fr='Robe pâle. Genêt, fleurs blanches, pierre à fusil. Bouche vive avec une certaine rondeur. Un plateau au sol chargé de silex, '
            'autour du château de Talleyrand, dans un pays plus connu pour un fromage de chèvre en pyramide tronquée.',
         en='Pale. Broom, white flowers, flint. Lively palate with some roundness. A plateau with flint-rich soils, around Talleyrand’s '
            'château, in a country better known for a goat’s cheese shaped like a truncated pyramid.',
         why=('« Pierre à fusil… forte charge en silex des sols » (cahier des charges) ; château de Talleyrand et fromage de Valençay.',
              '“Flint… high flint content of the soils” (rulebook); Talleyrand’s château and Valençay cheese.')),
    # ------------------------------------------------------------------ Centre-Loire
    dict(id='sancerre-b', aoc='Sancerre', alias=[], zone='centre', col=WHITE, grapes=SAU,
         fr='Robe or pâle. Agrumes, groseille à maquereau, fleurs blanches, pierre à fusil. Bouche ronde puis finale fraîche et ciselée. '
            'Collines de la rive gauche dominées par un bourg perché, sur des sols de « caillottes », de « terres blanches » et de silex ; '
            'le voisin idéal d’un petit chèvre de Chavignol.',
         en='Pale gold. Citrus, gooseberry, white flowers, flint. Round palate then a fresh, chiselled finish. Left-bank hills dominated '
            'by a hilltop town, on “caillottes”, “terres blanches” and flint soils; the ideal partner for a little Chavignol goat’s cheese.',
         why=('14 communes du Cher, collines de 200 à 400 m sur la rive gauche (cahier des charges) ; le crottin de Chavignol.',
              '14 Cher communes, 200–400 m hills on the left bank (rulebook); the Crottin de Chavignol.')),
    dict(id='sancerre-r', aoc='Sancerre', alias=[], zone='centre', col=RED, grapes=('Pinot noir', 'Pinot Noir'),
         fr='Robe rubis clair. Cerise, framboise, une note épicée. Tanins souples et élégants, puissance et finesse. Un pinot du centre de '
            'la France, dans une appellation dont la renommée vient surtout de son vin blanc.',
         en='Light ruby. Cherry, raspberry, a spicy note. Supple, elegant tannins, power and finesse. A Pinot from the centre of France, '
            'in an appellation famed mostly for its white.',
         why=('Pinot noir seul en rouge ; « tanins souples et élégants » (cahier des charges).', 'Pinot Noir alone for the red; “supple, elegant tannins” (rulebook).')),
    dict(id='pouilly-fume-b', aoc='Pouilly-Fumé', alias=['Pouilly Fume', 'Blanc Fumé de Pouilly'], zone='centre', col=WHITE, grapes=SAU,
         fr='Robe jaune pâle à or. Agrumes, fleurs blanches, notes de silex fumé. Bouche complexe, fine, généreuse et fraîche. Sept '
            'communes de la rive droite regroupées autour d’une butte coiffée d’une église ; le cépage y porte un nom local qui '
            'évoque la fumée.',
         en='Pale yellow to gold. Citrus, white flowers, smoky flint. Complex, fine, generous and fresh palate. Seven right-bank communes '
            'grouped around a hill topped by a church; the grape bears a local name evoking smoke.',
         why=('Butte de Saint-Andelain, 7 communes rive droite (cahier des charges) ; le sauvignon dit « blanc fumé ».',
              'The Saint-Andelain hill, 7 right-bank communes (rulebook); Sauvignon locally called “blanc fumé”.')),
    dict(id='pouilly-loire-b', aoc='Pouilly-sur-Loire', alias=['Pouilly sur Loire'], zone='centre', col=WHITE, grapes=('Chasselas', 'Chasselas'),
         fr='Robe pâle. Fleurs blanches, fruits secs, une note minérale. Bouche gouleyante, franche, avec une certaine rondeur. Même aire '
            'que son illustre voisin, mais un autre cépage : celui qu’on connaît surtout comme raisin de table — et en Suisse.',
         en='Pale. White flowers, dried fruit, a mineral note. Easy-drinking, frank palate with some roundness. Same area as its illustrious '
            'neighbour, but another grape: the one best known as a table grape — and in Switzerland.',
         why=('Chasselas : « gouleyants, francs… fruits secs » (cahier des charges) ; même aire que le Pouilly-Fumé.',
              'Chasselas: “easy-drinking, frank… dried fruit” (rulebook); same area as Pouilly-Fumé.')),
    dict(id='menetou-b', aoc='Menetou-Salon', alias=['Menetou Salon'], zone='centre', col=WHITE, grapes=SAU,
         fr='Robe jaune pâle à or. Agrumes, notes variétales et minérales. Attaque suave, finale fraîche. Dix communes du Cher sur une cuesta '
            'au nord-est de Bourges, au sud-ouest d’un voisin très célèbre.',
         en='Pale yellow to gold. Citrus, varietal and mineral notes. Smooth attack, fresh finish. Ten Cher communes on a cuesta north-east '
            'of Bourges, south-west of a very famous neighbour.',
         why=('10 communes, cuesta au nord-est de Bourges, au sud-ouest de Sancerre (cahier des charges).',
              '10 communes, a cuesta north-east of Bourges, south-west of Sancerre (rulebook).')),
    dict(id='quincy-b', aoc='Quincy', alias=[], zone='centre', col=WHITE, grapes=SAU,
         fr='Robe pâle. Fruits mûrs, fleurs blanches, tonalité minérale. Bouche sèche, fraîche et fine. Deux communes sur une ancienne '
            'terrasse de sables et de graviers de la rive gauche du Cher, entre Bourges et Vierzon — l’une des toutes premières AOC, '
            'reconnue en 1936.',
         en='Pale. Ripe fruit, white flowers, a mineral tone. Dry, fresh, fine palate. Two communes on an old terrace of sand and gravel on '
            'the left bank of the Cher, between Bourges and Vierzon — one of the very first AOCs, recognised in 1936.',
         why=('Quincy et Brinay, ancienne terrasse du Cher (cahier des charges) ; AOC dès 1936.', 'Quincy and Brinay, an old Cher terrace (rulebook); AOC since 1936.')),
    dict(id='reuilly-gris', aoc='Reuilly', alias=[], zone='centre', col=('Rosé (gris)', 'Rosé (gris)'), grapes=('Pinot gris', 'Pinot Gris'),
         fr='Robe pâle couleur « œil de perdrix ». Pêche blanche, groseille, fleurs. Bouche souple et délicate. Deux îlots de vignes au '
            'sud-ouest de Bourges, à cheval sur l’Indre et le Cher ; le rosé y est un pinot gris pressé directement.',
         en='Pale, “partridge eye” colour. White peach, redcurrant, flowers. Supple, delicate palate. Two vineyard islands south-west of '
            'Bourges, straddling the Indre and the Cher; the rosé here is a directly pressed Pinot Gris.',
         why=('Rosés « œil de perdrix » (cahier des charges), de pinot gris ; deux entités distantes de 7 km.',
              '“Partridge eye” rosés (rulebook), from Pinot Gris; two areas 7 km apart.')),
    dict(id='giennois-r', aoc='Coteaux du Giennois', alias=['Coteaux Giennois'], zone='centre', col=RED,
         grapes=('Pinot noir et gamay', 'Pinot Noir and Gamay'),
         fr='Robe rubis. Petits fruits rouges et noirs, notes épicées. Bouche fine et fruitée. Une étroite bande de coteaux qui longe la '
            'Loire sur 45 km, de la ville de la faïence jusqu’à Cosne ; le rouge y assemble deux cépages, comme en Bourgogne voisine.',
         en='Ruby. Small red and black fruit, spicy notes. Fine, fruity palate. A narrow strip of slopes along the Loire for 45 km, from the '
            'town of faience down to Cosne; the red blends two grapes, as in neighbouring Burgundy.',
         why=('45 km de Gien à Cosne-Cours-sur-Loire (cahier des charges) ; assemblage pinot noir-gamay.',
              '45 km from Gien to Cosne-Cours-sur-Loire (rulebook); a Pinot Noir–Gamay blend.')),
    dict(id='orleans-rs', aoc='Orléans', alias=['Orleans'], zone='centre', col=('Rosé', 'Rosé'), grapes=('Pinot meunier surtout', 'Mostly Pinot Meunier'),
         fr='Robe « œil de perdrix ». Petits fruits rouges, une douceur aromatique et de la vivacité. Le vignoble le plus septentrional du '
            'Val de Loire, entre la Beauce et la Sologne, autour d’une ville plus célèbre pour sa pucelle et son vinaigre que pour son vin ; '
            'le cépage-roi y est celui de la Champagne.',
         en='“Partridge eye” colour. Small red fruit, aromatic softness and liveliness. The Loire Valley’s northernmost vineyard, between '
            'the Beauce and the Sologne, around a city more famous for its Maid and its vinegar than its wine; the key grape is the one '
            'from Champagne.',
         why=('« La plus septentrionale de la vallée de la Loire », rosés « œil de perdrix » (cahier des charges) ; pinot meunier.',
              '“The northernmost of the Loire Valley”, “partridge eye” rosés (rulebook); Pinot Meunier.')),
    dict(id='chateaumeillant-gris', aoc='Châteaumeillant', alias=['Chateaumeillant'], zone='centre', col=('Vin gris', 'Vin gris'),
         grapes=('Gamay surtout', 'Mostly Gamay'),
         fr='Robe claire. Agrumes, fruits blancs, fraîcheur. Un gris de gamay du Berry, sur une bande de 20 km par 5 à cheval sur l’Indre '
            'et le Cher, au pied de la bordure la plus septentrionale du Massif central.',
         en='Light colour. Citrus, white fruit, freshness. A Gamay gris from the Berry, on a 20 by 5 km strip straddling the Indre and the '
            'Cher, at the foot of the northernmost edge of the Massif Central.',
         why=('Vins gris, bande de 20 × 5 km sur 7 communes, « bordure la plus septentrionale du Massif Central » (cahier des charges).',
              'Gris wines, a 20 × 5 km strip over 7 communes, “the northernmost edge of the Massif Central” (rulebook).')),
    # ------------------------------------------------------------------ Auvergne & upper Loire
    dict(id='st-pourcain-b', aoc='Saint-Pourçain', alias=['Saint Pourcain', 'St-Pourçain'], zone='auvergne', col=WHITE,
         grapes=('Chardonnay et tressallier', 'Chardonnay and Tressallier'),
         fr='Robe pâle. Fruits blancs, fruits exotiques, agrumes, parfois menthe. Vivacité et ampleur. Îlots de vigne au-dessus du val de '
            'l’Allier et de la Sioule ; l’assemblage blanc fait appel à un cépage local, le tressallier, presque inconnu ailleurs.',
         en='Pale. White fruit, exotic fruit, citrus, sometimes mint. Liveliness and breadth. Vineyard islands above the Allier and Sioule '
            'valleys; the white blend uses a local grape, Tressallier, almost unknown elsewhere.',
         why=('Le tressallier, cépage emblématique de Saint-Pourçain ; « notes florales ou mentholées » (cahier des charges).',
              'Tressallier, Saint-Pourçain’s signature grape; “floral or minty notes” (rulebook).')),
    dict(id='auvergne-r', aoc='Côtes d\'Auvergne', alias=['Côtes d’Auvergne', 'Cotes d Auvergne'], zone='auvergne', col=RED,
         grapes=('Gamay surtout, un peu de pinot noir', 'Mostly Gamay, a little Pinot Noir'),
         fr='Robe assez soutenue. Cassis, groseille, puis griotte et poivre. Bouche fruitée, une pointe minérale. Les rebords de la Limagne '
            'et les flancs des volcans, sur 80 km du nord au sud ; certains crus, comme Chanturgue ou Corent, peuvent ajouter leur nom.',
         en='Fairly deep colour. Blackcurrant, redcurrant, then morello and pepper. Fruity palate, a mineral touch. The edges of the Limagne '
            'and the flanks of the volcanoes, over 80 km north to south; some crus, such as Chanturgue or Corent, may add their name.',
         why=('« Flancs des édifices volcaniques », 80 km dans le Puy-de-Dôme (cahier des charges) ; dénominations Chanturgue, Corent, Boudes…',
              '“The flanks of volcanic edifices”, 80 km in the Puy-de-Dôme (rulebook); denominations Chanturgue, Corent, Boudes…')),
    dict(id='forez-r', aoc='Côtes du Forez', alias=['Cotes du Forez'], zone='auvergne', col=RED, grapes=('Gamay', 'Gamay'),
         fr='Robe intense aux reflets cerise. Petits fruits rouges ; sur basalte, des notes minérales et épicées et des tanins plus présents. '
            'Bouche souple et soyeuse. Au cœur du triangle Lyon – Clermont-Ferrand – Saint-Étienne, sur les premiers contreforts des '
            'monts du Forez.',
         en='Intense with cherry glints. Small red fruit; on basalt, mineral and spicy notes and firmer tannins. Supple, silky palate. In the '
            'heart of the Lyon – Clermont-Ferrand – Saint-Étienne triangle, on the first foothills of the Forez mountains.',
         why=('Gamay, « sols basaltiques… notes minérales et épicées », triangle Lyon-Clermont-Saint-Étienne (cahier des charges).',
              'Gamay, “basalt soils… mineral and spicy notes”, the Lyon–Clermont–Saint-Étienne triangle (rulebook).')),
]
