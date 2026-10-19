"""Jura, Savoie & Bugey batch for « Goûtez votre savoir » (see tasting_notes.py for the field list).
Descriptors and most clues from the CDCs (all have a filled-in « lien à l'origine », except Crémant du Jura and Bugey).
Vin de Savoie notes accept their dénomination (Apremont, Chignin-Bergeron, Arbin…) as an answer.
"""

ZONES_JS = {
    'jura': ('Jura', 'Jura'),
    'savoie': ('Savoie', 'Savoie'),
    'bugey': ('Bugey (Ain)', 'Bugey (Ain)'),
}
AOC_ZONE_JS = {'Arbois': 'jura', 'Château-Chalon': 'jura', 'Côtes du Jura': 'jura', 'Crémant du Jura': 'jura', "L'Étoile": 'jura',
               'Macvin du Jura': 'jura', 'Vin de Savoie': 'savoie', 'Roussette de Savoie': 'savoie', 'Seyssel': 'savoie',
               'Bugey': 'bugey', 'Roussette du Bugey': 'bugey'}

WHITE = ('Blanc sec', 'Dry white')
JAUNE = ('Vin jaune (blanc sec, élevé sous voile)', 'Vin jaune (dry white aged under flor)')


def sav(fr, en):
    return (f'Savoie · {fr}', f'Savoie · {en}')


NOTES_JS = [
    # ------------------------------------------------------------------ Jura
    dict(id='chateau-chalon', aoc='Château-Chalon', alias=['Chateau-Chalon', 'Château Chalon'], zone='jura', col=JAUNE,
         grapes=('Savagnin', 'Savagnin'),
         fr='Robe jaune doré prononcé. Noix fraîche, pomme très mûre, fruits confits, curry, cannelle, muscade : le « goût de jaune ». '
            'Bouche sèche, puissante, d’une longueur impressionnante. Élevé au moins six ans en fût sans jamais être complété, sous un '
            'voile de levures, puis mis en clavelin de 62 cl ; il se garde 50 à 100 ans. Une appellation qui ne produit que ce vin-là, '
            'autour d’un village perché sur un éperon rocheux.',
         en='Deep golden yellow. Fresh walnut, very ripe apple, candied fruit, curry, cinnamon, nutmeg: the “goût de jaune”. Dry, powerful '
            'palate of impressive length. Aged at least six years in barrel without ever being topped up, under a veil of yeast, then '
            'bottled in a 62 cl clavelin; it keeps 50 to 100 years. An appellation that makes nothing but this wine, around a village '
            'perched on a rocky spur.',
         why=('Seule AOC exclusivement en vin jaune ; « curry, cannelle, vanille, muscade », « 50 ans ou 100 ans » (cahier des charges).',
              'The only AOC exclusively for vin jaune; “curry, cinnamon, vanilla, nutmeg”, “50 or 100 years” (rulebook).')),
    dict(id='arbois-poulsard', aoc='Arbois', alias=['Arbois Pupillin', 'Pupillin'], zone='jura', col=('Rouge léger', 'Light red'),
         grapes=('Poulsard (ploussard)', 'Poulsard (Ploussard)'),
         fr='Robe rubis clair, presque rosée. Groseille, cerise, une note fumée et florale ; avec l’âge, sous-bois et champignon. Bouche '
            'légère, peu tannique. Un cépage local à la peau fine, roi du village de Pupillin, dans l’appellation de la ville natale '
            'de Louis Pasteur.',
         en='Light, almost pink ruby. Redcurrant, cherry, a smoky and floral note; with age, undergrowth and mushroom. Light palate, few '
            'tannins. A thin-skinned local grape, king of the village of Pupillin, in the appellation of Louis Pasteur’s home town.',
         why=('Poulsard, « teinte rubis clair caractéristique », « notamment sur la commune de Pupillin » (cahier des charges) ; Arbois, ville de Pasteur.',
              'Poulsard, “a characteristic light ruby tint”, “notably in the commune of Pupillin” (rulebook); Arbois, Pasteur’s town.')),
    dict(id='cdj-b', aoc='Côtes du Jura', alias=['Cotes du Jura'], zone='jura', col=('Blanc sec (ouillé ou typé)', 'Dry white'),
         grapes=('Chardonnay et savagnin', 'Chardonnay and Savagnin'),
         fr='Robe or pâle. Pierre à fusil, notes minérales, fruits frais, parfois une pointe de noix. Bouche vive, tendue, pleine de '
            'fraîcheur. L’assemblage des deux grands cépages blancs locaux, sur les marnes du « Revermont », la plus vaste appellation '
            'de sa petite région, entre la Bresse et le plateau.',
         en='Pale gold. Flint, mineral notes, fresh fruit, sometimes a hint of walnut. Lively, taut, very fresh palate. The blend of the two '
            'great local white grapes, on the marls of the “Revermont”, the largest appellation of its small region, between the Bresse '
            'and the plateau.',
         why=('« Assemblage des cépages chardonnay B et savagnin B… pierre à fusil » (cahier des charges).',
              '“A blend of Chardonnay and Savagnin… flint” (rulebook).')),
    dict(id='cdj-paille', aoc='Côtes du Jura', alias=['Cotes du Jura vin de paille', 'Vin de paille du Jura'], zone='jura',
         col=('Vin de paille (doux)', 'Vin de paille (sweet)'), grapes=('Chardonnay, savagnin, poulsard', 'Chardonnay, Savagnin, Poulsard'),
         fr='Robe ambrée. Pruneau, orange confite, miel, abricot sec. Bouche douce, onctueuse, d’une belle acidité. Des grappes séchées '
            'plusieurs semaines sur des claies ou suspendues avant d’être pressées ; on le vend dans un petit flacon de 37,5 cl.',
         en='Amber. Prune, candied orange, honey, dried apricot. Sweet, unctuous palate with good acidity. Bunches dried for several weeks '
            'on racks or hung up before pressing; it is sold in a small 37.5 cl bottle.',
         why=('Vin de paille « rappelant le pruneau ou l’orange confite… miel » (cahier des charges).', 'Vin de paille “recalling prune or candied orange… honey” (rulebook).')),
    dict(id='etoile-b', aoc='L\'Étoile', alias=['L Etoile', 'L’Étoile', 'Etoile'], zone='jura', col=WHITE, grapes=('Chardonnay et savagnin', 'Chardonnay and Savagnin'),
         fr='Robe or pâle. Pierre à fusil, notes minérales, fruits, une grande fraîcheur. Bouche tendue qui gagne à quelques années d’élevage. '
            'Une toute petite appellation au sud de Lons-le-Saunier, dont les sols sont parsemés de minuscules fossiles en forme d’étoiles — '
            'une des explications de son nom.',
         en='Pale gold. Flint, mineral notes, fruit, great freshness. A taut palate that benefits from a few years’ ageing. A tiny appellation '
            'south of Lons-le-Saunier, whose soils are scattered with tiny star-shaped fossils — one explanation of its name.',
         why=('« Sols particulièrement riches en petites étoiles, éléments… de crinoïdes » (cahier des charges).',
              '“Soils particularly rich in little stars, fragments… of crinoids” (rulebook).')),
    dict(id='cremant-jura', aoc='Crémant du Jura', alias=['Cremant du Jura'], zone='jura', col=('Blanc effervescent', 'Sparkling white'),
         grapes=('Chardonnay, pinot noir, trousseau (au moins 70 %)', 'Chardonnay, Pinot Noir, Trousseau (at least 70 %)'),
         fr='Robe pâle, bulles fines. Pomme, fleurs blanches, brioche, une touche de noisette. Bouche vive et fine. Méthode traditionnelle '
            'dans une région bien plus célèbre pour ses vins oxydatifs.',
         en='Pale, fine bubbles. Apple, white flowers, brioche, a touch of hazelnut. Lively, fine palate. Traditional method in a region far '
            'better known for its oxidative wines.',
         why=('Crémant : chardonnay, pinot noir et trousseau au moins 70 % de la cuvée (cahier des charges).', 'Crémant: Chardonnay, Pinot Noir and Trousseau at least 70 % (rulebook).')),
    dict(id='macvin', aoc='Macvin du Jura', alias=['Macvin'], zone='jura', col=('Vin de liqueur', 'Vin de liqueur'),
         grapes=('Savagnin, chardonnay, poulsard, trousseau, pinot noir', 'Savagnin, Chardonnay, Poulsard, Trousseau, Pinot Noir'),
         fr='Robe ambrée. Écorce d’orange, coing, fruits confits, pruneau, raisins secs, avec une note discrète de marc. Bouche grasse, '
            'onctueuse, équilibre entre sucre et alcool. Du moût de raisin dont on arrête la fermentation avec une eau-de-vie de marc '
            'de la même région, puis élevé en fût.',
         en='Amber. Orange peel, quince, candied fruit, prune, raisins, with a discreet note of marc. Rich, unctuous palate, balancing sugar '
            'and alcohol. Grape must whose fermentation is stopped with a marc brandy from the same region, then aged in barrel.',
         why=('« Arômes de marc… écorces d’orange et de coing » (cahier des charges) : moût muté au marc du Jura.',
              '“Marc aromas… orange peel and quince” (rulebook): must fortified with Jura marc.')),
    # ------------------------------------------------------------------ Savoie
    dict(id='savoie-apremont', aoc='Vin de Savoie', alias=['Apremont', 'Abymes', 'Les Abymes', 'Vin de Savoie Apremont', 'Vin de Savoie Abymes'],
         zone='savoie', col=WHITE, grapes=('Jacquère', 'Jacquère'), area=sav('Combe de Savoie & Chambéry', 'Combe de Savoie & Chambéry'),
         fr='Robe très pâle. Agrumes, fleurs blanches, pierre. Bouche légère, vive, souvent perlante car gardée sur lies fines. Le vin '
            'de la raclette, né sur les éboulis laissés au XIII<sup>e</sup> siècle par l’effondrement d’une montagne, le mont Granier.',
         en='Very pale. Citrus, white flowers, stone. Light, lively palate, often slightly prickly from being kept on fine lees. The raclette '
            'wine, grown on the scree left in the 13th century by the collapse of a mountain, Mont Granier.',
         why=('Jacquère, « souvent perlant » (cahier des charges) ; éboulement du mont Granier (1248) à l’origine des Abymes et d’Apremont.',
              'Jacquère, “often slightly sparkling” (rulebook); the 1248 Mont Granier landslide that formed Abymes and Apremont.')),
    dict(id='savoie-bergeron', aoc='Vin de Savoie', alias=['Chignin-Bergeron', 'Chignin Bergeron', 'Vin de Savoie Chignin-Bergeron'],
         zone='savoie', col=WHITE, grapes=('Roussanne (« bergeron »)', 'Roussanne (“Bergeron”)'), area=sav('Chignin', 'Chignin'),
         fr='Robe or. Abricot, coing, miel, amande. Bouche ample et ronde, plus riche que les autres blancs alpins. Un cépage rhodanien '
            'cultivé ici sous un nom local, sur les pentes ensoleillées sous les tours en ruine d’un village au sud-est de Chambéry.',
         en='Gold. Apricot, quince, honey, almond. Ample, round palate, richer than other Alpine whites. A Rhône grape grown here under a '
            'local name, on sunny slopes below the ruined towers of a village south-east of Chambéry.',
         why=('Dénomination Chignin-Bergeron : roussanne seule, appelée « bergeron » en Savoie.', 'The Chignin-Bergeron denomination: Roussanne alone, called “Bergeron” in Savoie.')),
    dict(id='savoie-mondeuse', aoc='Vin de Savoie', alias=['Arbin', 'Vin de Savoie Arbin', 'Mondeuse', 'Vin de Savoie Mondeuse'],
         zone='savoie', col=('Rouge', 'Red'), grapes=('Mondeuse', 'Mondeuse'), area=sav('Arbin', 'Arbin'),
         fr='Robe violacée profonde. Fruits noirs, violette, poivre. Bouche structurée, tannique, ample, mais avec beaucoup de vivacité. '
            'Le grand cépage rouge des Alpes, vinifié seul sur les coteaux d’Arbin, face à la combe de Savoie.',
         en='Deep purple. Black fruit, violet, pepper. Structured, tannic, ample palate, yet very lively. The great red grape of the Alps, '
            'made on its own on the slopes of Arbin, facing the Combe de Savoie.',
         why=('Mondeuse : « structurés, tanniques, amples, mais en conservant de la vivacité » ; Arbin = mondeuse seule (cahier des charges).',
              'Mondeuse: “structured, tannic, ample, yet keeping liveliness”; Arbin = Mondeuse alone (rulebook).')),
    dict(id='savoie-crepy', aoc='Vin de Savoie', alias=['Crépy', 'Crepy', 'Marignan', 'Marin', 'Ripaille', 'Vin de Savoie Crépy'],
         zone='savoie', col=WHITE, grapes=('Chasselas', 'Chasselas'), area=sav('rive du Léman', 'Lake Geneva shore'),
         fr='Robe très pâle aux reflets verts. Fleurs, tilleul, amande fraîche, un perlant léger. Bouche légère et désaltérante. Sur la '
            'rive française d’un grand lac, face à la Suisse ; le même cépage y donne les vins de Marin, Marignan et du château de Ripaille.',
         en='Very pale with green tints. Flowers, linden, fresh almond, a light prickle. Light, thirst-quenching palate. On the French shore '
            'of a great lake, facing Switzerland; the same grape makes the wines of Marin, Marignan and Ripaille castle.',
         why=('Dénominations Crépy, Marignan, Marin, Ripaille : chasselas, au bord du Léman (cahier des charges).',
              'The Crépy, Marignan, Marin, Ripaille denominations: Chasselas, on Lake Geneva (rulebook).')),
    dict(id='savoie-ayze', aoc='Vin de Savoie', alias=['Ayze', 'Vin de Savoie Ayze'], zone='savoie', col=('Blanc effervescent', 'Sparkling white'),
         grapes=('Gringet', 'Gringet'), area=sav('vallée de l’Arve', 'Arve valley'),
         fr='Robe pâle, bulles légères. Pomme, poire, fleurs, une note alpine herbacée. Bouche fraîche et délicate. Un village de la vallée '
            'de l’Arve, au pied du Mont-Blanc, qui cultive un cépage quasi unique au monde, longtemps sauvé par une poignée de vignerons.',
         en='Pale, light bubbles. Apple, pear, flowers, an Alpine herbal note. Fresh, delicate palate. A village in the Arve valley, below '
            'Mont Blanc, growing a grape almost unique in the world, long saved by a handful of growers.',
         why=('Dénomination Ayze : gringet, cépage quasi exclusif de ce village (cahier des charges).', 'The Ayze denomination: Gringet, a grape almost exclusive to this village (rulebook).')),
    dict(id='roussette-savoie', aoc='Roussette de Savoie', alias=['Roussette de Savoie Marestel', 'Marestel', 'Frangy'], zone='savoie', col=WHITE,
         grapes=('Altesse seule', 'Altesse only'),
         fr='Robe or pâle. Fruits blancs, miel, fleurs, amande. Attaque fraîche, puis de l’ampleur avec l’âge. Un cépage à part entière, '
            'qui aurait été rapporté de Chypre au Moyen Âge ; ses meilleurs coteaux, comme Marestel ou Frangy, ont leur propre nom.',
         en='Pale gold. White fruit, honey, flowers, almond. Fresh attack, then breadth with age. A grape of its own, said to have been brought '
            'back from Cyprus in the Middle Ages; its best slopes, such as Marestel or Frangy, have their own names.',
         why=('Altesse seule ; « fruits blancs et miel » ; dénominations Marestel, Frangy, Monterminod, Monthoux (cahier des charges).',
              'Altesse only; “white fruit and honey”; denominations Marestel, Frangy, Monterminod, Monthoux (rulebook).')),
    dict(id='seyssel-mousseux', aoc='Seyssel', alias=['Seyssel mousseux'], zone='savoie', col=('Blanc effervescent', 'Sparkling white'),
         grapes=('Molette et altesse', 'Molette and Altesse'),
         fr='Robe pâle, bulles fines. Fleurs, puis fruits cuits, pain d’épices, une note torréfiée. Attaque vive et parfumée. Une petite '
            'ville coupée en deux par le Rhône — et par une limite départementale — dont le mousseux associe un cépage rare, la molette, '
            'et l’altesse.',
         en='Pale, fine bubbles. Flowers, then cooked fruit, gingerbread, a roasted note. Lively, fragrant attack. A small town split in two '
            'by the Rhône — and by a département border — whose sparkling wine combines a rare grape, Molette, with Altesse.',
         why=('Mousseux « où domine le cépage molette associé obligatoirement au cépage altesse » (cahier des charges) ; Seyssel, Ain et Haute-Savoie.',
              'Sparkling wine “where Molette dominates, necessarily with Altesse” (rulebook); Seyssel, Ain and Haute-Savoie.')),
    # ------------------------------------------------------------------ Bugey
    dict(id='cerdon', aoc='Bugey', alias=['Bugey Cerdon', 'Cerdon'], zone='bugey', col=('Rosé effervescent doux', 'Sweet sparkling rosé'),
         grapes=('Gamay et poulsard', 'Gamay and Poulsard'),
         fr='Robe rose framboise, bulles légères. Fraise, framboise, groseille, bonbon. Bouche douce, fruitée, peu alcoolisée. Une fermentation '
            'unique achevée en bouteille, sans ajout de liqueur, dans une petite vallée de l’Ain ; les cépages viennent de Beaujolais et '
            'du Jura voisins.',
         en='Raspberry pink, light bubbles. Strawberry, raspberry, redcurrant, sweets. Sweet, fruity, low-alcohol palate. A single fermentation '
            'finished in bottle, with no added liqueur, in a small valley of the Ain; the grapes come from neighbouring Beaujolais and Jura.',
         why=('Dénomination Cerdon : « méthode ancestrale », gamay et poulsard (cahier des charges).', 'The Cerdon denomination: “méthode ancestrale”, Gamay and Poulsard (rulebook).')),
    dict(id='roussette-bugey', aoc='Roussette du Bugey', alias=['Roussette du Bugey Montagnieu'], zone='bugey', col=WHITE,
         grapes=('Altesse', 'Altesse'),
         fr='Robe or pâle aux reflets brillants. Fleurs blanches, puis, avec l’âge, une surprenante note de truffe blanche. Attaque vive '
            'et fraîche. Même cépage que de l’autre côté du Rhône, mais dans l’Ain ; deux dénominations minuscules, de 8 et 1,2 hectares.',
         en='Pale gold with bright tints. White flowers, then, with age, a surprising white-truffle note. Lively, fresh attack. The same grape '
            'as across the Rhône, but in the Ain; two tiny denominations, of 8 and 1.2 hectares.',
         why=('« Des notes de truffes blanches » ; Montagnieu 8 ha, Virieu-le-Grand 1,2 ha (cahier des charges).',
              '“White truffle notes”; Montagnieu 8 ha, Virieu-le-Grand 1.2 ha (rulebook).')),
]
