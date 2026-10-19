import re, glob, json, unicodedata, os
HERE = os.path.dirname(os.path.abspath(__file__))

COLOUR = {"B": "Blanc", "N": "Noir", "G": "Gris", "Rs": "Rosé", "Rg": "Rouge"}
COLOUR_WORDS = {"blanc": "Blanc", "blanche": "Blanche", "blancs": "Blanc", "noir": "Noir", "noire": "Noire",
                "gris": "Gris", "grise": "Grise", "rose": "Rosé", "rosé": "Rosé", "rouge": "Rouge", "rouges": "Rouge"}
SMALL = {"à", "de", "du", "des", "la", "le", "et"}
ALIAS = {"cinsault": "cinsaut", "cabernet sauvignon": "cabernet-sauvignon", "fer servadou": "fer",
         "mauzac blanc": "mauzac", "sauvignon blanc": "sauvignon", "semillon": "sémillon",
         "negrette": "négrette", "clairette rosé": "clairette rose", "égiodola": "egiodola",
         "muscat à petits grains rouges": "muscat à petits grains", "muscat à petits grains blancs": "muscat à petits grains",
         "manseng": "manseng noir", "lledonner pelut": "lledoner pelut", "castet": "castets",
         "maccabeu": "macabeu", "genovese": "genovèse", "génovese": "genovèse", "aleatico": "aléatico",
         "camaralet de lasseube": "camaralet", "clairette blanche": "clairette", "piquepoul": "piquepoul blanc",
         "ugni": "ugni blanc", "viognier blanc": "viognier", "pinot": "pinot noir", "mondeuse blanc": "mondeuse blanche",
         "roussane": "roussanne", "grenache": None}

def strip_acc(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")

def titlecase(s):
    out = []
    for i, w in enumerate(s.split(" ")):
        lw = w.lower()
        if i and lw in SMALL:
            out.append(lw); continue
        if i and lw.startswith(("d'", "l'")):
            out.append(lw[:2] + lw[2:].capitalize()); continue
        out.append("-".join(p[:1].upper() + p[1:] for p in lw.split("-")))
    return " ".join(out)

def canon(name, code):
    n = re.sub(r"\s+", " ", name.replace("’", "'").strip().lower())
    a = ALIAS.get(n, n)
    if a is None:  # bare "grenache" -> by colour
        a = {"N": "grenache", "B": "grenache blanc", "G": "grenache gris"}[code]
    # mondeuse B -> mondeuse blanche ; mondeuse N -> mondeuse
    if a == "mondeuse" and code == "B": a = "mondeuse blanche"
    if a == "carignan" and code == "B": a = "carignan blanc"
    if a == "terret" and code == "B": a = "terret blanc"
    if a == "terret" and code == "N": a = "terret noir"
    if a == "piquepoul blanc" and code == "N": a = "piquepoul noir"
    if a == "pinot noir" and code == "G": a = "pinot gris"
    if a == "sauvignon" and code == "G": a = "sauvignon gris"
    if a == "clairette" and code == "Rs": a = "clairette rose"
    if a == "grenache" and code == "B": a = "grenache blanc"
    if a == "grenache" and code == "G": a = "grenache gris"
    if a == "ugni blanc" and code == "Rs": a = "ugni rosé"
    return a

def display(key, code):
    words = key.split(" ")
    if any(strip_acc(w) in {strip_acc(c) for c in COLOUR_WORDS} for w in words):
        return " ".join(COLOUR_WORDS.get(w, w) for w in titlecase(key).split(" ")) \
            .replace("Blanc", "Blanc").replace(" Rose", " Rosé")
    return f"{titlecase(key)} {COLOUR[code]}"

def gid(key, code):
    return re.sub(r"[^a-z0-9]+", "-", strip_acc(key.replace("œ","oe")).lower()).strip("-") + "-" + code.lower()

GRAPE_RE = re.compile(r"^(.*?)\s+(B|N|G|Rs|Rg)(?:/(P|C|S|A))?(?:\s+(.*))?$")

def parse_all():
    aocs = []
    for f in sorted(glob.glob(os.path.join(HERE, "data", "*.txt"))):
        cur = None
        for raw in open(f, encoding="utf-8"):
            line = raw.rstrip("\n").strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("= "):
                parts = [p.strip() for p in line[2:].split("|")]
                cur = {"name": parts[0], "region": parts[1], "cdc": parts[2] if len(parts) > 2 else "",
                       "src": parts[3] if len(parts) > 3 else "cdc", "wines": [], "notes": []}
                aocs.append(cur); continue
            if line.startswith("! "):
                cur["notes"].append(line[2:]); continue
            label, _, rest = line.partition(":")
            grapes = []
            for item in rest.split(";"):
                item = item.strip()
                if not item: continue
                m = GRAPE_RE.match(item)
                if not m:
                    raise ValueError(f"{f}: {cur['name']}: cannot parse '{item}'")
                name, code, role, pct = m.groups()
                key = canon(name, code)
                adapt = bool(pct and "adaptation" in pct)
                if pct: pct = pct.replace("(variété d'adaptation)", "").strip() or None
                grapes.append({"id": gid(key, code), "key": key, "code": code,
                               "role": role or "", "pct": pct or "", "adapt": adapt})
            cur["wines"].append({"label": label.strip(), "grapes": grapes})
    return aocs

if __name__ == "__main__":
    aocs = parse_all()
    g = {}
    for a in aocs:
        for w in a["wines"]:
            for x in w["grapes"]:
                g.setdefault(x["id"], (x["key"], x["code"]))
    print(len(aocs), "AOCs;", len(g), "grapes")
    for k, (key, code) in sorted(g.items()):
        print(k, "|", display(key, code))
