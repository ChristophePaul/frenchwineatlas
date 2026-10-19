#!/usr/bin/env python3
"""Build assets/nav.js — the site-wide menu (site map + script) — from the pages in WEB Site/.

    python3 assets/nav_build.py

Rerun after adding, renaming or removing a page. The script (template) lives in nav.src.js;
the page tree is generated here. Pages not matched by a rule below land in « Autres / Other »,
so a new page is never missing from the menu — give it a proper home by adding a rule.
nav.js is loaded on every page by theme.js, so no page needs editing.
"""
import html, json, pathlib, re, unicodedata

SITE = pathlib.Path(__file__).resolve().parent.parent
ASSETS = SITE / 'assets'


def title_of(p):
    t = p.read_text(errors='ignore')
    m = re.search(r'<title>(.*?)</title>', t, re.S)
    return html.unescape(m.group(1).strip()) if m else p.stem


def name_of(p):
    """Short label: the part of the <title> before ' — '."""
    return re.split(r'\s+—\s+', title_of(p))[0].strip()


def fold(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn').lower()


pages = sorted(str(p.relative_to(SITE)) for p in SITE.rglob('*.html')
               if '_source' not in p.parts and '_backups' not in p.parts and not p.name.startswith('_'))
used = set()


def item(path, fr=None, en=None):
    assert path in pages, path
    used.add(path)
    fr = fr or name_of(SITE / path)
    return [path, fr] if not en or en == fr else [path, fr, en]


def grp(fr, en, items=None, groups=None):
    g = {'fr': fr, 'en': en}
    if items: g['items'] = items
    if groups: g['groups'] = groups
    return g


def folder(d, first=()):
    """Every page of a folder, overview pages first, then alphabetical."""
    ps = [p for p in pages if p.rsplit('/', 1)[0] == d]
    head = [p for f in first for p in ps if p.endswith('/' + f)]
    rest = sorted((p for p in ps if p not in head), key=lambda p: fold(name_of(SITE / p)))
    return head + rest


# ---------- regional maps ----------
R = lambda path, fr, en=None: item(path, fr, en)
regions = grp('Cartes régionales', 'Regional maps', groups=[
    grp('Nord-Est', 'North-East', [
        R('Alsace.html', 'Alsace'), R('Lorraine.html', 'Lorraine'), R('Champagne.html', 'Champagne')]),
    grp('Bourgogne, Beaujolais & Lyonnais', 'Burgundy, Beaujolais & Lyonnais', [
        R('Bourgogne Regions/Chablis_et_de_l_Auxerrois.html', 'Chablis & Auxerrois'),
        R("Bourgogne Regions/Cote-d_Or.html", "Côte-d'Or"),
        R('Bourgogne Regions/Saone-et-Loire.html', 'Saône-et-Loire'),
        R('Bourgogne Regions/Beaujolais.html', 'Beaujolais & Lyonnais', 'Beaujolais & Lyonnais')]),
    grp('Jura & Savoie', 'Jura & Savoie', [
        R('Jura.html', 'Jura'), R('Savoie_et_du_Bugey.html', 'Savoie & Bugey')]),
    grp('Val de Loire', 'Loire Valley', [
        R('Pays_Nantais.html', 'Pays Nantais'),
        R('Anjou_et_de_Touraine.html', 'Anjou, Saumur & Touraine'),
        R('Centre-Loire.html', 'Centre-Loire'),
        R('Auvergne_et_du_Haut_Val_de_Loire.html', 'Auvergne & Haut Val de Loire', 'Auvergne & Upper Loire')]),
    grp('Vallée du Rhône', 'Rhône Valley', [
        R('Rhone-septentrional.html', 'Rhône septentrional', 'Northern Rhône'),
        R('Rhone-meridional.html', 'Rhône méridional', 'Southern Rhône')]),
    grp('Provence, Corse & Languedoc-Roussillon', 'Provence, Corsica & Languedoc-Roussillon', [
        R('Provence-Cote-d-Azur.html', "Provence & Côte d'Azur"),
        R('Corse.html', 'Corse', 'Corsica'),
        R('Languedoc.html', 'Languedoc'),
        R('Malepere-et-Limoux.html', 'Malepère & Limoux'),
        R('Roussillon.html', 'Roussillon')]),
    grp('Bordeaux & Sud-Ouest', 'Bordeaux & South-West', [
        R('Bordeaux.html', 'Bordeaux'),
        R('South West Bergerac.html', 'Sud-Ouest · Bergerac', 'South-West · Bergerac'),
        R('South-West Toulouse.html', 'Sud-Ouest · Toulouse', 'South-West · Toulouse'),
        R('Landes_et_Pyrenees_Occidentales.html', 'Landes & Pyrénées-Atlantiques', 'Landes & Western Pyrenees'),
        R('Cognac.html', 'Cognac')]),
])

# ---------- Burgundy climats, north → south ----------
CL = 'Bourgogne Regions/Bourgogne climats'
climat_pages = {re.split(r'\s+—\s+', title_of(SITE / p))[0]: p for p in folder(CL)}


def climats(names):
    out = []
    for n in names:
        p = climat_pages.get(n) or next((p for k, p in climat_pages.items() if fold(k).startswith(fold(n))), None)   # exact name first (Chablis ≠ Chablis Grand Cru)
        if p: out.append(item(p, re.split(r'\s+—\s+', title_of(SITE / p))[0]))
    return out


climats_grp = grp('Climats de Bourgogne', 'Burgundy climats', groups=[
    grp('Chablis', 'Chablis', climats(['Chablis', 'Chablis Grand Cru'])),
    grp('Côte de Nuits', 'Côte de Nuits', climats([
        'Fixin', 'Gevrey', 'Morey', 'Chambolle', 'Vougeot', 'Vosne', 'Nuits'])),
    grp('Côte de Beaune', 'Côte de Beaune', climats([
        'Ladoix', 'Aloxe', 'Pernand', 'Savigny', 'Beaune', 'Pommard', 'Volnay', 'Monthélie',
        'Auxey', 'Meursault', 'Puligny', 'Chassagne', 'Saint-Aubin', 'Santenay', 'Maranges'])),
    grp('Côte Chalonnaise', 'Côte Chalonnaise', climats(['Rully', 'Mercurey', 'Givry', 'Montagny'])),
    grp('Mâconnais', 'Mâconnais', climats(['Pouilly-Fuissé', 'Pouilly-Vinzelles', 'Pouilly-Loché'])),
])

# ---------- cadastral plans ----------
PC = 'Plan Cadastraux/'
cad = lambda d, first=(): [item(p) for p in folder(PC + d, first)]
cadastre = grp('Plans cadastraux', 'Cadastral maps', groups=[
    grp('Bordeaux · Rive gauche', 'Bordeaux · Left Bank', cad('Bordeaux_LeftBank')),
    grp('Bordeaux · Rive droite', 'Bordeaux · Right Bank', cad('Bordeaux_RightBank')),
    grp('Bordeaux · Entre-deux-Mers', 'Bordeaux · Entre-deux-Mers', cad('Bordeaux_EntreDeuxMers')),
    grp('Bordeaux · Côtes de Bordeaux', 'Bordeaux · Côtes de Bordeaux', cad('Bordeaux_CotesDeBordeaux')),
    grp('Rhône septentrional', 'Northern Rhône', cad('Cotes_du_Rhone')),
    grp('Rhône méridional', 'Southern Rhône', cad('Cotes_du_Rhone_Sud', ['Cotes-du-Rhone-Villages.html'])),
    grp('Chablis & Auxerrois', 'Chablis & Auxerrois', cad('Chablis_Auxerrois', ['Petit-Chablis.html', 'Irancy.html', 'Saint-Bris.html', 'Vezelay.html'])),
    grp('Beaujolais & Lyonnais', 'Beaujolais & Lyonnais', cad('Beaujolais_Lyonnais')),
    grp('Côte chalonnaise', 'Côte Chalonnaise', cad('Cote_Chalonnaise', ['Bourgogne-Cote-Chalonnaise.html'])),
    grp('Mâconnais', 'Mâconnais', cad('Maconnais', ['Macon.html', 'Macon-Villages.html'])),
    grp('Savoie', 'Savoie', cad('Savoie', ['Vin-de-Savoie.html', 'Roussette-de-Savoie.html', 'Seyssel.html'])),
    grp('Bugey', 'Bugey', cad('Bugey', ['Bugey.html', 'Roussette-du-Bugey.html'])),
    grp('Jura', 'Jura', cad('Jura', ['Cotes-du-Jura.html', 'Arbois.html', 'Arbois-Pupillin.html', 'Chateau-Chalon.html', 'L-Etoile.html'])),
    grp('Loire · Pays nantais', 'Loire · Pays nantais', cad('Loire_Pays_Nantais')),
    grp('Loire · Anjou-Touraine', 'Loire · Anjou & Touraine', cad('Loire_Anjou_Touraine')),
    grp('Loire · Centre-Loire', 'Loire · Centre-Loire', cad('Loire_Centre')),
    grp('Auvergne et haut val de Loire', 'Auvergne & upper Loire', cad('Auvergne_Haut_Val_de_Loire')),
    grp('Sud-Ouest · Piémont pyrénéen', 'South-West · Pyrenean foothills', cad('Sud_Ouest_Pyrenees')),
    grp('Sud-Ouest · Haut-Pays', 'South-West · Haut-Pays', cad('Sud_Ouest_Haut_Pays')),
    grp('Sud-Ouest · Bergeracois et Garonne', 'South-West · Bergerac & Garonne', cad('Sud_Ouest_Bergerac_Garonne')),
    grp('Languedoc', 'Languedoc', cad('Languedoc')),
    grp('Malepère, Cabardès et Limoux', 'Malepère, Cabardès & Limoux', cad('Malepere_et_Limoux')),
    grp('Roussillon', 'Roussillon', cad('Roussillon', ['Cotes-du-Roussillon.html', 'Cotes-du-Roussillon-Villages.html'])),
    grp('Provence', 'Provence', cad('Provence')),
    grp('Corse', 'Corsica', cad('Corse', ['Vin-de-Corse.html'])),
    grp('Lorraine', 'Lorraine', cad('Lorraine', ['Moselle.html', 'Cotes-de-Toul.html'])),
    grp('Alsace · Grands crus', 'Alsace · Grands crus',
        [item(PC + 'Alsace_Grands_Crus/Alsace-Grands-Crus.html', 'Les 51 grands crus', 'All 51 grands crus')]
        + [item(p) for p in folder(PC + 'Alsace_Grands_Crus') if not p.endswith('/Alsace-Grands-Crus.html')]),
    grp('Champagne · Grands crus', 'Champagne · Grands crus',
        [item(PC + 'Champagne_Grands_Crus/Champagne-Grands-Crus.html', 'Les 17 grands crus', 'All 17 grands crus')]
        + [item(p) for p in folder(PC + 'Champagne_Grands_Crus') if not p.endswith('/Champagne-Grands-Crus.html')]),
])

# ---------- learning pages ----------
I = 'Infos/'
infos = grp('Comprendre le vin', 'Wine knowledge', groups=[
    grp('Appellations & cépages', 'Appellations & grapes', [
        item(I + 'Vine_and_Vineyard/Cepages/Cepages_et_Appellations.html', 'Cépages & appellations', 'Grapes & appellations'),
        item(I + 'Categories_of_French_Wines.html', 'Comprendre l’AOC-AOP', 'Understanding AOC-AOP'),
        item(I + 'AOC_Decree/AOC_Decree.html', "Anatomie d'un décret AOC", 'Anatomy of an AOC decree'),
        item(I + 'AOC_Decree/AOC_Library.html', 'Bibliothèque des décrets AOC', 'AOC decree library'),
        item(I + 'Vintages/Vintage_Chart.html', 'Millésimes', 'Vintage chart'),
        item(I + 'French_Wine_in_Numbers.html', 'La France viticole en chiffres', 'French wine in numbers'),
        item(I + 'Bottle_Sizes.html', 'Formats de bouteilles', 'Bottle sizes'),
        item(I + 'Crus_Classifications.html', 'Les classifications des crus', 'Crus & grands crus classifications'),
        item(I + 'Wine_Label/Wine_Label.html', 'Apprendre à lire… une étiquette', 'Learning to read… a wine label'),
        item(I + 'Tasting/Wine_Tasting.html', 'Déguster le vin', 'Tasting wine'),
        item(I + 'History/History_of_Wine.html', 'Histoire du vin', 'A history of wine'),
        item(I + 'Confidentialite.html', 'Confidentialité & mon compte', 'Privacy & my account')]),
    grp('La vigne & le vignoble', 'The vine & the vineyard', [
        item(I + 'Vine_and_Vineyard/Vine_Plant.html', '1 · La plante vigne', '1 · The vine plant'),
        item(I + 'Vine_and_Vineyard/Vine_Cycle.html', '2 · Le cycle de la vigne', '2 · The vine’s year'),
        item(I + 'Vine_and_Vineyard/Vine_Terroir.html', '3 · Terroir & site', '3 · Terroir & site'),
        item(I + 'Vine_and_Vineyard/Vine_Planting.html', '4 · Plantation & vie du vignoble', '4 · Planting & the life of a vineyard'),
        item(I + 'Vine_and_Vineyard/Vine_Pruning.html', '5 · Taille & modes de conduite', '5 · Training & pruning'),
        item(I + 'Vine_and_Vineyard/Vine_Canopy.html', '6 · Travaux en vert & du sol', '6 · Canopy & soil work'),
        item(I + 'Vine_and_Vineyard/Vine_Threats.html', '7 · Les ennemis de la vigne', '7 · Threats to the vine'),
        item(I + 'Vine_and_Vineyard/Vine_Farming.html', '8 · Philosophies culturales', '8 · Farming philosophies'),
        item(I + 'Vine_and_Vineyard/Vine_Harvest.html', '9 · Les vendanges', '9 · Harvest'),
        item(I + 'Vine_and_Vineyard/Vine_Glossary.html', '10 · Glossaire', '10 · Glossary')]),
    grp('Vinification', 'Wine making', [
        item(I + "How it's made/How wine is made.html", 'Vinification (interactif)', 'How wine is made (interactive)'),
        item(I + "How it's made/How wine is made - Illustrated.html", 'Vinification illustrée', 'How wine is made (illustrated)'),
        item(I + "How it's made/How sparkling wine is made.html", 'Vins effervescents', 'Sparkling wine'),
        item(I + "How it's made/How brandy is made.html", 'Eaux-de-vie', 'Brandy'),
        item(I + 'Barrel_Making/Barrel_Making.html', 'Comment naît une barrique', 'Birth of a wine barrel')]),
    grp('Littérature', 'Literature', [
        item(I + 'Literature/Wine_Quotes.html', 'Le vin en citations', 'Wine in quotations')]),
    grp('Jeux', 'Games', [
        item(I + 'Literature/Jeux.html', 'Tous les jeux', 'All games'),
        item(I + 'Literature/Wine_Quiz.html', 'Le grand quiz du vin', 'The great wine quiz'),
        item(I + 'Literature/Taste_Quiz.html', 'Goûtez votre savoir', 'Taste your knowledge'),
        item(I + 'Literature/Map_Game.html', 'Placez l’AOC', 'Pin the AOC'),
        item(I + 'Literature/Bon_Cep.html', 'Le bon cep', 'Grape Expectations'),
        item(I + 'Literature/IGP_Game.html', 'Au pays des IGP', 'Lost in the Pays')]),
    grp('Chimie du vin', 'Wine chemistry', [
        item(I + 'wine_chemistry_html/wine_chemistry_web.html', 'Chimie du vin', 'Wine chemistry'),
        item(I + 'wine_chemistry_html/wine_compound_count_web.html', 'Le vin en chiffres (composés)', 'Wine in numbers (compounds)')]),
])

top = [item('index.html', 'Accueil', 'Home'),
       item('Vignobles de France — Carte de France.html', 'Carte de France', 'Map of France'),
       item('Vignobles de France — Carte des IGP.html', 'Carte des IGP', 'IGP map')]

tree = {'top': top, 'groups': [regions, climats_grp, cadastre, infos]}
left = [p for p in pages if p not in used]
if left:
    tree['groups'].append(grp('Autres', 'Other', [item(p) for p in left]))
    print('unfiled (→ Autres):', *left, sep='\n  ')

src = (ASSETS / 'nav.src.js').read_text()
out = src.replace('/*@SITE@*/null', json.dumps(tree, ensure_ascii=False, separators=(',', ':')))
(ASSETS / 'nav.js').write_text('/* GENERATED by nav_build.py from nav.src.js — edit those, not this file. */\n' + out)
print(f'nav.js: {len(used)} pages, {len(out)//1024} KB')
