"""Answer bank of game 6 « De toutes les couleurs » / “True Colours”.

One row per AOC: the colours and types its cahier des charges allows (chapter I, point III « Couleur et types de produit »).
Plain still wines come straight from the Cépages DSL labels; everything else is in SPECIAL, read in the rulebooks (2026-11-24).

Codes  w r o      still white / red / rosé (gris and clairet = rosé, vin jaune = white)
       sw so sr   sparkling (mousseux, pétillant, crémant) white / rosé / red
       dw do dr da  sweet white / rosé / red / ambré (moelleux, liquoreux, VT-SGN, vin de paille, vin doux naturel, vin de liqueur)
A code after « + » is accepted but not required: a rare or debatable version that neither scores nor costs a point.
"""
import quiz_bank
from quiz_bank import AOCS, FAMOUS, KNOWN, REGION_EN, cep_link, slug

ORDER = ['w', 'r', 'o', 'sw', 'so', 'sr', 'dw', 'do', 'dr', 'da']

SIMPLE = {'Blanc': 'w', 'Rouge': 'r', 'Rosé': 'o', 'Gris': 'o', 'Clairet': 'o'}

VJ = ('Le vin jaune est un blanc sec ; le vin de paille, un blanc doux de raisins séchés.',
      'Vin jaune is a dry white; vin de paille is a sweet white made from dried grapes.')
VTSGN = ('Le blanc doux, ce sont les « vendanges tardives » et les « sélections de grains nobles ».',
         'The sweet white is “vendanges tardives” and “sélection de grains nobles”.')
MOEL = ('Les blancs portent la mention sec, demi-sec, moelleux ou doux : en bonne année, certains sont sucrés (réponse acceptée, pas exigée).',
        'Whites may be labelled sec, demi-sec, moelleux or doux: in good years some are sweet (accepted, not required).')
GRIS = ('Le « vin gris » est un rosé très pâle, pressé sans macération.', '“Vin gris” is a very pale rosé, pressed without maceration.')
LIQ = ('Uniquement du blanc liquoreux, de raisins à surmaturité (pourriture noble).', 'Sweet white only, from overripe grapes (noble rot).')
LIQ2 = ('Uniquement du blanc doux.', 'Sweet white only.')
VDNB = ('Vin doux naturel blanc, de muscat.', 'White vin doux naturel, from Muscat.')
VDL = ('C’est un vin de liqueur : du moût de raisin muté à l’eau-de-vie.', 'This is a vin de liqueur: grape must fortified with brandy.')
ANJ = ('Un rosé demi-sec, « tendre » : on le classe en rosé (« doux rosé » est accepté).', 'An off-dry rosé: filed under rosé (“sweet rosé” is accepted).')

# name: (codes, note FR/EN or None)
SPECIAL = {
    # Bordeaux
    'Premières Côtes de Bordeaux': ('dw', LIQ2), 'Cadillac': ('dw', LIQ), 'Loupiac': ('dw', LIQ), 'Sainte-Croix-du-Mont': ('dw', LIQ),
    'Cérons': ('dw', LIQ), 'Sauternes': ('dw', LIQ), 'Barsac': ('dw', LIQ),
    'Graves Supérieures': ('dw', ('Les Graves supérieures sont des blancs avec sucres résiduels ; le rouge et le blanc sec s’appellent Graves.',
                                  'Graves supérieures are whites with residual sugar; the red and the dry white are called Graves.')),
    'Côtes de Bordeaux': ('r w dw', ('Rouge partout ; blanc sec à Blaye, Francs et Sainte-Foy ; blanc liquoreux à Francs et Sainte-Foy.',
                                     'Red everywhere; dry white in Blaye, Francs and Sainte-Foy; sweet white in Francs and Sainte-Foy.')),
    'Côtes de Bordeaux Saint-Macaire': ('w dw', ('Que des blancs : secs, moelleux ou liquoreux.', 'Whites only: dry, medium-sweet or sweet.')),
    'Bordeaux': ('w r o + dw', ('Le clairet est un rosé foncé. Le rare « Bordeaux blanc avec sucres » est accepté, pas exigé.',
                                'Clairet is a dark rosé. The rare “Bordeaux white with residual sugar” is accepted, not required.')),
    'Bordeaux Supérieur': ('r dw + w', ('Le Bordeaux supérieur blanc garde toujours des sucres (plus de 17 g/l) : c’est un moelleux.',
                                        'White Bordeaux supérieur always keeps some sugar (over 17 g/l): it is medium-sweet.')),
    'Crémant de Bordeaux': ('sw so', None),
    'Graves de Vayres': ('w r + dw', ('Les blancs peuvent être secs ou garder des sucres (réponse acceptée, pas exigée).',
                                      'Whites may be dry or keep some sugar (accepted, not required).')),
    'Entre-deux-Mers': ('w r', ('Longtemps réservée au blanc sec, l’AOC accepte aussi le rouge.', 'Long reserved for dry white, the AOC now covers red too.')),
    'Médoc': ('r w', ('Surprise : le Médoc blanc existe désormais dans le cahier des charges.', 'Surprise: white Médoc is now in the rulebook.')),
    # Burgundy, Beaujolais, Champagne
    'Bourgogne Mousseux': ('sr', ('Le seul mousseux rouge parmi les appellations de Bourgogne.', 'The only red sparkling wine among Burgundy’s appellations.')),
    'Crémant de Bourgogne': ('sw so', None),
    'Bourgogne': ('w r o', ('La mention « clairet » désigne un rosé.', 'The “clairet” mention is a rosé.')),
    'Coteaux Bourguignons': ('w r o', None),
    'Marsannay': ('w r o', ('La seule appellation communale de Bourgogne qui produit les trois couleurs.', 'The only village appellation in Burgundy making all three colours.')),
    'Musigny': ('w r', ('Le seul grand cru de la Côte de Nuits à exister aussi en blanc.', 'The only Côte de Nuits grand cru that also exists in white.')),
    'Corton': ('w r', ('Les climats (Bressandes, Clos du Roi…) ne s’ajoutent qu’au rouge.', 'Climat names (Bressandes, Clos du Roi…) may only be added to the red.')),
    'Blagny': ('r', ('Blagny n’est que rouge : les blancs du hameau s’appellent Meursault ou Puligny-Montrachet.',
                     'Blagny is red only: the hamlet’s whites are called Meursault or Puligny-Montrachet.')),
    'Champagne': ('sw so', ('Même un champagne demi-sec ou doux reste un effervescent.', 'Even a demi-sec or doux Champagne counts as sparkling.')),
    'Coteaux Champenois': ('w r o', ('Les vins tranquilles de la Champagne, sans bulles.', 'Champagne’s still wines, without bubbles.')),
    # Jura, Savoie, Bugey
    'Arbois': ('w r o dw + da', VJ), 'Côtes du Jura': ('w r o dw + da', VJ),
    "L'Étoile": ('w dw + da', VJ),
    'Château-Chalon': ('w', ('Uniquement du vin jaune : un blanc sec de savagnin, élevé sous voile.', 'Vin jaune only: a dry white from Savagnin, aged under a veil of yeast.')),
    'Crémant du Jura': ('sw so', None), 'Macvin du Jura': ('dw do dr', VDL),
    'Bugey': ('w r o sw so', ('Le Cerdon est un mousseux rosé ; les mousseux et pétillants existent aussi en blanc.', 'Cerdon is a sparkling rosé; sparkling wines also exist in white.')),
    'Seyssel': ('w sw', None),
    'Vin de Savoie': ('w r o sw so', ('Les bulles : Crémant de Savoie et Ayze en blanc, mousseux en rosé.', 'The bubbles: Crémant de Savoie and Ayze in white, mousseux in rosé.')),
    # Alsace-Lorraine
    'Alsace': ('w r o dw', VTSGN),
    'Alsace Grand Cru': ('w r dw', ('Blanc partout, rouge (pinot noir) à Hengst, Kirchberg de Barr et Vorbourg, et des VT et SGN.',
                                    'White everywhere, red (Pinot Noir) in Hengst, Kirchberg de Barr and Vorbourg, plus VT and SGN.')),
    "Crémant d'Alsace": ('sw so', None),
    'Côtes de Toul': ('w r o', GRIS),
    # Languedoc
    'Clairette du Languedoc': ('w dw + da', ('Du blanc sec ou moelleux, et un vin de liqueur blanc ; le « rancio » tire sur l’ambre (accepté, pas exigé).',
                                             'Dry or medium-sweet white, plus a white vin de liqueur; “rancio” turns amber (accepted, not required).')),
    'Crémant de Limoux': ('sw so', None), 'Blanquette de Limoux': ('sw', None),
    'Blanquette méthode ancestrale': ('sw + dw', ('Douce, mais d’abord effervescente.', 'Sweet, but sparkling first of all.')),
    'Limoux': ('w r + sw', ('Sous le nom Limoux seul : blanc et rouge tranquilles. Les bulles portent le nom de Blanquette (accepté, pas exigé).',
                            'Under the name Limoux alone: still white and red. The bubbles are called Blanquette (accepted, not required).')),
    'Muscat de Frontignan': ('dw dr + da', ('Vin doux naturel ou vin de liqueur, en blanc… et en rouge.', 'Vin doux naturel or vin de liqueur, in white… and in red.')),
    'Muscat de Lunel': ('dw', VDNB), 'Muscat de Mireval': ('dw', VDNB), 'Muscat de Saint-Jean-de-Minervois': ('dw', VDNB),
    'Sable de Camargue': ('o', ('Uniquement du « gris » et du « gris de gris » : un rosé très pâle.', '“Gris” and “gris de gris” only: a very pale rosé.')),
    # Loire
    'Anjou': ('w r sw so + dw', ('Pas de rosé tranquille sous ce nom : il s’appelle Rosé d’Anjou ou Cabernet d’Anjou. Les blancs peuvent être moelleux (accepté, pas exigé).',
                                 'No still rosé under this name: it is called Rosé d’Anjou or Cabernet d’Anjou. Whites may be medium-sweet (accepted, not required).')),
    "Cabernet d'Anjou": ('o + do', ANJ), "Rosé d'Anjou": ('o + do', ANJ),
    'Bonnezeaux': ('dw', LIQ), 'Coteaux de Saumur': ('dw', LIQ2), "Coteaux de l'Aubance": ('dw', LIQ2), 'Coteaux du Layon': ('dw', LIQ),
    'Quarts de Chaume': ('dw', LIQ), 'Anjou Coteaux de la Loire': ('dw', LIQ2),
    'Coteaux du Vendômois': ('w r o', GRIS), 'Châteaumeillant': ('r o', GRIS), 'Touraine Noble Joué': ('o', GRIS),
    'Reuilly': ('w r o', ('Son rosé de pinot gris est souvent appelé « gris ».', 'Its Pinot Gris rosé is often called “gris”.')),
    'Crémant de Loire': ('sw so', None),
    'Montlouis-sur-Loire': ('w sw dw', ('Un seul cépage, tous les styles : sec, demi-sec, moelleux, doux, pétillant ou mousseux.',
                                        'One grape, every style: dry, off-dry, medium-sweet, sweet, semi-sparkling or sparkling.')),
    'Vouvray': ('w sw dw', ('Un seul cépage, tous les styles : sec, demi-sec, moelleux, doux, pétillant ou mousseux.',
                            'One grape, every style: dry, off-dry, medium-sweet, sweet, semi-sparkling or sparkling.')),
    'Saumur': ('w r o sw so', None),
    'Touraine': ('w r o sw so + sr dw', ('Trois couleurs tranquilles, et des mousseux blancs et rosés (un ancien cahier des charges prévoyait aussi un mousseux rouge).',
                                         'Three still colours, plus white and rosé sparkling wines (an earlier rulebook also allowed a red one).')),
    'Savennières': ('w + dw', MOEL), 'Savennières Roche aux Moines': ('w + dw', MOEL), 'Coulée de Serrant': ('w + dw', MOEL),
    'Jasnières': ('w + dw', MOEL), 'Cour-Cheverny': ('w + dw', MOEL),
    'Coteaux du Loir': ('w r o + dw', MOEL),
    "Coteaux d'Ancenis": ('w r o + dw', ('Le blanc, c’est la Malvoisie (pinot gris), souvent moelleuse (accepté, pas exigé).',
                                         'The white is Malvoisie (Pinot Gris), often medium-sweet (accepted, not required).')),
    # Rhône
    'Clairette de Die': ('sw', ('Uniquement des bulles blanches, douces ou brut.', 'White bubbles only, sweet or brut.')),
    'Crémant de Die': ('sw', None),
    'Condrieu': ('w + dw', ('Presque toujours sec ; une production confidentielle de moelleux existe (acceptée, pas exigée).',
                            'Almost always dry; a tiny sweet production exists (accepted, not required).')),
    'Hermitage': ('w r dw + da', ('Le blanc doux, c’est le rarissime vin de paille.', 'The sweet white is the very rare vin de paille.')),
    'Saint-Péray': ('w sw', None),
    'Châteauneuf-du-Pape': ('r w', ('Pas de rosé à Châteauneuf-du-Pape !', 'No rosé in Châteauneuf-du-Pape!')),
    'Gigondas': ('w r o', ('Le blanc a rejoint le rouge et le rosé dans le cahier des charges.', 'White has joined red and rosé in the rulebook.')),
    'Muscat de Beaumes-de-Venise': ('dw do dr', ('Vin doux naturel blanc, rosé ou rouge.', 'Vin doux naturel in white, rosé or red.')),
    'Rasteau': ('r dw do dr da', ('Du rouge sec, et des vins doux naturels blanc, rosé, grenat, tuilé et ambré.',
                                  'Dry red, plus vins doux naturels: white, rosé, grenat, tuilé and ambré.')),
    # Roussillon
    'Banyuls': ('dw do dr da', ('Blanc, rosé, rimage et traditionnel (rouges), ambré. Le rouge sec du même terroir s’appelle Collioure.',
                                'White, rosé, rimage and traditionnel (red), ambré. The dry red of the same vineyard is called Collioure.')),
    'Banyuls Grand Cru': ('dr + da', ('Le grand cru est un vin doux naturel rouge, élevé au moins 30 mois sous bois.',
                                      'The grand cru is a red vin doux naturel, aged at least 30 months in wood.')),
    'Grand Roussillon': ('dw do dr + da', None),
    'Maury': ('r dw dr da', ('Du rouge sec, et des vins doux naturels blanc, grenat, tuilé et ambré.', 'Dry red, plus vins doux naturels: white, grenat, tuilé and ambré.')),
    'Muscat de Rivesaltes': ('dw', VDNB),
    'Rivesaltes': ('do dr da', ('Ambré, grenat, tuilé ou rosé : il n’y a pas de mention « blanc ».', 'Ambré, grenat, tuilé or rosé: there is no “blanc” mention.')),
    'Muscat du Cap Corse': ('dw + da', VDNB),
    # South-West, Charentes
    'Corrèze': ('w r dw dr + da', ('Le vin de paille, de raisins séchés, existe en blanc et en rouge.', 'The vin de paille, from dried grapes, exists in white and red.')),
    'Côtes de Montravel': ('dw', LIQ2), 'Haut-Montravel': ('dw', LIQ2), 'Monbazillac': ('dw', LIQ), 'Saussignac': ('dw', LIQ2),
    'Rosette': ('dw', ('Uniquement du blanc moelleux, de 25 à 51 g/l de sucres. Rien à voir avec le rosé !', 'Medium-sweet white only, 25–51 g/l of sugar. Nothing to do with rosé!')),
    'Côtes de Bergerac': ('r dw', ('Les blancs sont moelleux ; le blanc sec et le rosé s’appellent Bergerac.', 'The whites are medium-sweet; the dry white and the rosé are called Bergerac.')),
    'Bergerac': ('w r o', ('Le blanc est toujours sec : le moelleux s’appelle Côtes de Bergerac.', 'The white is always dry: the medium-sweet one is called Côtes de Bergerac.')),
    'Côtes de Duras': ('w r o dw', ('Les blancs sont secs ou moelleux.', 'Whites are dry or medium-sweet.')),
    'Floc de Gascogne': ('dw do', ('C’est un vin de liqueur : du moût muté à l’armagnac, en blanc ou en rosé.', 'This is a vin de liqueur: must fortified with Armagnac, white or rosé.')),
    'Gaillac': ('w r o sw dw', ('Trois couleurs, des mousseux blancs (dont la méthode ancestrale) et des blancs doux et vendanges tardives.',
                                'Three colours, white sparkling wines (including the ancestral method) and sweet, late-harvest whites.')),
    'Gaillac Premières Côtes': ('w', ('Uniquement du blanc sec (4 g/l de sucres au plus).', 'Dry white only (4 g/l of sugar at most).')),
    'Jurançon': ('w dw', ('« Jurançon » tout court est toujours doux ; le sec s’appelle « Jurançon sec ».', 'Plain “Jurançon” is always sweet; the dry one is “Jurançon sec”.')),
    'Pacherenc du Vic-Bilh': ('w dw', ('Sec ou doux, mais toujours blanc.', 'Dry or sweet, but always white.')),
    'Montravel': ('w r', None),
    'Pineau des Charentes': ('dw do dr', ('C’est un vin de liqueur : du moût muté au cognac, en blanc, rosé ou rouge.', 'This is a vin de liqueur: must fortified with Cognac, white, rosé or red.')),
}
# DSL labels that carry a qualifier but stay plain still wines
PLAIN = {'Bourgogne Gamay': 'r', 'Rosé, Gris': 'o'}

L1_ADD = {"Crémant d'Alsace", 'Crémant de Bourgogne', "Rosé d'Anjou", 'Barsac', 'Clairette de Die', 'Blanquette de Limoux', 'Montrachet',
          'Muscat de Rivesaltes', 'Chambertin', 'Romanée-Conti', 'Pouilly-Sur-Loire'}
L1_OUT = {'Banyuls', 'Condrieu'}
L2_ADD = {'Banyuls', 'Condrieu', 'Crémant de Limoux', 'Crémant de Bordeaux', 'Crémant de Die', "Cabernet d'Anjou", 'Sainte-Croix-du-Mont', 'Loupiac', 'Cérons',
          'Coteaux Champenois', 'Rosé de Loire', 'Bugey', 'Touraine', 'Cabardès', 'Menetou-Salon', 'Muscat de Lunel', 'Floc de Gascogne',
          'Côtes de Bergerac', 'Haut-Montravel', 'Rosé des Riceys', 'Saint-Péray'}


def level(n):
    if n in L1_ADD or (n in FAMOUS and n not in L1_OUT):
        return 1
    return 2 if n in KNOWN or n in L2_ADD else 3


def answer(a):
    n = a['name']
    if n in SPECIAL:
        codes, note = SPECIAL[n]
        req, _, opt = codes.partition('+')
        return req.split(), opt.split(), note
    codes = set()
    for w in a['wines']:
        if w['label'] in PLAIN:
            codes.add(PLAIN[w['label']])
            continue
        for part in w['label'].split(', '):
            assert part in SIMPLE, f'{n}: « {w["label"]} » needs an entry in SPECIAL'
            codes.add(SIMPLE[part])
    return list(codes), [], None


def bank():
    names = {a['name'] for a in AOCS}
    assert set(SPECIAL) <= names, set(SPECIAL) - names
    out = []
    for a in AOCS:
        req, opt, note = answer(a)
        assert req and set(req + opt) <= set(ORDER) and not set(req) & set(opt), a['name']
        out.append(dict(id=slug(a['name']), name=a['name'], lv=level(a['name']), region=(a['region'], REGION_EN.get(a['region'], a['region'])),
                        req=sorted(req, key=ORDER.index), opt=sorted(opt, key=ORDER.index), note=note, href=cep_link(a['name'])))
    return out


if __name__ == '__main__':
    from collections import Counter
    B = bank()
    print(len(B), Counter(b['lv'] for b in B))
    print(Counter(' '.join(b['req']) for b in B).most_common())
