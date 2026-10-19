"""South-West & Charentes batch for « Goûtez votre savoir » (see tasting_notes.py for the field list).
Descriptors from the CDCs where the « lien » section is filled in (many are: Bergerac area, Buzet, Duras, Marmandais,
Fronton, Marcillac, Millau, Gaillac, Corrèze, Pineau); Cahors, Madiran, Pacherenc, Jurançon, Irouléguy, Saint-Mont,
Tursan and Floc have no usable product section → established facts, flagged in the review sheet.
"""

ZONES_SO = {
    'so_dordogne': ('Sud-Ouest · Bergerac & Dordogne', 'South-West · Bergerac & Dordogne'),
    'so_garonne': ('Sud-Ouest · Garonne & Lot-et-Garonne', 'South-West · Garonne & Lot-et-Garonne'),
    'so_haut': ('Sud-Ouest · Haut-Pays (Lot, Tarn, Aveyron, Corrèze)', 'South-West · uplands (Lot, Tarn, Aveyron, Corrèze)'),
    'so_pyr': ('Sud-Ouest · Gascogne & Pyrénées', 'South-West · Gascony & the Pyrenees'),
    'charentes': ('Charentes', 'Charentes'),
}
_Z = {'so_dordogne': ['Bergerac', 'Côtes de Bergerac', 'Monbazillac', 'Saussignac', 'Pécharmant', 'Rosette', 'Montravel',
                      'Côtes de Montravel', 'Haut-Montravel'],
      'so_garonne': ['Buzet', 'Côtes de Duras', 'Côtes du Marmandais', 'Brulhois', 'Fronton', 'Saint-Sardos'],
      'so_haut': ['Cahors', 'Coteaux du Quercy', 'Gaillac', 'Gaillac Premières Côtes', 'Marcillac', 'Entraygues-Le Fel', 'Estaing',
                  'Côtes de Millau', 'Corrèze'],
      'so_pyr': ['Madiran', 'Pacherenc du Vic-Bilh', 'Jurançon', 'Béarn', 'Irouléguy', 'Saint-Mont', 'Tursan', 'Floc de Gascogne'],
      'charentes': ['Pineau des Charentes']}
AOC_ZONE_SO = {a: z for z, names in _Z.items() for a in names}

RED = ('Rouge tranquille sec', 'Still dry red')
WHITE = ('Blanc sec', 'Dry white')
SEM = ('Sémillon, sauvignon, muscadelle', 'Sémillon, Sauvignon, Muscadelle')
BDX = ('Merlot, cabernets, cot', 'Merlot, the Cabernets, Cot')

NOTES_SO = [
    # ------------------------------------------------------------------ uplands
    dict(id='cahors-r', aoc='Cahors', alias=[], zone='so_haut', col=RED, grapes=('Malbec (cot), au moins 70 %', 'Malbec (Cot), at least 70 %'),
         fr='Robe d’encre, presque noire. Mûre, prune, violette, réglisse, une note de cuir avec l’âge. Bouche dense, tannique, fraîche en finale. '
            'Terrasses et causses calcaires dans les méandres du Lot, autour d’un pont fortifié médiéval ; jadis exporté sous le nom de '
            '« vin noir ».',
         en='Inky, almost black. Blackberry, plum, violet, liquorice, a leather note with age. Dense, tannic palate, fresh on the finish. Terraces '
            'and limestone causses in the meanders of the Lot, around a fortified medieval bridge; once exported as “black wine”.',
         why=('Malbec (cot) au moins 70 % ; le « vin noir » de Cahors ; pont Valentré.', 'At least 70 % Malbec (Cot); the “black wine” of Cahors; Pont Valentré.')),
    dict(id='marcillac-r', aoc='Marcillac', alias=[], zone='so_haut', col=RED, grapes=('Fer servadou (« mansois »), au moins 80 %', 'Fer Servadou (“Mansois”), at least 80 %'),
         fr='Robe rouge intense aux reflets violets. Fruits rouges, cassis, poivre, une touche végétale ; réglisse et cacao avec l’âge. Belle acidité, '
            'tanins présents sans agressivité. Un vallon de terres rouges près de Rodez, avec un cépage qu’on appelle ici « mansois ».',
         en='Intense red with violet tints. Red fruit, blackcurrant, pepper, a vegetal touch; liquorice and cocoa with age. Good acidity, present but '
            'gentle tannins. A valley of red soils near Rodez, with a grape known here as “Mansois”.',
         why=('Fer servadou ≥ 80 % « ce qui leur confère une grande originalité », vallon de Marcillac, 11 communes (cahier des charges).',
              'Fer Servadou ≥ 80 % “giving them great originality”, the Marcillac valley, 11 communes (rulebook).')),
    dict(id='gaillac-b', aoc='Gaillac', alias=['Gaillac perlé'], zone='so_haut', col=WHITE, grapes=('Len de l’el et mauzac', 'Len de l’El and Mauzac'),
         fr='Robe pâle, parfois un léger perlant. Pomme, poire, fleurs, une note herbacée. Acidité modérée, bouche souple. Deux cépages qu’on ne '
            'trouve guère ailleurs, dont l’un porte un nom occitan signifiant « loin de l’œil » ; dans l’ancien golfe de l’Albigeois, sur les '
            'rives du Tarn.',
         en='Pale, sometimes a light prickle. Apple, pear, flowers, a herbal note. Moderate acidity, supple palate. Two grapes hardly found elsewhere, '
            'one with an Occitan name meaning “far from the eye”; in the old “gulf” of the Albigeois, on the banks of the Tarn.',
         why=('Len de l’el (« loin de l’œil ») et mauzac ; « golfe de l’Albigeois », « acidité modérée » (cahier des charges).',
              'Len de l’El (“far from the eye”) and Mauzac; the “gulf of the Albigeois”, “moderate acidity” (rulebook).')),
    dict(id='millau-r', aoc='Côtes de Millau', alias=['Cotes de Millau'], zone='so_haut', col=RED, grapes=('Gamay, syrah, cabernet, fer', 'Gamay, Syrah, Cabernet, Fer'),
         fr='Robe rubis à reflets vifs. Fruits rouges, tanins fondus, élégants. Un vignoble accroché aux pentes des gorges du Tarn creusées dans les '
            'causses, au pied du plus haut pont routier du monde.',
         en='Ruby with bright tints. Red fruit, soft, elegant tannins. A vineyard clinging to the slopes of the Tarn gorges carved into the causses, '
            'below the world’s tallest road bridge.',
         why=('Haute vallée du Tarn, gorges creusées dans les causses (cahier des charges) ; viaduc de Millau.', 'Upper Tarn valley, gorges cut into the causses (rulebook); the Millau viaduct.')),
    dict(id='correze-paille', aoc='Corrèze', alias=['Vin de paille de la Corrèze', 'Correze'], zone='so_haut', col=('Vin de paille (doux)', 'Vin de paille (sweet)'),
         grapes=('Cabernets, merlot, chardonnay…', 'Cabernets, Merlot, Chardonnay…'),
         fr='Robe ambrée à acajou. Fruits secs, pruneau, figue, noix, une touche épicée. Bouche douce et fraîche. Des raisins séchés sur la paille ou '
            'des claies pendant l’hiver, entre Brive et la Dordogne, aux portes du Limousin — loin du Jura, l’autre patrie de ce style.',
         en='Amber to mahogany. Dried fruit, prune, fig, walnut, a spicy touch. Sweet, fresh palate. Grapes dried on straw or racks over winter, between '
            'Brive and the Dordogne, at the edge of the Limousin — far from the Jura, the other home of this style.',
         why=('L’AOC Corrèze (24 communes au sud-ouest du département) produit un vin de paille.', 'The Corrèze AOC (24 communes in the south-west of the département) makes a vin de paille.')),
    # ------------------------------------------------------------------ Garonne
    dict(id='fronton-r', aoc='Fronton', alias=[], zone='so_garonne', col=RED, grapes=('Négrette majoritaire', 'Mostly Négrette'),
         fr='Robe sombre. Violette, fruits rouges et noirs, réglisse, une note poivrée. Tanins présents. Terrasses du Tarn au nord de Toulouse ; '
            'pour ne pas trop extraire ce cépage local, les pressoirs continus y sont interdits.',
         en='Dark. Violet, red and black fruit, liquorice, a peppery note. Present tannins. Terraces of the Tarn north of Toulouse; to avoid over-'
            'extracting this local grape, continuous presses are banned.',
         why=('Négrette majoritaire, « les pressoirs continus sont interdits » (cahier des charges).', 'Négrette as the main grape, “continuous presses are banned” (rulebook).')),
    dict(id='marmandais-r', aoc='Côtes du Marmandais', alias=['Cotes du Marmandais'], zone='so_garonne', col=RED,
         grapes=('Merlot, cabernets, avec abouriou, cot, syrah', 'Merlot, Cabernets, with Abouriou, Cot, Syrah'),
         fr='Robe pourpre. Fruits rouges et noirs, épices. Bouche souple et fruitée. De part et d’autre de la Garonne, une appellation dont '
            'l’originalité est un cépage local, l’abouriou, aux côtés des cépages bordelais.',
         en='Purple. Red and black fruit, spice. Supple, fruity palate. On both sides of the Garonne, an appellation whose originality is a local '
            'grape, Abouriou, alongside the Bordeaux varieties.',
         why=('« L’abouriou, cépage particulier du Marmandais » (cahier des charges).', '“Abouriou, a grape particular to the Marmandais” (rulebook).')),
    dict(id='buzet-r', aoc='Buzet', alias=[], zone='so_garonne', col=RED, grapes=BDX,
         fr='Robe intense. Fruits, épices, notes fumées de pain grillé, café, vanille. Structure tannique veloutée. Entre Toulouse et Bordeaux, près '
            'du confluent de la Garonne et du Lot ; ici, les vignerons regroupés ont leur propre tonnellerie.',
         en='Intense colour. Fruit, spice, smoky notes of toast, coffee, vanilla. Velvety tannic structure. Between Toulouse and Bordeaux, near the '
            'confluence of the Garonne and the Lot; here the growers’ cooperative has its own cooperage.',
         why=('« A mi-chemin entre Toulouse et Bordeaux… confluence de la Garonne et du Lot », notes « pain grillé, café, vanille » (cahier des charges).',
              '“Halfway between Toulouse and Bordeaux… Garonne–Lot confluence”, “toast, coffee, vanilla” notes (rulebook).')),
    dict(id='duras-b', aoc='Côtes de Duras', alias=['Cotes de Duras'], zone='so_garonne', col=WHITE, grapes=('Sauvignon seul', 'Sauvignon only'),
         fr='Robe pâle. Buis, bourgeon de cassis, agrumes : très fruité et frais. La mention « sec » est obligatoire sur l’étiquette. Le prolongement '
            'du plateau de l’Entre-deux-Mers, à 70 km à l’est de Bordeaux, autour d’un château dont une romancière a pris le nom.',
         en='Pale. Boxwood, blackcurrant bud, citrus: very fruity and fresh. The word “sec” is compulsory on the label. The continuation of the '
            'Entre-deux-Mers plateau, 70 km east of Bordeaux, around a château whose name a novelist took as her own.',
         why=('« Buis ou bourgeon de cassis… mention sec obligatoire », 70 km à l’est de Bordeaux (cahier des charges) ; Marguerite Duras.',
              '“Boxwood or blackcurrant bud… sec compulsory”, 70 km east of Bordeaux (rulebook); Marguerite Duras.')),
    # ------------------------------------------------------------------ Bergerac & Dordogne
    dict(id='bergerac-r', aoc='Bergerac', alias=[], zone='so_dordogne', col=RED, grapes=BDX,
         fr='Robe rubis. Fruits rouges, souplesse du merlot, fermeté des cabernets. Un assemblage obligatoire, de part et d’autre de la Dordogne, '
            'dans une ville dont le plus célèbre « enfant », héros d’Edmond Rostand, n’y a en réalité jamais vécu.',
         en='Ruby. Red fruit, Merlot’s suppleness, the Cabernets’ firmness. A compulsory blend, on both sides of the Dordogne, in a town whose most '
            'famous “son”, Edmond Rostand’s hero, never actually lived there.',
         why=('Assemblage obligatoire d’au moins deux cépages (cahier des charges) ; Cyrano de Bergerac.', 'A compulsory blend of at least two grapes (rulebook); Cyrano de Bergerac.')),
    dict(id='pecharmant-r', aoc='Pécharmant', alias=['Pecharmant'], zone='so_dordogne', col=RED, grapes=('Cabernets, cot, merlot — aucun au-delà de 65 %', 'Cabernets, Cot, Merlot — none above 65 %'),
         fr='Robe rouge sombre et dense. Fruits noirs, épices. Ample, riche en tanins, charpenté, de garde. Les collines à l’est d’un amphithéâtre qui '
            'domine Bergerac ; aucun cépage ne peut dépasser 65 % et le vin ne sort qu’en septembre de l’année suivante.',
         en='Dark, dense red. Black fruit, spice. Ample, tannin-rich, structured, for ageing. The hills on the east side of an amphitheatre above Bergerac; '
            'no grape may exceed 65 % and the wine is released only in September of the following year.',
         why=('« Aucun… dans une proportion supérieure à 65 % », polyphénols > 50, élevage jusqu’au 1er septembre (cahier des charges).',
              '“None above 65 %”, polyphenols > 50, aged until 1 September (rulebook).')),
    dict(id='rosette-b', aoc='Rosette', alias=[], zone='so_dordogne', col=('Blanc moelleux', 'Medium-sweet white'), grapes=SEM,
         fr='Robe légèrement paillée. Fleurs blanches, pamplemousse, une douceur onctueuse. Souple, rond, élégant, à boire jeune. Une toute petite '
            'appellation sur les collines à l’ouest de l’amphithéâtre qui domine Bergerac, face à un voisin rouge.',
         en='Light straw. White flowers, grapefruit, an unctuous sweetness. Supple, round, elegant, best young. A tiny appellation on the hills to the '
            'west of the amphitheatre above Bergerac, facing a red-wine neighbour.',
         why=('« Partie occidentale de l’amphithéâtre… Rosette, partie orientale… Pécharmant » (cahier des charges).', '“Western part of the amphitheatre… Rosette; eastern part… Pécharmant” (rulebook).')),
    dict(id='monbazillac', aoc='Monbazillac', alias=[], zone='so_dordogne', col=('Blanc liquoreux', 'Sweet white'), grapes=SEM,
         fr='Robe or qui fonce avec le temps. Miel, acacia, pêche, agrumes et mirabelles confits. Bouche très sucrée — au moins 45 g par litre. '
            'Coteaux de la rive gauche de la Dordogne face à Bergerac, un quart du vignoble bergeracois, autour d’un château Renaissance.',
         en='Gold, darkening with time. Honey, acacia, peach, candied citrus and mirabelle plums. A very sweet palate — at least 45 g per litre. Slopes '
            'on the left bank of the Dordogne facing Bergerac, a quarter of the Bergerac vineyard, around a Renaissance château.',
         why=('« Miel, acacia, pêche… mirabelles confits », 45 g/l minimum, le quart du vignoble bergeracois (cahier des charges).',
              '“Honey, acacia, peach… candied mirabelles”, 45 g/l minimum, a quarter of the Bergerac vineyard (rulebook).')),
    dict(id='saussignac', aoc='Saussignac', alias=[], zone='so_dordogne', col=('Blanc liquoreux', 'Sweet white'), grapes=SEM,
         fr='Robe jaune doré. Miel, fleurs, agrumes, puis fruits confits, coing, abricot. Fin, élégant, riche. Des plateaux séparés de leur célèbre '
            'voisin liquoreux par un petit ruisseau ; les grands millésimes vivent des décennies.',
         en='Golden yellow. Honey, flowers, citrus, then candied fruit, quince, apricot. Fine, elegant, rich. Plateaus separated from their famous '
            'sweet-wine neighbour by a small stream; great vintages live for decades.',
         why=('La Gardonnette sépare Saussignac de Monbazillac ; « coing ou abricot » (cahier des charges).', 'The Gardonnette separates Saussignac from Monbazillac; “quince or apricot” (rulebook).')),
    dict(id='montravel-b', aoc='Montravel', alias=[], zone='so_dordogne', col=WHITE, grapes=('Sémillon et sauvignon', 'Sémillon and Sauvignon'),
         fr='Robe or pâle. Fruits exotiques, vivacité, minéralité ; puissance et rondeur après élevage sur lies, parfois en fût. Plateau calcaire à '
            'l’ouest de la Dordogne… et la terre d’un philosophe qui écrivit ses Essais dans la tour de son château.',
         en='Pale gold. Exotic fruit, liveliness, minerality; power and roundness after lees ageing, sometimes in oak. A limestone plateau in the west '
            'of the Dordogne… and the land of a philosopher who wrote his Essays in the tower of his château.',
         why=('« Arômes exotiques… grande fraîcheur minérale », élevage sur lies (cahier des charges) ; tour de Montaigne à Saint-Michel-de-Montaigne.',
              '“Exotic aromas… great mineral freshness”, lees ageing (rulebook); Montaigne’s tower at Saint-Michel-de-Montaigne.')),
    # ------------------------------------------------------------------ Gascony & Pyrenees
    dict(id='madiran-r', aoc='Madiran', alias=[], zone='so_pyr', col=RED, grapes=('Tannat surtout', 'Mostly Tannat'),
         fr='Robe noire violacée. Mûre, cassis, épices, réglisse, cacao. Bouche puissante, aux tanins massifs qui demandent des années. Le cépage le '
            'plus tannique de France, sur des « échines » parallèles du piémont pyrénéen ; c’est ici qu’on a inventé la micro-oxygénation pour '
            'l’assouplir.',
         en='Purplish black. Blackberry, blackcurrant, spice, liquorice, cocoa. Powerful palate with massive tannins that need years. France’s most '
            'tannic grape, on parallel ridges of the Pyrenean foothills; micro-oxygenation was invented here to soften it.',
         why=('Le tannat, 5 crêtes parallèles du piémont (cahier des charges) ; micro-oxygénation (Patrick Ducournau, 1990).',
              'Tannat, 5 parallel ridges in the foothills (rulebook); micro-oxygenation (Patrick Ducournau, 1990).')),
    dict(id='pacherenc', aoc='Pacherenc du Vic-Bilh', alias=['Pacherenc'], zone='so_pyr', col=('Blanc moelleux', 'Medium-sweet white'),
         grapes=('Petit manseng, gros manseng, arrufiac, courbu', 'Petit Manseng, Gros Manseng, Arrufiac, Courbu'),
         fr='Robe dorée. Fruits exotiques, coing, agrumes confits, miel, avec une acidité éclatante. Raisins passerillés sur pied jusqu’à la fin de '
            'l’automne. Même aire qu’un rouge très tannique, et un nom gascon qui évoquerait des « piquets en rang ».',
         en='Golden. Exotic fruit, quince, candied citrus, honey, with bright acidity. Grapes shrivelled on the vine into late autumn. Same area as a very '
            'tannic red, and a Gascon name said to mean “posts in a row”.',
         why=('Même aire que Madiran ; passerillage ; « pachet-en-renc » = piquets en rang.', 'Same area as Madiran; passerillage; “pachet-en-renc” = posts in a row.')),
    dict(id='jurancon-moelleux', aoc='Jurançon', alias=['Jurancon'], zone='so_pyr', col=('Blanc moelleux', 'Medium-sweet white'),
         grapes=('Petit manseng surtout', 'Mostly Petit Manseng'),
         fr='Robe or. Mangue, ananas, pamplemousse, coing, épices, miel, une acidité vibrante. Raisins passerillés sur pied jusqu’en hiver, sur des '
            'coteaux face aux Pyrénées près de Pau ; on en aurait frotté les lèvres d’un futur roi à sa naissance, avec une gousse d’ail.',
         en='Gold. Mango, pineapple, grapefruit, quince, spice, honey, vibrant acidity. Grapes shrivelled on the vine into winter, on slopes facing the '
            'Pyrenees near Pau; a future king’s lips are said to have been rubbed with it at birth, with a clove of garlic.',
         why=('Petit manseng passerillé ; le baptême d’Henri IV (ail et jurançon), Pau.', 'Shrivelled Petit Manseng; Henri IV’s christening (garlic and Jurançon), Pau.')),
    dict(id='irouleguy-r', aoc='Irouléguy', alias=['Irouleguy'], zone='so_pyr', col=RED, grapes=('Tannat, cabernet franc, cabernet-sauvignon', 'Tannat, Cabernet Franc, Cabernet Sauvignon'),
         fr='Robe sombre. Fruits noirs, poivre, une note de terre. Tanins fermes, fraîcheur montagnarde. Terrasses vertigineuses de grès rouge en '
            'Basse-Navarre, à quarante kilomètres de l’océan : le seul vignoble AOC du Pays basque français.',
         en='Dark. Black fruit, pepper, an earthy note. Firm tannins, mountain freshness. Dizzying terraces of red sandstone in Lower Navarre, forty '
            'kilometres from the ocean: the only AOC vineyard of the French Basque Country.',
         why=('Basse-Navarre, Pays basque, au pied des Pyrénées, à 40 km de l’océan (cahier des charges).', 'Lower Navarre, Basque Country, below the Pyrenees, 40 km from the ocean (rulebook).')),
    dict(id='saint-mont-r', aoc='Saint-Mont', alias=['Saint Mont'], zone='so_pyr', col=RED, grapes=('Tannat, cabernets, fer', 'Tannat, Cabernets, Fer'),
         fr='Robe sombre. Fruits noirs, épices, tanins bien présents mais polis. Coteaux de l’Adour dans le Gers, entre Armagnac et Pyrénées ; on y '
            'trouve une parcelle de vignes antérieures au phylloxéra classée monument historique.',
         en='Dark. Black fruit, spice, present but polished tannins. Slopes of the Adour in the Gers, between Armagnac and the Pyrenees; it holds a '
            'plot of pre-phylloxera vines listed as a historic monument.',
         why=('Vallée de l’Adour, à 100 km des Pyrénées et de l’océan (cahier des charges) ; vigne de Sarragachies, monument historique (2012).',
              'The Adour valley, 100 km from the Pyrenees and the ocean (rulebook); the Sarragachies vineyard, historic monument (2012).')),
    dict(id='tursan-b', aoc='Tursan', alias=[], zone='so_pyr', col=WHITE, grapes=('Baroque, gros manseng, petit manseng', 'Baroque, Gros Manseng, Petit Manseng'),
         fr='Robe or pâle. Poire, fruits secs, fleurs, une note d’amande. Bouche ronde et fraîche. Trente-six communes des Landes autour de la '
            'bastide de Geaune, avec un cépage blanc qu’on ne cultive presque nulle part ailleurs, le baroque.',
         en='Pale gold. Pear, dried fruit, flowers, an almond note. Round, fresh palate. Thirty-six communes of the Landes around the bastide of Geaune, '
            'with a white grape grown almost nowhere else, Baroque.',
         why=('36 communes autour de Geaune (cahier des charges) ; cépage baroque.', '36 communes around Geaune (rulebook); the Baroque grape.')),
    dict(id='floc', aoc='Floc de Gascogne', alias=['Floc'], zone='so_pyr', col=('Vin de liqueur', 'Vin de liqueur'),
         grapes=('Colombard, gros manseng, ugni blanc… (ou cépages rouges pour le rosé)', 'Colombard, Gros Manseng, Ugni Blanc… (or red grapes for the rosé)'),
         fr='Robe or pâle. Raisin frais, fruits blancs, fleurs, une chaleur d’eau-de-vie. Bouche douce et fraîche, servie fraîche en apéritif. Du moût '
            'de raisin muté avec une jeune eau-de-vie de la même région de Gascogne ; son nom signifie « bouquet de fleurs ».',
         en='Pale gold. Fresh grape, white fruit, flowers, the warmth of brandy. Sweet, fresh palate, served chilled as an aperitif. Grape must fortified '
            'with young brandy from the same Gascon region; its name means “bunch of flowers”.',
         why=('Moût muté à l’armagnac ; « lou floc » = bouquet de fleurs en gascon.', 'Must fortified with Armagnac; “lou floc” = a bunch of flowers in Gascon.')),
    # ------------------------------------------------------------------ Charentes
    dict(id='pineau', aoc='Pineau des Charentes', alias=['Pineau'], zone='charentes', col=('Vin de liqueur blanc', 'White vin de liqueur'),
         grapes=('Ugni blanc, colombard, folle blanche, montils', 'Ugni Blanc, Colombard, Folle Blanche, Montils'),
         fr='Robe jaune paille à dorée. Fruits frais ou confits, miel, une note de noix et de bois. Bouche ronde, fraîche, l’eau-de-vie fondue par '
            'l’élevage en chêne. Du moût muté avec une eau-de-vie célèbre de la même région, vieillie au moins un an ; la légende parle d’un '
            'vigneron distrait qui, en 1589, versa du moût dans un fût qui en contenait déjà.',
         en='Straw-yellow to gold. Fresh or candied fruit, honey, a walnut and wood note. Round, fresh palate, the brandy softened by oak ageing. Must '
            'fortified with a famous brandy from the same region, aged at least a year; legend speaks of an absent-minded grower who, in 1589, '
            'poured must into a cask that already held some.',
         why=('« Mutage du moût… par de l’eau-de-vie à appellation Cognac rassise », même aire que le Cognac (cahier des charges) ; légende de 1589.',
              '“Must fortified… with matured Cognac”, same area as Cognac (rulebook); the 1589 legend.')),
]
