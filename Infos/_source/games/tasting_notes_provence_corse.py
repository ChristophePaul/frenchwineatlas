"""Provence & Corsica batch for « Goûtez votre savoir » (see tasting_notes.py for the field list).
Descriptors and most clues from the CDCs (Les Baux and Pierrevert have no usable lien section; Pierrevert not written).
"""

ZONES_PC = {
    'provence': ('Provence', 'Provence'),
    'corse': ('Corse', 'Corsica'),
}
AOC_ZONE_PC = {a: 'provence' for a in ('Côtes de Provence', 'Bandol', 'Cassis', 'Bellet', 'Palette', 'Coteaux d\'Aix-en-Provence',
                                      'Coteaux Varois en Provence', 'Les Baux-de-Provence', 'Pierrevert')}
AOC_ZONE_PC.update({a: 'corse' for a in ('Patrimonio', 'Ajaccio', 'Vin de Corse', 'Muscat du Cap Corse')})

RED = ('Rouge tranquille sec', 'Still dry red')
ROSE = ('Rosé sec', 'Dry rosé')
WHITE = ('Blanc sec', 'Dry white')

NOTES_PC = [
    # ------------------------------------------------------------------ Provence
    dict(id='cdp-rs', aoc='Côtes de Provence', alias=['Cotes de Provence', 'Côtes de Provence Sainte-Victoire'], zone='provence', col=ROSE,
         grapes=('Grenache, cinsaut, syrah, mourvèdre, tibouren', 'Grenache, Cinsault, Syrah, Mourvèdre, Tibouren'),
         fr='Robe rose très pâle, presque transparente. Agrumes, pêche blanche, fruits exotiques, petits fruits rouges, une note minérale. '
            'Bouche équilibrée entre rondeur et vivacité. La plus vaste appellation de la région, des plages aux collines des Maures et de '
            'l’Esterel, où le rosé représente près de neuf bouteilles sur dix — et où pousse un vieux cépage local, le tibouren.',
         en='Very pale, almost transparent pink. Citrus, white peach, exotic fruit, small red berries, a mineral note. Balanced between '
            'roundness and liveliness. The region’s largest appellation, from the beaches to the Maures and Esterel hills, where rosé makes '
            'up nearly nine bottles in ten — and where an old local grape, Tibouren, still grows.',
         why=('« Les vins rosés… 89 % de la production », Maures et Esterel, tibouren cépage principal (cahier des charges).',
              '“Rosés… 89 % of production”, Maures and Esterel, Tibouren as a main grape (rulebook).')),
    dict(id='bandol-r', aoc='Bandol', alias=[], zone='provence', col=RED, grapes=('Mourvèdre (au moins 50 %)', 'Mourvèdre (at least 50 %)'),
         fr='Robe sombre. Fruits noirs, réglisse, garrigue, cuir, une note de truffe avec l’âge. Bouche puissante, charpentée, tannique, de '
            'longue garde. Au moins dix-huit mois en foudre, d’un cépage tardif qui ne mûrit bien que face à la mer, dans un amphithéâtre '
            'de restanques abrité du mistral ; un auteur de 1787 parlait déjà de « soleil en bouteille ».',
         en='Dark. Black fruit, liquorice, garrigue, leather, a truffle note with age. Powerful, structured, tannic, for long ageing. At least '
            'eighteen months in large casks, from a late grape that ripens well only facing the sea, in an amphitheatre of terraces sheltered '
            'from the mistral; a 1787 author already spoke of “sunshine in a bottle”.',
         why=('Mourvèdre au moins 50 %, « élevage minimum de 18 mois en fûts ou en foudres », restanques, « soleil en bouteille » (cahier des charges).',
              'At least 50 % Mourvèdre, “minimum 18 months in casks or foudres”, terraces, “sunshine in a bottle” (rulebook).')),
    dict(id='bandol-rs', aoc='Bandol', alias=['Bandol rosé'], zone='provence', col=ROSE, grapes=('Mourvèdre (au moins 20 %), cinsaut, grenache', 'Mourvèdre (at least 20 %), Cinsault, Grenache'),
         fr='Robe pâle couleur d’églantine. Fruits rouges, agrumes, épices douces. Bouche plus tannique et plus structurée que les autres rosés '
            'de la région, capable de vieillir quelques années. Le cépage rouge tardif de ce golfe y entre toujours.',
         en='Pale, wild-rose colour. Red fruit, citrus, sweet spice. More tannic and structured than the region’s other rosés, able to age a '
            'few years. The gulf’s late-ripening red grape always goes into it.',
         why=('Rosé « églantine », mourvèdre obligatoire (20 % minimum), « plus tannique que les autres vins rosés provençaux » (cahier des charges).',
              'A “wild-rose” rosé, Mourvèdre required (20 % minimum), “more tannic than other Provence rosés” (rulebook).')),
    dict(id='cassis-b', aoc='Cassis', alias=[], zone='provence', col=WHITE, grapes=('Marsanne et clairette', 'Marsanne and Clairette'),
         fr='Robe or pâle. Fleurs, fruits blancs, notes balsamiques, et une vivacité presque salée venue de la mer. Bouche ronde et sèche, '
            'le vin de la bouillabaisse. Terrasses d’une seule commune lovée dans une baie, au pied des plus hautes falaises maritimes de '
            'France ; c’était l’une des six toutes premières AOC, en 1936.',
         en='Pale gold. Flowers, white fruit, balsamic notes, and an almost salty liveliness from the sea. Round, dry palate, the bouillabaisse '
            'wine. Terraces of a single commune nestled in a bay, below France’s highest sea cliffs; it was one of the first six AOCs, in 1936.',
         why=('Cap Canaille (416 m), « caractère iodé, vivacité presque salée », bouillabaisse (cahier des charges) ; AOC du 15 mai 1936.',
              'Cap Canaille (416 m), “iodine character, almost salty liveliness”, bouillabaisse (rulebook); AOC of 15 May 1936.')),
    dict(id='bellet-rs', aoc='Bellet', alias=[], zone='provence', col=ROSE, grapes=('Braquet, fuella nera, grenache', 'Braquet, Fuella Nera, Grenache'),
         fr='Robe pâle. Fleurs sauvages, rose ancienne, violette, avec une note iodée en bouche. Fin et original. Quelques collines au-dessus '
            'du Var, à l’intérieur même des limites d’une grande ville de la Côte d’Azur, avec deux cépages locaux qu’on ne trouve guère '
            'ailleurs.',
         en='Pale. Wild flowers, old rose, violet, with an iodine note on the palate. Fine and original. A few hills above the Var, inside the '
            'city limits of a big Riviera town, with two local grapes found hardly anywhere else.',
         why=('Bellet, sur la commune de Nice ; braquet et fuella nera ; rosés « rose ancienne… notes iodées » (cahier des charges).',
              'Bellet, within the commune of Nice; Braquet and Fuella Nera; rosés “old rose… iodine notes” (rulebook).')),
    dict(id='palette-b', aoc='Palette', alias=[], zone='provence', col=WHITE, grapes=('Clairette et clairette rose, et de très vieux cépages', 'Clairette and Clairette Rose, and very old varieties'),
         fr='Robe or. Fleurs, notes balsamiques et de pignons de pin. Bouche vive, longue, au potentiel de garde étonnant. Un petit cirque '
            'boisé aux portes d’Aix, au pied de la montagne chère à Cézanne, qui a conservé des cépages disparus partout ailleurs dans le Midi.',
         en='Gold. Flowers, balsamic and pine-nut notes. Lively, long palate with astonishing ageing potential. A small wooded cirque at the gates '
            'of Aix, below the mountain Cézanne loved, which has kept grape varieties that vanished everywhere else in the south.',
         why=('« Arômes floraux, balsamiques et de pignons de pins… potentiel de garde étonnant », hameau du Tholonet sous la Sainte-Victoire (cahier des charges).',
              '“Floral, balsamic and pine-nut aromas… astonishing ageing potential”, a hamlet of Le Tholonet below Sainte-Victoire (rulebook).')),
    dict(id='aix-r', aoc='Coteaux d\'Aix-en-Provence', alias=['Coteaux d Aix en Provence', 'Coteaux d’Aix-en-Provence'], zone='provence', col=RED,
         grapes=('Grenache, mourvèdre, syrah, avec cabernet-sauvignon', 'Grenache, Mourvèdre, Syrah, with Cabernet Sauvignon'),
         fr='Robe rubis. Violette, puis foin, laurier, tabac, et avec l’âge cannelle et fourrure. Bouche équilibrée et fruitée, plénitude après deux '
            'ou trois ans. De la Durance à la mer et du Rhône à la Sainte-Victoire ; le cabernet-sauvignon s’y mêle souvent aux cépages méditerranéens.',
         en='Ruby. Violet, then hay, bay leaf, tobacco, and with age cinnamon and fur. Balanced, fruity palate, at its best after two or three years. '
            'From the Durance to the sea and from the Rhône to Sainte-Victoire; Cabernet Sauvignon often joins the Mediterranean grapes.',
         why=('« Foin, laurier, tabac… cannelle ou fourrure », 47 communes des Bouches-du-Rhône et 2 du Var (cahier des charges).',
              '“Hay, bay leaf, tobacco… cinnamon or fur”, 47 communes in the Bouches-du-Rhône and 2 in the Var (rulebook).')),
    dict(id='varois-rs', aoc='Coteaux Varois en Provence', alias=['Coteaux Varois'], zone='provence', col=ROSE,
         grapes=('Cinsaut, grenache, syrah', 'Cinsault, Grenache, Syrah'),
         fr='Robe rose franc et vif. Fruits rouges frais, puis thym, romarin, genévrier : la garrigue. Fraîcheur et structure. Vingt-huit communes '
            'autour de Brignoles, dans la Provence calcaire, au pied d’un massif qui dépasse les mille mètres.',
         en='Bright, frank pink. Fresh red fruit, then thyme, rosemary, juniper: the garrigue. Freshness and structure. Twenty-eight communes around '
            'Brignoles, in limestone Provence, below a massif rising above a thousand metres.',
         why=('28 communes autour de Brignoles, massif de la Sainte-Baume, « thym, romarin, genêt, genévrier » (cahier des charges).',
              '28 communes around Brignoles, the Sainte-Baume massif, “thyme, rosemary, broom, juniper” (rulebook).')),
    dict(id='baux-r', aoc='Les Baux-de-Provence', alias=['Baux de Provence', 'Les Baux'], zone='provence', col=RED,
         grapes=('Grenache, syrah, mourvèdre, cabernet-sauvignon', 'Grenache, Syrah, Mourvèdre, Cabernet Sauvignon'),
         fr='Robe sombre. Fruits noirs, olive noire, garrigue, épices. Bouche ample, tanins serrés. Vignes au pied des Alpilles, autour d’un '
            'village perché sur un éperon de calcaire blanc ; presque tous les domaines y travaillent en agriculture biologique.',
         en='Dark. Black fruit, black olive, garrigue, spice. Ample palate, tight tannins. Vines below the Alpilles, around a village perched on a spur '
            'of white limestone; almost all the estates farm organically.',
         why=('Les Alpilles et le village des Baux ; une des plus fortes proportions de vignes bio de France.',
              'The Alpilles and the village of Les Baux; one of the highest shares of organic vineyards in France.')),
    # ------------------------------------------------------------------ Corsica
    dict(id='patrimonio-r', aoc='Patrimonio', alias=[], zone='corse', col=RED, grapes=('Nielluccio (au moins 90 %)', 'Nielluccio (at least 90 %)'),
         fr='Robe rubis à grenat. Cassis, mûre, puis épices, notes grillées et balsamiques. Bouche charpentée, tannique, chaleureuse, de garde. '
            'Un amphithéâtre ouvert sur le golfe de Saint-Florent, au pied du Cap, fermé au sud par un désert de maquis — la plus ancienne AOC '
            'de son île.',
         en='Ruby to garnet. Blackcurrant, blackberry, then spice, toasty and balsamic notes. Structured, tannic, warm, for ageing. An amphitheatre '
            'opening onto the Gulf of Saint-Florent, at the foot of the Cape, closed to the south by a scrubland desert — the oldest AOC on its island.',
         why=('Nielluccio « au moins 90 % », golfe de Saint-Florent, désert des Agriates (cahier des charges) ; première AOC corse (1968).',
              'Nielluccio “at least 90 %”, Gulf of Saint-Florent, Agriates desert (rulebook); Corsica’s first AOC (1968).')),
    dict(id='ajaccio-r', aoc='Ajaccio', alias=[], zone='corse', col=RED, grapes=('Sciaccarello', 'Sciaccarello'),
         fr='Robe brillante, d’intensité moyenne. Petits fruits rouges, cassis, amande, poivre. Bouche fine et élégante, tanins présents mais '
            'discrets. Vallées granitiques de la côte ouest, du golfe de Porto à celui de Valinco, autour de la ville natale de Napoléon.',
         en='Bright, medium intensity. Small red berries, blackcurrant, almond, pepper. Fine, elegant palate, present but discreet tannins. Granite '
            'valleys of the west coast, from the Gulf of Porto to that of Valinco, around Napoleon’s birthplace.',
         why=('Rouges « très marqués par le sciaccarello… petits fruits rouges, cassis, amande, épices », du golfe de Porto au Valinco (cahier des charges).',
              'Reds “strongly marked by Sciaccarello… small red fruit, blackcurrant, almond, spice”, from Porto to Valinco (rulebook).')),
    dict(id='corse-rs', aoc='Vin de Corse', alias=['Corse', 'Vin de Corse Porto-Vecchio', 'Vin de Corse Sartène', 'Vin de Corse Calvi', 'Vin de Corse Figari'],
         zone='corse', col=ROSE, grapes=('Sciaccarello, nielluccio, grenache', 'Sciaccarello, Nielluccio, Grenache'),
         fr='Robe pâle. Fruits rouges, agrumes, fleurs, une touche de maquis. Bouche fraîche et intense. Un vignoble presque entièrement littoral, '
            'qui fait le tour de l’île sur 110 communes ; les rosés y représentent environ six bouteilles sur dix, et cinq secteurs peuvent '
            'ajouter leur nom.',
         en='Pale. Red fruit, citrus, flowers, a touch of maquis. Fresh, intense palate. An almost entirely coastal vineyard ringing the island over '
            '110 communes; rosés make up about six bottles in ten, and five areas may add their name.',
         why=('« Vignoble littoral », 110 communes, rosés « environ 60 % » ; dénominations Calvi, Figari, Porto-Vecchio, Sartène, Coteaux du Cap Corse (cahier des charges).',
              '“A coastal vineyard”, 110 communes, rosés “about 60 %”; denominations Calvi, Figari, Porto-Vecchio, Sartène, Coteaux du Cap Corse (rulebook).')),
    dict(id='cap-corse-b', aoc='Vin de Corse', alias=['Vin de Corse Coteaux du Cap Corse', 'Coteaux du Cap Corse'], zone='corse', col=WHITE,
         grapes=('Vermentino (au moins 80 %)', 'Vermentino (at least 80 %)'), area=('Corse · Cap Corse', 'Corsica · Cap Corse'),
         fr='Robe pâle aux reflets verts. Fleurs blanches, agrumes, amande, une note saline. Bouche vive et minérale. Le cépage blanc roi de '
            'l’île, sur les schistes du doigt montagneux qui pointe au nord vers la Ligurie.',
         en='Pale with green tints. White flowers, citrus, almond, a saline note. Lively, mineral palate. The island’s king white grape, on the '
            'schists of the mountainous finger pointing north towards Liguria.',
         why=('Dénomination Coteaux du Cap Corse : vermentino au moins 80 % (cahier des charges).', 'The Coteaux du Cap Corse denomination: at least 80 % Vermentino (rulebook).')),
    dict(id='muscat-cap-corse', aoc='Muscat du Cap Corse', alias=[], zone='corse', col=('Vin doux naturel (blanc)', 'Vin doux naturel (white)'),
         grapes=('Muscat à petits grains', 'Muscat à Petits Grains'),
         fr='Robe or. Raisin frais, agrumes confits, miel, abricot, fleurs. Bouche douce, fraîche, très aromatique. Un vin muté au pied des '
            'falaises du nord de l’île, la seule appellation de vin doux naturel de Corse.',
         en='Gold. Fresh grape, candied citrus, honey, apricot, flowers. Sweet, fresh, very aromatic palate. A fortified wine from below the cliffs '
            'of the island’s north, Corsica’s only vin doux naturel appellation.',
         why=('Muscat à petits grains, mutage ; seul VDN de Corse (décret 2011-781).', 'Muscat à Petits Grains, fortified; Corsica’s only VDN (decree 2011-781).')),
]
