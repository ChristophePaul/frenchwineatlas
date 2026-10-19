#!/usr/bin/env python3
"""Clone an English source to a sibling appellation and apply literal edits.
Usage: clone_en.py <src_slug> <dst_slug> "<Src name>" "<Dst name>" [old=>new ...]
Replaces “Src” / “SRC” (quoted forms only) and then each old=>new literal (must match once or more)."""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src, dst, a, b = sys.argv[1:5]
t = open(os.path.join(ROOT, "_en_src", src + ".txt"), encoding="utf-8").read()
for x, y in [(f"“{a}”", f"“{b}”"), (f"“{a.upper()}”", f"“{b.upper()}”"), (f"– “{a}”", f"– “{b}”")]:
    t = t.replace(x, y)
for e in sys.argv[5:]:
    old, new = e.split("=>", 1)
    if old not in t: sys.exit("NOT FOUND: " + old)
    t = t.replace(old, new)
open(os.path.join(ROOT, "_en_src", dst + ".txt"), "w", encoding="utf-8").write(t)
print("wrote", dst)
