#!/usr/bin/env python3
"""Compare the immediate-proximity commune lists of a Burgundy decree with the standard
Chambertin lists and print @listop lines. Usage: prox_ops.py <slug> [pages]"""
import sys, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
def text(slug, pages=None):
    ocr = os.path.join(ROOT, "_ocr", slug + ".txt")
    if os.path.exists(ocr): t = open(ocr).read()
    else: t = subprocess.run([sys.executable, os.path.join(HERE, "extract_fr.py"), slug] + ([pages] if pages else []), capture_output=True, text=True).stdout
    t = re.sub(r"(?m)^(RUNNING:.*|=== p.*|\d+)$", " ", t)
    t = re.sub(r"(//|\*\*)?Procédure nationale d.opposition.*?(\d\d/\d\d/\d{4}|\d{4})", " ", t)
    t = t.replace("’", "'"); t = re.sub(r"-\s+", "-", t); t = re.sub(r"\s+", " ", t)
    return t
DEPTS = [("CO", r"Côte.d'Or"), ("RH", r"Rhône"), ("SL", r"Saône-et-Loire"), ("YO", r"Yonne")]
def lists(t):
    out = {}
    i = t.find("proximité immédiate, définie")
    if i < 0: i = t.find("proximité immédiate")
    t = t[i:].replace("Saint-Vérand Sainte-Paule", "Saint-Vérand, Sainte-Paule")
    for i, (k, pat) in enumerate(DEPTS):
        m = re.search(r"(?:Département|département) d(?:e la |u |e |e l')" + pat + r"\s*:\s*(.*?)(?:[;.]?\s*-?\s*(?:Dans le )?(?:Département|département) d|V\.\s*-?\s*Encépagement|$)", t)
        if not m: continue
        items = [re.sub(r"\s+", " ", x).strip(" ;.") for x in re.split(r",|\set\s", m.group(1))]
        out[k] = [x for x in items if x]
    return out
ref = lists(text("bourgogne_cote_de_nuits_chambertin"))
tgt = lists(text(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
def inv(x):
    m = re.match(r"(.*?)\s*\((La|Le|Les|L')\)$", x.strip())
    return (m.group(2) + ("" if m.group(2) == "L'" else " ") + m.group(1)) if m else x
norm0 = lambda x: re.sub(r"[^a-z]", "", x.lower().replace("é","e").replace("è","e").replace("ê","e").replace("î","i").replace("ô","o").replace("â","a").replace("œ","oe"))
norm = lambda x: norm0(inv(x)).replace("serein","serin").replace("tonnerrois","tonnerois")
for k, _ in DEPTS:
    if k not in tgt: print(f"# {k}: not found"); continue
    R = {norm(x): x for x in ref[k]}; T = {norm(x): x for x in tgt[k]}
    rem = [R[x] for x in R if x not in T]; add = [T[x] for x in T if x not in R]
    if not rem and not add: print(f"@@BG_PROX_{k}")
    else: print(f"@listop BG_PROX_{k} | " + " | ".join(["-" + r for r in rem] + ["+" + a for a in add]))
