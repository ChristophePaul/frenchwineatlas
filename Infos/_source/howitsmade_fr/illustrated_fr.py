"""French version of « How wine is made - Illustrated.html » — 2026-10-19, user request.
Red / white / sweet / rosé steps, the glossary and the prose are word-for-word the interactive page's, so their
French comes from wine_fr.py; only the 9-step Brandy flow is translated here.
Run once from WEB Site/Infos:  python3 _source/howitsmade_fr/illustrated_fr.py
Backup of the English-only page: WEB Site/_backups/2026-10-19/How wine is made - Illustrated.html
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import js, sub1, bilingual, details, LANG_JS, LANG_INIT  # noqa: E402
import wine_fr  # noqa: E402

PAGE = Path(__file__).resolve().parents[2] / "How it's made" / 'How wine is made - Illustrated.html'
G, WHY, step = wine_fr.G, wine_fr.WHY, wine_fr.step

BRANDY_FR = {'label': 'Eaux-de-vie', 'cls': 'brandy', 'steps': [
 step('Vin, marc ou fruits', 'Base Wine & Raw Material', 'Vin · marc · fruits entiers', 1,
      f'<p>Une eau-de-vie se distille à partir de quelque chose de déjà fermenté. Le <b>cognac</b> et l’<b>armagnac</b> distillent un vin blanc léger et acide (surtout de l’ugni blanc) ; une <i>fine</i> ou un {G("marc", "marc")} distille le marc de raisin pressé ; et les <i>eaux-de-vie</i> de fruits distillent des fruits entiers fermentés — prune, poire, cerise, framboise.</p>',
      'un alambic concentre tout ce qu’on lui donne, défauts compris — la base doit donc être nette, peu alcoolisée, peu soufrée et bien acide.'),
 step('Première chauffe', 'First Distillation', 'Vin → brouillis (~28 %)', 2,
      '<p>Dans l’<i>alambic charentais</i> en cuivre, le vin est chauffé à la flamme. Les vapeurs d’alcool montent par le <i>chapiteau</i> et le <i>col de cygne</i>, puis se condensent dans le serpentin : on obtient une eau-de-vie trouble et peu alcoolisée — le <i>brouillis</i>, autour de 28 % vol.</p>',
      'ce premier passage sépare grossièrement l’alcool de l’eau et prépare la seconde distillation, décisive.'),
 step('Bonne chauffe', 'Second Distillation', 'Couper le cœur (~70 %)', 3,
      '<p>Le brouillis est redistillé. Le distillateur fait la <b>coupe</b> : les <i>têtes</i> et les <i>secondes / queues</i> sont mises de côté, et seul le <i>cœur</i> est gardé — une eau-de-vie nette à environ 70 % vol.</p>',
      'seul le cœur porte des arômes purs et fins ; les têtes et les queues contiennent des composés volatils agressifs qui gâteraient l’eau-de-vie.'),
 step('L’alambic charentais', 'The Charentais Still', 'L’alambic à repasse du Cognac, en cuivre', 4,
      '<p>Le cognac se fait dans l’<i>alambic charentais</i> : un alambic en cuivre, avec son <i>chapiteau</i> en forme d’oignon, son col de cygne et son serpentin. La loi impose que le cognac y soit distillé <b>deux fois</b>, par charges, et que la distillation soit achevée au 31 mars qui suit la vendange.</p>',
      'le cuivre, la forme de l’alambic et la double distillation donnent au cognac sa finesse.'),
 step('L’alambic armagnaçais', 'The Armagnac Still', 'Un alambic continu, à colonne', 5,
      '<p>L’armagnac, en Gascogne, utilise traditionnellement son propre <i>alambic armagnaçais</i> — un alambic <b>continu</b>, à colonne. Le vin entre par le haut et rencontre les vapeurs qui montent à travers une série de plateaux : il se distille en <b>un seul passage</b>, à un degré plus bas (~52–72 % vol.).</p>',
      'une seule distillation, à plus bas degré, laisse plus d’arômes dans l’eau-de-vie — l’armagnac est en général plus riche et plus rustique que le cognac.'),
 step('Eaux-de-vie de fruits', 'Fruit Eaux-de-Vie', 'Un alcool pur, issu du fruit entier', 6,
      '<p>Au-delà du raisin, la France distille des <i>eaux-de-vie</i> de fruits entiers fermentés dans de petits alambics — mirabelle et quetsche, poire williams, kirsch (cerise), framboise. Elles ne sont en général <b>pas vieillies</b> et sont mises en bouteille limpides, pour saisir le fruit pur.</p>',
      'sans bois pour masquer quoi que ce soit, une eau-de-vie est un portrait nu du fruit — et il faut des kilos de fruits pour une seule bouteille.'),
 step('Élevage en fût de chêne', 'Oak Ageing', 'Des années en chêne français', 7,
      '<p>Les eaux-de-vie de raisin vieillissent des années — souvent des décennies — en chêne français (Limousin, Tronçais). L’eau-de-vie, incolore, prend peu à peu couleur, arômes et rondeur, tandis que 1 à 3 % s’évaporent chaque année : la <i>part des anges</i>.</p>',
      'le chêne et une lente oxydation transforment une eau-de-vie brûlante en un alcool ambré et moelleux ; les comptes d’âge (VS, VSOP, XO) se basent sur l’eau-de-vie la plus jeune de l’assemblage.'),
 step('Assemblage & réduction', 'Blending & Reduction', 'L’art du maître de chai', 8,
      '<p>Le <i>maître de chai</i> marie des eaux-de-vie de crus, d’âges et de fûts différents pour créer un style de maison constant, puis <b>réduit</b> doucement le degré vers 40 % vol. en ajoutant des <i>petites eaux</i> (eau distillée) par petites étapes, sur des semaines ou des mois.</p>',
      'l’assemblage assure la constance d’une année sur l’autre ; une réduction lente évite de brusquer l’eau-de-vie et la garde harmonieuse.'),
 step('Mise en bouteille', 'Bottling', 'Filtrée, remplie, scellée', 9,
      '<p>L’eau-de-vie reçoit une dernière filtration légère, puis elle est mise en bouteille, bouchée, capsulée et étiquetée avec sa mention de qualité (VS, VSOP, XO — ou un <i>millésime</i> pour l’armagnac).</p>',
      'contrairement au vin, une eau-de-vie n’évolue plus une fois en bouteille — ce qui quitte le chai est exactement ce qui arrive dans le verre.'),
]}


def main():
    s = PAGE.read_text()
    if 'S_FR' in s:
        raise SystemExit('already bilingual')
    S_FR = dict(wine_fr.S_FR)
    S_FR['brandy'] = BRANDY_FR
    s = sub1(s, '<title>How Wine Is Made — Illustrated</title>',
             '<title data-fr="Comment se fait le vin — illustré" data-en="How Wine Is Made — Illustrated">Comment se fait le vin — illustré</title>', 'title')
    s = bilingual(s, '<h1>', 'How Wine Is Made', '</h1>', 'Comment se fait le vin', 'h1')
    p_en = ('From vine to bottle — the winemaker\'s road for each style of wine.\n     Tap any step to open the details, '
            'hover the <span class="gdemo">underlined terms</span> for a quick definition.')
    s = bilingual(s, '<p>', p_en, '</p>',
                  'De la vigne à la bouteille : le chemin du vigneron pour chaque style de vin. Touchez une étape pour en lire le détail, '
                  'survolez les <span class="gdemo">termes soulignés</span> pour une définition rapide.', 'header p')
    for k, en, fr in [('red', 'Red', 'Rouge'), ('white', 'White', 'Blanc'), ('sweet', 'Sweet &amp; Late-Harvest', 'Liquoreux &amp; tardifs'),
                      ('rose', 'Rosé', 'Rosé'), ('brandy', 'Brandy', 'Eaux-de-vie')]:
        s = bilingual(s, f'<div class="tab" data-k="{k}">', en, '</div>', fr, 'tab ' + k)
    s = bilingual(s, '<div class="hint">',
                  'Showing: click <b>Red</b> and <b>White</b> together for the classic side-by-side, or switch to Sweet / Rosé.', '</div>',
                  'Affichage : sélectionnez <b>Rouge</b> et <b>Blanc</b> ensemble pour la comparaison classique, ou passez aux liquoreux, au rosé ou aux eaux-de-vie.', 'hint')
    s = bilingual(s, '<div class="empty" id="empty">',
                  'Select a step in the flow to read what happens, why it matters,<br>and its French name.', '</div>',
                  'Choisissez une étape pour lire ce qui s’y passe, pourquoi c’est important,<br>et son nom en anglais.', 'empty')
    s = bilingual(s, '<figcaption>', 'Harvesting — <i>Vendange</i>', '</figcaption>', 'Vendange — <i>Harvesting</i>', 'figcaption')
    s = bilingual(s, '<h2>', 'In the winemaker\'s words', '</h2>', 'Les mots du vigneron', 'prose h2')
    for cls, (sum_fr, body_fr) in wine_fr.PROSE.items():
        s = details(s, cls, sum_fr, body_fr, 'details ' + cls)
    s = bilingual(s, '<h2>', 'Glossary', '</h2>', 'Glossaire', 'glossary h2')
    s = bilingual(s, '<footer>',
                  '\n    Interactive edition of <i>“How Wine Is Made”</i> · A Quick Glance at French Wine · Chris Paul.<br>\n    Works fully offline — a single self-contained file.\n  ',
                  '</footer>',
                  '\n    Édition interactive de <i>« Comment se fait le vin »</i> · A Quick Glance at French Wine · Christophe A. Paul.<br>\n    Fonctionne entièrement hors ligne — un seul fichier autonome.\n  ', 'footer')
    # script
    s = sub1(s, '/* ---------- RENDER ---------- */',
             '/* ---------- FRENCH DATA (2026-10-19) — same keys; `fr` holds the English name in this set ---------- */\n'
             f'const GLOSS_FR = {js(wine_fr.GLOSS_FR)};\nconst S_FR = {js(S_FR)};\n{LANG_JS}\n/* ---------- RENDER ---------- */', 'render marker')
    s = sub1(s, '  const d = S[key];', '  const d = SS()[key];', 'buildFlow S')
    # icons are picked from the ENGLISH step title, whatever the language shown
    s = sub1(s, "n.innerHTML='<div class=\"icon\">'+iconFor(st.t)+'</div>'", "n.innerHTML='<div class=\"icon\">'+iconFor(S[key].steps[i].t)+'</div>'", 'node icon')
    s = sub1(s, "'<div class=\"hero\" style=\"color:'+col+'\">'+iconFor(st.t)+'</div>'", "'<div class=\"hero\" style=\"color:'+col+'\">'+iconFor(S[key].steps[i].t)+'</div>'", 'hero icon')
    s = sub1(s, "(st.opt?' <span class=\"badge\">optional</span>':'')", "(st.opt?' <span class=\"badge\">'+UI('optional')+'</span>':'')", 'badge')
    s = sub1(s, '  const st=S[key].steps[i];\n  emptyEl', '  const st=SS()[key].steps[i];\n  emptyEl', 'select S')
    s = sub1(s, "'<div><div class=\"ph\">'+S[key].label+' · '+st.ph+(st.opt?' · optional':'')+'</div>'",
             "'<div><div class=\"ph\">'+SS()[key].label+' · '+st.ph+(st.opt?' · '+UI('optional'):'')+'</div>'", 'ph')
    s = sub1(s, '      const st=S[key].steps[i];\n      thumb.src', '      const st=SS()[key].steps[i];\n      thumb.src', 'hover pic S')
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
    s = sub1(s, old_l, old_l.replace("  const key=", "  const G=GG();\n  const key=").replace('GLOSS', 'G'), 'lookup')
    s = sub1(s, 'const g=lookup(el.textContent);', 'const g=lookup(el.dataset.g||el.textContent);', 'wire lookup')
    s = sub1(s, "document.getElementById('deco2').innerHTML=ICONS.grape;\nrenderTabs(); renderFlows();",
             "document.getElementById('deco2').innerHTML=ICONS.grape;\nrenderTabs(); renderFlows();\n" + LANG_INIT, 'init')
    PAGE.write_text(s)
    print(PAGE.name, 'now bilingual:', sum(len(v['steps']) for v in S_FR.values()), 'steps')


if __name__ == '__main__':
    main()
