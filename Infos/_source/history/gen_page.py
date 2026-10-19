"""Builds Infos/History/History_of_Wine.html — « Histoire du vin » / "A history of wine".

Facts only, each one tied to a numbered source (superscripts; assets/ref_tips.js shows the source on mouse-over).
Figures that are estimates or ranges carry « ≈ ». Bilingual FR/EN like the other Infos pages.
Shared look = Vine & Vineyard base.css.
Run:  python3 gen_page.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
INFOS = HERE.parent.parent
sys.path.insert(0, str(INFOS / 'Vine_and_Vineyard' / '_source'))
from common import base_css, t, blk, att  # noqa: E402

OUT = INFOS / 'History' / 'History_of_Wine.html'


def L(url, label='lien'):
    return f' <a href="{url}" target="_blank" rel="noopener">{label}</a>'


def doi(d):
    return L('https://doi.org/' + d, 'doi')


# ------------------------------------------------------------------ sources (key, FR, EN)
SOURCES = [
    ('dong', 'Dong Y. <i>et al.</i> (2023). Dual domestications and origin of traits in grapevine evolution. <i>Science</i> 379 : 892–901.' + doi('10.1126/science.add8655'),
             'Dong Y. <i>et al.</i> (2023). Dual domestications and origin of traits in grapevine evolution. <i>Science</i> 379: 892–901.' + doi('10.1126/science.add8655')),
    ('jiahu', 'McGovern P.E. <i>et al.</i> (2004). Fermented beverages of pre- and proto-historic China. <i>PNAS</i> 101(51) : 17593–17598 (site de Jiahu, Henan).' + doi('10.1073/pnas.0407921102'),
              'McGovern P.E. <i>et al.</i> (2004). Fermented beverages of pre- and proto-historic China. <i>PNAS</i> 101(51): 17593–17598 (Jiahu site, Henan).' + doi('10.1073/pnas.0407921102')),
    ('georgia', 'McGovern P.E. <i>et al.</i> (2017). Early Neolithic wine of Georgia in the South Caucasus. <i>PNAS</i> 114(48) : E10309–E10318 (Gadachrili Gora, Shulaveris Gora).' + doi('10.1073/pnas.1714728114'),
                'McGovern P.E. <i>et al.</i> (2017). Early Neolithic wine of Georgia in the South Caucasus. <i>PNAS</i> 114(48): E10309–E10318 (Gadachrili Gora, Shulaveris Gora).' + doi('10.1073/pnas.1714728114')),
    ('iran', 'McGovern P.E., Glusker D.L., Exner L.J., Voigt M.M. (1996). Neolithic resinated wine. <i>Nature</i> 381 : 480–481 (Hajji Firuz Tepe, Iran).' + doi('10.1038/381480a0'),
             'McGovern P.E., Glusker D.L., Exner L.J., Voigt M.M. (1996). Neolithic resinated wine. <i>Nature</i> 381: 480–481 (Hajji Firuz Tepe, Iran).' + doi('10.1038/381480a0')),
    ('areni', 'Barnard H. <i>et al.</i> (2011). Chemical evidence for wine production around 4000 BCE in the Late Chalcolithic Near Eastern highlands. <i>Journal of Archaeological Science</i> 38(5) : 977–984 (grotte d’Areni-1, Arménie).' + doi('10.1016/j.jas.2010.11.012'),
              'Barnard H. <i>et al.</i> (2011). Chemical evidence for wine production around 4000 BCE in the Late Chalcolithic Near Eastern highlands. <i>Journal of Archaeological Science</i> 38(5): 977–984 (Areni-1 cave, Armenia).' + doi('10.1016/j.jas.2010.11.012')),
    ('unesco', 'UNESCO, Patrimoine culturel immatériel (2013) : « Méthode ancestrale de vinification traditionnelle géorgienne en qvevri ».' + L('https://ich.unesco.org/fr/RL/methode-ancestrale-de-vinification-traditionnelle-georgienne-en-qvevri-00870', 'ich.unesco.org'),
               'UNESCO, Intangible Cultural Heritage (2013): “Ancient Georgian traditional Qvevri wine-making method”.' + L('https://ich.unesco.org/en/RL/ancient-georgian-traditional-qvevri-wine-making-method-00870', 'ich.unesco.org')),
    ('egypt', 'McGovern P.E. <i>et al.</i> (2009). Ancient Egyptian herbal wines. <i>PNAS</i> 106(18) : 7361–7366 (tombe U-j de Scorpion I<sup>er</sup>, Abydos).' + doi('10.1073/pnas.0811578106'),
              'McGovern P.E. <i>et al.</i> (2009). Ancient Egyptian herbal wines. <i>PNAS</i> 106(18): 7361–7366 (tomb U-j of Scorpion I, Abydos).' + doi('10.1073/pnas.0811578106')),
    ('cerny', 'Černý J. (1965). <i>Hieratic Inscriptions from the Tomb of Tut‘ankhamūn</i>. Oxford, Griffith Institute (étiquettes des jarres de vin : année, domaine, chef vigneron).',
              'Černý J. (1965). <i>Hieratic Inscriptions from the Tomb of Tut‘ankhamūn</i>. Oxford, Griffith Institute (wine-jar labels: year, estate, chief vintner).'),
    ('mcgovern_book', 'McGovern P.E. (2003, rééd. 2019). <i>Ancient Wine: The Search for the Origins of Viniculture</i>. Princeton University Press.',
                      'McGovern P.E. (2003, new ed. 2019). <i>Ancient Wine: The Search for the Origins of Viniculture</i>. Princeton University Press.'),
    ('marseille', 'Encyclopædia Britannica, « Marseille » (fondée vers 600 av. J.-C. par des Grecs de Phocée).' + L('https://www.britannica.com/place/Marseille', 'britannica.com'),
                  'Encyclopædia Britannica, “Marseille” (founded c. 600 BC by Greeks from Phocaea).' + L('https://www.britannica.com/place/Marseille', 'britannica.com')),
    ('lattes', 'McGovern P.E. <i>et al.</i> (2013). Beginning of viniculture in France. <i>PNAS</i> 110(25) : 10147–10152 (Lattara / Lattes, Hérault).' + doi('10.1073/pnas.1216126110'),
               'McGovern P.E. <i>et al.</i> (2013). Beginning of viniculture in France. <i>PNAS</i> 110(25): 10147–10152 (Lattara / Lattes, Hérault).' + doi('10.1073/pnas.1216126110')),
    ('oxford', 'Robinson J., Harding J. (dir.) (2015). <i>The Oxford Companion to Wine</i>, 4<sup>e</sup> éd. Oxford University Press (articles « Domitian », « Probus », « Monasteries », « Bordeaux », « Australia »…).',
               'Robinson J., Harding J. (eds) (2015). <i>The Oxford Companion to Wine</i>, 4th ed. Oxford University Press (entries “Domitian”, “Probus”, “Monasteries”, “Bordeaux”, “Australia”…).'),
    ('dion', 'Dion R. (1959). <i>Histoire de la vigne et du vin en France des origines au XIX<sup>e</sup> siècle</i>. Paris (rééd. CNRS Éditions, 2010).',
             'Dion R. (1959). <i>Histoire de la vigne et du vin en France des origines au XIX<sup>e</sup> siècle</i>. Paris (repr. CNRS Éditions, 2010; in French).'),
    ('johnson', 'Johnson H. (1989). <i>The Story of Wine</i>. Mitchell Beazley — éd. fr. <i>Une histoire mondiale du vin</i>, Hachette, 1990.',
                'Johnson H. (1989). <i>The Story of Wine</i>. Mitchell Beazley (new ed. 2020, Academie du Vin Library).'),
    ('shiji', 'Sima Qian (v. 90 av. J.-C.). <i>Shiji</i> (Mémoires historiques), chap. 123, « Dayuan liezhuan » : le Ferghana fait du vin de raisin, les envoyés Han en rapportent les vignes.',
              'Sima Qian (c. 90 BC). <i>Shiji</i> (Records of the Grand Historian), ch. 123, “Account of Dayuan”: Ferghana makes grape wine; Han envoys bring vines back.'),
    ('laufer', 'Laufer B. (1919). <i>Sino-Iranica</i>. Field Museum of Natural History, Chicago (conteste le rôle personnel de Zhang Qian).',
               'Laufer B. (1919). <i>Sino-Iranica</i>. Field Museum of Natural History, Chicago (disputes Zhang Qian’s personal role).'),
    ('tang', '<i>Taiping yulan</i> (977–983), cité par l’article « Wine in China », Wikipédia (prise de Gaochang en 640, raisin « tétine de jument », méthode de vinification).' + L('https://en.wikipedia.org/wiki/Wine_in_China', 'wikipedia'),
             '<i>Taiping yulan</i> (977–983), quoted in “Wine in China”, Wikipedia (capture of Gaochang in 640, “mare’s nipple” grape, wine-making method).' + L('https://en.wikipedia.org/wiki/Wine_in_China', 'wikipedia')),
    ('changyu', 'Changyu Pioneer Wine Co., fondée en 1892 à Yantai par Zhang Bishi — article « Changyu », Wikipédia.' + L('https://en.wikipedia.org/wiki/Changyu', 'wikipedia'),
                'Changyu Pioneer Wine Co., founded in 1892 in Yantai by Zhang Bishi — “Changyu”, Wikipedia.' + L('https://en.wikipedia.org/wiki/Changyu', 'wikipedia')),
    ('oiv', 'OIV (2025). <i>State of the World Vine and Wine Sector in 2024</i> (surfaces viticoles par pays). Paris/Dijon.' + L('https://winemag.co.za/wp-content/uploads/2025/04/OIV-State-of-the-World-Vine-and-Wine-Sector-2024.pdf', 'pdf'),
            'OIV (2025). <i>State of the World Vine and Wine Sector in 2024</i> (vineyard area by country). Paris/Dijon.' + L('https://winemag.co.za/wp-content/uploads/2025/04/OIV-State-of-the-World-Vine-and-Wine-Sector-2024.pdf', 'pdf')),
    ('gamay', '« 31 July 1395: the banning of Gamay », <i>The Drinks Business</i> (ordonnance de Philippe le Hardi).' + L('https://www.thedrinksbusiness.com/2016/07/31-july-1395-the-banning-of-gamay/', 'thedrinksbusiness.com'),
              '“31 July 1395: the banning of Gamay”, <i>The Drinks Business</i> (Philip the Bold’s ordinance).' + L('https://www.thedrinksbusiness.com/2016/07/31-july-1395-the-banning-of-gamay/', 'thedrinksbusiness.com')),
    ('hospices', 'Hospices Civils de Beaune, <i>Dossier de présentation de l’Hôtel-Dieu de Beaune</i> (fondation en 1443 par Nicolas Rolin et Guigone de Salins).' + L('https://musee.hospices-de-beaune.com/sites/musee/files/2022-06/Dossier%20de%20pr%C3%A9sentation%20-%20H%C3%B4tel-Dieu%20de%20Beaune%20-%20Hospices%20Civils%20de%20Beaune_0.pdf', 'pdf'),
                 'Hospices Civils de Beaune, <i>Hôtel-Dieu de Beaune presentation file</i> (founded in 1443 by Nicolas Rolin and Guigone de Salins; in French).' + L('https://musee.hospices-de-beaune.com/sites/musee/files/2022-06/Dossier%20de%20pr%C3%A9sentation%20-%20H%C3%B4tel-Dieu%20de%20Beaune%20-%20Hospices%20Civils%20de%20Beaune_0.pdf', 'pdf')),
    ('sothebys', 'Sotheby’s, catalogue de la 161<sup>e</sup> vente des vins des Hospices de Beaune (domaine d’≈&nbsp;60&nbsp;ha, enchères publiques depuis 1859).' + L('https://www.sothebys.com/en/digital-catalogues/161e-vente-des-vins-des-hospices-de-beaune', 'sothebys.com'),
                 'Sotheby’s, catalogue of the 161st Hospices de Beaune wine sale (≈&nbsp;60&nbsp;ha estate, public auctions since 1859).' + L('https://www.sothebys.com/en/digital-catalogues/161e-vente-des-vins-des-hospices-de-beaune', 'sothebys.com')),
    ('tapia', 'Tapia A.M. <i>et al.</i> (2007). Determining the Spanish origin of representative ancient American grapevine varieties. <i>American Journal of Enology and Viticulture</i> 58(2) : 242–251 (Listán Prieto = Mission = País = Criolla chica).' + doi('10.5344/ajev.2007.58.2.242'),
              'Tapia A.M. <i>et al.</i> (2007). Determining the Spanish origin of representative ancient American grapevine varieties. <i>American Journal of Enology and Viticulture</i> 58(2): 242–251 (Listán Prieto = Mission = País = Criolla chica).' + doi('10.5344/ajev.2007.58.2.242')),
    ('cape', '« On this day 1659: the first wine in South Africa », <i>The Drinks Business</i> (journal de Jan van Riebeeck, 2 février 1659).' + L('https://www.thedrinksbusiness.com/2018/02/on-this-day-1659the-first-wine-in-south-africa/', 'thedrinksbusiness.com'),
             '“On this day 1659: the first wine in South Africa”, <i>The Drinks Business</i> (Jan van Riebeeck’s journal, 2 February 1659).' + L('https://www.thedrinksbusiness.com/2018/02/on-this-day-1659the-first-wine-in-south-africa/', 'thedrinksbusiness.com')),
    ('phyllo', 'INRAE, « 1887 : une mission viticole en Amérique pour sauver les vignobles français » ; Campbell C. (2004). <i>Phylloxera: How Wine Was Saved for the World</i>. HarperCollins.' + L('https://agate.inrae.fr/agate/en/content/1887a-viticultural-mission-america-save-french-vineyards', 'inrae.fr'),
               'INRAE, “1887: a viticultural mission to America to save French vineyards”; Campbell C. (2004). <i>Phylloxera: How Wine Was Saved for the World</i>. HarperCollins.' + L('https://agate.inrae.fr/agate/en/content/1887a-viticultural-mission-america-save-french-vineyards', 'inrae.fr')),
    ('inao', 'INAO, « 1935-1970 : l’avènement de l’INAO et la création des AOC » (décret-loi du 30 juillet 1935 ; premières AOC le 15 mai 1936).' + L('https://www.inao.gouv.fr/en/history-1935-1970', 'inao.gouv.fr'),
             'INAO, “1935-1970: the advent of INAO and the creation of AOCs” (decree-law of 30 July 1935; first AOCs on 15 May 1936).' + L('https://www.inao.gouv.fr/en/history-1935-1970', 'inao.gouv.fr')),
    ('wine_grapes', 'Robinson J., Harding J., Vouillamoz J. (2012). <i>Wine Grapes: A Complete Guide to 1,368 Vine Varieties</i>. Allen Lane / Ecco.',
                    'Robinson J., Harding J., Vouillamoz J. (2012). <i>Wine Grapes: A Complete Guide to 1,368 Vine Varieties</i>. Allen Lane / Ecco.'),
    ('bowers99', 'Bowers J. <i>et al.</i> (1999). Historical genetics: the parentage of Chardonnay, Gamay, and other wine grapes of northeastern France. <i>Science</i> 285 : 1562–1565.' + doi('10.1126/science.285.5433.1562'),
                 'Bowers J. <i>et al.</i> (1999). Historical genetics: the parentage of Chardonnay, Gamay, and other wine grapes of northeastern France. <i>Science</i> 285: 1562–1565.' + doi('10.1126/science.285.5433.1562')),
    ('bowers97', 'Bowers J.E., Meredith C.P. (1997). The parentage of a classic wine grape, Cabernet Sauvignon. <i>Nature Genetics</i> 16 : 84–87.' + doi('10.1038/ng0597-84'),
                 'Bowers J.E., Meredith C.P. (1997). The parentage of a classic wine grape, Cabernet Sauvignon. <i>Nature Genetics</i> 16: 84–87.' + doi('10.1038/ng0597-84')),
    ('merlot', 'Boursiquot J.-M. <i>et al.</i> (2009). Parentage of Merlot and related winegrape cultivars of southwestern France: discovery of the missing link. <i>Australian Journal of Grape and Wine Research</i> 15 : 144–155.' + doi('10.1111/j.1755-0238.2008.00041.x'),
               'Boursiquot J.-M. <i>et al.</i> (2009). Parentage of Merlot and related winegrape cultivars of southwestern France: discovery of the missing link. <i>Australian Journal of Grape and Wine Research</i> 15: 144–155.' + doi('10.1111/j.1755-0238.2008.00041.x')),
    ('savagnin', 'Ramos-Madrigal J. <i>et al.</i> (2019). Palaeogenomic insights into the origins of French grapevine diversity. <i>Nature Plants</i> 5 : 595–603 (pépin médiéval d’Orléans = Savagnin).' + doi('10.1038/s41477-019-0437-5'),
                 'Ramos-Madrigal J. <i>et al.</i> (2019). Palaeogenomic insights into the origins of French grapevine diversity. <i>Nature Plants</i> 5: 595–603 (medieval Orléans seed = Savagnin).' + doi('10.1038/s41477-019-0437-5')),
    ('muscat', 'Crespan M., Milani N. (2001). The Muscats: a molecular analysis of synonyms, homonyms and genetic relationships within a large family of grapevine cultivars. <i>Vitis</i> 40(1) : 23–30.',
               'Crespan M., Milani N. (2001). The Muscats: a molecular analysis of synonyms, homonyms and genetic relationships within a large family of grapevine cultivars. <i>Vitis</i> 40(1): 23–30.'),
]
NUM = {k: i + 1 for i, (k, _, _) in enumerate(SOURCES)}


def r(*keys):
    return '<sup class="ref">' + ','.join(f'<a href="#src-{NUM[k]}">{NUM[k]}</a>' for k in keys) + '</sup>'


# ------------------------------------------------------------------ « first wine » chart
# (year, short FR, short EN, place FR, place EN, kind, source)
FIRSTS = [
    (-9000, 'Domestication de la vigne', 'Grapevine domesticated', 'Asie occidentale & Caucase', 'Western Asia & Caucasus', 'vine', 'dong'),
    (-7000, 'Plus ancienne boisson fermentée', 'Oldest fermented drink', 'Jiahu, Chine', 'Jiahu, China', 'china', 'jiahu'),
    (-6000, 'Plus ancien vin de raisin', 'Oldest grape wine', 'Géorgie', 'Georgia', 'wine', 'georgia'),
    (-5400, 'Vin résiné en jarre', 'Resinated wine in a jar', 'Hajji Firuz Tepe, Iran', 'Hajji Firuz Tepe, Iran', 'wine', 'iran'),
    (-4100, 'Plus ancienne cave connue', 'Oldest known winery', 'Areni-1, Arménie', 'Areni-1, Armenia', 'wine', 'areni'),
    (-3150, 'Vin importé pour un roi', 'Wine imported for a king', 'Abydos, Égypte', 'Abydos, Egypt', 'wine', 'egypt'),
    (-425, 'Premier vin fait en France', 'First wine made in France', 'Lattes, Hérault', 'Lattes, Hérault', 'france', 'lattes'),
]
X0, X1 = -9500, 0


def year_label(y):
    a = abs(y)
    fr = f'≈ {a:,} av. J.-C.'.replace(',', '&#8239;')
    en = f'c. {a:,} BC'
    return fr, en


def firsts_html():
    rows = []
    for y, sfr, sen, pfr, pen, kind, src in FIRSTS:
        pos = (y - X0) / (X1 - X0) * 100
        yfr, yen = year_label(y)
        if kind == 'vine':
            yfr, yen = '≈ 11&#8239;000 ans', 'c. 11,000 years ago'
        rows.append(
            f'<div class="fr-row k-{kind}"><div class="fr-lab">{t((sfr, sen), "b")}{t((pfr, pen), "small")}</div>'
            f'<div class="fr-track"><span class="fr-bar" style="width:{pos:.1f}%"></span>'
            f'<span class="fr-dot" style="left:{pos:.1f}%"></span>'
            f'<span class="fr-yr" style="left:{pos:.1f}%">{t((yfr, yen))}{r(src)}</span></div></div>')
    ticks = ''.join(f'<span style="left:{(y - X0) / (X1 - X0) * 100:.1f}%">{t((f"{abs(y):,}".replace(",", "&#8239;") if y else "0", f"{abs(y):,}" if y else "0"))}</span>'
                    for y in (-9000, -7000, -5000, -3000, -1000))
    axis = f'<div class="fr-row axis"><div class="fr-lab">{t(("av. J.-C.", "BC"), "small")}</div><div class="fr-track fr-ticks">{ticks}</div></div>'
    return ''.join(rows) + axis


# ------------------------------------------------------------------ eras
def era(id_, kick, title, lead, cards, extra=''):
    k = t(kick, 'p', 'kick')
    h = t(title, 'h2')
    cs = ''.join(f'<article class="ev"><div class="ev-when">{t(w)}</div><h3>{t(h3)}</h3>{blk(body)}</article>'
                 for w, h3, body in cards)
    return (f'<section class="sec" id="{id_}"><div class="sec-head">{k}{h}</div>'
            f'<div class="panel lede">{blk(lead)}</div><div class="evs">{cs}</div>{extra}</section>')


ERAS = []

# 1 · origins
ERAS.append(era('origines', ('01 · Les origines', '01 · Origins'),
    ('La vigne <em>apprivoisée</em>', 'Taming <em>the vine</em>'),
    ('La vigne sauvage d’Eurasie, <i>Vitis vinifera</i> subsp. <i>sylvestris</i>, pousse des côtes de l’Atlantique jusqu’à l’Asie centrale. L’étude génétique de ≈&nbsp;3&nbsp;500 vignes cultivées et sauvages montre que l’homme l’a domestiquée <b>il y a ≈&nbsp;11&nbsp;000 ans</b>, au même moment en <b>Asie occidentale</b> et dans le <b>Caucase</b> : d’un côté des raisins de table, de l’autre des raisins de cuve' + r('dong') + '.',
     'The wild Eurasian grapevine, <i>Vitis vinifera</i> subsp. <i>sylvestris</i>, grows from the Atlantic coast to Central Asia. A genetic study of ≈&nbsp;3,500 cultivated and wild vines shows that people domesticated it <b>≈&nbsp;11,000 years ago</b>, at the same time in <b>Western Asia</b> and the <b>Caucasus</b>: table grapes on one side, wine grapes on the other' + r('dong') + '.'),
    [(('Une plante transformée', 'A transformed plant'),
      ('Ce que l’on a changé', 'What was changed'),
      ('La vigne sauvage a des pieds mâles et des pieds femelles. Les vignerons ont sélectionné des plantes <b>hermaphrodites</b>, qui se fécondent seules, et des baies plus grosses et plus sucrées' + r('dong') + '.',
       'Wild vines have separate male and female plants. Growers selected <b>hermaphrodite</b> plants, which pollinate themselves, and larger, sweeter berries' + r('dong') + '.')),
     (('Comment le sait-on ?', 'How do we know?'),
      ('La « signature » du raisin', 'The grape’s “signature”'),
      ('Les archéologues analysent les résidus imprégnés dans les poteries. L’<b>acide tartrique</b> n’existe en grande quantité que dans le raisin : c’est la preuve chimique la plus utilisée qu’un vase a contenu du vin' + r('iran', 'mcgovern_book') + '.',
       'Archaeologists analyse residues soaked into pottery. <b>Tartaric acid</b> occurs in large amounts only in grapes: it is the most widely used chemical proof that a jar once held wine' + r('iran', 'mcgovern_book') + '.')),
     (('Vers l’Europe', 'Into Europe'),
      ('La vigne voyage avec les premiers paysans', 'The vine travels with the first farmers'),
      ('Les vignes domestiquées gagnent l’Europe avec les premiers agriculteurs et se croisent avec les vignes sauvages locales ; la lignée des <b>muscats</b> se distingue dès la fin du Néolithique' + r('dong') + '.',
       'Domesticated vines reached Europe with the first farmers and crossed with local wild vines; the <b>muscat</b> lineage was already distinct by the late Neolithic' + r('dong') + '.'))]))

# 2 · China
china_box = ('<div class="panel answer" id="premier-vin"><h3>' + t(('Alors, qui a fait du vin le premier&nbsp;?', 'So who made wine first?')) + '</h3>'
    + blk(('<b>La Chine détient la plus ancienne trace chimique d’une boisson fermentée</b> (≈&nbsp;7000 av. J.-C.), qui contenait peut-être du raisin. <b>La Géorgie détient la plus ancienne trace d’un vin de raisin proprement dit</b> (≈&nbsp;6000 av. J.-C.). Les deux affirmations sont vraies : elles ne parlent pas de la même boisson' + r('jiahu', 'georgia') + '.',
           '<b>China holds the oldest chemical trace of a fermented drink</b> (≈&nbsp;7000 BC), which may have contained grape. <b>Georgia holds the oldest trace of a true grape wine</b> (≈&nbsp;6000 BC). Both statements are true: they do not describe the same drink' + r('jiahu', 'georgia') + '.'))
    + '<div class="firsts">' + firsts_html() + '</div>'
    + t(('Dates approximatives (≈), d’après les analyses publiées. Échelle linéaire.', 'Approximate dates (≈), from published analyses. Linear scale.'), 'p', 'note')
    + '</div>')
ERAS.append(era('chine', ('02 · La Chine', '02 · China'),
    ('La Chine, <em>≈&nbsp;9&nbsp;000 ans de boissons fermentées</em>', 'China, <em>≈&nbsp;9,000 years of fermented drinks</em>'),
    ('La Chine possède de nombreuses espèces de vignes sauvages qui lui sont propres. Mais la vigne à vin européenne, <i>Vitis vinifera</i>, y est arrivée bien plus tard, par la <b>route de la soie</b>. L’histoire chinoise du vin commence donc par une boisson mélangée, puis par un raisin importé.',
     'China has many wild vine species of its own. But the European wine grape, <i>Vitis vinifera</i>, arrived much later, along the <b>Silk Road</b>. China’s wine story therefore begins with a mixed drink, then with an imported grape.'),
    [(('≈ 7000 av. J.-C.', 'c. 7000 BC'),
      ('Jiahu : la plus ancienne boisson fermentée connue', 'Jiahu: the oldest known fermented drink'),
      ('Dans le village néolithique de <b>Jiahu</b> (province du Henan), des jarres contenaient une boisson fermentée de <b>riz, de miel et de fruits</b> (aubépine et/ou raisin). C’est la plus ancienne preuve chimique d’une boisson fermentée au monde, plus ancienne d’environ 1&nbsp;000 ans que le premier vin de raisin connu' + r('jiahu') + '.',
       'In the Neolithic village of <b>Jiahu</b> (Henan province), jars held a fermented drink of <b>rice, honey and fruit</b> (hawthorn and/or grape). It is the oldest chemical evidence of a fermented drink anywhere in the world, about 1,000 years older than the first known grape wine' + r('jiahu') + '.')),
     (('II<sup>e</sup> s. av. J.-C.', '2nd c. BC'),
      ('La vigne arrive par la route de la soie', 'The vine arrives along the Silk Road'),
      ('Les <i>Mémoires historiques</i> de Sima Qian racontent que le royaume de <b>Dayuan</b> (Ferghana, Ouzbékistan actuel) fait du vin de raisin, et que les envoyés de la dynastie <b>Han</b> en rapportent des vignes, plantées près de la capitale' + r('shiji') + '. La tradition en attribue le mérite à l’explorateur <b>Zhang Qian</b>, mais les historiens en discutent depuis 1919' + r('laufer') + '.',
       'Sima Qian’s <i>Records of the Grand Historian</i> say that the kingdom of <b>Dayuan</b> (Ferghana, today’s Uzbekistan) made grape wine, and that envoys of the <b>Han</b> dynasty brought vines back and planted them near the capital' + r('shiji') + '. Tradition credits the explorer <b>Zhang Qian</b>, but historians have debated this since 1919' + r('laufer') + '.')),
     (('640', '640'),
      ('Les Tang apprennent à vinifier', 'The Tang learn to make wine'),
      ('Après la prise de <b>Gaochang</b> (près de Tourfan) en 640, l’empereur <b>Taizong</b> des Tang en rapporte un raisin appelé « <b>tétine de jument</b> » (<i>manaizi</i>) et la méthode de vinification, et fait planter des vignes dans les jardins impériaux' + r('tang') + '.',
       'After taking <b>Gaochang</b> (near Turpan) in 640, Emperor <b>Taizong</b> of the Tang brought back a grape called “<b>mare’s nipple</b>” (<i>manaizi</i>) and the wine-making method, and had vines planted in the imperial gardens' + r('tang') + '.')),
     (('1892', '1892'),
      ('Changyu, première cave moderne', 'Changyu, the first modern winery'),
      ('<b>Zhang Bishi</b> fonde à <b>Yantai</b> (Shandong) la cave <b>Changyu</b>, la première cave industrielle de Chine. Les vignes européennes importées souffrant du climat, on les greffe sur des vignes sauvages du nord-est de la Chine' + r('changyu') + '.',
       '<b>Zhang Bishi</b> founded the <b>Changyu</b> winery in <b>Yantai</b> (Shandong), China’s first industrial winery. As the imported European vines struggled in the climate, they were grafted onto wild vines from north-east China' + r('changyu') + '.')),
     (('Aujourd’hui', 'Today'),
      ('Le 3<sup>e</sup> vignoble du monde', 'The world’s 3rd-largest vineyard'),
      ('Avec ≈&nbsp;750&nbsp;000 hectares de vignes (2024), la Chine a la <b>3<sup>e</sup> surface viticole du monde</b>, derrière l’Espagne et la France, dont une grande partie sert au raisin de table' + r('oiv') + '.',
       'With ≈&nbsp;750,000 hectares of vines (2024), China has the <b>world’s 3rd-largest vineyard area</b>, behind Spain and France, much of it for table grapes' + r('oiv') + '.'))],
    china_box))

# 3 · Caucasus & Near East
ERAS.append(era('caucase', ('03 · Caucase & Proche-Orient', '03 · Caucasus & Near East'),
    ('Le berceau <em>du vin de raisin</em>', 'The cradle <em>of grape wine</em>'),
    ('C’est entre la mer Noire, la Caspienne et les monts Zagros que l’on trouve les plus anciennes preuves d’un vin fait uniquement de raisin.',
     'The oldest evidence of a wine made from grapes alone is found between the Black Sea, the Caspian and the Zagros mountains.'),
    [(('≈ 6000 av. J.-C.', 'c. 6000 BC'),
      ('Géorgie : le plus ancien vin de raisin', 'Georgia: the oldest grape wine'),
      ('Sur deux villages néolithiques au sud de Tbilissi, <b>Gadachrili Gora</b> et <b>Shulaveris Gora</b>, de grandes jarres portent des traces d’acide tartrique : c’est le plus ancien vin de raisin identifié à ce jour' + r('georgia') + '. La Géorgie vinifie encore en <b>qvevri</b>, grandes jarres enterrées, une méthode inscrite au patrimoine immatériel de l’UNESCO en 2013' + r('unesco') + '.',
       'At two Neolithic villages south of Tbilisi, <b>Gadachrili Gora</b> and <b>Shulaveris Gora</b>, large jars carry traces of tartaric acid: the oldest grape wine identified so far' + r('georgia') + '. Georgia still makes wine in <b>qvevri</b>, large buried jars, a method added to UNESCO’s intangible heritage list in 2013' + r('unesco') + '.')),
     (('≈ 5400 av. J.-C.', 'c. 5400 BC'),
      ('Iran : le vin résiné', 'Iran: resinated wine'),
      ('À <b>Hajji Firuz Tepe</b> (monts Zagros), une jarre contenait du vin additionné de <b>résine de térébinthe</b>, sans doute pour le conserver : le vin était fait volontairement' + r('iran') + '.',
       'At <b>Hajji Firuz Tepe</b> (Zagros mountains), a jar held wine mixed with <b>terebinth resin</b>, probably as a preservative: the wine was made on purpose' + r('iran') + '.')),
     (('≈ 4100 av. J.-C.', 'c. 4100 BC'),
      ('Arménie : la plus ancienne cave connue', 'Armenia: the oldest known winery'),
      ('Dans la grotte d’<b>Areni-1</b>, les archéologues ont trouvé un fouloir en argile, une cuve de fermentation et des jarres de stockage en place : la plus ancienne installation de vinification complète connue' + r('areni') + '. Le village d’Areni a donné son nom à un cépage local, l’<b>Areni noir</b>' + r('wine_grapes') + '.',
       'In the <b>Areni-1</b> cave, archaeologists found a clay treading floor, a fermentation vat and storage jars in place: the oldest complete wine-making installation known' + r('areni') + '. The village of Areni gave its name to a local grape, <b>Areni Noir</b>' + r('wine_grapes') + '.'))]))

# 4 · Egypt
ERAS.append(era('egypte', ('04 · Égypte & Mésopotamie', '04 · Egypt & Mesopotamia'),
    ('Le vin <em>des rois</em>', 'The wine <em>of kings</em>'),
    ('Dans les grandes civilisations du Proche-Orient, le vin reste une boisson de prestige, réservée aux rois, aux temples et aux élites ; le peuple boit surtout de la bière' + r('mcgovern_book') + '.',
     'In the great civilisations of the Near East, wine remained a prestige drink for kings, temples and elites; ordinary people drank mostly beer' + r('mcgovern_book') + '.'),
    [(('≈ 3150 av. J.-C.', 'c. 3150 BC'),
      ('Le vin du roi Scorpion', 'King Scorpion’s wine'),
      ('La tombe du roi <b>Scorpion I<sup>er</sup></b> à Abydos contenait des centaines de jarres de vin importées du Levant. Les analyses y ont trouvé du vin aromatisé aux herbes, la plus ancienne preuve d’herbes ajoutées au vin' + r('egypt') + '.',
       'The tomb of King <b>Scorpion I</b> at Abydos held hundreds of wine jars imported from the Levant. Analyses found wine flavoured with herbs, the earliest evidence of herbs added to wine' + r('egypt') + '.')),
     (('≈ 1323 av. J.-C.', 'c. 1323 BC'),
      ('Les premières « étiquettes »', 'The first “labels”'),
      ('Dans la tombe de <b>Toutânkhamon</b>, les jarres de vin portent une inscription : l’<b>année du règne</b>, le <b>domaine</b> d’origine et le nom du <b>chef vigneron</b>. C’est l’ancêtre direct de nos étiquettes avec millésime et producteur' + r('cerny') + '.',
       'In <b>Tutankhamun</b>’s tomb, the wine jars carry an inscription: the <b>year of the reign</b>, the <b>estate</b> of origin and the name of the <b>chief vintner</b>. It is the direct ancestor of our labels with vintage and producer' + r('cerny') + '.'))]))

# 5 · Greece, Rome, Gaul
ERAS.append(era('mediterranee', ('05 · Grèce, Rome & Gaule', '05 · Greece, Rome & Gaul'),
    ('Le vin conquiert <em>la Méditerranée</em>', 'Wine conquers <em>the Mediterranean</em>'),
    ('Phéniciens, Grecs puis Romains diffusent la vigne et le vin autour de la Méditerranée. C’est par le sud que le vin arrive dans ce qui deviendra la France' + r('johnson', 'oxford') + '.',
     'Phoenicians, Greeks and then Romans spread the vine and wine around the Mediterranean. Wine reached what would become France from the south' + r('johnson', 'oxford') + '.'),
    [(('≈ 600 av. J.-C.', 'c. 600 BC'),
      ('Les Grecs fondent Marseille', 'Greeks found Marseille'),
      ('Des Grecs venus de Phocée (Asie Mineure) fondent <b>Massalia</b>, Marseille' + r('marseille') + '. Le commerce du vin entre la Méditerranée et la Gaule s’y développe' + r('dion') + '.',
       'Greeks from Phocaea (Asia Minor) founded <b>Massalia</b>, Marseille' + r('marseille') + '. The wine trade between the Mediterranean and Gaul grew from there' + r('dion') + '.')),
     (('≈ 425 av. J.-C.', 'c. 425 BC'),
      ('Le premier vin fait en France', 'The first wine made in France'),
      ('À <b>Lattes</b> (près de Montpellier), des amphores étrusques montrent du vin importé d’Italie vers ≈&nbsp;500 av. J.-C. ; un pressoir en pierre daté de ≈&nbsp;425 av. J.-C. porte des traces de raisin : c’est la plus ancienne preuve de vin <b>produit</b> en France' + r('lattes') + '.',
       'At <b>Lattes</b> (near Montpellier), Etruscan amphorae show wine imported from Italy around ≈&nbsp;500 BC; a stone press dated ≈&nbsp;425 BC carries grape traces: the oldest evidence of wine <b>made</b> in France' + r('lattes') + '.')),
     (('I<sup>er</sup> – III<sup>e</sup> s.', '1st – 3rd c.'),
      ('Les Romains plantent la Gaule', 'The Romans plant Gaul'),
      ('La vigne gagne la Narbonnaise, puis la vallée du Rhône, le Bordelais, la Bourgogne et la Moselle. Vers 92, l’empereur <b>Domitien</b> interdit de nouvelles plantations en Italie et ordonne d’arracher une partie des vignes des provinces ; la mesure fut peu appliquée. L’empereur <b>Probus</b> (276-282) encourage au contraire la plantation' + r('oxford', 'dion') + '.',
       'The vine spread to Narbonensis, then the Rhône valley, Bordeaux, Burgundy and the Moselle. Around 92, Emperor <b>Domitian</b> banned new planting in Italy and ordered part of the provincial vineyards uprooted; the measure was little enforced. Emperor <b>Probus</b> (276–282), by contrast, encouraged planting' + r('oxford', 'dion') + '.'))]))

# 6 · Middle Ages
ERAS.append(era('moyen-age', ('06 · Moyen Âge', '06 · Middle Ages'),
    ('Moines, ducs <em>et marchands</em>', 'Monks, dukes <em>and merchants</em>'),
    ('Après la chute de Rome, l’Église entretient la vigne : il faut du vin pour la messe, et les monastères reçoivent des terres en dons. Les grands vignobles se structurent autour des abbayes, des princes et des ports' + r('oxford', 'dion') + '.',
     'After the fall of Rome, the Church kept the vine going: wine was needed for Mass, and monasteries received land as gifts. The great vineyards took shape around abbeys, princes and ports' + r('oxford', 'dion') + '.'),
    [(('XII<sup>e</sup> s.', '12th c.'),
      ('Les Cisterciens en Bourgogne', 'The Cistercians in Burgundy'),
      ('Les moines de l’abbaye de <b>Cîteaux</b>, fondée en 1098, constituent le <b>Clos de Vougeot</b>, qu’ils entourent de murs. Les abbayes deviennent les grands propriétaires de vignes de Bourgogne' + r('oxford', 'johnson') + '.',
       'The monks of <b>Cîteaux</b> abbey, founded in 1098, built up the <b>Clos de Vougeot</b> and walled it in. The abbeys became Burgundy’s great vineyard owners' + r('oxford', 'johnson') + '.')),
     (('1152', '1152'),
      ('Bordeaux devient anglais', 'Bordeaux becomes English'),
      ('Le mariage d’<b>Aliénor d’Aquitaine</b> avec Henri Plantagenêt, futur roi d’Angleterre, lie l’Aquitaine à la couronne anglaise jusqu’en 1453. Bordeaux expédie alors d’énormes quantités de vin clair, le « <b>claret</b> », vers l’Angleterre' + r('oxford', 'johnson') + '.',
       'The marriage of <b>Eleanor of Aquitaine</b> to Henry Plantagenet, future king of England, tied Aquitaine to the English crown until 1453. Bordeaux then shipped huge quantities of light red wine, “<b>claret</b>”, to England' + r('oxford', 'johnson') + '.')),
     (('1395', '1395'),
      ('Le gamay banni', 'Gamay banned'),
      ('Le duc de Bourgogne <b>Philippe le Hardi</b> ordonne d’arracher le <b>gamay</b>, « très mauvais et très déloyal plant », pour protéger la réputation du <b>pinot</b>. C’est l’une des premières lois de qualité sur un cépage' + r('gamay', 'dion') + '.',
       'The Duke of Burgundy, <b>Philip the Bold</b>, ordered <b>Gamay</b> to be uprooted as a “very bad and very disloyal plant”, to protect the reputation of <b>Pinot</b>. It is one of the first quality laws about a grape variety' + r('gamay', 'dion') + '.')),
     (('1443', '1443'),
      ('Les Hospices de Beaune', 'The Hospices de Beaune'),
      ('Le chancelier <b>Nicolas Rolin</b> et son épouse <b>Guigone de Salins</b> fondent à Beaune l’<b>Hôtel-Dieu</b>, un hôpital pour les pauvres' + r('hospices') + '. Au fil des siècles, des donateurs lui lèguent leurs vignes : les Hospices possèdent aujourd’hui ≈&nbsp;60&nbsp;ha, surtout en premiers et grands crus, dont les vins sont vendus aux <b>enchères publiques depuis 1859</b>, le troisième dimanche de novembre' + r('sothebys') + '. L’Hôtel-Dieu abrite aussi une collection de <a href="../Bottle_Sizes.html#tastevin">tastevins</a>.',
       'Chancellor <b>Nicolas Rolin</b> and his wife <b>Guigone de Salins</b> founded the <b>Hôtel-Dieu</b> in Beaune, a hospital for the poor' + r('hospices') + '. Over the centuries donors bequeathed their vineyards to it: the Hospices now own ≈&nbsp;60&nbsp;ha, mostly premiers and grands crus, whose wines have been sold at <b>public auction since 1859</b>, on the third Sunday of November' + r('sothebys') + '. The Hôtel-Dieu also holds a collection of <a href="../Bottle_Sizes.html#tastevin">tastevins</a>.'))]))

# 7 · Modern times
ERAS.append(era('temps-modernes', ('07 · Temps modernes', '07 · Early modern era'),
    ('La bouteille <em>et le Nouveau Monde</em>', 'The bottle <em>and the New World</em>'),
    ('Du XVI<sup>e</sup> au XIX<sup>e</sup> siècle, le vin change de contenant et de continent : la bouteille de verre et le bouchon de liège permettent de le faire vieillir, et les Européens plantent la vigne sur tous les continents' + r('johnson') + '.',
     'From the 16th to the 19th century, wine changed container and continent: the glass bottle and the cork made ageing possible, and Europeans planted vines on every continent' + r('johnson') + '.'),
    [(('XVI<sup>e</sup> s.', '16th c.'),
      ('La vigne arrive aux Amériques', 'The vine reaches the Americas'),
      ('Les Espagnols plantent la vigne au Mexique, au Pérou, au Chili et en Argentine. Le cépage de ces premiers vignobles, connu sous les noms de <b>Mission</b>, <b>País</b> ou <b>Criolla chica</b>, est en fait le <b>Listán Prieto</b> des îles Canaries et de Castille' + r('tapia') + '.',
       'The Spanish planted vines in Mexico, Peru, Chile and Argentina. The grape of these first vineyards, known as <b>Mission</b>, <b>País</b> or <b>Criolla chica</b>, is in fact <b>Listán Prieto</b> from the Canary Islands and Castile' + r('tapia') + '.')),
     (('XVII<sup>e</sup> – XVIII<sup>e</sup> s.', '17th – 18th c.'),
      ('La bouteille de verre', 'The glass bottle'),
      ('Un verre anglais plus solide, le bouchon de liège et la bouteille cylindrique que l’on peut coucher permettent de transporter et de faire vieillir le vin en bouteille. Toute l’histoire est sur la page <a href="../Bottle_Sizes.html#histoire">Histoire de la bouteille</a>.',
       'Stronger English glass, the cork and the cylindrical bottle that can be laid down made it possible to ship and age wine in bottle. The full story is on the <a href="../Bottle_Sizes.html#histoire">History of the bottle</a> page.')),
     (('1659', '1659'),
      ('Le premier vin du Cap', 'The first Cape wine'),
      ('Le 2 février 1659, <b>Jan van Riebeeck</b>, commandant néerlandais du Cap, note dans son journal le pressurage du premier vin d’Afrique du Sud' + r('cape') + '. Des vignes arrivent en Australie avec la « First Fleet » britannique en 1788' + r('oxford') + '.',
       'On 2 February 1659, <b>Jan van Riebeeck</b>, Dutch commander at the Cape, recorded in his journal the pressing of South Africa’s first wine' + r('cape') + '. Vines reached Australia with the British First Fleet in 1788' + r('oxford') + '.')),
     (('1855', '1855'),
      ('Le classement de Bordeaux', 'The Bordeaux classification'),
      ('Pour l’Exposition universelle de Paris, les courtiers de Bordeaux classent les grands vins du Médoc et de Sauternes selon leur prix' + r('oxford') + '. Voir la page <a href="../Crus_Classifications.html">Les classifications des crus</a>.',
       'For the Paris Universal Exhibition, Bordeaux brokers ranked the great wines of the Médoc and Sauternes by price' + r('oxford') + '. See the <a href="../Crus_Classifications.html">Crus classifications</a> page.'))]))

# 8 · crises & laws
ERAS.append(era('crises', ('08 · Crises & lois', '08 · Crises & laws'),
    ('Le phylloxéra <em>et la naissance des AOC</em>', 'Phylloxera <em>and the birth of the AOC</em>'),
    ('À la fin du XIX<sup>e</sup> siècle, un minuscule insecte venu d’Amérique détruit la plus grande partie du vignoble européen. La reconstruction, puis les fraudes qui suivent, mènent à la loi sur les appellations d’origine' + r('phyllo', 'inao') + '.',
     'In the late 19th century, a tiny insect from America destroyed most of Europe’s vineyards. Rebuilding them, and the frauds that followed, led to the law on appellations of origin' + r('phyllo', 'inao') + '.'),
    [(('1863 – 1868', '1863 – 1868'),
      ('Le phylloxéra', 'Phylloxera'),
      ('Des vignes dépérissent dans le sud de la vallée du Rhône dès ≈&nbsp;1863. En 1868, le botaniste <b>Jules-Émile Planchon</b> identifie la cause : un puceron des racines venu d’Amérique, qu’il nomme <i>Phylloxera vastatrix</i>, « le dévastateur »' + r('phyllo') + '.',
       'Vines began dying in the southern Rhône valley from ≈&nbsp;1863. In 1868 the botanist <b>Jules-Émile Planchon</b> identified the cause: a root aphid from America, which he named <i>Phylloxera vastatrix</i>, “the devastator”' + r('phyllo') + '.')),
     (('1880 – 1900', '1880 – 1900'),
      ('Le salut : la greffe', 'The cure: grafting'),
      ('Les vignes américaines résistent à l’insecte. On replante donc les cépages européens <b>greffés sur des porte-greffes américains</b> : c’est encore la règle aujourd’hui dans la plupart des vignobles du monde' + r('phyllo') + '.',
       'American vines resist the insect. European varieties were therefore replanted <b>grafted onto American rootstocks</b>: still the rule today in most of the world’s vineyards' + r('phyllo') + '.')),
     (('1935 – 1936', '1935 – 1936'),
      ('Naissance des AOC', 'The AOC is born'),
      ('Le décret-loi du <b>30 juillet 1935</b> crée le Comité national des appellations d’origine, futur <b>INAO</b>. Les premières AOC sont reconnues le <b>15 mai 1936</b> : Arbois, Cassis, Châteauneuf-du-Pape, Cognac, Monbazillac et Tavel' + r('inao') + '. Voir aussi <a href="../Categories_of_French_Wines.html">Comprendre l’AOC-AOP</a>.',
       'The decree-law of <b>30 July 1935</b> created the National Committee for Appellations of Origin, later the <b>INAO</b>. The first AOCs were recognised on <b>15 May 1936</b>: Arbois, Cassis, Châteauneuf-du-Pape, Cognac, Monbazillac and Tavel' + r('inao') + '. See also <a href="../Categories_of_French_Wines.html">Understanding AOC-AOP</a>.'))]))

# ------------------------------------------------------------------ ancestral grapes
GRAPES = [
    ('Vitis vinifera sylvestris', 'Vitis vinifera sylvestris', ('La vigne sauvage', 'The wild vine'), '#6b8f4e',
     ('L’ancêtre de toutes les vignes à vin. Elle pousse encore à l’état sauvage, de l’Europe à l’Asie centrale, mais elle est devenue rare' + r('dong') + '.',
      'The ancestor of every wine grape. It still grows wild from Europe to Central Asia, but has become rare' + r('dong') + '.')),
    ('Muscat à petits grains', 'Muscat Blanc à Petits Grains', ('Famille très ancienne', 'A very old family'), '#c9a23a',
     ('La lignée des muscats est distincte dès la fin du Néolithique' + r('dong') + '. Le muscat à petits grains est un parent du <b>muscat d’Alexandrie</b>' + r('muscat') + '.',
      'The muscat lineage was distinct by the late Neolithic' + r('dong') + '. Muscat Blanc à Petits Grains is a parent of <b>Muscat of Alexandria</b>' + r('muscat') + '.')),
    ('Savagnin (Traminer)', 'Savagnin (Traminer)', ('Jura, Alsace, Europe centrale', 'Jura, Alsace, Central Europe'), '#b9a24a',
     ('Un pépin médiéval trouvé à Orléans (≈&nbsp;XII<sup>e</sup> siècle) a le même ADN que le savagnin actuel : il est multiplié à l’identique par bouturage depuis ≈&nbsp;900 ans' + r('savagnin') + '. Le gewurztraminer en est une forme aromatique' + r('wine_grapes') + '.',
      'A medieval seed found in Orléans (≈&nbsp;12th century) has the same DNA as today’s Savagnin: it has been propagated identically by cuttings for ≈&nbsp;900 years' + r('savagnin') + '. Gewurztraminer is an aromatic form of it' + r('wine_grapes') + '.')),
    ('Pinot', 'Pinot', ('Bourgogne', 'Burgundy'), '#7d2a3a',
     ('Le pinot est l’un des deux parents du <b>chardonnay</b>, du <b>gamay</b>, de l’<b>aligoté</b>, du <b>melon</b> et d’une douzaine d’autres cépages du nord-est de la France' + r('bowers99') + '.',
      'Pinot is one of the two parents of <b>Chardonnay</b>, <b>Gamay</b>, <b>Aligoté</b>, <b>Melon</b> and a dozen other grapes of north-eastern France' + r('bowers99') + '.')),
    ('Gouais blanc', 'Gouais Blanc', ('Le « mauvais » ancêtre', 'The “humble” ancestor'), '#9a9a6a',
     ('Cépage paysan longtemps méprisé, souvent interdit, il est pourtant l’autre parent du chardonnay et de ses ≈&nbsp;15 frères et sœurs (croisements naturels avec le pinot)' + r('bowers99') + '.',
      'A peasant grape long despised and often banned, yet it is the other parent of Chardonnay and its ≈&nbsp;15 siblings (natural crosses with Pinot)' + r('bowers99') + '.')),
    ('Cabernet franc', 'Cabernet Franc', ('Bordeaux, Loire', 'Bordeaux, Loire'), '#5a2a4a',
     ('Parent du <b>cabernet-sauvignon</b> (avec le sauvignon blanc)' + r('bowers97') + ' et du <b>merlot</b> (avec la magdeleine noire des Charentes)' + r('merlot') + '.',
      'Parent of <b>Cabernet Sauvignon</b> (with Sauvignon Blanc)' + r('bowers97') + ' and of <b>Merlot</b> (with Magdeleine Noire des Charentes)' + r('merlot') + '.')),
    ('Saperavi & Rkatsiteli', 'Saperavi & Rkatsiteli', ('Géorgie', 'Georgia'), '#4a1a2a',
     ('Deux cépages autochtones géorgiens très anciens, le <b>saperavi</b> (rouge, à pulpe colorée) et le <b>rkatsiteli</b> (blanc), toujours vinifiés en qvevri' + r('wine_grapes', 'unesco') + '.',
      'Two very old native Georgian grapes, <b>Saperavi</b> (red, with coloured flesh) and <b>Rkatsiteli</b> (white), still made in qvevri' + r('wine_grapes', 'unesco') + '.')),
    ('Areni noir', 'Areni Noir', ('Arménie', 'Armenia'), '#6a2030',
     ('Cépage rouge arménien qui porte le nom du village de la plus ancienne cave connue' + r('wine_grapes', 'areni') + '.',
      'Armenian red grape named after the village of the oldest known winery' + r('wine_grapes', 'areni') + '.')),
    ('« Tétine de jument »', '“Mare’s nipple”', ('Chine (manaizi)', 'China (manaizi)'), '#8a7a3a',
     ('Raisin allongé rapporté de Gaochang par les Tang en 640, avec la méthode de vinification' + r('tang') + '.',
      'Elongated grape brought back from Gaochang by the Tang in 640, together with the wine-making method' + r('tang') + '.')),
    ('Listán Prieto', 'Listán Prieto', ('Mission · País · Criolla', 'Mission · País · Criolla'), '#7a3a2a',
     ('Le premier cépage européen planté aux Amériques par les Espagnols au XVI<sup>e</sup> siècle' + r('tapia') + '.',
      'The first European grape planted in the Americas by the Spanish in the 16th century' + r('tapia') + '.')),
]


def grapes_html():
    out = []
    for nfr, nen, region, col, txt in GRAPES:
        out.append(f'<article class="gp" style="--c:{col}"><div class="gp-dot" aria-hidden="true"></div>'
                   f'<h3>{t((nfr, nen))}</h3>{t(region, "p", "gp-reg")}{blk(txt)}</article>')
    return ''.join(out)


# ------------------------------------------------------------------ page
TOC = [('origines', '01 Origines', '01 Origins'), ('chine', '02 Chine', '02 China'), ('caucase', '03 Caucase', '03 Caucasus'),
       ('egypte', '04 Égypte', '04 Egypt'), ('mediterranee', '05 Grèce & Rome', '05 Greece & Rome'),
       ('moyen-age', '06 Moyen Âge', '06 Middle Ages'), ('temps-modernes', '07 Temps modernes', '07 Early modern'),
       ('crises', '08 Phylloxéra & AOC', '08 Phylloxera & AOC'), ('cepages', 'Cépages ancestraux', 'Ancestral grapes'),
       ('sources', 'Sources', 'Sources')]

KEYS = [
    ('≈ 11 000 ans', 'c. 11,000 years', 'domestication de la vigne', 'since the vine was domesticated', 'dong'),
    ('≈ 7000 av. J.-C.', 'c. 7000 BC', 'boisson fermentée de Jiahu (Chine)', 'Jiahu fermented drink (China)', 'jiahu'),
    ('≈ 6000 av. J.-C.', 'c. 6000 BC', 'plus ancien vin de raisin (Géorgie)', 'oldest grape wine (Georgia)', 'georgia'),
    ('≈ 425 av. J.-C.', 'c. 425 BC', 'premier vin produit en France', 'first wine made in France', 'lattes'),
]


def keys_html():
    return ''.join(f'<div class="key"><b>{t((a, b))}</b>{t((c, d), "small")}{r(s)}</div>' for a, b, c, d, s in KEYS)


def sources_html():
    return ''.join(f'<li id="src-{i + 1}">{t((fr, en))}</li>' for i, (_, fr, en) in enumerate(SOURCES))


CSS = r'''
  sup.ref{font-size:.68em;line-height:0;margin-left:1px;}
  sup.ref a{color:var(--gold);text-decoration:none;font-weight:700;}
  sup.ref a:hover{text-decoration:underline;}
  .lede{padding:clamp(18px,3vw,30px);}
  .lede p{margin:0;font-size:15.5px;line-height:1.72;}
  .lede a,.ev a{color:var(--gold-soft);}
  .sec-head .kick{font-size:10.5px;letter-spacing:.3em;text-transform:uppercase;color:var(--gold);font-weight:700;margin:0 0 8px;}
  .keys{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;margin-top:24px;}
  .key{padding:14px 16px;border-radius:16px;border:1px solid var(--hair);background:var(--glass);text-align:left;}
  .key b{display:block;font-family:var(--serif);font-weight:500;font-size:22px;color:var(--title);line-height:1.1;}
  .key small{font-size:12.5px;color:var(--muted);line-height:1.4;}
  .evs{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;margin-top:14px;}
  .ev{padding:16px 18px 18px;border-radius:16px;background:var(--glass);border:1px solid var(--hair);position:relative;}
  .ev-when{font-family:var(--serif);font-size:15px;color:var(--gold-soft);margin-bottom:4px;}
  .ev h3{margin:0 0 8px;font-family:var(--serif);font-weight:500;font-size:20px;line-height:1.2;color:var(--title);}
  .ev p{margin:0;font-size:14.2px;line-height:1.64;}
  .answer{margin-top:14px;padding:clamp(18px,3vw,30px);border-color:var(--hair-hi);}
  .answer h3{margin:0 0 10px;font-family:var(--serif);font-weight:500;font-size:24px;color:var(--title);}
  .answer > p{font-size:15px;line-height:1.7;margin:0 0 6px;}
  .firsts{margin-top:18px;display:grid;gap:6px;}
  .fr-row{display:grid;grid-template-columns:minmax(150px,230px) 1fr;gap:14px;align-items:center;}
  .fr-lab b{display:block;font-size:13.5px;font-weight:600;color:var(--title);line-height:1.25;}
  .fr-lab small{font-size:11.5px;color:var(--muted);}
  .fr-track{position:relative;height:34px;border-radius:8px;background:var(--track);}
  .fr-bar{position:absolute;left:0;top:15px;height:4px;border-radius:2px;background:linear-gradient(90deg,transparent,color-mix(in srgb,var(--k) 55%,transparent));}
  .fr-dot{position:absolute;top:10px;width:14px;height:14px;margin-left:-7px;border-radius:50%;background:var(--k);box-shadow:0 0 0 3px color-mix(in srgb,var(--k) 25%,transparent);}
  .fr-yr{position:absolute;top:-1px;transform:translateX(12px);font-size:11.5px;white-space:nowrap;color:var(--muted);}
  .fr-row.k-vine{--k:#6b8f4e;} .fr-row.k-china{--k:#c8102e;} .fr-row.k-wine{--k:#9b2235;} .fr-row.k-france{--k:#2c5aa0;}
  html:not([data-theme="cream"]) .fr-row.k-wine{--k:#d9566b;} html:not([data-theme="cream"]) .fr-row.k-france{--k:#6f9be0;}
  .fr-row:nth-child(n+5) .fr-yr{transform:translateX(calc(-100% - 12px));}
  .fr-ticks{background:none;height:18px;border-top:1px solid var(--hair-hi);border-radius:0;}
  .fr-ticks span{position:absolute;top:3px;transform:translateX(-50%);font-size:10.5px;color:var(--faint);}
  .note{font-size:12px;color:var(--faint);margin:12px 0 0;}
  .gps{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px;margin-top:14px;}
  .gp{padding:16px 18px 18px;border-radius:16px;background:var(--glass);border:1px solid var(--hair);border-top:3px solid var(--c);position:relative;}
  .gp-dot{position:absolute;top:16px;right:16px;width:22px;height:22px;border-radius:50%;
    background:radial-gradient(circle at 35% 30%,color-mix(in srgb,var(--c) 40%,#fff),var(--c) 60%);box-shadow:inset -2px -3px 5px rgba(0,0,0,.25);}
  .gp h3{margin:0 30px 2px 0;font-family:var(--serif);font-weight:500;font-size:19px;color:var(--title);}
  .gp-reg{margin:0 0 8px;font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--gold);font-weight:700;}
  .gp p{margin:0;font-size:13.8px;line-height:1.6;}
  .sources-list{margin:0;padding-left:26px;font-size:13px;line-height:1.6;color:var(--muted);columns:2;column-gap:34px;}
  .sources-list li{break-inside:avoid;margin-bottom:6px;}
  .sources-list li:target{color:var(--title);background:color-mix(in srgb,var(--gold) 14%,transparent);border-radius:6px;}
  .sources-list a{color:var(--gold);}
  .method{font-size:12.5px;color:var(--faint);line-height:1.6;margin:14px 0 0;}
  @media (max-width:900px){ .keys{grid-template-columns:repeat(2,minmax(0,1fr));} .sources-list{columns:1;} }
  @media (max-width:620px){
    .fr-row{grid-template-columns:1fr;gap:4px;}
    .fr-row.axis .fr-lab{display:none;}
    .fr-yr{font-size:10.5px;}
  }
  @media (max-width:420px){ .keys{grid-template-columns:1fr;} }
'''

TEMPLATE = '''<!DOCTYPE html>
<html lang="fr">
<head>
<!--fw-theme:start--><script src="../../assets/theme.js"></script><!--fw-theme:end-->
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Histoire du vin</title>
<meta name="description" content="Histoire du vin, de la domestication de la vigne il y a 11 000 ans à la naissance des AOC : Chine, Géorgie, Égypte, Rome, Moyen Âge, phylloxéra, cépages ancestraux. Faits sourcés.">
<style>
@@BASE_CSS@@
@@CSS@@
</style>
</head>
<body>
<div class="wrap">
  <div class="topbar">
    <a class="back" href="../../index.html" data-fr="← Retour" data-en="← Back">← Retour</a>
    <button class="lang" id="langbtn" type="button" aria-label="Language">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 3.8 5.8 3.8 9S14.5 18.5 12 21C9.5 18.5 8.2 15.2 8.2 12S9.5 5.5 12 3Z"/></svg>
      <span id="langlbl">English</span>
    </button>
  </div>

  <header>
    <p class="eyebrow" data-fr="De la vigne sauvage aux AOC" data-en="From the wild vine to the AOC">De la vigne sauvage aux AOC</p>
    <h1 data-fr="Histoire <em>du vin</em>" data-en="A history <em>of wine</em>">Histoire <em>du vin</em></h1>
    <div class="rule"></div>
    @@TAGLINE@@
    <div class="keys">@@KEYS@@</div>
    <nav class="toc">@@TOC@@</nav>
  </header>

@@ERAS@@

  <section class="sec" id="cepages">
    <div class="sec-head">
      <p class="kick" data-fr="09 · Les cépages ancestraux" data-en="09 · Ancestral grapes">09 · Les cépages ancestraux</p>
      <h2 data-fr="Les ancêtres <em>de nos cépages</em>" data-en="The ancestors <em>of our grapes</em>">Les ancêtres <em>de nos cépages</em></h2>
    </div>
    <div class="panel lede">@@GRAPES_LEAD@@</div>
    <div class="gps">@@GRAPES@@</div>
  </section>

  <footer id="sources">
    <h3 data-fr="Sources" data-en="Sources">Sources</h3>
    <ol class="sources-list">@@SOURCES@@</ol>
    @@METHOD@@
  </footer>
</div>
<script>
(function(){
  var LANG = 'fr';
  try{ var s = localStorage.getItem('fw_lang'); if(s==='fr'||s==='en') LANG = s; }catch(e){}
  var $ = function(id){ return document.getElementById(id); };
  function applyLang(){
    document.documentElement.lang = LANG;
    document.title = LANG==='fr' ? 'Histoire du vin' : 'A history of wine';
    var nodes = document.querySelectorAll('[data-fr]');
    for(var i=0;i<nodes.length;i++){ var v = nodes[i].getAttribute('data-'+LANG); if(v!==null) nodes[i].innerHTML = v; }
    $('langlbl').textContent = LANG==='fr' ? 'English' : 'Français';
  }
  $('langbtn').addEventListener('click', function(){
    LANG = LANG==='fr' ? 'en' : 'fr';
    try{ localStorage.setItem('fw_lang', LANG); }catch(e){}
    applyLang();
  });
  document.addEventListener('fw:lang', function(e){
    var l = (e.detail && e.detail.lang) || document.documentElement.lang;
    if((l==='fr'||l==='en') && l!==LANG){ LANG = l; applyLang(); }
  });
  applyLang();
  if(location.hash){
    var tgt = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if(tgt) setTimeout(function(){ tgt.scrollIntoView({block:'start'}); }, 0);
  }
})();
</script>
</body>
</html>
'''


def main():
    toc = ''.join(f'<a href="#{i}">{t((fr, en))}</a>' for i, fr, en in TOC)
    rep = {
        '@@BASE_CSS@@': base_css(),
        '@@CSS@@': CSS,
        '@@TAGLINE@@': t(('Du premier raisin domestiqué aux appellations d’origine : 11&nbsp;000 ans d’histoire, de la Chine à la Géorgie, de l’Égypte à la Bourgogne. Uniquement des faits établis : chaque affirmation renvoie à sa source (survolez ou touchez les petits numéros). Les dates et chiffres approximatifs sont marqués « ≈ ».',
                          'From the first domesticated grape to appellations of origin: 11,000 years of history, from China to Georgia, from Egypt to Burgundy. Established facts only: every statement links to its source (hover over or tap the small numbers). Approximate dates and figures are marked “≈”.'), 'p', 'tagline'),
        '@@KEYS@@': keys_html(),
        '@@TOC@@': toc,
        '@@ERAS@@': '\n'.join(ERAS),
        '@@GRAPES_LEAD@@': blk(('Grâce à l’ADN, on connaît aujourd’hui les « parents » de nombreux cépages. Certains sont très anciens et ont donné naissance à des familles entières ; d’autres sont les premiers cépages plantés sur un continent. Voici ceux que la recherche a clairement établis.',
                                'Thanks to DNA, we now know the “parents” of many grape varieties. Some are very old and gave rise to whole families; others were the first grapes planted on a continent. Here are those that research has clearly established.')),
        '@@GRAPES@@': grapes_html(),
        '@@SOURCES@@': sources_html(),
        '@@METHOD@@': t(('Méthode : seules les affirmations appuyées par une publication scientifique, un texte historique ou une institution officielle sont retenues. Quand les sources divergent (dates, attributions), la page le signale. Page rédigée en 2026 · ©&nbsp;2026 Christophe A. Paul.',
                         'Method: only statements supported by a scientific publication, a historical text or an official institution are kept. Where sources disagree (dates, attributions), the page says so. Page written in 2026 · ©&nbsp;2026 Christophe A. Paul.'), 'p', 'method'),
    }
    html = TEMPLATE
    for k, v in rep.items():
        html = html.replace(k, v)
    assert '@@' not in html, html[html.index('@@'):html.index('@@') + 40]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html)
    used = set()
    import re
    for m in re.finditer(r'href="#src-(\d+)"', html):
        used.add(int(m.group(1)))
    unused = [k for k, n in NUM.items() if n not in used]
    print(f'{OUT.relative_to(INFOS.parent)}: {len(html) // 1024} KB, {len(SOURCES)} sources, unused: {unused}')


if __name__ == '__main__':
    main()
