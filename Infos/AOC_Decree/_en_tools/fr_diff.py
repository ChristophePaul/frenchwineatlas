#!/usr/bin/env python3
"""Sentence-level diff of two French decrees (names normalised).
Usage: fr_diff.py <ref_slug> <target_slug> "<Ref name>" "<Target name>" [pages]"""
import sys, os, re, subprocess, difflib
HERE = os.path.dirname(os.path.abspath(__file__))
def text(slug, pages=None):
    ocr = os.path.join(os.path.dirname(HERE), "_ocr", slug + ".txt")
    if os.path.exists(ocr): return open(ocr).read().replace("'", "’")
    args = [sys.executable, os.path.join(HERE, "extract_fr.py"), slug] + ([pages] if pages else [])
    t = subprocess.run(args, capture_output=True, text=True).stdout
    t = re.sub(r"(?m)^(RUNNING:.*|=== p\d+)$", "", t)
    return t
def sents(t, name):
    for n in sorted(set([name, name.upper(), name.lower()]), key=len, reverse=True):
        t = t.replace(n, "§NAME§")
    t = re.sub(r"(//|\*\*)?Procédure nationale d.opposition.*?(\d\d/\d\d/\d{4}|\d{4})", " ", t)
    t = re.sub(r"\*\*|//", " ", t)
    t = re.sub(r"\s+", " ", t)
    t = re.sub(r"(\w)- (\w)", r"\1-\2", t)
    t = t.replace("° C", " °C").replace("  ", " ")
    return [x.strip() for x in re.split(r"(?<=[.;:])\s+(?=[-–―A-ZÀ-Ý«a-z0-9])", t) if x.strip()]
def wdiff(x, y):
    xa, ya = x.split(), y.split(); out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, xa, ya).get_opcodes():
        if tag == "equal": out.append(" ".join(xa[i1:i2]) if i2 - i1 < 12 else " ".join(xa[i1:i1+4]) + " … " + " ".join(xa[i2-4:i2]))
        else: out.append("[-" + " ".join(xa[i1:i2]) + "-]{+" + " ".join(ya[j1:j2]) + "+}")
    return " ".join(out)
def key(x):
    x = re.sub(r"[^0-9a-zà-ÿ~§]", "", x.lower().replace("ème", "").replace("ère", "").replace("structurants", "structurant").replace("dorée", "doré").replace("agréés", "agrées"))
    return x
a = sents(text(sys.argv[1]), sys.argv[3])
b = sents(text(sys.argv[2], sys.argv[5] if len(sys.argv) > 5 else None), sys.argv[4])
# merge to key-equal: drop pairs equal after normalisation by comparing joined keys of whole blocks
sm = difflib.SequenceMatcher(None, [key(x) for x in a], [key(y) for y in b], autojunk=False)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal": continue
    A, B = a[i1:i2], b[j1:j2]
    if key(" ".join(A)) == key(" ".join(B)): continue
    print(f"@@ {tag} after: {a[i1-1][:80] if i1 else '^'}")
    if tag == "replace" and len(A) == len(B):
        for x, y in zip(A, B):
            if difflib.SequenceMatcher(None, x, y).ratio() > 0.6: print("  ~ " + wdiff(x, y))
            else: print("  - " + x + "\n  + " + y)
    else:
        for x in A: print("  - " + x)
        for y in B: print("  + " + y)
