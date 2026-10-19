"""Tasting notes for « Goûtez votre savoir » / "Taste your knowledge" (Infos/Literature/Taste_Quiz.html).

One note per AOC + colour. Style descriptors follow each AOC's cahier des charges (section « Lien avec la zone
géographique — caractéristiques du produit »); every note carries at least one clue that only that wine has
(a place, a soil, a classification fact, a rule…), explained in `why`.

Fields: id, aoc (must match the Cépages page name), alias (other accepted answers), zone (sub-region key, see ZONES),
col (fr, en) colour & style, grapes (fr, en) hint, fr / en note, why (fr, en) shown after the answer.
Batch status: BORDEAUX (here) and BOURGOGNE (tasting_notes_bourgogne.py) = drafts for the user's review (2026-10-10).
"""

ZONES = {
    'medoc': ('Bordeaux · Médoc (rive gauche)', 'Bordeaux · Médoc (left bank)'),
    'graves': ('Bordeaux · Graves (rive gauche)', 'Bordeaux · Graves (left bank)'),
    'libournais': ('Bordeaux · Libournais (rive droite)', 'Bordeaux · Libournais (right bank)'),
    'cotes': ('Bordeaux · Côtes & Blayais-Bourgeais (rive droite)', 'Bordeaux · Côtes & Blaye-Bourg (right bank)'),
    'e2m': ('Bordeaux · Entre-deux-Mers', 'Bordeaux · Entre-deux-Mers'),
    'liquoreux': ('Bordeaux · Sauternais & liquoreux de la Garonne', 'Bordeaux · Sauternes & the Garonne sweet wines'),
    'regional': ('Bordeaux · appellations régionales (toute la Gironde)', 'Bordeaux · regional appellations (all of the Gironde)'),
}

# every Bordeaux AOC of the Cépages page → zone (used for partial credit on typed answers)
AOC_ZONE = {
    'Médoc': 'medoc', 'Haut-Médoc': 'medoc', 'Margaux': 'medoc', 'Saint-Julien': 'medoc', 'Pauillac': 'medoc',
    'Saint-Estèphe': 'medoc', 'Listrac-Médoc': 'medoc', 'Moulis-en-Médoc': 'medoc',
    'Pessac-Léognan': 'graves', 'Graves': 'graves', 'Graves Supérieures': 'graves',
    'Saint-Émilion': 'libournais', 'Saint-Émilion Grand Cru': 'libournais', 'Pomerol': 'libournais',
    'Lalande-de-Pomerol': 'libournais', 'Fronsac': 'libournais', 'Canon-Fronsac': 'libournais',
    'Montagne-Saint-Émilion': 'libournais', 'Lussac-Saint-Émilion': 'libournais', 'Puisseguin-Saint-Émilion': 'libournais',
    'Saint-Georges-Saint-Émilion': 'libournais',
    'Côtes de Bourg': 'cotes', 'Côtes de Bordeaux': 'cotes',
    'Entre-deux-Mers': 'e2m', 'Graves de Vayres': 'e2m', 'Côtes de Bordeaux Saint-Macaire': 'e2m',
    'Sauternes': 'liquoreux', 'Barsac': 'liquoreux', 'Cérons': 'liquoreux', 'Loupiac': 'liquoreux',
    'Sainte-Croix-du-Mont': 'liquoreux', 'Cadillac': 'liquoreux', 'Premières Côtes de Bordeaux': 'liquoreux',
    'Bordeaux': 'regional', 'Bordeaux Supérieur': 'regional', 'Crémant de Bordeaux': 'regional',
}

RED = ('Rouge tranquille sec', 'Still dry red')
WHITE = ('Blanc sec', 'Dry white')
SWEET = ('Blanc liquoreux', 'Sweet white (liquoreux)')
CS = ('Cabernet-sauvignon majoritaire, avec merlot', 'Mostly Cabernet Sauvignon, with Merlot')
ME = ('Merlot majoritaire, avec cabernet franc et cabernet-sauvignon', 'Mostly Merlot, with Cabernet Franc and Cabernet Sauvignon')
SEM = ('Sémillon majoritaire, avec sauvignon et muscadelle', 'Mostly Sémillon, with Sauvignon and Muscadelle')

NOTES = [
    # ------------------------------------------------------------------ Médoc
    dict(id='pauillac-r', aoc='Pauillac', alias=[], zone='medoc', col=RED, grapes=CS,
         fr='Robe pourpre presque noire. Nez de cassis, de mine de crayon et de boîte à cigares, avec une pointe mentholée. '
            'Bouche droite et profonde, tanins serrés et puissants, longue finale sur le graphite : un vin bâti pour vingt ans de cave. '
            'Il naît sur de profondes croupes de graves où le cabernet-sauvignon est roi, dans la seule commune qui compte '
            'à elle seule trois premiers crus du classement de 1855.',
         en='Purple, almost black. Blackcurrant, pencil shavings and cigar box on the nose, with a minty touch. '
            'Straight, deep palate, tight and powerful tannins, a long graphite finish: a wine built for twenty years in the cellar. '
            'It grows on deep gravel ridges where Cabernet Sauvignon is king, in the only commune that holds three '
            'of the 1855 First Growths on its own.',
         why=('Trois premiers crus de 1855 dans une seule commune : Lafite Rothschild, Latour et Mouton Rothschild — c’est Pauillac.',
              'Three 1855 First Growths in a single commune — Lafite Rothschild, Latour and Mouton Rothschild — means Pauillac.')),
    dict(id='margaux-r', aoc='Margaux', alias=[], zone='medoc', col=RED, grapes=CS,
         fr='Robe rubis profond. Nez d’une grande finesse : violette, framboise, cassis, une touche de rose. '
            'Bouche soyeuse, tanins fins comme une dentelle — l’élégance avant la puissance. '
            'Ses graves s’étagent en terrasses sur plusieurs communes ; c’est la plus vaste des appellations communales '
            'de la presqu’île, et la seule qui porte le même nom que l’un des cinq premiers crus.',
         en='Deep ruby. A very fine nose: violet, raspberry, blackcurrant, a touch of rose. '
            'Silky palate, lace-fine tannins — elegance before power. '
            'Its gravels rise in terraces over several communes; it is the largest of the peninsula’s communal appellations, '
            'and the only one sharing its name with one of the five First Growths.',
         why=('Plus vaste appellation communale du Médoc (cahier des charges) et homonyme du Château Margaux.',
              'The largest communal appellation of the Médoc (per its rulebook), and namesake of Château Margaux.')),
    dict(id='saint-julien-r', aoc='Saint-Julien', alias=['St-Julien', 'Saint-Julien-Beychevelle'], zone='medoc', col=RED, grapes=CS,
         fr='Robe grenat sombre. Cassis, cèdre et tabac blond. Bouche harmonieuse, tout en équilibre entre la puissance '
            'de la commune voisine au nord et la grâce de celle du sud. Petite appellation presque entièrement occupée par '
            'des crus classés — onze, dont trois qui partagent le même nom de Léoville — mais sans aucun premier cru.',
         en='Dark garnet. Blackcurrant, cedar and light tobacco. A harmonious palate, poised between the power of the '
            'neighbouring commune to the north and the grace of the one to the south. A small appellation almost entirely '
            'taken up by classified growths — eleven, three of which share the name Léoville — yet without a single First Growth.',
         why=('Les trois Léoville (Las Cases, Poyferré, Barton) et onze crus classés, mais aucun premier : Saint-Julien, entre Pauillac et Margaux.',
              'The three Léovilles (Las Cases, Poyferré, Barton) and eleven classified growths, but no First Growth: Saint-Julien, between Pauillac and Margaux.')),
    dict(id='saint-estephe-r', aoc='Saint-Estèphe', alias=['St-Estèphe', 'Saint-Estephe'], zone='medoc', col=RED, grapes=CS,
         fr='Robe très sombre. Fruits noirs, terre fraîche et épices, un nez réservé dans la jeunesse. Bouche charpentée, '
            'tanins fermes et acidité vive : un vin qui demande de la patience. C’est la plus septentrionale des appellations '
            'communales du Médoc, où l’argile se mêle aux graves et où le merlot gagne du terrain ; un de ses crus classés '
            'arbore des tours en forme de pagode.',
         en='Very dark. Black fruit, fresh earth and spice, a reserved nose when young. Firm, structured palate, solid tannins '
            'and lively acidity: a wine that asks for patience. It is the northernmost of the Médoc’s communal appellations, '
            'where clay mixes with the gravel and Merlot is gaining ground; one of its classified growths sports pagoda towers.',
         why=('Appellation communale la plus au nord du Médoc ; les pagodes sont celles de Cos d’Estournel.',
              'The northernmost communal appellation of the Médoc; the pagodas belong to Cos d’Estournel.')),
    dict(id='medoc-r', aoc='Médoc', alias=['Medoc'], zone='medoc', col=RED, grapes=CS,
         fr='Robe rubis intense. Fruits rouges et noirs, poivre et épices douces. Bouche franche, tanins présents mais sans dureté, '
            'le merlot y apportant plus de rondeur qu’au sud. Ce vignoble s’étire sur près de 80 km et une cinquantaine '
            'de communes jusqu’à la pointe de la presqu’île, entre la forêt et l’estuaire, autour de Bégadan et de Saint-Yzans.',
         en='Intense ruby. Red and black fruit, pepper and sweet spice. Frank palate, present but gentle tannins, Merlot giving '
            'more roundness than further south. The vineyard stretches over nearly 80 km and some fifty communes up to the tip '
            'of the peninsula, between the forest and the estuary, around Bégadan and Saint-Yzans.',
         why=('« Près de 80 km du nord au sud, 50 communes » : l’aire de l’AOC Médoc (cahier des charges), qui couvre aussi le Bas-Médoc.',
              '“Nearly 80 km north to south, 50 communes”: the Médoc AOC area (rulebook), which also covers the northern Bas-Médoc.')),
    dict(id='haut-medoc-r', aoc='Haut-Médoc', alias=['Haut-Medoc'], zone='medoc', col=RED, grapes=CS,
         fr='Robe pourpre profond. Cassis, épices et vanille d’un élevage en barrique plus courant qu’au nord. Bouche concentrée, '
            'tanins de longue macération qui demandent quelques années. L’appellation court sur une cinquantaine de kilomètres '
            'et 28 communes, du Taillan jusqu’à Saint-Seurin-de-Cadourne ; cinq crus classés de 1855, dont La Lagune et Cantemerle, '
            'portent simplement son nom.',
         en='Deep purple. Blackcurrant, spice and vanilla from barrel ageing, more common than further north. Concentrated palate, '
            'long-maceration tannins that need a few years. The appellation runs for some fifty kilometres and 28 communes, '
            'from Le Taillan to Saint-Seurin-de-Cadourne; five 1855 classified growths, including La Lagune and Cantemerle, '
            'simply carry its name.',
         why=('28 communes, du Taillan-Médoc à Saint-Seurin-de-Cadourne (cahier des charges) ; La Lagune, La Tour Carnet, Belgrave, Camensac et Cantemerle sont classés en AOC Haut-Médoc.',
              '28 communes from Le Taillan-Médoc to Saint-Seurin-de-Cadourne (rulebook); La Lagune, La Tour Carnet, Belgrave, Camensac and Cantemerle are classified as Haut-Médoc.')),
    dict(id='listrac-r', aoc='Listrac-Médoc', alias=['Listrac'], zone='medoc', col=RED, grapes=ME,
         fr='Robe intense. Fruits noirs, réglisse, une touche minérale. Bouche puissante et tannique, mais d’une rondeur '
            'inattendue sur la presqu’île : ici le merlot est souvent majoritaire, sur le calcaire le plus ancien du Médoc. '
            'Le vignoble est perché sur un plateau à 43 mètres, le point culminant de la presqu’île, loin de l’estuaire.',
         en='Intense colour. Black fruit, liquorice, a mineral touch. Powerful, tannic palate, yet unexpectedly round for the '
            'peninsula: Merlot often leads here, on the oldest limestone of the Médoc. The vineyard sits on a plateau at '
            '43 metres, the highest point of the peninsula, far from the estuary.',
         why=('Plateau de 43 m, « point le plus haut du Médoc », calcaire « de Listrac » et merlot majoritaire : tout est dans son cahier des charges.',
              'A 43 m plateau, “the highest point of the Médoc”, the “Listrac” limestone and Merlot-led blends: all from its rulebook.')),
    dict(id='moulis-r', aoc='Moulis-en-Médoc', alias=['Moulis'], zone='medoc', col=RED, grapes=ME,
         fr='Robe profonde. Nez élégant de fruits rouges et noirs aux nuances épicées. Bouche fine et ronde dès la jeunesse, '
            'puis une structure qui la porte sept à dix ans. L’appellation forme un étroit ruban de douze kilomètres '
            'perpendiculaire à l’estuaire ; c’est la communale la plus à l’ouest, sans façade sur la Gironde — '
            '« un formidable concentré du Médoc viticole ».',
         en='Deep colour. An elegant nose of red and black fruit with spicy hints. Fine and round from youth, then a structure '
            'that carries it seven to ten years. The appellation is a narrow twelve-kilometre ribbon at right angles to the '
            'estuary; it is the westernmost communal, with no frontage on the Gironde — “a remarkable concentrate of the wine Médoc”.',
         why=('Ruban de 12 km perpendiculaire à l’estuaire, communale la plus à l’ouest sans façade sur la Gironde (cahier des charges).',
              'A 12 km ribbon at right angles to the estuary, the westernmost communal with no Gironde frontage (rulebook).')),
    # ------------------------------------------------------------------ Graves
    dict(id='pessac-r', aoc='Pessac-Léognan', alias=['Pessac-Leognan', 'Pessac'], zone='graves', col=RED, grapes=CS,
         fr='Robe rubis sombre. Cassis d’abord, puis des notes fumées, de cuir, de tabac et de pruneau. Bouche ample, tanins '
            'fondus par la barrique. Ses graves profondes pénètrent jusque dans les faubourgs de Bordeaux, où se trouve '
            'le seul premier cru de 1855 qui ne soit pas médocain.',
         en='Dark ruby. Blackcurrant first, then smoky notes, leather, tobacco and prune. Ample palate, tannins softened by '
            'the barrel. Its deep gravels reach right into the suburbs of Bordeaux, home to the only 1855 First Growth '
            'that is not in the Médoc.',
         why=('Haut-Brion, à Pessac, est le seul premier cru de 1855 hors Médoc. Notes fumées, de cuir et de pruneau : cahier des charges.',
              'Haut-Brion, in Pessac, is the only non-Médoc 1855 First Growth. Smoke, leather and prune: per the rulebook.')),
    dict(id='pessac-b', aoc='Pessac-Léognan', alias=['Pessac-Leognan', 'Pessac'], zone='graves', col=WHITE,
         grapes=('Sauvignon et sémillon', 'Sauvignon and Sémillon'),
         fr='Robe jaune paille assez pâle. Agrumes, buis, fleurs blanches, un boisé noble. Bouche à la fois nerveuse et '
            'pleine de sève, longue ; avec l’âge, le vin se dore et évoque le tilleul et le genêt. Il vient de l’appellation '
            'créée en 1987 au sud immédiat de Bordeaux, qui rassemble tous les crus classés des Graves.',
         en='Fairly pale straw. Citrus, boxwood, white flowers, fine oak. A palate both nervy and full of sap, long; with age '
            'the wine turns golden and recalls linden and broom. It comes from the appellation created in 1987 just south '
            'of Bordeaux, which brings together all the classified growths of the Graves.',
         why=('Appellation créée en 1987 qui regroupe tous les crus classés des Graves ; tilleul et genêt cités par son cahier des charges.',
              'Created in 1987 and home to all the Graves classified growths; linden and broom are named in its rulebook.')),
    dict(id='graves-r', aoc='Graves', alias=[], zone='graves', col=RED, grapes=('Cabernet-sauvignon et merlot équilibrés', 'Balanced Cabernet Sauvignon and Merlot'),
         fr='Robe rubis. Fruits rouges, notes épicées et grillées, une finale finement fumée. Élégant, structuré, à son apogée '
            'entre cinq et dix ans. Rive gauche, au sud de Bordeaux jusqu’à Langon : c’est la seule grande appellation '
            'bordelaise qui porte le nom de son sol.',
         en='Ruby. Red fruit, spicy and toasty notes, a finely smoky finish. Elegant, structured, at its peak between five '
            'and ten years. Left bank, south of Bordeaux down to Langon: the only major Bordeaux appellation named after its soil.',
         why=('Les « graves » sont les graviers et galets déposés par la Garonne ; apogée entre 5 et 10 ans selon le cahier des charges.',
              '“Graves” are the gravels and pebbles laid down by the Garonne; peak between 5 and 10 years per the rulebook.')),
    dict(id='graves-b', aoc='Graves', alias=[], zone='graves', col=WHITE, grapes=('Sémillon, avec sauvignon et muscadelle', 'Sémillon, with Sauvignon and Muscadelle'),
         fr='Robe jaune pâle. Fleurs, agrumes, parfois une note exotique ou mentholée. Bouche élégante et charnue : le sémillon '
            'y apporte un gras naturel qui n’exclut pas la fraîcheur, le sauvignon de la vivacité, la muscadelle une touche musquée. '
            'Le vignoble enserre le Sauternais, sur les terrasses de cailloux roulés de la rive gauche.',
         en='Pale yellow. Flowers, citrus, sometimes an exotic or minty note. Elegant, fleshy palate: Sémillon brings a natural '
            'richness that keeps its freshness, Sauvignon liveliness, Muscadelle a musky touch. The vineyard surrounds the '
            'Sauternes area, on the left bank’s terraces of rolled pebbles.',
         why=('Les notes « exotiques ou mentholées » et le gras du sémillon sont décrits par le cahier des charges des Graves blancs.',
              'The “exotic or minty” notes and Sémillon’s richness are described in the white Graves rulebook.')),
    # ------------------------------------------------------------------ Libournais
    dict(id='st-emilion-gc-r', aoc='Saint-Émilion Grand Cru', alias=['Saint-Emilion Grand Cru', 'St-Émilion Grand Cru', 'Saint-Émilion'],
         zone='libournais', col=RED, grapes=ME,
         fr='Robe grenat intense. Fruits rouges et noirs bien mûrs, prune, vanille de la barrique. Bouche ronde aux tanins '
            'soyeux, chair généreuse ; le cabernet franc y ajoute une fraîcheur légèrement épicée. Plateau calcaire et côtes '
            'argilo-calcaires autour d’une cité médiévale inscrite au patrimoine mondial de l’UNESCO, dont le classement '
            'des crus est révisé environ tous les dix ans.',
         en='Intense garnet. Ripe red and black fruit, plum, vanilla from oak. Round palate with silky tannins and generous flesh; '
            'Cabernet Franc adds a slightly spicy freshness. A limestone plateau and clay-limestone slopes around a medieval town '
            'on the UNESCO World Heritage list, whose classification of growths is revised roughly every ten years.',
         why=('Juridiction inscrite à l’UNESCO (1999) et seul classement bordelais révisé périodiquement (le dernier en 2022).',
              'A jurisdiction on the UNESCO list (1999) and the only Bordeaux classification revised periodically (latest in 2022).')),
    dict(id='pomerol-r', aoc='Pomerol', alias=[], zone='libournais', col=RED,
         grapes=('Merlot très largement majoritaire', 'Overwhelmingly Merlot'),
         fr='Robe sombre, presque d’encre. Nez puissant de fruits noirs, de violette et de truffe. Bouche ample et veloutée, '
            'sans la moindre dureté, d’une grande longueur. Petit plateau d’argiles et de graves au sous-sol parfois chargé '
            'de « crasse de fer » ; aucun classement officiel n’y existe, et pourtant certains de ses vins comptent parmi les '
            'plus chers du monde.',
         en='Dark, almost inky. A powerful nose of black fruit, violet and truffle. Ample, velvety palate without any hardness, '
            'very long. A small plateau of clay and gravel, its subsoil sometimes rich in iron pan (“crasse de fer”); there is '
            'no official classification, yet some of its wines are among the most expensive in the world.',
         why=('Violette et truffe (cahier des charges), crasse de fer, et la seule grande appellation bordelaise sans aucun classement (Pétrus, Le Pin…).',
              'Violet and truffle (rulebook), iron pan, and the only great Bordeaux appellation with no classification at all (Pétrus, Le Pin…).')),
    dict(id='lalande-r', aoc='Lalande-de-Pomerol', alias=['Lalande de Pomerol'], zone='libournais', col=RED, grapes=ME,
         fr='Robe rubis aux reflets grenat. Petits fruits rouges et noirs, une note de violette. Bouche charnue et ample, sans dureté, '
            'charmeuse dans la jeunesse. Elle s’étend juste au nord d’une prestigieuse voisine dont elle emprunte le nom, '
            'de l’autre côté du petit ruisseau de la Barbanne.',
         en='Ruby with garnet tints. Small red and black fruit, a hint of violet. Fleshy, ample, without hardness, charming '
            'when young. It lies just north of a prestigious neighbour whose name it borrows, across the little Barbanne stream.',
         why=('La Barbanne sépare Pomerol de Lalande-de-Pomerol ; « harmonie, équilibre, élégance » selon son cahier des charges.',
              'The Barbanne stream separates Pomerol from Lalande-de-Pomerol; “harmony, balance, elegance” per its rulebook.')),
    dict(id='fronsac-r', aoc='Fronsac', alias=[], zone='libournais', col=RED,
         grapes=('Merlot, cabernets et un peu de malbec', 'Merlot, the Cabernets and a little Malbec'),
         fr='Robe intense teintée de pourpre. Nez puissant de fruits rouges, souvent truffé, parfois giboyeux ou minéral. '
            'Texture qui allie robustesse et élégance. Coteaux argilo-calcaires et tertre au confluent de l’Isle et de la Dordogne, '
            'face à Libourne ; le malbec y est le quatrième cépage et apporte réglisse et petits fruits noirs.',
         en='Intense with a purple tinge. A powerful nose of red fruit, often truffled, sometimes gamey or mineral. A texture '
            'that combines sturdiness and elegance. Clay-limestone slopes and a hilltop (tertre) at the confluence of the Isle '
            'and the Dordogne, facing Libourne; Malbec is the fourth grape here, bringing liquorice and small black fruit.',
         why=('Confluent de l’Isle et de la Dordogne, malbec « quatrième cépage », notes truffées et giboyeuses : cahier des charges de Fronsac.',
              'Isle–Dordogne confluence, Malbec as “fourth grape”, truffle and game notes: the Fronsac rulebook.')),
    dict(id='canon-fronsac-r', aoc='Canon-Fronsac', alias=['Canon Fronsac'], zone='libournais', col=RED,
         grapes=('Merlot, cabernets et un peu de malbec', 'Merlot, the Cabernets and a little Malbec'),
         fr='Robe rouge intense, reflets rubis. Mûre, cerise, cassis, qui évoluent vers des notes truffées, giboyeuses ou épicées. '
            'Une petite appellation de coteaux pentus, de tertres et de vallonnements rocailleux, enclavée dans une voisine plus vaste '
            'du même nom, sur les pentes qui dominent la Dordogne au-dessus de ports autrefois très actifs.',
         en='Intense red with ruby tints. Blackberry, cherry, blackcurrant, turning truffled, gamey or spicy with age. '
            'A small appellation of steep slopes, hilltops and rocky folds, set inside a larger neighbour of the same name, '
            'on slopes overlooking the Dordogne above once-busy river ports.',
         why=('« Coteaux, tertres, vallonnements rocailleux… ports très accessibles » : le cahier des charges de Canon-Fronsac, petite enclave dans Fronsac.',
              '“Slopes, hilltops, rocky folds… easily reached ports”: the Canon-Fronsac rulebook, a small enclave within Fronsac.')),
    dict(id='montagne-r', aoc='Montagne-Saint-Émilion', alias=['Montagne-Saint-Emilion', 'Montagne'], zone='libournais', col=RED, grapes=ME,
         fr='Robe soutenue. Fruits rouges intenses qui évoluent vers les épices, le cuir et la réglisse ; grillé et vanille '
            'd’une barrique fréquente. Bouche puissante et ronde. C’est le plus vaste des « satellites » qui ajoutent à leur nom '
            'celui de la célèbre cité voisine, au nord de la Barbanne, sur des coteaux argilo-calcaires.',
         en='Deep colour. Intense red fruit evolving towards spice, leather and liquorice; toast and vanilla from frequent '
            'barrel ageing. Powerful, round palate. It is the largest of the “satellites” that add the famous neighbouring town’s '
            'name to their own, north of the Barbanne, on clay-limestone slopes.',
         why=('Plus grand des quatre satellites (avec Lussac, Puisseguin et Saint-Georges) ; « cuir et réglisse » cités par son cahier des charges.',
              'The largest of the four satellites (with Lussac, Puisseguin and Saint-Georges); “leather and liquorice” are named in its rulebook.')),
    # ------------------------------------------------------------------ Côtes, Bourg, Blaye
    dict(id='bourg-r', aoc='Côtes de Bourg', alias=['Bourg', 'Bourgeais', 'Cotes de Bourg'], zone='cotes', col=RED,
         grapes=('Merlot et cabernet-sauvignon, un peu de malbec', 'Merlot and Cabernet Sauvignon, a little Malbec'),
         fr='Robe pourpre. Fruits noirs, notes grillées et vanillées quand il passe en barrique. Bouche généreuse et structurée, '
            'tanins de garde. Coteaux escarpés face au confluent de la Dordogne et de la Garonne, là où naît la Gironde, '
            'autour d’un petit port qui a expédié le vin jusqu’au XIX<sup>e</sup> siècle ; on surnommait le pays « la petite Suisse girondine ».',
         en='Purple. Black fruit, toasty and vanilla notes when barrel-aged. Generous, structured palate, tannins for keeping. '
            'Steep slopes facing the confluence of the Dordogne and the Garonne, where the Gironde begins, around a small port that '
            'shipped wine until the 19th century; the area was nicknamed “the little Switzerland of the Gironde”.',
         why=('Face au Bec d’Ambès (confluent Dordogne-Garonne), port de Bourg cité par le cahier des charges.',
              'Facing the Bec d’Ambès (Dordogne–Garonne confluence); the port of Bourg is cited in the rulebook.')),
    dict(id='castillon-r', aoc='Côtes de Bordeaux', alias=['Castillon Côtes de Bordeaux', 'Castillon', 'Côtes de Castillon'],
         zone='cotes', col=RED, grapes=ME,
         fr='Robe rubis foncé. Bouquet concentré et profond : pruneau, cuir, gibier, touches fraîches de sous-bois et de petits '
            'fruits rouges bien mûrs. Bouche fruitée, charpentée, puissante. Il vient des coteaux à l’est de Saint-Émilion, '
            'au bord de la Dordogne, là où s’acheva la guerre de Cent Ans en 1453.',
         en='Dark ruby. A concentrated, deep bouquet: prune, leather, game, fresh hints of undergrowth and very ripe red berries. '
            'Fruity, firm, powerful palate. It comes from the slopes east of Saint-Émilion, on the Dordogne, where the Hundred '
            'Years’ War ended in 1453.',
         why=('Bataille de Castillon (1453). Castillon est une dénomination de l’AOC Côtes de Bordeaux ; pruneau, cuir, gibier : cahier des charges.',
              'The Battle of Castillon (1453). Castillon is a denomination of the Côtes de Bordeaux AOC; prune, leather, game: per the rulebook.')),
    dict(id='blaye-b', aoc='Côtes de Bordeaux', alias=['Blaye Côtes de Bordeaux', 'Blaye', 'Côtes de Blaye'],
         zone='cotes', col=WHITE, grapes=('Sauvignon, sémillon et muscadelle', 'Sauvignon, Sémillon and Muscadelle'),
         fr='Robe or pâle. Genêt, agrumes et fruits jaunes. Bouche ronde et fruitée, une jolie fraîcheur. Ses vignes regardent '
            'le Médoc de l’autre côté de l’estuaire, au pied d’une citadelle de Vauban inscrite au patrimoine mondial.',
         en='Pale gold. Broom, citrus and yellow fruit. Round, fruity palate with good freshness. Its vines look across the '
            'estuary at the Médoc, below a Vauban citadel on the World Heritage list.',
         why=('Citadelle de Blaye (fortifications de Vauban, UNESCO 2008) ; « genêts, agrumes, fruits jaunes » pour les blancs de Blaye (cahier des charges).',
              'The Blaye citadel (Vauban fortifications, UNESCO 2008); “broom, citrus, yellow fruit” for Blaye whites (rulebook).')),
    # ------------------------------------------------------------------ regional
    dict(id='bordeaux-r', aoc='Bordeaux', alias=[], zone='regional', col=RED,
         grapes=('Merlot et cabernets en assemblage', 'A Merlot and Cabernet blend'),
         fr='Robe rubis vif. Fruits rouges croquants, une pointe d’épice. Bouche souple, tanins légers : à boire dans ses '
            'premières années. C’est l’appellation la plus vaste de la région, avec plus de deux millions d’hectolitres de rouge '
            'par an, produits dans presque toute la Gironde viticole.',
         en='Bright ruby. Crunchy red fruit, a touch of spice. Supple palate, light tannins: drink in its first few years. '
            'It is the region’s largest appellation, with more than two million hectolitres of red a year, made across almost '
            'all of the Gironde’s vineyards.',
         why=('« Plus de 2 000 000 hectolitres de vins rouges » : l’AOC Bordeaux (cahier des charges).',
              '“More than 2,000,000 hectolitres of red wine”: the Bordeaux AOC (rulebook).')),
    dict(id='bordeaux-sup-r', aoc='Bordeaux Supérieur', alias=['Bordeaux Superieur'], zone='regional', col=RED,
         grapes=('Merlot et cabernet-sauvignon', 'Merlot and Cabernet Sauvignon'),
         fr='Robe profonde. Fruits rouges frais et confits, qui évoluent vers les épices et les fruits cuits. Bouche ronde, ample '
            'et structurée, après un élevage long. Même aire que l’appellation régionale de base, mais des rendements plus bas '
            'et un élevage plus long — et jamais de rosé.',
         en='Deep colour. Fresh and candied red fruit, turning to spice and cooked fruit. Round, ample, structured palate after '
            'a long ageing. Same area as the basic regional appellation, but lower yields and longer ageing — and never any rosé.',
         why=('Même aire que Bordeaux, rendements plus faibles, « élevage long » (cahier des charges) ; seulement rouge et blanc moelleux.',
              'Same area as Bordeaux, lower yields, “long ageing” (rulebook); only red and medium-sweet white.')),
    dict(id='clairet', aoc='Bordeaux', alias=['Bordeaux Clairet', 'Clairet'], zone='regional', col=('Clairet', 'Clairet'),
         grapes=('Merlot et cabernets', 'Merlot and the Cabernets'),
         fr='Robe entre le rosé soutenu et le rouge léger, couleur cerise. Fraise, framboise, groseille. Bouche fraîche et légère, '
            'avec un soupçon de tanin. Obtenu par une courte macération, il est l’héritier du vin pâle que les Anglais buvaient '
            'au Moyen Âge — et auquel ils ont donné leur mot pour désigner tous les rouges de la région.',
         en='Somewhere between deep rosé and light red, cherry-coloured. Strawberry, raspberry, redcurrant. Fresh, light palate '
            'with a hint of tannin. Made by a short maceration, it is the heir to the pale wine the English drank in the Middle Ages '
            '— and which gave them their word for all the region’s reds.',
         why=('Le « clairet » a donné le mot anglais « claret ». C’est une mention de l’AOC Bordeaux.',
              '“Clairet” gave the English word “claret”. It is a mention within the Bordeaux AOC.')),
    dict(id='cremant-b', aoc='Crémant de Bordeaux', alias=['Cremant de Bordeaux'], zone='regional',
         col=('Blanc effervescent', 'Sparkling white'), grapes=('Sémillon, sauvignon, cabernet franc, merlot…', 'Sémillon, Sauvignon, Cabernet Franc, Merlot…'),
         fr='Robe brillante, bulles fines et mousse persistante. Nez frais d’agrumes et de fleurs blanches, puis, après l’élevage '
            'sur lies, des notes plus mûres, beurrées et de pain grillé. Bouche nerveuse, finale longue et fruitée. Élaboré en '
            'blanc de blancs ou en blanc de noirs selon l’année, par seconde fermentation en bouteille, dans une région bien plus '
            'connue pour ses vins tranquilles.',
         en='Bright, fine bubbles and a persistent mousse. A fresh nose of citrus and white flowers, then, after ageing on the lees, '
            'riper, buttery and toasted-bread notes. Nervy palate, long fruity finish. Made as blanc de blancs or blanc de noirs '
            'depending on the year, by second fermentation in bottle, in a region far better known for its still wines.',
         why=('Le crémant de la Gironde, en méthode traditionnelle ; « blancs de blancs ou blancs de noirs », « pain grillé » : cahier des charges.',
              'The Gironde’s crémant, made by the traditional method; “blanc de blancs or blanc de noirs”, “toasted bread”: per the rulebook.')),
    # ------------------------------------------------------------------ Entre-deux-Mers
    dict(id='e2m-b', aoc='Entre-deux-Mers', alias=['Entre deux Mers'], zone='e2m', col=WHITE,
         grapes=('Sauvignon, sémillon, muscadelle', 'Sauvignon, Sémillon, Muscadelle'),
         fr='Robe jaune paille aux reflets verts. Fleurs blanches comme l’acacia, agrumes, fruits exotiques. Attaque vive, '
            'puis une bouche ample et ronde. Il naît sur un vaste plateau calcaire entre deux grands fleuves que les marées '
            'faisaient appeler des « mers ».',
         en='Straw yellow with green tints. White flowers such as acacia, citrus, exotic fruit. A lively attack, then an ample, '
            'round palate. It grows on a large limestone plateau between two great rivers whose tides earned them the name '
            '“seas”.',
         why=('Entre la Garonne et la Dordogne, soumises à la marée ; acacia, agrumes et fruits exotiques : cahier des charges.',
              'Between the tidal Garonne and Dordogne; acacia, citrus and exotic fruit: per the rulebook.')),
    dict(id='vayres-r', aoc='Graves de Vayres', alias=['Graves-de-Vayres'], zone='e2m', col=RED, grapes=ME,
         fr='Robe rubis. Nez très aromatique de fruits rouges. Bouche ronde et veloutée, tanins solides mais jamais durs, '
            'agréable jeune et capable de cinq à dix ans de garde. Une petite enclave de sols graveleux sur un méandre de la '
            'Dordogne, face à Libourne, en plein Entre-deux-Mers.',
         en='Ruby. A very aromatic red-fruit nose. Round, velvety palate, tannins firm but never hard, pleasant young and able '
            'to keep five to ten years. A small enclave of gravel soils on a meander of the Dordogne, facing Libourne, in the '
            'heart of the Entre-deux-Mers.',
         why=('Méandre de la Dordogne et graves, face à Libourne ; « 5 à 10 ans » selon la part de cabernet-sauvignon (cahier des charges).',
              'A Dordogne meander and gravel, facing Libourne; “5 to 10 years” depending on Cabernet Sauvignon (rulebook).')),
    # ------------------------------------------------------------------ sweet whites
    dict(id='sauternes', aoc='Sauternes', alias=[], zone='liquoreux', col=SWEET, grapes=SEM,
         fr='Robe or, qui s’ambre avec les années. Abricot sec, miel, agrumes confits, safran, et ce « rôti » caractéristique '
            'de la pourriture noble. Bouche très grasse, onctueuse, d’une persistance immense ; des décennies de garde. '
            'Les brumes d’automne naissent là où un petit affluent froid rejoint la Garonne plus chaude, et l’appellation '
            'abrite le seul « premier cru supérieur » du classement de 1855.',
         en='Gold, turning amber over the years. Dried apricot, honey, candied citrus, saffron, and the “roasted” character of '
            'noble rot. Very rich, unctuous palate with immense length; decades of ageing. Autumn mists rise where a small, cold '
            'tributary meets the warmer Garonne, and the appellation is home to the only “superior first growth” of the 1855 '
            'classification.',
         why=('Les brumes du Ciron et Château d’Yquem, seul premier cru supérieur ; bouquet « rôti » (cahier des charges).',
              'The Ciron mists and Château d’Yquem, the only superior first growth; the “roasted” bouquet (rulebook).')),
    dict(id='barsac', aoc='Barsac', alias=[], zone='liquoreux', col=SWEET, grapes=SEM,
         fr='Robe dorée. Fruits très expressifs, agrumes, miel, et une vivacité marquée, presque une texture minérale. '
            'Liquoreux de pourriture noble né sur un plateau calcaire de la rive gauche du Ciron ; ses vins ont le droit '
            'd’utiliser aussi le nom de leur illustre voisin.',
         en='Golden. Very expressive fruit, citrus, honey, and marked liveliness, almost a mineral texture. A noble-rot sweet wine '
            'from a limestone plateau on the left bank of the Ciron; its wines may also use the name of their illustrious neighbour.',
         why=('Le calcaire donne « vivacité » et « texture minérale » (cahier des charges) ; un Barsac peut aussi s’étiqueter Sauternes.',
              'The limestone gives “liveliness” and a “mineral texture” (rulebook); a Barsac may also be labelled Sauternes.')),
    dict(id='cerons', aoc='Cérons', alias=['Cerons'], zone='liquoreux', col=SWEET, grapes=SEM,
         fr='Robe dorée. Agrumes, miel et fleur d’acacia. Très aromatique, fin, fruité et frais, avec une belle vivacité '
            'et beaucoup d’onctuosité. Une toute petite appellation de la rive gauche, entre Barsac et Podensac, '
            'enclavée dans les Graves dont elle suit les règles pour planter la vigne.',
         en='Golden. Citrus, honey and acacia blossom. Very aromatic, fine, fruity and fresh, with good liveliness and plenty '
            'of unctuousness. A tiny left-bank appellation between Barsac and Podensac, set inside the Graves, whose rules it '
            'follows for planting.',
         why=('« Agrumes, miel, acacia », et « l’établissement du vignoble suit les mêmes règles que pour les Graves » : cahier des charges de Cérons.',
              '“Citrus, honey, acacia”, and “vineyards follow the same rules as the Graves”: the Cérons rulebook.')),
    dict(id='loupiac', aoc='Loupiac', alias=[], zone='liquoreux', col=SWEET, grapes=SEM,
         fr='Robe dorée qui s’ambre doucement. Fruits blancs et fleurs dans la jeunesse, puis fruits confits et agrumes, '
            'des notes grillées s’il est élevé en barrique. Délicat et nerveux, d’une belle vivacité. Il vient de coteaux '
            'au relief accidenté sur la rive droite de la Garonne, face au Sauternais, entre Cadillac et Sainte-Croix-du-Mont.',
         en='Golden, slowly turning amber. White fruit and flowers when young, then candied fruit and citrus, toasty notes if '
            'barrel-aged. Delicate and nervy, with lovely liveliness. It comes from steep slopes on the right bank of the Garonne, '
            'facing Sauternes, between Cadillac and Sainte-Croix-du-Mont.',
         why=('Rive droite de la Garonne, entre Cadillac et Sainte-Croix-du-Mont ; « délicats et nerveux » (cahier des charges).',
              'Right bank of the Garonne, between Cadillac and Sainte-Croix-du-Mont; “delicate and nervy” (rulebook).')),
    dict(id='sainte-croix', aoc='Sainte-Croix-du-Mont', alias=['Sainte Croix du Mont', 'Ste-Croix-du-Mont'], zone='liquoreux', col=SWEET, grapes=SEM,
         fr='Robe dorée. Fruits blancs et fleurs, puis fruits confits et agrumes. Une grande douceur, équilibrée et délicate, '
            'à la persistance riche. Ses coteaux dominent la Garonne face au Sauternais ; sous le village, un banc d’huîtres '
            'fossiles géantes abrite des caves creusées dans le coquillage.',
         en='Golden. White fruit and flowers, then candied fruit and citrus. Great sweetness, balanced and delicate, with rich '
            'length. Its slopes overlook the Garonne opposite Sauternes; beneath the village, a bank of giant fossil oysters '
            'holds cellars carved into the shells.',
         why=('Le célèbre banc d’huîtres fossiles de Sainte-Croix-du-Mont ; concentration « 10 à 12 jours » sur argilo-calcaire (cahier des charges).',
              'Sainte-Croix-du-Mont’s famous fossil-oyster bank; “10 to 12 days” of concentration on clay-limestone (rulebook).')),
    dict(id='cadillac', aoc='Cadillac', alias=[], zone='liquoreux', col=SWEET, grapes=SEM,
         fr='Robe dorée. Fruits blancs et fleurs, puis fruits confits, agrumes et parfois grillé. Douceur et élégance, grande '
            'persistance. Les vendangeurs y passent de pied en pied en trois ou quatre tries pour ne cueillir que les grains '
            'rôtis. L’appellation porte le nom d’une bastide de la rive droite de la Garonne dominée par le château des ducs '
            'd’Épernon.',
         en='Golden. White fruit and flowers, then candied fruit, citrus and sometimes toast. Sweetness and elegance, great '
            'length. Pickers go from vine to vine in three or four passes (tries) to take only the shrivelled grapes. The '
            'appellation is named after a right-bank Garonne bastide town dominated by the castle of the Dukes of Épernon.',
         why=('Bastide de Cadillac et château des ducs d’Épernon ; tries successives décrites par le cahier des charges.',
              'The bastide of Cadillac and the Dukes of Épernon’s castle; successive tries described in the rulebook.')),
]


from tasting_notes_bourgogne import ZONES_BGY, AOC_ZONE_BGY, NOTES_BGY  # noqa: E402

ZONES.update(ZONES_BGY)
AOC_ZONE.update(AOC_ZONE_BGY)
NOTES += NOTES_BGY
from tasting_notes_beaujolais import ZONES_BJL, AOC_ZONE_BJL, NOTES_BJL  # noqa: E402
ZONES.update(ZONES_BJL)
AOC_ZONE.update(AOC_ZONE_BJL)
NOTES += NOTES_BJL
from tasting_notes_rhone import ZONES_RHO, AOC_ZONE_RHO, NOTES_RHO  # noqa: E402
ZONES.update(ZONES_RHO)
AOC_ZONE.update(AOC_ZONE_RHO)
NOTES += NOTES_RHO
from tasting_notes_loire import ZONES_LOI, AOC_ZONE_LOI, NOTES_LOI  # noqa: E402
ZONES.update(ZONES_LOI)
AOC_ZONE.update(AOC_ZONE_LOI)
NOTES += NOTES_LOI
from tasting_notes_alsace import ZONES_ALS, AOC_ZONE_ALS, NOTES_ALS  # noqa: E402
ZONES.update(ZONES_ALS)
AOC_ZONE.update(AOC_ZONE_ALS)
NOTES += NOTES_ALS
from tasting_notes_champagne import ZONES_CHA, AOC_ZONE_CHA, NOTES_CHA  # noqa: E402
ZONES.update(ZONES_CHA)
AOC_ZONE.update(AOC_ZONE_CHA)
NOTES += NOTES_CHA
from tasting_notes_jura_savoie import ZONES_JS, AOC_ZONE_JS, NOTES_JS  # noqa: E402
ZONES.update(ZONES_JS)
AOC_ZONE.update(AOC_ZONE_JS)
NOTES += NOTES_JS
from tasting_notes_provence_corse import ZONES_PC, AOC_ZONE_PC, NOTES_PC  # noqa: E402
ZONES.update(ZONES_PC)
AOC_ZONE.update(AOC_ZONE_PC)
NOTES += NOTES_PC
from tasting_notes_languedoc_roussillon import ZONES_LR, AOC_ZONE_LR, NOTES_LR  # noqa: E402
ZONES.update(ZONES_LR)
AOC_ZONE.update(AOC_ZONE_LR)
NOTES += NOTES_LR
from tasting_notes_sudouest import ZONES_SO, AOC_ZONE_SO, NOTES_SO  # noqa: E402
ZONES.update(ZONES_SO)
AOC_ZONE.update(AOC_ZONE_SO)
NOTES += NOTES_SO


def notes():
    return NOTES


if __name__ == '__main__':
    from collections import Counter
    print(len(NOTES), Counter(n['zone'] for n in NOTES))
    ids = [n['id'] for n in NOTES]
    assert len(ids) == len(set(ids))
    for n in NOTES:
        assert n['aoc'] in AOC_ZONE and n['zone'] == AOC_ZONE[n['aoc']], n['id']
