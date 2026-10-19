import json, re, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from parse import parse_all, display, strip_acc, COLOUR
from desc import D
from desc_en import E

OUT = sys.argv[1]
vv = json.load(open(os.path.join(HERE, "vinvigne.json")))
ha_raw = json.load(open(os.path.join(HERE, "ha.json")))
HA_MAP = {"ALIGOTE": "aligote-b", "CABERNET FRANC": "cabernet-franc-n", "CABERNET SAUVIGNON": "cabernet-sauvignon-n",
          "CARIGNAN": "carignan-n", "CHARDONNAY": "chardonnay-b", "CHASSELAS": "chasselas-b", "CHENIN BLANC": "chenin-b",
          "CINSAUT": "cinsaut-n", "CLAIRETTE": "clairette-b", "COLOMBARD": "colombard-b", "GAMAY NOIR A JUS BLANC": "gamay-n",
          "GEWURZTRAMINER": "gewurztraminer-rs", "GRENACHE BLANC": "grenache-blanc-b", "GRENACHE GRIS": "grenache-gris-g",
          "GRENACHE NOIR": "grenache-n", "MALBEC OR COT": "cot-n", "MARSANNE": "marsanne-b", "MAUZAC": "mauzac-b",
          "MELON": "melon-b", "MERLOT": "merlot-n", "MEUNIER": "meunier-n", "MONDEUSE": "mondeuse-n", "MOURVÈDRE": "mourvedre-n",
          "MUSCADELLE": "muscadelle-b", "MUSCAT BLANC A PETIT GRAINS": "muscat-a-petits-grains-b", "MUSCAT OTTONEL": "muscat-ottonel-b",
          "NÉGRETTE": "negrette-n", "PINOT BLANC": "pinot-blanc-b", "PINOT GRIS": "pinot-gris-g", "PINOT NOIR": "pinot-noir-n",
          "PETIT MANSENG": "petit-manseng-b", "POULSARD": "poulsard-n", "RIESLING": "riesling-b", "ROMORANTIN BLANC": "romorantin-b",
          "ROUSSANE": "roussanne-b", "SAUVIGNON BLANC": "sauvignon-b", "SAVAGNIN": "savagnin-b", "SÉMILLON": "semillon-b",
          "SYLVANER": "sylvaner-b", "SYRAH": "syrah-n", "TANNAT": "tannat-n", "UGNI BLANC": "ugni-blanc-b",
          "VERMENTINO": "vermentino-b", "VIOGNIER": "viognier-b"}
HA = {HA_MAP[n]: int(re.sub(r"[^\d]", "", h)) for n, h, _ in ha_raw if n in HA_MAP}

EXTRA_SYN = {"cot-n": "Malbec, Auxerrois (Cahors), Pressac", "vermentino-b": "Rolle, Malvoisie de Corse",
             "fer-n": "Fer Servadou, Mansois, Braucol, Pinenc", "melon-b": "Melon de Bourgogne, Muscadet",
             "sauvignon-b": "Sauvignon Blanc, Blanc Fumé", "chenin-b": "Chenin Blanc, Pineau de la Loire",
             "nielluccio-n": "Sangiovese", "ugni-blanc-b": "Trebbiano, Saint-Émilion (Charentes)",
             "macabeu-b": "Macabeo, Viura", "tourbat-b": "Malvoisie du Roussillon", "alvarinho-b": "Albariño",
             "lledoner-pelut-n": "Grenache poilu", "picardan-b": "Araignan", "morrastel-n": "Minustellu, Graciano",
             "brun-argente-n": "Camarèse, Vaccarèse", "poulsard-n": "Ploussard", "altesse-b": "Roussette",
             "orbois-b": "Menu Pineau", "gewurztraminer-rs": "Traminer aromatique", "savagnin-b": "Naturé, Traminer",
             "savagnin-rose-rs": "Klevener de Heiligenstein", "barbaroux-rs": "Barbarossa", "sciaccarello-n": "Sciaccarellu",
             "calabrese-n": "Nero d'Avola", "teoulier-n": "Manosquin", "saint-come-b": "Rousselou",
             "fuella-nera-n": "Folle Noire", "abouriou-n": "Gamay Saint-Laurent", "rivairenc-n": "Aspiran Noir",
             "terret-gris-g": "Terret-Bourret", "oeillade-n": "Œillade noire", "camaralet-b": "Camaralet de Lasseube",
             "pinot-gris-g": "Malvoisie (Loire), Tokay (anc. Alsace)", "meunier-n": "Pinot Meunier",
             "grolleau-n": "Groslot", "muscat-d-alexandrie-b": "Muscat romain", "gamay-n": "Gamay noir à jus blanc",
             "corbeau-n": "Douce Noire, Charbono", "souvignier-gris-rs": "Souvignier Gris"}

REGION_ORDER = ["Alsace-Lorraine", "Beaujolais", "Bordeaux", "Bourgogne", "Champagne", "Charentes", "Corse", "Jura",
                "Languedoc", "Provence", "Roussillon", "Savoie-Bugey", "Sud-Ouest", "Val de Loire", "Vallée du Rhône"]
AOC_ALIASES = {"Clos de Vougeot": "Clos Vougeot", "Crozes-Hermitage": "Crozes-Ermitage",
               "Hermitage": "Ermitage, L'Hermitage", "Moulis-en-Médoc": "Moulis", "Pouilly-Fumé": "Blanc Fumé de Pouilly",
               "Muscat de Frontignan": "Frontignan, Vin de Frontignan", "Vin de Corse": "Corse", "Vin de Savoie": "Savoie",
               "Côtes de Bourg": "Bourg, Bourgeais", "Bellet": "Vin de Bellet", "Entraygues-Le Fel": "Entraygues et le Fel",
               "Mâcon": "Mâcon-Villages", "Chablis": "Chablis Premier Cru", "Premières Côtes de Bordeaux": "",
               "Bourgogne": "Bourgogne Côte d'Or, Hautes-Côtes de Beaune, Hautes-Côtes de Nuits, Côte Chalonnaise, Épineuil",
               "Muscadet Sèvre et Maine": "Clisson, Gorges, Le Pallet, Château-Thébaud, Goulaine, Monnières-Saint-Fiacre, Mouzillon-Tillières",
               "Côtes de Bordeaux": "Blaye, Côtes de Blaye, Sainte-Foy-Bordeaux, Sainte-Foy Côtes de Bordeaux, Blaye Côtes de Bordeaux, Cadillac Côtes de Bordeaux, Castillon Côtes de Bordeaux, Francs Côtes de Bordeaux",
               "Languedoc": "Pézenas, Grès de Montpellier, Saint-Saturnin, Montpeyroux, Cabrières, Sommières",
               "Grés de Montpellier": "Grès de Montpellier (ancienne dénomination de l'AOC Languedoc)", "Laudun": "Côtes du Rhône Villages Laudun (ancien nom)",
               "Boutenac": "Corbières-Boutenac (ancien nom)", "Graves": "", "Anjou Brissac": "Anjou Villages Brissac (ancien nom)", "La Livinière": "Minervois-La Livinière (ancien nom)",
               "Coulée de Serrant": "Savennières Coulée de Serrant (ancien nom)",
               "Vin de Savoie ": ""}

aocs = parse_all()
grapes = {}
for a in aocs:
    ids = set()
    for w in a["wines"]:
        for x in w["grapes"]:
            ids.add(x["id"])
            grapes.setdefault(x["id"], {"key": x["key"], "code": x["code"]})
    a["single"] = len(ids) == 1

def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", strip_acc(s.lower()).replace("œ", "oe")).strip("-")

G = []
for gid_, g in grapes.items():
    info = vv.get(gid_, {})
    syn = EXTRA_SYN.get(gid_, "")
    if info.get("syn"):
        syn = (syn + ", " if syn else "") + info["syn"]
    if gid_ not in D or gid_ not in E:
        print("NO DESC", gid_)
    G.append({"id": gid_, "n": display(g["key"], g["code"]), "c": g["code"],
              "fr": D.get(gid_, ""), "en": E.get(gid_, ""), "syn": syn.strip(", "),
              "orig": info.get("origin", ""), "ha": HA.get(gid_)})
G.sort(key=lambda x: strip_acc(x["n"]).lower())

A = []
for a in aocs:
    A.append({"id": slug(a["name"]), "n": a["name"], "r": a["region"], "cdc": a["cdc"], "src": a["src"],
              "one": a["single"], "aka": AOC_ALIASES.get(a["name"], ""), "notes": a["notes"],
              "w": [{"l": w["label"], "g": [[x["id"], x["role"], x["pct"], 1 if x["adapt"] else 0] for x in w["grapes"]]}
                    for w in a["wines"]]})
A.sort(key=lambda x: strip_acc(x["n"]).lower())
assert len({a["id"] for a in A}) == len(A), "duplicate AOC ids"

data = {"grapes": G, "aocs": A, "regions": REGION_ORDER}
tpl = open(os.path.join(HERE, "template.html"), encoding="utf-8").read()
html = tpl.replace("/*__DATA__*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":")))
open(OUT, "w", encoding="utf-8").write(html)
print(len(G), "grapes,", len(A), "AOCs ->", OUT, f"{len(html)//1024} KB")
print("single-varietal AOCs:", sum(a["one"] for a in A))
