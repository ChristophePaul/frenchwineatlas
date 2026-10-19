"""Alsace & Lorraine batch for « Goûtez votre savoir » (see tasting_notes.py for the field list).

Alsace is labelled by grape: most notes share the answer « Alsace » (grape name accepted as alias), the grands crus share
« Alsace Grand Cru » (cru name accepted). Descriptors and many clues from the CDCs (Alsace, Alsace grand cru — one
lien section per cru —, Crémant d'Alsace, Moselle, Côtes de Toul).
"""

ZONES_ALS = {
    'als': ('Alsace · AOC Alsace & Crémant', 'Alsace · Alsace AOC & Crémant'),
    'als_gc': ('Alsace · les 51 grands crus', 'Alsace · the 51 grands crus'),
    'lorraine': ('Lorraine · Moselle & Côtes de Toul', 'Lorraine · Moselle & Côtes de Toul'),
}
AOC_ZONE_ALS = {'Alsace': 'als', 'Crémant d\'Alsace': 'als', 'Alsace Grand Cru': 'als_gc', 'Moselle': 'lorraine', 'Côtes de Toul': 'lorraine'}

WHITE = ('Blanc sec', 'Dry white')
GC = 'Alsace Grand Cru'


def gc_alias(name):
    return [f'Alsace Grand Cru {name}', f'Grand Cru {name}', name]


NOTES_ALS = [
    # ------------------------------------------------------------------ AOC Alsace, by grape
    dict(id='als-riesling', aoc='Alsace', alias=['Alsace Riesling', 'Riesling d’Alsace', 'Riesling'], zone='als', col=WHITE,
         grapes=('Riesling', 'Riesling'),
         fr='Robe or pâle aux reflets verts. Citron, pomme verte, fleurs blanches, une pointe de pierre et, avec l’âge, une note '
            'de pétrole. Bouche sèche, tendue, minérale, saline. Le cépage roi d’une région où l’on étiquette le vin par son raisin, '
            'dans une flûte élancée, au pied des Vosges.',
         en='Pale gold with green tints. Lemon, green apple, white flowers, a stony hint and, with age, a petrol note. Dry, taut, '
            'mineral, saline palate. The king grape of a region where wine is labelled by its grape, in a slender flute bottle, at '
            'the foot of the Vosges.',
         why=('Vins « secs et minéraux, à l’acidité tendue » (cahier des charges) ; la flûte d’Alsace et l’étiquetage par cépage.',
              '“Dry, mineral wines with taut acidity” (rulebook); the Alsace flute and labelling by grape.')),
    dict(id='als-gewurz', aoc='Alsace', alias=['Alsace Gewurztraminer', 'Gewurztraminer', 'Gewurztraminer d’Alsace'], zone='als',
         col=('Blanc (souvent avec un peu de sucre)', 'White (often slightly sweet)'), grapes=('Gewurztraminer', 'Gewurztraminer'),
         fr='Robe or soutenu. Nez exubérant de rose, de litchi, d’épices douces et de pain d’épices. Bouche ample, grasse, souvent avec '
            'quelques grammes de sucre, une légère amertume en finale. Le plus parfumé des cépages de la région ; son nom allemand '
            'signifie à peu près « traminer épicé ».',
         en='Deep gold. An exuberant nose of rose, lychee, sweet spice and gingerbread. Ample, rich palate, often with a few grams of '
            'sugar, a light bitterness on the finish. The most perfumed grape of the region; its German name roughly means “spicy '
            'Traminer”.',
         why=('Rose et litchi ; vins « fruités, plus souples… extraits secs importants » liés au gewurztraminer (cahier des charges).',
              'Rose and lychee; “fruity, softer… high dry extract” wines linked to Gewurztraminer (rulebook).')),
    dict(id='als-pinot-gris', aoc='Alsace', alias=['Alsace Pinot Gris', 'Pinot Gris d’Alsace', 'Pinot Gris'], zone='als',
         col=('Blanc', 'White'), grapes=('Pinot gris', 'Pinot Gris'),
         fr='Robe or. Poire mûre, abricot, miel, sous-bois et une note fumée. Bouche ronde, opulente, capiteuse. Autrefois vendu sous '
            'le nom de « Tokay », abandonné à la demande de la Hongrie ; ici, ce pinot à la peau grise donne des blancs puissants.',
         en='Gold. Ripe pear, apricot, honey, undergrowth and a smoky note. Round, opulent, heady palate. Once sold as “Tokay”, a name '
            'dropped at Hungary’s request; here this grey-skinned Pinot makes powerful whites.',
         why=('Le pinot gris d’Alsace, ex-« Tokay d’Alsace » (mention interdite depuis 2007) ; type « fruité » du cahier des charges.',
              'Alsace Pinot Gris, formerly “Tokay d’Alsace” (banned since 2007); the “fruity” type of the rulebook.')),
    dict(id='als-muscat', aoc='Alsace', alias=['Alsace Muscat', 'Muscat d’Alsace', 'Muscat'], zone='als', col=WHITE,
         grapes=('Muscat à petits grains et muscat ottonel', 'Muscat à Petits Grains and Muscat Ottonel'),
         fr='Robe pâle. Le nez du raisin frais croqué sur la grappe, fleur de sureau, orange. Surprise en bouche : il est sec, léger, '
            'aérien. Un muscat qui ne ressemble pas à ceux du Midi, servi traditionnellement à l’apéritif ou avec les asperges.',
         en='Pale. The nose of fresh grapes eaten off the bunch, elderflower, orange. A surprise on the palate: it is dry, light, airy. '
            'A Muscat unlike those of the south of France, traditionally served as an aperitif or with asparagus.',
         why=('Muscat sec ; classé par le cahier des charges parmi les vins « secs et minéraux ».', 'A dry Muscat; listed by the rulebook among the “dry, mineral” wines.')),
    dict(id='als-sylvaner', aoc='Alsace', alias=['Alsace Sylvaner', 'Sylvaner'], zone='als', col=WHITE, grapes=('Sylvaner', 'Sylvaner'),
         fr='Robe très pâle. Herbe fraîche, agrumes, une touche florale. Bouche légère, désaltérante, avec ce petit picotement de gaz '
            'carbonique que les vignerons du pays appellent « spritzig ». Le compagnon des tartes flambées et des fruits de mer.',
         en='Very pale. Fresh grass, citrus, a floral touch. Light, thirst-quenching palate, with the little prickle of carbon dioxide '
            'local growers call “spritzig”. The companion of tarte flambée and seafood.',
         why=('« Légère saturation en gaz carbonique traduite localement par le terme spretsig » (cahier des charges).',
              '“Slight CO2 saturation, locally called spretsig” (rulebook).')),
    dict(id='als-pinot-blanc', aoc='Alsace', alias=['Alsace Pinot Blanc', 'Pinot Blanc', 'Klevner', 'Alsace Klevner'], zone='als', col=WHITE,
         grapes=('Pinot blanc et auxerrois', 'Pinot Blanc and Auxerrois'),
         fr='Robe or pâle. Pomme, poire, fleurs blanches, une touche d’amande. Bouche souple, ronde, équilibrée, sans aspérité. Sous ce '
            'nom de cépage, l’usage local permet d’assembler un autre raisin, l’auxerrois ; on l’appelle aussi « Klevner ».',
         en='Pale gold. Apple, pear, white flowers, a touch of almond. Supple, round, balanced, without edges. Under this grape name, local '
            'usage allows blending in another grape, Auxerrois; it is also called “Klevner”.',
         why=('Dénomination « Pinot blanc, Pinot ou Klevner » qui peut contenir de l’auxerrois (cahier des charges).',
              'The “Pinot blanc, Pinot or Klevner” name, which may contain Auxerrois (rulebook).')),
    dict(id='als-edelzwicker', aoc='Alsace', alias=['Edelzwicker', 'Gentil'], zone='als', col=WHITE,
         grapes=('Assemblage de cépages blancs alsaciens', 'A blend of Alsace white grapes'),
         fr='Robe or pâle. Fruits blancs, fleurs, une pointe épicée. Bouche simple, fruitée, conviviale : le vin de carafe des winstubs. '
            'Exception dans une région de vins de cépage, c’est un assemblage, dont le nom signifie « noble mélange ».',
         en='Pale gold. White fruit, flowers, a spicy hint. Simple, fruity, convivial palate: the carafe wine of the winstubs. An exception '
            'in a region of single-grape wines, it is a blend, whose name means “noble mixture”.',
         why=('« Edelzwicker » = dénomination des assemblages (cahier des charges).', '“Edelzwicker” = the name for blends (rulebook).')),
    dict(id='als-pinot-noir', aoc='Alsace', alias=['Alsace Pinot Noir', 'Pinot Noir d’Alsace'], zone='als', col=('Rouge', 'Red'),
         grapes=('Pinot noir', 'Pinot Noir'),
         fr='Robe rubis clair. Cerise, framboise, griotte, une note de sous-bois. Bouche légère et fraîche, tanins fins. Le seul cépage '
            'rouge d’une région de blancs, qui donne aussi ses rosés et ses crémants rosés ; il a obtenu en 2022 ses premiers grands crus.',
         en='Light ruby. Cherry, raspberry, morello, a hint of undergrowth. Light, fresh palate, fine tannins. The only red grape of a white '
            'wine region, which also makes its rosés and rosé crémants; it gained its first grands crus in 2022.',
         why=('Rouges et rosés « issus du seul cépage pinot noir » (cahier des charges) ; grands crus rouges depuis 2022.',
              'Reds and rosés “from Pinot Noir alone” (rulebook); red grands crus since 2022.')),
    dict(id='als-klevener', aoc='Alsace', alias=['Klevener de Heiligenstein', 'Alsace Klevener de Heiligenstein'], zone='als', col=WHITE,
         grapes=('Savagnin rose', 'Savagnin Rose'),
         fr='Robe or pâle. Rose discrète, épices douces, coing, noisette. Bouche plus retenue et plus fraîche qu’un gewurztraminer, '
            'longue. Un cépage cousin du traminer, introduit au XVIII<sup>e</sup> siècle par un maire de village et cultivé autour '
            'de quelques communes seulement, au nord d’Obernai.',
         en='Pale gold. Discreet rose, sweet spice, quince, hazelnut. More restrained and fresher than a Gewurztraminer, long. A grape '
            'related to Traminer, introduced in the 18th century by a village mayor and grown around only a few communes north of Obernai.',
         why=('Le Klevener de Heiligenstein (savagnin rose), dénomination propre à quelques communes ; introduit vers 1742.',
              'Klevener de Heiligenstein (Savagnin Rose), a denomination limited to a few communes; introduced around 1742.')),
    dict(id='als-vt', aoc='Alsace', alias=['Alsace Vendanges Tardives', 'Vendanges Tardives'], zone='als',
         col=('Blanc moelleux (vendanges tardives)', 'Sweet white (late harvest)'), grapes=('Gewurztraminer, pinot gris, riesling ou muscat', 'Gewurztraminer, Pinot Gris, Riesling or Muscat'),
         fr='Robe or soutenu. Fruits confits, coing, épices, miel, une note de surmaturité. Bouche riche et douce, mais tendue par l’acidité. '
            'Des raisins laissés sur pied longtemps après la récolte normale, d’un seul des quatre cépages autorisés pour cette mention.',
         en='Deep gold. Candied fruit, quince, spice, honey, an overripe note. Rich, sweet palate, yet taut with acidity. Grapes left on the '
            'vine long after the normal harvest, from just one of the four grapes allowed for this mention.',
         why=('Mention « Vendanges tardives » : gewurztraminer, pinot gris, riesling, muscat (cahier des charges).',
              'The “Vendanges tardives” mention: Gewurztraminer, Pinot Gris, Riesling, Muscat (rulebook).')),
    dict(id='als-sgn', aoc='Alsace', alias=['Alsace Sélection de Grains Nobles', 'Sélection de Grains Nobles', 'SGN'], zone='als',
         col=('Blanc liquoreux (grains nobles)', 'Sweet white (noble rot)'), grapes=('Gewurztraminer, pinot gris, riesling ou muscat', 'Gewurztraminer, Pinot Gris, Riesling or Muscat'),
         fr='Robe vieil or. Abricot sec, miel, safran, agrumes confits, ce « rôti » de la pourriture noble. Bouche liquoreuse, d’une '
            'concentration et d’une longueur immenses. Les grains botrytisés sont cueillis un à un en plusieurs passages ; une mention '
            'rare, que l’on ne produit pas tous les ans.',
         en='Old gold. Dried apricot, honey, saffron, candied citrus, the “roasted” character of noble rot. A sweet palate of immense '
            'concentration and length. Botrytised berries are picked one by one in several passes; a rare mention, not made every year.',
         why=('Mention « Sélection de grains nobles », réservée aux mêmes quatre cépages, grains atteints de pourriture noble.',
              'The “Sélection de grains nobles” mention, reserved for the same four grapes, from noble-rot berries.')),
    # ------------------------------------------------------------------ Crémant
    dict(id='cremant-als-b', aoc='Crémant d\'Alsace', alias=['Cremant d Alsace', 'Crémant d’Alsace'], zone='als',
         col=('Blanc effervescent', 'Sparkling white'), grapes=('Pinot blanc, auxerrois, riesling, chardonnay…', 'Pinot Blanc, Auxerrois, Riesling, Chardonnay…'),
         fr='Robe jaune pâle aux reflets verts, mousse fine et légère. Fruits frais, puis notes beurrées et de pain grillé après l’élevage '
            'sur lies. Bouche vive, à dominante acide, presque toujours brut. Le crémant le plus vendu de France, élaboré dans une '
            'région de vins tranquilles de cépage.',
         en='Pale yellow with green tints, fine light mousse. Fresh fruit, then buttery and toasted-bread notes after ageing on the lees. '
            'Lively, acid-led palate, almost always brut. France’s best-selling crémant, made in a region of single-grape still wines.',
         why=('« Mousse fine et légère », « notes beurrées ou de pain grillé », surtout « brut » (cahier des charges) ; premier crémant de France en volume.',
              '“Fine, light mousse”, “buttery or toasted-bread notes”, mostly “brut” (rulebook); France’s top crémant by volume.')),
    dict(id='cremant-als-rs', aoc='Crémant d\'Alsace', alias=['Cremant d Alsace rosé', 'Crémant d’Alsace rosé'], zone='als',
         col=('Rosé effervescent', 'Sparkling rosé'), grapes=('Pinot noir seul', 'Pinot Noir only'),
         fr='Robe rose transparente. Fraise, framboise, groseille. Bouche fraîche et fine, bulles légères. Un rosé effervescent qui ne peut '
            'être fait que d’un seul cépage rouge, le seul autorisé dans sa région.',
         en='Transparent pink. Strawberry, raspberry, redcurrant. Fresh, fine palate, light bubbles. A sparkling rosé that may be made '
            'from only one red grape, the only one allowed in its region.',
         why=('Rosés « issus du seul cépage pinot noir » (cahier des charges du Crémant d’Alsace).', 'Rosés “from Pinot Noir alone” (Crémant d’Alsace rulebook).')),
    # ------------------------------------------------------------------ grands crus
    dict(id='gc-rangen', aoc=GC, alias=gc_alias('Rangen'), zone='als_gc', col=WHITE, grapes=('Riesling, pinot gris ou gewurztraminer', 'Riesling, Pinot Gris or Gewurztraminer'),
         fr='Robe or. Fumé, pierre chaude, agrumes confits, épices. Bouche puissante, d’une minéralité presque brûlante. Le grand cru le plus '
            'au sud, à Thann, sur des pentes vertigineuses de roches volcaniques au-dessus de la Thur, dominées par une petite chapelle.',
         en='Gold. Smoke, hot stone, candied citrus, spice. Powerful palate with an almost burning minerality. The southernmost grand cru, '
            'at Thann, on dizzying slopes of volcanic rock above the Thur, overlooked by a small chapel.',
         why=('Rangen de Thann : « roches volcaniques sédimentaires… tufs volcaniques, andésite » (cahier des charges) ; chapelle Saint-Urbain.',
              'Rangen at Thann: “volcanic sedimentary rocks… volcanic tuffs, andesite” (rulebook); Saint-Urbain chapel.')),
    dict(id='gc-schlossberg', aoc=GC, alias=gc_alias('Schlossberg'), zone='als_gc', col=WHITE, grapes=('Riesling surtout', 'Mostly Riesling'),
         fr='Robe or pâle. Agrumes, fleurs, pierre à fusil. Bouche droite, ciselée, minérale. Terrasses de granite sous les ruines d’un '
            'château, entre Kientzheim et Kaysersberg ; c’est le tout premier grand cru reconnu en Alsace, en 1975.',
         en='Pale gold. Citrus, flowers, flint. Straight, chiselled, mineral palate. Granite terraces below castle ruins, between Kientzheim '
            'and Kaysersberg; it was the very first grand cru recognised in Alsace, in 1975.',
         why=('« Alsace grand cru Schlossberg est reconnue en 1975 » (cahier des charges) : le premier.', '“Alsace grand cru Schlossberg was recognised in 1975” (rulebook): the first.')),
    dict(id='gc-kaefferkopf', aoc=GC, alias=gc_alias('Kaefferkopf'), zone='als_gc', col=WHITE,
         grapes=('Gewurztraminer, riesling, pinot gris — seuls ou assemblés', 'Gewurztraminer, Riesling, Pinot Gris — alone or blended'),
         fr='Robe or. Rose, épices, agrumes, fruits jaunes. Bouche ample et complexe. Coteau d’Ammerschwihr, le dernier des 51 grands crus '
            'reconnus (2007) ; il est l’un des rares à autoriser l’assemblage, avec le gewurztraminer comme cépage principal.',
         en='Gold. Rose, spice, citrus, yellow fruit. Ample, complex palate. A slope at Ammerschwihr, the last of the 51 grands crus to be '
            'recognised (2007); it is one of the few to allow blends, with Gewurztraminer as the main grape.',
         why=('Kaefferkopf : 51e grand cru (2007), assemblage permis « cépage principal : gewurztraminer » (cahier des charges).',
              'Kaefferkopf: the 51st grand cru (2007), blends allowed with “main grape: Gewurztraminer” (rulebook).')),
    dict(id='gc-altenberg-bergheim', aoc=GC, alias=gc_alias('Altenberg de Bergheim'), zone='als_gc', col=('Blanc (assemblage)', 'White (blend)'),
         grapes=('Riesling, avec gewurztraminer et pinot gris, souvent complantés', 'Riesling, with Gewurztraminer and Pinot Gris, often interplanted'),
         fr='Robe jaune doré. Discret à l’attaque, puis volumineux, fruité, souvent marqué par la pourriture noble mais toujours salivant ; '
            'parfois des arômes de fossiles. Jamais techniquement sec. Moûts jamais enrichis, apogée après quinze à vingt ans, et des '
            'vignes où plusieurs cépages poussent mêlés.',
         en='Golden yellow. Discreet on the attack, then voluminous, fruity, often marked by noble rot yet always mouth-watering; sometimes '
            'fossil-like aromas. Never technically dry. Musts never enriched, a peak after fifteen to twenty years, and vineyards where '
            'several grapes grow mixed together.',
         why=('« Apogée après 15 à 20 ans… mouts jamais enrichis… arômes de fossiles », assemblage riesling majoritaire (cahier des charges).',
              '“Peak after 15–20 years… musts never enriched… fossil aromas”, Riesling-led blend (rulebook).')),
    dict(id='gc-zotzenberg', aoc=GC, alias=gc_alias('Zotzenberg'), zone='als_gc', col=WHITE, grapes=('Sylvaner', 'Sylvaner'),
         fr='Robe or pâle. Agrumes, herbes, une touche fumée. Bouche plus dense et plus longue qu’on ne l’attend de ce cépage. Coteau de '
            'Mittelbergheim : le seul grand cru où l’on peut revendiquer un vin d’un cépage que les autres grands crus ignorent.',
         en='Pale gold. Citrus, herbs, a smoky touch. Denser and longer than one expects from this grape. A slope at Mittelbergheim: the only '
            'grand cru where a wine can be claimed from a grape the other grands crus ignore.',
         why=('Zotzenberg, seul grand cru autorisant le sylvaner (cahier des charges).', 'Zotzenberg, the only grand cru allowing Sylvaner (rulebook).')),
    dict(id='gc-hengst-r', aoc=GC, alias=gc_alias('Hengst'), zone='als_gc', col=('Rouge', 'Red'), grapes=('Pinot noir', 'Pinot Noir'),
         fr='Robe rubis profond. Cerise noire, épices, une note minérale. Bouche structurée, tanins fins et serrés. Coteau marno-calcaire de '
            'Wintzenheim, grand cru pour ses blancs depuis 1983 — et, depuis 2022, l’un des trois premiers grands crus rouges d’Alsace.',
         en='Deep ruby. Black cherry, spice, a mineral note. Structured palate, fine, tight tannins. A marl-limestone slope at Wintzenheim, '
            'grand cru for its whites since 1983 — and, since 2022, one of Alsace’s first three red grands crus.',
         why=('Hengst « reconnue en 1983 pour les vins blancs puis en 2022 pour les vins rouges » (cahier des charges), avec Kirchberg de Barr et Vorbourg.',
              'Hengst “recognised in 1983 for whites, then in 2022 for reds” (rulebook), with Kirchberg de Barr and Vorbourg.')),
    dict(id='gc-brand', aoc=GC, alias=gc_alias('Brand'), zone='als_gc', col=WHITE, grapes=('Riesling surtout', 'Mostly Riesling'),
         fr='Robe or. Agrumes mûrs, pêche, une note de pierre chauffée. Bouche ample et solaire, d’une belle tension. Un coteau de granite à '
            'l’entrée de la vallée de Munster, au-dessus de Turckheim, largement ensoleillé et balayé par le foehn ; son nom évoque un '
            'incendie légendaire.',
         en='Gold. Ripe citrus, peach, a note of heated stone. Ample, sunny palate with fine tension. A granite slope at the mouth of the '
            'Munster valley, above Turckheim, very sunny and swept by the foehn wind; its name recalls a legendary fire.',
         why=('Brand (« brûlé ») à Turckheim : « soumis aux vents (foehn)… largement ensoleillé » (cahier des charges).',
              'Brand (“burnt”) at Turckheim: “exposed to the foehn… very sunny” (rulebook).')),
    dict(id='gc-kitterle', aoc=GC, alias=gc_alias('Kitterlé'), zone='als_gc', col=WHITE, grapes=('Riesling, gewurztraminer, pinot gris', 'Riesling, Gewurztraminer, Pinot Gris'),
         fr='Robe or. Fruits mûrs, fumé, une touche épicée. Bouche puissante et généreuse. Un éperon de grès rose des Vosges au nord de '
            'Guebwiller, aux pentes si raides qu’on y travaille en terrasses.',
         en='Gold. Ripe fruit, smoke, a spicy touch. Powerful, generous palate. A spur of pink Vosges sandstone north of Guebwiller, with '
            'slopes so steep they are worked in terraces.',
         why=('Kitterlé : « éperon… grès vosgien grossier » au nord de Guebwiller (cahier des charges).', 'Kitterlé: “a spur… coarse Vosges sandstone” north of Guebwiller (rulebook).')),
    # ------------------------------------------------------------------ Lorraine
    dict(id='toul-gris', aoc='Côtes de Toul', alias=['Cotes de Toul'], zone='lorraine', col=('Vin gris', 'Vin gris'),
         grapes=('Gamay et pinot noir', 'Gamay and Pinot Noir'),
         fr='Robe saumonée brillante. Fruits frais, groseille, pêche. Bouche sèche, légère, vive, gourmande. Pressé immédiatement comme un '
            'blanc, ce rosé pâle est « indissociable de l’identité » d’une région de l’Est plus connue pour la mirabelle ; l’appellation '
            'cultive aussi l’aubin, un cépage blanc presque introuvable ailleurs.',
         en='Bright salmon. Fresh fruit, redcurrant, peach. Dry, light, lively, tempting. Pressed straight away like a white, this pale rosé '
            'is “inseparable from the identity” of an eastern region better known for mirabelle plums; the appellation also grows Aubin, '
            'a white grape almost impossible to find elsewhere.',
         why=('« Indissociable de l’identité lorraine, le vin gris » (cahier des charges) ; gamay et pinot noir ; cépage aubin.',
              '“Inseparable from Lorraine’s identity, vin gris” (rulebook); Gamay and Pinot Noir; the Aubin grape.')),
    dict(id='moselle-b', aoc='Moselle', alias=[], zone='lorraine', col=WHITE, grapes=('Auxerrois, müller-thurgau, pinot gris', 'Auxerrois, Müller-Thurgau, Pinot Gris'),
         fr='Robe or pâle. Fleurs, fruits blancs, une légère note d’agrumes. Bouche légère, fine et fraîche. Coteaux de la vallée d’une '
            'rivière qui file vers le Luxembourg et l’Allemagne ; la seule AOC française où le müller-thurgau est un cépage principal.',
         en='Pale gold. Flowers, white fruit, a light citrus note. Light, fine, fresh palate. Slopes in the valley of a river heading for '
            'Luxembourg and Germany; the only French AOC where Müller-Thurgau is a main grape.',
         why=('Blancs « légers et fins… notes florales » (cahier des charges) ; auxerrois et müller-thurgau principaux.',
              'Whites “light and fine… floral notes” (rulebook); Auxerrois and Müller-Thurgau as main grapes.')),
]
