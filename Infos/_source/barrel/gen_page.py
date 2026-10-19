"""Builds Infos/Barrel_Making/Barrel_Making.html — « Comment naît une barrique » / "Birth of a wine barrel".

Photos: the user's 24 pictures taken at Tonnellerie François Frères, Saint-Romain (Côte-d'Or), November 2013
(Infos/Photos/Barrel_Making = 900 px copies; full-size originals in Infos/Photos/Barrel Pictures).
They were re-exported from the originals to Infos/Barrel_Making/img/*.webp (1600 px, q80) — see IMG below.
Facts: every claim carries a numbered source (SOURCES). Shared look = Vine & Vineyard base.css.
Run:  python3 gen_page.py   (then python3 assets/theme_apply.py Infos/Barrel_Making/Barrel_Making.html)
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INFOS = HERE.parent.parent
sys.path.insert(0, str(INFOS / 'Vine_and_Vineyard' / '_source'))
from common import base_css  # noqa: E402
sys.path.insert(0, str(HERE))
from seal_svg import seal_svg, head_svg  # noqa: E402

OUT = INFOS / 'Barrel_Making' / 'Barrel_Making.html'


def att(s):
    return s.replace('&', '&amp;').replace('"', '&quot;')


def dl(fr, en, tag='span', cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c} data-fr="{att(fr)}" data-en="{att(en)}">{fr}</{tag}>'


def LL(fr, en, tag='p', cls=''):
    """long text: both languages in the page, CSS shows the right one"""
    c = (' ' + cls) if cls else ''
    return f'<{tag} class="L fr{c}">{fr}</{tag}><{tag} class="L en{c}">{en}</{tag}>'


# ------------------------------------------------------------------ sources
SOURCES = [
    ('acad', 'B. Thibaut et R. Teissier du Cros, « Bois et tonnellerie : le mariage de la vigne et de la forêt », Académie d’Agriculture de France, Encyclopédie, fiche Questions sur… n° 02.03.Q13 (2018, revue en mars 2026). <a href="https://www.academie-agriculture.fr/sites/default/files/publications/encyclopedie/bois_et_tonnellerie.pdf" target="_blank" rel="noopener">PDF</a>',
             'B. Thibaut and R. Teissier du Cros, “Bois et tonnellerie : le mariage de la vigne et de la forêt” (Wood and cooperage: the marriage of vine and forest), French Academy of Agriculture, Encyclopaedia, sheet No. 02.03.Q13 (2018, revised March 2026). <a href="https://www.academie-agriculture.fr/sites/default/files/publications/encyclopedie/bois_et_tonnellerie.pdf" target="_blank" rel="noopener">PDF</a>'),
    ('genty', 'C. Genty (2025), « Entre réalité semi-mécanisée et esprit artisanal, la tonnellerie française, une activité économique millénaire », <i>Revue forestière française</i>, 76(1), p. 87-96 — dont le tableau des 28 étapes de la tonnellerie et la loi du 13 juin 1866 sur les contenances. <a href="https://doi.org/10.20870/revforfr.2024.9253" target="_blank" rel="noopener">doi:10.20870/revforfr.2024.9253</a>',
              'C. Genty (2025), “Entre réalité semi-mécanisée et esprit artisanal, la tonnellerie française, une activité économique millénaire” (French cooperage between semi-mechanisation and craftsmanship), <i>Revue forestière française</i>, 76(1), pp. 87-96 — including the table of the 28 steps of cooperage and the law of 13 June 1866 on capacities. <a href="https://doi.org/10.20870/revforfr.2024.9253" target="_blank" rel="noopener">doi:10.20870/revforfr.2024.9253</a>'),
    ('pollon', 'M. Pollon et al. (2023), « Volatile Compound Release from Oak Chips in Model Wine Media: Combined Influence of Toasting Degree, Size, Time of Contact, and Ethanol Content », <i>Journal of Agricultural and Food Chemistry</i>, 71(36), p. 13440-13450. <a href="https://pubmed.ncbi.nlm.nih.gov/37664949/" target="_blank" rel="noopener">PubMed</a>',
               'M. Pollon et al. (2023), “Volatile Compound Release from Oak Chips in Model Wine Media: Combined Influence of Toasting Degree, Size, Time of Contact, and Ethanol Content”, <i>Journal of Agricultural and Food Chemistry</i>, 71(36), pp. 13440-13450. <a href="https://pubmed.ncbi.nlm.nih.gov/37664949/" target="_blank" rel="noopener">PubMed</a>'),
    ('darney', 'AFP, « “Grand cru” des forêts françaises, le chêne de Darney s’arrache à prix d’or », 13 décembre 2020 (vente ONF de Darney, Vosges). <a href="https://www.linfodurable.fr/grand-cru-des-forets-francaises-le-chene-de-darney-sarrache-prix-dor-21922" target="_blank" rel="noopener">L’Info durable</a>',
               'AFP, “‘Grand cru’ des forêts françaises, le chêne de Darney s’arrache à prix d’or” (The grand cru of French forests: Darney oak fetches a fortune), 13 December 2020 (ONF sale at Darney, Vosges). <a href="https://www.linfodurable.fr/grand-cru-des-forets-francaises-le-chene-de-darney-sarrache-prix-dor-21922" target="_blank" rel="noopener">L’Info durable</a>'),
    ('jr', 'JancisRobinson.com, « The first family of oak » (la tonnellerie François Frères, fondée en 1910 à Saint-Romain). <a href="https://www.jancisrobinson.com/articles/the-first-family-of-oak" target="_blank" rel="noopener">jancisrobinson.com</a>',
           'JancisRobinson.com, “The first family of oak” (the François Frères cooperage, founded in 1910 in Saint-Romain). <a href="https://www.jancisrobinson.com/articles/the-first-family-of-oak" target="_blank" rel="noopener">jancisrobinson.com</a>'),
]
SIDX = {k: i + 1 for i, (k, _, _) in enumerate(SOURCES)}


def r(*keys):
    return '<sup class="ref">' + ','.join(f'<a href="#src-{k}">{SIDX[k]}</a>' for k in keys) + '</sup>'


# ------------------------------------------------------------------ photos  (file, w/h of the original)
IMG = {
    'logs': 1.5, 'grain': 1.5, 'grain_2': .667, 'splitting': .742, 'split_bundles': .788,
    'seasoning_yard': 2.11, 'seasoning_close': .935, 'stave_machining': 1.229, 'stave_machining_2': 1.112,
    'stave_matching': .714, 'raising': .706, 'raising_2': .72, 'bending_water': .667, 'bending_fire': .667,
    'toasting': .641, 'head_boards': 1.431, 'head_cutting': .975, 'heading': .815, 'hoop_press': .688,
    'hoop_press_2': .985, 'final_hoops': 1.23, 'final_hoops_2': 1.127, 'laser_mark': 1.162, 'finished_barrel': .681,
}

# ------------------------------------------------------------------ the ten steps
# photos: (file, layout, caption FR, caption EN); layout = 'w' (both columns), 'h' (one column),
# 'tall' (one column, two rows high); optional frame ratio after a colon, e.g. 'w:2'
STEPS = [
    dict(id='chene', fr='Le chêne', en='The oak', kfr='Choisir le bois', ken='Choosing the wood',
         body=(
             'Une barrique naît en forêt. On utilise les deux grands chênes à feuilles caduques de la forêt française, le chêne sessile et le chêne pédonculé : leur bois est solide, se fend, s’usine et se cintre bien, et il est riche en tanins et en arômes qui passeront dans le vin. Les tonneliers distinguent mal les deux espèces ; ils regardent d’abord la largeur des cernes, plus grande chez le pédonculé.' + r('acad'),
             'Les plus beaux arbres sont vendus comme des grands crus. À Darney, dans les Vosges, des chênes de plusieurs siècles qui grossissent d’environ 2 mm de diamètre par an — d’où leur grain très fin — se sont vendus en moyenne 907 € le mètre cube en 2020, et jusqu’à 1 443 €, quand le bois de chauffage vaut 30 à 40 €. Le grain doit être régulier : un grain irrégulier, et la barrique fuit.' + r('darney'),
         ),
         body_en=(
             'A barrel begins in the forest. Coopers use the two great deciduous oaks of the French forest, sessile oak and pedunculate oak: their wood is strong, splits, machines and bends well, and it is rich in tannins and aromas that will pass into the wine. Coopers find the two species hard to tell apart; they look first at the width of the growth rings, larger in pedunculate oak.' + r('acad'),
             'The finest trees are sold like grands crus. At Darney, in the Vosges, oaks several centuries old that grow about 2 mm in diameter a year — hence their very fine grain — sold for an average of €907 per cubic metre in 2020, and up to €1,443, when firewood fetches €30 to €40. The grain must be regular: an irregular grain, and the barrel leaks.' + r('darney'),
         ),
         photos=[('logs', 'w:2', 'Les grumes de chêne', 'Oak logs'),
                 ('grain', 'h:.8', 'L’écorce et le bois, en coupe', 'Bark and wood, in section'),
                 ('grain_2', 'h:.8', 'Les cernes : un an de croissance par anneau', 'Growth rings: one year per ring')]),
    dict(id='fendage', fr='Fendre', en='Splitting', kfr='Du tronc au merrain', ken='From log to stave wood',
         body=(
             'Le tronc est débité « sur quartier » : on le fend en suivant le fil du bois, à l’origine à la main, aujourd’hui à la fendeuse hydraulique. On obtient des planches sans défaut et de fil très droit, d’environ un mètre de long : les <b>merrains</b>.' + r('acad'),
             'Fendre plutôt que scier, c’est respecter les fibres : une douelle qui suit le fil reste étanche. Les merrains sont ensuite mis en bottes, prêts à sécher.' + r('acad', 'darney'),
         ),
         body_en=(
             'The log is cut “on the quarter”: it is split along the grain, once by hand, today with a hydraulic splitter. The result is defect-free, very straight-grained boards about one metre long: the <b>merrains</b> (stave wood).' + r('acad'),
             'Splitting rather than sawing respects the fibres: a stave that follows the grain stays watertight. The merrains are then bundled, ready to dry.' + r('acad', 'darney'),
         ),
         photos=[('splitting', 'h:.75', 'La fendeuse ouvre le billon dans le fil du bois', 'The splitter opens the log along the grain'),
                 ('split_bundles', 'h:.75', 'Les merrains fendus, en bottes', 'Split stave wood, in bundles')]),
    dict(id='sechage', fr='Laisser mûrir', en='Seasoning', kfr='Un à trois ans dehors', ken='One to three years outdoors',
         body=(
             'Les merrains sèchent à l’air libre, sans abri, de un à trois ans, empilés en croisillons. Le bois passe d’environ 60 % d’humidité dans l’arbre à 15–16 %. Cette alternance de pluie, de soleil et de vent évite les fentes de séchage.' + r('acad'),
             'C’est aussi une <b>maturation</b> : des champignons et des bactéries s’installent dans le bois et transforment ses tanins. Le merrain devient moins amer et plus aromatique. Un séchage forcé, en séchoir, ne prend qu’une semaine environ — mais ne fait pas mûrir le bois.' + r('acad', 'genty'),
         ),
         body_en=(
             'The merrains dry in the open air, unsheltered, for one to three years, stacked in criss-cross piles. The wood goes from about 60 % moisture in the tree to 15–16 %. The alternation of rain, sun and wind prevents drying cracks.' + r('acad'),
             'It is also a <b>maturation</b>: fungi and bacteria settle in the wood and transform its tannins. The stave wood becomes less bitter and more aromatic. Forced drying, in a kiln, takes only about a week — but does not mature the wood.' + r('acad', 'genty'),
         ),
         photos=[('seasoning_yard', 'w:2.1', 'Le parc à bois : des allées de merrains', 'The stave yard: aisles of stave wood'),
                 ('seasoning_close', 'w:1.8', 'Les piles croisées laissent passer l’air et la pluie', 'Criss-cross piles let air and rain through')]),
    dict(id='douelles', fr='Façonner les douelles', en='Shaping the staves', kfr='Usinage et appareillage', ken='Machining and matching',
         body=(
             'Le merrain sec devient une <b>douelle</b>. Quatre gestes, autrefois à la scie, à la plane, au couteau de revers et à la colombe, aujourd’hui sur une machine combinée : l’<b>écourtage</b> (la mise à longueur), le <b>dolage</b> (la face extérieure), l’<b>évidage</b> (la face intérieure, creusée) et le <b>jointage</b> (les chants, taillés en biais pour que les douelles se rejoignent en cercle).' + r('genty'),
             'Vient l’<b>appareillage</b> : on assemble des douelles de largeurs différentes pour former exactement la circonférence d’une barrique.' + r('genty'),
         ),
         body_en=(
             'The dry merrain becomes a <b>stave</b>. Four operations, once done with a handsaw, a drawknife, a hollowing knife and a long jointer plane, today on a combined machine: <b>docking</b> (cutting to length), <b>backing</b> (the outer face), <b>hollowing</b> (the inner face) and <b>jointing</b> (the edges, bevelled so that the staves close into a circle).' + r('genty'),
             'Then comes <b>matching</b>: staves of different widths are put together to make up exactly the circumference of one barrel.' + r('genty'),
         ),
         photos=[('stave_matching', 'tall', 'L’appareillage : choisir les douelles d’une même barrique', 'Matching: choosing the staves for one barrel'),
                 ('stave_machining', 'h:1.45', 'L’usinage des douelles', 'Machining the staves'),
                 ('stave_machining_2', 'h:1.45', 'Le merrain passe à la scie', 'The stave wood goes through the saw')]),
    dict(id='rose', fr='Monter en rose', en='Raising the barrel', kfr='Le montage', ken='Assembly',
         body=(
             'Le tonnelier dresse les douelles debout, serrées dans un cercle de montage : c’est la <b>mise en rose</b>. Le haut est fermé, le bas s’ouvre en jupe — la barrique a la forme d’un tronc de cône.' + r('genty'),
             'Des cercles provisoires, chassés au marteau, tiennent l’ensemble.' + r('genty'),
         ),
         body_en=(
             'The cooper stands the staves upright, held tight in a raising hoop: this is <b>raising</b> (in French, <i>mise en rose</i>, “setting up the rose”). The top is closed, the bottom splays like a skirt — the barrel is shaped like a truncated cone.' + r('genty'),
             'Temporary hoops, driven down with a hammer, hold it all together.' + r('genty'),
         ),
         photos=[('raising', 'h:.71', 'Les douelles montées dans le cercle de montage', 'The staves raised inside the raising hoop'),
                 ('raising_2', 'h:.71', 'La « rose » : une jupe de douelles', 'The “rose”: a skirt of staves')]),
    dict(id='cintrage', fr='Cintrer au feu', en='Bending over the fire', kfr='Le cintrage', ken='Bending',
         body=(
             'Pour refermer la jupe, il faut courber les douelles. On les chauffe à cœur — à moins de 100 °C — en les mouillant : ici, à l’ancienne, un feu brûle dans la barrique pendant que le tonnelier arrose le bois.' + r('acad', 'genty'),
             'Le bois assoupli, un câble tiré par un cabestan resserre peu à peu le bas de la barrique, jusqu’à ce que les douelles se rejoignent : la barrique a pris son galbe. D’autres ateliers cintrent à la vapeur ou par immersion.' + r('genty'),
         ),
         body_en=(
             'To close the skirt, the staves must be bent. They are heated right through — below 100 °C — while being moistened: here, the traditional way, a fire burns inside the barrel while the cooper waters the wood.' + r('acad', 'genty'),
             'Once the wood is supple, a cable drawn by a windlass slowly tightens the bottom of the barrel until the staves meet: the barrel has its curve. Other workshops bend with steam or by immersion.' + r('genty'),
         ),
         photos=[('bending_water', 'h:.667', 'Le feu dedans, l’eau dehors', 'Fire inside, water outside'),
                 ('bending_fire', 'h:.667', 'Le feu de cintrage', 'The bending fire')]),
    dict(id='bousinage', fr='Le bousinage', en='Toasting', kfr='La chauffe aromatique', ken='The aromatic toast',
         body=(
             'Une seconde chauffe, plus forte — vers 200 °C —, grille l’intérieur de la barrique : c’est le <b>bousinage</b>. Il fixe définitivement le cintrage et commence à dégrader la lignine et les hémicelluloses du bois, d’où naissent de nouveaux arômes.' + r('acad'),
             'Les tonneliers la considèrent comme l’étape la plus délicate. Sa durée et son intensité se choisissent selon le vin ou l’eau-de-vie qui sera élevé dans le fût — jusqu’à un début de carbonisation pour certains alcools forts.' + r('acad'),
         ),
         body_en=(
             'A second, stronger heating — around 200 °C — toasts the inside of the barrel: this is <b>toasting</b> (<i>bousinage</i>). It permanently sets the bend and begins to break down the wood’s lignin and hemicelluloses, which gives rise to new aromas.' + r('acad'),
             'Coopers consider it the most delicate step. Its length and intensity are chosen according to the wine or spirit that will age in the cask — up to the first stage of charring for some spirits.' + r('acad'),
         ),
         photos=[('toasting', 'h:.75', 'Le bousinage : le feu grille l’intérieur du fût', 'Toasting: the fire toasts the inside of the cask')]),
    dict(id='fonds', fr='Les fonds', en='The heads', kfr='Fermer la barrique', ken='Closing the barrel',
         body=(
             'Les deux <b>fonds</b> sont faits de planches de chêne rabotées sur leurs quatre faces, assemblées autrefois par des chevilles (tourillons), aujourd’hui à rainure et languette (bouvetage), puis taillées en disque.' + r('genty'),
             'Aux deux extrémités des douelles, la machine creuse le <b>jable</b>, une rainure où viendra s’emboîter le fond, et taille le <b>chanfrein</b>. Le tonnelier ouvre légèrement la barrique et y insère le fond : c’est le <b>fonçage</b>. Autrefois, on ajoutait de la farine de froment pour parfaire l’étanchéité ; plus aujourd’hui.' + r('genty'),
         ),
         body_en=(
             'The two <b>heads</b> are made of oak boards planed on all four faces, once joined with dowels, today tongue-and-groove, then cut into a disc.' + r('genty'),
             'At both ends of the staves, the machine cuts the <b>croze</b>, a groove into which the head will fit, and the <b>chamfer</b>. The cooper slightly loosens the barrel and fits the head in: this is <b>heading</b>. In the past wheat flour was added to perfect the seal; no longer.' + r('genty'),
         ),
         photos=[('head_boards', 'h:.74', 'Les planches de fond, assemblées', 'Head boards, joined'),
                 ('head_cutting', 'h:.9', 'La taille du fond en disque', 'Cutting the head into a disc'),
                 ('heading', 'h:.9', 'Le fonçage : le fond entre dans le jable', 'Heading: the head goes into the croze')]),
    dict(id='cerclage', fr='Cercler', en='Hooping', kfr='Serrer et finir', ken='Tightening and finishing',
         body=(
             'Les cercles d’acier sont découpés, mis en forme (le gironnage) et rivetés. Une cercleuse hydraulique les chasse ensuite sur la barrique — le travail que faisaient autrefois la chasse et le marteau.' + r('genty'),
             'La barrique est poncée et reçoit ses cercles définitifs — sur les photos, les cercles de travail noirs ont fait place à des cercles brillants.' + r('genty'),
         ),
         body_en=(
             'The steel hoops are cut, shaped (flared to fit the barrel’s curve) and riveted. A hydraulic hooping machine then drives them onto the barrel — the job once done with a hoop driver and a hammer.' + r('genty'),
             'The barrel is sanded and gets its final hoops — in the photos, the black working hoops have given way to shiny ones.' + r('genty'),
         ),
         photos=[('hoop_press', 'tall', 'La cercleuse chasse les cercles', 'The hooping machine drives the hoops down'),
                 ('hoop_press_2', 'h:1.45', 'Aux commandes de la cercleuse', 'At the controls of the hooping machine'),
                 ('final_hoops', 'h:1.45', 'Les cercles définitifs', 'The final hoops'),
                 ('final_hoops_2', 'w:2', 'Les barriques terminées attendent le contrôle', 'Finished barrels waiting to be checked')]),
    dict(id='finitions', fr='Percer, éprouver, marquer', en='Bung, test, mark', kfr='Les finitions', ken='Finishing',
         body=(
             'On perce le <b>trou de bonde</b> sur le bouge, la partie la plus large. La barrique est éprouvée : un échaudage, à la vapeur aujourd’hui, vérifie son étanchéité, et on mesure sa contenance exacte.' + r('acad', 'genty'),
             'Enfin, la marque : le nom du tonnelier, et souvent la chauffe ou l’origine du bois, gravés au fond — autrefois au burin ou au fer, aujourd’hui au laser. Ici, la marque de la tonnellerie François Frères, fondée en 1910 à Saint-Romain, dans la Côte-d’Or.' + r('genty', 'jr'),
         ),
         body_en=(
             'The <b>bung hole</b> is drilled on the bilge, the widest part. The barrel is tested: scalding, with steam today, checks that it is watertight, and its exact capacity is measured.' + r('acad', 'genty'),
             'Finally, the mark: the cooper’s name, and often the toast or the origin of the wood, engraved on the head — once with a chisel or a branding iron, today by laser. Here, the mark of the François Frères cooperage, founded in 1910 in Saint-Romain, in the Côte-d’Or.' + r('genty', 'jr'),
         ),
         photos=[('finished_barrel', 'h:.68', 'Le trou de bonde, sur le bouge', 'The bung hole, on the bilge'),
                 ('laser_mark', 'h:.68', 'Le marquage au laser', 'Laser marking')]),
]

# ------------------------------------------------------------------ formats
FORMATS = [
    ('Barrique bordelaise', 'Bordeaux barrique', '225 L', 'La barrique du Bordelais.', 'The Bordeaux cask.', 'genty'),
    ('Pièce de Bourgogne', 'Burgundy pièce', '228 L', 'Dite aussi « pièce de Beaune ».', 'Also called the “pièce de Beaune”.', 'genty'),
    ('Mâconnaise', 'Mâconnaise', '212 L', 'Un des trois fûts fixés par la loi du 13 juin 1866, abrogée en 2007.', 'One of the three casks set by the law of 13 June 1866, repealed in 2007.', 'genty'),
    ('Fût à Cognac', 'Cognac cask', '350 L', 'Agrandi depuis un modèle ancien de 275–280 L, de même forme.', 'Enlarged from an older 275–280 L model of the same shape.', 'genty'),
    ('Demi-muid', 'Demi-muid', '600 L', 'Un grand fût, au-delà des barriques.', 'A large cask, beyond barrique size.', 'genty'),
    ('Tonneau (unité de vente)', 'Tonneau (trade unit)', '900 L', 'À Bordeaux, une unité de compte du vrac : 4 barriques. Pas un fût.', 'In Bordeaux, a unit for bulk sales: 4 barriques. Not a cask.', 'genty'),
]

# ------------------------------------------------------------------ the 28 steps (Genty 2025, table 1)
T28 = [
    ('Commun', 'Common', [
        ('Maturation', 'Maturation', 'Maturation passive', 'Passive maturation', 'Maturation contrôlée ou active', 'Controlled or active maturation'),
        ('Séchage', 'Drying', 'Séchage passif', 'Passive drying', 'Séchage actif', 'Active drying')]),
    ('La coque', 'The body', [
        ('Écourtage', 'Docking', 'Scie égoïne', 'Handsaw', 'Machine combinée', 'Combined machine'),
        ('Dolage', 'Backing', 'Plane', 'Drawknife', 'Machine combinée', 'Combined machine'),
        ('Évidage', 'Hollowing', 'Couteau de revers', 'Hollowing knife', 'Machine combinée', 'Combined machine'),
        ('Jointage', 'Jointing', 'Colombe', 'Long jointer plane', 'Machine combinée', 'Combined machine'),
        ('Appareillage', 'Matching', 'Table d’appareillage', 'Matching bench', 'Automatisation', 'Automated'),
        ('Montage', 'Raising', 'Clef de montage + cercle de moule', 'Raising key + raising hoop', 'Machine à mettre en rose', 'Raising machine'),
        ('Chauffe de cintrage', 'Bending heat', 'Feu + eau', 'Fire + water', 'Vapeur ou immersion', 'Steam or immersion'),
        ('Cintrage', 'Bending', 'Cabestan à câble', 'Cable windlass', 'Cabestan à câble / mâchoires', 'Cable windlass / jaws'),
        ('Bousinage', 'Toasting', 'Chauffe humaine', 'Fire tended by hand', 'Chauffe thermorégulée', 'Temperature-controlled'),
        ('Rognage – chanfrein', 'Trimming – chamfer', 'Asse', 'Adze', 'Rogneuse', 'Trimming machine'),
        ('Rognage – mise à niveau', 'Trimming – levelling', 'Rabot', 'Plane', 'Rogneuse', 'Trimming machine'),
        ('Rognage – pas d’asse', 'Trimming – howel', 'Asse', 'Adze', 'Rogneuse', 'Trimming machine'),
        ('Rognage – jable', 'Trimming – croze', 'Ruelle', 'Croze', 'Rogneuse', 'Trimming machine')]),
    ('Les fonds', 'The heads', [
        ('Usinage', 'Machining', 'Rabot', 'Plane', 'Corroyeuse 4 faces', 'Four-sided planer'),
        ('Assemblage', 'Joining', 'Tourillons / pointes', 'Dowels / nails', 'Bouvetage', 'Tongue and groove'),
        ('Taillage', 'Cutting', 'Scie à chantourner + plane', 'Bow saw + drawknife', 'Taileuse de fonds', 'Head-cutting machine')]),
    ('Les cercles', 'The hoops', [
        ('Découpage', 'Cutting', 'Burin / marteau', 'Chisel / hammer', 'Cisaille', 'Shears'),
        ('Gironnage', 'Flaring', 'Poinçonnage / torsion', 'Punching / twisting', 'À plat / sur la tranche', 'Flat / on edge'),
        ('Rivetage', 'Riveting', 'Marteau + poinçon / riveuse', 'Hammer + punch / riveter', 'Riveteuse', 'Riveting machine')]),
    ('Commun', 'Common', [
        ('Fonçage', 'Heading', 'Ajout de farine de froment', 'Wheat flour added', 'Pas d’ajout', 'Nothing added'),
        ('Cerclage', 'Hooping', 'Chasse + marteau', 'Hoop driver + hammer', 'Cercleuse', 'Hooping machine'),
        ('Trou de bonde', 'Bung hole', 'Bondonnière', 'Bung auger', 'Perceuse', 'Drill'),
        ('Ponçage', 'Sanding', 'Bastringue + guistre', 'Spokeshave + scraper', 'Ponceuse', 'Sander'),
        ('Étanchéité', 'Leak test', 'Échaudage', 'Scalding', 'Échaudage vapeur', 'Steam scalding'),
        ('Contenance', 'Capacity', 'Pesée en eau', 'Weighing with water', 'Machine à épalement', 'Gauging machine'),
        ('Personnalisation', 'Marking', 'Burin / marque à feu ou à encre', 'Chisel / brand or ink', 'Laser', 'Laser')]),
]


# ------------------------------------------------------------------ builders
def fig(name, lay, cfr, cen, idx):
    kind, _, ratio = lay.partition(':')
    style = '' if kind == 'tall' else f' style="aspect-ratio:{ratio or IMG[name]}"'
    w = 1600 if IMG[name] >= 1 else round(1600 * IMG[name])
    h = round(w / IMG[name])
    return (f'<figure class="ph-{kind}"><button type="button" class="zoom" data-i="{idx}"{style} aria-label="Agrandir / Enlarge">'
            f'<img src="img/{name}.webp" alt="{att(cfr)} / {att(cen)}" loading="lazy" decoding="async" width="{w}" height="{h}"></button>'
            f'{dl(cfr, cen, "figcaption")}</figure>')


def steps_html():
    out, idx = [], 0
    for n, s in enumerate(STEPS, 1):
        figs = []
        for name, lay, cfr, cen in s['photos']:
            figs.append(fig(name, lay, cfr, cen, idx))
            idx += 1
        extra = TOAST_CARD if s['id'] == 'bousinage' else ''
        if s['id'] == 'fonds':   # the head seen from above, drawn, next to the photo of the head boards
            figs.insert(1, '<figure class="ph-h"><div class="draw-tile">' + head_svg() + '</div>'
                        + dl('Schéma : le fond vu de dessus', 'Diagram: the head seen from above', 'figcaption') + '</figure>')
        paras = ''.join(LL(fr, en) for fr, en in zip(s['body'], s['body_en']))
        rev = ' rev' if n % 2 == 0 else ''
        one = ' one' if len(s['photos']) == 1 else ''
        out.append(f'''
  <section class="stage{rev}" id="{s["id"]}">
    <div class="st-text panel">
      <p class="kick"><span class="st-n">{n:02d}</span>{dl(s["kfr"], s["ken"])}</p>
      {dl(s["fr"], s["en"], "h2")}
      {paras}
    </div>
    <div class="st-ph{one}">{"".join(figs)}{extra}</div>
  </section>{SEAL_BLOCK() if s['id'] == 'fonds' else ''}''')
    return ''.join(out)


def gallery_js():
    items = []
    for s in STEPS:
        for name, _, cfr, cen in s['photos']:
            items.append('{s:"img/%s.webp",fr:"%s",en:"%s"}' % (name, cfr.replace('"', '\\"'), cen.replace('"', '\\"')))
    items.append('{s:"img/barrel_anatomy_fr.webp",sen:"img/barrel_anatomy.webp",fr:"Anatomie d’une barrique",en:"Anatomy of a barrel"}')
    return '[' + ','.join(items) + ']'


# stage 08: how the heads are held and how the barrel is made watertight (drawing in seal_svg.py)
SEAL_NOTES = [
    ('Le jable', 'The croze',
     'Une rainure creusée à l’intérieur, au bout des douelles. Le bord du fond, taillé en biseau, s’y emboîte : c’est lui qui tient le fond. Le jable doit être parfaitement régulier sur tout le tour, sinon la barrique fuit.',
     'A groove cut on the inside, near the ends of the staves. The edge of the head, bevelled, fits into it: that is what holds the head. The croze must be perfectly even all the way round, or the barrel leaks.', ('genty',)),
    ('Les cercles serrent', 'The hoops squeeze',
     'Chassés sur la barrique, les cercles plaquent les douelles les unes contre les autres et contre le fond. C’est ce serrage qui fait l’étanchéité — sans colle ni clou. La forme galbée du fût permet de le serrer ainsi avec des cercles de diamètres adaptés.',
     'Driven onto the barrel, the hoops press the staves against one another and against the head. This squeeze is what makes it watertight — with no glue and no nails. The cask’s curved shape is what lets hoops of the right diameters tighten it.', ('acad',)),
    ('Des douelles jointives', 'Staves that meet',
     'Fendues dans le fil du bois, les douelles n’ont pas de fibres coupées par où le vin pourrait passer ; leurs chants, taillés en biais au jointage, se plaquent exactement l’un contre l’autre.',
     'Split along the grain, the staves have no cut fibres for the wine to seep through; their edges, bevelled during jointing, press exactly against each other.', ('acad', 'darney', 'genty')),
    ('Un fond d’un seul tenant', 'A head in one piece',
     'Les planches du fond sont assemblées autrefois par des chevilles, aujourd’hui à rainure et languette. Au fonçage, on ajoutait jadis de la farine de froment pour parfaire l’étanchéité.',
     'The head boards were once joined with dowels, today with tongue and groove. At heading, wheat flour was once added to perfect the seal.', ('genty',)),
    ('L’épreuve', 'The test',
     'Avant de quitter l’atelier, chaque barrique est éprouvée par échaudage — à la vapeur aujourd’hui — pour vérifier qu’elle ne fuit pas.',
     'Before leaving the workshop, every barrel is tested by scalding — with steam today — to check that it does not leak.', ('genty',)),
]


def SEAL_BLOCK():
    notes = ''.join(
        f'<li><span class="sn-n">{i}</span><div>{dl(tfr, ten, "b")}{LL(fr + r(*src), en + r(*src), "p")}</div></li>'
        for i, (tfr, ten, fr, en, src) in enumerate(SEAL_NOTES, 1))
    return ('<div class="seal" id="etancheite">' + dl('Comment le fond tient, et pourquoi le vin ne fuit pas', 'How the head stays in, and why the wine does not leak', 'h3')
            + f'<div class="seal-card">{seal_svg()}</div><ol class="seal-notes">{notes}</ol></div>')


TOAST_CARD = '<div class="toast panel">' + dl('Ce que la chauffe change', 'What the toast changes', 'h3') + LL(
    'Dans une étude sur des copeaux de chêne plongés dans un vin modèle, une chauffe plus forte a fait <b>monter le gaïacol</b> (notes fumées) et <b>baisser les lactones du chêne</b> (noix de coco) au-delà d’une chauffe moyenne ; la vanilline était la plus abondante après une chauffe forte. Ces composés naissent de la lignine et des sucres du bois.' + r('pollon', 'acad'),
    'In a study of oak chips steeped in a model wine, a stronger toast <b>raised guaiacol</b> (smoky notes) and <b>lowered the oak lactones</b> (coconut) beyond a medium toast; vanillin was most abundant after a heavy toast. These compounds come from the wood’s lignin and sugars.' + r('pollon', 'acad')) + '''
<div class="tbar" aria-hidden="true"><span class="t1"></span><span class="t2"></span><span class="t3"></span><span class="t4"></span></div>
<div class="tlab">''' + dl('légère', 'light') + dl('moyenne', 'medium') + dl('moyenne +', 'medium +') + dl('forte', 'heavy') + '</div></div>'


def formats_html():
    return ''.join(f'<div class="fmt panel"><b class="vol">{vol}</b>{dl(nfr, nen, "h3")}{LL(dfr + r(src), den + r(src), "p")}</div>'
                   for nfr, nen, vol, dfr, den, src in FORMATS)


def table28():
    rows, n = [], 0
    for gfr, gen, items in T28:
        rows.append(f'<tr class="grp"><th colspan="4">{dl(gfr, gen)}</th></tr>')
        for sfr, sen, hfr, hen, cfr, cen in items:
            n += 1
            rows.append(f'<tr><td class="n">{n}</td><td>{dl(sfr, sen)}</td><td>{dl(hfr, hen)}</td><td>{dl(cfr, cen)}</td></tr>')
    head = (f'<tr><th></th><th>{dl("Étape", "Step")}</th><th>{dl("Autrefois", "Then")}</th>'
            f'<th>{dl("Aujourd’hui", "Now")}</th></tr>')
    return f'<table class="t28"><thead>{head}</thead><tbody>{"".join(rows)}</tbody></table>'


def anatomy_svg():
    """Barrel in elevation (bilge from a quadratic curve) + a section through the head joint."""
    cx, y0, y1, hw, bulge = 270, 70, 470, 118, 92      # half-width at the heads, extra half-width at the bilge

    def half(y):
        t = (y - y0) / (y1 - y0)
        return hw + bulge * 2 * t * (1 - t)            # quadratic curve: control point = hw + bulge
    ctrl = hw + bulge
    ym = (y0 + y1) / 2
    p = []
    # body
    p.append(f'<path d="M{cx-hw},{y0} Q{cx-ctrl},{ym} {cx-hw},{y1} A{hw},20 0 0 0 {cx+hw},{y1} Q{cx+ctrl},{ym} {cx+hw},{y0} Z" fill="url(#oak)" stroke="#5a3a1c" stroke-width="2"/>')
    # staves
    for k in range(-7, 8):
        f = k / 8
        p.append(f'<path d="M{cx+f*hw:.1f},{y0+20*(1-f*f)**.5:.1f} Q{cx+f*ctrl:.1f},{ym+20*(1-f*f)**.5:.1f} {cx+f*hw:.1f},{y1+20*(1-f*f)**.5:.1f}" fill="none" stroke="#7a5430" stroke-width=".9" opacity=".55"/>')
    # hoops (pairs of y), drawn as bands following the curve, with a slight perspective sag
    for a, b in [(78, 96), (118, 132), (168, 182), (358, 372), (408, 422), (444, 462)]:
        la, lb = half(a), half(b)
        p.append(f'<path d="M{cx-la:.1f},{a} Q{cx},{a+2*22} {cx+la:.1f},{a} L{cx+lb:.1f},{b} Q{cx},{b+2*22} {cx-lb:.1f},{b} Z" fill="#3b3430" opacity=".9"/>')
    # top: stave ends (chime) and the head inside
    p.append(f'<ellipse cx="{cx}" cy="{y0}" rx="{hw}" ry="20" fill="#c9a272" stroke="#5a3a1c" stroke-width="2"/>')
    p.append(f'<ellipse cx="{cx}" cy="{y0+3}" rx="{hw-11}" ry="15" fill="#e2c597" stroke="#8a6438" stroke-width="1.2"/>')
    for k in (-2, -1, 0, 1, 2):
        x = cx + k * 22
        dy = 15 * (1 - (k * 22 / (hw - 11)) ** 2) ** .5
        p.append(f'<line x1="{x}" y1="{y0+3-dy:.1f}" x2="{x}" y2="{y0+3+dy:.1f}" stroke="#a07a4a" stroke-width=".9"/>')
    # bung hole
    p.append(f'<ellipse cx="{cx}" cy="{ym+20}" rx="12" ry="10" fill="#2a1a10" stroke="#5a3a1c"/>')

    def lab(x, y, tx, ty, fr, en, anchor='start'):
        return (f'<line x1="{x}" y1="{y}" x2="{tx}" y2="{ty}" class="ld"/><circle cx="{x}" cy="{y}" r="3.2" class="ldot"/>'
                f'<text x="{tx + (6 if anchor == "start" else -6)}" y="{ty+4}" text-anchor="{anchor}" class="lb" data-fr="{att(fr)}" data-en="{att(en)}">{fr}</text>')
    L = [
        lab(cx - 40, y0 + 2, 80, 30, 'Fond', 'Head', 'end'),
        lab(cx + hw - 4, y0 - 4, 450, 30, 'Têtes des douelles', 'Stave ends'),
        lab(cx - half(130) + 6, 125, 62, 125, 'Cercles', 'Hoops', 'end'),
        lab(cx - ctrl + 46, ym - 50, 62, ym - 50, 'Douelle', 'Stave', 'end'),
        lab(cx + 12, ym + 20, 450, ym + 20, 'Trou de bonde', 'Bung hole'),
        lab(cx + ctrl - 46, ym - 70, 450, ym - 70, 'Bouge (le ventre)', 'Bilge (the belly)'),
    ]
    # section through the barrel wall at the head: outside on the left, inside (and the head) on the right
    S = ['<g transform="translate(690,290)">',
         '<rect x="-62" y="-200" width="282" height="330" rx="14" fill="#fffaf0" stroke="#d9c7a3"/>',
         '<path d="M20,-160 L20,96 L66,96 L66,-160 Z" fill="url(#oak2)" stroke="#5a3a1c" stroke-width="1.6"/>',   # stave
         '<path d="M66,-160 L44,-160 L66,-126 Z" fill="#fffaf0" stroke="#5a3a1c" stroke-width="1.2"/>',          # chamfer
         '<path d="M66,-94 L50,-88 L50,-66 L66,-60 Z" fill="#fffaf0" stroke="#5a3a1c" stroke-width="1.2"/>',      # croze
         '<path d="M52,-80 L66,-88 L206,-88 L206,-68 L66,-68 L52,-74 Z" fill="#e2c597" stroke="#5a3a1c" stroke-width="1.4"/>',  # head
         '<rect x="12" y="-140" width="8" height="34" fill="#3b3430"/>',                                           # hoop
         ]
    sl = [  # dot x, y, text x, y, anchor
        (58, -150, 100, -168, 'start', 'Chanfrein', 'Chamfer'),
        (66, -110, 100, -124, 'start', 'Pas d’asse', 'Howel'),
        (178, -78, 182, -42, 'middle', 'Fond', 'Head'),
        (58, -64, 100, -36, 'start', 'Jable', 'Croze'),
        (43, 40, 100, 44, 'start', 'Douelle', 'Stave'),
        (14, -123, -12, -176, 'middle', 'Cercle', 'Hoop'),
    ]
    for x, y, tx, ty, anc, fr, en in sl:
        ly = ty + 6 if anc == 'middle' and ty < y else (ty - 14 if anc == 'middle' else ty)
        dx, dy = (4, 4) if anc == 'start' else (0, 0)
        S.append(f'<line x1="{x}" y1="{y}" x2="{tx}" y2="{ly}" class="ld"/><circle cx="{x}" cy="{y}" r="2.6" class="ldot"/>'
                 f'<text x="{tx + dx}" y="{ty + dy}" text-anchor="{anc}" class="lb sm" data-fr="{att(fr)}" data-en="{att(en)}">{fr}</text>')
    S.append('<text x="150" y="80" text-anchor="middle" class="lb tiny" data-fr="intérieur" data-en="inside">intérieur</text>')
    S.append('<text x="-22" y="80" text-anchor="middle" class="lb tiny" data-fr="extérieur" data-en="outside">extérieur</text>')
    S.append('<text x="79" y="120" text-anchor="middle" class="lb cap" data-fr="Coupe au bord du fond" data-en="Section at the edge of the head">Coupe au bord du fond</text>')
    S.append('</g>')
    defs = ('<defs><linearGradient id="oak" x1="0" x2="1"><stop offset="0" stop-color="#b48654"/><stop offset=".35" stop-color="#e3c08e"/>'
            '<stop offset=".7" stop-color="#d2a974"/><stop offset="1" stop-color="#9c6f40"/></linearGradient>'
            '<linearGradient id="oak2" x1="0" x2="1"><stop offset="0" stop-color="#c79a63"/><stop offset="1" stop-color="#e3c08e"/></linearGradient></defs>')
    return (f'<svg class="anat" viewBox="0 0 920 520" role="img" aria-label="Anatomie d’une barrique / Anatomy of a barrel">{defs}'
            + ''.join(p) + ''.join(L) + ''.join(S) + '</svg>')


ANAT_I = sum(len(s['photos']) for s in STEPS)   # lightbox index of the anatomy picture (after the step photos)


def anatomy_img():
    """The user's labelled barrel picture (2026-10-18; replaces the drawn SVG, anatomy_svg() kept unused).
    Two versions: barrel_anatomy.webp (English labels, fix_anatomy.py) and barrel_anatomy_fr.webp (make_fr.py)."""
    return (f'<button type="button" class="zoom anat-zoom" data-i="{ANAT_I}" aria-label="Agrandir / Enlarge">'
            '<img src="img/barrel_anatomy_fr.webp" data-src-fr="img/barrel_anatomy_fr.webp" data-src-en="img/barrel_anatomy.webp" '
            'alt="Anatomie d’une barrique / Anatomy of a barrel" '
            'loading="lazy" decoding="async" width="1144" height="1375"></button>')


def sources_html():
    return ''.join(f'<li id="src-{k}">{dl(fr, en)}</li>' for k, fr, en in SOURCES)


CSS = r'''
  sup.ref{font-size:.68em;line-height:0;margin-left:1px;}
  sup.ref a{color:var(--gold);text-decoration:none;font-weight:700;}
  .figs{display:flex;flex-wrap:wrap;justify-content:center;gap:10px clamp(18px,3vw,36px);margin-top:26px;}
  .fig{text-align:center;min-width:110px;}
  .fig b{display:block;font-family:var(--serif);font-weight:500;font-size:clamp(24px,3vw,32px);color:var(--gold-soft);line-height:1.05;}
  .fig span{font-size:11.5px;letter-spacing:.06em;color:var(--muted);}
  .lede{display:grid;grid-template-columns:1.2fr 1fr;gap:clamp(18px,3vw,36px);padding:clamp(20px,3vw,34px);}
  .lede p{margin:0 0 12px;font-size:15px;line-height:1.72;}
  .lede h3{font-family:var(--serif);font-weight:500;font-size:20px;margin:0 0 10px;color:var(--title);}
  .lede .side{border-left:1px solid var(--hair);padding-left:clamp(16px,2.5vw,30px);}
  .lede ul{margin:0;padding-left:18px;font-size:14px;line-height:1.6;color:var(--muted);}
  .lede li{margin-bottom:6px;}
  .lede li b{color:var(--parchment);font-weight:600;}

  .stage{display:grid;grid-template-columns:minmax(0,.92fr) minmax(0,1.08fr);gap:clamp(16px,2.6vw,32px);align-items:start;margin-top:clamp(36px,5vw,64px);}
  .stage.rev .st-text{order:2;}
  .st-text{padding:clamp(20px,2.6vw,30px);position:sticky;top:20px;}
  .st-text .kick{display:flex;align-items:baseline;gap:12px;margin:0 0 6px;font-size:11px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);}
  .st-n{font-family:var(--serif);font-size:44px;letter-spacing:0;line-height:.9;color:var(--gold-soft);font-weight:500;}
  .st-text h2{font-family:var(--serif);font-weight:500;font-size:clamp(26px,3.2vw,36px);color:var(--title);margin:0 0 14px;line-height:1.1;}
  .st-text p{margin:0 0 12px;font-size:15px;line-height:1.72;}
  .st-text p:last-child{margin-bottom:0;}
  .st-text b{color:var(--gold-soft);font-weight:600;}
  .st-ph{display:grid;grid-template-columns:1fr 1fr;gap:10px;grid-auto-flow:dense;}
  .st-ph.one{grid-template-columns:minmax(0,1fr);max-width:460px;}
  .st-ph figure{margin:0;display:flex;flex-direction:column;gap:6px;min-width:0;}
  .st-ph .ph-w{grid-column:span 2;}
  .st-ph .ph-tall{grid-row:span 2;}
  .st-ph.one .ph-w{grid-column:auto;}
  .st-ph .zoom{display:block;width:100%;padding:0;border:1px solid var(--hair);border-radius:14px;overflow:hidden;cursor:zoom-in;background:#2a1a10;box-shadow:var(--shadow);}
  .st-ph .ph-tall .zoom{flex:1;}
  .st-ph img{display:block;width:100%;height:100%;object-fit:cover;transition:transform .5s;}
  .st-ph .zoom:hover img{transform:scale(1.035);}
  .st-ph figcaption{font-size:12px;line-height:1.4;color:var(--muted);padding:0 4px;}
  .toast{padding:16px 18px;grid-column:1/-1;}
  .toast h3{font-family:var(--serif);font-weight:500;font-size:19px;margin:0 0 8px;color:var(--title);}
  .toast p{margin:0 0 12px;font-size:13.5px;line-height:1.6;color:var(--muted);}
  .toast b{color:var(--parchment);}
  .tbar{display:grid;grid-template-columns:repeat(4,1fr);height:12px;border-radius:6px;overflow:hidden;}
  .tbar .t1{background:#e3c08e}.tbar .t2{background:#b9834a}.tbar .t3{background:#86522a}.tbar .t4{background:#4a2814}
  .tlab{display:grid;grid-template-columns:repeat(4,1fr);font-size:11px;color:var(--muted);margin-top:5px;text-align:center;}

  .seal{margin-top:clamp(20px,3vw,32px);}   /* outside the stage grid, so the sticky text panel stops above it */
  .seal h3{font-family:var(--serif);font-weight:500;font-size:clamp(21px,2.4vw,26px);color:var(--title);margin:0 0 12px;}
  .seal-card{background:#fbf5e8;border:1px solid var(--paper-edge);border-radius:16px;box-shadow:var(--shadow);padding:clamp(6px,1.4vw,16px);overflow-x:auto;}
  .seal-svg{display:block;width:100%;min-width:620px;height:auto;}
  .draw-tile{aspect-ratio:.74;background:#fbf5e8;border:1px solid var(--paper-edge);border-radius:14px;box-shadow:var(--shadow);overflow:hidden;display:flex;align-items:center;}
  .seal-svg.head-svg{min-width:0;height:100%;}
  .seal-notes{list-style:none;margin:14px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(176px,1fr));gap:10px;}
  .seal-notes li{display:flex;gap:10px;padding:12px 14px;border-radius:14px;border:1px solid var(--hair);background:var(--glass);}
  .seal-notes .sn-n{flex:0 0 22px;height:22px;border-radius:50%;display:grid;place-items:center;font-size:12px;font-weight:700;color:#fff;background:#9b2235;}
  .seal-notes b{display:block;font-family:var(--serif);font-weight:500;font-size:16.5px;color:var(--title);margin-bottom:4px;}
  .seal-notes p{margin:0;font-size:13.5px;line-height:1.55;color:var(--muted);}
  .anat-card{background:var(--paper);border:1px solid var(--paper-edge);border-radius:16px;box-shadow:var(--shadow);padding:clamp(8px,1.6vw,18px);}
  .anat{display:block;width:100%;height:auto;}
  .anat-card{background:#fff;}
  .anat-zoom{display:block;margin:0 auto;max-width:640px;width:100%;padding:0;border:0;background:none;cursor:zoom-in;}
  .anat-zoom img{display:block;width:100%;height:auto;}
  .anat .ld{stroke:#7a2333;stroke-width:1.1;}
  .anat .ldot{fill:#7a2333;}
  .anat .lb{font-family:var(--sans);font-size:15px;fill:#2e1419;font-weight:600;}
  .anat .lb.sm{font-size:13.5px;}
  .anat .lb.cap{font-size:12.5px;font-style:italic;font-weight:500;fill:#6b4a2a;}
  .anat .lb.tiny{font-size:11px;font-weight:500;fill:#8a6a4a;}

  .fgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;}
  .fmt{padding:16px 18px;}
  .fmt .vol{display:block;font-family:var(--serif);font-weight:500;font-size:30px;color:var(--gold-soft);line-height:1;}
  .fmt h3{font-family:var(--serif);font-weight:500;font-size:18px;margin:6px 0 6px;color:var(--title);}
  .fmt p{margin:0;font-size:13.5px;line-height:1.55;color:var(--muted);}

  details.pro28{margin-top:16px;padding:0;overflow:hidden;}
  details.pro28 summary{cursor:pointer;list-style:none;padding:16px 20px;display:flex;align-items:center;gap:10px;font-family:var(--serif);font-size:19px;color:var(--title);}
  details.pro28 summary::-webkit-details-marker{display:none;}
  details.pro28 summary::after{content:"›";margin-left:auto;font-size:22px;color:var(--gold);transition:transform .2s;}
  details.pro28[open] summary::after{transform:rotate(90deg);}
  .t28wrap{padding:0 20px 18px;overflow-x:auto;}
  .t28{width:100%;border-collapse:collapse;font-size:13.5px;}
  .t28 th,.t28 td{text-align:left;padding:7px 10px;border-top:1px solid var(--hair);vertical-align:top;}
  .t28 thead th{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);border-top:0;}
  .t28 tr.grp th{font-family:var(--serif);font-weight:500;font-size:15px;color:var(--gold-soft);padding-top:14px;}
  .t28 td.n{color:var(--faint);width:28px;font-variant-numeric:tabular-nums;}
  .t28 td:nth-child(3){color:var(--muted);}
  .chips-note{font-size:14px;line-height:1.65;padding:16px 20px;margin-top:16px;}
  .chips-note p{margin:0;}

  .sources-list{margin:0;padding-left:26px;font-size:13px;line-height:1.6;color:var(--muted);columns:2;column-gap:34px;}
  .sources-list li{break-inside:avoid;margin-bottom:6px;}
  .sources-list li:target{color:var(--title);background:color-mix(in srgb,var(--gold) 14%,transparent);border-radius:6px;}
  .sources-list a{color:var(--gold);}
  .credit{font-size:12px;color:var(--faint);margin-top:16px;line-height:1.6;}

  /* lightbox with caption and arrows */
  dialog.blb{border:none;padding:0;background:transparent;max-width:96vw;max-height:96vh;overflow:visible;}
  dialog.blb::backdrop{background:rgba(12,3,6,.88);}
  dialog.blb img{display:block;max-width:94vw;max-height:calc(96vh - 60px);border-radius:10px;margin:0 auto;}
  dialog.blb p{margin:10px 0 0;text-align:center;color:#f4ecd8;font-size:14px;font-family:var(--sans);}
  dialog.blb p small{opacity:.6;margin-left:8px;}
  dialog.blb button{position:fixed;width:44px;height:44px;border-radius:50%;border:1px solid rgba(244,236,216,.35);background:rgba(20,8,10,.6);color:#f4ecd8;font-size:22px;cursor:pointer;}
  dialog.blb .x{top:14px;right:14px;}
  dialog.blb .pv{left:14px;top:50%;margin-top:-22px;}
  dialog.blb .nx{right:14px;top:50%;margin-top:-22px;}

  @media (max-width:900px){
    .lede{grid-template-columns:1fr;}
    .lede .side{border-left:none;padding-left:0;border-top:1px solid var(--hair);padding-top:16px;}
    .stage{grid-template-columns:minmax(0,1fr);}
    .stage.rev .st-text{order:0;}
    .st-text{position:static;}
    .fgrid{grid-template-columns:repeat(2,minmax(0,1fr));}
    .sources-list{columns:1;}
  }
  @media (max-width:520px){
    .fgrid{grid-template-columns:minmax(0,1fr);}
    .st-ph{grid-template-columns:minmax(0,1fr);}
    .st-ph .ph-w{grid-column:auto;}
    .st-ph .ph-tall{grid-row:auto;}
    .st-ph .ph-tall .zoom{aspect-ratio:.75;}
  }
'''

PAGE = r'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title data-fr="Comment naît une barrique" data-en="Birth of a wine barrel">Comment naît une barrique</title>
<meta name="description" content="Comment se fabrique une barrique de chêne, du tronc au fût marqué : fendage, séchage, douelles, cintrage au feu, bousinage, fonds et cerclage — en photos, à la tonnellerie François Frères (Saint-Romain).">
<style>
@@BASE_CSS@@
@@CSS@@
</style>
</head>
<body>
<div class="wrap">

  <div class="topbar">
    <a class="back" href="../../index.html" data-fr="← Retour" data-en="← Back">← Retour</a>
  </div>

  <header>
    <p class="eyebrow" data-fr="La tonnellerie" data-en="Cooperage">La tonnellerie</p>
    <h1 data-fr="Comment naît <em>une barrique</em>" data-en="Birth of <em>a wine barrel</em>">Comment naît <em>une barrique</em></h1>
    <div class="rule"></div>
    <p class="tagline" data-fr="Du chêne abattu en forêt au fût marqué au laser : dix étapes, en photos, chez un tonnelier de Bourgogne."
       data-en="From an oak felled in the forest to a laser-marked cask: ten steps, in pictures, at a Burgundy cooperage.">Du chêne abattu en forêt au fût marqué au laser : dix étapes, en photos, chez un tonnelier de Bourgogne.</p>
    <div class="figs">
      <div class="fig"><b>1–3</b>@@F1@@</div>
      <div class="fig"><b>&lt; 100 °C</b>@@F2@@</div>
      <div class="fig"><b>≈ 200 °C</b>@@F3@@</div>
      <div class="fig"><b>28</b>@@F4@@</div>
      <div class="fig"><b>≈ 540 000</b>@@F5@@</div>
    </div>
    <nav class="toc">@@TOC@@</nav>
  </header>

  <section class="sec" id="intro">
    <div class="lede panel">
      <div>@@LEDE@@</div>
      <div class="side">
        <h3 data-fr="Ce que le bois apporte au vin" data-en="What the wood gives the wine">Ce que le bois apporte au vin</h3>
        @@GIVES@@
      </div>
    </div>
  </section>
@@STEPS@@

  <section class="sec" id="anatomie">
    <div class="sec-head">
      <h2 data-fr="Anatomie <em>d’une barrique</em>" data-en="Anatomy <em>of a barrel</em>">Anatomie <em>d’une barrique</em></h2>
      <p data-fr="Les mots du tonnelier, de la douelle au jable." data-en="The cooper’s words, from stave to croze.">Les mots du tonnelier, de la douelle au jable.</p>
    </div>
    <div class="anat-card">@@ANAT@@</div>
  </section>

  <section class="sec" id="formats">
    <div class="sec-head">
      <h2 data-fr="Les formats <em>de fûts</em>" data-en="Cask <em>sizes</em>">Les formats <em>de fûts</em></h2>
      <p data-fr="Chaque région a son fût. Trois contenances restent courantes dans les tonnelleries françaises : 225, 228 et 350 litres."
         data-en="Each region has its cask. Three capacities remain common in French cooperages: 225, 228 and 350 litres.">Chaque région a son fût. Trois contenances restent courantes dans les tonnelleries françaises : 225, 228 et 350 litres.</p>
    </div>
    <div class="fgrid">@@FORMATS@@</div>
    <div class="chips-note panel">@@CHIPS@@</div>
    <details class="pro28 panel" id="etapes">
      <summary>@@T28H@@</summary>
      <div class="t28wrap">@@T28INTRO@@@@T28@@</div>
    </details>
  </section>

  <section class="sec" id="sources">
    <div class="sec-head"><h2 data-fr="Sources" data-en="Sources">Sources</h2></div>
    <ol class="sources-list">@@SOURCES@@</ol>
    <p class="credit">@@CREDIT@@</p>
  </section>

</div>
<dialog class="blb" id="blb"><img alt=""><p></p><button type="button" class="x" aria-label="Fermer / Close">✕</button><button type="button" class="pv" aria-label="Précédente / Previous">‹</button><button type="button" class="nx" aria-label="Suivante / Next">›</button></dialog>
<script>
(function(){
  var G = @@GALLERY@@, cur = 0;
  var dlg = document.getElementById('blb'), im = dlg.querySelector('img'), cap = dlg.querySelector('p');
  function lang(){ return document.documentElement.lang === 'en' ? 'en' : 'fr'; }
  function show(i){
    cur = (i + G.length) % G.length;
    im.src = (lang() === 'en' && G[cur].sen) || G[cur].s; im.alt = G[cur][lang()];
    cap.innerHTML = G[cur][lang()] + '<small>' + (cur+1) + ' / ' + G.length + '</small>';
  }
  var z = document.querySelectorAll('.st-ph .zoom, .anat-zoom');
  for(var i=0;i<z.length;i++) z[i].addEventListener('click', function(){ show(+this.getAttribute('data-i')); if(dlg.showModal) dlg.showModal(); });
  dlg.querySelector('.x').addEventListener('click', function(){ dlg.close(); });
  dlg.querySelector('.pv').addEventListener('click', function(e){ e.stopPropagation(); show(cur-1); });
  dlg.querySelector('.nx').addEventListener('click', function(e){ e.stopPropagation(); show(cur+1); });
  dlg.addEventListener('click', function(e){ if(e.target === dlg) dlg.close(); });
  document.addEventListener('keydown', function(e){
    if(!dlg.open) return;
    if(e.key === 'ArrowLeft') show(cur-1); else if(e.key === 'ArrowRight') show(cur+1);
  });
  /* language: the site menu sets <html lang>; data-fr/data-en nodes follow, .L blocks switch by CSS */
  function apply(){
    var l = lang();
    var n = document.querySelectorAll('[data-fr][data-en]');
    for(var i=0;i<n.length;i++){ if(n[i].tagName.toLowerCase() === 'text') n[i].textContent = n[i].getAttribute('data-'+l); else n[i].innerHTML = n[i].getAttribute('data-'+l); }
    var t = document.querySelector('title[data-en]'); if(t) document.title = t.getAttribute('data-'+l);
    var im2 = document.querySelectorAll('img[data-src-'+l+']');
    for(i=0;i<im2.length;i++) im2[i].src = im2[i].getAttribute('data-src-'+l);
    if(dlg.open) show(cur);
  }
  new MutationObserver(apply).observe(document.documentElement, {attributes:true, attributeFilter:['lang']});
  if(document.documentElement.lang === 'en') apply();
})();
</script>
</body>
</html>
'''


def main():
    toc = ''.join(f'<a href="#{s["id"]}">{n:02d} · {dl(s["fr"], s["en"])}</a>' for n, s in enumerate(STEPS, 1))
    toc += f'<a href="#anatomie">{dl("Anatomie", "Anatomy")}</a><a href="#formats">{dl("Formats", "Sizes")}</a>'
    rep = {
        '@@BASE_CSS@@': base_css(), '@@CSS@@': CSS,
        '@@F1@@': dl('ans de séchage en plein air', 'years of open-air seasoning') + r('acad'),
        '@@F2@@': dl('pour cintrer les douelles', 'to bend the staves') + r('acad'),
        '@@F3@@': dl('pour le bousinage', 'for the toast') + r('acad'),
        '@@F4@@': dl('étapes de fabrication', 'manufacturing steps') + r('genty'),
        '@@F5@@': dl('barriques faites en France en 2024', 'barrels made in France in 2024') + r('acad'),
        '@@TOC@@': toc,
        '@@LEDE@@': LL('Le tonneau tel qu’on le connaît a été inventé dans le monde celte il y a près de trois mille ans ; plus léger et plus solide que l’amphore, il l’a vite supplantée dans le commerce du vin entre Rome et l’Europe du Nord. Sa forme galbée permet de le serrer avec des cercles, et de rouler sans effort un fût de plusieurs centaines de kilos.' + r('acad'),
                       'The barrel as we know it was invented in the Celtic world nearly three thousand years ago; lighter and stronger than the amphora, it soon replaced it in the wine trade between Rome and Northern Europe. Its curved shape lets hoops tighten it, and lets a cask of several hundred kilos be rolled with ease.' + r('acad'))
                + LL('Aujourd’hui, la France fabrique environ 540 000 barriques par an (2024). Un tiers reste en France, le reste part à l’export, surtout aux États-Unis.' + r('acad') + ' Les photos de cette page ont été prises en novembre 2013 à la tonnellerie François Frères, fondée en 1910 à Saint-Romain, dans la Côte-d’Or.' + r('jr'),
                     'Today France makes about 540,000 barrels a year (2024). A third stay in France; the rest are exported, mostly to the United States.' + r('acad') + ' The photos on this page were taken in November 2013 at the François Frères cooperage, founded in 1910 in Saint-Romain, in the Côte-d’Or.' + r('jr')),
        '@@GIVES@@': LL('<ul><li><b>De l’oxygène, à petites doses.</b> Le bois agit comme une membrane semi-perméable : il laisse passer un peu d’oxygène, d’eau et d’alcool.</li><li><b>Des tanins et des arômes.</b> Le chêne contient une centaine de molécules solubles dans l’eau ou l’alcool, qui passent dans le vin.</li><li><b>Une vie microbienne.</b> Champignons et bactéries du bois modifient tanins et arômes.</li><li><b>De l’inertie.</b> Le bois isole le vin des écarts de température.</li></ul>' + r('acad'),
                        '<ul><li><b>Oxygen, in small doses.</b> Wood acts as a semi-permeable membrane: it lets a little oxygen, water and alcohol through.</li><li><b>Tannins and aromas.</b> Oak contains around a hundred molecules soluble in water or alcohol, which pass into the wine.</li><li><b>Microbial life.</b> The wood’s fungi and bacteria modify tannins and aromas.</li><li><b>Inertia.</b> Wood shields the wine from temperature swings.</li></ul>' + r('acad'), 'div'),
        '@@STEPS@@': steps_html(),
        '@@ANAT@@': anatomy_img(),
        '@@FORMATS@@': formats_html(),
        '@@CHIPS@@': LL('<b>Barrique ou copeaux&nbsp;?</b> Depuis 2005, l’Union européenne autorise l’élevage du vin avec des copeaux de chêne, en cuve. C’est bien moins cher, et ce sont souvent les tonneliers qui les fournissent, à partir des chutes de fabrication : les deux se complètent plus qu’ils ne s’opposent.' + r('acad'),
                        '<b>Barrel or chips?</b> Since 2005 the European Union has allowed wine to be aged with oak chips, in tanks. It is far cheaper, and it is often coopers who supply them, from manufacturing offcuts: the two complement each other more than they compete.' + r('acad')),
        '@@T28H@@': dl('Les 28 étapes d’une barrique, d’hier à aujourd’hui', 'The 28 steps of a barrel, then and now'),
        '@@T28INTRO@@': LL('Aucune étape n’a disparu avec la mécanisation : les machines ont seulement remplacé les outils.' + r('genty'),
                           'No step has disappeared with mechanisation: machines have simply replaced the tools.' + r('genty'), 'p', 'note'),
        '@@T28@@': table28(),
        '@@SOURCES@@': sources_html(),
        '@@GALLERY@@': gallery_js(),
        '@@CREDIT@@': dl('Textes et photos : © 2026 Christophe A. Paul. Photos prises à la tonnellerie François Frères, Saint-Romain (Côte-d’Or), en novembre 2013 ; schéma « Anatomie d’une barrique » : Christophe A. Paul. Les faits cités renvoient aux sources ci-dessus.',
                         'Text and photos: © 2026 Christophe A. Paul. Photos taken at the François Frères cooperage, Saint-Romain (Côte-d’Or), in November 2013; “Anatomy of a barrel” picture: Christophe A. Paul. The facts quoted refer to the sources above.'),
    }
    html = PAGE
    for k, v in rep.items():
        html = html.replace(k, v)
    assert '@@' not in html, html[html.index('@@'):html.index('@@') + 40]
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html)
    used = {k for k in SIDX if f'#src-{k}"' in html.split('<ol class="sources-list">')[0]}
    print(f'{OUT.relative_to(INFOS.parent)}: {len(html) // 1024} KB, {len(SOURCES)} sources '
          f'(unused: {sorted(set(SIDX) - used) or "none"}), {sum(len(s["photos"]) for s in STEPS)} photos')


if __name__ == '__main__':
    main()
