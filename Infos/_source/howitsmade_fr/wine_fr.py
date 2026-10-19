"""French version of « How wine is made.html » (interactive) — 2026-10-19, user request.
Run once from WEB Site/Infos:  python3 _source/howitsmade_fr/wine_fr.py
(The page is hand-written: this script edits it in place; a second run stops with "expected 1 match".)
Backup of the English-only page: WEB Site/_backups/2026-10-19/How wine is made.html
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import A, js, sub1, bilingual, details, LANG_JS, LANG_INIT  # noqa: E402

PAGE = Path(__file__).resolve().parents[2] / "How it's made" / 'How wine is made.html'

G = lambda key, word: f"<span class='g' data-g='{key}'>{word}</span>"   # glossary term inside French text
WHY = '<b>Pourquoi c’est important :</b> '

GLOSS_FR = {
 "sulphur": ["Soufre (SO₂) — <i>sulphur</i>", "Le dioxyde de soufre, principal antioxydant et antiseptique du vigneron. Un peu protège le jus et le vin de l’oxydation et des micro-organismes indésirables ; les vins « nature » cherchent à en mettre le moins possible."],
 "must": ["Moût — <i>must</i>", "Le jus de raisin fraîchement foulé ou pressé, avec (pour les rouges) les pellicules, la pulpe et les pépins, avant et pendant la fermentation."],
 "foudres": ["Foudre", "Une grande cuve en bois (bien plus grande qu’une barrique), utilisée pour fermenter ou élever le vin sans lui donner beaucoup de goût boisé."],
 "cuvaison": ["Cuvaison", "La période où, pour un vin rouge, jus, pellicules et pépins macèrent ensemble <b>pendant la fermentation alcoolique</b> : c’est là que s’extraient la couleur et les tanins."],
 "pigeage": ["Pigeage — <i>punching down</i>", "Enfoncer le chapeau de marc qui flotte dans le jus, à la main ou au pigeou, pour continuer d’extraire couleur et tanins."],
 "remontage": ["Remontage — <i>pumping over</i>", "Tirer le jus du bas de la cuve et l’arroser sur le chapeau de marc : l’équivalent mécanique du pigeage."],
 "vin de goutte": ["Vin de goutte — <i>free-run wine</i>", "Le vin qui s’écoule de la cuve par simple gravité, avant tout pressurage. Généralement la fraction la plus fine."],
 "vin de presse": ["Vin de presse — <i>press wine</i>", "Le vin extrait en pressant le marc une fois le vin de goutte écoulé. Plus coloré et plus tannique ; assemblé en partie, ou gardé à part."],
 "marc": ["Marc — <i>pomace</i>", "Le gâteau de pellicules, pépins et pulpe qui reste après le pressurage. Il peut être distillé pour faire l’eau-de-vie qui porte aussi le nom de <i>marc</i>."],
 "malolactic fermentation": ["Fermentation malolactique — <i>FML</i>", "Une seconde fermentation, due à des bactéries, qui transforme l’acide malique, mordant, en acide lactique, plus doux. Systématique pour les rouges ; facultative pour les blancs, à qui elle donne une note plus ronde, « beurrée »."],
 "malolactique": ["Fermentation malolactique", "Voir <i>fermentation malolactique</i> : des bactéries transforment l’acide malique, mordant, en acide lactique, plus doux, ce qui arrondit le vin."],
 "macerated": ["Macération", "Laisser le jus au contact des pellicules pour en extraire couleur, tanins et arômes. Longue pour les rouges, brève ou absente pour les blancs, courte pour les rosés."],
 "débourbage": ["Débourbage", "Laisser reposer le jus blanc fraîchement pressé pour que les grosses particules (les « bourbes ») tombent au fond, puis soutirer le jus clair avant la fermentation."],
 "élevage": ["Élevage", "Littéralement « élever » le vin : sa maturation après la fermentation, en barrique, en foudre ou en cuve, jusqu’à ce qu’il soit prêt à être mis en bouteille."],
 "collage": ["Collage — <i>fining</i>", "Ajouter une colle (blanc d’œuf, bentonite, gélatine…) qui fixe les troubles et les particules dures et les entraîne au fond : le vin s’éclaircit et s’assouplit."],
 "bentonite": ["Bentonite", "Une argile naturelle utilisée pour coller les vins blancs : elle capte les protéines instables qui troubleraient le vin, puis se dépose."],
 "vin de garde": ["Vin de garde", "Un vin fait pour vieillir — avec la structure (tanins, acidité, concentration) pour s’améliorer des années en bouteille, par opposition à un vin à boire jeune."],
 "Botrytis cinerea": ["Botrytis cinerea — pourriture noble", "Un champignon bienfaisant qui, lors d’un automne humide puis sec, flétrit les raisins et concentre leur sucre et leurs arômes : le secret du sauternes, du tokaji et des grands liquoreux."],
 "passerillage": ["Passerillage", "Faire sécher les raisins pour concentrer leur sucre — laissés sur la vigne au-delà de la maturité, ou sur des claies de paille — sans pourriture noble. La base de nombreux <i>vins de paille</i>."],
 "mutage": ["Mutage", "Arrêter la fermentation en ajoutant de l’alcool neutre de raisin : il tue les levures alors qu’il reste du sucre, ce qui donne les <i>vins doux naturels</i> et les vins de type porto."],
 "grand vin": ["Grand vin", "Le vin le plus prestigieux d’un producteur — issu des raisins les plus mûrs et de l’élevage le plus soigné (et le plus long)."],
}


def step(t, en_name, sub, n, html, why, opt=False):
    d = {'t': t, 'fr': en_name, 'sub': sub, 'ph': f'Étape {n}', 'html': html, 'why': WHY + why}
    if opt:
        d['opt'] = True
    return d


S_FR = {
 'red': {'label': 'Vin rouge', 'cls': 'red', 'steps': [
  step('Vendange', 'Harvesting', 'À la main ou à la machine', 1,
       '<p>Les raisins sont cueillis soit <b>à la main</b> — plus délicatement, et c’est la seule solution sur les coteaux raides ou en terrasses — soit <b>à la machine</b>, plus rapide et moins chère. La vendange manuelle permet un premier tri des grappes saines dès la vigne.</p>',
       'la date et le mode de cueillette fixent le sucre, l’acidité et l’état sanitaire des raisins — tout le reste en dépend.'),
  step('Tri', 'Sorting', 'Écarter les fruits verts ou pourris', 2,
       '<p>Sur une <b>table de tri</b> (ou un trieur optique), on retire les baies vertes, passerillées ou pourries, les feuilles et autres débris, pour ne garder que des fruits sains.</p>',
       'une simple poignée de pourri ou de raisins verts peut gâter toute une cuve.'),
  step('Foulage & éraflage', 'Crushing & Destemming', 'Facultatif — certains gardent les grappes entières', 3,
       f'<p>L’<b>érafloir-fouloir</b> fait éclater les baies pour libérer le jus et, le plus souvent, les détache de la rafle. Certains rouges sont vinifiés en <b>grappes entières</b> (macération carbonique dans le Beaujolais, vendange entière dans le Rhône et en Bourgogne). On peut ajouter ici un peu de {G("sulphur", "soufre")}.</p>',
       'mûres, les rafles apportent de la tenue et une note poivrée ; vertes, des tanins durs — d’où « facultatif ».', opt=True),
  step('Cuvaison', 'Maceration + Fermentation', 'Macération et fermentation, ensemble', 4,
       f'<p>C’est le cœur de la vinification en rouge. Dans la cuve, les levures transforment le sucre en alcool <b>pendant</b> que le jus macère avec les pellicules : c’est la {G("cuvaison", "cuvaison")}. Le chapeau de marc qui flotte est réincorporé par {G("pigeage", "pigeage")} ou par {G("remontage", "remontage")} pour extraire couleur et tanins. La température est contrôlée ; l’étape peut durer de quelques jours à plusieurs semaines.</p>',
       'presque toute la couleur, les tanins et la structure d’un vin rouge se construisent ici.'),
  step('Pressurage', 'Pressing', 'Vin de goutte et vin de presse', 5,
       f'<p>Le {G("vin de goutte", "vin de goutte")} s’écoule d’abord ; le {G("marc", "marc")} restant est ensuite pressé pour en tirer le {G("vin de presse", "vin de presse")}, plus sombre et plus ferme. Le vigneron décide quelle part de vin de presse réassembler, ou pas.</p>',
       'le vin de presse apporte couleur et mâche — un peu donne de la profondeur, trop rend le vin dur.', opt=True),
  step('Fermentation malolactique', 'Malolactic Fermentation', 'Assouplir l’acidité', 6,
       '<p>Une seconde fermentation, due à des <b>bactéries</b>, transforme l’acide malique, mordant, en acide lactique, plus doux. Pour les rouges, elle est pratiquement toujours faite, et elle stabilise aussi le vin.</p>',
       'elle arrondit un vin jeune et acide, et évite que la transformation se fasse plus tard, en bouteille.'),
  step('Élevage en barrique', 'Barrel Ageing', 'Facultatif — jusqu’à ~24 mois', 7,
       f'<p>Un {G("vin de garde", "vin de garde")} est élevé ({G("élevage", "élevage")}) en <b>barriques</b> de chêne ou en {G("foudres", "foudres")} plus grands, parfois jusqu’à deux ans. Le bois neuf apporte des notes épicées et des tanins ; le bois plus ancien laisse surtout le vin respirer et se poser.</p>',
       'le bois et le temps fondent les tanins et ajoutent de la complexité — mais les vins de tous les jours s’en passent pour rester frais et abordables.', opt=True),
  step('Collage & filtration', 'Fining & Filtering', 'Facultatif — clarifier le vin', 8,
       f'<p>Pour polir le vin avant la mise en bouteille, on peut le <b>coller</b> — traditionnellement au <b>blanc d’œuf</b> ({G("collage", "collage")}) — et/ou le <b>filtrer</b>. Les deux éliminent les troubles et les particules dures. Certains producteurs ne font ni l’un ni l’autre et mettent en bouteille « non collé, non filtré ».</p>',
       'le vin devient limpide et stable, même si une filtration poussée peut lui enlever un peu de texture.', opt=True),
  step('Mise en bouteille', 'Bottling', 'Prêt à vendre ou à garder', 9,
       '<p>Le vin terminé est mis en bouteille, bouché ou capsulé, puis étiqueté. Les vins de garde peuvent encore reposer des mois ou des années avant leur mise en vente.</p>',
       'le voyage de la vigne au verre est achevé — le reste est affaire de patience.'),
 ]},
 'white': {'label': 'Vin blanc', 'cls': 'white', 'steps': [
  step('Vendange', 'Harvesting', 'Souvent plus tôt, pour garder l’acidité', 1,
       '<p>Comme pour le rouge — à la main ou à la machine — mais les blancs sont souvent cueillis <b>plus tôt</b> et à la <b>fraîcheur du matin ou de la nuit</b>, pour préserver l’acidité et les arômes.</p>',
       'la vivacité et le parfum d’un blanc se perdent vite avec la surmaturité ou la chaleur.'),
  step('Tri', 'Sorting', 'Écarter les fruits indésirables', 2,
       '<p>Les baies abîmées ou vertes et les débris sont retirés avant le pressurage.</p>',
       'sans macération pour les masquer, les défauts se voient vite dans un vin blanc.'),
  step('Foulage / éraflage', 'Crushing / Destemming', 'Facultatif — souvent pressurage direct', 3,
       '<p>Les blancs sont souvent <b>pressés en grappes entières</b>, sans foulage, pour obtenir le jus le plus net. Quand on foule, c’est en douceur, et le contact avec les pellicules est volontairement bref ou absent.</p>',
       'une longue macération donnerait de la couleur et une amertume phénolique que la plupart des blancs ne recherchent pas.', opt=True),
  step('Pressurage', 'Pressing', 'Le jus est extrait tout de suite', 4,
       '<p>Contrairement au rouge, les blancs sont <b>pressés avant la fermentation</b> : les pellicules sont séparées tout de suite et seul le jus continue. Le <b>résidu</b> peut servir pour du vin de table ordinaire.</p>',
       'presser avant de fermenter est <i>la</i> différence fondamentale entre vinification en blanc et en rouge.'),
  step('Débourbage', 'Débourbage / Clarification', 'Laisser reposer le jus', 5,
       f'<p>Le jus trouble est refroidi et laissé au repos pour que les grosses particules (les « bourbes ») tombent ; le jus clair est soutiré avant la fermentation. Un peu de {G("sulphur", "soufre")} le protège entre-temps.</p>',
       'fermenter un jus propre donne un vin plus pur et plus précis.'),
  step('Fermentation alcoolique', 'Fermentation', 'Plus fraîche que pour le rouge', 6,
       '<p>Les levures transforment le sucre en alcool, généralement à <b>basse température</b> (12–18 °C) en cuve — ou, pour les grands vins (blancs de Bourgogne, grands bordeaux), en barrique de chêne.</p>',
       'une fermentation fraîche et lente préserve les arômes fragiles, floraux et fruités.'),
  step('Fermentation malolactique', 'Malolactic Fermentation', 'Facultative pour les blancs', 7,
       '<p>Elle n’est pas automatique pour les blancs. On la <b>favorise</b> pour les styles riches, élevés sous bois (blancs de Bourgogne), pour leur donner une rondeur crémeuse — et on la <b>bloque</b> pour les styles vifs et aromatiques (sauvignon, riesling), pour garder leur fraîcheur.</p>',
       'c’est le choix de style le plus décisif entre un blanc « beurré » et un blanc « vif ».', opt=True),
  step('Collage & clarification', 'Fining & Clarification', 'Souvent à la bentonite', 8,
       f'<p>Les blancs sont généralement collés — souvent avec de l’argile, la {G("bentonite", "bentonite")}, qui retire les protéines instables — puis clarifiés ou filtrés pour rester limpides et ne pas se troubler.</p>',
       'un blanc trouble en rayon paraît défectueux, même s’il est bon.', opt=True),
  step('Mise en bouteille', 'Bottling', 'Le plus souvent vendu jeune', 9,
       '<p>La plupart des blancs sont mis en bouteille et vendus jeunes pour saisir leur fraîcheur ; quelques blancs de garde sont gardés plus longtemps.</p>',
       'la fraîcheur est la valeur première de la plupart des blancs — une mise rapide la protège.'),
 ]},
 'sweet': {'label': 'Liquoreux & vendanges tardives', 'cls': 'sweet', 'steps': [
  step('Concentrer les raisins', 'Concentrating the Grapes', 'Botrytis · séchage · gel', 1,
       f'<p>La douceur commence à la vigne, en concentrant le sucre à l’extrême : le {G("Botrytis cinerea", "Botrytis cinerea")} (pourriture noble) flétrit les baies (sauternes, tokaji, sélection de grains nobles d’Alsace) ; le {G("passerillage", "passerillage")} les sèche sur la souche ou sur la paille ; ou bien on laisse les raisins <b>geler</b> pour le vin de glace.</p>',
       'impossible de tricher — un grand liquoreux se fait avec une fraction de la récolte normale.'),
  step('Tries successives', 'Selective Harvest', 'Plusieurs passages, baie par baie', 2,
       '<p>Les raisins botrytisés mûrissent inégalement : les vendangeurs passent <b>plusieurs fois</b> dans la vigne (les <i>tries</i>), en ne prenant que les baies flétries à leur optimum. Un travail minutieux pour un rendement minuscule.</p>',
       'ce travail manuel explique la rareté et le prix des plus grands liquoreux.'),
  step('Pressurage', 'Pressing', 'Lent — le jus est un sirop', 3,
       '<p>Les raisins déshydratés ne donnent que très peu de jus, et lentement. Il en sort un moût extrêmement sucré.</p>',
       'les rendements peuvent tomber au quart de ceux d’un vin sec — la concentration se paie en quantité.'),
  step('Fermentation partielle', 'Fermentation (partial)', 'S’arrête avec du sucre restant', 4,
       f'<p>Les levures commencent à transformer le sucre en alcool mais <b>ne peuvent pas finir</b> : la masse de sucre et l’alcool qui monte les épuisent. La fermentation est volontairement <b>arrêtée</b> par le froid et l’ajout de {G("sulphur", "soufre")} alors qu’il reste beaucoup de sucre naturel.</p>',
       'l’équilibre entre alcool, sucre et acidité trouvé ici définit tout le vin.'),
  step('Mutage / sulfitage', 'Stopping & Stabilising', 'Éliminer les levures', 5,
       f'<p>Les levures restantes sont éliminées par le froid, la centrifugation, la pasteurisation ou le soutirage, pour qu’elles ne repartent pas. (Pour les <i>vins doux naturels</i>, la fermentation est arrêtée en ajoutant de l’alcool de raisin : le {G("mutage", "mutage")}.) Le sucre résiduel se situe le plus souvent vers <b>50–150 g/L</b>.</p>',
       'une bouteille qui refermenterait serait perdue — la stabilité est indispensable pour un vin doux.', opt=True),
  step('Élevage & mise', 'Ageing & Bottling', 'Souvent très longue garde', 6,
       f'<p>Beaucoup de liquoreux font un long {G("élevage", "élevage")} (souvent en barrique) et sont réputés pour leur longévité : ils évoluent pendant des décennies en bouteille.</p>',
       'le sucre et l’acidité sont des conservateurs naturels — ce sont parmi les vins de plus longue garde.'),
 ]},
 'rose': {'label': 'Rosé', 'cls': 'rose', 'steps': [
  step('Vendange & tri', 'Harvesting & Sorting', 'Raisins noirs, cueillis frais', 1,
       '<p>Le rosé se fait avec des <b>raisins noirs</b>, en général cueillis pour garder une acidité vive, puis triés comme pour tout vin de qualité.</p>',
       'le rosé vit de sa fraîcheur : il faut des raisins sains et croquants.'),
  step('Macération courte', 'Brief Skin Contact', 'Quelques heures, pas des jours', 2,
       '<p>La couleur vient d’une macération <b>courte</b> sur les pellicules — quelques heures seulement. Deux voies : le <b>pressurage direct</b> (pressé presque comme un blanc, très pâle — le style provençal) ou la <b>saignée</b>, où l’on « saigne » du jus rose d’une cuve de rouge.</p>',
       'la durée de macération fixe exactement la couleur d’un rosé, du plus pâle au plus soutenu.'),
  step('Pressurage / saignée', 'Pressing / Running-off', 'Séparer le jus des pellicules', 3,
       '<p>Le jus légèrement coloré est séparé des pellicules. Avec la <b>saignée</b>, le vin rouge resté dans la cuve s’en trouve concentré.</p>',
       'la réglementation européenne interdit de mélanger rouge et blanc pour faire un rosé tranquille — la couleur doit venir des pellicules.'),
  step('Fermentation fraîche', 'Cool Fermentation', 'Comme pour un blanc', 4,
       '<p>À partir d’ici, le rosé suit la <b>route du vin blanc</b> : le jus fermente au frais en cuve pour garder ses arômes délicats de fruits rouges et de fleurs.</p>',
       'la maîtrise de la température protège le caractère frais et fruité qu’on aime dans le rosé.'),
  step('Collage & mise', 'Fining & Bottling', 'Vendu jeune', 5,
       '<p>Légèrement collé et clarifié, puis mis en bouteille tôt. L’immense majorité des rosés est faite pour être bue fraîche dans l’année.</p>',
       'le rosé est à son meilleur jeune et frais — la plupart ne sont pas faits pour vieillir.', opt=True),
 ]},
}

PROSE = {
 'red': ('Le vin rouge',
  f'''
        <p>Après la vendange, les raisins sont égrappés et triés — à la main ou à la machine — pour écarter les fruits
        indésirables et les débris. Les baies sont ensuite foulées et le plus souvent éraflées. On peut alors ajouter
        un peu de {G("sulphur", "soufre")} pour éviter que le {G("must", "moût")} ne s’oxyde trop tôt ; celui-ci est
        ensuite pompé dans des cuves en inox ou des cuves en bois ({G("foudres", "foudres")}).</p>
        <p>Pour le vin rouge, macération et fermentation alcoolique se font <b>ensemble</b>, dans la même cuve : c’est
        la {G("cuvaison", "cuvaison")}. Pendant quelques jours à quelques semaines, le chapeau de marc reste au contact du
        jus, par {G("pigeage", "pigeage")} ou par {G("remontage", "remontage")}, pour extraire couleur et tanins. À la fin de
        la fermentation, le {G("vin de goutte", "vin de goutte")} est écoulé et le {G("marc", "marc")} restant est pressé pour
        donner le {G("vin de presse", "vin de presse")}, réassemblé ou non.</p>
        <p>Le vin repose ensuite pendant que la {G("malolactic fermentation", "fermentation malolactique")} assouplit son
        acidité. Un {G("vin de garde", "vin de garde")} peut être élevé en barrique ({G("élevage", "élevage")}) jusqu’à environ
        24 mois avant d’être collé — souvent au blanc d’œuf ({G("collage", "collage")}) — et/ou filtré, puis mis en bouteille.</p>
      '''),
 'white': ('Le vin blanc',
  f'''
        <p>L’immense variété des vins blancs reflète autant de vinifications, chacune adaptée à un vin. La vinification
        en blanc diffère du rouge à plusieurs étapes — avant tout, les pellicules sont rarement
        {G("macerated", "mises à macérer")} avec le jus. Les raisins sont en général pressés tout de suite et seul le jus
        est mis à fermenter.</p>
        <p>Après le pressurage, le jus trouble est laissé au repos pour que les matières solides se déposent — c’est
        le {G("débourbage", "débourbage")}. La fermentation se fait ensuite plus au frais que pour le rouge, pour protéger
        les arômes délicats. La plupart des blancs ne sont pas élevés en barrique, sauf certains grands vins — les grands
        crus de Bourgogne, les crus classés de Bordeaux. La {G("malolactic fermentation", "fermentation malolactique")} n’est
        pas automatique pour les blancs, mais elle est de plus en plus pratiquée pour les grands vins. Un dernier collage
        (souvent à la {G("bentonite", "bentonite")}) et une clarification précèdent la mise en bouteille.</p>
      '''),
 'sweet': ('Les liquoreux & vendanges tardives',
  f'''
        <p>Les vins doux gardent du sucre dans le vin fini : on part de raisins bien plus mûrs et concentrés, puis on
        arrête la fermentation avant que les levures n’aient consommé tout le sucre. La concentration peut venir du
        {G("Botrytis cinerea", "Botrytis cinerea")} (pourriture noble), qui flétrit les baies — comme à Sauternes, en
        Quarts-de-Chaume dans la Loire, en sélection de grains nobles d’Alsace ou à Tokaj —, du séchage sur la souche
        ({G("passerillage", "passerillage")}) ou du gel (vin de glace, <i>Eiswein</i>).</p>
        <p>La fermentation est arrêtée par le froid, par l’ajout de {G("sulphur", "dioxyde de soufre")} et en éliminant les
        levures par centrifugation, pasteurisation ou soutirage. Les vins obtenus sont très riches — environ 50 à
        150 g/L de sucre résiduel. (Une famille voisine, les <i>vins doux naturels</i> comme le muscat de
        Beaumes-de-Venise, arrête au contraire la fermentation en ajoutant de l’alcool de raisin : c’est le
        {G("mutage", "mutage")}.)</p>
      '''),
 'rose': ('Le rosé',
  '''
        <p>Le rosé tient sa couleur d’une courte macération sur les pellicules, et non d’un mélange de rouge et de blanc
        (interdit pour les vins tranquilles dans l’Union européenne, le champagne étant l’exception notable). Deux
        méthodes principales : le <b>pressurage direct</b>, où les raisins noirs sont pressés presque comme des blancs pour
        une couleur très pâle (le style provençal) ; et la <b>saignée</b>, où l’on tire un peu de jus rose d’une cuve de
        rouge après quelques heures de macération, ce qui donne une couleur plus soutenue — et concentre au passage le
        vin rouge restant. La fermentation et la suite suivent la route du vin blanc.</p>
      '''),
}


def main():
    s = PAGE.read_text()
    if 'S_FR' in s:
        raise SystemExit('already bilingual')
    # ---- static text
    s = sub1(s, '<title>How Wine Is Made — Interactive</title>',
             '<title data-fr="Comment se fait le vin — interactif" data-en="How Wine Is Made — Interactive">Comment se fait le vin — interactif</title>', 'title')
    s = bilingual(s, '<h1>', 'How Wine Is Made', '</h1>', 'Comment se fait <em>le vin</em>', 'h1')
    p_en = ('From vine to bottle — the winemaker\'s road for each style of wine.\n     Tap any step to open the details, '
            'hover the <span class="gdemo">underlined terms</span> for a quick definition.')
    s = bilingual(s, '<p>', p_en, '</p>',
                  'De la vigne à la bouteille : le chemin du vigneron pour chaque style de vin. Touchez une étape pour en lire le détail, '
                  'survolez les <span class="gdemo">termes soulignés</span> pour une définition rapide.', 'header p')
    for k, en, fr in [('red', 'Red', 'Rouge'), ('white', 'White', 'Blanc'), ('sweet', 'Sweet &amp; Late-Harvest', 'Liquoreux &amp; tardifs'), ('rose', 'Rosé', 'Rosé')]:
        s = bilingual(s, f'<div class="tab" data-k="{k}">', en, '</div>', fr, 'tab ' + k)
    s = bilingual(s, '<div class="hint">',
                  'Showing: click <b>Red</b> and <b>White</b> together for the classic side-by-side, or switch to Sweet / Rosé.', '</div>',
                  'Affichage : sélectionnez <b>Rouge</b> et <b>Blanc</b> ensemble pour la comparaison classique, ou passez aux liquoreux / au rosé.', 'hint')
    s = bilingual(s, '<div class="empty" id="empty">',
                  'Select a step in the flow to read what happens, why it matters,<br>and its French name.', '</div>',
                  'Choisissez une étape pour lire ce qui s’y passe, pourquoi c’est important,<br>et son nom en anglais.', 'empty')
    s = bilingual(s, '<h2>', 'In the winemaker\'s words', '</h2>', 'Les mots du vigneron', 'prose h2')
    for cls, (sum_fr, body_fr) in PROSE.items():
        s = details(s, cls, sum_fr, body_fr, 'details ' + cls)
    s = bilingual(s, '<h2>', 'Glossary', '</h2>', 'Glossaire', 'glossary h2')
    s = bilingual(s, '<footer>',
                  '\n    Interactive edition of <i>“How Wine Is Made”</i> · A Quick Glance at French Wine · Chris Paul.<br>\n    Works fully offline — a single self-contained file.\n  ',
                  '</footer>',
                  '\n    Édition interactive de <i>« Comment se fait le vin »</i> · A Quick Glance at French Wine · Christophe A. Paul.<br>\n    Fonctionne entièrement hors ligne — un seul fichier autonome.\n  ', 'footer')
    # ---- script: French data + language-aware rendering
    s = sub1(s, '/* ---------- RENDER ---------- */',
             '/* ---------- FRENCH DATA (2026-10-19) — same keys; `fr` holds the English name in this set ---------- */\n'
             f'const GLOSS_FR = {js(GLOSS_FR)};\nconst S_FR = {js(S_FR)};\n{LANG_JS}\n/* ---------- RENDER ---------- */', 'render marker')
    s = sub1(s, '  const d = S[key];', '  const d = SS()[key];', 'buildFlow S')
    s = sub1(s, "(st.opt?' <span class=\"badge\">optional</span>':'')", "(st.opt?' <span class=\"badge\">'+UI('optional')+'</span>':'')", 'badge')
    s = sub1(s, '  const st=S[key].steps[i];', '  const st=SS()[key].steps[i];', 'select S')
    s = sub1(s, "'<div class=\"ph\">'+S[key].label+' · '+st.ph+(st.opt?' · optional':'')+'</div>'",
             "'<div class=\"ph\">'+SS()[key].label+' · '+st.ph+(st.opt?' · '+UI('optional'):'')+'</div>'", 'ph')
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
    // avoid duplicate display entries (malolactique/malolactic map to same idea)
    if(k==='malolactique') return;
    const d=document.createElement('div'); d.className='glitem';
    d.innerHTML='<dt>'+G[k][0]+'</dt><dd>'+G[k][1]+'</dd>';
    gEl.appendChild(d);
  });
}
renderGloss();'''
    s = sub1(s, old_g, new_g, 'glossary list')
    old_l = '''  const key=text.toLowerCase().trim().replace(/[.,;:]$/,'');
  if(GLOSS[key]) return GLOSS[key];
  for(const k in GLOSS){ if(k.toLowerCase()===key) return GLOSS[k]; }
  // partials
  if(key.includes('malolactic')) return GLOSS['malolactic fermentation'];
  if(key.includes('botrytis')) return GLOSS['Botrytis cinerea'];
  if(key.includes('foudre')) return GLOSS['foudres'];
  if(key.includes('macerat')) return GLOSS['macerated'];
  if(key.includes('grand vin')) return GLOSS['grand vin'];'''
    new_l = old_l.replace("  const key=", "  const G=GG();\n  const key=").replace('GLOSS', 'G')
    s = sub1(s, old_l, new_l, 'lookup')
    s = sub1(s, 'const g=lookup(el.textContent);', 'const g=lookup(el.dataset.g||el.textContent);', 'wire lookup')
    s = sub1(s, '/* init */\nrenderTabs(); renderFlows();', '/* init */\nrenderTabs(); renderFlows();\n' + LANG_INIT, 'init')
    PAGE.write_text(s)
    print(PAGE.name, 'now bilingual:', sum(len(v['steps']) for v in S_FR.values()), 'steps,', len(GLOSS_FR), 'glossary entries')


if __name__ == '__main__':
    main()
