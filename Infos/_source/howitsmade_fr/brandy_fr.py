"""French version of « How brandy is made.html » — 2026-10-19, user request.
Run once from WEB Site/Infos:  python3 _source/howitsmade_fr/brandy_fr.py
Backup of the English-only page: WEB Site/_backups/2026-10-19/How brandy is made.html
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import js, sub1, bilingual, details, LANG_JS, LANG_INIT  # noqa: E402

PAGE = Path(__file__).resolve().parents[2] / "How it's made" / 'How brandy is made.html'

G = lambda key, word: f'<span class="g" data-g="{key}">{word}</span>'
AS = "angels' share"   # glossary key with an apostrophe (no backslashes allowed inside f-string braces before 3.12)
WHY = '<b>Pourquoi c’est important :</b> '

GLOSS_FR = {
 "eau-de-vie": ["Eau-de-vie", "Un alcool limpide distillé à partir de fruits fermentés ou de vin. Le cognac, l’armagnac, le marc et les eaux-de-vie de fruits sont tous des eaux-de-vie."],
 "alambic charentais": ["Alambic charentais — <i>Charentais pot still</i>", "L’alambic en cuivre du Cognac, conduit par charges successives. Sa forme et la <b>double distillation</b> qu’il permet donnent au cognac sa finesse."],
 "alambic armagnaçais": ["Alambic armagnaçais — <i>Armagnac still</i>", "Un petit alambic <b>à colonne</b>, continu : le vin descend à travers des plateaux chauffés en un seul passage, ce qui donne une eau-de-vie moins forte, plus aromatique et plus rustique que le cognac."],
 "brouillis": ["Brouillis", "La « première eau-de-vie », trouble (environ 28–32 % vol.), issue de la première distillation du cognac ; elle est distillée une seconde fois pour donner l’eau-de-vie finale."],
 "première chauffe": ["Première chauffe — <i>first heating</i>", "La première distillation du cognac, qui transforme le vin de base en brouillis, peu alcoolisé."],
 "bonne chauffe": ["Bonne chauffe — <i>the good heating</i>", "La seconde distillation du cognac, décisive : le distillateur fait la coupe et ne garde que le cœur."],
 "the cut": ["La coupe — <i>the cut</i>", "Séparer le distillat en têtes, cœur et queues. Seul le cœur, net, est gardé pour le vieillissement."],
 "cœur": ["Cœur — <i>the heart</i>", "La fraction centrale, pure, de la distillation — vers 70 % vol. — qui devient l’eau-de-vie. Têtes et queues sont écartées ou redistillées."],
 "angels' share": ["Part des anges — <i>angels’ share</i>", "Le vin et l’eau-de-vie qui s’évaporent chaque année à travers le chêne pendant le vieillissement — une perte réelle et mesurable (c’est aussi le nom du champignon noir qui se nourrit de ces vapeurs dans les chais)."],
 "reduction": ["Réduction — <i>reduction</i>", "Abaisser peu à peu le degré d’une eau-de-vie, sortie de fût, jusqu’au degré de mise en bouteille (environ 40 %), en ajoutant de l’eau distillée ou des « petites eaux »."],
 "assemblage": ["Assemblage — <i>blending</i>", "Marier des eaux-de-vie d’âges, de crus et de fûts différents pour créer le style d’une maison — l’art du maître de chai."],
 "grande champagne": ["Grande Champagne", "Le plus recherché des six crus du Cognac (sols crayeux), qui donne les eaux-de-vie les plus fines et de plus longue garde. Viennent ensuite la Petite Champagne, les Borderies et les Bois."],
 "ugni blanc": ["Ugni blanc", "Le cépage blanc acide, peu alcoolisé (trebbiano), à l’origine de la plupart des cognacs et armagnacs — un piètre vin de table, mais une base idéale pour la distillation."],
 "vsop": ["Les comptes d’âge", "Les eaux-de-vie de raisin sont classées selon l’eau-de-vie la plus jeune de l’assemblage : <b>VS</b> (≥ 2 ans), <b>VSOP</b> (≥ 4 ans), <b>Napoléon</b>, <b>XO</b> (≥ 10 ans), <b>Hors d’âge</b>."],
 "blanche armagnac": ["Blanche d’Armagnac", "Un armagnac non vieilli, limpide comme l’eau, qui ne repose qu’en verre ou en inox — le fruit pur de l’eau-de-vie, avant tout passage sous bois."],
 "marc": ["Marc — <i>pomace brandy</i>", "Une eau-de-vie distillée à partir du <i>marc</i> : les pellicules, pépins et rafles qui restent après le pressurage. Le marc de Bourgogne et le marc de Champagne sont célèbres ; la grappa italienne repose sur la même idée."],
}


def step(t, en_name, sub, n, ic, html, why, opt=False):
    d = {'t': t, 'fr': en_name, 'sub': sub, 'ph': f'Étape {n}', 'ic': ic, 'html': html, 'why': WHY + why}
    if opt:
        d['opt'] = True
    return d


S_FR = {
 'cognac': {'label': 'Cognac', 'cls': 'cognac', 'steps': [
  step('Vendange', 'Harvest', 'Ugni blanc, cueilli pour l’acidité', 1, 'grape',
       f'<p>Le cognac commence par un vin blanc acide et léger — presque toujours d’{G("ugni blanc", "ugni blanc")}, cueilli quand l’acidité est élevée et le sucre bas. Les meilleurs viennent des crus crayeux autour de la {G("grande champagne", "Grande Champagne")}.</p>',
       'un vin vif et peu alcoolisé est une piètre boisson mais la matière idéale pour l’eau-de-vie — assez net et neutre pour se révéler à la distillation.'),
  step('Fermentation', 'Fermentation', 'Un vin de base léger — sans soufre', 2, 'ferment',
       '<p>Le jus fermente en un vin de base d’environ 9 % vol. On n’ajoute <b>pas de soufre</b> — il passerait dans l’eau-de-vie — et le vin est distillé peu après, souvent encore sur ses lies.</p>',
       'tout ce que contient le vin se retrouve concentré dans l’alambic : la pureté est ici essentielle.'),
  step('Première chauffe', 'First Distillation', '→ le brouillis, trouble', 3, 'potstill',
       f'<p>Dans l’{G("alambic charentais", "alambic charentais")} en cuivre, le vin est chauffé une première fois — la {G("première chauffe", "première chauffe")} — ce qui donne une eau-de-vie trouble et peu alcoolisée, le {G("brouillis", "brouillis")} (environ 28–32 %).</p>',
       'la signature du cognac, c’est d’être distillé <b>deux fois</b> — voici le premier des deux passages.'),
  step('Bonne chauffe', 'Second Distillation', 'La coupe → le cœur', 4, 'potstill',
       f'<p>Le brouillis est distillé à nouveau — c’est la {G("bonne chauffe", "bonne chauffe")}. Le distillateur fait alors {G("the cut", "la coupe")} : il écarte les têtes et les queues, agressives, et ne garde que le {G("cœur", "cœur")}, net, à environ 70 % vol.</p>',
       'l’art de la coupe décide de la qualité de toute l’eau-de-vie — en garder trop, et elle devient grossière.'),
  step('Vieillissement', 'Oak Ageing', 'Chêne du Limousin et de Tronçais', 5, 'barrel',
       f'<p>L’eau-de-vie, incolore, vieillit en chêne français (Limousin, Tronçais), qui lui donne couleur, épices et rondeur. Chaque année, un peu s’évapore — la {G(AS, "part des anges")}. L’âge détermine les comptes, du {G("vsop", "VSOP")} jusqu’au XO.</p>',
       'une eau-de-vie incolore et brûlante ne devient un cognac ambré et moelleux qu’après des années sous bois.'),
  step('Assemblage & réduction', 'Blending & Reduction', 'Au style de la maison, ~40 %', 6, 'blend',
       f'<p>Le maître de chai marie de nombreuses eaux-de-vie d’âges et de crus différents — l’{G("assemblage", "assemblage")} — puis ramène le degré à environ 40 % par {G("reduction", "réduction")}.</p>',
       'presque tout le cognac est un assemblage ; la constance et la complexité se construisent ici.'),
  step('Mise en bouteille', 'Bottling', 'Prêt à servir', 7, 'spiritglass',
       '<p>Le cognac terminé est mis en bouteille — il ne vieillit plus une fois sorti du fût et passé en verre.</p>',
       'contrairement au vin, l’âge d’une eau-de-vie est fixé le jour où elle quitte le fût.'),
 ]},
 'armagnac': {'label': 'Armagnac', 'cls': 'armagnac', 'steps': [
  step('Vendange', 'Harvest', 'Quatre cépages blancs de Gascogne', 1, 'grape',
       f'<p>La plus ancienne eau-de-vie de France, née en Gascogne. Le vin est fait d’{G("ugni blanc", "ugni blanc")}, avec du baco, de la folle blanche et du colombard — un mélange plus aromatique que celui du cognac.</p>',
       'l’encépagement, surtout le baco, donne à l’armagnac son caractère rustique et plus ample.'),
  step('Fermentation', 'Fermentation', 'Un vin de base, sans soufre', 2, 'ferment',
       '<p>Comme pour le cognac, un vin de base peu alcoolisé fermente sans soufre, prêt pour l’alambic.</p>',
       'un vin de base net garde l’eau-de-vie fidèle à son fruit.'),
  step('Distillation continue', 'Continuous Distillation', 'Un seul passage — alambic à colonne', 3, 'columnstill',
       f'<p>Voici la grande différence avec le cognac : l’armagnac est le plus souvent distillé <b>une seule fois</b>, dans un {G("alambic armagnaçais", "alambic armagnaçais")} à colonne, continu. Il sort à un degré plus bas (52–60 %), et garde plus d’arômes et de corps.</p>',
       'une seule distillation, à bas degré, explique pourquoi l’armagnac est plus riche et plus rustique que le cognac, distillé deux fois.'),
  step('Vieillissement', 'Oak Ageing', 'Chêne noir de Gascogne — millésimes fréquents', 4, 'barrel',
       f'<p>Élevé en chêne noir local, l’armagnac évolue avec sa propre {G(AS, "part des anges")}. Les millésimes sont une fierté de la région — tandis que la {G("blanche armagnac", "blanche d’Armagnac")}, limpide et non vieillie, est mise en bouteille jeune.</p>',
       'le goût de l’armagnac pour les millésimes permet de boire une eau-de-vie de l’année exacte d’une naissance ou d’un anniversaire.'),
  step('Assemblage ou millésime, & réduction', 'Blending or Vintage, & Reduction', 'Ou une seule année', 5, 'blend',
       f'<p>L’eau-de-vie est soit assemblée ({G("assemblage", "assemblage")}) selon le style de la maison et un compte d’âge, soit gardée en millésime — puis réduite vers le degré de mise en bouteille.</p>',
       'assemblage ou millésime, c’est ici que se fixent le caractère final et la mention d’âge.'),
  step('Mise en bouteille', 'Bottling', 'Prêt à servir', 6, 'spiritglass',
       '<p>Mis en bouteille et prêt — de la blanche limpide au vieil hors d’âge, profond.</p>',
       'l’armagnac offre une palette exceptionnellement large, du blanc au fruit brut à l’ambre de plusieurs décennies.'),
 ]},
 'marc': {'label': 'Marc & eau-de-vie', 'cls': 'marc', 'steps': [
  step('La matière première', 'The Raw Material', 'Du marc, ou le fruit entier', 1, 'pomace',
       f'<p>Deux eaux-de-vie économes partagent une même idée : distiller ce qui reste, ou ce qui est mûr. Le {G("marc", "marc")} se fait avec le <b>marc</b> (pellicules, pépins et rafles) qui reste après le pressurage. Une {G("eau-de-vie", "eau-de-vie")} de fruit part au contraire du fruit entier bien mûr — poire, cerise (kirsch), prune (mirabelle, quetsche) ou framboise.</p>',
       'le marc transforme un sous-produit du vin en trésor ; les eaux-de-vie de fruits enferment tout un verger dans un verre.'),
  step('Fermentation', 'Fermentation', 'Du marc ou des fruits écrasés', 2, 'ferment',
       '<p>Le marc (avec ses sucres résiduels) ou les fruits écrasés fermentent en un moût alcoolisé — la matière que l’alambic va concentrer.</p>',
       'seul le sucre transformé en alcool peut être distillé — il faut des fruits sains et mûrs.'),
  step('Distillation', 'Distillation', 'Alambic à repasse ou à colonne', 3, 'potstill',
       f'<p>Le moût est distillé — en alambic à repasse ou à colonne — et le distillateur fait {G("the cut", "la coupe")}, en ne gardant que le cœur, net, du distillat.</p>',
       'les eaux-de-vie de fruits, surtout, exigent une coupe soignée pour rester pures et aromatiques.'),
  step('Vieillissement', 'Ageing', 'Facultatif', 4, 'barrel',
       f'<p>Le {G("marc", "marc")} de raisin est souvent élevé en chêne (marc de Bourgogne, de Champagne, de gewurztraminer) et devient ambré et moelleux. La plupart des eaux-de-vie de <b>fruits</b> ne sont <b>pas</b> vieillies en bois : elles reposent en verre ou en inox pour rester limpides et garder leur fruit frais.</p>',
       'le bois masquerait le fruit délicat d’un kirsch ou d’une poire — c’est pourquoi ils restent limpides, volontairement.', opt=True),
  step('Mise en bouteille', 'Bottling', 'Limpide ou ambrée', 5, 'spiritglass',
       '<p>Mises en bouteille vers 40–45 % — les eaux-de-vie de fruits limpides servies glacées, les marcs vieillis dégustés lentement, comme un cognac.</p>',
       'la température de service et le verre révèlent le meilleur de chaque style.'),
 ]},
}

PROSE = {
 'cognac': ('Cognac — la finesse de la double distillation',
  f'''
        <p>Le cognac est <b>distillé deux fois</b> dans un {G("alambic charentais", "alambic charentais")} en cuivre. Un vin léger d’{G("ugni blanc", "ugni blanc")} devient le {G("brouillis", "brouillis")}, trouble, puis la {G("bonne chauffe", "bonne chauffe")} donne le {G("cœur", "cœur")}, pur. Des années en chêne du Limousin — en perdant chaque année une {G(AS, "part des anges")} — puis un dernier {G("assemblage", "assemblage")} et une {G("reduction", "réduction")} font l’eau-de-vie ambrée et moelleuse, classée du VS au XO.</p>
      '''),
 'armagnac': ('Armagnac — la plus ancienne eau-de-vie de France',
  f'''
        <p>L’armagnac est le plus souvent distillé <b>une seule fois</b>, dans un {G("alambic armagnaçais", "alambic armagnaçais")} continu. Une distillation à plus bas degré garde davantage d’arômes : l’armagnac est plus riche et plus rustique que le cognac. Vieilli en chêne noir de Gascogne, il est fièrement vendu en millésimes — et en {G("blanche armagnac", "blanche d’Armagnac")}, limpide et non vieillie.</p>
      '''),
 'marc': ('Marc & eau-de-vie — du marc et des fruits',
  f'''
        <p>Le {G("marc", "marc")} distille le marc qui reste après le pressurage (la grappa italienne repose sur la même idée), tandis qu’une {G("eau-de-vie", "eau-de-vie")} de fruit distille des fruits fermentés — poire, cerise (kirsch), prune. Les marcs de raisin sont souvent élevés sous bois ; les eaux-de-vie de fruits restent en général limpides pour garder la fraîcheur du verger.</p>
      '''),
}


def main():
    s = PAGE.read_text()
    if 'S_FR' in s:
        raise SystemExit('already bilingual')
    m = __import__('re').search(r'<title>(.*?)</title>', s)
    s = sub1(s, m.group(0), f'<title data-fr="Comment se fait l’eau-de-vie" data-en="{m.group(1)}">Comment se fait l’eau-de-vie</title>', 'title')
    s = bilingual(s, '<h1>', 'How Brandy Is Made', '</h1>', 'Comment se fait l’eau-de-vie', 'h1')
    p_en = ('From wine — and pomace, and ripe fruit — to spirit: how France distils its great brandies.\n     Tap any step to open the details, '
            'hover the <span class="gdemo">underlined terms</span> for a quick definition.')
    s = bilingual(s, '<p>', p_en, '</p>',
                  'Du vin — et du marc, et des fruits mûrs — à l’eau-de-vie : comment la France distille ses grandes eaux-de-vie. '
                  'Touchez une étape pour en lire le détail, survolez les <span class="gdemo">termes soulignés</span> pour une définition rapide.', 'header p')
    s = bilingual(s, '<div class="tab" data-k="marc">', 'Marc &amp; Eau-de-Vie', '</div>', 'Marc &amp; eau-de-vie', 'tab marc')
    s = bilingual(s, '<div class="hint">',
                  'Showing <b>Cognac</b> and <b>Armagnac</b> side-by-side &mdash; the two great grape brandies. Switch on <b>Marc &amp; Eau-de-Vie</b> to see the pomace and fruit spirits.',
                  '</div>',
                  'Affichage : <b>Cognac</b> et <b>Armagnac</b> côte à côte — les deux grandes eaux-de-vie de vin. Activez <b>Marc &amp; eau-de-vie</b> pour voir les eaux-de-vie de marc et de fruits.', 'hint')
    s = bilingual(s, '<div class="empty" id="empty">',
                  'Select a step in the flow to read what happens, why it matters,<br>and its French name.', '</div>',
                  'Choisissez une étape pour lire ce qui s’y passe, pourquoi c’est important,<br>et son nom en anglais.', 'empty')
    s = bilingual(s, '<h2>', 'The great French brandies', '</h2>', 'Les grandes eaux-de-vie françaises', 'prose h2')
    for cls, (sum_fr, body_fr) in PROSE.items():
        s = details(s, cls, sum_fr, body_fr, 'details ' + cls)
    s = bilingual(s, '<h2>', 'Glossary', '</h2>', 'Glossaire', 'glossary h2')
    s = bilingual(s, '<footer>',
                  '\n    Interactive guide to French brandy &amp; eau-de-vie &middot; A Quick Glance at French Wine &middot; Chris Paul.<br>\n    Works fully offline &mdash; a single self-contained file.\n  ',
                  '</footer>',
                  '\n    Guide interactif des eaux-de-vie françaises · A Quick Glance at French Wine · Christophe A. Paul.<br>\n    Fonctionne entièrement hors ligne — un seul fichier autonome.\n  ', 'footer')
    # script
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
