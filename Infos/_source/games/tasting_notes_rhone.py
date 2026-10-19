"""Rhône batch for « Goûtez votre savoir » (see tasting_notes.py for the field list).

Almost every Rhône cahier des charges has a filled-in « lien à l'origine »; descriptors and most clues come from it
(quoted in `why`). Extra facts outside the CDC are flagged in the review sheet.
"""

ZONES_RHO = {
    'rh_nord': ('Vallée du Rhône · septentrionale', 'Rhône Valley · northern'),
    'rh_diois': ('Vallée du Rhône · Diois', 'Rhône Valley · Diois'),
    'rh_sud': ('Vallée du Rhône · méridionale (crus)', 'Rhône Valley · southern (crus)'),
    'rh_reg': ('Vallée du Rhône · Côtes du Rhône & Villages', 'Rhône Valley · Côtes du Rhône & Villages'),
    'rh_peri': ('Vallée du Rhône · Ventoux, Luberon, Drôme & Vivarais', 'Rhône Valley · Ventoux, Luberon, Drôme & Vivarais'),
}
_Z = {'rh_nord': ['Côte-Rôtie', 'Condrieu', 'Château-Grillet', 'Saint-Joseph', 'Hermitage', 'Crozes-Hermitage', 'Cornas', 'Saint-Péray'],
      'rh_diois': ['Clairette de Die', 'Crémant de Die', 'Châtillon-en-Diois', 'Coteaux de Die'],
      'rh_sud': ['Châteauneuf-du-Pape', 'Gigondas', 'Vacqueyras', 'Beaumes-de-Venise', 'Muscat de Beaumes-de-Venise', 'Rasteau',
                 'Cairanne', 'Vinsobres', 'Lirac', 'Tavel'],
      'rh_reg': ['Côtes du Rhône', 'Côtes du Rhône Villages'],
      'rh_peri': ['Ventoux', 'Luberon', 'Grignan-les-Adhémar', 'Côtes du Vivarais']}
AOC_ZONE_RHO = {a: z for z, names in _Z.items() for a in names}

RED = ('Rouge tranquille sec', 'Still dry red')
WHITE = ('Blanc sec', 'Dry white')
SY = ('Syrah', 'Syrah')
GSM = ('Grenache majoritaire, avec syrah et mourvèdre', 'Mostly Grenache, with Syrah and Mourvèdre')

NOTES_RHO = [
    # ------------------------------------------------------------------ north
    dict(id='cote-rotie-r', aoc='Côte-Rôtie', alias=['Cote Rotie', 'Côte Rôtie'], zone='rh_nord', col=RED,
         grapes=('Syrah, avec un peu de viognier', 'Syrah, with a little Viognier'),
         fr='Robe sombre, presque noire. Fruits noirs, poivre, et une touche de violette qui trahit quelques grappes de raisin blanc '
            'cofermentées ; avec l’âge, pain grillé, café, cacao. Tanins soyeux, une rondeur inattendue. Coteaux vertigineux face à '
            'Vienne, le bastion le plus septentrional de la syrah.',
         en='Dark, almost black. Black fruit, pepper and a touch of violet that betrays a few bunches of white grapes co-fermented; '
            'with age, toast, coffee, cocoa. Silky tannins, unexpected roundness. Dizzying slopes facing Vienne, Syrah’s '
            'northernmost stronghold.',
         why=('« Bastion le plus septentrional de la syrah », face à Vienne, avec jusqu’à 20 % de viognier cofermenté (cahier des charges).',
              '“Syrah’s northernmost stronghold”, facing Vienne, with up to 20 % co-fermented Viognier (rulebook).')),
    dict(id='condrieu-b', aoc='Condrieu', alias=[], zone='rh_nord', col=WHITE, grapes=('Viognier', 'Viognier'),
         fr='Robe or aux reflets intenses. Nez exubérant d’abricot et de pêche mûre, de violette et de fleurs blanches. Bouche '
            'puissante, grasse, presque moelleuse, mais portée par une belle vivacité. Coteaux escarpés de la rive droite répartis '
            'sur trois départements ; au XIX<sup>e</sup> siècle, ce vin était doux et se buvait six mois après la vendange.',
         en='Gold with intense glints. An exuberant nose of apricot and ripe peach, violet and white flowers. Powerful, rich, almost '
            'sweet palate, yet lifted by good liveliness. Steep right-bank slopes spread over three départements; in the 19th '
            'century this wine was sweet and drunk six months after harvest.',
         why=('Viognier seul ; 7 communes sur le Rhône, la Loire et l’Ardèche ; vin « doux » au milieu du XIXe siècle (cahier des charges).',
              'Viognier only; 7 communes in the Rhône, Loire and Ardèche; a “sweet” wine in the mid-19th century (rulebook).')),
    dict(id='grillet-b', aoc='Château-Grillet', alias=['Chateau Grillet', 'Château Grillet'], zone='rh_nord', col=WHITE,
         grapes=('Viognier', 'Viognier'),
         fr='Robe jaune or lumineuse. Une minéralité surprenante, puis violette, abricot, pâte d’amande, miel. Bouche grasse '
            'relevée d’une pointe d’acidité, élevée au moins dix-huit mois. Moins de 3,5 hectares en amphithéâtre sur la face sud '
            'd’un promontoire, enclavés au cœur d’une appellation voisine du même cépage : l’une des plus petites AOC de France, '
            'longtemps aux mains d’un seul propriétaire.',
         en='Luminous yellow-gold. A surprising minerality, then violet, apricot, almond paste, honey. Rich palate lifted by a touch '
            'of acidity, aged at least eighteen months. Under 3.5 hectares in an amphitheatre on the south face of a promontory, '
            'set inside a neighbouring appellation of the same grape: one of France’s smallest AOCs, long held by a single owner.',
         why=('Enclave de moins de 3,5 ha dans Condrieu, élevage d’au moins 18 mois (cahier des charges) ; un monopole.',
              'An enclave of under 3.5 ha inside Condrieu, at least 18 months’ ageing (rulebook); a monopole.')),
    dict(id='st-joseph-r', aoc='Saint-Joseph', alias=['Saint Joseph', 'St-Joseph'], zone='rh_nord', col=RED, grapes=SY,
         fr='Robe pourpre. Fruits noirs, épices, réglisse, sous-bois ; une syrah d’élégance et de finesse aux tanins veloutés. '
            'Un long ruban d’une soixantaine de kilomètres sur 23 communes de la rive droite, exposé plein sud, entre le pays '
            'du viognier au nord et celui de Saint-Péray au sud.',
         en='Purple. Black fruit, spice, liquorice, undergrowth; a Syrah of elegance and finesse with velvety tannins. A long ribbon '
            'of some sixty kilometres across 23 right-bank communes, facing south, between Viognier country to the north and '
            'Saint-Péray to the south.',
         why=('« 60 kilomètres environ », 23 communes de la rive droite, la syrah appelée « sérine » (cahier des charges).',
              '“About 60 kilometres”, 23 right-bank communes, Syrah locally called “sérine” (rulebook).')),
    dict(id='hermitage-r', aoc='Hermitage', alias=['Ermitage', "L'Hermitage"], zone='rh_nord', col=RED, grapes=SY,
         fr='Robe intense. Fruits mûrs, épices, sous-bois. Bouche puissante et tannique, de très longue garde. Une colline de granite '
            'que le fleuve a détachée de la montagne ardéchoise, devenue un îlot sur la rive gauche, couronnée d’une chapelle et '
            'visible depuis l’autoroute du Soleil.',
         en='Intense colour. Ripe fruit, spice, undergrowth. Powerful, tannic palate, for very long ageing. A granite hill the river '
            'cut off from the Ardèche mountains, now an island on the left bank, crowned by a chapel and visible from the A7 motorway.',
         why=('« Lambeau de massif granitique que le Rhône a séparé de la montagne ardéchoise » (cahier des charges) ; chapelle Saint-Christophe.',
              '“A fragment of granite massif the Rhône separated from the Ardèche mountains” (rulebook); the Saint-Christophe chapel.')),
    dict(id='hermitage-paille', aoc='Hermitage', alias=['Ermitage', 'Hermitage vin de paille'], zone='rh_nord',
         col=('Vin de paille (blanc liquoreux)', 'Vin de paille (sweet white)'), grapes=('Marsanne et roussanne', 'Marsanne and Roussanne'),
         fr='Robe ambrée. Abricot sec, coing, miel, épices, fruits confits. Bouche liquoreuse et concentrée, d’une longueur infinie. '
            'Des raisins blancs mis à sécher après la vendange ; c’est la seule appellation de la Vallée du Rhône septentrionale '
            'à produire ce type de vin, dans des volumes confidentiels.',
         en='Amber. Dried apricot, quince, honey, spice, candied fruit. A sweet, concentrated palate of endless length. White grapes '
            'left to dry after picking; it is the only appellation of the northern Rhône to make this type of wine, in tiny volumes.',
         why=('L’Hermitage « se distingue… par une production de vins blancs bénéficiant de la mention vin de paille » (cahier des charges).',
              'Hermitage “stands out… with white wines bearing the vin de paille mention” (rulebook).')),
    dict(id='crozes-r', aoc='Crozes-Hermitage', alias=['Crozes Hermitage', 'Crozes'], zone='rh_nord', col=RED, grapes=SY,
         fr='Robe grenat foncé. Framboise et aubépine sauvage, poivre. Bouche agréable, aromatique, structurée sans excès. La plus '
            'vaste appellation du nord, sur onze communes de la Drôme autour d’une célèbre colline, entre l’Isère et un cromlech '
            'de grès nommé « la Roche-qui-danse ».',
         en='Dark garnet. Raspberry and wild hawthorn, pepper. Pleasant, aromatic palate, structured without excess. The largest '
            'northern appellation, over eleven Drôme communes around a famous hill, between the Isère and a sandstone cromlech '
            'called “the Dancing Rock”.',
         why=('« Arôme de framboise et d’aubépine sauvage » (1943), 11 communes, la Roche-qui-danse (cahier des charges).',
              '“Aroma of raspberry and wild hawthorn” (1943), 11 communes, the Roche-qui-danse (rulebook).')),
    dict(id='cornas-r', aoc='Cornas', alias=[], zone='rh_nord', col=RED, grapes=('Syrah, et rien d’autre', 'Syrah, and nothing else'),
         fr='Robe très foncée, grenat presque noir. Fruits noirs, poivre, olive noire, notes animales avec l’âge. Bouche puissante, '
            'charpentée, que l’on qualifie volontiers de « virile » : il faut l’attendre longtemps. Une seule commune de la rive droite, '
            'face à Valence ; la seule appellation du nord où le vin vient exclusivement de la syrah.',
         en='Very dark, almost black garnet. Black fruit, pepper, black olive, animal notes with age. A powerful, structured palate '
            'often called “virile”: it needs long waiting. A single right-bank commune facing Valence; the only northern appellation '
            'made exclusively from Syrah.',
         why=('« Seule appellation… des Côtes du Rhône septentrionales où le vin est produit exclusivement à partir du cépage syrah » ; vins « virils » (cahier des charges).',
              '“The only northern Rhône appellation made exclusively from Syrah”; “virile” wines (rulebook).')),
    dict(id='st-peray-b', aoc='Saint-Péray', alias=['Saint Peray', 'St-Péray'], zone='rh_nord',
         col=('Blanc mousseux ou tranquille', 'Sparkling or still white'), grapes=('Marsanne et roussanne', 'Marsanne and Roussanne'),
         fr='Robe or pâle aux reflets verts, mousse fine et abondante pour la version effervescente. Violette, aubépine, acacia, puis '
            'miel et minéral. Bouche grasse et ronde, une vinosité marquée. Deux communes face à Valence, au pied d’une montagne '
            'calcaire coiffée des ruines d’un château ; au début du XX<sup>e</sup> siècle, neuf bouteilles sur dix y étaient mousseuses.',
         en='Pale gold with green tints, a fine, abundant mousse for the sparkling version. Violet, hawthorn, acacia, then honey and '
            'mineral notes. Rich, round palate, marked vinosity. Two communes facing Valence, below a limestone mountain topped by '
            'castle ruins; in the early 20th century, nine bottles in ten were sparkling.',
         why=('Montagne de Crussol et ses ruines, 2 communes, 90 % de mousseux au début du XXe siècle (cahier des charges).',
              'The Crussol mountain and its ruins, 2 communes, 90 % sparkling in the early 20th century (rulebook).')),
    # ------------------------------------------------------------------ Diois
    dict(id='clairette-die', aoc='Clairette de Die', alias=['Clairette de Die méthode ancestrale', 'Clairette de Die tradition'],
         zone='rh_diois', col=('Blanc effervescent doux', 'Sweet sparkling white'), grapes=('Muscat à petits grains (au moins 75 %) et clairette', 'Muscat à Petits Grains (at least 75 %) and Clairette'),
         fr='Robe pâle, bulles légères. Raisin frais, litchi, agrumes, miel, fleurs : un nez de muscat qui explose. Bouche douce, '
            'fruitée, à peine 7 à 9 % d’alcool. La fermentation est freinée par le froid, puis s’achève en bouteille sans ajout de '
            'liqueur, au pied des falaises du Vercors.',
         en='Pale, light bubbles. Fresh grape, lychee, citrus, honey, flowers: a bursting Muscat nose. Sweet, fruity palate, only '
            '7–9 % alcohol. Fermentation is slowed by cold, then finishes in bottle with no added liqueur, below the Vercors cliffs.',
         why=('Méthode ancestrale : fermentation stoppée par le froid puis achevée en bouteille, 7 à 9 % vol. ; 88 % de la production du Diois (cahier des charges).',
              'Ancestral method: fermentation stopped by cold then finished in bottle, 7–9 % abv; 88 % of Diois output (rulebook).')),
    dict(id='cremant-die', aoc='Crémant de Die', alias=['Cremant de Die'], zone='rh_diois',
         col=('Blanc effervescent brut', 'Dry sparkling white'), grapes=('Clairette (au moins 55 %), aligoté, un peu de muscat', 'Clairette (at least 55 %), Aligoté, a little Muscat'),
         fr='Robe pâle, bulles fines. Fruits très frais et fleur blanche. Bouche sèche, vive, élégante. Méthode traditionnelle, dans '
            'une petite vallée subalpine connue surtout pour un autre effervescent, doux celui-là ; ici, la clairette domine et '
            'l’aligoté apporte la tension.',
         en='Pale, fine bubbles. Very fresh fruit and white flowers. Dry, lively, elegant palate. Traditional method, in a small '
            'sub-Alpine valley best known for another, sweet sparkling wine; here Clairette leads and Aligoté adds tension.',
         why=('Clairette au moins 55 %, aligoté, peu de muscat : il « se distingue des autres vins mousseux du Diois » (cahier des charges).',
              'At least 55 % Clairette, Aligoté, little Muscat: it “stands apart from the Diois’s other sparkling wines” (rulebook).')),
    dict(id='chatillon-r', aoc='Châtillon-en-Diois', alias=['Chatillon en Diois'], zone='rh_diois', col=RED,
         grapes=('Gamay, avec pinot noir et syrah', 'Gamay, with Pinot Noir and Syrah'),
         fr='Robe rubis. Fruits rouges et notes de garrigue. Bouche ronde avec une petite structure tannique et une minéralité. '
            'Un vignoble de montagne de seulement 36 hectares, entre les falaises du Glandasse et un gigantesque éboulement calcaire, '
            'où le gamay rencontre l’influence de la Provence.',
         en='Ruby. Red fruit and garrigue notes. Round palate with light tannic structure and minerality. A mountain vineyard of '
            'only 36 hectares, between the Glandasse cliffs and a gigantic limestone rockfall, where Gamay meets the influence of '
            'Provence.',
         why=('36 ha, le Glandasse et le Claps de Luc-en-Diois, gamay « aux notes de garrigue » (cahier des charges).',
              '36 ha, the Glandasse and the Claps de Luc-en-Diois, Gamay with “garrigue notes” (rulebook).')),
    # ------------------------------------------------------------------ southern crus
    dict(id='cdp-r', aoc='Châteauneuf-du-Pape', alias=['Chateauneuf du Pape', 'Châteauneuf'], zone='rh_sud', col=RED,
         grapes=('Grenache surtout, parmi treize cépages autorisés', 'Mostly Grenache, among thirteen permitted varieties'),
         fr='Robe grenat profond. Fruits noirs confits, garrigue, cuir, épices douces. Bouche puissante, chaleureuse, d’une grande '
            'complexité et d’une longue persistance. Un plateau couvert de gros galets roulés qui restituent la chaleur la nuit ; '
            'dix-huit variétés y sont permises, souvent mêlées dans la même vigne, au pied du château d’été d’un pape d’Avignon.',
         en='Deep garnet. Candied black fruit, garrigue, leather, sweet spice. Powerful, warm palate of great complexity and length. '
            'A plateau covered with big rolled pebbles that give back the heat at night; eighteen varieties are allowed, often mixed '
            'in the same vineyard, below the summer castle of an Avignon pope.',
         why=('« Dix-huit cépages, souvent complantés » (cahier des charges), les galets roulés et le château des papes.',
              '“Eighteen varieties, often interplanted” (rulebook), the rolled pebbles and the popes’ castle.')),
    dict(id='cdp-b', aoc='Châteauneuf-du-Pape', alias=['Chateauneuf du Pape', 'Châteauneuf'], zone='rh_sud', col=WHITE,
         grapes=('Grenache blanc, clairette, roussanne', 'Grenache Blanc, Clairette, Roussanne'),
         fr='Robe or pâle. Fleurs blanches, fruits à chair blanche, fenouil, une touche de miel. Bouche ample et très expressive, '
            'avec une belle fraîcheur aromatique. Un blanc rare (moins d’une bouteille sur dix) d’une appellation célèbre pour ses '
            'rouges et ses bouteilles frappées des clés de saint Pierre.',
         en='Pale gold. White flowers, white-fleshed fruit, fennel, a touch of honey. Ample, very expressive palate with fine aromatic '
            'freshness. A rare white (fewer than one bottle in ten) from an appellation famous for its reds and for bottles embossed '
            'with St Peter’s keys.',
         why=('Blancs « principalement élaborés à partir des cépages grenache B, clairette B et roussanne B » (cahier des charges) ; armoiries papales sur la bouteille.',
              'Whites “mainly from Grenache Blanc, Clairette and Roussanne” (rulebook); papal arms on the bottle.')),
    dict(id='gigondas-r', aoc='Gigondas', alias=[], zone='rh_sud', col=RED, grapes=GSM,
         fr='Robe rubis à grenat foncé. Fruits rouges et noirs très mûrs, puis sous-bois et truffe. Bouche charpentée, généreuse, '
            'de garde. Au pied d’une crête calcaire déchiquetée qui culmine au Rocher du Turc ; en ombrageant le matin, la montagne '
            'allonge la maturation du grenache.',
         en='Ruby to dark garnet. Very ripe red and black fruit, then undergrowth and truffle. Structured, generous palate, for ageing. '
            'Below a jagged limestone ridge topped by the Rocher du Turc; by shading the vines in the morning, the mountain lengthens '
            'Grenache’s ripening.',
         why=('Les Dentelles de Montmirail « en limitant l’ensoleillement du matin… allongent la maturité » du grenache (cahier des charges).',
              'The Dentelles de Montmirail, “by limiting morning sun… lengthen the ripening” of Grenache (rulebook).')),
    dict(id='vacqueyras-r', aoc='Vacqueyras', alias=[], zone='rh_sud', col=RED, grapes=GSM,
         fr='Robe sombre. Fruits rouges et noirs aux accents de surmaturité, confiture, puis épices, cuir et gibier. Bouche généreuse, '
            'souvent après un élevage assez long. Autre village au pied des mêmes Dentelles que son voisin plus connu ; un célèbre '
            'troubadour du XII<sup>e</sup> siècle y serait né.',
         en='Dark. Red and black fruit with overripe accents, jam, then spice, leather and game. Generous palate, often after fairly '
            'long ageing. Another village beneath the same Dentelles as its better-known neighbour; a famous 12th-century troubadour '
            'is said to have been born there.',
         why=('« Fruits confits ou confiturés… cuir, gibier » (cahier des charges) ; le troubadour Raimbaut de Vaqueiras.',
              '“Candied or jammy fruit… leather, game” (rulebook); the troubadour Raimbaut de Vaqueiras.')),
    dict(id='beaumes-r', aoc='Beaumes-de-Venise', alias=['Beaumes de Venise'], zone='rh_sud', col=RED,
         grapes=('Grenache et syrah obligatoires', 'Grenache and Syrah, both required'),
         fr='Robe intense. Fruits rouges et épices, puis notes animales avec l’âge. Bouche élégante, ample et ronde, tanins soyeux. '
            'Sur le versant sud des Dentelles de Montmirail ; le nom ne vient pas de l’Italie mais des grottes du Comtat Venaissin, '
            'et le village est plus connu pour un vin doux.',
         en='Intense colour. Red fruit and spice, then animal notes with age. Elegant, ample, round palate, silky tannins. On the south '
            'slope of the Dentelles de Montmirail; the name comes not from Italy but from the caves of the Comtat Venaissin, and the '
            'village is better known for a sweet wine.',
         why=('« Doit son nom aux Balmes (grottes) du Comtat Venaissin » (cahier des charges) ; rouge sec distinct du muscat.',
              '“Takes its name from the Balmes (caves) of the Comtat Venaissin” (rulebook); a dry red, distinct from the Muscat.')),
    dict(id='muscat-bdv', aoc='Muscat de Beaumes-de-Venise', alias=['Muscat de Beaumes de Venise'], zone='rh_sud',
         col=('Vin doux naturel (blanc)', 'Vin doux naturel (white)'), grapes=('Muscat à petits grains', 'Muscat à Petits Grains'),
         fr='Robe jaune or. Fleurs blanches, miel, pêche, abricot, litchi. Bouche douce et puissante, mais fraîche. Raisins cueillis '
            'à la main en terrasses, très riches en sucre, fermentation arrêtée par ajout d’alcool : au moins 100 g de sucre et '
            '15 % d’alcool, au pied d’une crête calcaire de 732 m.',
         en='Yellow-gold. White flowers, honey, peach, apricot, lychee. Sweet and powerful, yet fresh. Grapes hand-picked on terraces, '
            'very high in sugar, fermentation stopped by adding spirit: at least 100 g of sugar and 15 % alcohol, below a 732 m '
            'limestone ridge.',
         why=('VDN de muscat à petits grains : 252 g/l de sucre à la récolte, 15 % vol. après mutage (cahier des charges).',
              'A Muscat à Petits Grains VDN: 252 g/l of sugar at harvest, 15 % abv after fortification (rulebook).')),
    dict(id='rasteau-vdn', aoc='Rasteau', alias=['Rasteau VDN'], zone='rh_sud', col=('Vin doux naturel (rouge)', 'Vin doux naturel (red)'),
         grapes=('Grenache noir surtout', 'Mostly Grenache Noir'),
         fr='Robe grenat. Kirsch, cerise à l’eau-de-vie, fruits à noyau bien mûrs, puis fruits secs et torréfaction pour les mentions '
            '« hors d’âge » et « rancio ». Bouche ample, douce, tenue par les tanins. Un village dont 98 % de la production est '
            'pourtant du rouge sec ; ses vins mutés sont une rareté du sud de la vallée.',
         en='Garnet. Kirsch, brandied cherry, very ripe stone fruit, then dried fruit and roasted notes for the “hors d’âge” and '
            '“rancio” mentions. Ample, sweet palate held by tannins. A village whose output is 98 % dry red; its fortified wines '
            'are a rarity of the southern valley.',
         why=('VDN de grenache, mentions « hors d’âge » et « rancio » ; « kirsch, cerise à l’eau-de-vie » (cahier des charges).',
              'A Grenache VDN, “hors d’âge” and “rancio” mentions; “kirsch, brandied cherry” (rulebook).')),
    dict(id='cairanne-r', aoc='Cairanne', alias=[], zone='rh_sud', col=RED,
         grapes=('Grenache, syrah, mourvèdre et vieux carignan', 'Grenache, Syrah, Mourvèdre and old Carignan'),
         fr='Robe grenat. Fruits rouges qui évoluent avec la garde. Bouche fine et élégante, juste équilibre acidité-alcool, tanins fins. '
            'Ici, de vieilles vignes de carignan entrent souvent dans l’assemblage — une signature que n’ont pas les villages voisins ; '
            'le village est devenu « cru » en 2016.',
         en='Garnet. Red fruit evolving with age. Fine, elegant palate, a good acid–alcohol balance, fine tannins. Here old Carignan '
            'vines often join the blend — a signature the neighbouring villages lack; the village became a “cru” in 2016.',
         why=('« De vieilles vignes de Carignan… encépagement particulier et distinctif de Cairanne » (cahier des charges).',
              '“Old Carignan vines… a grape mix particular to Cairanne” (rulebook).')),
    dict(id='vinsobres-r', aoc='Vinsobres', alias=[], zone='rh_sud', col=RED, grapes=GSM,
         fr='Robe concentrée. Fruits frais puis fruits confiturés, eau-de-vie, poivre ; vanille et fumé après élevage. Bouche '
            'structurée et corsée, tanins soyeux. Collines du bassin de Valréas au bord de l’Aygues ; premier cru de la Drôme '
            '(2006), au nom qui invite pourtant à la modération.',
         en='Concentrated colour. Fresh then jammy fruit, eau-de-vie, pepper; vanilla and smoke after ageing. Structured, full-bodied '
            'palate, silky tannins. Hills of the Valréas basin by the Aygues; the Drôme’s first cru (2006), with a name that '
            'nevertheless advises moderation.',
         why=('« Vinsobres » : vin sobre ; premier cru de la Drôme ; « fruits confiturés, eau-de-vie, poivre » (cahier des charges).',
              '“Vinsobres”: sober wine; the Drôme’s first cru; “jammy fruit, eau-de-vie, pepper” (rulebook).')),
    dict(id='lirac-r', aoc='Lirac', alias=[], zone='rh_sud', col=RED,
         grapes=('Grenache, syrah, mourvèdre, cinsaut', 'Grenache, Syrah, Mourvèdre, Cinsault'),
         fr='Robe sombre. Fruits rouges et noirs mûrs, épices, aromates, cuir. Bouche ample, puissance élégante, tanins ronds ; '
            'tri de la vendange obligatoire. Terrasses gardoises de la rive droite, sur quatre communes dont Roquemaure, d’où '
            'partaient au XVIII<sup>e</sup> siècle les tonneaux marqués « C.D.R. » — le berceau du nom Côtes du Rhône.',
         en='Dark. Ripe red and black fruit, spice, herbs, leather. Ample palate, elegant power, round tannins; sorting of the harvest '
            'is compulsory. Right-bank terraces in the Gard, over four communes including Roquemaure, from where 18th-century casks '
            'branded “C.D.R.” were shipped — the birthplace of the Côtes du Rhône name.',
         why=('4 communes du Gard, « berceau de l’appellation » Côtes du Rhône, tri obligatoire (cahier des charges).',
              '4 Gard communes, “cradle” of the Côtes du Rhône name, compulsory sorting (rulebook).')),
    dict(id='tavel-rs', aoc='Tavel', alias=[], zone='rh_sud', col=('Rosé', 'Rosé'),
         grapes=('Grenache, cinsaut, clairette, mourvèdre…', 'Grenache, Cinsault, Clairette, Mourvèdre…'),
         fr='Robe rosé foncé, presque rubis. Fruits rouges francs, puis réglisse, aromates, pierre à fusil et épices avec le temps. '
            'Bouche ronde, structurée, d’une persistance très longue : un rosé de gastronomie, qui se garde. Une appellation du Gard '
            'balayée par le mistral, qui ne produit rien d’autre que du rosé.',
         en='Deep pink, almost ruby. Frank red fruit, then liquorice, herbs, flint and spice over time. Round, structured palate of very '
            'long length: a food rosé that can age. A mistral-swept Gard appellation that makes nothing but rosé.',
         why=('« Réservé aux seuls vins tranquilles rosés », « rosé foncé d’une belle couleur hématurique » (cahier des charges).',
              '“Reserved for still rosé wines only”, a “deep rosé of a fine blood-red colour” (rulebook).')),
    # ------------------------------------------------------------------ regional
    dict(id='cdr-r', aoc='Côtes du Rhône', alias=['Cotes du Rhone'], zone='rh_reg', col=RED, grapes=GSM,
         fr='Robe rubis soutenu. Fruits rouges, épices douces, une touche de garrigue. Bouche fruitée et généreuse, plus légère sur '
            'sables, plus tannique sur galets et argiles. Une immense appellation de Vienne à Avignon, sur six départements des deux '
            'rives du fleuve ; 93 % de sa production est en rouge.',
         en='Deep ruby. Red fruit, sweet spice, a touch of garrigue. Fruity, generous palate, lighter on sand, more tannic on pebbles '
            'and clay. A huge appellation from Vienne to Avignon, over six départements on both banks; 93 % of its output is red.',
         why=('Entre Vienne et Avignon, 6 départements, 93 % de rouges (cahier des charges).', 'Between Vienne and Avignon, 6 départements, 93 % red (rulebook).')),
    dict(id='cdrv-r', aoc='Côtes du Rhône Villages', alias=['Cotes du Rhone Villages', 'Côtes du Rhône-Villages'], zone='rh_reg', col=RED,
         grapes=('Grenache au moins 50 %, avec syrah ou mourvèdre', 'Grenache at least 50 %, with Syrah or Mourvèdre'),
         fr='Robe intense. Fruits noirs, épices, garrigue. Bouche pleine et généreuse, plus de densité qu’un Côtes du Rhône simple. '
            'Quatre-vingt-quinze communes entre Montélimar et Avignon, dont certaines peuvent ajouter leur nom sur l’étiquette.',
         en='Intense colour. Black fruit, spice, garrigue. Full, generous palate, denser than plain Côtes du Rhône. Ninety-five communes '
            'between Montélimar and Avignon, some of which may add their name to the label.',
         why=('95 communes entre Montélimar et Avignon ; grenache au moins 50 % (cahier des charges).', '95 communes between Montélimar and Avignon; at least 50 % Grenache (rulebook).')),
    # ------------------------------------------------------------------ periphery
    dict(id='ventoux-r', aoc='Ventoux', alias=['Côtes du Ventoux'], zone='rh_peri', col=RED, grapes=GSM,
         fr='Robe rubis. Fruits rouges frais, poivre, une fraîcheur d’altitude. Bouche riche et équilibrée sur argilo-calcaire, plus '
            'aromatique sur sables et grès ocreux. Cinquante-trois communes du Vaucluse enroulées au pied d’un sommet de 1 912 m '
            'surnommé « le Géant de Provence ».',
         en='Ruby. Fresh red fruit, pepper, an altitude freshness. Rich, balanced palate on clay-limestone, more aromatic on sand and '
            'ochre sandstone. Fifty-three Vaucluse communes wrapped around the foot of a 1,912 m summit nicknamed “the Giant of Provence”.',
         why=('« Le Géant de Provence, le Mont Ventoux, du haut de ses 1912 mètres » ; 53 communes (cahier des charges).',
              '“The Giant of Provence, Mont Ventoux, 1,912 metres high”; 53 communes (rulebook).')),
    dict(id='luberon-rs', aoc='Luberon', alias=['Côtes du Luberon'], zone='rh_peri', col=('Rosé', 'Rosé'),
         grapes=('Grenache, syrah, cinsaut', 'Grenache, Syrah, Cinsault'),
         fr='Robe pâle. Agrumes, fruits exotiques, petits fruits rouges. Bouche fraîche, vive, fruitée. Il fait le lien entre le Rhône '
            'et la Provence, autour d’un massif calcaire de 55 km de long qui culmine au Mourre Nègre, entre Cavaillon et Manosque.',
         en='Pale. Citrus, exotic fruit, small red berries. Fresh, lively, fruity palate. It links the Rhône and Provence, around a '
            '55 km limestone massif that peaks at the Mourre Nègre, between Cavaillon and Manosque.',
         why=('« Rosés… lien entre le vignoble rhodanien et les influences provençales », massif de 55 km, Mourre Nègre 1 125 m (cahier des charges).',
              '“Rosés… a link between the Rhône vineyard and Provençal influences”, a 55 km massif, Mourre Nègre 1,125 m (rulebook).')),
    dict(id='grignan-r', aoc='Grignan-les-Adhémar', alias=['Grignan les Adhemar', 'Coteaux du Tricastin'], zone='rh_peri', col=RED,
         grapes=('Syrah et grenache', 'Syrah and Grenache'),
         fr='Robe vive. Fruits rouges, notes végétales et florales de la syrah, finesse du grenache planté ici à sa limite de maturité. '
            'Bouche ronde, à boire jeune. Vingt et une communes de la Drôme provençale, autour du château où Madame de Sévigné '
            'venait voir sa fille — l’appellation a changé de nom en 2010.',
         en='Bright colour. Red fruit, Syrah’s vegetal and floral notes, finesse from Grenache planted here at the edge of ripening. '
            'Round palate, best young. Twenty-one communes of Drôme provençale, around the castle where Madame de Sévigné visited '
            'her daughter — the appellation changed its name in 2010.',
         why=('Drôme provençale, 21 communes, grenache « en limite de maturité » (cahier des charges) ; château de Grignan ; ex-Coteaux du Tricastin.',
              'Drôme provençale, 21 communes, Grenache “at the limit of ripening” (rulebook); Grignan castle; formerly Coteaux du Tricastin.')),
    dict(id='vivarais-r', aoc='Côtes du Vivarais', alias=['Cotes du Vivarais'], zone='rh_peri', col=RED,
         grapes=('Syrah et grenache', 'Syrah and Grenache'),
         fr='Robe pourpre profond. Arômes végétaux, fruités et poivrés de la syrah. Bouche équilibrée, à boire jeune. Un plateau calcaire '
            'de part et d’autre de la rivière Ardèche et de ses gorges, sur le Gard et l’Ardèche : « les plus septentrionaux des '
            'méridionaux ».',
         en='Deep purple. Syrah’s vegetal, fruity and peppery aromas. Balanced palate, best young. A limestone plateau on both sides '
            'of the Ardèche river and its gorges, in the Gard and Ardèche: “the northernmost of the southern wines”.',
         why=('« Les plus septentrionaux des méridionaux », 14 communes du Gard et de l’Ardèche (cahier des charges).',
              '“The northernmost of the southerners”, 14 communes in the Gard and Ardèche (rulebook).')),
]
