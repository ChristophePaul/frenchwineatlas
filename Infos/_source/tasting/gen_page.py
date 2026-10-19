"""Builds Infos/Tasting/Wine_Tasting.html — « Déguster le vin : l’équilibre » / "Tasting wine: the balance".

Source text: the user's « Equilibre du vin.docx » (A quick Glance at French Wine/), kept in its own words and
structure (EN), corrected where the science has moved on, translated to FR, with numbered sources.
The balance diagram is the user's sketch redrawn (interactive, fixed sector logic, 3 modes).
Shared look = Vine & Vineyard base.css (pro fold-outs, plates, lightbox).
Run:  python3 gen_page.py
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INFOS = HERE.parent.parent
sys.path.insert(0, str(INFOS / 'Vine_and_Vineyard' / '_source'))
from common import base_css, t, blk, plate, att, PRO_ICON  # noqa: E402

OUT = INFOS / 'Tasting' / 'Wine_Tasting.html'

# ------------------------------------------------------------------ sources
SOURCES = [
    ('peynaud', 'Peynaud É., Blouin J. (2013). <i>Le Goût du vin</i>, 5<sup>e</sup> éd. Dunod, Paris. — Trad. angl. <i>The Taste of Wine</i>, 2<sup>e</sup> éd., Wiley, 1996.',
                'Peynaud É., Blouin J. (2013). <i>Le Goût du vin</i>, 5th ed. Dunod, Paris. — English ed. <i>The Taste of Wine</i>, 2nd ed., Wiley, 1996.'),
    ('jackson', 'Jackson R.S. (2017). <i>Wine Tasting: A Professional Handbook</i>, 3<sup>e</sup> éd. Academic Press, Londres.',
                'Jackson R.S. (2017). <i>Wine Tasting: A Professional Handbook</i>, 3rd ed. Academic Press, London.'),
    ('ribereau', 'Ribéreau-Gayon P., Glories Y., Maujean A., Dubourdieu D. (2006). <i>Traité d’œnologie</i>, t. 2 : <i>Chimie du vin, stabilisation et traitements</i>. Dunod (éd. angl. <i>Handbook of Enology</i>, vol. 2, Wiley).',
                 'Ribéreau-Gayon P., Glories Y., Maujean A., Dubourdieu D. (2006). <i>Handbook of Enology</i>, vol. 2: <i>The Chemistry of Wine, Stabilization and Treatments</i>, 2nd ed. Wiley.'),
    ('iso', 'ISO 3591:1977, <i>Analyse sensorielle — Appareillage — Verre à dégustation pour l’analyse sensorielle des vins</i> (réexaminée et confirmée en 2022). <a href="https://www.iso.org/standard/9002.html" target="_blank" rel="noopener">iso.org</a>',
            'ISO 3591:1977, <i>Sensory analysis — Apparatus — Wine-tasting glass</i> (reviewed and confirmed in 2022). <a href="https://www.iso.org/standard/9002.html" target="_blank" rel="noopener">iso.org</a>'),
    ('wset', 'Wine &amp; Spirit Education Trust (WSET), <i>Level 3 Award in Wines — Systematic Approach to Tasting Wine® (SAT)</i>, Londres.',
             'Wine &amp; Spirit Education Trust (WSET), <i>Level 3 Award in Wines — Systematic Approach to Tasting Wine® (SAT)</i>, London.'),
    ('rose', 'Centre de recherche et d’expérimentation sur le vin rosé (Centre du Rosé, Vidauban), nuancier des couleurs des vins rosés.',
             'Rosé wine research centre (Centre du Rosé, Vidauban, Provence), rosé colour chart.'),
    ('thomson', 'Thomson J. (1855). On certain curious motions observable at the surfaces of wine and other alcoholic liquors. <i>Philosophical Magazine</i> 10 : 330–333.',
                'Thomson J. (1855). On certain curious motions observable at the surfaces of wine and other alcoholic liquors. <i>Philosophical Magazine</i> 10: 330–333.'),
    ('dukler', 'Dukler Y., Ji H., Falcon C., Bertozzi A.L. (2020). Theory for undercompressive shocks in tears of wine. <i>Physical Review Fluids</i> 5 : 034002. <a href="https://journals.aps.org/prfluids/abstract/10.1103/PhysRevFluids.5.034002" target="_blank" rel="noopener">doi</a>',
               'Dukler Y., Ji H., Falcon C., Bertozzi A.L. (2020). Theory for undercompressive shocks in tears of wine. <i>Physical Review Fluids</i> 5: 034002. <a href="https://journals.aps.org/prfluids/abstract/10.1103/PhysRevFluids.5.034002" target="_blank" rel="noopener">doi</a>'),
    ('nurgel', 'Nurgel C., Pickering G. (2005). Contribution of glycerol, ethanol and sugar to the perception of viscosity and density elicited by model white wines. <i>Journal of Texture Studies</i> 36 : 303–323.',
               'Nurgel C., Pickering G. (2005). Contribution of glycerol, ethanol and sugar to the perception of viscosity and density elicited by model white wines. <i>Journal of Texture Studies</i> 36: 303–323.'),
    ('liger', 'Liger-Belair G., Jeandet P. (2002). Effervescence in a glass of champagne: a bubble story. <i>Europhysics News</i> 33(1) : 10–14 ; Liger-Belair G. (2004). <i>Uncorked: The Science of Champagne</i>. Princeton University Press.',
              'Liger-Belair G., Jeandet P. (2002). Effervescence in a glass of champagne: a bubble story. <i>Europhysics News</i> 33(1): 10–14; Liger-Belair G. (2004). <i>Uncorked: The Science of Champagne</i>. Princeton University Press.'),
    ('buck', 'Buck L., Axel R. (1991). A novel multigene family may encode odorant receptors: a molecular basis for odor recognition. <i>Cell</i> 65 : 175–187 (prix Nobel de médecine 2004).',
             'Buck L., Axel R. (1991). A novel multigene family may encode odorant receptors: a molecular basis for odor recognition. <i>Cell</i> 65: 175–187 (Nobel Prize in Medicine 2004).'),
    ('bushdid', 'Bushdid C., Magnasco M.O., Vosshall L.B., Keller A. (2014). Humans can discriminate more than 1 trillion olfactory stimuli. <i>Science</i> 343 : 1370–1372.',
                'Bushdid C., Magnasco M.O., Vosshall L.B., Keller A. (2014). Humans can discriminate more than 1 trillion olfactory stimuli. <i>Science</i> 343: 1370–1372.'),
    ('gerkin', 'Gerkin R.C., Castro J.B. (2015). The number of olfactory stimuli that humans can discriminate is still unknown. <i>eLife</i> 4 : e08127.',
               'Gerkin R.C., Castro J.B. (2015). The number of olfactory stimuli that humans can discriminate is still unknown. <i>eLife</i> 4: e08127.'),
    ('shepherd', 'Shepherd G.M. (2006). Smell images and the flavour system in the human brain. <i>Nature</i> 444 : 316–321.',
                 'Shepherd G.M. (2006). Smell images and the flavour system in the human brain. <i>Nature</i> 444: 316–321.'),
    ('noble', 'Noble A.C. <i>et al.</i> (1987). Modification of a standardized system of wine aroma terminology. <i>American Journal of Enology and Viticulture</i> 38 : 143–146 (la « roue des arômes »).',
              'Noble A.C. <i>et al.</i> (1987). Modification of a standardized system of wine aroma terminology. <i>American Journal of Enology and Viticulture</i> 38: 143–146 (the “Wine Aroma Wheel”).'),
    ('wood', 'Wood C. <i>et al.</i> (2008). From wine to pepper: rotundone, an obscure sesquiterpene, is a potent spicy aroma compound. <i>Journal of Agricultural and Food Chemistry</i> 56 : 3738–3744.',
             'Wood C. <i>et al.</i> (2008). From wine to pepper: rotundone, an obscure sesquiterpene, is a potent spicy aroma compound. <i>Journal of Agricultural and Food Chemistry</i> 56: 3738–3744.'),
    ('gray', 'Standring S. (dir.) (2020). <i>Gray’s Anatomy</i>, 42<sup>e</sup> éd. Elsevier (muscles et papilles de la langue).',
             'Standring S. (ed.) (2020). <i>Gray’s Anatomy</i>, 42nd ed. Elsevier (tongue muscles and papillae).'),
    ('miller', 'Miller I.J., Reedy F.E. (1990). Variations in human taste bud density and taste intensity perception. <i>Physiology &amp; Behavior</i> 47 : 1213–1219.',
               'Miller I.J., Reedy F.E. (1990). Variations in human taste bud density and taste intensity perception. <i>Physiology &amp; Behavior</i> 47: 1213–1219.'),
    ('chandra', 'Chandrashekar J., Hoon M.A., Ryba N.J.P., Zuker C.S. (2006). The receptors and cells for mammalian taste. <i>Nature</i> 444 : 288–294.',
                'Chandrashekar J., Hoon M.A., Ryba N.J.P., Zuker C.S. (2006). The receptors and cells for mammalian taste. <i>Nature</i> 444: 288–294.'),
    ('otop', 'Tu Y.-H. <i>et al.</i> (2018). An evolutionarily conserved gene family encodes proton-selective ion channels. <i>Science</i> 359 : 1047–1050 (OTOP1, récepteur de l’acide).',
             'Tu Y.-H. <i>et al.</i> (2018). An evolutionarily conserved gene family encodes proton-selective ion channels. <i>Science</i> 359: 1047–1050 (OTOP1, the sour receptor).'),
    ('ikeda', 'Ikeda K. (1909), trad. angl. (2002). New seasonings. <i>Chemical Senses</i> 27 : 847–849 (découverte de l’umami).',
              'Ikeda K. (1909), English transl. (2002). New seasonings. <i>Chemical Senses</i> 27: 847–849 (discovery of umami).'),
    ('hanig', 'Hänig D.P. (1901). Zur Psychophysik des Geschmackssinnes. <i>Philosophische Studien</i> 17 : 576–623 ; Boring E.G. (1942). <i>Sensation and Perception in the History of Experimental Psychology</i>. Appleton-Century (origine de la « carte de la langue »).',
              'Hänig D.P. (1901). Zur Psychophysik des Geschmackssinnes. <i>Philosophische Studien</i> 17: 576–623; Boring E.G. (1942). <i>Sensation and Perception in the History of Experimental Psychology</i>. Appleton-Century (origin of the “tongue map”).'),
    ('carb', 'Chandrashekar J. <i>et al.</i> (2009). The taste of carbonation. <i>Science</i> 326 : 443–445.',
             'Chandrashekar J. <i>et al.</i> (2009). The taste of carbonation. <i>Science</i> 326: 443–445.'),
    ('gawel', 'Gawel R. (1998). Red wine astringency: a review. <i>Australian Journal of Grape and Wine Research</i> 4 : 74–95.',
              'Gawel R. (1998). Red wine astringency: a review. <i>Australian Journal of Grape and Wine Research</i> 4: 74–95.'),
    ('trevisani', 'Trevisani M. <i>et al.</i> (2002). Ethanol elicits and potentiates nociceptor responses via the vanilloid receptor-1. <i>Nature Neuroscience</i> 5 : 546–551.',
                  'Trevisani M. <i>et al.</i> (2002). Ethanol elicits and potentiates nociceptor responses via the vanilloid receptor-1. <i>Nature Neuroscience</i> 5: 546–551.'),
    ('bartoshuk', 'Bartoshuk L.M., Duffy V.B., Miller I.J. (1994). PTC/PROP tasting: anatomy, psychophysics, and sex effects. <i>Physiology &amp; Behavior</i> 56 : 1165–1171.',
                  'Bartoshuk L.M., Duffy V.B., Miller I.J. (1994). PTC/PROP tasting: anatomy, psychophysics, and sex effects. <i>Physiology &amp; Behavior</i> 56: 1165–1171.'),
]
NUM = {k: i + 1 for i, (k, _, _) in enumerate(SOURCES)}


def r(*keys):
    """Superscript citation link(s)."""
    return '<sup class="ref">' + ','.join(f'<a href="#src-{NUM[k]}">{NUM[k]}</a>' for k in keys) + '</sup>'


def pro(items):
    rows = ''.join(f'<div class="pro-item"><dt>{t(lbl)}</dt><dd>{blk(txt, "div")}</dd></div>' for lbl, txt in items)
    return (f'<details class="pro"><summary>{PRO_ICON}{t(("Pour les professionnels", "For professionals"))}'
            f'<span class="chev" aria-hidden="true">›</span></summary><dl>{rows}</dl></details>')


def cards(items, cls='fcard'):
    out = []
    for title, body in items:
        out.append(f'<div class="{cls}"><h4>{t(title)}</h4>{blk(body)}</div>')
    return ''.join(out)


# ------------------------------------------------------------------ 1 · SIGHT
SIGHT_INTRO = (
    'Un rapide examen visuel du vin est le premier indicateur, et le plus important, de ses caractéristiques et de son potentiel. '
    'Les conditions idéales pour bien observer un vin : une lumière blanche et vive mais pas trop intense, et un fond blanc qui préserve les couleurs naturelles '
    '(une nappe ou une feuille de papier suffit). Inclinez le verre à environ 45° au-dessus de ce fond. Cette analyse est essentielle : elle renseigne déjà sur le type de vin et sa maturité.'
    + r('peynaud', 'iso'),
    'A quick visual analysis of the wine is the first and foremost indicator of the wine’s characteristics and potential. '
    'The ideal conditions to properly observe a wine are a bright white light, but not too intense, and a white background to help preserve the natural colours '
    '(a tablecloth or a sheet of paper will do). Tilt the glass to about 45° over that background. This analysis is key to providing various factors such as the wine’s type and maturity.'
    + r('peynaud', 'iso'))

SIGHT_CARDS = [
    (('Limpidité', 'Clarity'),
     ('Un simple coup d’œil indique si le vin est trouble, voilé ou flou. Un vin légèrement trouble n’est pas forcément défectueux (il peut ne pas avoir été filtré), '
      'mais il peut signaler une altération. À l’inverse, de petits cristaux au fond du verre ou sur le bouchon (tartre) sont inoffensifs : ils témoignent seulement d’un vin peu traité ayant connu le froid.',
      'A quick look at the wine will tell you whether it is cloudy, hazy or blurry. Although a slightly cloudy wine is not necessarily a faulty wine (it may not have been filtered), '
      'it may show signs of possible alteration. On the other hand, small crystals at the bottom of the glass or on the cork (tartrates) are harmless: they simply show a lightly treated wine that has been exposed to cold.')),
    (('Brillance', 'Brilliance'),
     ('C’est la capacité du vin à réfléchir la lumière. Elle est souvent le signe d’une vivacité apportée par l’acidité : plus le pH est bas, plus la couleur d’un rouge est vive et éclatante — '
      'et d’une vinification soignée.' + r('ribereau'),
      'It is the wine’s capacity to reflect light. It is often a sign of liveliness brought to the wine by its acidity — the lower the pH, the brighter and more vivid a red wine’s colour — '
      'and of appropriate winemaking methods.' + r('ribereau'))),
    (('Couleur', 'Colour'),
     ('Avec un peu d’entraînement et de patience, les couleurs et nuances d’un vin renseignent sur sa maturité, les cépages possibles et même son origine (voir le nuancier ci-dessous). '
      'Les blancs vont du jaune pâle à reflets verts à l’or profond, voire à l’ambre ; les rosés du gris pâle et du saumon jusqu’au framboise, couleur souvent liée à une macération plus longue ; '
      'les rouges du pourpre violacé au rubis, au grenat puis au tuilé et à la brique. Regardez surtout le <b>bord</b> du disque : c’est là que se lit l’âge.',
      'With a little training and some patience, the different colours and hues seen in a wine can tell its maturity, the possible grape varieties and even its origin (see the colour chart below). '
      'Common white wine colours range from pale greenish yellow to deep gold or even amber; rosés from pale grey-pink and salmon to raspberry, a deeper colour often being a sign of prolonged skin contact; '
      'reds from purple to ruby, garnet, then tawny and brick. Look above all at the <b>rim</b> of the wine: that is where age shows.')),
    (('Intensité', 'Intensity or depth'),
     ('Souvent oubliée, c’est pourtant l’une des analyses les plus importantes. Elle dépend directement des cépages (un pinot noir à peau fine est naturellement plus clair qu’une syrah), '
      'de l’origine, du rendement, du millésime, de la durée de macération et même du mode d’élevage.' + r('ribereau'),
      'Often forgotten, it is however one of the most important analyses. It is directly affected by the grape varieties (a thin-skinned Pinot Noir is naturally paler than a Syrah), '
      'origin, yield, vintage, length of skin contact and even ageing methods.' + r('ribereau'))),
    (('Viscosité & « larmes »', 'Viscosity & “legs”'),
     ('Faire tourner le vin dans le verre renseigne sur son « épaisseur ». Les « larmes » (ou « jambes ») qui coulent sur la paroi sont dues avant tout à l’<b>alcool</b> : '
      'l’éthanol, plus volatil que l’eau, s’évapore plus vite du film de vin collé à la paroi ; la tension superficielle de ce film augmente et tire le liquide vers le haut (effet Marangoni), '
      'jusqu’à ce que la gravité le fasse retomber en gouttes.' + r('thomson', 'dukler') + ' Contrairement à une idée répandue, le glycérol et les sucres jouent peu sur les larmes ; '
      'ils se sentent davantage en bouche, sous forme de rondeur et de « gras ».' + r('nurgel'),
      'Swirling the wine in the glass will indicate its “thickness”. The “legs” (or “tears”) running down the glass are first of all due to <b>alcohol</b>: '
      'ethanol, being more volatile than water, evaporates faster from the thin film of wine clinging to the glass; the surface tension of that film rises and pulls liquid upwards (the Marangoni effect) '
      'until gravity brings it back down as drops.' + r('thomson', 'dukler') + ' Contrary to popular belief, glycerol and sugars play little part in the legs; '
      'they are felt rather on the palate, as roundness and richness.' + r('nurgel'))),
    (('Effervescence', 'Effervescence'),
     ('Dans un vin tranquille, la présence de CO₂ n’est pas forcément un défaut : un léger perlant dans un muscadet sur lie ou un chasselas de Savoie peut apporter de la fraîcheur. '
      'Si en revanche cette effervescence est forte, elle peut trahir une seconde fermentation en bouteille ou une altération (piqûre) : deux signes d’un vin défectueux. '
      'Dans le champagne et les vins effervescents, le dégustateur juge la finesse des bulles, leur vitesse et la persistance de l’effervescence. '
      'Un verre mal rincé (traces de détergent) ou trop parfaitement essuyé peut fausser le jugement : les bulles naissent surtout sur de minuscules fibres de cellulose (torchon, poussière) collées à la paroi.' + r('liger'),
      'In a non-sparkling wine, the presence of CO₂ is not necessarily a fault: a light fizz in Muscadet sur lie or Chasselas from Savoie can add a certain freshness to the wine. '
      'If, however, this effervescence is strong, it may be a sign of a second fermentation in the bottle or of acetic spoilage: both signs of a faulty wine. '
      'In Champagne or sparkling wine, the taster will judge the finesse of the bubbles, their speed and the persistence of the effervescence. '
      'A poorly rinsed glass (detergent residue) or one wiped too perfectly can skew the judgement: bubbles are mostly born on tiny cellulose fibres (from the cloth or the air) stuck to the glass.' + r('liger'))),
]

PRO_SIGHT = [
    (('Le verre', 'The glass'),
     ('Le verre normalisé ISO 3591 (dit « verre INAO ») a une coupe en forme d’œuf allongé, dont l’ouverture est plus étroite que la panse pour concentrer les arômes ; '
      'la norme, de 1977, a été confirmée en 2022. On le remplit au tiers environ pour pouvoir le faire tourner.' + r('iso'),
      'The ISO 3591 standard glass (the “INAO glass”) has an elongated-egg bowl whose opening is narrower than its widest part, to concentrate the aromas; '
      'the 1977 standard was reconfirmed in 2022. Fill it to about a third so it can be swirled.' + r('iso'))),
    (('Pigments', 'Pigments'),
     ('La couleur des rouges vient des anthocyanes de la pellicule. Au fil de l’élevage, elles se combinent aux tanins en pigments polymérisés plus stables, d’où le passage du pourpre (vin jeune, pH bas) '
      'au tuilé. Les blancs, eux, foncent par oxydation lente des composés phénoliques : un blanc doré jeune peut signaler un élevage en barrique, une vendange très mûre ou une oxydation prématurée.' + r('ribereau'),
      'Red wine colour comes from the anthocyanins in the skins. During ageing they combine with tannins into more stable polymeric pigments, hence the shift from purple (young wine, low pH) '
      'to tawny. White wines darken through slow oxidation of their phenolic compounds: a young white that is already golden may indicate barrel ageing, very ripe fruit or premature oxidation.' + r('ribereau'))),
    (('Physique des larmes', 'Physics of the tears'),
     ('Décrites par James Thomson dès 1855, les larmes relèvent de l’effet Marangoni (gradient de tension superficielle créé par l’évaporation de l’éthanol). '
      'Un modèle de 2020 (UCLA) montre qu’elles naissent d’une « onde de choc sous-compressive » partant du ménisque. Leur abondance renseigne sur le degré d’alcool, '
      'mais dépend aussi de la température, de l’humidité de l’air et de la propreté du verre.' + r('thomson', 'dukler') + ' Le glycérol (env. 5–10 g/L dans un vin sec, davantage dans les liquoreux botrytisés) '
      'n’augmente sensiblement la viscosité perçue qu’à des teneurs plus élevées.' + r('nurgel', 'ribereau'),
      'First described by James Thomson in 1855, tears are a Marangoni effect (a surface-tension gradient created by ethanol evaporation). '
      'A 2020 model (UCLA) shows they arise from a “reverse undercompressive shock” travelling up from the meniscus. Their abundance hints at the alcohol level, '
      'but also depends on temperature, air humidity and glass cleanliness.' + r('thomson', 'dukler') + ' Glycerol (about 5–10 g/L in a dry wine, more in botrytised sweet wines) '
      'only noticeably raises perceived viscosity at higher concentrations.' + r('nurgel', 'ribereau'))),
    (('Les bulles', 'Bubbles'),
     ('Les bulles ne naissent pas sur les irrégularités du verre, trop petites, mais dans des fibres de cellulose creuses déposées sur la paroi. La taille des bulles dépend surtout de la teneur en CO₂ dissous, '
      'de la température et du trajet qu’elles parcourent (elles grossissent en montant). Une bulle fine est souvent associée à la qualité, mais elle dépend aussi de l’âge du vin et du verre.' + r('liger'),
      'Bubbles are not born on irregularities in the glass, which are too small, but inside hollow cellulose fibres left on its wall. Bubble size depends mostly on dissolved CO₂, '
      'temperature and the distance travelled (they grow as they rise). Fine bubbles are often linked with quality, but they also depend on the wine’s age and the glass.' + r('liger'))),
]

# colour chart: (fr, en, core, rim)
PALETTES = {   # (fr, en, core, rim, example fr, example en)
    'blanc': [('Jaune pâle, reflets verts', 'Pale yellow, green hints', '#e9ebb1', '#f4f6d6', 'Muscadet sur lie, Chablis jeunes', 'Young Muscadet sur lie, Chablis'),
              ('Jaune citron', 'Lemon', '#ebe08a', '#f6efc0', 'Sancerre, riesling d’Alsace jeune', 'Sancerre, young Alsace Riesling'),
              ('Jaune paille', 'Straw', '#e6cc6a', '#f3e2a6', 'Meursault, Condrieu', 'Meursault, Condrieu'),
              ('Or', 'Gold', '#d9ad45', '#ecd08a', 'Sauternes jeune, bourgogne blanc de 10 ans', 'Young Sauternes, 10-year-old white Burgundy'),
              ('Vieil or', 'Old gold', '#c38d2c', '#deb466', 'Vin jaune (Château-Chalon), Sauternes de 20 ans', 'Vin Jaune (Château-Chalon), 20-year-old Sauternes'),
              ('Ambre', 'Amber', '#a5661e', '#cf9650', 'Rivesaltes ambré, très vieux Sauternes', 'Rivesaltes ambré, very old Sauternes'),
              ('Ocre, brun', 'Ochre, brown', '#7a4618', '#b07a40', 'Rivesaltes ambré hors d’âge (rancio) ; un blanc sec à ce stade est madérisé', 'Rivesaltes ambré hors d’âge (rancio); a dry white this colour is maderised')],
    'rose': [('Gris, très pâle', 'Pale grey-pink', '#f2dccd', '#f8ece3', 'Côtes de Toul (vin gris)', 'Côtes de Toul (vin gris)'),
             ('Pétale de rose', 'Rose petal', '#f0c2bf', '#f8dfdc', 'Côtes de Provence', 'Côtes de Provence'),
             ('Saumon', 'Salmon', '#eea48c', '#f6c9b8', 'Bandol, Coteaux d’Aix-en-Provence', 'Bandol, Coteaux d’Aix-en-Provence'),
             ('Corail', 'Coral', '#e98074', '#f3afa6', 'Rosé de Loire, Côtes du Rhône', 'Rosé de Loire, Côtes du Rhône'),
             ('Framboise', 'Raspberry', '#d8586f', '#ec95a3', 'Tavel, Cabernet d’Anjou', 'Tavel, Cabernet d’Anjou'),
             ('Groseille, clairet', 'Redcurrant, clairet', '#b02740', '#d76a7c', 'Bordeaux clairet', 'Bordeaux Clairet'),
             ('Pelure d’oignon', 'Onion skin', '#cf8a5c', '#e6b48e', 'Tavel de quelques années, rosé évolué', 'Tavel a few years old, a mature rosé')],
    'rouge': [('Pourpre, violacé', 'Purple', '#33061f', '#7d2160', 'Beaujolais nouveau, Cahors jeune', 'Beaujolais Nouveau, young Cahors'),
              ('Rubis', 'Ruby', '#470614', '#a8152e', 'Bourgogne rouge jeune, Chinon', 'Young red Burgundy, Chinon'),
              ('Cerise', 'Cherry', '#4a0a12', '#b52a2a', 'Morgon, Saumur-Champigny', 'Morgon, Saumur-Champigny'),
              ('Grenat', 'Garnet', '#3c0a0f', '#8f2a26', 'Châteauneuf-du-Pape, bordeaux de 8–10 ans', 'Châteauneuf-du-Pape, 8–10-year-old Bordeaux'),
              ('Tuilé', 'Tawny, tile', '#3b1309', '#a2542c', 'Bourgogne de 15–20 ans, Rivesaltes tuilé', '15–20-year-old Burgundy, Rivesaltes tuilé'),
              ('Brique', 'Brick', '#3a190c', '#8f5a2e', 'Grand bordeaux de 25–30 ans, vieil Hermitage', '25–30-year-old fine Bordeaux, old Hermitage'),
              ('Acajou, ambré', 'Mahogany, amber', '#3a1e10', '#7f5634', 'Banyuls grand cru, Maury hors d’âge', 'Banyuls Grand Cru, Maury hors d’âge')],
}


def glass_svg(core, rim, i):
    """A wine surface seen at 45° over a white sheet: core colour, paler watery rim."""
    g = f'gl{i}'
    return (f'<svg viewBox="0 0 120 92" class="swatch" aria-hidden="true"><defs>'
            f'<radialGradient id="{g}" cx="50%" cy="52%" r="58%"><stop offset="0" stop-color="{core}"/>'
            f'<stop offset=".62" stop-color="{core}"/><stop offset=".9" stop-color="{rim}"/><stop offset="1" stop-color="{rim}" stop-opacity=".55"/></radialGradient></defs>'
            f'<ellipse cx="60" cy="46" rx="54" ry="40" fill="#fff" stroke="#d9cfbd" stroke-width="1"/>'
            f'<ellipse cx="60" cy="47" rx="48" ry="34" fill="url(#{g})"/>'
            f'<ellipse cx="44" cy="34" rx="14" ry="5" fill="#fff" opacity=".28"/></svg>')


def colour_chart():
    tabs, groups, i = [], [], 0
    for key, fr, en in [('blanc', 'Blancs', 'Whites'), ('rose', 'Rosés', 'Rosés'), ('rouge', 'Rouges', 'Reds')]:
        tabs.append(f'<button type="button" class="tab{" on" if key == "rouge" else ""}" data-pal="{key}" data-fr="{fr}" data-en="{en}">{fr}</button>')
        cells = []
        for fr_n, en_n, core, rim, ex_fr, ex_en in PALETTES[key]:
            i += 1
            cap = t((fr_n, en_n), 'b') + t((ex_fr, ex_en), 'small', 'ex')
            cells.append(f'<figure class="sw">{glass_svg(core, rim, i)}<figcaption>{cap}</figcaption></figure>')
        groups.append(f'<div class="pal{" on" if key == "rouge" else ""}" data-pal="{key}">{"".join(cells)}</div>')
    return (f'<div class="tabs" role="tablist">{"".join(tabs)}</div>'
            f'<div class="age-axis"><span data-fr="Jeune" data-en="Young">Jeune</span><i></i><span data-fr="Évolué" data-en="Mature">Évolué</span></div>'
            f'{"".join(groups)}'
            + blk(('Nuancier indicatif, du plus jeune au plus évolué : la couleur fonce pour les blancs et s’éclaircit vers l’orangé pour les rouges. Les exemples sont des repères typiques : la teinte réelle dépend du millésime, du producteur et de l’âge du vin. '
                   'Pour les rosés, le Centre du Rosé de Vidauban publie un nuancier de référence.' + r('rose'),
                   'Indicative chart, from youngest to most mature: white wines darken, red wines fade towards orange. The examples are typical landmarks: the actual hue depends on vintage, producer and the wine’s age. '
                   'For rosés, the Centre du Rosé in Provence publishes a reference colour chart.' + r('rose')), 'p', 'cap'))


# ------------------------------------------------------------------ 2 · SMELL
SMELL_INTRO = (
    'De nos cinq sens, l’odorat est sans doute le plus méconnu. On a longtemps répété que le nez humain distingue « environ 10 000 odeurs » ; ce chiffre n’a jamais reposé sur une mesure. '
    'Une étude de 2014 a avancé plus de mille milliards de mélanges discernables, estimation elle-même contestée : la seule certitude est que nous en distinguons un nombre immense.'
    + r('bushdid', 'gerkin') + ' Les « capteurs » se trouvent en haut des fosses nasales, dans l’épithélium olfactif : plusieurs millions de neurones olfactifs y portent des cils '
    'garnis de récepteurs sensibles aux molécules odorantes — environ 400 types de récepteurs différents.' + r('buck') + ' Stimulés, ils envoient un influx au bulbe olfactif, situé juste au-dessus des fosses nasales, '
    'qui transmet le signal au cerveau — directement aux zones de l’émotion et de la mémoire, d’où le pouvoir d’évocation des odeurs.',
    'Of all five senses, the sense of smell is probably the least understood. It was long said that the human nose can detect “about 10,000 different odours”; that figure was never based on a measurement. '
    'A 2014 study put forward more than a trillion distinguishable mixtures, an estimate that is itself disputed: the only certainty is that we can tell apart an immense number.'
    + r('bushdid', 'gerkin') + ' Its “sensors” are located on the upper part of the nasal cavities, in the olfactory epithelium: several million olfactory nerve cells there carry “cilia” '
    'covered with receptors sensitive to odour molecules — about 400 different receptor types.' + r('buck') + ' When stimulated, they send an impulse to the olfactory bulb, located just above the nasal cavities, '
    'which in turn sends a signal to the brain — straight to the areas of emotion and memory, hence the evocative power of smells.')

NOSES = [
    (('1', 'Premier nez', 'First nose'),
     ('Verre immobile, sans l’agiter. On perçoit les molécules les plus volatiles, souvent les plus délicates. Un défaut (bouchon, réduction) se repère souvent ici.',
      'Glass still, not swirled. You pick up the most volatile, often most delicate molecules. A fault (cork taint, reduction) is often spotted here.')),
    (('2', 'Second nez', 'Second nose'),
     ('Après avoir fait tourner le vin : l’aération et l’agrandissement de la surface libèrent les arômes moins volatils, plus profonds et plus complexes.',
      'After swirling: aeration and a larger surface release the less volatile, deeper and more complex aromas.')),
    (('3', 'Rétro-olfaction', 'Retronasal smell'),
     ('Le vin en bouche se réchauffe ; ses arômes remontent par l’arrière-gorge jusqu’au nez. C’est ce qu’on appelle couramment le « goût » d’un vin : il est en réalité surtout olfactif.' + r('shepherd'),
      'Once in the mouth the wine warms up; its aromas rise through the back of the throat to the nose. This is what we usually call a wine’s “taste”: it is in fact mostly smell.' + r('shepherd'))),
]

AROMAS = [
    (('Arômes primaires ou variétaux', 'Primary or varietal aromas'), '#6f9a3c',
     ('Ils proviennent directement du raisin, du cépage lui-même, même si le terroir, le millésime, le climat et la vinification les influencent directement. '
      '<i>Ex. : fleurs blanches, agrumes, fruits rouges et noirs, poivre (syrah), poivron vert (cabernet), litchi et rose (gewurztraminer).</i>',
      'They come directly from the grape variety itself, although many factors such as terroir, vintage, climate and winemaking techniques have a direct influence. '
      '<i>E.g.: white flowers, citrus, red and black fruit, pepper (Syrah), green pepper (Cabernet), lychee and rose (Gewurztraminer).</i>')),
    (('Arômes secondaires ou fermentaires', 'Secondary or fermentation aromas'), '#c99a2e',
     ('Ils sont révélés par les fermentations, alcoolique ou malolactique. Arômes secondaires typiques : beurre frais (malolactique), lait, brioche et pain grillé (levures), banane (fermentation, surtout la macération carbonique du beaujolais nouveau).',
      'They are revealed by fermentation, whether alcoholic or malolactic. Typical secondary aromas are fresh butter (malolactic), milk, brioche and toast (yeast), banana (fermentation, especially the carbonic maceration of Beaujolais Nouveau).')),
    (('Arômes tertiaires ou d’évolution (le « bouquet »)', 'Tertiary or maturity aromas (the “bouquet”)'), '#8a4b2a',
     ('Ils proviennent de l’évolution, du vieillissement du vin : élevage en fût (vanille, toasté), puis lente évolution en bouteille (sous-bois, champignon, cuir, truffe, fruits secs, miel). '
      'Ce sont souvent les plus complexes, et ceux que l’aération révèle le mieux.',
      'They come from the “evolution”, the ageing of the wine: barrel ageing (vanilla, toast), then slow evolution in bottle (forest floor, mushroom, leather, truffle, dried fruit, honey). '
      'They are often the most complex, and the ones best revealed by swirling.')),
]

PRO_SMELL = [
    (('Récepteurs', 'Receptors'),
     ('Environ 400 gènes de récepteurs olfactifs fonctionnels chez l’homme (Buck &amp; Axel, Nobel 2004). Chaque molécule active une combinaison de récepteurs : c’est ce « code combinatoire » qui explique la diversité des odeurs perçues.' + r('buck'),
      'About 400 functional olfactory receptor genes in humans (Buck &amp; Axel, Nobel 2004). Each molecule activates a combination of receptors: this “combinatorial code” explains the variety of perceived smells.' + r('buck'))),
    (('Molécules clés', 'Key molecules'),
     ('Quelques marqueurs actifs à l’état de traces (ng/L, milliardièmes de gramme par litre) : <b>rotundone</b> (poivre de la syrah)' + r('wood') + ' ; <b>méthoxypyrazines</b> (poivron vert, cabernet et sauvignon) ; '
      '<b>thiols</b> (pamplemousse, buis, fruit de la passion du sauvignon) ; <b>linalol</b> (muscat) ; <b>acétate d’isoamyle</b> (banane) ; <b>diacétyle</b> (beurre, malolactique) ; '
      '<b>TDN</b> (« pétrole » du riesling évolué) ; <b>sotolon</b> (noix, curry du vin jaune) ; <b>TCA</b> (le « goût de bouchon », perceptible dès quelques ng/L).' + r('ribereau', 'jackson'),
      'A few markers active at trace levels (ng/L, billionths of a gram per litre): <b>rotundone</b> (Syrah’s pepper)' + r('wood') + '; <b>methoxypyrazines</b> (green pepper, Cabernet and Sauvignon); '
      '<b>thiols</b> (grapefruit, boxwood, passion fruit in Sauvignon); <b>linalool</b> (Muscat); <b>isoamyl acetate</b> (banana); <b>diacetyl</b> (butter, malolactic); '
      '<b>TDN</b> (the “petrol” of aged Riesling); <b>sotolon</b> (walnut, curry in Vin Jaune); <b>TCA</b> (“corked” taint, detectable from a few ng/L).' + r('ribereau', 'jackson'))),
    (('Deux classifications', 'Two classifications'),
     ('La tradition française (Peynaud) range les arômes de fermentation parmi les secondaires. Le WSET classe la fermentation alcoolique avec les <i>primaires</i> et réserve les <i>secondaires</i> '
      'aux opérations post-fermentaires (malolactique, lies, bois). Les deux coexistent : précisez celle que vous utilisez.' + r('peynaud', 'wset'),
      'The French tradition (Peynaud) counts fermentation aromas as secondary. WSET puts alcoholic fermentation with the <i>primary</i> aromas and keeps <i>secondary</i> '
      'for post-fermentation winemaking (malolactic, lees, oak). Both are in use: say which one you follow.' + r('peynaud', 'wset'))),
    (('Vocabulaire', 'Vocabulary'),
     ('La « roue des arômes » d’Ann C. Noble (UC Davis, 1987) organise les descripteurs en familles (fruité, floral, épicé, végétal, boisé, chimique…) du général au précis : un excellent outil d’entraînement.' + r('noble'),
      'Ann C. Noble’s Wine Aroma Wheel (UC Davis, 1987) organises descriptors into families (fruity, floral, spicy, vegetative, woody, chemical…) from general to specific: an excellent training tool.' + r('noble'))),
]

# ------------------------------------------------------------------ 3 · TASTE
TASTE_INTRO = (
    'La langue est un hydrostat musculaire composé de huit muscles (quatre intrinsèques, quatre extrinsèques), constamment humidifié par la salive sécrétée par les glandes salivaires.' + r('gray') + ' '
    'Outre ses fonctions phonétique et de nettoyage, c’est le principal organe du goût chez l’homme. Elle porte plusieurs milliers de bourgeons du goût — de l’ordre de 2 000 à 8 000, le nombre variant fortement d’une personne à l’autre — '
    'logés dans les papilles et reliés à un réseau complexe de nerfs ; on en trouve aussi sur le palais mou et dans la gorge.' + r('miller', 'gray'),
    'The tongue is a muscular hydrostat composed of eight muscles (four intrinsic, four extrinsic) and constantly moistened by saliva secreted by the salivary glands.' + r('gray') + ' '
    'Other than its phonetic and cleaning functions, the tongue is the main gustatory organ in humans. It carries several thousand taste buds — roughly 2,000 to 8,000, the number varying widely from one person to another — '
    'set in the papillae and each connected to an intricate web of nerves; there are also taste buds on the soft palate and in the throat.' + r('miller', 'gray'))

TASTES = [
    (('Sucré', 'Sweet'), '#c2477a',
     ('Miel, fruits mûrs, sucres divers… Sensation agréable déclenchée par les sucres. <b>Dans le vin :</b> sucres résiduels, mais aussi l’alcool et le glycérol, qui donnent une impression de douceur même à un vin sec.',
      'Honey, ripe fruit, various sugars… A pleasurable sensation triggered by sugars. <b>In wine:</b> residual sugar, but also alcohol and glycerol, which give an impression of sweetness even to a dry wine.')),
    (('Acide', 'Sour'), '#3d9a8c',
     ('Citron, orange, pamplemousse, raisin vert… Détecte la présence d’acides dilués (ions H⁺). <b>Dans le vin :</b> acides tartrique, malique, citrique, lactique, succinique ; l’acidité donne la fraîcheur et la tension.',
      'Lemon, orange, grapefruit, green grape… Detects the presence of diluted acids (H⁺ ions). <b>In wine:</b> tartaric, malic, citric, lactic and succinic acids; acidity brings freshness and tension.')),
    (('Amer', 'Bitter'), '#6b5aa6',
     ('Maté, marmelade, bière, olive, endive… Souvent perçue comme désagréable, voire repoussante, c’est un signal d’alerte contre les substances toxiques. <b>Dans le vin :</b> certains composés phénoliques (tanins jeunes, pépins), l’alcool à haute dose.',
      'Mate, marmalade, beer, olive, chicory… Often perceived as distasteful, sharp or even repulsive, it is a warning taste against toxic substances. <b>In wine:</b> some phenolic compounds (young tannins, seeds), alcohol at high levels.')),
    (('Salé', 'Salty'), '#c9a43a',
     ('Sel de table et tout ce qui apporte des ions sodium ; d’autres ions (potassium, lithium…) peuvent aussi paraître salés. <b>Dans le vin :</b> discret, dû aux sels minéraux ; il participe à la sensation dite « saline » de certains blancs côtiers.',
      'Table salt and anything that carries sodium ions; other ions (potassium, lithium…) can be perceived as salty too. <b>In wine:</b> discreet, due to mineral salts; it contributes to the so-called “saline” feel of some coastal whites.')),
    (('Umami', 'Umami'), '#a0522d',
     ('Sauce soja, parmesan, bouillon, tomate mûre… Saveur « savoureuse » identifiée par Kikunae Ikeda en 1908 ; elle détecte le glutamate et certains ribonucléotides.' + r('ikeda') + ' <b>Dans le vin :</b> faible ; elle peut apparaître dans les vins longuement élevés sur lies.',
      'Soy sauce, Parmesan, broth, ripe tomato… An appetising, savoury taste identified by Kikunae Ikeda in 1908; it detects glutamate and certain ribonucleotides.' + r('ikeda') + ' <b>In wine:</b> faint; it may appear in wines aged at length on their lees.')),
]

MOUTHFEEL = [
    (('Astringence', 'Astringency'),
     ('Ce n’est pas une saveur mais un toucher : les tanins se lient aux protéines de la salive, qui ne lubrifie plus ; la bouche paraît sèche, râpeuse.' + r('gawel'),
      'Not a taste but a touch: tannins bind to saliva proteins, which stop lubricating; the mouth feels dry and rough.' + r('gawel'))),
    (('Chaleur', 'Heat'),
     ('L’alcool active le récepteur de la douleur et de la chaleur (TRPV1) : au-delà d’un certain degré, le vin « brûle ».' + r('trevisani'),
      'Alcohol activates the pain-and-heat receptor (TRPV1): beyond a certain level, the wine “burns”.' + r('trevisani'))),
    (('Picotement', 'Prickle'),
     ('Le CO₂ est perçu à la fois par le toucher et par les cellules de l’acide, grâce à une enzyme (anhydrase carbonique 4).' + r('carb'),
      'CO₂ is sensed both by touch and by the sour-sensing cells, thanks to an enzyme (carbonic anhydrase 4).' + r('carb'))),
    (('Corps & texture', 'Body & texture'),
     ('Fluide, soyeux, ample, gras : l’impression de volume vient de l’alcool, des sucres, du glycérol et des tanins.' + r('nurgel', 'peynaud'),
      'Fluid, silky, broad, rich: the sense of volume comes from alcohol, sugars, glycerol and tannins.' + r('nurgel', 'peynaud'))),
]

PRO_TASTE = [
    (('Récepteurs', 'Receptors'),
     ('Sucré : T1R2 + T1R3 ; umami : T1R1 + T1R3 ; amer : environ vingt-cinq récepteurs TAS2R ; acide : canal à protons OTOP1 (identifié en 2018) ; salé : en partie le canal ENaC.' + r('chandra', 'otop'),
      'Sweet: T1R2 + T1R3; umami: T1R1 + T1R3; bitter: some twenty-five TAS2R receptors; sour: the OTOP1 proton channel (identified in 2018); salty: partly the ENaC channel.' + r('chandra', 'otop'))),
    (('Chronologie', 'Time course'),
     ('Les saveurs n’apparaissent pas en même temps : le sucré domine l’attaque, l’acidité s’exprime en milieu de bouche, l’amertume et l’astringence se révèlent en finale et persistent. '
      'D’où les trois temps de l’analyse : attaque, milieu, finale (et sa longueur, en secondes ou « caudalies »).' + r('peynaud'),
      'Tastes do not appear at the same time: sweetness dominates the attack, acidity shows mid-palate, bitterness and astringency come out on the finish and linger. '
      'Hence the three stages of the analysis: attack, mid-palate, finish (and its length, in seconds or “caudalies”).' + r('peynaud'))),
    (('Température', 'Temperature'),
     ('Le froid atténue le sucré et les arômes mais durcit l’amertume et l’astringence ; la chaleur exalte l’alcool. D’où un rouge tannique servi plus tempéré qu’un blanc vif.' + r('jackson', 'peynaud'),
      'Cold dampens sweetness and aromas but hardens bitterness and astringency; warmth exaggerates alcohol. Hence a tannic red served warmer than a crisp white.' + r('jackson', 'peynaud'))),
    (('Inégaux devant le goût', 'Not all equal'),
     ('La densité de papilles fongiformes varie beaucoup ; les « super-goûteurs » (forte sensibilité au PROP, un composé amer) perçoivent plus intensément l’amertume et l’astringence.' + r('bartoshuk', 'miller'),
      'The density of fungiform papillae varies a lot; “supertasters” (highly sensitive to PROP, a bitter compound) perceive bitterness and astringency more intensely.' + r('bartoshuk', 'miller'))),
]


def tongue_svg():
    """Redrawn tongue: the four papilla types, no taste zones (the zone map is a myth)."""
    import random
    rnd = random.Random(7)
    outline = 'M200 30 C292 30 338 70 338 150 C338 250 318 330 290 392 C266 444 236 474 200 474 C164 474 134 444 110 392 C82 330 62 250 62 150 C62 70 108 30 200 30 Z'
    parts = [f'<path d="{outline}" fill="#f2a18f" stroke="#b5604e" stroke-width="2.4"/>',
             '<path d="M200 70 C198 200 202 320 200 440" stroke="#c97a68" stroke-width="2.2" fill="none" stroke-linecap="round"/>']

    def half(y):
        if y < 150:
            return 138 * math.sqrt(max(0.0, 1 - ((150 - y) / 122) ** 2))
        return 138 * math.sqrt(max(0.0, 1 - ((y - 150) / 326) ** 2))

    def inside(x, y, m=8):
        return 34 < y < 468 and abs(x - 200) < half(y) - m
    # filiform: everywhere (small ticks)
    for _ in range(1400):
        x, y = rnd.uniform(64, 336), rnd.uniform(110, 462)
        if inside(x, y, 10):
            parts.append(f'<path d="M{x:.0f} {y:.0f}l1.4 -3.6" stroke="#cf7867" stroke-width="1.2" stroke-linecap="round"/>')
    # fungiform: mostly on the tip and the edges (red dots)
    for _ in range(2600):
        x, y = rnd.uniform(64, 336), rnd.uniform(190, 466)
        if not inside(x, y, 9):
            continue
        edge = half(y) - abs(x - 200)
        tipness = (y - 330) / 140
        p = max(0.0, 1 - edge / 34) * 0.5 + max(0.0, tipness) * 0.35
        if rnd.random() < p * 0.35:
            parts.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(2.8, 4.4):.1f}" fill="#c3313f" stroke="#fff" stroke-width=".9"/>')
    # foliate: folds on the rear sides
    for side in (-1, 1):
        for k in range(6):
            y = 120 + k * 12
            x0 = 200 + side * (122 - k * 1.5)
            parts.append(f'<path d="M{x0:.0f} {y}q{side * -12} 4 {side * -24} 2" stroke="#8f3a52" stroke-width="2.6" fill="none" stroke-linecap="round"/>')
    # circumvallate: V-shaped row at the back
    for k in range(-4, 5):
        x = 200 + k * 21
        y = 70 + abs(k) * 8
        parts.append(f'<circle cx="{x}" cy="{y}" r="8.5" fill="#f6c6d4" stroke="#8f3a52" stroke-width="2"/><circle cx="{x}" cy="{y}" r="3.6" fill="#b4234a"/>')
    # callouts
    calls = [(1, 200, 70, 200, 14), (2, 82, 150, 22, 150), (3, 262, 420, 380, 438), (4, 150, 260, 22, 300)]
    for n, x, y, lx, ly in calls:
        parts.append(f'<line x1="{x}" y1="{y}" x2="{lx}" y2="{ly}" stroke="#2b2018" stroke-width="1.4"/>'
                     f'<circle cx="{lx}" cy="{ly}" r="13" fill="#2b2018"/><text x="{lx}" y="{ly + 5}" text-anchor="middle" font-size="15" font-weight="700" fill="#f4ecd8" font-family="system-ui,sans-serif">{n}</text>')
    lab = ('<text x="200" y="500" text-anchor="middle" font-size="13" fill="#6b5a48" font-family="system-ui,sans-serif" letter-spacing="2" data-fr="POINTE" data-en="TIP">POINTE</text>'
           '<text x="372" y="40" text-anchor="end" font-size="13" fill="#6b5a48" font-family="system-ui,sans-serif" letter-spacing="2" data-fr="ARRIÈRE" data-en="BACK">ARRIÈRE</text>')
    return f'<svg viewBox="0 0 400 510" class="diagram tongue" role="img" aria-label="Langue / Tongue">{"".join(parts)}{lab}</svg>'


PAPILLAE = [
    (('1', 'Papilles caliciformes', 'Circumvallate papillae'),
     ('8 à 12, alignées en V au fond de la langue. Elles portent de nombreux bourgeons du goût ; des glandes (de von Ebner) les rincent en permanence.',
      '8 to 12, lined up in a V at the back of the tongue. They carry many taste buds; glands (von Ebner’s) rinse them constantly.')),
    (('2', 'Papilles foliées', 'Foliate papillae'),
     ('Replis sur les bords arrière de la langue, riches en bourgeons du goût — absentes de beaucoup de schémas.',
      'Folds along the rear edges of the tongue, rich in taste buds — missing from many diagrams.')),
    (('3', 'Papilles fongiformes', 'Fungiform papillae'),
     ('En forme de champignon, surtout sur la pointe et les bords. Elles portent quelques bourgeons chacune et sont les principaux capteurs de l’avant de la langue.',
      'Mushroom-shaped, mainly on the tip and edges. Each carries a few taste buds; they are the main sensors at the front of the tongue.')),
    (('4', 'Papilles filiformes', 'Filiform papillae'),
     ('Les plus nombreuses, sur toute la surface. Sans bourgeons du goût : elles assurent la fonction « mécanique » (toucher, texture, nettoyage).',
      'The most numerous, over the whole surface. No taste buds: they handle the “mechanical” side (touch, texture, cleaning).')),
]

# ------------------------------------------------------------------ 4 · BALANCE (the user's sketch, redrawn)
# angles in degrees, maths convention (0 = right, counter-clockwise). Axes: tannin 90, acidity 210, softness 330.
WORDS = [
    (90, ('Charpenté', 'Well-built'), ('Amer', 'Bitter'),
     ('Tanins présents mais enrobés : un vin bâti pour durer.', 'Present but well-coated tannins: a wine built to last.'),
     ('Tanins (ou amertume) dominants : le vin finit amer.', 'Dominant tannin (or bitterness): the wine finishes bitter.')),
    (120, ('Austère', 'Austere'), ('Astringent', 'Astringent'),
     ('Tanins et acidité un peu en avant : vin sérieux, souvent jeune, qui demande du temps.', 'Tannin and acidity slightly forward: serious, often young, needs time.'),
     ('Tanins + acidité sans moelleux : la bouche s’assèche et râpe.', 'Tannin + acidity without softness: the mouth dries and rasps.')),
    (150, ('Sévère', 'Severe'), ('Dur', 'Hard'),
     ('Manque un peu de moelleux face à l’acidité et aux tanins.', 'A little short of softness against acidity and tannin.'),
     ('Manque de moelleux (alcool, gras) : vin dur, anguleux.', 'Lacking softness (alcohol, richness): a hard, angular wine.')),
    (180, ('Vif', 'Lively'), ('Rêche', 'Harsh'),
     ('Acidité un peu en avant, soutenue par une trame : vin tonique.', 'Acidity slightly forward, with some backbone: a bracing wine.'),
     ('Acidité agressive, appuyée par les tanins.', 'Aggressive acidity, reinforced by tannin.')),
    (210, ('Nerveux', 'Vigorous'), ('Acide', 'Acidic'),
     ('Belle tension : l’acidité porte le vin.', 'Fine tension: acidity carries the wine.'),
     ('Acidité excessive : vin vert, mordant.', 'Excessive acidity: a green, biting wine.')),
    (240, ('Frais', 'Fresh'), ('Maigre', 'Thin'),
     ('Acidité désaltérante, structure légère.', 'Thirst-quenching acidity, light structure.'),
     ('Acide et sans matière : vin mince, creux.', 'Acidic and lacking substance: a thin, hollow wine.')),
    (270, ('Tendre', 'Tender'), ('Faible', 'Weak'),
     ('Peu de tanins, agréable et facile.', 'Little tannin, pleasant and easy.'),
     ('Ni tanins ni structure : vin dilué, sans tenue.', 'No tannin, no structure: a diluted wine with no backbone.')),
    (300, ('Souple', 'Supple'), ('Fade', 'Dull'),
     ('Moelleux un peu dominant, tanins fondus : vin coulant.', 'Softness slightly dominant, melted tannins: an easy-flowing wine.'),
     ('Ni acidité ni tanins pour le relever : vin plat, sans relief.', 'Neither acidity nor tannin to lift it: flat and featureless.')),
    (330, ('Onctueux', 'Unctuous'), ('Lourd', 'Heavy'),
     ('Alcool, glycérol ou sucres en avant : texture caressante.', 'Alcohol, glycerol or sugar forward: a caressing texture.'),
     ('Excès d’alcool ou de sucre : vin lourd, capiteux, écœurant.', 'Excess alcohol or sugar: heavy, heady, cloying.')),
    (0, ('Charnu', 'Fleshy'), ('Pâteux', 'Cloying'),
     ('De la chair et du volume, un peu moins de fraîcheur.', 'Flesh and volume, slightly less freshness.'),
     ('Gras sans fraîcheur : la bouche colle.', 'Rich with no freshness: the palate feels sticky.')),
    (30, ('Généreux', 'Generous'), ('Mou', 'Flabby'),
     ('Ample et chaleureux, acidité discrète.', 'Broad and warm, discreet acidity.'),
     ('Manque d’acidité : vin mou, flasque, qui vieillira mal.', 'Lacking acidity: flabby, and unlikely to age well.')),
    (60, ('Puissant', 'Muscular'), ('Grossier', 'Coarse'),
     ('Tanins et alcool généreux : vin corsé.', 'Generous tannin and alcohol: a full-bodied wine.'),
     ('Tanins et alcool sans fraîcheur : vin épais, rustique.', 'Tannin and alcohol with no freshness: thick and rustic.')),
]
CENTRE = (('Équilibré', 'Balanced'), ('Aucune composante ne domine : c’est l’harmonie recherchée.', 'No component dominates: the harmony we are looking for.'))

MODES = {
    'red': {'axes': [('Tanins', 'Tannin', ''), ('Acidité', 'Acidity', ''), ('Moelleux', 'Softness', 'alcool · glycérol · sucres|alcohol · glycerol · sugar')],
            'presets': [('Beaujolais (gamay)', 'Beaujolais (Gamay)', 6, 5, 3), ('Bourgogne rouge (pinot noir)', 'Red Burgundy (Pinot Noir)', 6, 5, 5),
                        ('Bordeaux jeune (cabernet)', 'Young Bordeaux (Cabernet)', 6, 5, 9), ('Châteauneuf-du-Pape', 'Châteauneuf-du-Pape', 4, 8, 6)]},
    'white': {'axes': [('Amertume', 'Bitterness', 'composés phénoliques|phenolic compounds'), ('Acidité', 'Acidity', ''), ('Moelleux', 'Softness', 'alcool · glycérol · sucres|alcohol · glycerol · sugar')],
              'presets': [('Muscadet sur lie', 'Muscadet sur lie', 8, 4, 4), ('Chablis', 'Chablis', 7, 5, 4),
                          ('Meursault', 'Meursault', 5, 7, 4), ('Condrieu (viognier)', 'Condrieu (Viognier)', 3, 8, 5)]},
    'sweet': {'axes': [('Amertume', 'Bitterness', 'composés phénoliques|phenolic compounds'), ('Acidité', 'Acidity', ''), ('Sucre + alcool', 'Sugar + alcohol', 'le moelleux|the softness')],
              'presets': [('Vouvray moelleux', 'Vouvray moelleux', 8, 7, 4), ('Sauternes', 'Sauternes', 6, 8, 5),
                          ('Alsace SGN', 'Alsace SGN', 7, 8, 4), ('Muscat de Rivesaltes', 'Muscat de Rivesaltes', 3, 9, 4)]},
}
# preset tuple = (fr, en, acidity, softness, tannin/bitterness)


def P(r_, a):
    a = math.radians(a)
    return r_ * math.cos(a), -r_ * math.sin(a)


def balance_svg():
    R, RD, RI, RO, RA = 200, 285, 128, 244, 334
    s = ['<svg viewBox="-380 -372 760 744" class="diagram balance" id="bal" role="img" aria-label="Équilibre du vin / Wine balance">',
         '<defs><radialGradient id="balg" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#f6e3e3"/><stop offset=".7" stop-color="#ecc5c6"/>'
         '<stop offset="1" stop-color="#d79599"/></radialGradient>'
         '<marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0 0 10 5 0 10 3 5Z" fill="#2b2018"/></marker></defs>',
         f'<circle r="{RD}" fill="none" stroke="#6b5a48" stroke-width="1" stroke-dasharray="3 4"/>',
         f'<circle r="{R}" fill="url(#balg)" stroke="#c07a80" stroke-width="2"/>',
         '<circle r="46" fill="#fbf1ec" stroke="#c07a80" stroke-width="1" stroke-dasharray="2 3"/>']
    tri = ' '.join('%.1f,%.1f' % P(RD, a) for a in (90, 210, 330))
    s.append(f'<polygon points="{tri}" fill="none" stroke="#2b2018" stroke-width="1.6"/>')
    # six spokes: 3 axes (excess, arrow) + 3 opposites (deficiency, plain)
    for a in (90, 210, 330):
        x0, y0 = P(52, a); x1, y1 = P(RA - 22, a)
        s.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#2b2018" stroke-width="2" marker-end="url(#arr)"/>')
    for a in (270, 30, 150):
        x0, y0 = P(52, a); x1, y1 = P(RD + 40, a)
        s.append(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke="#2b2018" stroke-width="1.2" stroke-dasharray="6 5"/>')
    s.append('<g id="dot"><circle r="22" fill="#8e1f33" opacity=".22"/><circle r="10" fill="#8e1f33" stroke="#fff" stroke-width="2.5"/></g>')
    # sector words
    for i, (a, inner, outer, _, _) in enumerate(WORDS):
        xi, yi = P(RI, a); xo, yo = P(RO, a)
        s.append(f'<text class="w in" data-i="{i}" x="{xi:.1f}" y="{yi + 5:.1f}" data-fr="{inner[0]}" data-en="{inner[1]}">{inner[0]}</text>')
        s.append(f'<text class="w out" data-o="{i}" x="{xo:.1f}" y="{yo + 5:.1f}" data-fr="{outer[0]}" data-en="{outer[1]}">{outer[0]}</text>')
    # axis labels (filled by JS per mode)
    for k, a in enumerate((90, 210, 330)):
        x, y = P(RA, a)
        dy = -8 if a == 90 else 26
        anchor = 'middle'
        s.append(f'<text class="ax" id="ax{k}" x="{x:.1f}" y="{y + dy:.1f}" text-anchor="{anchor}"></text>'
                 f'<text class="axs" id="axs{k}" x="{x:.1f}" y="{y + dy + 18:.1f}" text-anchor="{anchor}"></text>')
    # deficiency labels at the dashed spokes
    for a, fr, en in ((270, 'manque de tanins', 'lacking tannin'), (30, 'manque d’acidité', 'lacking acidity'), (150, 'manque de moelleux', 'lacking softness')):
        x, y = P(RD + 52, a)
        s.append(f'<text class="def" id="def{a}" x="{x:.1f}" y="{y + 4:.1f}" text-anchor="middle" data-fr="{fr}" data-en="{en}">{fr}</text>')
    s.append('</svg>')
    return ''.join(s)


def balance_js_data():
    import json
    words = [{'a': a, 'i': list(i), 'o': list(o), 'di': list(di), 'do': list(do)} for a, i, o, di, do in WORDS]
    return json.dumps({'words': words, 'centre': [list(CENTRE[0]), list(CENTRE[1])], 'modes': MODES}, ensure_ascii=False)


PRO_BAL = [
    (('La formule', 'The formula'),
     ('Émile Peynaud résume l’équilibre d’un vin rouge par une balance : <b>saveurs douces</b> (sucres, alcool, glycérol) d’un côté, <b>saveurs acides et amères</b> (acides, tanins) de l’autre — '
      'plus il y a de tanins, moins un rouge supporte l’acidité. Un blanc sec, presque sans tanins, s’équilibre surtout entre acidité et moelleux ; un liquoreux a besoin de beaucoup d’acidité pour ne pas paraître lourd.' + r('peynaud'),
      'Émile Peynaud sums up a red wine’s balance as a pair of scales: <b>sweet-tasting</b> components (sugars, alcohol, glycerol) on one side, <b>acid and bitter</b> ones (acids, tannins) on the other — '
      'the more tannin, the less acidity a red can carry. A dry white, almost tannin-free, balances mainly acidity against softness; a sweet wine needs plenty of acidity not to taste heavy.' + r('peynaud'))),
    (('Lire le schéma', 'Reading the chart'),
     ('Chaque flèche pleine indique l’<b>excès</b> d’une composante ; chaque branche en pointillés, à l’opposé, son <b>manque</b>. Le disque rosé est la zone d’équilibre, où les mots décrivent des nuances ; '
      'au-delà, les mots en rouge décrivent des déséquilibres. Seules les proportions comptent : un vin peut être à la fois très concentré et parfaitement équilibré.',
      'Each solid arrow shows an <b>excess</b> of one component; each dashed branch, opposite, shows its <b>lack</b>. The pink disc is the balance zone, where words describe nuances; '
      'beyond it, the red words describe imbalances. Only proportions matter: a wine can be very concentrated and perfectly balanced at the same time.')),
    (('Au-delà du triangle', 'Beyond the triangle'),
     ('L’équilibre se juge aussi dans le temps (attaque, milieu, finale) et avec les arômes : intensité aromatique à la hauteur de la structure, et longueur en bouche. '
      'Les grilles professionnelles (WSET SAT, fiches de concours) notent séparément équilibre, intensité, complexité et longueur pour conclure sur la qualité et le potentiel de garde.' + r('wset', 'jackson'),
      'Balance is also judged over time (attack, mid-palate, finish) and with the aromas: aromatic intensity matching the structure, and length. '
      'Professional grids (WSET SAT, competition sheets) score balance, intensity, complexity and length separately to conclude on quality and ageing potential.' + r('wset', 'jackson'))),
]

STEPS = [
    ('01', ('La vue', 'Sight'), ('Limpidité, couleur, intensité, larmes, bulles.', 'Clarity, colour, depth, legs, bubbles.'), '#vue'),
    ('02', ('L’odorat', 'Smell'), ('Premier nez, second nez, familles d’arômes.', 'First nose, second nose, aroma families.'), '#odorat'),
    ('03', ('Le goût', 'Taste'), ('Saveurs, toucher, chronologie en bouche.', 'Tastes, touch, how the palate unfolds.'), '#gout'),
    ('04', ('L’équilibre', 'Balance'), ('La synthèse : le vin est-il harmonieux ?', 'The synthesis: is the wine harmonious?'), '#equilibre'),
]


def steps_html():
    return ''.join(f'<a class="step" href="{h}"><span class="sn">{n}</span>{t(ti, "b")}{t(d, "small")}</a>' for n, ti, d, h in STEPS)


def noses_html():
    return ''.join(f'<div class="nose"><span class="nn">{n}</span><div>{t((fr, en), "h4")}{blk(d)}</div></div>' for (n, fr, en), d in NOSES)


def aromas_html():
    return ''.join(f'<div class="aroma" style="--c:{c}">{t(ti, "h4")}{blk(d)}</div>' for ti, c, d in AROMAS)


def tastes_html():
    return ''.join(f'<div class="taste" style="--c:{c}"><span class="tdot"></span>{t(ti, "h4")}{blk(d)}</div>' for ti, c, d in TASTES)


def papillae_html():
    return ''.join(f'<li><span class="pn">{n}</span><div>{t((fr, en), "b")}{blk(d, "p")}</div></li>' for (n, fr, en), d in PAPILLAE)


def sources_html():
    return ''.join(f'<li id="src-{i + 1}">{t((fr, en))}</li>' for i, (_, fr, en) in enumerate(SOURCES))


def main():
    tpl = (HERE / 'page_template.html').read_text()
    rep = {
        '@@BASE_CSS@@': base_css(),
        '@@STEPS@@': steps_html(),
        '@@SIGHT_INTRO@@': blk(SIGHT_INTRO),
        '@@SIGHT_CARDS@@': cards(SIGHT_CARDS),
        '@@COLOURS@@': colour_chart(),
        '@@PRO_SIGHT@@': pro(PRO_SIGHT),
        '@@SMELL_INTRO@@': blk(SMELL_INTRO),
        '@@GLASS@@': plate('img/smell_glass.webp', 'Verre et zones olfactives / Glass and smelling zones', 330, 1004, 'glass'),
        '@@NOSES@@': noses_html(),
        '@@INAO@@': plate('img/Verre_Inao.svg', 'Verre INAO, cotes ISO 3591 / INAO glass, ISO 3591 dimensions', 700, 700, 'inao-plate'),
        '@@AROMAS@@': aromas_html(),
        '@@PRO_SMELL@@': pro(PRO_SMELL),
        '@@TASTE_INTRO@@': blk(TASTE_INTRO),
        '@@TONGUE@@': tongue_svg(),
        '@@PAPILLAE@@': papillae_html(),
        '@@MYTH_REF@@': r('hanig', 'chandra'),
        '@@TASTES@@': tastes_html(),
        '@@MOUTHFEEL@@': cards(MOUTHFEEL, 'fcard sm'),
        '@@PRO_TASTE@@': pro(PRO_TASTE),
        '@@BALANCE_SVG@@': balance_svg(),
        '@@BAL_DATA@@': balance_js_data(),
        '@@PRO_BAL@@': pro(PRO_BAL),
        '@@PEYNAUD@@': r('peynaud'),
        '@@SOURCES@@': sources_html(),
    }
    html = tpl
    for k, v in rep.items():
        html = html.replace(k, v)
    assert '@@' not in html, html[html.index('@@'):html.index('@@') + 40]
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html)
    print(f'{OUT.relative_to(INFOS.parent)}: {len(html) // 1024} KB, {len(SOURCES)} sources')


if __name__ == '__main__':
    main()
