# -*- coding: utf-8 -*-
"""Builds WEB Site/Infos/Crus_Classifications.html — « Les Classifications des Crus » / "Crus & Grands Crus
Classifications". Lists live in data.py; prose is written here (FR + EN). Run: python3 gen_page.py
Native cream/dark CSS (don't run theme_apply.py on the output)."""
import html, re, unicodedata
from pathlib import Path
from data import *

OUT = Path(__file__).resolve().parents[2] / 'Crus_Classifications.html'
PC = '../Plan%20Cadastraux/'


def esc(s): return html.escape(s, quote=True)
def T(fr, en, tag='span', cls=''):
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c} data-fr="{esc(fr)}" data-en="{esc(en)}">{fr}</{tag}>'
def L(fr, en):  # long bilingual blocks, toggled by html[lang]
    return f'<div class="L fr">{fr}</div><div class="L en">{en}</div>'
def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode()
    return re.sub(r'[^A-Za-z0-9]+', '-', s).strip('-')
def plan(path, fr, en):
    return f'<a class="plan" href="{PC}{path}">{T(fr + " →", en + " →")}</a>'
def facts(items):
    return '<div class="facts">' + ''.join(
        f'<div class="fact"><b>{n}</b>{T(fr, en)}</div>' for n, fr, en in items) + '</div>'


def tier(fr, en, rows, cls='', note=''):
    lis = ''.join(f'<li><span class="nm">{esc(n)}</span><span class="cm">{esc(c)}</span></li>' for n, c in rows)
    return (f'<div class="tier {cls}"><div class="tier-h"><h3>{T(fr, en)}</h3><span class="n">{len(rows)}</span></div>'
            f'<ul>{lis}</ul>{note}</div>')


def cb_tier(key, fr, en, cls):
    groups = CB[key]
    n = sum(len(l) for _, l in groups)
    body = ''.join(f'<div class="cbg"><h4>{a} <span>{len(l)}</span></h4><ul>'
                   + ''.join(f'<li>{esc(x)}</li>' for x in l) + '</ul></div>' for a, l in groups)
    return (f'<div class="tier {cls}"><div class="tier-h"><h3>{T(fr, en)}</h3><span class="n">{n}</span></div>'
            f'<div class="cbgs">{body}</div></div>')


def timeline(rows):
    return '<ol class="tl">' + ''.join(
        f'<li><b>{y}</b>{T(fr, en)}</li>' for y, fr, en in rows) + '</ol>'


def sec_head(id_, kick_fr, kick_en, h_fr, h_en, plans=''):
    return (f'<section class="sec" id="{id_}"><div class="sec-head"><div>'
            f'<p class="kick" data-fr="{esc(kick_fr)}" data-en="{esc(kick_en)}">{kick_fr}</p>'
            f'<h2 data-fr="{esc(h_fr)}" data-en="{esc(h_en)}">{h_fr}</h2></div>'
            f'<div class="plans">{plans}</div></div>')


COLR = {'R': ('rouge', 'red'), 'B': ('blanc', 'white'), 'RB': ('rouge & blanc', 'red & white')}
def colour_tag(c):
    fr, en = COLR[c]
    return f'<span class="col c{c}">{T(fr, en)}</span>'



def R(s):  # mini template: {%expr%} evaluated at module level (Python 3.9 f-strings can't nest same quotes)
    return re.sub(r'\{%(.*?)%\}', lambda m: str(eval(m.group(1), globals())), s, flags=re.S)

# ======================================================================================
parts = []

# ---------- intro ----------
parts.append(R("""
<section class="panel intro">
  {%L('''<p>En France, « cru » désigne un vignoble précis et le vin qui en naît. Deux philosophies se partagent les classements.
  <b>À Bordeaux, on classe le château</b> : une marque et une propriété, qui peut acheter ou vendre des parcelles sans perdre son rang
  (1855, Graves, Saint-Émilion, Crus Bourgeois). <b>En Bourgogne, en Alsace et en Champagne, on classe la terre</b> : un climat,
  un lieu-dit ou un village, quel que soit le producteur qui l’exploite. Certains classements sont figés depuis 150 ans,
  d’autres sont révisés tous les cinq ou dix ans.</p>''',
  '''<p>In France a “cru” is a specific vineyard and the wine it gives. Two philosophies share the classifications.
  <b>Bordeaux classifies the château</b>: a brand and an estate, which can buy or sell plots without losing its rank
  (1855, Graves, Saint-Émilion, Crus Bourgeois). <b>Burgundy, Alsace and Champagne classify the land</b>: a climat,
  a lieu-dit or a village, whoever farms it. Some classifications have been frozen for 150 years, others are
  revised every five or ten years.</p>''')%}
  <div class="two">
    <div class="phil"><span class="ph-ic">⌂</span><div>{%T('Le château', 'The château', 'b')%}
      <p>{%T('Bordeaux · 1855 · Graves · Saint-Émilion · Crus Bourgeois', 'Bordeaux · 1855 · Graves · Saint-Émilion · Crus Bourgeois')%}</p></div></div>
    <div class="phil"><span class="ph-ic">▦</span><div>{%T('Le terroir', 'The land', 'b')%}
      <p>{%T('Bourgogne (climats) · Alsace (lieux-dits) · Champagne (villages)', 'Burgundy (climats) · Alsace (lieux-dits) · Champagne (villages)')%}</p></div></div>
  </div>
</section>"""))

# ---------- 1855 Médoc ----------
m_tiers = ''.join(tier(fr, en, rows, cls=f't{i+1}') for i, (fr, en, rows) in enumerate(M1855))
parts.append(sec_head('medoc-1855', 'Bordeaux · Rive gauche', 'Bordeaux · Left Bank',
                      'Le classement de 1855 — Médoc', 'The 1855 Classification — Médoc',
                      plan('Bordeaux_LeftBank/Pauillac.html', 'Pauillac', 'Pauillac')
                      + plan('Bordeaux_LeftBank/Margaux.html', 'Margaux', 'Margaux')
                      + plan('Bordeaux_LeftBank/Saint-Julien.html', 'Saint-Julien', 'Saint-Julien')
                      + plan('Bordeaux_LeftBank/Saint-Estephe.html', 'Saint-Estèphe', 'Saint-Estèphe')) + R("""
  {%facts([('61', 'crus classés rouges', 'classified red wines'), ('5', 'niveaux', 'tiers'),
          ('1855', 'Exposition universelle de Paris', 'Paris World Fair'), ('3', 'changements en 170 ans', 'changes in 170 years')])%}
  <div class="panel prose">
  {%L('''<p>Pour l’Exposition universelle de Paris de 1855, Napoléon III veut présenter les meilleurs vins de France.
  La Chambre de commerce de Bordeaux confie la tâche aux <b>courtiers</b> de la place, qui classent les crus
  d’après leur réputation et surtout <b>le prix auquel ils se vendaient depuis des décennies</b>. Le résultat, publié le
  18 avril 1855, compte 58 rouges (tous du Médoc, sauf Haut-Brion, dans les Graves) répartis en cinq crus, et 21 blancs
  liquoreux de Sauternes et Barsac. Conçu comme une liste de circonstance, il est devenu le classement de vin le plus
  célèbre au monde — et n’a presque jamais bougé.</p>''',
  '''<p>For the 1855 Paris Exposition Universelle, Napoleon III wanted to show off France’s finest wines. The Bordeaux
  Chamber of Commerce handed the job to the city’s <b>wine brokers</b>, who ranked the estates by reputation and above all by
  <b>the prices they had fetched for decades</b>. The result, published on 18 April 1855, listed 58 reds (all from the Médoc
  except Haut-Brion, in the Graves) in five growths, and 21 sweet whites from Sauternes and Barsac. Meant as a one-off list,
  it became the world’s most famous wine classification — and has barely moved since.</p>''')%}
  <h3 class="sub-h">{%T('Les trois changements', 'The three changes')%}</h3>
  <div class="changes">
    <div class="chg"><span class="num">1</span><b>1856</b>
      {%L('<p><b>Château Cantemerle</b> (Macau, Haut-Médoc) est ajouté comme cinquième cru, un an après la publication : son propriétaire avait obtenu qu’on répare son oubli.</p>',
         '<p><b>Château Cantemerle</b> (Macau, Haut-Médoc) is added as a fifth growth a year after publication, its owner having had the omission put right.</p>')%}</div>
    <div class="chg"><span class="num">2</span><b>≈ 1900</b>
      {%L('<p><b>Château Dubignon</b>, troisième cru de Margaux, disparaît : ses vignes sont absorbées par Château Malescot Saint-Exupéry au tournant du XX<sup>e</sup> siècle. Le classement passe ainsi de 62 à 61 crus.</p>',
         '<p><b>Château Dubignon</b>, a Margaux third growth, disappears: its vines were absorbed into Château Malescot Saint-Exupéry around the turn of the 20th century. The list thus goes from 62 to 61 growths.</p>')%}</div>
    <div class="chg"><span class="num">3</span><b>1973</b>
      {%L('<p><b>Château Mouton Rothschild</b>, deuxième cru en 1855, est promu premier cru par arrêté ministériel après cinquante ans de campagne du baron Philippe de Rothschild. La devise « Premier ne puis, second ne daigne, Mouton suis » devient « Premier je suis, second je fus, Mouton ne change ». Seule révision officielle du classement.</p>',
         '<p><b>Château Mouton Rothschild</b>, a second growth in 1855, is promoted to first growth by ministerial decree after Baron Philippe de Rothschild’s fifty-year campaign. The motto “First I cannot be, second I do not deign to be, Mouton I am” becomes “First I am, second I was, Mouton does not change”. The only official revision of the classification.</p>')%}</div>
  </div>
  {%L('<p class="small">Les autres différences avec 1855 sont des partages ou des changements de nom (les Léoville, les Pichon, d’Armailhac — ex-Mouton d’Armailhacq, Mouton Baron Philippe puis Mouton Baronne Philippe —, Marquis d’Alesme-Becker devenu Marquis d’Alesme…). Les vignobles ont souvent beaucoup changé de taille : c’est le château qui est classé, pas ses parcelles.</p>',
     '<p class="small">Other differences from 1855 are splits or name changes (the Léovilles, the Pichons, d’Armailhac — formerly Mouton d’Armailhacq, then Mouton Baron Philippe and Mouton Baronne Philippe —, Marquis d’Alesme-Becker now Marquis d’Alesme…). Vineyards have often changed size a great deal: it is the château that is classified, not its plots.</p>')%}
  </div>
  <div class="tiers t5">{%m_tiers%}</div>
</section>"""))

# ---------- 1855 Sauternes ----------
s_tiers = ''.join(tier(fr, en, rows, cls=f's{i+1}') for i, (fr, en, rows) in enumerate(S1855))
parts.append(sec_head('sauternes-1855', 'Bordeaux · Vins liquoreux', 'Bordeaux · Sweet wines',
                      'Le classement de 1855 — Sauternes & Barsac', 'The 1855 Classification — Sauternes & Barsac',
                      plan('Bordeaux_LeftBank/Sauternes.html', 'Sauternes', 'Sauternes')
                      + plan('Bordeaux_LeftBank/Barsac.html', 'Barsac', 'Barsac')) + R("""
  {%facts([('27', 'crus classés', 'classified growths'), ('1', 'premier cru supérieur', 'superior first growth'),
          ('11', 'premiers crus', 'first growths'), ('15', 'deuxièmes crus', 'second growths')])%}
  <div class="panel prose">
  {%L('''<p>Les blancs liquoreux de Sauternes, Barsac, Bommes, Fargues et Preignac sont classés le même jour que les rouges. Un rang
  unique est créé pour <b>Château d’Yquem</b>, seul <b>premier cru supérieur</b>, tant ses prix dépassaient ceux de tous les autres.
  Les 21 crus d’origine sont devenus 27 au fil des partages de propriétés (Rabaud, Doisy, Lamothe, Romer…) ; aucun cru n’a été
  ajouté ou promu.</p>''',
  '''<p>The sweet whites of Sauternes, Barsac, Bommes, Fargues and Preignac were classified the same day as the reds. A unique rank
  was created for <b>Château d’Yquem</b>, the only <b>premier cru supérieur</b>, so far above everyone else were its prices.
  The 21 original growths have become 27 as estates were divided (Rabaud, Doisy, Lamothe, Romer…); none has been added or promoted.</p>''')%}
  </div>
  <div class="tiers t3">{%s_tiers%}</div>
</section>"""))

# ---------- Graves 1959 ----------
g_rows = ''.join(f'<li><span class="nm">{esc(n)}</span><span class="cm">{esc(c)}</span>{colour_tag(col)}</li>' for n, c, col in GRAVES)
parts.append(sec_head('graves-1959', 'Bordeaux · Pessac-Léognan', 'Bordeaux · Pessac-Léognan',
                      'Les crus classés de Graves — 1953 · 1959', 'The Graves Classification — 1953 · 1959',
                      plan('Bordeaux_LeftBank/Pessac-Leognan.html', 'Pessac-Léognan', 'Pessac-Léognan')) + R("""
  {%facts([('16', 'châteaux', 'châteaux'), ('13', 'classés en rouge', 'classified for red'),
          ('9', 'classés en blanc', 'classified for white'), ('0', 'hiérarchie', 'ranking')])%}
  <div class="two-col">
  <div class="panel prose">
  {%L('''<p>En 1855, seul <b>Haut-Brion</b> représentait les Graves. Les producteurs voisins obtiennent leur propre classement,
  établi par l’INAO : les <b>rouges en 1953</b>, puis les <b>blancs en 1959</b>, année où la liste complète est homologuée.
  Il n’y a <b>aucune hiérarchie</b> : chaque château porte simplement la mention « cru classé de Graves », pour son rouge,
  son blanc ou les deux. Haut-Brion figure dans les deux classements, mais seulement pour son rouge : ses propriétaires
  n’ont pas présenté le blanc, jugeant sa production trop confidentielle.</p>
  <p>Aucune révision n’a eu lieu ni n’est prévue. Depuis la création de l’AOC <b>Pessac-Léognan</b> en 1987, les seize
  châteaux se trouvent tous dans cette appellation.</p>''',
  '''<p>In 1855 only <b>Haut-Brion</b> represented the Graves. Its neighbours won a classification of their own, drawn up by
  the INAO: <b>reds in 1953</b>, then <b>whites in 1959</b>, when the full list was ratified. There is <b>no ranking</b>: each
  château simply carries “cru classé de Graves”, for its red, its white, or both. Haut-Brion appears in both classifications,
  but for its red only: the owners did not submit the white, which they felt was made in too small a quantity.</p>
  <p>No revision has taken place or is planned. Since the <b>Pessac-Léognan</b> AOC was created in 1987, all sixteen
  châteaux lie within it.</p>''')%}
  {%L('<p class="small">¹ La Tour Haut-Brion est intégré à La Mission Haut-Brion depuis le millésime 2005. ² Laville Haut-Brion est vendu sous le nom La Mission Haut-Brion blanc depuis 2009.</p>',
     '<p class="small">¹ La Tour Haut-Brion has been part of La Mission Haut-Brion since the 2005 vintage. ² Laville Haut-Brion has been sold as La Mission Haut-Brion blanc since 2009.</p>')%}
  </div>
  <div class="tier graves"><div class="tier-h"><h3>{%T('Crus classés de Graves', 'Classified growths of Graves')%}</h3><span class="n">16</span></div><ul>{%g_rows%}</ul></div>
  </div>
</section>"""))

# ---------- Saint-Émilion 2022 ----------
def se_li(n, pre='Château '):
    new = n in SE_NEW
    full = n if n.startswith(('Clos', 'Couvent', 'Lassègue')) else pre + n
    return f'<li class="{"new" if new else ""}">{esc(full)}</li>'
parts.append(sec_head('saint-emilion', 'Bordeaux · Rive droite', 'Bordeaux · Right Bank',
                      'Le classement de Saint-Émilion — 2022', 'The Saint-Émilion Classification — 2022',
                      plan('Bordeaux_RightBank/Saint-Emilion.html', 'Saint-Émilion', 'Saint-Émilion')) + R("""
  {%facts([('85', 'crus classés', 'classified estates'), ('2', 'premiers grands crus classés A', 'premiers grands crus classés A'),
          ('12', 'premiers grands crus classés B', 'premiers grands crus classés B'), ('71', 'grands crus classés', 'grands crus classés')])%}
  <div class="panel prose">
  {%L('''<p>Créé en <b>1955</b> pour l’AOC Saint-Émilion grand cru, c’est le seul grand classement bordelais <b>révisé tous les dix ans</b> :
  1969, 1986, 1996, 2006 (annulé par la justice), 2012 et <b>2022</b>. Les candidats sont notés par dégustation de plusieurs millésimes
  (la moitié de la note, quel que soit le niveau), réputation, terroir et conduite du domaine.
  La liste 2022 a été approuvée par l’INAO le 8 septembre 2022.</p>
  <p>Cette édition a été marquée par le départ de trois piliers : <b>Cheval Blanc</b> et <b>Ausone</b> (2021), puis <b>Angélus</b> (2022)
  ont retiré leur candidature, jugeant que les critères faisaient trop de place à la notoriété, à l’œnotourisme et aux médias
  au détriment du vin et du terroir. <b>La Gaffelière</b> ne s’est pas non plus représenté. <b>Figeac</b> rejoint Pavie au rang
  « A » ; seize domaines font leur entrée parmi les grands crus classés. Prochaine révision attendue vers 2032.</p>''',
  '''<p>Created in <b>1955</b> for the Saint-Émilion grand cru AOC, it is the only major Bordeaux classification <b>revised every ten
  years</b>: 1969, 1986, 1996, 2006 (struck down in court), 2012 and <b>2022</b>. Candidates are scored on a tasting of several vintages
  (half the mark, whatever the level), reputation, terroir and estate management. The 2022
  list was approved by the INAO on 8 September 2022.</p>
  <p>This edition saw three pillars leave: <b>Cheval Blanc</b> and <b>Ausone</b> (2021), then <b>Angélus</b> (2022) withdrew,
  arguing the criteria gave too much weight to reputation, wine tourism and media at the expense of the wine and the land.
  <b>La Gaffelière</b> did not reapply either. <b>Figeac</b> joins Pavie at “A” level; sixteen estates are new among the grands
  crus classés. The next revision is expected around 2032.</p>''')%}
  </div>
  <div class="tiers se">
    <div class="tier t1"><div class="tier-h"><h3>{%T('Premiers grands crus classés « A »', 'Premiers grands crus classés “A”')%}</h3><span class="n">2</span></div>
      <ul>{%''.join(f'<li>{esc(n)}</li>' for n in SE_A)%}</ul>
      {%L('<p class="small">En 2012 : Angélus, Ausone, Cheval Blanc, Pavie.</p>', '<p class="small">In 2012: Angélus, Ausone, Cheval Blanc, Pavie.</p>')%}</div>
    <div class="tier t2"><div class="tier-h"><h3>{%T('Premiers grands crus classés « B »', 'Premiers grands crus classés “B”')%}</h3><span class="n">12</span></div>
      <ul>{%''.join(f'<li>{esc(n)}</li>' for n in SE_B)%}</ul></div>
    <div class="tier t3 wide"><div class="tier-h"><h3>{%T('Grands crus classés', 'Grands crus classés')%}</h3><span class="n">71</span></div>
      <ul class="cols">{%''.join(se_li(n) for n in SE_GCC)%}</ul>
      <p class="small legend"><i class="dot"></i>{%T('nouveau ou réintégré en 2022', 'new or reinstated in 2022')%}</p></div>
  </div>
</section>"""))

# ---------- Crus Bourgeois 2025 ----------
cb_by_aoc = {}
for k in ('exc', 'sup', 'cb'):
    for a, l in CB[k]:
        cb_by_aoc[a] = cb_by_aoc.get(a, 0) + len(l)
aoc_bar = ''.join(f'<div class="bar"><span>{a}</span><i style="width:{n/91*100:.1f}%"></i><b>{n}</b></div>'
                  for a, n in sorted(cb_by_aoc.items(), key=lambda x: -x[1]))
parts.append(sec_head('crus-bourgeois', 'Bordeaux · Médoc', 'Bordeaux · Médoc',
                      'Les Crus Bourgeois du Médoc — 2025', 'Crus Bourgeois du Médoc — 2025',
                      plan('Bordeaux_LeftBank/Medoc.html', 'Médoc', 'Médoc')
                      + plan('Bordeaux_LeftBank/Haut-Medoc.html', 'Haut-Médoc', 'Haut-Médoc')) + R("""
  {%facts([('170', 'châteaux classés', 'classified châteaux'), ('14', 'exceptionnels', 'exceptionnels'),
          ('36', 'supérieurs', 'supérieurs'), ('120', 'crus bourgeois', 'crus bourgeois'), ('5', 'ans de validité', 'years of validity')])%}
  <div class="two-col">
  <div class="panel prose">
  {%L('''<p>Le nom remonte au Moyen Âge : sous la domination anglaise (1152-1453), les <b>bourgeois</b> de Bordeaux — marchands
  et artisans du « bourg » — étaient exemptés de taxes sur la vente de leurs vins. Ce privilège leur permit d’acheter dès le
  XV<sup>e</sup> siècle les meilleures terres du Médoc, bientôt appelées « crus des bourgeois ».</p>
  <p>Le classement actuel est <b>quinquennal</b> : les châteaux sont jugés sur dégustation de plusieurs millésimes, et pour
  les niveaux Supérieur et Exceptionnel sur un dossier et une visite (conduite du vignoble, environnement, accueil). Le
  classement 2025, dévoilé le 10 février 2025 à Wine Paris, compte <b>170 châteaux</b> contre 249 en 2020 ; répartis dans six appellations du Médoc. Le prochain est prévu en 2030.</p>''',
  '''<p>The name goes back to the Middle Ages: under English rule (1152-1453) the <b>bourgeois</b> of Bordeaux — the merchants
  and craftsmen of the “bourg” — were exempt from tax on the sale of their wines. That privilege let them buy the best land in
  the Médoc from the 15th century on, soon known as the “crus des bourgeois”.</p>
  <p>Today’s classification is renewed <b>every five years</b>: châteaux are judged by tasting several vintages and, for the
  Supérieur and Exceptionnel levels, on a written file and a site visit (vineyard practice, environment, hospitality). The 2025
  classification, unveiled at Wine Paris on 10 February 2025, holds <b>170 châteaux</b> against 249 in 2020, spread over six Médoc appellations. The next is due in 2030.</p>''')%}
  </div>
  <div class="panel aocs"><h3 class="sub-h">{%T('Par appellation', 'By appellation')%}</h3>{%aoc_bar%}</div>
  </div>
  <h3 class="sub-h">{%T('Une longue histoire', 'A long history')%}</h3>
  {%timeline([
    ('1740', 'La Chambre de commerce de Bordeaux établit un premier relevé des prix des crus bourgeois.',
             'The Bordeaux Chamber of Commerce draws up a first record of crus bourgeois prices.'),
    ('1858', 'M. d’Armailhac publie un ouvrage qui répartit officieusement 248 crus bourgeois en trois catégories.',
             'M. d’Armailhac publishes a book that unofficially ranks 248 crus bourgeois in three categories.'),
    ('1932', 'Chambre de commerce et Chambre d’agriculture de la Gironde recensent 444 crus bourgeois ; jamais homologuée, la liste fera référence pendant des décennies.',
             'The Chamber of Commerce and the Gironde Chamber of Agriculture list 444 crus bourgeois; never ratified, it stays the reference for decades.'),
    ('1962', 'Naissance du Syndicat des Crus Bourgeois du Médoc.', 'The Syndicat des Crus Bourgeois du Médoc is founded.'),
    ('1979', 'La mention traditionnelle « cru bourgeois » est reconnue par la réglementation européenne.',
             'The traditional term “cru bourgeois” is recognised by European labelling rules.'),
    ('2003', 'Premier classement officiel : 247 châteaux sur 490 candidats (9 exceptionnels, 87 supérieurs, 151 crus bourgeois).',
             'First official classification: 247 châteaux out of 490 candidates (9 exceptionnels, 87 supérieurs, 151 crus bourgeois).'),
    ('2007', 'La cour administrative d’appel de Bordeaux l’annule : le jury comptait des membres du syndicat — « on ne peut être juge et partie ».',
             'The Bordeaux administrative appeal court strikes it down: the jury included members of the syndicate — “one cannot be both judge and party”.'),
    ('2010', 'Une « Sélection officielle » annuelle, sans niveaux, remplace le classement (millésimes 2008 à 2017).',
             'An annual “Official Selection” without tiers replaces it (vintages 2008 to 2017).'),
    ('2020', 'Premier classement quinquennal : 249 châteaux, les trois niveaux sont rétablis.',
             'First five-year classification: 249 châteaux, the three tiers are restored.'),
    ('2025', 'Deuxième classement quinquennal : 170 châteaux (14 / 36 / 120).',
             'Second five-year classification: 170 châteaux (14 / 36 / 120).'),
  ])%}
  <p class="note-top">{%T('Les noms sont donnés sans le mot « Château ».', 'Names are given without the word “Château”.')%}</p>
  <div class="tiers cb">
    {%cb_tier('exc', 'Crus Bourgeois Exceptionnels', 'Crus Bourgeois Exceptionnels', 't1 wide')%}
    {%cb_tier('sup', 'Crus Bourgeois Supérieurs', 'Crus Bourgeois Supérieurs', 't2 wide')%}
    {%cb_tier('cb', 'Crus Bourgeois', 'Crus Bourgeois', 't3 wide')%}
  </div>
</section>"""))

# ---------- Crus Artisans 2023 ----------
ca_n = sum(len(l) for _, l in CA)
ca_body = ''.join('<div class="cbg"><h4>' + a + ' <span>' + str(len(l)) + '</span></h4><ul>'
                  + ''.join('<li>' + esc(x) + '</li>' for x in l) + '</ul></div>' for a, l in CA)
ca_tl = timeline([
    ('XIXᵉ', 'Les artisans médocains (tonneliers, forgerons…) exploitent leurs propres petites vignes.',
             'Médoc artisans (coopers, blacksmiths…) farm small vineyards of their own.'),
    ('1994', 'La mention « cru artisan » est reconnue par la réglementation européenne.',
             'The term “cru artisan” is recognised by EU rules.'),
    ('2006', 'Premier classement officiel : 44 crus (arrêté publié au JO du 11 janvier 2006).',
             'First official classification: 44 crus (decree in the Journal Officiel, 11 January 2006).'),
    ('2018', '36 crus, millésimes 2017-2021.', '36 crus, vintages 2017-2021.'),
    ('2023', '33 crus, dont 6 nouveaux, millésimes 2022-2026.', '33 crus, 6 of them new, vintages 2022-2026.'),
])
ca_txt = L('''<p>Le terme est presque aussi ancien que le classement de 1855 : au XIX<sup>e</sup> siècle, les <b>artisans</b> du Médoc —
  tonneliers, forgerons, charrons, maçons… — possédaient souvent une petite vigne dont ils vendaient le vin. Aujourd’hui, un
  cru artisan est une <b>petite propriété familiale</b> où le vigneron cultive, vinifie, élève et commercialise lui-même son vin,
  au château.</p>
  <p>La mention est reconnue par l’Union européenne en 1994 et le premier classement officiel est homologué en <b>2006</b>
  (44 propriétés). Il est désormais <b>révisé tous les cinq ans</b> par un organisme indépendant (Qualisud), sur dégustation
  et contrôle du cahier des charges : 36 crus en 2018, puis <b>33 en 2023</b> (arrêté du 21 octobre 2022), valable pour les
  millésimes 2022 à 2026. Château Moutte Blanc est classé pour son Haut-Médoc et pour son Margaux.</p>''',
  '''<p>The term is almost as old as the 1855 Classification: in the 19th century the Médoc’s <b>artisans</b> — coopers,
  blacksmiths, wheelwrights, masons… — often owned a small vineyard and sold its wine. Today a cru artisan is a <b>small family
  estate</b> where the grower farms, makes, ages and sells the wine themselves, at the property.</p>
  <p>The term was recognised by the European Union in 1994 and the first official classification was ratified in <b>2006</b>
  (44 estates). It is now <b>revised every five years</b> by an independent body (Qualisud), through tasting and checks against
  the specifications: 36 crus in 2018, then <b>33 in 2023</b> (decree of 21 October 2022), valid for the 2022 to 2026 vintages.
  Château Moutte Blanc is classified for both its Haut-Médoc and its Margaux.</p>''')
parts.append(sec_head('crus-artisans', 'Bordeaux · Médoc', 'Bordeaux · Médoc',
                      'Les Crus Artisans du Médoc — 2023', 'Crus Artisans du Médoc — 2023',
                      plan('Bordeaux_LeftBank/Medoc.html', 'Médoc', 'Médoc')
                      + plan('Bordeaux_LeftBank/Margaux.html', 'Margaux', 'Margaux'))
    + facts([('33', 'crus artisans', 'crus artisans'), ('32', 'châteaux', 'châteaux'),
             ('6', 'appellations', 'appellations'), ('2022–26', 'millésimes couverts', 'vintages covered')])
    + '<div class="two-col"><div class="panel prose">' + ca_txt + '</div><div class="panel">' + ca_tl + '</div></div>'
    + '<p class="note-top">' + T('Les noms sont donnés sans le mot « Château ».', 'Names are given without the word “Château”.') + '</p>'
    + '<div class="tiers cb"><div class="tier t2 wide"><div class="tier-h"><h3>' + T('Crus Artisans du Médoc', 'Crus Artisans du Médoc')
    + '</h3><span class="n">' + str(ca_n) + '</span></div><div class="cbgs">' + ca_body + '</div></div></div></section>')

# ---------- Burgundy ----------
def bgc_group(fr, en, rows, extra=''):
    return (f'<div class="tier"><div class="tier-h"><h3>{T(fr, en)}</h3><span class="n">{len(rows)}</span></div><ul>'
            + ''.join(f'<li><span class="nm">{esc(n)}</span><span class="cm">{esc(c)}</span>{colour_tag(col)}</li>' for n, c, col in rows)
            + '</ul>' + extra + '</div>')
MOUTONNE = ('<div class="moutonne"><div class="mt-h"><span class="nm">La Moutonne</span>'
    + T('l’exception · monopole', 'the exception · monopole', cls='mt-tag') + '</div>'
    + L('<p>Ce n’est pas l’un des sept climats officiels : ses 2,35 ha sont à cheval sur <b>Vaudésir</b> (≈ 95 %) et <b>Les Preuses</b> (≈ 5 %). '
        'Ancienne vigne des moines de l’abbaye de Pontigny, elle appartient en entier au <b>Domaine Long-Depaquit</b> (Albert Bichot). '
        'Absente du cadastre lors de la délimitation de 1938, elle n’a jamais été classée comme climat, mais l’INAO autorise depuis 1952 '
        'son nom d’usage séculaire : le domaine est le seul à pouvoir étiqueter « Moutonne » avec la mention Chablis grand cru.</p>',
        '<p>It is not one of the seven official climats: its 2.35 ha straddle <b>Vaudésir</b> (≈ 95 %) and <b>Les Preuses</b> (≈ 5 %). '
        'Once a vineyard of the monks of Pontigny Abbey, it is wholly owned by <b>Domaine Long-Depaquit</b> (Albert Bichot). '
        'Missing from the land register when the appellation was delimited in 1938, it was never classified as a climat, but since 1952 '
        'the INAO has allowed its centuries-old name: the estate alone may label “Moutonne” together with Chablis grand cru.</p>')
    + '<!--@MOUTONNE_LINK@-->'
    + '</div>')
from pyr_svg import svg as _pyr_svg  # one true triangle, four bands
pyr_html = _pyr_svg()
parts.append(sec_head('bourgogne', 'Bourgogne · Le terroir classé', 'Burgundy · Classified land',
                      'Les climats de Bourgogne', 'The Climats of Burgundy',
                      f'<a class="plan" href="../Bourgogne%20Regions/Cote-d_Or.html">{T("Carte de la Côte-d’Or →", "Côte-d’Or map →")}</a>'
                      f'<a class="plan" href="../Bourgogne%20Regions/Chablis_et_de_l_Auxerrois.html">{T("Chablis →", "Chablis →")}</a>') + R("""
  <div class="two-col">
  <div class="panel prose">
  {%L('''<p>En Bourgogne, on ne classe pas des domaines mais des <b>climats</b> : des parcelles délimitées depuis des siècles
  par les moines de Cîteaux et de Cluny, puis par les vignerons. Un même climat est souvent partagé entre des dizaines de
  propriétaires — le Clos de Vougeot en compte plus de 80. La hiérarchie a quatre niveaux, inscrits dans les appellations
  elles-mêmes : <b>régionale</b> (Bourgogne), <b>village</b> (Gevrey-Chambertin), <b>premier cru</b> (Gevrey-Chambertin 1<sup>er</sup> cru
  Clos Saint-Jacques) et <b>grand cru</b>, qui ne porte que le nom du climat (Chambertin).</p>''',
  '''<p>Burgundy classifies <b>climats</b>, not estates: plots mapped over centuries by the monks of Cîteaux and Cluny, then by the
  growers. One climat is often shared by dozens of owners — Clos de Vougeot has more than 80. The hierarchy has four levels,
  built into the appellations themselves: <b>regional</b> (Bourgogne), <b>village</b> (Gevrey-Chambertin), <b>premier cru</b>
  (Gevrey-Chambertin 1<sup>er</sup> cru Clos Saint-Jacques) and <b>grand cru</b>, which bears only the climat’s name (Chambertin).</p>''')%}
  {%timeline([
    ('1855', 'Le Dr Jules Lavalle publie l’<i>Histoire et statistique de la vigne et des grands vins de la Côte-d’Or</i>, qui hiérarchise les climats.',
             'Dr Jules Lavalle publishes his <i>History and statistics of the vine and great wines of the Côte-d’Or</i>, ranking the climats.'),
    ('1861', 'Le Comité d’agriculture de Beaune en tire un classement officiel (têtes de cuvée, 1<sup>res</sup>, 2<sup>es</sup>, 3<sup>es</sup> cuvées).',
             'The Beaune Agricultural Committee turns it into an official ranking (têtes de cuvée, 1st, 2nd, 3rd cuvées).'),
    ('1936-37', 'Premières AOC : les grands crus de la Côte d’Or sont reconnus comme appellations à part entière.',
                'First AOCs: the Côte d’Or grands crus become appellations in their own right.'),
    ('1938', 'Chablis grand cru (une AOC, sept climats).', 'Chablis grand cru (one AOC, seven climats).'),
    ('1943', 'Les premiers crus sont délimités et inscrits dans les appellations villages.',
             'Premiers crus are delimited and written into the village appellations.'),
    ('1992', 'La Grande Rue (Vosne-Romanée) devient le dernier grand cru reconnu.',
             'La Grande Rue (Vosne-Romanée) becomes the most recent grand cru.'),
    ('2015', 'Les « Climats du vignoble de Bourgogne » (1 247 climats) sont inscrits au patrimoine mondial de l’UNESCO.',
             'The “Climats of the Burgundy vineyard” (1,247 climats) are inscribed as a UNESCO World Heritage Site.'),
    ('2020', '<b>Pouilly-Fuissé</b> obtient 22 premiers crus, les premiers du Mâconnais ; suivront Pouilly-Vinzelles (3) et Pouilly-Loché (1).',
             '<b>Pouilly-Fuissé</b> gains 22 premiers crus, the first in the Mâconnais; Pouilly-Vinzelles (3) and Pouilly-Loché (1) follow.'),
  ])%}
  </div>
  <div class="panel">{%pyr_html%}</div>
  </div>
  <h3 class="sub-h">{%T('Les 33 grands crus', 'The 33 grands crus')%}</h3>
  <div class="tiers bgc">{%bgc_group(*BGC[1]) + '<div class="bstack">' + bgc_group(*BGC[0], extra=MOUTONNE) + bgc_group(*BGC[2]) + '</div>'%}</div>
  {%L('<p class="small">Mazoyères-Chambertin peut aussi être vendu sous le nom de Charmes-Chambertin ; Charlemagne n’est quasiment jamais revendiqué (vendu en Corton-Charlemagne). Les grands crus ne représentent qu’environ 1 % de la production bourguignonne.</p>',
     '<p class="small">Mazoyères-Chambertin may also be sold as Charmes-Chambertin; Charlemagne is hardly ever used (sold as Corton-Charlemagne). Grands crus make up only about 1 % of Burgundy’s production.</p>')%}
</section>"""))

# ---------- Alsace ----------
agc = ''.join(f'<a class="chip{" red" if n in AGC_RED else ""}" href="{PC}Alsace_Grands_Crus/{slug(n)}.html">{esc(n)}</a>' for n in AGC)
parts.append(sec_head('alsace', 'Alsace · Les lieux-dits', 'Alsace · The lieux-dits',
                      'Les grands crus d’Alsace', 'The Alsace Grands Crus',
                      plan('Alsace_Grands_Crus/Alsace-Grands-Crus.html', 'Les 51 plans', 'All 51 maps')
                      + '<a class="plan" href="../Alsace.html">' + T('Carte de l’Alsace →', 'Alsace map →') + '</a>') + R("""
  {%facts([('51', 'AOC grand cru', 'grand cru AOCs'), ('≈ 1 700', 'hectares', 'hectares'), ('4 %', 'de la production', 'of production'),
          ('13', 'dénominations communales', 'communal denominations')])%}
  <div class="two-col">
  <div class="panel prose">
  {%L('''<p>L’Alsace classe ses meilleurs <b>lieux-dits</b>, coteaux délimités au cadastre. Un grand cru est en principe planté
  des quatre cépages « nobles » — <b>riesling, pinot gris, gewurztraminer et muscat</b> — avec des exceptions locales
  (sylvaner au Zotzenberg, assemblages à l’Altenberg de Bergheim et au Kaefferkopf). Rendement : 50 hl/ha.
  Depuis 2022, le <b>pinot noir</b> peut aussi y être grand cru (rouge) : Hengst et Kirchberg de Barr, puis Vorbourg en 2025.</p>
  <p>Entre l’AOC Alsace et les grands crus, une étape intermédiaire se construit : 13 <b>dénominations géographiques</b>
  (Alsace Bergheim, Vallée Noble, Côte de Rouffach…), et un futur niveau <b>premier cru</b> pour les lieux-dits :
  en juin 2025, l’INAO a adopté la grille d’instruction et sept premiers dossiers sont à l’étude.</p>''',
  '''<p>Alsace classifies its best <b>lieux-dits</b>, slopes delimited on the land register. A grand cru is in principle planted
  with the four “noble” grapes — <b>riesling, pinot gris, gewurztraminer and muscat</b> — with local exceptions (sylvaner in
  Zotzenberg, blends in Altenberg de Bergheim and Kaefferkopf). Yield: 50 hl/ha. Since 2022 <b>pinot noir</b> can be a (red)
  grand cru too: Hengst and Kirchberg de Barr, then Vorbourg in 2025.</p>
  <p>Between AOC Alsace and the grands crus a middle tier is taking shape: 13 <b>geographical denominations</b> (Alsace Bergheim,
  Vallée Noble, Côte de Rouffach…), and a future <b>premier cru</b> level for lieux-dits: in June 2025 the INAO
  adopted the assessment framework and seven first applications are under review.</p>''')%}
  </div>
  <div class="panel">{%timeline([
    ('1962', 'AOC Alsace.', 'AOC Alsace.'),
    ('1975', 'Création de l’AOC Alsace grand cru ; le Schlossberg est le premier délimité.', 'The Alsace grand cru AOC is created; Schlossberg is the first delimited.'),
    ('1983', '25 lieux-dits délimités.', '25 lieux-dits delimited.'),
    ('1992', '25 de plus : 50 grands crus.', '25 more: 50 grands crus.'),
    ('2007', 'Le Kaefferkopf devient le 51<sup>e</sup>.', 'Kaefferkopf becomes the 51st.'),
    ('2011', 'Chaque grand cru devient une AOC à part entière ; premières dénominations communales.', 'Each grand cru becomes an AOC of its own; first communal denominations.'),
    ('2022', 'Grands crus rouges : Hengst, Kirchberg de Barr.', 'Red grands crus: Hengst, Kirchberg de Barr.'),
    ('2025', 'Vorbourg rouge ; cadre INAO pour les futurs premiers crus.', 'Red Vorbourg; INAO framework for future premiers crus.'),
  ])%}</div>
  </div>
  <h3 class="sub-h">{%T('Les 51 grands crus', 'The 51 grands crus')%} <span class="hint">{%T('— cliquez pour le plan cadastral', '— click for the parcel map')%}</span></h3>
  <div class="chips">{%agc%}</div>
  <p class="small legend"><i class="dot red"></i>{%T('grand cru autorisé aussi en pinot noir (rouge)', 'grand cru also allowed for pinot noir (red)')%}</p>
</section>"""))

# ---------- Champagne ----------
cgc = ''.join(f'<a class="chip{" y85" if n in CGC_1985 else ""}" href="{PC}Champagne_Grands_Crus/{"Ay" if n == "Aÿ" else slug(n)}.html">{esc(n)}</a>' for n in CGC)
cpc = ''.join(f'<span class="chip pc">{esc(n)}</span>' for n in CPC)
parts.append(sec_head('champagne', 'Champagne · Les villages', 'Champagne · The villages',
                      'L’échelle des crus de Champagne', 'The Champagne Échelle des Crus',
                      plan('Champagne_Grands_Crus/Champagne-Grands-Crus.html', 'Les 17 plans', 'All 17 maps')
                      + '<a class="plan" href="../Champagne.html">' + T('Carte de la Champagne →', 'Champagne map →') + '</a>') + R("""
  {%facts([('17', 'villages grands crus', 'grand cru villages'), ('42', 'villages premiers crus', 'premier cru villages'),
          ('≈ 320', 'crus (communes)', 'crus (villages)'), ('100 %', 'note d’un grand cru', 'a grand cru’s rating')])%}
  <div class="two-col">
  <div class="panel prose">
  {%L('''<p>En Champagne, c’est le <b>village</b> entier qui est classé. Après les émeutes vigneronnes de 1911, l’interprofession
  met en place l’<b>échelle des crus</b> : chaque commune reçoit un pourcentage qui fixe le prix de son raisin. Les villages à
  <b>100 %</b> sont grands crus, ceux de <b>90 à 99 %</b> premiers crus ; les autres se situaient jusqu’à 80 %.</p>
  <p>À l’origine, douze villages étaient à 100 % ; <b>en 1985</b>, Chouilly, Le Mesnil-sur-Oger, Oger, Oiry et Verzy
  les rejoignent : 17 grands crus. Le système de prix a été abandonné, et l’échelle elle-même supprimée en 2010, mais les
  mentions « grand cru » et « premier cru » restent inscrites dans le cahier des charges pour les vins issus exclusivement
  de ces villages.</p>''',
  '''<p>In Champagne the whole <b>village</b> is classified. After the growers’ riots of 1911 the trade set up the <b>échelle des
  crus</b> (“ladder of growths”): each village was given a percentage that set the price of its grapes. Villages rated <b>100 %</b>
  are grands crus, those at <b>90–99 %</b> premiers crus; the rest went down to 80 %.</p>
  <p>Twelve villages were originally rated 100 %; <b>in 1985</b> Chouilly, Le Mesnil-sur-Oger, Oger, Oiry and Verzy joined them,
  making 17 grands crus. The pricing system was dropped and the scale itself abolished in 2010, but “grand cru” and
  “premier cru” remain in the cahier des charges for wines made only from those villages.</p>''')%}
  </div>
  <div class="panel scale">
    <div class="sc-row gc"><b>100 %</b><span>{%T('Grand cru · 17 villages', 'Grand cru · 17 villages')%}</span></div>
    <div class="sc-row pc"><b>90–99 %</b><span>{%T('Premier cru · 42 villages', 'Premier cru · 42 villages')%}</span></div>
    <div class="sc-row ot"><b>80–89 %</b><span>{%T('Autres crus · ≈ 260 villages', 'Other crus · ≈ 260 villages')%}</span></div>
  </div>
  </div>
  <h3 class="sub-h">{%T('Les 17 grands crus', 'The 17 grands crus')%} <span class="hint">{%T('— cliquez pour le plan cadastral', '— click for the parcel map')%}</span></h3>
  <div class="chips">{%cgc%}</div>
  <p class="small legend"><i class="dot gold"></i>{%T('promu grand cru en 1985', 'promoted to grand cru in 1985')%}</p>
  <h3 class="sub-h">{%T('Les 42 premiers crus', 'The 42 premiers crus')%}</h3>
  <div class="chips small-chips">{%cpc%}</div>
</section>"""))

# ---------- other regions ----------
OTHER = [
  ('Côtes de Provence', 'Provence', '1955',
   'Les <b>crus classés de Côtes de Provence</b> : 23 domaines classés en 1955, avant même l’AOC (1977) ; 18 portent encore la mention. Plus récemment, cinq <b>dénominations de terroir</b> : Sainte-Victoire et Fréjus (2005), La Londe (2008), Pierrefeu (2013), Notre-Dame des Anges (2019).',
   'The <b>crus classés of Côtes de Provence</b>: 23 estates classified in 1955, before the AOC itself (1977); 18 still use the term. More recently, five <b>terroir denominations</b>: Sainte-Victoire and Fréjus (2005), La Londe (2008), Pierrefeu (2013), Notre-Dame des Anges (2019).',
   '../Provence-Cote-d-Azur.html'),
  ('Loire · Anjou', 'Loire · Anjou', '2011',
   '<b>Quarts de Chaume grand cru</b> (2011), premier grand cru de la Loire, et <b>Coteaux du Layon premier cru Chaume</b> : deux liquoreux de chenin avec des rendements très bas et la récolte de raisins passerillés ou botrytisés.',
   '<b>Quarts de Chaume grand cru</b> (2011), the Loire’s first grand cru, and <b>Coteaux du Layon premier cru Chaume</b>: two sweet chenins with very low yields and harvests of shrivelled or botrytised grapes.',
   '../Anjou_et_de_Touraine.html'),
  ('Loire · Muscadet', 'Loire · Muscadet', '2011 · 2019',
   'Les <b>crus communaux du Muscadet Sèvre et Maine</b> : Clisson, Gorges et Le Pallet (2011), puis Château-Thébaud, Goulaine, Monnières-Saint-Fiacre et Mouzillon-Tillières (2019). Long élevage sur lies (18 mois et plus) ; d’autres crus sont à l’étude.',
   'The <b>crus communaux of Muscadet Sèvre et Maine</b>: Clisson, Gorges and Le Pallet (2011), then Château-Thébaud, Goulaine, Monnières-Saint-Fiacre and Mouzillon-Tillières (2019). Long lees ageing (18 months and more); more crus are under review.',
   '../Pays_Nantais.html'),
  ('Vallée du Rhône', 'Rhône Valley', '2016',
   'Une pyramide à quatre étages : Côtes du Rhône, Côtes du Rhône Villages, Villages suivis d’un nom de commune, et <b>17 crus</b>. Les derniers promus : Vinsobres (2006), Rasteau (2010) et <b>Cairanne (2016)</b> ; de nouveaux villages nommés s’ajoutent régulièrement.',
   'A four-step pyramid: Côtes du Rhône, Côtes du Rhône Villages, Villages with a named commune, and <b>17 crus</b>. The latest promotions: Vinsobres (2006), Rasteau (2010) and <b>Cairanne (2016)</b>; new named villages are added regularly.',
   '../Rhone-meridional.html'),
  ('Languedoc', 'Languedoc', '2011 →',
   'Une hiérarchie en trois niveaux : AOC Languedoc, « grands vins du Languedoc » et <b>crus du Languedoc</b> — Minervois-La Livinière (1999), Corbières-Boutenac (2005), Terrasses du Larzac (2014), La Clape (2015), Pic Saint-Loup (2017), Saint-Chinian Berlou et Roquebrun…',
   'A three-level hierarchy: AOC Languedoc, “grands vins du Languedoc” and <b>crus du Languedoc</b> — Minervois-La Livinière (1999), Corbières-Boutenac (2005), Terrasses du Larzac (2014), La Clape (2015), Pic Saint-Loup (2017), Saint-Chinian Berlou and Roquebrun…',
   '../Languedoc.html'),
  ('Beaujolais', 'Beaujolais', '→ 2026',
   'Dix <b>crus</b> depuis Régnié (1988). Les premiers <b>premiers crus</b> du Beaujolais sont en préparation : Fleurie a déposé son dossier à l’INAO fin 2023 (sept lieux-dits), Moulin-à-Vent et Brouilly suivent. Rien n’est encore homologué.',
   'Ten <b>crus</b> since Régnié (1988). Beaujolais’ first <b>premiers crus</b> are in the making: Fleurie filed with the INAO in late 2023 (seven lieux-dits), Moulin-à-Vent and Brouilly are following. Nothing is ratified yet.',
   '../Bourgogne%20Regions/Beaujolais.html'),
  ('Mâconnais', 'Mâconnais', '2020',
   '<b>Pouilly-Fuissé</b> : 22 climats premiers crus (Les Ménétrières, Le Clos, Vers Cras, Les Perrières…) à partir du millésime 2020 — les premiers premiers crus du sud de la Bourgogne.',
   '<b>Pouilly-Fuissé</b>: 22 premier cru climats (Les Ménétrières, Le Clos, Vers Cras, Les Perrières…) from the 2020 vintage — the first premiers crus in southern Burgundy.',
   '../Bourgogne%20Regions/Saone-et-Loire.html'),
]
cards = ''.join(f'''<a class="ocard panel" href="{href}"><div class="oc-top"><span class="oc-y">{y}</span>
  <h3>{T(tfr, ten)}</h3></div>{L(f"<p>{fr}</p>", f"<p>{en}</p>")}<span class="oc-go">{T("Voir la carte →", "See the map →")}</span></a>'''
  for tfr, ten, y, fr, en, href in OTHER)
parts.append(sec_head('autres', 'Les nouveaux classements', 'The newer classifications',
                      'Ailleurs en France', 'Elsewhere in France') + R("""
  <div class="panel prose">{%L('<p>Depuis les années 2000, presque toutes les régions bâtissent leur pyramide, sur le modèle bourguignon : crus communaux, premiers crus, grands crus. Ces classements sont inscrits dans les cahiers des charges des AOC et validés par l’INAO.</p>',
   '<p>Since the 2000s nearly every region has been building its own pyramid on the Burgundian model: communal crus, premiers crus, grands crus. These classifications are written into the AOC cahiers des charges and approved by the INAO.</p>')%}</div>
  <div class="ocards">{%cards%}</div>
</section>"""))

import extras
X = extras.build(T, L, esc, plan, sec_head, BGC)
BODY = '\n'.join(parts)
_i = BODY.index('<section class="sec" id="crus-bourgeois"')
BODY = BODY[:_i] + X['pomerol'] + '\n' + BODY[_i:]
_i = BODY.index('<section class="sec" id="alsace"'); _j = BODY.rindex('</section>', 0, _i)
BODY = BODY[:_j] + X['pc_search'] + BODY[_j:]
BODY += '\n' + X['sources']
# link the static « 33 grands crus » table names to their spot on the climats maps
_a = BODY.index('<div class="tiers bgc">'); _b = BODY.index('</section>', _a)
_seg = BODY[_a:_b]
for _n, _u in X['gc_links'].items():
    _seg = _seg.replace('<span class="nm">' + esc(_n) + '</span>', '<a class="nm gcl" href="' + _u + '">' + esc(_n) + ' <i>⌖</i></a>', 1)
    _seg = _seg.replace(' · ' + _n + ' · ', ' · <a class="gcl" href="' + _u + '">' + _n + '</a> · ', 1)
    _seg = _seg.replace('>' + _n + ' · ', '><a class="gcl" href="' + _u + '">' + _n + '</a> · ', 1)
    _seg = _seg.replace(' · ' + _n + '</span>', ' · <a class="gcl" href="' + _u + '">' + _n + '</a></span>', 1)
BODY = BODY[:_a] + _seg + BODY[_b:]
BODY = BODY.replace('<!--@MOUTONNE_LINK@-->', '<a class="plan mt-link" href="' + X['moutonne'] + '">' + T('Voir sur le plan cadastral (emplacement approximatif) →', 'See it on the parcel map (approximate location) →') + '</a>', 1)

JUMP = [('medoc-1855', '1855 Médoc', '1855 Médoc'), ('sauternes-1855', '1855 Sauternes', '1855 Sauternes'),
        ('graves-1959', 'Graves', 'Graves'), ('saint-emilion', 'Saint-Émilion', 'Saint-Émilion'), ('pomerol', 'Pomerol', 'Pomerol'),
        ('crus-bourgeois', 'Crus Bourgeois', 'Crus Bourgeois'), ('crus-artisans', 'Crus Artisans', 'Crus Artisans'), ('bourgogne', 'Bourgogne', 'Burgundy'), ('premiers-crus', '1ers crus · recherche', '1ers crus · search'),
        ('alsace', 'Alsace', 'Alsace'), ('champagne', 'Champagne', 'Champagne'),
        ('autres', 'Autres régions', 'Other regions'), ('sources', 'Sources', 'Sources')]
jump = ''.join(f'<a href="#{i}" data-fr="{esc(fr)}" data-en="{esc(en)}">{fr}</a>' for i, fr, en in JUMP)

tpl = (Path(__file__).parent / 'page_template.html').read_text()
out = tpl.replace('<!--@JUMP@-->', jump).replace('<!--@BODY@-->', BODY)
OUT.write_text(out)
print('wrote', OUT, len(out) // 1024, 'KB')
