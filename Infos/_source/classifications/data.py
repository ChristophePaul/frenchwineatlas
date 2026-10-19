# -*- coding: utf-8 -*-
"""Lists for Infos/Crus_Classifications.html (see gen_page.py).
Sources: the user's « All Classification Liste_2026.docx » + « Cru Bourgeois Classification_2025.docx »
(Bordeaux_Classification/), checked against: INAO notice of 8 Sept 2022 (Saint-Émilion), Alliance des Crus
Bourgeois press kit, Feb 2025 (official 2025 list), the 1855 and 1959 official lists, the Alsace & Champagne CDCs."""

# ---------------- 1855 Médoc (61) ----------------
M1855 = [
    ('Premiers crus', 'First growths', [
        ('Château Lafite Rothschild', 'Pauillac'), ('Château Latour', 'Pauillac'),
        ('Château Margaux', 'Margaux'), ('Château Haut-Brion', 'Pessac · Graves'),
        ('Château Mouton Rothschild', 'Pauillac · 1973')]),
    ('Deuxièmes crus', 'Second growths', [
        ('Château Rauzan-Ségla', 'Margaux'), ('Château Rauzan-Gassies', 'Margaux'),
        ('Château Léoville Las Cases', 'Saint-Julien'), ('Château Léoville Poyferré', 'Saint-Julien'),
        ('Château Léoville Barton', 'Saint-Julien'), ('Château Durfort-Vivens', 'Margaux'),
        ('Château Gruaud Larose', 'Saint-Julien'), ('Château Lascombes', 'Margaux'),
        ('Château Brane-Cantenac', 'Margaux'), ('Château Pichon Baron', 'Pauillac'),
        ('Château Pichon Comtesse de Lalande', 'Pauillac'), ('Château Ducru-Beaucaillou', 'Saint-Julien'),
        ('Château Cos d’Estournel', 'Saint-Estèphe'), ('Château Montrose', 'Saint-Estèphe')]),
    ('Troisièmes crus', 'Third growths', [
        ('Château Kirwan', 'Margaux'), ('Château d’Issan', 'Margaux'), ('Château Lagrange', 'Saint-Julien'),
        ('Château Langoa Barton', 'Saint-Julien'), ('Château Giscours', 'Margaux'),
        ('Château Malescot Saint-Exupéry', 'Margaux'), ('Château Cantenac Brown', 'Margaux'),
        ('Château Boyd-Cantenac', 'Margaux'), ('Château Palmer', 'Margaux'),
        ('Château La Lagune', 'Haut-Médoc'), ('Château Desmirail', 'Margaux'),
        ('Château Calon Ségur', 'Saint-Estèphe'), ('Château Ferrière', 'Margaux'),
        ('Château Marquis d’Alesme', 'Margaux')]),
    ('Quatrièmes crus', 'Fourth growths', [
        ('Château Saint-Pierre', 'Saint-Julien'), ('Château Talbot', 'Saint-Julien'),
        ('Château Branaire-Ducru', 'Saint-Julien'), ('Château Duhart-Milon', 'Pauillac'),
        ('Château Pouget', 'Margaux'), ('Château La Tour Carnet', 'Haut-Médoc'),
        ('Château Lafon-Rochet', 'Saint-Estèphe'), ('Château Beychevelle', 'Saint-Julien'),
        ('Château Prieuré-Lichine', 'Margaux'), ('Château Marquis de Terme', 'Margaux')]),
    ('Cinquièmes crus', 'Fifth growths', [
        ('Château Pontet-Canet', 'Pauillac'), ('Château Batailley', 'Pauillac'),
        ('Château Haut-Batailley', 'Pauillac'), ('Château Grand-Puy-Lacoste', 'Pauillac'),
        ('Château Grand-Puy-Ducasse', 'Pauillac'), ('Château Lynch-Bages', 'Pauillac'),
        ('Château Lynch-Moussas', 'Pauillac'), ('Château Dauzac', 'Margaux'),
        ('Château d’Armailhac', 'Pauillac'), ('Château du Tertre', 'Margaux'),
        ('Château Haut-Bages Libéral', 'Pauillac'), ('Château Pédesclaux', 'Pauillac'),
        ('Château Belgrave', 'Haut-Médoc'), ('Château de Camensac', 'Haut-Médoc'),
        ('Château Cos Labory', 'Saint-Estèphe'), ('Château Clerc Milon', 'Pauillac'),
        ('Château Croizet-Bages', 'Pauillac'), ('Château Cantemerle', 'Haut-Médoc · 1856')]),
]

# ---------------- 1855 Sauternes & Barsac (27) ----------------
S1855 = [
    ('Premier cru supérieur', 'Superior first growth', [('Château d’Yquem', 'Sauternes')]),
    ('Premiers crus', 'First growths', [
        ('Château La Tour Blanche', 'Bommes'), ('Château Lafaurie-Peyraguey', 'Bommes'),
        ('Clos Haut-Peyraguey', 'Bommes'), ('Château de Rayne Vigneau', 'Bommes'),
        ('Château Suduiraut', 'Preignac'), ('Château Coutet', 'Barsac'), ('Château Climens', 'Barsac'),
        ('Château Guiraud', 'Sauternes'), ('Château Rieussec', 'Fargues'),
        ('Château Rabaud-Promis', 'Bommes'), ('Château Sigalas Rabaud', 'Bommes')]),
    ('Deuxièmes crus', 'Second growths', [
        ('Château de Myrat', 'Barsac'), ('Château Doisy Daëne', 'Barsac'), ('Château Doisy-Dubroca', 'Barsac'),
        ('Château Doisy-Védrines', 'Barsac'), ('Château d’Arche', 'Sauternes'), ('Château Filhot', 'Sauternes'),
        ('Château Broustet', 'Barsac'), ('Château Nairac', 'Barsac'), ('Château Caillou', 'Barsac'),
        ('Château Suau', 'Barsac'), ('Château de Malle', 'Preignac'), ('Château Romer', 'Fargues'),
        ('Château Romer du Hayot', 'Fargues'), ('Château Lamothe', 'Sauternes'),
        ('Château Lamothe Guignard', 'Sauternes')]),
]

# ---------------- Graves 1959 (16) : name, commune, R/B ----------------
GRAVES = [
    ('Château Bouscaut', 'Cadaujac', 'RB'), ('Château Carbonnieux', 'Léognan', 'RB'),
    ('Domaine de Chevalier', 'Léognan', 'RB'), ('Château Couhins', 'Villenave-d’Ornon', 'B'),
    ('Château Couhins-Lurton', 'Villenave-d’Ornon', 'B'), ('Château de Fieuzal', 'Léognan', 'R'),
    ('Château Haut-Bailly', 'Léognan', 'R'), ('Château Haut-Brion', 'Pessac', 'R'),
    ('Château La Mission Haut-Brion', 'Talence', 'R'), ('Château La Tour Haut-Brion ¹', 'Talence', 'R'),
    ('Château Laville Haut-Brion ²', 'Talence', 'B'), ('Château Latour-Martillac', 'Martillac', 'RB'),
    ('Château Malartic-Lagravière', 'Léognan', 'RB'), ('Château Olivier', 'Léognan', 'RB'),
    ('Château Pape Clément', 'Pessac', 'R'), ('Château Smith Haut Lafitte', 'Martillac', 'R'),
]

# ---------------- Saint-Émilion 2022 (INAO, 8 Sept 2022) ----------------
SE_A = ['Château Figeac', 'Château Pavie']
SE_B = ['Château Beau-Séjour Bécot', 'Château Beauséjour Héritiers Duffau-Lagarrosse', 'Château Bélair-Monange',
        'Château Canon', 'Château Canon-la-Gaffelière', 'Château Larcis Ducasse', 'Château Pavie Macquin',
        'Château Troplong Mondot', 'Château Trottevieille', 'Château Valandraud', 'Clos Fourtet', 'La Mondotte']
SE_NEW = {'Badette', 'Boutisse', 'Corbin Michotte', 'Croix de Labrie', 'La Confession', 'La Croizille',
          'Lassègue', 'Mangot', 'Montlabert', 'Montlisse', 'Rol Valentin', 'Tour Baladoz',
          'Tour Saint-Christophe', 'Clos Dubreuil', 'Clos Badon Thunevin', 'Clos Saint-Julien'}
SE_GCC = ['Badette', 'Balestard la Tonnelle', 'Barde-Haut', 'Bellefont-Belcier', 'Bellevue', 'Berliquet',
          'Boutisse', 'Cadet-Bon', 'Cap de Mourlin', 'Chauvin', 'Clos de Sarpe', 'Corbin', 'Corbin Michotte',
          'Côte de Baleau', 'Croix de Labrie', 'Dassault', 'de Ferrand', 'de Pressac', 'Destieux', 'Faugères',
          'Fleur Cardinale', 'Fombrauge', 'Fonplégade', 'Fonroque', 'Franc Mayne', 'Grand Corbin',
          'Grand Corbin-Despagne', 'Grand Mayne', 'Guadet', 'Haut-Sarpe', 'Jean Faure', 'La Commanderie',
          'La Confession', 'La Couspaude', 'La Croizille', 'La Dominique', 'La Fleur Morange', 'La Marzelle',
          'La Serre', 'La Tour Figeac', 'Laniote', 'Larmande', 'Laroque', 'Laroze', 'Le Châtelet', 'Le Prieuré',
          'Mangot', 'Monbousquet', 'Montlabert', 'Montlisse', 'Moulin du Cadet', 'Péby Faugères',
          'Petit Faurie de Soutard', 'Ripeau', 'Rochebelle', 'Rol Valentin', 'Saint-Georges (Côte Pavie)',
          'Sansonnet', 'Soutard', 'Tour Baladoz', 'Tour Saint-Christophe', 'Villemaurine', 'Yon-Figeac',
          'Clos Badon Thunevin', 'Clos de l’Oratoire', 'Clos des Jacobins', 'Clos Dubreuil', 'Clos Saint-Julien',
          'Clos Saint-Martin', 'Couvent des Jacobins', 'Lassègue']

# ---------------- Crus Bourgeois du Médoc 2025 (Alliance press kit, 10 Feb 2025) ----------------
CB = {
 'exc': [
  ('Médoc', ['La Cardonne', 'Castera', 'Laujac']),
  ('Haut-Médoc', ['Malescasse', 'de Malleret', 'Paloumey', 'Reysson', 'du Taillan']),
  ('Listrac-Médoc', ['Reverdi']),
  ('Margaux', ['d’Arsac', 'Mongravey', 'Paveil de Luze']),
  ('Saint-Estèphe', ['Le Crock', 'Laffitte Carcasset'])],
 'sup': [
  ('Médoc', ['La Branne', 'Escot', 'Fleur La Mothe', 'La France Delhomme', 'Greysac', 'Haut-Bana', 'Labadie',
             'Noaillac', 'Patache d’Aux', 'Pierre de Montignac', 'Poitevin', 'Preuillac', 'Saint-Hilaire',
             'Les Tuileries']),
  ('Haut-Médoc', ['Beaumont', 'Bel Air Gloria', 'Clos La Bohème', 'du Cartillon', 'Cissac', 'Dillon',
                  'Lamothe-Bergeron', 'Lestage Simon', 'Liversan', 'Magnol', 'Meyre', 'du Moulin Rouge',
                  'Peyrabon', 'Peyrat-Fourthon', 'Pontoise Cabarrus', 'Ramage La Batisse']),
  ('Moulis-en-Médoc', ['Biston-Brillette', 'Lalaudey', 'La Mouline']),
  ('Margaux', ['La Fortune']),
  ('Saint-Estèphe', ['de Côme', 'Tour des Termes'])],
 'cb': [
  ('Médoc', ['Les Anguilleys', 'd’Argan', 'L’Argenteyre', 'Beauvillage', 'Bégadan', 'Bégadanet', 'Bellegrave',
             'Bellevue', 'de Bensse', 'Bessan Ségur', 'Le Bourdieu', 'Bournac', 'des Cabans', 'Cangruey',
             'Carcanieux', 'La Chandellière', 'Chantemerle', 'Clément Saint-Jean', 'Côtes de Blaignan',
             'de la Croix', 'd’Escurac', 'Gémeillan', 'La Grange de Bessan', 'des Granges d’Or', 'Grivière',
             'Haut Barrail', 'Haut Canteloup', 'Haut-Maurac', 'Haut Queyran', 'Lacombe Noaillac', 'Ladignac',
             'Lalande d’Auvion', 'Lassus', 'Les Lattes', 'Leboscq', 'Lestruelle', 'Lousteauneuf',
             'Maison Blanche', 'Mareil', 'Mazails', 'Méric', 'Moulin de Bel Air', 'Moulin de Canhaut',
             'Moulin de l’Abbaye', 'Moulin de Taffard', 'Les Mourlanes', 'Nouret', 'de Panigon', 'Pey de Pont',
             'La Pirouette', 'Plagnac', 'Pontet Barrail', 'Pontey', 'Ramafort', 'La Ribaud', 'Ricaudet',
             'La Roque de By', 'Roquegrave', 'Rousseau de Sipian', 'Saint-Aubin', 'Saint-Bonnet',
             'Saint-Christophe', 'Le Temple', 'Tour Castillon', 'Tour Prignac', 'Tour Saint-Vincent',
             'des Tourelles', 'Les Tresquots', 'Troussas', 'La Valière', 'Vieux Château Landon',
             'Le Vieux Fort', 'Vieux Robin', 'Le Vieux Serestin']),
  ('Haut-Médoc', ['d’Arcins', 'd’Aurilhac', 'Barateau', 'Barreyres', 'Bibian', 'Le Bourdieu Vertheuil',
                  'de Braude', 'de Cartujac', 'Corconnac', 'Croix du Trale', 'Dasvin Bel Air',
                  'Devise d’Ardilley', 'La Fon du Berger', 'Grand Clapeau Olivier', 'Grandis', 'Haut Beyzac',
                  'Haut-Madrac', 'Lacour Jacquet', 'Martin', 'Le Monteil d’Arsac', 'Moulin de Blanchon',
                  'Moulin des Moines', 'Prieuré de Beyzac', 'Puy Castéra', 'du Raux', 'Rollin', 'Saint-Ahon',
                  'Sénilhac', 'Tourteran', 'Victoria', 'Vieux Landat', 'de Villambis']),
  ('Listrac-Médoc', ['Capdet', 'Donissan', 'Lafon', 'Lalande', 'Liouner', 'Sémeillan-Mazeau']),
  ('Moulis-en-Médoc', ['Guitignan', 'Pomeys']),
  ('Pauillac', ['Plantey']),
  ('Saint-Estèphe', ['La Commanderie', 'Coutelin-Merville', 'German Marbuzet', 'Picard', 'Tour Saint-Fort'])],
}

# ---------------- Burgundy : the 33 grand cru AOCs ----------------
BGC = [
  ('Chablis', 'Chablis', [('Chablis Grand Cru', 'Blanchot · Bougros · Les Clos · Grenouilles · Preuses · Valmur · Vaudésir', 'B')]),
  ('Côte de Nuits', 'Côte de Nuits', [
    ('Chambertin', 'Gevrey-Chambertin', 'R'), ('Chambertin-Clos de Bèze', 'Gevrey-Chambertin', 'R'),
    ('Chapelle-Chambertin', 'Gevrey-Chambertin', 'R'), ('Charmes-Chambertin', 'Gevrey-Chambertin', 'R'),
    ('Griotte-Chambertin', 'Gevrey-Chambertin', 'R'), ('Latricières-Chambertin', 'Gevrey-Chambertin', 'R'),
    ('Mazis-Chambertin', 'Gevrey-Chambertin', 'R'), ('Ruchottes-Chambertin', 'Gevrey-Chambertin', 'R'),
    ('Mazoyères-Chambertin', 'Gevrey-Chambertin', 'R'),
    ('Clos de la Roche', 'Morey-Saint-Denis', 'R'), ('Clos Saint-Denis', 'Morey-Saint-Denis', 'R'),
    ('Clos des Lambrays', 'Morey-Saint-Denis', 'R'), ('Clos de Tart', 'Morey-Saint-Denis', 'R'),
    ('Bonnes-Mares', 'Chambolle-Musigny · Morey', 'R'), ('Musigny', 'Chambolle-Musigny', 'RB'),
    ('Clos de Vougeot', 'Vougeot', 'R'),
    ('Échezeaux', 'Flagey-Échezeaux', 'R'), ('Grands-Échezeaux', 'Flagey-Échezeaux', 'R'),
    ('Richebourg', 'Vosne-Romanée', 'R'), ('Romanée-Conti', 'Vosne-Romanée', 'R'),
    ('La Romanée', 'Vosne-Romanée', 'R'), ('Romanée-Saint-Vivant', 'Vosne-Romanée', 'R'),
    ('La Tâche', 'Vosne-Romanée', 'R'), ('La Grande Rue', 'Vosne-Romanée · 1992', 'R')]),
  ('Côte de Beaune', 'Côte de Beaune', [
    ('Corton', 'Aloxe · Ladoix · Pernand', 'RB'), ('Corton-Charlemagne', 'Aloxe · Ladoix · Pernand', 'B'),
    ('Charlemagne', 'Aloxe · Pernand', 'B'), ('Montrachet', 'Puligny · Chassagne', 'B'),
    ('Chevalier-Montrachet', 'Puligny-Montrachet', 'B'), ('Bâtard-Montrachet', 'Puligny · Chassagne', 'B'),
    ('Bienvenues-Bâtard-Montrachet', 'Puligny-Montrachet', 'B'), ('Criots-Bâtard-Montrachet', 'Chassagne-Montrachet', 'B')]),
]

# ---------------- Alsace : 51 grands crus (file name in Plan Cadastraux/Alsace_Grands_Crus) ----------------
AGC = ['Altenberg de Bergbieten', 'Altenberg de Bergheim', 'Altenberg de Wolxheim', 'Brand', 'Bruderthal',
       'Eichberg', 'Engelberg', 'Florimont', 'Frankstein', 'Froehn', 'Furstentum', 'Geisberg', 'Gloeckelberg',
       'Goldert', 'Hatschbourg', 'Hengst', 'Kaefferkopf', 'Kanzlerberg', 'Kastelberg', 'Kessler',
       'Kirchberg de Barr', 'Kirchberg de Ribeauvillé', 'Kitterlé', 'Mambourg', 'Mandelberg', 'Marckrain',
       'Moenchberg', 'Muenchberg', 'Ollwiller', 'Osterberg', 'Pfersigberg', 'Pfingstberg', 'Praelatenberg',
       'Rangen', 'Rosacker', 'Saering', 'Schlossberg', 'Schoenenbourg', 'Sommerberg', 'Sonnenglanz', 'Spiegel',
       'Sporen', 'Steinert', 'Steingrubler', 'Steinklotz', 'Vorbourg', 'Wiebelsberg', 'Wineck-Schlossberg',
       'Winzenberg', 'Zinnkoepflé', 'Zotzenberg']
AGC_RED = {'Hengst', 'Kirchberg de Barr', 'Vorbourg'}

# ---------------- Champagne ----------------
CGC = ['Ambonnay', 'Avize', 'Aÿ', 'Beaumont-sur-Vesle', 'Bouzy', 'Chouilly', 'Cramant', 'Louvois',
       'Mailly-Champagne', 'Le Mesnil-sur-Oger', 'Oger', 'Oiry', 'Puisieulx', 'Sillery', 'Tours-sur-Marne',
       'Verzenay', 'Verzy']
CGC_1985 = {'Chouilly', 'Le Mesnil-sur-Oger', 'Oger', 'Oiry', 'Verzy'}
CPC = ['Avenay-Val-d’Or', 'Bergères-lès-Vertus', 'Bezannes', 'Billy-le-Grand', 'Bisseuil', 'Chamery', 'Champillon',
       'Chigny-lès-Roses', 'Coligny', 'Cormontreuil', 'Coulommes-la-Montagne', 'Cuis', 'Cumières', 'Dizy',
       'Écueil', 'Étréchy', 'Grauves', 'Hautvillers', 'Jouy-lès-Reims', 'Ludes', 'Mareuil-sur-Aÿ', 'Les Mesneux',
       'Montbré', 'Mutigny', 'Pargny-lès-Reims', 'Pierry', 'Rilly-la-Montagne', 'Sacy', 'Sermiers', 'Taissy',
       'Tauxières-Mutry', 'Trépail', 'Trois-Puits', 'Vaudemange', 'Vertus', 'Villedommange',
       'Villeneuve-Renneville-Chevigny', 'Villers-Allerand', 'Villers-aux-Nœuds', 'Villers-Marmery', 'Voipreux',
       'Vrigny']

if __name__ == '__main__':
    n = lambda groups: sum(len(x[1]) for x in groups)
    print('1855 Médoc', sum(len(t[2]) for t in M1855), '| Sauternes', sum(len(t[2]) for t in S1855),
          '| Graves', len(GRAVES), '| SE', len(SE_A), len(SE_B), len(SE_GCC), '| new', len(SE_NEW & set(SE_GCC)))
    print('CB', n(CB['exc']), n(CB['sup']), n(CB['cb']), [(a, len(l)) for a, l in CB['cb']])
    print('Burgundy GC', sum(len(x[2]) for x in BGC), '| Alsace', len(AGC), '| Champagne', len(CGC), len(CPC))

# ---------------- Crus Artisans du Médoc 2023 (Qualisud, closed 12 May 2023; vintages 2022-2026) ----------------
# Moutte Blanc is classified for both its Haut-Médoc and its Margaux → 33 entries, 32 châteaux.
CA = [
  ('Médoc', ['Bejac Romelys', 'Gadet Terrefort', 'Garance Haut Grenat', 'Haut Brisey', 'Haut Couloumey', 'Haut Gravat',
             'La Baie de Lalo', 'La Hourcade', 'La Tessonnière', 'Les Graves de Loirac', 'L’Évasion', 'Saint-Grégoire',
             'Vieux Gadet']),
  ('Haut-Médoc', ['de Coudot', 'Domaine de la Garenne', 'de Lauga', 'd’Osmond', 'du Ha', 'Grand Brun', 'Micalet',
                  'Moutte Blanc', 'Pey Mallet', 'Tour du Goua', 'Vieux Gabarey']),
  ('Listrac-Médoc', ['Dacher de Delmonte']),
  ('Margaux', ['des Graviers', 'Les Barraillots', 'Moutte Blanc', 'Clos de Bigos']),
  ('Saint-Julien', ['La Fleur Lauga']),
  ('Saint-Estèphe', ['Graves de Pez', 'Linot', 'Marceline']),
]
