"""Beaujolais batch for « Goûtez votre savoir » (see tasting_notes.py for the field list).

CDC « lien à l'origine » filled in for Beaujolais (geography), Brouilly, Régnié and Coteaux du Lyonnais only;
the 2010 rulebooks of the other crus leave it empty → established facts, flagged in the review sheet.
"""

ZONES_BJL = {
    'bjl_crus': ('Beaujolais · les dix crus (nord, granite)', 'Beaujolais · the ten crus (north, granite)'),
    'bjl_reg': ('Beaujolais · Beaujolais & Beaujolais-Villages', 'Beaujolais · Beaujolais & Beaujolais-Villages'),
    'lyonnais': ('Beaujolais · Coteaux du Lyonnais', 'Beaujolais · Coteaux du Lyonnais'),
}
AOC_ZONE_BJL = {a: 'bjl_crus' for a in ('Brouilly', 'Côte de Brouilly', 'Chénas', 'Chiroubles', 'Fleurie', 'Juliénas',
                                       'Morgon', 'Moulin-à-Vent', 'Régnié', 'Saint-Amour')}
AOC_ZONE_BJL.update({'Beaujolais': 'bjl_reg', 'Beaujolais-Villages': 'bjl_reg', 'Coteaux du Lyonnais': 'lyonnais'})

RED = ('Rouge tranquille sec', 'Still dry red')
GAM = ('Gamay', 'Gamay')

NOTES_BJL = [
    dict(id='bjl-nouveau', aoc='Beaujolais', alias=['Beaujolais Nouveau', 'Beaujolais Primeur'], zone='bjl_reg',
         col=('Rouge primeur', 'Red, primeur'), grapes=GAM,
         fr='Robe violacée, presque fluo. Nez explosif de bonbon anglais, de banane, de fraise et de framboise. Bouche légère, '
            'désaltérante, tanins quasi absents : à boire frais et vite. Mis en bouteille quelques semaines après la vendange, '
            'il est attendu dans le monde entier le troisième jeudi de novembre.',
         en='Violet, almost neon. An explosive nose of pear drops, banana, strawberry and raspberry. Light, thirst-quenching, '
            'almost tannin-free: drink it cool and quickly. Bottled a few weeks after harvest, it is awaited worldwide on the '
            'third Thursday of November.',
         why=('Le Beaujolais Nouveau (primeur), mis en vente le troisième jeudi de novembre ; arômes de macération carbonique.',
              'Beaujolais Nouveau (primeur), released on the third Thursday of November; carbonic-maceration aromas.')),
    dict(id='bjl-r', aoc='Beaujolais', alias=[], zone='bjl_reg', col=RED, grapes=GAM,
         fr='Robe rubis vif. Cerise, groseille, une touche florale. Bouche souple et fruitée, tanins légers. Il vient surtout du sud '
            'de la région, entre Villefranche et Lyon, où les villages sont bâtis d’un calcaire ocre qui dore au soleil couchant — '
            'le « pays des Pierres Dorées ».',
         en='Bright ruby. Cherry, redcurrant, a floral touch. Supple, fruity palate, light tannins. It comes mostly from the south '
            'of the region, between Villefranche and Lyon, where villages are built of an ochre limestone that glows at sunset — '
            'the “land of Golden Stones”.',
         why=('Le sud calcaire du Beaujolais, « pays des Pierres Dorées » ; l’aire couvre 85 communes du Rhône et 11 de Saône-et-Loire (cahier des charges).',
              'The limestone south of the Beaujolais, the “Pierres Dorées”; the area covers 85 communes in the Rhône and 11 in Saône-et-Loire (rulebook).')),
    dict(id='bjl-villages-r', aoc='Beaujolais-Villages', alias=['Beaujolais Villages'], zone='bjl_reg', col=RED, grapes=GAM,
         fr='Robe rubis violacé. Fruits rouges croquants, pivoine, une pointe poivrée. Bouche plus dense et plus structurée qu’un '
            'beaujolais simple. Il provient de la moitié nord de la région, sur des sols de granite, de 38 communes que l’on '
            'a le droit d’accoler à son nom.',
         en='Purplish ruby. Crunchy red fruit, peony, a peppery hint. Denser and more structured than plain Beaujolais. It comes '
            'from the northern half of the region, on granite soils, from 38 communes whose name may be added to its own.',
         why=('Mention « Villages » : 30 communes du Rhône et 8 de Saône-et-Loire, dans la moitié nord (cahier des charges).',
              'The “Villages” mention: 30 communes in the Rhône and 8 in Saône-et-Loire, in the northern half (rulebook).')),
    dict(id='saint-amour-r', aoc='Saint-Amour', alias=['Saint Amour'], zone='bjl_crus', col=RED, grapes=GAM,
         fr='Robe rubis. Pêche de vigne, framboise, une note épicée. Bouche tendre et charmeuse. Le cru le plus septentrional, '
            'le seul situé entièrement en Saône-et-Loire, à la frontière du Mâconnais ; son nom en fait le vin de toutes les '
            'Saint-Valentin.',
         en='Ruby. Vine peach, raspberry, a spicy note. Tender, charming palate. The northernmost cru, the only one entirely in '
            'Saône-et-Loire, on the border of the Mâconnais; its name makes it the wine of every Valentine’s Day.',
         why=('Saint-Amour-Bellevue : cru le plus au nord, entièrement en Saône-et-Loire ; succès de la Saint-Valentin.',
              'Saint-Amour-Bellevue: the northernmost cru, entirely in Saône-et-Loire; a Valentine’s Day favourite.')),
    dict(id='julienas-r', aoc='Juliénas', alias=['Julienas'], zone='bjl_crus', col=RED, grapes=GAM,
         fr='Robe grenat. Fruits rouges, pivoine, une touche épicée. Bouche charnue, assez charpentée. Le village devrait son nom à '
            'Jules César ; on y déguste les vins dans une église désaffectée transformée en cellier.',
         en='Garnet. Red fruit, peony, a spicy touch. Fleshy, fairly structured palate. The village is said to take its name from '
            'Julius Caesar; wines are tasted there in a deconsecrated church turned into a cellar.',
         why=('Juliénas et Jules César (tradition) ; le Cellier de la Vieille Église.',
              'Juliénas and Julius Caesar (tradition); the Cellier de la Vieille Église.')),
    dict(id='chenas-r', aoc='Chénas', alias=['Chenas'], zone='bjl_crus', col=RED, grapes=GAM,
         fr='Robe rubis profond. Pivoine, rose, fruits rouges, parfois une note boisée. Bouche ronde et structurée. Le plus petit des '
            'crus, dont le nom rappelle la forêt de grands arbres qui couvrait autrefois ses coteaux.',
         en='Deep ruby. Peony, rose, red fruit, sometimes a woody note. Round, structured palate. The smallest of the crus, whose name '
            'recalls the forest of great trees that once covered its slopes.',
         why=('Chénas, de « chêne » ; le plus petit des dix crus.', 'Chénas, from “chêne” (oak); the smallest of the ten crus.')),
    dict(id='moulin-a-vent-r', aoc='Moulin-à-Vent', alias=['Moulin a Vent'], zone='bjl_crus', col=RED, grapes=GAM,
         fr='Robe grenat soutenu. Cerise noire, iris, épices, puis des notes de sous-bois qui rappellent la Bourgogne voisine. '
            'Bouche puissante, tanins fermes : le cru de plus longue garde. Il porte le nom d’un vieux bâtiment monument historique '
            'qui domine le vignoble — il n’existe aucune commune de ce nom.',
         en='Deep garnet. Black cherry, iris, spice, then undergrowth notes recalling neighbouring Burgundy. Powerful palate, firm '
            'tannins: the longest-lived cru. It is named after an old listed building overlooking the vineyard — there is no '
            'village of that name.',
         why=('Le moulin de Romanèche-Thorins (monument historique) ; le « roi du Beaujolais », réputé pour sa garde.',
              'The windmill at Romanèche-Thorins (listed monument); the “king of Beaujolais”, famous for ageing.')),
    dict(id='fleurie-r', aoc='Fleurie', alias=[], zone='bjl_crus', col=RED, grapes=GAM,
         fr='Robe rubis brillant. Iris, violette, rose, fruits rouges : le plus parfumé des crus. Bouche soyeuse et élégante. Granite '
            'rose et une chapelle dédiée à la Vierge au sommet de la colline ; on la surnomme « la reine du Beaujolais ».',
         en='Bright ruby. Iris, violet, rose, red fruit: the most fragrant of the crus. Silky, elegant palate. Pink granite and a '
            'chapel to the Virgin on the hilltop; it is nicknamed “the queen of Beaujolais”.',
         why=('Fleurie, la « reine du Beaujolais » : granite rose, chapelle de la Madone.', 'Fleurie, “queen of Beaujolais”: pink granite, the Madone chapel.')),
    dict(id='chiroubles-r', aoc='Chiroubles', alias=[], zone='bjl_crus', col=RED, grapes=GAM,
         fr='Robe rubis clair. Violette, muguet, framboise. Bouche légère, fraîche et vive, à boire dans sa jeunesse. Le cru perché '
            'le plus haut, sur des pentes raides de granite tourné vers le soleil levant.',
         en='Light ruby. Violet, lily of the valley, raspberry. Light, fresh, lively palate, best young. The highest of the crus, '
            'on steep granite slopes facing the rising sun.',
         why=('Chiroubles, le plus élevé des crus (jusqu’à environ 450 m).', 'Chiroubles, the highest cru (up to about 450 m).')),
    dict(id='morgon-r', aoc='Morgon', alias=[], zone='bjl_crus', col=RED, grapes=GAM,
         fr='Robe grenat foncé. Cerise noire, kirsch, une note minérale. Bouche charnue et puissante, qui évolue vers des arômes de '
            'noyau ; on dit alors que le vin « morgonne ». Son climat le plus célèbre, la Côte du Py, repose sur une roche bleue '
            'friable que les vignerons appellent « roche pourrie ».',
         en='Dark garnet. Black cherry, kirsch, a mineral note. Fleshy, powerful palate, evolving towards stone-fruit aromas; the '
            'wine is then said to “morgonner”. Its most famous climat, the Côte du Py, sits on a crumbly blue rock that growers '
            'call “rotten rock”.',
         why=('Le verbe « morgonner » et la Côte du Py, sur schistes altérés (« roche pourrie »).', 'The verb “morgonner” and the Côte du Py, on decomposed schist (“roche pourrie”).')),
    dict(id='regnie-r', aoc='Régnié', alias=['Regnie'], zone='bjl_crus', col=RED, grapes=GAM,
         fr='Robe rouge violacé qui tire vers le grenat. Fleurs et fruits rouges, puis des nuances épicées. Attaque franche, finesse, '
            'grande souplesse, très fruité. Sables de granite au pied d’un sommet de 842 m ; c’est le plus jeune des dix crus, '
            'reconnu en 1988, et son église a deux clochers.',
         en='Purplish red turning garnet. Flowers and red fruit, then spicy hints. A frank attack, finesse, great suppleness, very '
            'fruity. Granite sands below an 842 m summit; it is the youngest of the ten crus, recognised in 1988, and its church '
            'has twin bell towers.',
         why=('Régnié, dixième cru (1988) ; « fût d’Avenas, 842 m », arènes granitiques (cahier des charges).',
              'Régnié, the tenth cru (1988); “Fût d’Avenas, 842 m”, granite sands (rulebook).')),
    dict(id='brouilly-r', aoc='Brouilly', alias=[], zone='bjl_crus', col=RED, grapes=GAM,
         fr='Robe rubis, plus violacée sur granite. Fruits rouges dominants. Bouche souple, charnue, fine : on le dit le plus tendre '
            'des crus. C’est aussi le plus vaste ; il fait le tour d’une petite montagne isolée, sur six communes.',
         en='Ruby, more purple on granite. Red fruit dominates. Supple, fleshy, fine palate: it is said to be the most tender of the '
            'crus. It is also the largest; it runs right round a small isolated mountain, across six communes.',
         why=('« Le plus tendre de tous » les crus, ceinturant le Mont Brouilly sur 6 communes (cahier des charges).',
              '“The most tender of all” the crus, encircling Mont Brouilly over 6 communes (rulebook).')),
    dict(id='cote-brouilly-r', aoc='Côte de Brouilly', alias=['Cote de Brouilly'], zone='bjl_crus', col=RED, grapes=GAM,
         fr='Robe rubis profond. Cassis, myrtille, une touche minérale. Bouche plus concentrée et plus fraîche que celle de son voisin. '
            'Vignes sur les pentes mêmes d’une petite montagne de roche bleue (diorite) ; une chapelle à son sommet accueille chaque '
            'septembre un pèlerinage des vignerons.',
         en='Deep ruby. Blackcurrant, blueberry, a mineral touch. More concentrated and fresher than its neighbour. Vines on the very '
            'slopes of a small mountain of blue rock (diorite); a chapel on its summit hosts a growers’ pilgrimage every September.',
         why=('Les pentes du Mont Brouilly, sa « pierre bleue » et la chapelle Notre-Dame-aux-Raisins.',
              'The slopes of Mont Brouilly, its “blue stone” and the Notre-Dame-aux-Raisins chapel.')),
    dict(id='lyonnais-r', aoc='Coteaux du Lyonnais', alias=[], zone='lyonnais', col=RED, grapes=GAM,
         fr='Robe vive. Fruits rouges, parfum gourmand, tanins modérés ; certaines cuvées se boivent en primeur, la plupart '
            'gagnent à attendre un à trois ans. Collines de vergers et de prairies autour d’une grande ville gastronomique ; le '
            'vignoble, qui couvrait 12 000 ha au XIX<sup>e</sup> siècle, ne subsiste plus qu’en deux îlots.',
         en='Bright colour. Red fruit, a tempting perfume, moderate tannins; some cuvées are drunk as primeur, most improve after '
            'one to three years. Hills of orchards and meadows around a great gastronomic city; the vineyard, which covered '
            '12,000 ha in the 19th century, survives in only two islands.',
         why=('Autour de Lyon (49 communes) ; « 12 000 hectares au XIXe siècle… deux îlots » (cahier des charges).',
              'Around Lyon (49 communes); “12,000 hectares in the 19th century… two islands” (rulebook).')),
]
