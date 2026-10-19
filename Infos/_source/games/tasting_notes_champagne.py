"""Champagne batch for « Goûtez votre savoir » (see tasting_notes.py for the field list).

Three AOCs only (Champagne, Coteaux champenois, Rosé des Riceys): the sparkling notes all answer « Champagne » (style names
accepted as aliases). Optional `area` overrides the « Région » hint with the sub-area. Rules from the 2025 CDCs.
"""

ZONES_CHA = {
    'champ': ('Champagne · vins effervescents', 'Champagne · sparkling wines'),
    'champ_tq': ('Champagne · vins tranquilles', 'Champagne · still wines'),
}
AOC_ZONE_CHA = {'Champagne': 'champ', 'Coteaux Champenois': 'champ_tq', 'Rosé des Riceys': 'champ_tq'}

SPK = ('Blanc effervescent', 'Sparkling white')
ASS = ('Chardonnay, pinot noir et meunier', 'Chardonnay, Pinot Noir and Meunier')


def area(fr, en):
    return (f'Champagne · {fr}', f'Champagne · {en}')


NOTES_CHA = [
    dict(id='ch-brut-nv', aoc='Champagne', alias=['Champagne brut', 'Brut sans année', 'Champagne brut sans année'], zone='champ',
         col=('Blanc effervescent, brut', 'Sparkling white, brut'), grapes=ASS, area=area('assemblage de crus', 'blend of crus'),
         fr='Robe or pâle, bulles fines et persistantes. Pomme, poire, agrumes, brioche, une touche de noisette. Bouche vive, crayeuse, '
            'avec une pointe de sucre à peine perceptible. Un assemblage de cépages, de villages et d’années — grâce aux vins de réserve — '
            'resté au moins quinze mois en bouteille avant d’être vendu.',
         en='Pale gold, fine and persistent bubbles. Apple, pear, citrus, brioche, a touch of hazelnut. Lively, chalky palate with a barely '
            'perceptible hint of sugar. A blend of grapes, villages and years — thanks to reserve wines — kept at least fifteen months '
            'in bottle before sale.',
         why=('« Élevage de quinze mois minimum à compter de la date du tirage », vins de réserve (cahier des charges).',
              '“A minimum of fifteen months’ ageing from bottling”, reserve wines (rulebook).')),
    dict(id='ch-bdb', aoc='Champagne', alias=['Champagne blanc de blancs', 'Blanc de blancs'], zone='champ', col=SPK,
         grapes=('Chardonnay seul', 'Chardonnay only'), area=area('Côte des Blancs', 'Côte des Blancs'),
         fr='Robe jaune très pâle aux reflets verts. Citron, fleurs blanches, craie, puis amande et brioche. Bouche tendue, fine, '
            'saline, d’une grande élégance. Issu des seuls raisins blancs d’un coteau de craie au sud d’Épernay, autour de villages '
            'comme Cramant, Avize ou le Mesnil-sur-Oger.',
         en='Very pale yellow with green tints. Lemon, white flowers, chalk, then almond and brioche. Taut, fine, saline palate of great '
            'elegance. Made from white grapes only on a chalk slope south of Épernay, around villages such as Cramant, Avize or '
            'Le Mesnil-sur-Oger.',
         why=('« Issus seulement de raisins blancs [blanc de blancs] » (cahier des charges) ; la Côte des Blancs et ses grands crus.',
              '“Made from white grapes only [blanc de blancs]” (rulebook); the Côte des Blancs and its grands crus.')),
    dict(id='ch-bdn', aoc='Champagne', alias=['Champagne blanc de noirs', 'Blanc de noirs'], zone='champ', col=SPK,
         grapes=('Pinot noir et/ou meunier', 'Pinot Noir and/or Meunier'), area=area('Montagne de Reims', 'Montagne de Reims'),
         fr='Robe or soutenu, presque cuivrée. Fruits rouges, pomme cuite, pain d’épices. Bouche ample, vineuse, charpentée. Un vin '
            'blanc fait uniquement de raisins noirs pressés délicatement, venu d’une montagne boisée entre Reims et Épernay où un phare '
            'veille au milieu des vignes, à Verzenay.',
         en='Deep gold, almost coppery. Red fruit, baked apple, gingerbread. Ample, vinous, structured palate. A white wine made only '
            'from gently pressed black grapes, from a wooded hill between Reims and Épernay where a lighthouse stands among the vines, '
            'at Verzenay.',
         why=('« Seulement de raisins noirs [blanc de noirs] » (cahier des charges) ; le phare de Verzenay, Montagne de Reims.',
              '“From black grapes only [blanc de noirs]” (rulebook); the Verzenay lighthouse, Montagne de Reims.')),
    dict(id='ch-rose', aoc='Champagne', alias=['Champagne rosé', 'Rosé de Champagne'], zone='champ', col=('Rosé effervescent', 'Sparkling rosé'),
         grapes=ASS, area=area('toute l’appellation', 'whole appellation'),
         fr='Robe rose saumon. Fraise des bois, framboise, groseille, agrumes. Bouche fraîche et fruitée, bulles fines. Il peut être '
            'obtenu par saignée, mais le plus souvent en ajoutant un peu de vin rouge tranquille au vin blanc — une pratique interdite '
            'pour les rosés tranquilles en Europe.',
         en='Salmon pink. Wild strawberry, raspberry, redcurrant, citrus. Fresh, fruity palate, fine bubbles. It may be made by saignée, '
            'but usually by adding a little still red wine to the white — a practice banned for still rosés in Europe.',
         why=('Rosés « obtenus par assemblage ou par saignée » (cahier des charges) : le rosé d’assemblage, interdit pour les rosés tranquilles.',
              'Rosés “made by blending or by saignée” (rulebook): blended rosé, banned for still rosés.')),
    dict(id='ch-vintage', aoc='Champagne', alias=['Champagne millésimé', 'Millésimé'], zone='champ', col=SPK, grapes=ASS,
         area=area('une seule année', 'a single year'),
         fr='Robe or. Fruits jaunes, fruits cuits, miel, épices, noisette grillée, une touche de torréfaction. Bouche riche, crémeuse, '
            'longue. Ici, pas de vins de réserve : une seule récolte, déclarée seulement les belles années, et au moins trois ans '
            'd’élevage avant la vente.',
         en='Gold. Yellow fruit, cooked fruit, honey, spice, toasted hazelnut, a roasted touch. Rich, creamy, long palate. No reserve wines '
            'here: a single harvest, declared only in good years, and at least three years’ ageing before sale.',
         why=('Les millésimés ne sortent qu’après une période d’élevage plus longue (trois ans) ; vins de réserve exclus (cahier des charges).',
              'Vintage wines only leave after a longer ageing period (three years); reserve wines excluded (rulebook).')),
    dict(id='ch-brut-nature', aoc='Champagne', alias=['Champagne brut nature', 'Brut nature', 'Zéro dosage'], zone='champ',
         col=('Blanc effervescent, non dosé', 'Sparkling white, zero dosage'), grapes=ASS, area=area('toute l’appellation', 'whole appellation'),
         fr='Robe pâle. Agrumes, pomme verte, craie, coquille d’huître. Bouche très sèche, tranchante, sans aucun arrondi : on n’a ajouté '
            'aucune liqueur après le dégorgement, et le vin contient moins de 3 g de sucre par litre.',
         en='Pale. Citrus, green apple, chalk, oyster shell. Very dry, cutting palate without any softening: no liqueur was added after '
            'disgorgement, and the wine holds less than 3 g of sugar per litre.',
         why=('Brut nature : aucune liqueur d’expédition, moins de 3 g/l de sucre.', 'Brut nature: no liqueur d’expédition, under 3 g/l of sugar.')),
    dict(id='ch-demi-sec', aoc='Champagne', alias=['Champagne demi-sec', 'Demi-sec'], zone='champ',
         col=('Blanc effervescent, demi-sec', 'Sparkling white, demi-sec'), grapes=ASS, area=area('toute l’appellation', 'whole appellation'),
         fr='Robe dorée. Fruits jaunes, fruits confits, miel, brioche. Bouche ronde et nettement sucrée, entre 32 et 50 g de sucre par litre, '
            'tenue par la fraîcheur des bulles : le champagne du dessert, longtemps le style préféré des cours européennes.',
         en='Golden. Yellow fruit, candied fruit, honey, brioche. Round, clearly sweet palate, 32–50 g of sugar per litre, held up by the '
            'freshness of the bubbles: the dessert Champagne, long the favourite style of Europe’s courts.',
         why=('Demi-sec : 32 à 50 g/l de sucre après dosage.', 'Demi-sec: 32–50 g/l of sugar after dosage.')),
    dict(id='ch-meunier', aoc='Champagne', alias=['Champagne meunier'], zone='champ', col=SPK, grapes=('Meunier', 'Meunier'),
         area=area('Vallée de la Marne', 'Marne Valley'),
         fr='Robe or pâle. Fruits blancs bien mûrs, pomme, abricot, une rondeur gourmande. Bouche souple, fruitée, accessible jeune. '
            'Le cépage des sols plus argileux et des fonds frais de la vallée d’une rivière, celle où une abbaye bénédictine, à Hautvillers, '
            'abrite la tombe d’un célèbre moine cellérier.',
         en='Pale gold. Ripe white fruit, apple, apricot, a tempting roundness. Supple, fruity palate, approachable young. The grape of the '
            'more clayey soils and cool valley floors of a river valley, the one where a Benedictine abbey at Hautvillers holds the tomb '
            'of a famous cellarer monk.',
         why=('Le meunier, cépage de la Vallée de la Marne ; l’abbaye d’Hautvillers et la tombe de Dom Pérignon.',
              'Meunier, the grape of the Marne Valley; Hautvillers abbey and Dom Pérignon’s tomb.')),
    dict(id='ch-bar', aoc='Champagne', alias=['Champagne Côte des Bar'], zone='champ', col=SPK, grapes=('Pinot noir surtout', 'Mostly Pinot Noir'),
         area=area('Côte des Bar (Aube)', 'Côte des Bar (Aube)'),
         fr='Robe or soutenu. Fruits rouges, pêche, épices. Bouche ample et vineuse. Des vignes plus proches de Chablis que de Reims, sur '
            'les mêmes marnes à petites huîtres fossiles, dans un département qui fut exclu de l’appellation en 1908 — d’où les émeutes '
            'de 1911 — et n’y fut pleinement réintégré qu’en 1927.',
         en='Deep gold. Red fruit, peach, spice. Ample, vinous palate. Vines closer to Chablis than to Reims, on the same marls full of tiny '
            'fossil oysters, in a département excluded from the appellation in 1908 — hence the 1911 riots — and fully reinstated only in 1927.',
         why=('La Côte des Bar (Aube), sur marnes kimméridgiennes ; l’Aube exclue en 1908, émeutes de 1911, réintégrée en 1927.',
              'The Côte des Bar (Aube), on Kimmeridgian marls; the Aube excluded in 1908, 1911 riots, reinstated in 1927.')),
    # ------------------------------------------------------------------ still wines
    dict(id='cc-r', aoc='Coteaux Champenois', alias=['Coteaux champenois rouge', 'Bouzy rouge'], zone='champ_tq', col=('Rouge tranquille', 'Still red'),
         grapes=('Pinot noir', 'Pinot Noir'),
         fr='Robe rouge transparente. Cerise, framboise, une note crayeuse. Bouche légère, fine, attaque soyeuse. Un rouge sans bulles, '
            'souvent étiqueté du nom de son village, dans une région où presque tout le raisin finit en vin mousseux ; le plus connu vient '
            'de Bouzy.',
         en='Transparent red. Cherry, raspberry, a chalky note. Light, fine palate with a silky attack. A red without bubbles, often labelled '
            'with its village name, in a region where almost every grape ends up sparkling; the best known comes from Bouzy.',
         why=('Vins tranquilles « souvent désignés par le nom de la commune », rouges « tout en légèreté » (cahier des charges) ; Bouzy rouge.',
              'Still wines “often named after the commune”, reds “all lightness” (rulebook); Bouzy rouge.')),
    dict(id='cc-b', aoc='Coteaux Champenois', alias=['Coteaux champenois blanc'], zone='champ_tq', col=('Blanc tranquille', 'Still white'),
         grapes=('Chardonnay surtout', 'Mostly Chardonnay'),
         fr='Robe pâle. Fleurs, agrumes, craie. Bouche cristalline, saline, très minérale, d’une belle persistance. Un chardonnay sans '
            'bulles né sur les mêmes coteaux que les grands effervescents — une rareté.',
         en='Pale. Flowers, citrus, chalk. Crystalline, saline, very mineral palate with good length. A Chardonnay without bubbles from the '
            'same slopes as the great sparkling wines — a rarity.',
         why=('Blancs à la « texture cristalline, saline, avec une minéralité qui domine » (cahier des charges).',
              'Whites with a “crystalline, saline texture, dominated by minerality” (rulebook).')),
    dict(id='riceys-rs', aoc='Rosé des Riceys', alias=['Rose des Riceys'], zone='champ_tq', col=('Rosé tranquille', 'Still rosé'),
         grapes=('Pinot noir', 'Pinot Noir'),
         fr='Robe lumineuse, du saumon au rouge garance. Fruits rouges jeune, puis fruits secs, épices, parfois fruits confits. Bouche fine et '
            'harmonieuse, longue. Toujours millésimé, produit en tout petit volume, dans un village de l’Aube qui est le seul de France à '
            'posséder trois appellations d’origine contrôlée.',
         en='Luminous, from salmon to madder red. Red fruit when young, then dried fruit, spice, sometimes candied fruit. Fine, harmonious, '
            'long. Always vintage-dated, made in tiny volumes, in an Aube village that is the only one in France with three AOCs.',
         why=('« Vin tranquille obligatoirement millésimé » (cahier des charges) ; Les Riceys : Champagne, Coteaux champenois et Rosé des Riceys.',
              '“A still wine that must be vintage-dated” (rulebook); Les Riceys: Champagne, Coteaux Champenois and Rosé des Riceys.')),
]
