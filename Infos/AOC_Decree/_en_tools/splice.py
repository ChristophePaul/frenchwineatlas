#!/usr/bin/env python3
"""Replace the text between two markers (start inclusive, end exclusive) in _en_src/<slug>.txt with a file's content.
Usage: splice.py <slug> "<start marker>" "<end marker>" <file>"""
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
slug, a, b, f = sys.argv[1:5]
p = os.path.join(ROOT, "_en_src", slug + ".txt"); t = open(p, encoding="utf-8").read()
i = t.index(a); j = t.index(b, i)
t = t[:i] + open(f, encoding="utf-8").read().rstrip("\n") + "\n" + t[j:]
open(p, "w", encoding="utf-8").write(t); print("spliced", slug)
