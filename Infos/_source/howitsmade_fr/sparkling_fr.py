"""French version of « How sparkling wine is made.html » — 2026-10-19, user request.
Run once from WEB Site/Infos:  python3 _source/howitsmade_fr/sparkling_fr.py
Backup of the English-only page: WEB Site/_backups/2026-10-19/How sparkling wine is made.html
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import js, sub1, bilingual, details, LANG_JS, LANG_INIT  # noqa: E402

PAGE = Path(__file__).resolve().parents[2] / "How it's made" / 'How sparkling wine is made.html'

G = lambda key, word: f'<span class="g" data-g="{key}">{word}</span>'
LE = "liqueur d'expédition"
WHY = '<b>Pourquoi c’est important :</b> '

GLOSS_FR = {
 "base wine": ["Vin de base — <i>vin clair</i>", "Un vin tranquille sec, acide et peu alcoolisé : la matière première de tout vin effervescent, avant l’arrivée des bulles."],
 "méthode traditionnelle": ["Méthode traditionnelle — <i>champenoise</i>", "La méthode classique où les bulles naissent d’une <b>seconde fermentation en bouteille</b>. Celle du champagne, des crémants, du cava et d’autres."],
 "assemblage": ["Assemblage — <i>blending</i>", "Marier différents cépages, villages et années — souvent avec des vins de réserve plus anciens — pour créer un style de maison constant avant la mise en bouteille."],
 "reserve wines": ["Vins de réserve — <i>reserve wines</i>", "Des vins tranquilles des récoltes précédentes, gardés de côté et ajoutés à l’assemblage pour qu’une cuvée non millésimée garde le même goût d’une année sur l’autre."],
 "tirage": ["Tirage", "La mise en bouteille du vin assemblé avec la liqueur de tirage, fermée par une capsule, pour déclencher la seconde fermentation."],
 "liqueur de tirage": ["Liqueur de tirage", "Une dose de vin, de sucre et de levures ajoutée à la mise en bouteille : le carburant de la seconde fermentation, qui fait les bulles."],
 "prise de mousse": ["Prise de mousse", "La seconde fermentation dans la bouteille fermée : son CO₂ ne peut pas s’échapper et se dissout dans le vin en bulles fines."],
 "sur lie": ["Sur lie — <i>on the lees</i>", "Élever le vin au contact des levures mortes ; c’est de là que viennent les notes de pain grillé, de brioche et de biscuit du champagne."],
 "lees": ["Lies — <i>lees</i>", "Les levures mortes qui restent après la fermentation. Un long contact avec elles (autolyse) apporte une complexité crémeuse, panaire."],
 "autolysis": ["Autolyse — <i>autolysis</i>", "La lente décomposition des levures mortes pendant l’élevage sur lies, qui libère les arômes grillés et briochés recherchés dans les vins de méthode traditionnelle."],
 "remuage": ["Remuage — <i>riddling</i>", "Incliner et tourner peu à peu chaque bouteille, col vers le bas, pour que les lies glissent dans le goulot. À la main sur des <i>pupitres</i>, ou à la machine (gyropalette)."],
 "gyropalette": ["Gyropalette", "Une cage pilotée par ordinateur qui remue des centaines de bouteilles à la fois — quelques jours là où le remuage à la main prenait des semaines."],
 "dégorgement": ["Dégorgement — <i>disgorgement</i>", "Retirer le dépôt de lies : le col est congelé, la capsule ôtée, et le glaçon de lies est expulsé par la pression de la bouteille."],
 "dosage": ["Dosage", "La touche finale de vin et de sucre ajoutée après le dégorgement, qui fixe le niveau de sucre du vin."],
 "liqueur d'expédition": ["Liqueur d’expédition", "Le mélange de vin et de sucre utilisé pour le dosage ; sa teneur en sucre décide si le vin sera brut, extra-brut, etc."],
 "brut": ["Le brut & l’échelle de sucre", "Le dosage fixe le style : <b>brut nature</b> (0–3 g/L, rien d’ajouté), <b>extra-brut</b>, <b>brut</b> (&lt; 12 g/L), <b>extra-dry</b>, <b>sec</b>, <b>demi-sec</b>, <b>doux</b> (le plus sucré)."],
 "muselet": ["Muselet", "La cage en fil de fer qui retient le bouchon champignon contre la pression de la bouteille — environ 6 bars, trois fois un pneu de voiture."],
 "méthode ancestrale": ["Méthode ancestrale", "La plus ancienne façon de faire un vin effervescent : une <b>seule</b> fermentation, mise en bouteille avant la fin pour que le dernier CO₂ reste piégé. Ni levures ni sucre ajoutés."],
 "pétillant naturel": ["Pétillant naturel — « pét-nat »", "Le nom moderne des vins de méthode ancestrale : légèrement pétillants, souvent troubles et un peu sucrés, fermés par une capsule."],
 "méthode charmat": ["Méthode Charmat — <i>cuve close</i>", "La méthode en cuve : la seconde fermentation se fait dans une grande <b>cuve sous pression</b>, et non en bouteille. Rapide et axée sur le fruit — c’est ainsi que se font le prosecco et l’asti."],
 "coquard": ["Pressoir Coquard", "Le pressoir champenois traditionnel, large et peu profond, qui presse doucement les grappes entières et garde le jus pâle, même avec des raisins noirs."],
}


def step(t, en_name, sub, n, ic, html, why, opt=False):
    d = {'t': t, 'fr': en_name, 'sub': sub, 'ph': f'Étape {n}', 'ic': ic, 'html': html, 'why': WHY + why}
    if opt:
        d['opt'] = True
    return d


S_FR = {
 'champagne': {'label': 'Champagne', 'cls': 'champagne', 'steps': [
  step('Vendange', 'Harvest', 'À la main, en grappes entières', 1, 'grape',
       '<p>Le champagne est <b>vendangé à la main</b>, par obligation, en grappes entières, à partir du chardonnay, du pinot noir et du meunier. Les raisins sont cueillis <b>tôt</b>, quand l’acidité est élevée et le sucre modéré — exactement ce qu’il faut à un vin de base effervescent.</p>',
       'une acidité élevée et un degré bas sont la colonne vertébrale d’un vin qui doit supporter une seconde fermentation et un long vieillissement.'),
  step('Pressurage en grappes entières', 'Whole-bunch Pressing', 'Doux — un jus pâle même de raisins noirs', 2, 'press',
       f'<p>Les grappes entières sont pressées doucement dans un large pressoir {G("coquard", "Coquard")}. Même les pinots noirs donnent un jus presque incolore ; les rendements sont strictement plafonnés, et seule la première fraction, la plus fine (la <i>cuvée</i>), va dans les meilleurs vins.</p>',
       'un pressurage doux garde le jus blanc et sans tanins durs — indispensable pour un effervescent élégant.'),
  step('Fermentation alcoolique', 'First Fermentation', 'Elle donne le vin de base, tranquille', 3, 'ferment',
       f'<p>Le jus fermente en un {G("base wine", "vin de base")} (<i>vin clair</i>) sec, vif et tranquille, de seulement 10–11 % vol. Chaque cépage, village et parcelle est en général gardé à part pour l’instant.</p>',
       'ce vin tranquille austère est la toile vierge sur laquelle toute la méthode est construite.'),
  step('Assemblage', 'Assemblage', 'Assembler la cuvée', 4, 'blend',
       f'<p>Le chef de cave assemble des dizaines de vins de base — cépages, villages et souvent des {G("reserve wines", "vins de réserve")} plus anciens — dans l’{G("assemblage", "assemblage")} final. C’est là que naît la signature d’une maison, et c’est ainsi qu’un champagne non millésimé garde le même goût chaque année.</p>',
       'l’assemblage, et non un vignoble unique, est l’art au cœur du champagne.'),
  step('Mise en tirage', 'Tirage', 'En bouteille avec levures + sucre', 5, 'tirage',
       f'<p>L’assemblage est mis en bouteille avec une {G("liqueur de tirage", "liqueur de tirage")} (vin, sucre et levures) et fermé par une capsule. C’est le {G("tirage", "tirage")} — le point de départ de la magie à venir.</p>',
       'à partir d’ici, les bulles se font <i>dans cette bouteille même</i> — l’idée qui définit la méthode.'),
  step('Prise de mousse', 'Second Fermentation in Bottle', 'Les bulles naissent', 6, 'mousse',
       f'<p>Couchées, les bouteilles font une lente seconde fermentation — la {G("prise de mousse", "prise de mousse")}. Le CO₂ ne peut pas sortir de la bouteille fermée : il se dissout dans le vin en bulles fines, et la pression monte à environ 6 bars.</p>',
       f'cette fermentation en bouteille sépare la {G("méthode traditionnelle", "méthode traditionnelle")} de toutes les méthodes plus rapides.'),
  step('Élevage sur lie', 'Ageing on the Lees', 'Au moins 15 mois — souvent bien plus', 7, 'lees',
       f'<p>Le vin repose ensuite {G("sur lie", "sur lie")} — sur les {G("lees", "lies")} de levures mortes. Une lente {G("autolysis", "autolyse")} donne au champagne ses notes de pain grillé, de brioche et de biscuit. Le minimum légal est de 15 mois (3 ans pour un millésimé) ; les grandes maisons vont bien au-delà.</p>',
       'c’est pendant l’élevage sur lies qu’un vin pétillant devient <i>du champagne</i> — complexe, crémeux et profond.'),
  step('Remuage', 'Riddling', 'Amener les lies dans le col', 8, 'remuage',
       f'<p>Chaque bouteille est peu à peu inclinée col en bas et tournée — le {G("remuage", "remuage")} — jusqu’à ce que toutes les {G("lees", "lies")} se rassemblent contre la capsule. Autrefois à la main sur des <i>pupitres</i> en bois, aujourd’hui le plus souvent en {G("gyropalette", "gyropalette")}.</p>',
       'rassembler les lies dans le col permet de les retirer proprement à l’étape suivante.'),
  step('Dégorgement', 'Disgorgement', 'Expulser les lies', 9, 'disgorge',
       f'<p>Le col est plongé dans une saumure glacée pour emprisonner les lies dans un petit glaçon ; on ôte la capsule et la pression de la bouteille expulse le glaçon — le {G("dégorgement", "dégorgement")} — laissant un vin parfaitement limpide.</p>',
       'on retire le dépôt sans perdre les précieuses bulles.'),
  step('Dosage & bouchage', 'Dosage & Corking', 'Il fixe le niveau de sucre', 10, 'dosage',
       f'<p>Le petit vide est complété avec la {G(LE, "liqueur d’expédition")} — le {G("dosage", "dosage")} — qui fixe le style, du {G("brut", "brut")} nature, très sec, au doux. Puis viennent le bouchon champignon, le {G("muselet", "muselet")} et la coiffe.</p>',
       'quelques grammes de sucre décident ici si le vin sera tendu ou rond.'),
  step('Repos & expédition', 'Ageing & Release', 'Un dernier repos, puis la vente', 11, 'sparkbottle',
       '<p>Les bouteilles terminées reposent encore quelques mois pour que le dosage se fonde, puis elles sont étiquetées et mises en vente — prêtes à s’ouvrir dans un doux « soupir » (jamais une détonation, qui gâche la mousse).</p>',
       'un court repos final laisse tout s’harmoniser pour que la première gorgée chante.'),
 ]},
 'cremant': {'label': 'Crémant', 'cls': 'cremant', 'steps': [
  step('Vendange', 'Harvest', 'À la main, en grappes entières', 1, 'grape',
       f'<p>Le crémant est élaboré selon la {G("méthode traditionnelle", "méthode traditionnelle")} <b>hors</b> de la Champagne — en Alsace, dans la Loire, en Bourgogne, à Limoux, à Bordeaux, à Die, dans le Jura et en Savoie. Comme le champagne, il doit être <b>vendangé à la main en grappes entières</b>, avec les cépages propres à chaque région (chenin, chardonnay, pinot, riesling, mauzac…).</p>',
       'la règle de la vendange manuelle en grappes entières permet au crémant de revendiquer la même méthode de qualité que le champagne.'),
  step('Pressurage en grappes entières', 'Whole-bunch Pressing', 'Doux, rendements plafonnés', 2, 'press',
       '<p>Comme en Champagne, les grappes entières sont pressées doucement, avec des rendements en jus limités, pour obtenir un jus de base net et pâle.</p>',
       'le même pressurage doux garde le crémant frais et fin plutôt que grossier.'),
  step('Fermentation alcoolique', 'First Fermentation', 'Le vin de base, tranquille', 3, 'ferment',
       f'<p>Le jus fermente en un {G("base wine", "vin de base")} sec et très acide, exactement comme pour le champagne.</p>',
       'un vin de base vif est le fondement de bulles vives.'),
  step('Assemblage', 'Assemblage', 'Assembler la cuvée', 4, 'blend',
       '<p>Les vins de base sont assemblés en une cuvée — exprimant souvent les cépages d’une seule région plutôt que les assemblages de nombreux villages de la Champagne.</p>',
       'l’assemblage équilibre le vin et fixe le style de chaque producteur.'),
  step('Mise en tirage', 'Tirage', 'Levures + sucre, puis capsule', 5, 'tirage',
       f'<p>Mis en bouteille avec la {G("liqueur de tirage", "liqueur de tirage")} et capsulé pour lancer la seconde fermentation — exactement le même {G("tirage", "tirage")} qu’en Champagne.</p>',
       'la fermentation en bouteille est précisément ce qui en fait un vin de « méthode traditionnelle ».'),
  step('Prise de mousse', 'Second Fermentation in Bottle', 'Les bulles naissent en bouteille', 6, 'mousse',
       f'<p>La {G("prise de mousse", "prise de mousse")} a lieu dans chaque bouteille fermée et emprisonne le CO₂ en bulles fines.</p>',
       'la même physique qu’en Champagne — une mousse réelle, fine et persistante.'),
  step('Élevage sur lie', 'Ageing on the Lees', 'Au moins 9 mois', 7, 'lees',
       f'<p>Le crémant doit reposer {G("sur lie", "sur lie")} au moins <b>9 mois</b> (contre 15 pour le champagne) — l’une des rares vraies différences. Beaucoup de producteurs vont bien au-delà pour gagner en caractère d’{G("autolysis", "autolyse")}.</p>',
       'ce minimum plus court explique en partie pourquoi un bon crémant offre la méthode champenoise à un prix plus doux.'),
  step('Remuage', 'Riddling', 'Les lies vers le col', 8, 'remuage',
       f'<p>Les bouteilles sont remuées — le {G("remuage", "remuage")} — à la main ou en {G("gyropalette", "gyropalette")} pour rassembler les lies dans le col.</p>',
       'la même étape de préparation à la limpidité qu’en Champagne.'),
  step('Dégorgement', 'Disgorgement', 'Les lies expulsées', 9, 'disgorge',
       f'<p>Le glaçon de lies est expulsé sous pression — le {G("dégorgement", "dégorgement")} —, laissant un vin limpide.</p>',
       'on retire le dépôt en gardant les bulles.'),
  step('Dosage & bouchage', 'Dosage & Corking', 'Le sucre fixé, puis le bouchon', 10, 'dosage',
       f'<p>Un {G("dosage", "dosage")} fixe le style, puis on pose le bouchon, le {G("muselet", "muselet")} et la coiffe.</p>',
       'la touche finale qui équilibre le vin.'),
  step('Expédition', 'Release', 'Prêt à déguster', 11, 'sparkbottle',
       '<p>Après un court repos, le crémant est étiqueté et mis en vente — souvent d’un superbe rapport qualité-prix pour un vrai effervescent fermenté en bouteille.</p>',
       'la preuve que la méthode champenoise voyage bien à travers la France.'),
 ]},
 'ancestrale': {'label': 'Méthode ancestrale', 'cls': 'ancestrale', 'steps': [
  step('Vendange', 'Harvest', 'Des raisins mûrs et sains', 1, 'grape',
       '<p>La plus ancienne de toutes les méthodes effervescentes — plus ancienne que le champagne. Des cépages comme le mauzac (Limoux), le gamay (Bugey-Cerdon) ou le muscat sont cueillis avec assez de sucre naturel pour porter une fermentation unique, inachevée.</p>',
       'tout dépend du sucre du raisin lui-même — rien n’est ajouté ensuite.'),
  step('Pressurage', 'Pressing', 'Le jus en cuve', 2, 'press',
       '<p>Les raisins sont pressés et le jus envoyé en cuve pour commencer une fermentation unique.</p>',
       'un départ net pour la seule et unique fermentation de ce vin.'),
  step('La fermentation unique commence', 'Single Fermentation begins', 'Commencée — mais pas achevée', 3, 'ferment',
       '<p>La fermentation démarre en cuve, souvent fraîche et lente. Surtout, on <b>ne la laisse pas finir</b> : le vigneron surveille la baisse du sucre jusqu’au point exact.</p>',
       'tout est affaire de moment : trop tôt, le vin est sucré et trop gazeux ; trop tard, il est plat.'),
  step('Mise en bouteille précoce', 'Early Bottling', 'En bouteille en pleine fermentation — sans ajout', 4, 'tirage',
       '<p>Alors qu’il fermente encore, le vin est mis en bouteille et fermé — le plus souvent par une capsule. <b>Ni levures ni sucre ne sont ajoutés</b> : le sucre naturel restant suffit.</p>',
       f'cette fermentation unique, ininterrompue, est ce qui définit la {G("méthode ancestrale", "méthode ancestrale")}.'),
  step('La fermentation s’achève en bouteille', 'Fermentation Finishes in Bottle', 'Une bulle douce et naturelle', 5, 'mousse',
       '<p>La fin de la fermentation se fait dans la bouteille fermée et emprisonne le CO₂ en une effervescence douce et naturelle. La pression est en général plus basse qu’en Champagne, et le vin est souvent trouble et légèrement sucré.</p>',
       f'le charme d’un {G("pétillant naturel", "pétillant naturel")} tient justement à cette fraîcheur rustique, légèrement pétillante.'),
  step('Dégorger ou laisser trouble', 'Disgorge or Leave Cloudy', 'Facultatif — sans dosage', 6, 'disgorge',
       f'<p>Certains producteurs dégorgent les lies pour un vin plus limpide ; beaucoup les laissent pour un « pét-nat » trouble et plein de caractère. Dans les deux cas, <b>pas de {G("dosage", "dosage")}</b> : le vin est mis en bouteille tel que la nature l’a laissé.</p>',
       'c’est un choix de style, pas une règle — la limpidité ou l’authenticité rustique.', opt=True),
  step('Expédition', 'Release', 'À boire jeune et frais', 7, 'sparkbottle',
       '<p>Les vins de méthode ancestrale — la blanquette de Limoux méthode ancestrale, le bugey-cerdon, le gaillac, la clairette de Die — se boivent jeunes, légèrement rafraîchis.</p>',
       'la fraîcheur et l’immédiateté comptent ici, pas un long vieillissement.'),
 ]},
 'charmat': {'label': 'Méthode Charmat', 'cls': 'charmat', 'steps': [
  step('Vendange', 'Harvest', 'Des cépages aromatiques', 1, 'grape',
       '<p>La méthode en cuve convient aux cépages <b>aromatiques</b> dont on veut garder le parfum frais et floral — le glera (pour le prosecco), le muscat (pour l’asti) et bien des styles fruités.</p>',
       'toute la méthode est conçue pour préserver les arômes primaires de fruits et de fleurs.'),
  step('Vin de base', 'Base Wine', 'Pressé et fermenté une première fois', 2, 'ferment',
       f'<p>Les raisins sont pressés et fermentés en un {G("base wine", "vin de base")} tranquille, frais et fruité, comme d’habitude.</p>',
       'un vin de base net et aromatique est justement ce que la méthode en cuve veut garder intact.'),
  step('Cuve close', 'Second Fermentation in Tank', 'Les bulles naissent en cuve sous pression', 3, 'autoclave',
       f'<p>Voici la grande différence : la seconde fermentation se fait dans une grande cuve en acier fermée et sous pression (<i>autoclave</i>) — la {G("méthode charmat", "méthode Charmat")} (ou <i>cuve close</i>). Tout le lot prend mousse ensemble, en quelques semaines plutôt qu’en quelques années.</p>',
       'une fermentation en cuve rapide et fraîche enferme les arômes frais de raisin qu’un long élevage sur lies masquerait.'),
  step('Sur lie (court)', 'Brief Lees Contact', 'Facultatif — en général court', 4, 'lees',
       f'<p>La plupart des vins Charmat ne passent que peu ou pas de temps sur {G("lees", "lies")}, pour rester éclatants et fruités — même si un style « Charmat lungo » repose plus longtemps pour un peu plus de complexité.</p>',
       'garder un contact court avec les lies est voulu — cela préserve le caractère frais et primaire.', opt=True),
  step('Filtration isobare', 'Filter under Pressure', 'Refroidi et clarifié', 5, 'clarify',
       '<p>Le vin effervescent est refroidi et filtré <b>sous pression</b> pour rester limpide et garder ses bulles.</p>',
       'filtrer sous pression retire les levures sans laisser échapper les bulles.'),
  step('Tirage isobare', 'Bottling & Dosage', 'Mis en bouteille sous pression', 6, 'dosage',
       f'<p>Avec une tireuse à contre-pression, le vin est mis en bouteille sous pression et reçoit son {G("dosage", "dosage")}, qui fixe le niveau de sucre (le prosecco est souvent extra-dry ; l’asti plus sucré).</p>',
       'la mise en bouteille isobare est l’astuce qui amène les bulles de la cuve à la bouteille sans les perdre.'),
  step('Expédition', 'Release', 'À boire frais et jeune', 7, 'sparkbottle',
       '<p>Les effervescents Charmat sont faits pour être bus jeunes, quand leurs arômes frais de fruits et de fleurs sont les plus vifs.</p>',
       'ces vins sont faits pour une fraîcheur immédiate et joyeuse — pas pour la cave.'),
 ]},
}

PROSE = {
 'champagne': ('Champagne — méthode traditionnelle',
  f'''
        <p>Le champagne est la référence de la {G("méthode traditionnelle", "méthode traditionnelle")} : un {G("base wine", "vin de base")} tranquille est assemblé ({G("assemblage", "assemblage")}), mis en bouteille avec une {G("liqueur de tirage", "liqueur de tirage")}, et fermente une <b>seconde fois dans la bouteille</b> ({G("prise de mousse", "prise de mousse")}). Un long élevage {G("sur lie", "sur lie")}, puis le {G("remuage", "remuage")}, le {G("dégorgement", "dégorgement")} et le {G("dosage", "dosage")} achèvent le vin. Seuls les raisins cultivés et vendangés à la main en Champagne peuvent porter ce nom.</p>
      '''),
 'cremant': ('Crémant — la méthode au-delà de la Champagne',
  f'''
        <p>Le crémant, c’est exactement la même méthode, pratiquée <b>hors</b> de la Champagne — en Alsace, dans la Loire, en Bourgogne, à Limoux, à Bordeaux, à Die, dans le Jura et en Savoie. Vendange manuelle et pressurage en grappes entières sont obligatoires ; la principale différence est un élevage minimal {G("sur lie", "sur lie")} plus court (9 mois). Souvent un excellent rapport qualité-prix pour un vrai effervescent fermenté en bouteille.</p>
      '''),
 'ancestrale': ('Méthode ancestrale — le « pét-nat » d’origine',
  f'''
        <p>La {G("méthode ancestrale", "méthode ancestrale")} est plus ancienne que le champagne et bien plus simple : une fermentation <b>unique</b> est mise en bouteille avant d’être achevée, ce qui emprisonne un CO₂ naturel, sans levures ni sucre ajoutés et sans {G("dosage", "dosage")}. Le {G("pétillant naturel", "pétillant naturel")} d’aujourd’hui la fait revivre — légèrement pétillant, souvent trouble. Les classiques : blanquette de Limoux méthode ancestrale, bugey-cerdon, clairette de Die, gaillac.</p>
      '''),
 'charmat': ('Méthode Charmat — la cuve close',
  f'''
        <p>La {G("méthode charmat", "méthode Charmat")} (méthode en cuve / <i>cuve close</i>) fait la seconde fermentation dans une grande <b>cuve sous pression</b> plutôt qu’en bouteille, puis met en bouteille sous pression. Rapide et axée sur le fruit, elle est idéale pour les cépages aromatiques — c’est la méthode du prosecco et de l’asti.</p>
      '''),
}


def main():
    s = PAGE.read_text()
    if 'S_FR' in s:
        raise SystemExit('already bilingual')
    s = sub1(s, '<title>How Sparkling Wine Is Made — Illustrated</title>',
             '<title data-fr="Comment se font les vins effervescents" data-en="How Sparkling Wine Is Made — Illustrated">Comment se font les vins effervescents</title>', 'title')
    s = bilingual(s, '<h1>', 'How Sparkling Wine Is Made', '</h1>', 'Comment se font les effervescents', 'h1')
    p_en = ('How the bubbles get into the bottle — the four French roads to sparkling wine.\n     Tap any step to open the details, '
            'hover the <span class="gdemo">underlined terms</span> for a quick definition.')
    s = bilingual(s, '<p>', p_en, '</p>',
                  'Comment les bulles entrent dans la bouteille : les quatre routes françaises vers le vin effervescent. '
                  'Touchez une étape pour en lire le détail, survolez les <span class="gdemo">termes soulignés</span> pour une définition rapide.', 'header p')
    s = bilingual(s, '<div class="tab" data-k="ancestrale">', 'M&eacute;thode Ancestrale', '</div>', 'Méthode ancestrale', 'tab ancestrale')
    s = bilingual(s, '<div class="hint">',
                  'Showing <b>Champagne</b> and <b>Cr&eacute;mant</b> side-by-side &mdash; both the M&eacute;thode Traditionnelle. Switch on <b>Ancestrale</b> (p&eacute;t-nat) or <b>Charmat</b> (tank method) to compare.',
                  '</div>',
                  'Affichage : <b>Champagne</b> et <b>Crémant</b> côte à côte — tous deux en méthode traditionnelle. Activez <b>Ancestrale</b> (pét-nat) ou <b>Charmat</b> (cuve close) pour comparer.', 'hint')
    s = bilingual(s, '<div class="empty" id="empty">',
                  'Select a step in the flow to read what happens, why it matters,<br>and its French name.', '</div>',
                  'Choisissez une étape pour lire ce qui s’y passe, pourquoi c’est important,<br>et son nom en anglais.', 'empty')
    s = bilingual(s, '<h2>', 'The four roads to bubbles', '</h2>', 'Les quatre routes vers les bulles', 'prose h2')
    for cls, (sum_fr, body_fr) in PROSE.items():
        s = details(s, cls, sum_fr, body_fr, 'details ' + cls)
    s = bilingual(s, '<h2>', 'Glossary', '</h2>', 'Glossaire', 'glossary h2')
    s = bilingual(s, '<footer>',
                  '\n    Interactive guide to French sparkling wine &middot; A Quick Glance at French Wine &middot; Chris Paul.<br>\n    Works fully offline &mdash; a single self-contained file.\n  ',
                  '</footer>',
                  '\n    Guide interactif des vins effervescents français · A Quick Glance at French Wine · Christophe A. Paul.<br>\n    Fonctionne entièrement hors ligne — un seul fichier autonome.\n  ', 'footer')
    s = sub1(s, '/* ---------- STEP PICTURES ---------- */',
             '/* ---------- FRENCH DATA (2026-10-19) — same keys; `fr` holds the English name in this set ---------- */\n'
             f'const GLOSS_FR = {js(GLOSS_FR)};\nconst S_FR = {js(S_FR)};\n{LANG_JS}\n/* ---------- STEP PICTURES ---------- */', 'pictures marker')
    s = sub1(s, '      const st=S[key].steps[i];\n      thumb.src', '      const st=SS()[key].steps[i];\n      thumb.src', 'hover pic S')
    s = sub1(s, '  const d = S[key];', '  const d = SS()[key];', 'buildFlow S')
    s = sub1(s, "(st.opt?' <span class=\"badge\">optional</span>':'')", "(st.opt?' <span class=\"badge\">'+UI('optional')+'</span>':'')", 'badge')
    s = sub1(s, '  const st=S[key].steps[i];\n  emptyEl', '  const st=SS()[key].steps[i];\n  emptyEl', 'select S')
    s = sub1(s, "'<div><div class=\"ph\">'+S[key].label+' · '+st.ph+(st.opt?' · optional':'')+'</div>'",
             "'<div><div class=\"ph\">'+SS()[key].label+' · '+st.ph+(st.opt?' · '+UI('optional'):'')+'</div>'", 'ph')
    old_g = '''Object.keys(GLOSS).sort((a,b)=>GLOSS[a][0].localeCompare(GLOSS[b][0])).forEach(k=>{
  // avoid duplicate display entries (malolactique/malolactic map to same idea)
  if(k==='malolactique') return;
  const d=document.createElement('div'); d.className='glitem';
  d.innerHTML='<dt>'+GLOSS[k][0]+'</dt><dd>'+GLOSS[k][1]+'</dd>';
  gEl.appendChild(d);
});'''
    new_g = '''function renderGloss(){
  const G=GG(); gEl.innerHTML='';
  Object.keys(G).sort((a,b)=>G[a][0].localeCompare(G[b][0],isEN()?'en':'fr')).forEach(k=>{
    const d=document.createElement('div'); d.className='glitem';
    d.innerHTML='<dt>'+G[k][0]+'</dt><dd>'+G[k][1]+'</dd>';
    gEl.appendChild(d);
  });
}
renderGloss();'''
    s = sub1(s, old_g, new_g, 'glossary list')
    old_l = '''  const key=text.toLowerCase().trim().replace(/[.,;:]$/,'');
  if(GLOSS[key]) return GLOSS[key];
  for(const k in GLOSS){ if(k.toLowerCase()===key) return GLOSS[k]; }'''
    s = sub1(s, old_l, old_l.replace("  const key=", "  const G=GG();\n  const key=").replace('GLOSS', 'G'), 'lookup')
    s = sub1(s, 'const g=lookup(el.textContent);', 'const g=lookup(el.dataset.g||el.textContent);', 'wire lookup')
    s = sub1(s, 'wireBigPic();\nrenderTabs(); renderFlows();', 'wireBigPic();\nrenderTabs(); renderFlows();\n' + LANG_INIT, 'init')
    PAGE.write_text(s)
    print(PAGE.name, 'now bilingual:', sum(len(v['steps']) for v in S_FR.values()), 'steps,', len(GLOSS_FR), 'glossary entries')


if __name__ == '__main__':
    main()
