"""Adds the « Le tire-bouchon » section (#tire-bouchon) to Infos/Bottle_Sizes.html, after the tastevin (2026-10-18).
The page is hand-written: this script inserts / replaces the block between <!--cs:start--> and <!--cs:end-->,
plus a jump-nav chip and a few CSS rules (<!--cs-css-->). Safe to rerun after editing the texts below.
Pictures: the user will supply them later -> Bottle_Sizes_img/corkscrew_<key>.webp (KEYS below); until a file
exists the card shows a dashed « photo à venir » frame; rerun this script once the pictures are in place.
"""
import html
import re
from pathlib import Path

PAGE = Path(__file__).resolve().parents[2] / 'Bottle_Sizes.html'


def A(s):           # attribute value: the site menu swaps innerHTML from data-fr / data-en
    return html.escape(s, quote=True)


def bi(tag, fr, en, cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c} data-fr="{A(fr)}" data-en="{A(en)}">{fr}</{tag}>'


def R(*n):
    return '<sup class="src">' + ','.join(f'<a href="#cs-src-{k}">{k}</a>' for k in n) + '</sup>'


SOURCES = [
    ('B. Scriber, « Seven twists in corkscrew history », <i>National Geographic</i>, 14 juillet 2015 (tire-balles des mousquets, catalogue de 1681, brevet Henshall de 1795, Wienke, double levier, Screwpull). <a class="u" href="https://www.nationalgeographic.com/culture/article/tools-seven-twists-in-corkscrew-history" target="_blank" rel="noopener">nationalgeographic.com</a>',
     'B. Scriber, “Seven twists in corkscrew history”, <i>National Geographic</i>, 14 July 2015 (musket gun worms, the 1681 catalogue, Henshall’s 1795 patent, Wienke, double lever, Screwpull). <a class="u" href="https://www.nationalgeographic.com/culture/article/tools-seven-twists-in-corkscrew-history" target="_blank" rel="noopener">nationalgeographic.com</a>'),
    ('Wikipédia (en), « Corkscrew » : tire-balles utilisé depuis au moins les années 1630, bouton Henshall, couteau de sommelier de Wienke (1882), double levier de W. Burton Baker (1880), brevet américain de D. Rosati (1930), bilame, Screwpull de H. Allen (1979, collection du MoMA), d’après l’<i>Oxford Companion to Wine</i>. <a class="u" href="https://en.wikipedia.org/wiki/Corkscrew" target="_blank" rel="noopener">en.wikipedia.org</a>',
     'Wikipedia, “Corkscrew”: gun worm used since at least the 1630s, the Henshall button, Wienke’s waiter’s friend (1882), W. Burton Baker’s double lever (1880), D. Rosati’s US patent (1930), twin-prong puller, H. Allen’s Screwpull (1979, MoMA collection), after the <i>Oxford Companion to Wine</i>. <a class="u" href="https://en.wikipedia.org/wiki/Corkscrew" target="_blank" rel="noopener">en.wikipedia.org</a>'),
    ('Académie française, <i>Dictionnaire</i>, 2<sup>e</sup> édition (1718), t. 2, p. 697, article « tire-bouchon ». <a class="u" href="https://www.dictionnaire-academie.fr/article/A2T0356" target="_blank" rel="noopener">dictionnaire-academie.fr</a>',
     'Académie française, <i>Dictionnaire</i>, 2nd edition (1718), vol. 2, p. 697, entry “tire-bouchon”. <a class="u" href="https://www.dictionnaire-academie.fr/article/A2T0356" target="_blank" rel="noopener">dictionnaire-academie.fr</a>'),
    ('C. F. A. Wienke (Rostock), « Lever-Corkscrew », brevet américain n° 283 731, 21 août 1883 (après le brevet allemand de 1882). <a class="u" href="https://patents.google.com/patent/US283731A/en" target="_blank" rel="noopener">Google Patents</a>',
     'C. F. A. Wienke (Rostock), “Lever-Corkscrew”, US Patent No. 283,731, 21 August 1883 (after the German patent of 1882). <a class="u" href="https://patents.google.com/patent/US283731A/en" target="_blank" rel="noopener">Google Patents</a>'),
    ('The Wine History Project of San Luis Obispo County, « Corkscrew development exhibit » (double levier A1 de James Heeley &amp; Sons, 1888). <a class="u" href="https://winehistoryproject.org/corkscrew-development-exhibit/" target="_blank" rel="noopener">winehistoryproject.org</a>',
     'The Wine History Project of San Luis Obispo County, “Corkscrew development exhibit” (James Heeley &amp; Sons A1 double lever, 1888). <a class="u" href="https://winehistoryproject.org/corkscrew-development-exhibit/" target="_blank" rel="noopener">winehistoryproject.org</a>'),
]

# (when FR, place FR, when EN, place EN, title FR, title EN, text FR, text EN)
TIMELINE = [
    ('≈ 1630', 'Armes à feu', '≈ 1630', 'Firearms', 'Le tire-balles', 'The gun worm',
     'Soldats et chasseurs retirent les charges ratées du canon des mousquets avec une petite spirale de métal au bout de la baguette, le « tire-balles ». Le tire-bouchon en descendrait sans doute.' + R(1, 2),
     'Soldiers and hunters pulled misfired charges out of musket barrels with a small metal spiral on the end of the ramrod, the “gun worm”. The corkscrew most likely descends from it.' + R(1, 2)),
    ('1681', 'Angleterre', '1681', 'England', 'Un « ver d’acier »', 'A “steel worm”',
     'Première mention écrite connue : le catalogue d’un musée anglais décrit un « ver d’acier » servant à tirer les bouchons des bouteilles (<i>a Steel Worme used for the drawing of Corks out of Bottles</i>).' + R(1),
     'The first known written mention: an English museum catalogue describes “a Steel Worme used for the drawing of Corks out of Bottles”.' + R(1)),
    ('1718', 'France', '1718', 'France', 'Le mot « tire-bouchon »', 'The word “tire-bouchon”',
     'Le <i>Dictionnaire de l’Académie</i> le définit : une « sorte de vis de fer ou d’acier, qui tient à un anneau » pour tirer les bouchons des bouteilles.' + R(3),
     'The Académie’s <i>Dictionnaire</i> defines the French word: “a kind of iron or steel screw attached to a ring” for pulling corks from bottles.' + R(3)),
    ('1795', 'Angleterre', '1795', 'England', 'Le premier brevet', 'The first patent',
     'Le révérend <b>Samuel Henshall</b> obtient le premier brevet de tire-bouchon. Sa trouvaille : un petit disque, le « bouton Henshall », entre la mèche et la poignée, qui empêche la vis de s’enfoncer trop loin dans le bouchon.' + R(1, 2),
     'The Reverend <b>Samuel Henshall</b> was granted the first corkscrew patent. His idea: a small disc, the “Henshall button”, between the worm and the handle, which stops the screw going too deep into the cork.' + R(1, 2)),
    ('1880 · 1888', 'Angleterre', '1880 · 1888', 'England', 'Le double levier', 'The double lever',
     'Premiers tire-bouchons à deux leviers : brevet de <b>William Burton Baker</b> en 1880, puis le célèbre « A1 » de <b>James Heeley &amp; Sons</b> en 1888. On abaisse les deux bras, et le bouchon monte.' + R(2, 5),
     'The first two-lever corkscrews: <b>William Burton Baker</b>’s patent in 1880, then the famous “A1” by <b>James Heeley &amp; Sons</b> in 1888. Push both arms down and the cork rises.' + R(2, 5)),
    ('1882', 'Rostock', '1882', 'Rostock', 'Le couteau de sommelier', 'The waiter’s friend',
     'L’Allemand <b>Carl Wienke</b> brevète un tire-bouchon pliant à levier qui prend appui sur le bord du goulot : c’est le « limonadier », l’outil de poche de tous les sommeliers.' + R(2, 4),
     'The German <b>Carl Wienke</b> patented a folding lever corkscrew that rests on the rim of the bottle neck: the “waiter’s friend”, every sommelier’s pocket tool.' + R(2, 4)),
    ('1930', 'États-Unis', '1930', 'United States', 'Le tire-bouchon à ailes', 'The winged corkscrew',
     'L’Italien <b>Domenico Rosati</b> obtient le premier brevet américain du tire-bouchon « à ailes » : deux bras à crémaillère qui se lèvent quand la mèche entre dans le bouchon.' + R(2),
     'The Italian <b>Domenico Rosati</b> was granted the first US patent for the “winged” corkscrew: two rack-and-pinion arms that rise as the worm goes into the cork.' + R(2)),
    ('1979', 'États-Unis', '1979', 'United States', 'Le Screwpull', 'The Screwpull',
     'L’Américain <b>Herbert Allen</b> invente le <b>Screwpull</b> (brevet accordé en 1981) : une mèche longue et fine, gainée de téflon, et une cage qui se pose sur le col ; on tourne toujours dans le même sens et le bouchon remonte tout seul. Il entre dans la collection du MoMA.' + R(1, 2),
     'The American <b>Herbert Allen</b> invented the <b>Screwpull</b> (patent granted in 1981): a long, thin, Teflon-coated worm and a frame that sits on the neck; you keep turning the same way and the cork climbs out by itself. It is in MoMA’s collection.' + R(1, 2)),
]

# (image key, name FR, name EN, kicker FR, kicker EN, text FR, text EN)
TYPES = [
    ('t', 'Le tire-bouchon en T', 'The T-handle corkscrew', 'Le plus simple', 'The simplest',
     'Une mèche et une poignée : on visse, puis on tire à la force du bras. C’est la forme décrite par l’Académie en 1718.' + R(3),
     'A worm and a handle: screw in, then pull by sheer strength. This is the form the Académie described in 1718.' + R(3)),
    ('henshall', 'Le tire-bouchon à bouton', 'The button corkscrew', 'Henshall, 1795', 'Henshall, 1795',
     'Le disque au-dessus de la mèche bute sur le bouchon : la vis ne s’enfonce pas plus loin, et ne traverse pas le liège.' + R(1, 2),
     'The disc above the worm stops against the cork: the screw goes no deeper, and does not pierce right through.' + R(1, 2)),
    ('limonadier', 'Le limonadier', 'The waiter’s friend', 'Couteau de sommelier', 'Sommelier’s knife',
     'Pliant, avec une petite lame pour la capsule et un levier qui prend appui sur le goulot. Léger et précis : l’outil des professionnels.' + R(2, 4),
     'Folding, with a small blade for the capsule and a lever that rests on the bottle neck. Light and precise: the professionals’ tool.' + R(2, 4)),
    ('ailes', 'Le tire-bouchon à ailes', 'The winged corkscrew', 'Double levier', 'Double lever',
     'En vissant, les deux bras se lèvent ; en les abaissant, on fait monter le bouchon. Pas besoin de force.' + R(2),
     'As you screw in, the two arms rise; pushing them down lifts the cork. No strength needed.' + R(2)),
    ('bilame', 'Le bilame', 'The twin-prong puller', 'Sans mèche', 'No worm',
     'Deux lames fines glissent de part et d’autre du bouchon, entre le liège et le verre ; on tourne et on tire. Le bouchon sort sans être percé et peut être remis.' + R(2),
     'Two thin blades slide down either side of the cork, between cork and glass; twist and pull. The cork comes out unpierced and can be put back.' + R(2)),
    ('screwpull', 'Le Screwpull et ses cousins', 'The Screwpull and lever pulls', 'Depuis 1979', 'Since 1979',
     'Une cage posée sur le col guide une longue mèche téflonée : le bouchon remonte sans effort. Ses descendants « à levier », plus encombrants et plus chers, sont encore plus rapides.' + R(1, 2),
     'A frame resting on the neck guides a long Teflon-coated worm: the cork climbs out effortlessly. Its “lever” descendants, bulkier and dearer, are faster still.' + R(1, 2)),
]

CSS = '''
  /* corkscrew section (cs) */
  .cs-gal{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:16px;}
  @media (max-width:860px){ .cs-gal{grid-template-columns:repeat(2,1fr);} }
  @media (max-width:520px){ .cs-gal{grid-template-columns:1fr;} }
  .cs-gal .tv-card .ph{position:relative;}
  .cs-gal .tv-card .ph .cs-soon{position:absolute;inset:6px 18%;border:1.5px dashed var(--hair-hi);border-radius:12px;display:flex;align-items:center;justify-content:center;
    font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);text-align:center;padding:8px;}
  .cs-gal .tv-card .ph img{position:relative;z-index:1;}
  .cs-gal .tv-card .ph img[hidden]{display:none;}
  .cs-gal .meta{font-size:10.5px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--gold);margin-top:2px;}
'''


def section():
    tl = ''.join(
        f'<li><div class="when" data-fr="{A(wf + "<small>" + pf + "</small>")}" data-en="{A(we + "<small>" + pe + "</small>")}">{wf}<small>{pf}</small></div>'
        f'<div class="what">{bi("h3", tf, te)}{bi("p", xf, xe)}</div></li>'
        for wf, pf, we, pe, tf, te, xf, xe in TIMELINE)
    cards = ''.join(
        f'<article class="panel tv-card"><div class="ph">'
        + (f'<img src="Bottle_Sizes_img/corkscrew_{k}.webp" alt="{A(nf)} / {A(ne)}" loading="lazy" draggable="false">'
           if (PAGE.parent / 'Bottle_Sizes_img' / f'corkscrew_{k}.webp').exists()
           else f'<span class="cs-soon" data-fr="{A("Photo à venir")}" data-en="{A("Photo coming soon")}">Photo à venir</span>') + '</div>'
        f'{bi("h3", nf, ne)}{bi("div", mf, me, "meta")}{bi("p", xf, xe)}</article>'
        for k, nf, ne, mf, me, xf, xe in TYPES)
    srcs = ''.join(f'<li id="cs-src-{i}" data-fr="{A(f)}" data-en="{A(e)}">{f}</li>' for i, (f, e) in enumerate(SOURCES, 1))
    intro_fr = ('Dès que le bouchon de liège entre à force dans le col des bouteilles, au XVII<sup>e</sup> siècle, il faut un outil pour l’en sortir. '
                'On le trouve du côté des armes : une petite spirale d’acier qu’on visse dans le liège.' + R(1, 2)
                + ' En trois siècles, cette vis s’est dotée de boutons, de leviers, d’ailes et de cages — mais le principe n’a pas changé.')
    intro_en = ('As soon as the cork was pushed tight into the bottle neck, in the 17th century, a tool was needed to get it out. '
                'It came from the world of firearms: a small steel spiral screwed into the cork.' + R(1, 2)
                + ' In three centuries the screw has gained buttons, levers, wings and frames — but the principle has not changed.')
    who_fr = ('Personne en particulier : l’outil dérive très probablement du tire-balles des armes à feu, et la première mention écrite, en 1681, n’a pas d’auteur connu. '
              'Le premier <b>brevet</b>, lui, a un nom : le révérend anglais <b>Samuel Henshall</b>, en 1795.' + R(1, 2))
    who_en = ('No one in particular: the tool most likely derives from the gun worm of firearms, and the first written mention, in 1681, has no known author. '
              'The first <b>patent</b>, however, has a name: the English Reverend <b>Samuel Henshall</b>, in 1795.' + R(1, 2))
    return f'''<!--cs:start-->
  <!-- ===== corkscrew (Infos/_source/corkscrew/add_section.py) ===== -->
  <section class="sec" id="tire-bouchon">
    <div class="sec-head"><div>
      {bi("h2", "Le <em>tire-bouchon</em>", "The <em>corkscrew</em>")}
      {bi("p", "D’un outil d’armurier à l’objet de poche du sommelier : une brève histoire, et les principaux modèles.", "From a gunsmith’s tool to the sommelier’s pocket: a short history, and the main kinds.")}
    </div></div>
    <div class="panel hist-intro">
      <div>{bi("p", intro_fr, intro_en)}</div>
      <div class="who">{bi("h3", "Qui a inventé le tire-bouchon&nbsp;?", "Who invented the corkscrew?")}{bi("p", who_fr, who_en)}</div>
    </div>
    <div class="panel"><ol class="tl">{tl}</ol></div>
    <div class="sec-head" style="margin-top:26px"><div>{bi("h2", "Quelques <em>modèles</em>", "A few <em>kinds</em>")}</div></div>
    <div class="cs-gal" id="tire-bouchon-modeles">{cards}</div>
    <div class="panel tv-box tv-sources" id="tire-bouchon-sources" style="margin-top:16px">
      {bi("h3", "Sources", "Sources")}
      <ol>{srcs}</ol>
    </div>
  </section>
<!--cs:end-->'''


def main():
    s = PAGE.read_text()
    block = section()
    if '<!--cs:start-->' in s:
        s = re.sub(r'<!--cs:start-->.*?<!--cs:end-->', lambda m: block, s, flags=re.S)
    else:
        anchor = '\n  <footer'
        i = s.index(anchor)
        s = s[:i] + '\n\n  ' + block + '\n' + s[i:]
    chip = '    <a href="#tire-bouchon" data-fr="Le tire-bouchon" data-en="The corkscrew">Le tire-bouchon</a>\n'
    if 'href="#tire-bouchon"' not in s.split('</nav>')[0]:
        k = s.index('    <a href="#tastevin"')
        k = s.index('\n', k) + 1
        s = s[:k] + chip + s[k:]
    if '<!--cs-css-->' not in s:
        k = s.index('</style>')
        s = s[:k] + '/*<!--cs-css-->*/' + CSS + s[k:]
    PAGE.write_text(s)
    print(f'{PAGE.name}: section #tire-bouchon written ({len(TIMELINE)} dates, {len(TYPES)} kinds, {len(SOURCES)} sources)')


if __name__ == '__main__':
    main()
