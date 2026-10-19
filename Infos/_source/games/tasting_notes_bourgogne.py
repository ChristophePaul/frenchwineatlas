"""Burgundy batch for « Goûtez votre savoir » (see tasting_notes.py for the field list).

Sources: where the cahier des charges has a filled-in « lien à l'origine » (Chablis, Petit Chablis, Chablis grand cru,
Vézelay, Bouzeron, Clos de Vougeot, Volnay, Givry, Pouilly-Fuissé, Saint-Véran, Viré-Clessé) its product description
is followed. The 2010-era Côte d'Or rulebooks leave that section empty: those notes use well-established facts
(classifications, places, history) — flagged in the review sheet.
"""

ZONES_BGY = {
    'chablis': ('Bourgogne · Chablis & Grand Auxerrois (Yonne)', 'Burgundy · Chablis & Grand Auxerrois (Yonne)'),
    'nuits': ('Bourgogne · Côte de Nuits', 'Burgundy · Côte de Nuits'),
    'beaune': ('Bourgogne · Côte de Beaune', 'Burgundy · Côte de Beaune'),
    'chalonnais': ('Bourgogne · Côte chalonnaise', 'Burgundy · Côte Chalonnaise'),
    'maconnais': ('Bourgogne · Mâconnais', 'Burgundy · Mâconnais'),
    'bregional': ('Bourgogne · appellations régionales', 'Burgundy · regional appellations'),
}

_B = {'beaune': ['Aloxe-Corton', 'Bienvenues-Bâtard-Montrachet', 'Blagny', 'Chassagne-Montrachet', 'Chevalier-Montrachet',
                 'Chorey-lès-Beaune', 'Corton-Charlemagne', 'Côte de Beaune-Villages', 'Côte de Beaune', 'Criots-Bâtard-Montrachet',
                 'Ladoix', 'Maranges', 'Meursault', 'Monthélie', 'Montrachet', 'Pernand-Vergelesses', 'Pommard',
                 'Puligny-Montrachet', 'Saint-Aubin', 'Saint-Romain', 'Santenay', 'Savigny-lès-Beaune', 'Auxey-Duresses',
                 'Bâtard-Montrachet', 'Beaune', 'Corton', 'Volnay', 'Charlemagne'],
      'nuits': ['Bonnes-Mares', 'Chambertin-Clos de Bèze', 'Chambertin', 'Chambolle-Musigny', 'Chapelle-Chambertin',
                'Charmes-Chambertin', 'Clos Saint-Denis', 'Clos de Vougeot', 'Clos de Tart', 'Clos de la Roche',
                'Clos des Lambrays', 'Échezeaux', 'Gevrey-Chambertin', 'Grands-Échezeaux', 'Griotte-Chambertin', 'La Grande Rue',
                'La Romanée', 'La Tâche', 'Mazis-Chambertin', 'Mazoyères-Chambertin', 'Richebourg', 'Romanée-Conti',
                'Romanée-Saint-Vivant', 'Ruchottes-Chambertin', 'Vosne-Romanée', 'Latricières-Chambertin',
                'Côte de Nuits-Villages', 'Fixin', 'Marsannay', 'Morey-Saint-Denis', 'Musigny', 'Nuits-Saint-Georges', 'Vougeot'],
      'chablis': ['Chablis', 'Chablis Grand Cru', 'Petit Chablis', 'Irancy', 'Saint-Bris', 'Vézelay'],
      'chalonnais': ['Bouzeron', 'Givry', 'Mercurey', 'Montagny', 'Rully'],
      'maconnais': ['Mâcon', 'Pouilly-Fuissé', 'Pouilly-Loché', 'Pouilly-Vinzelles', 'Saint-Véran', 'Viré-Clessé'],
      'bregional': ['Bourgogne Mousseux', 'Bourgogne Passe-Tout-Grains', 'Bourgogne Aligoté', 'Coteaux Bourguignons',
                    'Crémant de Bourgogne', 'Bourgogne']}
AOC_ZONE_BGY = {a: z for z, names in _B.items() for a in names}

RED = ('Rouge tranquille sec', 'Still dry red')
WHITE = ('Blanc sec', 'Dry white')
PN = ('Pinot noir', 'Pinot Noir')
CH = ('Chardonnay', 'Chardonnay')

NOTES_BGY = [
    # ------------------------------------------------------------------ Chablis & Yonne
    dict(id='chablis-b', aoc='Chablis', alias=['Chablis Premier Cru', 'Chablis 1er cru'], zone='chablis', col=WHITE, grapes=CH,
         fr='Robe or pâle aux reflets verts. Nez de citron, de pomme verte, de fleurs blanches et ce parfum de coquille d’huître '
            'et de pierre mouillée. Bouche vive, tendue, saline, d’une grande pureté ; il gagne en complexité avec huit à dix ans. '
            'Ses coteaux bordent la vallée du Serein, sur des marnes truffées de minuscules huîtres fossiles en forme de virgule.',
         en='Pale gold with green tints. Lemon, green apple, white flowers and that scent of oyster shell and wet stone. '
            'A lively, taut, saline palate of great purity; it gains complexity over eight to ten years. Its slopes line the '
            'Serein valley, on marls studded with tiny comma-shaped fossil oysters.',
         why=('Vallée du Serein et « Marnes à Exogyra virgula », riches en petites huîtres en forme de virgule (cahier des charges) : le kimméridgien de Chablis.',
              'The Serein valley and the “Exogyra virgula marls”, full of tiny comma-shaped oysters (rulebook): Chablis’s Kimmeridgian.')),
    dict(id='chablis-gc-b', aoc='Chablis Grand Cru', alias=['Chablis GC'], zone='chablis', col=WHITE, grapes=CH,
         fr='Robe or vert. Nez concentré : agrumes, fleurs, silex, une pointe de miel. Bouche ferme dans la jeunesse, minérale mais '
            'charnue, longue ; plénitude vers dix ans. Une seule colline exposée au sud-ouest, sur la rive droite d’une petite '
            'rivière, face au bourg, découpée en sept climats.',
         en='Green-gold. A concentrated nose: citrus, flowers, flint, a hint of honey. Firm when young, mineral yet fleshy, long; '
            'at its peak around ten years. A single south-west-facing hill on the right bank of a small river, facing the town, '
            'divided into seven climats.',
         why=('Un coteau unique, rive droite du Serein face à Chablis, en sept climats (Blanchot, Bougros, Les Clos, Grenouilles, Preuses, Valmur, Vaudésir).',
              'One hillside, right bank of the Serein facing Chablis, in seven climats (Blanchot, Bougros, Les Clos, Grenouilles, Preuses, Valmur, Vaudésir).')),
    dict(id='petit-chablis-b', aoc='Petit Chablis', alias=[], zone='chablis', col=WHITE, grapes=CH,
         fr='Robe très pâle. Citron, pomme verte, une touche florale. Bouche légère, vive et minérale, sans prétention : un vin '
            'qui ne demande pas à vieillir. Il vient surtout des plateaux qui dominent la vallée du Serein, au-dessus des coteaux '
            'de son grand frère.',
         en='Very pale. Lemon, green apple, a floral touch. A light, lively, mineral palate, without pretension: a wine that '
            'does not need ageing. It comes mostly from the plateaus above the Serein valley, over the slopes of its big brother.',
         why=('« Minéralité et légèreté… un vin de primeur ne demandant pas à vieillir » (cahier des charges) : le plus simple des vins du Chablisien.',
              '“Minerality and lightness… a wine that does not need ageing” (rulebook): the simplest of the Chablis wines.')),
    dict(id='saint-bris-b', aoc='Saint-Bris', alias=['Saint Bris'], zone='chablis', col=WHITE,
         grapes=('Sauvignon blanc et sauvignon gris', 'Sauvignon Blanc and Sauvignon Gris'),
         fr='Robe pâle. Nez explosif de buis, de pamplemousse, de groseille à maquereau et de bourgeon de cassis. Bouche vive, '
            'tranchante, très aromatique. Surprise : nous sommes en Bourgogne, près d’Auxerre, dans la seule appellation de la '
            'région qui n’est pas faite de chardonnay, d’aligoté ou de pinot.',
         en='Pale. An explosive nose of boxwood, grapefruit, gooseberry and blackcurrant bud. Lively, cutting, very aromatic palate. '
            'Surprise: we are in Burgundy, near Auxerre, in the only appellation of the region not made from Chardonnay, Aligoté '
            'or Pinot.',
         why=('Seule AOC de Bourgogne issue du sauvignon (blanc et gris).', 'The only Burgundy AOC made from Sauvignon (Blanc and Gris).')),
    dict(id='irancy-r', aoc='Irancy', alias=[], zone='chablis', col=RED,
         grapes=('Pinot noir, avec un peu de césar', 'Pinot Noir, with a little César'),
         fr='Robe rubis. Cerise et griotte, une touche poivrée et un grain de tanin un peu rustique. Bouche fraîche, assez structurée '
            'pour un rouge du nord de la Bourgogne. Village de l’Yonne entouré de cerisiers, seul de la région à pouvoir ajouter '
            'au pinot un vieux cépage local nommé, dit-on, en souvenir des légions romaines.',
         en='Ruby. Cherry and morello, a peppery touch and a slightly rustic tannic grain. A fresh palate, fairly structured for a '
            'northern Burgundy red. A Yonne village ringed by cherry orchards, the only one in the region allowed to add to its '
            'Pinot an old local grape said to be named after the Roman legions.',
         why=('Le césar, cépage local autorisé en complément du pinot noir à Irancy ; village célèbre pour ses cerisiers.',
              'César, a local grape allowed alongside Pinot Noir in Irancy; the village is famous for its cherry trees.')),
    dict(id='vezelay-b', aoc='Vézelay', alias=['Vezelay'], zone='chablis', col=WHITE, grapes=CH,
         fr='Robe or jaune pâle. Nez floral, frais et minéral. Bouche droite, d’une belle fraîcheur, qui gagne en complexité avec '
            'l’âge. Coteaux calcaires de la vallée de la Cure à l’orée du Morvan, loin de tout autre vignoble bourguignon, au pied '
            'd’une colline couronnée par une basilique célèbre, départ d’un chemin de Compostelle.',
         en='Pale yellow-gold. A floral, fresh, mineral nose. Straight palate with fine freshness, gaining complexity with age. '
            'Limestone slopes of the Cure valley at the edge of the Morvan, far from any other Burgundy vineyard, below a hill '
            'crowned by a famous basilica, a starting point of the Way of St James.',
         why=('Vallée de la Cure, Morvan, isolement géographique (cahier des charges) et basilique de Vézelay (UNESCO).',
              'The Cure valley, the Morvan, geographical isolation (rulebook) and the basilica of Vézelay (UNESCO).')),
    # ------------------------------------------------------------------ Côte chalonnaise
    dict(id='bouzeron-b', aoc='Bouzeron', alias=['Bourgogne Aligoté Bouzeron'], zone='chalonnais', col=WHITE,
         grapes=('Aligoté', 'Aligoté'),
         fr='Robe or pâle, légèrement vert d’eau. Acacia, fleurs blanches, noisette, citron, une note de silex et parfois de croissant '
            'chaud. Bouche ronde et persistante, d’une vivacité gourmande. Une petite vallée fraîche ouverte au nord, au bout de la '
            'Côte chalonnaise : la seule appellation de village de Bourgogne qui ne s’intéresse pas au chardonnay.',
         en='Pale gold with a light green tinge. Acacia, white flowers, hazelnut, lemon, a flinty note and sometimes warm croissant. '
            'A round, lasting palate with mouth-watering liveliness. A small cool valley opening to the north at the end of the '
            'Côte Chalonnaise: the only Burgundy village appellation that has no interest in Chardonnay.',
         why=('« Seule appellation communale élaborée à partir du cépage aligoté » (cahier des charges).',
              '“The only communal appellation made from Aligoté” (rulebook).')),
    dict(id='rully-b', aoc='Rully', alias=[], zone='chalonnais', col=WHITE, grapes=CH,
         fr='Robe or pâle. Fleurs blanches, poire, une touche de noisette. Bouche fraîche, fruitée, à boire dans ses premières années. '
            'Village de la Côte chalonnaise où l’on a commencé, au XIX<sup>e</sup> siècle, à faire mousser les vins de Bourgogne : '
            'on y voit le berceau du crémant de la région.',
         en='Pale gold. White flowers, pear, a touch of hazelnut. Fresh, fruity palate, to drink in its first years. A Côte '
            'Chalonnaise village where, in the 19th century, Burgundy wines were first made sparkling: it is seen as the cradle '
            'of the region’s crémant.',
         why=('Rully, berceau des vins mousseux de Bourgogne au XIXe siècle ; le village a aussi une AOC communale en blanc et en rouge.',
              'Rully, cradle of Burgundy sparkling wine in the 19th century; the village also has its own still white and red AOC.')),
    dict(id='mercurey-r', aoc='Mercurey', alias=[], zone='chalonnais', col=RED, grapes=PN,
         fr='Robe rubis soutenu. Cerise noire, fraise des bois, une note de sous-bois. Bouche charpentée pour la région, tanins '
            'présents, belle fraîcheur. La plus grande appellation de la Côte chalonnaise, surtout rouge, dont le nom rappellerait '
            'un temple romain dédié au dieu du commerce.',
         en='Deep ruby. Black cherry, wild strawberry, an undergrowth note. Fairly structured for the area, present tannins, good '
            'freshness. The largest appellation of the Côte Chalonnaise, mostly red, whose name is said to recall a Roman temple '
            'to the god of trade.',
         why=('Plus vaste appellation de la Côte chalonnaise ; nom traditionnellement rattaché à Mercure.',
              'The largest appellation of the Côte Chalonnaise; its name is traditionally linked to Mercury.')),
    dict(id='givry-r', aoc='Givry', alias=[], zone='chalonnais', col=RED, grapes=PN,
         fr='Robe rubis. Fruits rouges, puis des notes épicées et animales. Bouche fine, souple, tanins présents mais soyeux. Coteaux '
            'tournés vers le soleil levant, à l’abri des brouillards de la plaine de la Saône ; la légende en fait le vin préféré '
            'du roi Henri IV.',
         en='Ruby. Red fruit, then spicy and animal notes. A fine, supple palate, present but silky tannins. Slopes facing the '
            'rising sun, out of the Saône plain’s mists; legend makes it King Henri IV’s favourite wine.',
         why=('« Fins, souples, tanins soyeux… notes épicées et animales » (cahier des charges) ; Givry et Henri IV, une légende tenace.',
              '“Fine, supple, silky tannins… spicy and animal notes” (rulebook); Givry and Henri IV, a stubborn legend.')),
    dict(id='montagny-b', aoc='Montagny', alias=[], zone='chalonnais', col=WHITE, grapes=CH,
         fr='Robe or vert. Fleurs blanches, agrumes, noisette fraîche. Bouche vive et tendue. Au sud de la Côte chalonnaise, autour de '
            'Buxy : la seule appellation de la Côte chalonnaise vouée au seul chardonnay — et qui compte des dizaines de premiers crus.',
         en='Green-gold. White flowers, citrus, fresh hazelnut. Lively, taut palate. In the south of the Côte Chalonnaise, around '
            'Buxy: the only Côte Chalonnaise appellation devoted to Chardonnay alone — with dozens of premiers crus.',
         why=('Montagny : chardonnay seulement (Bouzeron, l’autre AOC 100 % blanche du secteur, est en aligoté), quatre communes autour de Buxy.',
              'Montagny: Chardonnay only (Bouzeron, the area’s other all-white AOC, is Aligoté), four communes around Buxy.')),
    # ------------------------------------------------------------------ Côte de Nuits
    dict(id='marsannay-rs', aoc='Marsannay', alias=[], zone='nuits', col=('Rosé', 'Rosé'), grapes=PN,
         fr='Robe saumonée. Groseille, framboise, pêche de vigne. Bouche fraîche, fruitée, avec une petite mâche. Aux portes de Dijon, '
            'à l’extrémité nord de la Côte de Nuits : le seul village de la Côte d’Or dont l’appellation communale peut être '
            'revendiquée en rosé.',
         en='Salmon pink. Redcurrant, raspberry, vine peach. A fresh, fruity palate with a little grip. At the gates of Dijon, '
            'at the northern tip of the Côte de Nuits: the only Côte d’Or village whose communal appellation can be made as a rosé.',
         why=('Marsannay est la seule appellation communale de la Côte d’Or produite en rouge, blanc… et rosé.',
              'Marsannay is the only Côte d’Or communal appellation made in red, white… and rosé.')),
    dict(id='gevrey-r', aoc='Gevrey-Chambertin', alias=['Gevrey'], zone='nuits', col=RED, grapes=PN,
         fr='Robe rubis profond. Cerise noire, mûre, réglisse, puis cuir et sous-bois. Bouche puissante, charpentée, tanins serrés : '
            'un pinot de garde. Le village détient à lui seul neuf grands crus, dont celui que Napoléon aurait coupé d’eau '
            'pendant ses campagnes.',
         en='Deep ruby. Black cherry, blackberry, liquorice, then leather and undergrowth. Powerful, structured palate, tight '
            'tannins: a Pinot for keeping. The village holds nine grands crus on its own, including the one Napoleon is said to '
            'have drunk, diluted with water, on campaign.',
         why=('Neuf grands crus (Chambertin, Clos de Bèze, Chapelle, Charmes, Griotte, Latricières, Mazis, Mazoyères, Ruchottes) : record de Bourgogne.',
              'Nine grands crus (Chambertin, Clos de Bèze, Chapelle, Charmes, Griotte, Latricières, Mazis, Mazoyères, Ruchottes): a Burgundy record.')),
    dict(id='morey-r', aoc='Morey-Saint-Denis', alias=['Morey'], zone='nuits', col=RED, grapes=PN,
         fr='Robe rubis sombre. Fruits noirs, violette, une touche de terre et d’épices. Bouche entre la puissance de son voisin du '
            'nord et la finesse de celui du sud. Petit village coincé entre deux célébrités, qui compte cinq grands crus, dont '
            'deux « clos » chacun aux mains d’un seul propriétaire.',
         en='Dark ruby. Black fruit, violet, a touch of earth and spice. A palate between the power of its northern neighbour '
            'and the finesse of its southern one. A small village squeezed between two celebrities, with five grands crus, two '
            'of them walled “clos” each owned by a single estate.',
         why=('Clos de la Roche, Clos Saint-Denis, Clos des Lambrays, Clos de Tart (ces deux derniers quasi monopoles) et une part de Bonnes-Mares.',
              'Clos de la Roche, Clos Saint-Denis, Clos des Lambrays, Clos de Tart (the last two near-monopoles) and part of Bonnes-Mares.')),
    dict(id='chambolle-r', aoc='Chambolle-Musigny', alias=['Chambolle'], zone='nuits', col=RED, grapes=PN,
         fr='Robe rubis clair et brillant. Framboise, violette, rose, une grande délicatesse. Bouche soyeuse, aérienne, tanins de '
            'velours : on parle du plus « féminin » des vins de la Côte de Nuits. Sols calcaires légers et caillouteux, entre deux '
            'grands crus, dont un qui donne aussi un rarissime vin blanc.',
         en='Light, bright ruby. Raspberry, violet, rose, great delicacy. Silky, airy palate, velvet tannins: it is called the most '
            '“feminine” of the Côte de Nuits wines. Light, stony limestone soils between two grands crus, one of which also makes '
            'a very rare white.',
         why=('Chambolle : Musigny (qui existe aussi en blanc) et Bonnes-Mares ; réputation de finesse et de dentelle.',
              'Chambolle: Musigny (which also exists in white) and Bonnes-Mares; renowned for finesse and lace.')),
    dict(id='clos-vougeot-r', aoc='Clos de Vougeot', alias=['Clos Vougeot', 'Vougeot'], zone='nuits', col=RED, grapes=PN,
         fr='Robe rouge profond. Cerise, mûre, cassis, sous-bois et violette, d’une intensité aromatique remarquable. Bouche ample, '
            'charnue, tanins fins, longue garde. Un enclos d’une cinquantaine d’hectares ceint de murs par des moines cisterciens, '
            'resté d’un seul tenant jusqu’en 1889, aujourd’hui partagé entre quelque 80 propriétaires.',
         en='Deep red. Cherry, blackberry, blackcurrant, undergrowth and violet, with remarkable aromatic intensity. Ample, fleshy '
            'palate, fine tannins, long ageing. A walled enclosure of some fifty hectares built by Cistercian monks, kept whole '
            'until 1889, now shared by some 80 owners.',
         why=('« Site entouré de murs », « divisé seulement depuis 1889 » (cahier des charges) : le clos des moines de Cîteaux.',
              '“A site surrounded by walls”, “divided only since 1889” (rulebook): the Cîteaux monks’ clos.')),
    dict(id='vosne-r', aoc='Vosne-Romanée', alias=['Vosne-Romanee', 'Vosne'], zone='nuits', col=RED, grapes=PN,
         fr='Robe rubis profond. Cerise noire, rose fanée, épices orientales, une note de sous-bois. Bouche veloutée, à la fois riche '
            'et aérienne, finale interminable. Le village des grands crus les plus célèbres du monde ; un abbé du XVIII<sup>e</sup> '
            'siècle écrivait qu’on n’y trouve « point de vins communs ».',
         en='Deep ruby. Black cherry, faded rose, oriental spices, a hint of undergrowth. Velvety palate, rich yet airy, an endless '
            'finish. The village of the world’s most famous grands crus; an 18th-century abbé wrote that it held “no common wines”.',
         why=('Romanée-Conti, La Tâche, Richebourg… et la phrase de l’abbé Courtépée : « Il n’y a point de vins communs à Vosne ».',
              'Romanée-Conti, La Tâche, Richebourg… and Abbé Courtépée’s line: “There are no common wines in Vosne”.')),
    dict(id='nuits-r', aoc='Nuits-Saint-Georges', alias=['Nuits Saint Georges', 'Nuits'], zone='nuits', col=RED, grapes=PN,
         fr='Robe sombre. Fruits noirs, cuir, terre, gibier avec l’âge. Bouche ferme et tannique, un pinot de caractère qui demande '
            'du temps. La petite ville qui a donné son nom à toute la côte nord, riche de dizaines de premiers crus… mais sans '
            'un seul grand cru.',
         en='Dark. Black fruit, leather, earth, game with age. Firm, tannic palate, a Pinot of character that needs time. The little '
            'town that gave its name to the whole northern côte, rich in dozens of premiers crus… but without a single grand cru.',
         why=('Nuits-Saint-Georges a donné son nom à la Côte de Nuits ; 41 premiers crus (avec Premeaux) mais aucun grand cru.',
              'Nuits-Saint-Georges gave its name to the Côte de Nuits; 41 premiers crus (with Premeaux) but no grand cru.')),
    dict(id='musigny-b', aoc='Musigny', alias=['Musigny blanc'], zone='nuits', col=WHITE, grapes=CH,
         fr='Robe or pâle. Fleurs blanches, agrumes, amande, une profondeur minérale. Bouche dense et vibrante. Une rareté absolue : '
            'quelques centaines de bouteilles par an, le seul grand cru blanc de la Côte de Nuits, né au cœur d’un grand cru '
            'surtout célèbre pour ses rouges.',
         en='Pale gold. White flowers, citrus, almond, mineral depth. Dense, vibrant palate. An absolute rarity: a few hundred bottles '
            'a year, the only white grand cru of the Côte de Nuits, born in the heart of a grand cru mostly famous for its reds.',
         why=('Le Musigny blanc est le seul grand cru blanc de la Côte de Nuits.', 'Musigny blanc is the only white grand cru of the Côte de Nuits.')),
    # ------------------------------------------------------------------ Côte de Beaune
    dict(id='corton-r', aoc='Corton', alias=['Corton Grand Cru'], zone='beaune', col=RED, grapes=PN,
         fr='Robe grenat profond. Fruits noirs, épices, une note ferreuse. Bouche charpentée, tanins fermes, longue garde. Une colline '
            'boisée en forme de dôme au nord de Beaune ; c’est le seul grand cru rouge de toute la Côte de Beaune.',
         en='Deep garnet. Black fruit, spice, an iron note. A structured palate, firm tannins, long ageing. A dome-shaped wooded hill '
            'north of Beaune; it is the only red grand cru of the whole Côte de Beaune.',
         why=('Corton, seul grand cru rouge de la Côte de Beaune, sur la colline de Corton (Aloxe, Ladoix, Pernand).',
              'Corton, the only red grand cru of the Côte de Beaune, on the hill of Corton (Aloxe, Ladoix, Pernand).')),
    dict(id='corton-charlemagne-b', aoc='Corton-Charlemagne', alias=['Corton Charlemagne'], zone='beaune', col=WHITE, grapes=CH,
         fr='Robe or. Pomme cuite, cannelle, beurre, silex, une puissance minérale. Bouche ample, droite, très longue ; il se referme '
            'quelques années avant de s’épanouir. Sur le haut d’une colline boisée ; la légende veut qu’un empereur à barbe blanche '
            'y ait fait planter du blanc pour ne plus tacher sa barbe de vin rouge.',
         en='Gold. Baked apple, cinnamon, butter, flint, mineral power. Ample, straight, very long palate; it closes up for a few '
            'years before opening. High on a wooded hill; legend has it that an emperor with a white beard had white grapes '
            'planted there so as not to stain his beard with red wine.',
         why=('Charlemagne et sa barbe : la légende du grand cru blanc de la colline de Corton.',
              'Charlemagne and his beard: the legend of the white grand cru on the hill of Corton.')),
    dict(id='beaune-r', aoc='Beaune', alias=[], zone='beaune', col=RED, grapes=PN,
         fr='Robe rubis. Fraise, cerise, une touche épicée. Bouche ronde, charmeuse, tanins fondus. La capitale du vin de Bourgogne, '
            'riche de premiers crus mais sans grand cru, où se tient chaque novembre depuis le XIX<sup>e</sup> siècle une vente '
            'aux enchères de charité devenue mondiale.',
         en='Ruby. Strawberry, cherry, a spicy touch. Round, charming palate, soft tannins. The capital of Burgundy wine, rich in '
            'premiers crus but without a grand cru, where a charity auction, now world-famous, has been held every November '
            'since the 19th century.',
         why=('La vente des Hospices de Beaune (depuis 1859), le troisième week-end de novembre.',
              'The Hospices de Beaune auction (since 1859), on the third weekend of November.')),
    dict(id='pommard-r', aoc='Pommard', alias=[], zone='beaune', col=RED, grapes=PN,
         fr='Robe rubis sombre. Fruits noirs, cerise à l’eau-de-vie, cuir, une note ferrugineuse. Bouche charpentée, tanins fermes : '
            'le plus robuste des rouges de la Côte de Beaune, qui ne produit d’ailleurs que du rouge. Ses deux premiers crus les '
            'plus réputés s’appellent les Rugiens — pour la couleur rouille de leur terre — et les Épenots.',
         en='Dark ruby. Black fruit, brandied cherry, leather, an iron note. Structured palate, firm tannins: the sturdiest red of '
            'the Côte de Beaune, which in fact makes nothing but red. Its two most famous premiers crus are Les Rugiens — named for '
            'the rusty colour of their soil — and Les Épenots.',
         why=('Pommard : uniquement du rouge, réputation de puissance ; premiers crus Rugiens (terre rouge) et Épenots.',
              'Pommard: red only, known for power; premiers crus Rugiens (red soil) and Épenots.')),
    dict(id='volnay-r', aoc='Volnay', alias=[], zone='beaune', col=RED, grapes=PN,
         fr='Robe rubis. Framboise, violette, cerise, puis épices et gibier avec l’âge. Bouche d’une grande finesse, charpente '
            'tannique équilibrée par une acidité discrète. Le plus élégant des rouges de la Côte de Beaune, qui fut le vin des ducs '
            'de Bourgogne ; certains de ses premiers crus poussent en fait sur la commune voisine, célèbre pour ses blancs.',
         en='Ruby. Raspberry, violet, cherry, then spice and game with age. A palate of great finesse, tannic frame balanced by '
            'discreet acidity. The most elegant red of the Côte de Beaune, once the wine of the Dukes of Burgundy; some of its '
            'premiers crus actually grow in the neighbouring commune, famous for its whites.',
         why=('Aire sur Volnay et Meursault (Volnay-Santenots), « héritage des ducs de Bourgogne » (cahier des charges).',
              'Area covering Volnay and Meursault (Volnay-Santenots), “heritage of the Dukes of Burgundy” (rulebook).')),
    dict(id='meursault-b', aoc='Meursault', alias=[], zone='beaune', col=WHITE, grapes=CH,
         fr='Robe or soutenu. Noisette grillée, beurre frais, brioche, fleurs jaunes. Bouche ronde, grasse, opulente, avec une belle '
            'fraîcheur en finale. Grand village de blancs sans grand cru, mais avec des premiers crus célèbres comme les Perrières '
            'ou les Charmes ; chaque novembre, on y fête la fin des vendanges par un célèbre déjeuner où chacun apporte ses '
            'bouteilles.',
         en='Deep gold. Toasted hazelnut, fresh butter, brioche, yellow flowers. Round, rich, opulent palate with good freshness on '
            'the finish. A great white-wine village without a grand cru, but with famous premiers crus such as Perrières and '
            'Charmes; every November it celebrates the end of harvest with a famous lunch where everyone brings their own bottles.',
         why=('La Paulée de Meursault ; style noisette-beurre ; aucun grand cru, mais des premiers crus réputés.',
              'The Paulée de Meursault; hazelnut-butter style; no grand cru, but famous premiers crus.')),
    dict(id='puligny-b', aoc='Puligny-Montrachet', alias=['Puligny'], zone='beaune', col=WHITE, grapes=CH,
         fr='Robe or pâle. Fleurs blanches, citron, amande, une pointe de miel. Bouche ciselée, tendue, d’une élégance rare. Village '
            'de grands blancs qui partage le plus célèbre grand cru blanc avec son voisin ; la nappe phréatique y est si haute '
            'qu’on n’y creuse guère de caves souterraines.',
         en='Pale gold. White flowers, lemon, almond, a hint of honey. A chiselled, taut palate of rare elegance. A village of great '
            'whites that shares the most famous white grand cru with its neighbour; the water table is so high that underground '
            'cellars are hardly dug here.',
         why=('Puligny : Montrachet, Chevalier, Bâtard, Bienvenues ; caves en surface à cause de la nappe phréatique.',
              'Puligny: Montrachet, Chevalier, Bâtard, Bienvenues; above-ground cellars because of the water table.')),
    dict(id='chassagne-r', aoc='Chassagne-Montrachet', alias=['Chassagne'], zone='beaune', col=RED, grapes=PN,
         fr='Robe rubis. Cerise, fraise, une touche de terre et d’épices. Bouche ronde, assez charpentée. Surprise : ce village, '
            'connu pour ses grands blancs et pour ses carrières d’une pierre qui imite le marbre, a longtemps produit davantage '
            'de rouge que de blanc.',
         en='Ruby. Cherry, strawberry, a touch of earth and spice. Round, fairly structured palate. Surprise: this village, known '
            'for its great whites and for its quarries of a marble-like stone, long produced more red than white.',
         why=('Chassagne (Montrachet, Bâtard, Criots) : longtemps majoritairement rouge ; célèbres carrières de « pierre de Chassagne ».',
              'Chassagne (Montrachet, Bâtard, Criots): long mainly red; famous quarries of “Chassagne stone”.')),
    dict(id='montrachet-b', aoc='Montrachet', alias=['Le Montrachet'], zone='beaune', col=WHITE, grapes=CH,
         fr='Robe or. Nez immense : agrumes confits, miel, noisette, beurre, fleurs, silex. Bouche d’une densité et d’une longueur '
            'inouïes, à garder vingt ans. Huit hectares à cheval sur deux communes ; une phrase attribuée à Alexandre Dumas dit '
            'qu’il faut le boire à genoux et tête découverte.',
         en='Gold. An immense nose: candied citrus, honey, hazelnut, butter, flowers, flint. A palate of unheard-of density and '
            'length, to keep twenty years. Eight hectares straddling two communes; a line attributed to Alexandre Dumas says it '
            'should be drunk kneeling, with head bared.',
         why=('Le grand cru blanc le plus célèbre, partagé entre Puligny et Chassagne ; la citation « à genoux » figure sur notre page de citations.',
              'The most famous white grand cru, shared by Puligny and Chassagne; the “kneeling” quotation is on our quotations page.')),
    dict(id='santenay-r', aoc='Santenay', alias=[], zone='beaune', col=RED, grapes=PN,
         fr='Robe rubis soutenu. Fruits rouges et noirs, une touche terreuse. Bouche franche, assez tannique. Dernier grand village '
            'de la Côte de Beaune avant la Saône-et-Loire, connu aussi pour ses sources thermales et son casino.',
         en='Deep ruby. Red and black fruit, an earthy touch. Frank, fairly tannic palate. The last big village of the Côte de Beaune '
            'before Saône-et-Loire, also known for its thermal springs and its casino.',
         why=('Santenay, village thermal (source Carnot) avec un casino, au sud de la Côte de Beaune.',
              'Santenay, a spa village (Carnot spring) with a casino, at the southern end of the Côte de Beaune.')),
    dict(id='maranges-r', aoc='Maranges', alias=[], zone='beaune', col=RED, grapes=PN,
         fr='Robe rubis sombre. Cerise, mûre, une note réglissée. Bouche rustique et généreuse, tanins présents. La toute dernière '
            'appellation de village de la Côte de Beaune, réunissant trois villages qui portent tous le même suffixe — et '
            'qui se trouvent déjà en Saône-et-Loire, au-delà de la limite de la Côte-d’Or.',
         en='Dark ruby. Cherry, blackberry, a liquorice note. Rustic, generous palate, present tannins. The very last village '
            'appellation of the Côte de Beaune, bringing together three villages sharing the same suffix — already in '
            'Saône-et-Loire, beyond the Côte-d’Or border.',
         why=('Cheilly-, Dezize- et Sampigny-lès-Maranges, en Saône-et-Loire : l’extrémité sud de la Côte de Beaune.',
              'Cheilly-, Dezize- and Sampigny-lès-Maranges, in Saône-et-Loire: the southern tip of the Côte de Beaune.')),
    # ------------------------------------------------------------------ Mâconnais
    dict(id='pouilly-fuisse-b', aoc='Pouilly-Fuissé', alias=['Pouilly Fuisse'], zone='maconnais', col=WHITE, grapes=CH,
         fr='Robe or vert. Fleurs blanches et agrumes, puis noisette, amande grillée, vanille et pierre à fusil. Bouche pleine et riche, '
            'puissance et élégance. Vignes au pied de deux spectaculaires roches calcaires, Solutré et Vergisson ; depuis 2020, '
            'l’appellation compte 22 premiers crus, une première dans le Mâconnais.',
         en='Green-gold. White flowers and citrus, then hazelnut, toasted almond, vanilla and flint. Full, rich palate, power and '
            'elegance. Vines beneath two spectacular limestone rocks, Solutré and Vergisson; since 2020 it has 22 premiers crus, '
            'a first in the Mâconnais.',
         why=('Roches de Solutré et de Vergisson ; premiers crus reconnus en 2020 ; « pierre à fusil » (cahier des charges).',
              'The Solutré and Vergisson rocks; premiers crus recognised in 2020; “flint” (rulebook).')),
    dict(id='saint-veran-b', aoc='Saint-Véran', alias=['Saint-Veran', 'St-Véran'], zone='maconnais', col=WHITE, grapes=CH,
         fr='Robe or vert. Fleurs blanches, fruits à chair blanche, puis noisette, amande grillée, une touche de miel. Bouche ample, '
            'équilibrée. Appellation du sud du Mâconnais qui s’étend de part et d’autre d’un voisin plus célèbre, et qui porte le nom d’un village… '
            'auquel elle a retiré sa dernière lettre.',
         en='Green-gold. White flowers, white-fleshed fruit, then hazelnut, toasted almond, a touch of honey. Ample, balanced palate. '
            'A southern Mâconnais appellation lying on both sides of a more famous neighbour, named after a village… minus its last letter.',
         why=('Le village s’appelle Saint-Vérand (avec un d), l’appellation Saint-Véran ; elle se trouve au nord et au sud de Pouilly-Fuissé.',
              'The village is Saint-Vérand (with a d), the appellation Saint-Véran; it lies north and south of Pouilly-Fuissé.')),
    dict(id='vire-clesse-b', aoc='Viré-Clessé', alias=['Vire-Clesse'], zone='maconnais', col=WHITE, grapes=CH,
         fr='Robe or vert. Fleurs blanches et jaunes, fruits secs, note minérale. Bouche franche, souple, longue. Deux villages du nord '
            'du Mâconnais réunis en une appellation dont le règlement autorise aussi, dans certains secteurs, un vin demi-sec issu '
            'de raisins surmûris.',
         en='Green-gold. White and yellow flowers, dried fruit, a mineral note. Frank, supple, long palate. Two northern Mâconnais '
            'villages joined in one appellation whose rules also allow, in some spots, a medium-dry wine from overripe grapes.',
         why=('Le cahier des charges de Viré-Clessé prévoit un « vin demi-sec » issu de raisins surmûris.',
              'The Viré-Clessé rulebook provides for a “medium-dry wine” from overripe grapes.')),
    # ------------------------------------------------------------------ regional
    dict(id='ptg-r', aoc='Bourgogne Passe-Tout-Grains', alias=['Passe-Tout-Grains', 'Passetoutgrain'], zone='bregional', col=RED,
         grapes=('Pinot noir et gamay', 'Pinot Noir and Gamay'),
         fr='Robe rubis vif. Cerise, framboise, une pointe poivrée. Bouche légère, gouleyante, tanins souples : un rouge de bistrot. '
            'Son nom dit tout : deux cépages rouges de la région vinifiés ensemble, l’un apportant la finesse, l’autre le fruit.',
         en='Bright ruby. Cherry, raspberry, a peppery hint. Light, easy-drinking palate, soft tannins: a bistro red. Its name says '
            'it all: the region’s two red grapes fermented together, one bringing finesse, the other fruit.',
         why=('« Passe-tout-grains » : pinot noir et gamay vinifiés ensemble.', '“Passe-tout-grains”: Pinot Noir and Gamay fermented together.')),
    dict(id='cremant-bgy', aoc='Crémant de Bourgogne', alias=['Cremant de Bourgogne'], zone='bregional',
         col=('Blanc effervescent', 'Sparkling white'), grapes=('Chardonnay et pinot noir surtout', 'Mainly Chardonnay and Pinot Noir'),
         fr='Robe or pâle, bulles fines. Pomme, agrumes, brioche après un long séjour sur lies. Bouche fraîche et crémeuse. Méthode '
            'traditionnelle, chardonnay et pinot noir comme en Champagne voisine ; ses cuvées vieillies au moins deux et trois ans '
            'peuvent porter les mentions « Éminent » et « Grand Éminent ».',
         en='Pale gold, fine bubbles. Apple, citrus, brioche after long ageing on the lees. Fresh, creamy palate. Traditional method, '
            'Chardonnay and Pinot Noir as in neighbouring Champagne; cuvées aged at least two and three years may be labelled '
            '“Éminent” and “Grand Éminent”.',
         why=('Les mentions « Éminent » (24 mois) et « Grand Éminent » (36 mois) sont propres au crémant de Bourgogne.',
              'The “Éminent” (24 months) and “Grand Éminent” (36 months) mentions are specific to Crémant de Bourgogne.')),
]
