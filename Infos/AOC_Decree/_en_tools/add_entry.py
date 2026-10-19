#!/usr/bin/env python3
"""Add a French CDC PDF that is missing from the library.
Usage: add_entry.py <src.pdf> <slug> <region> <sub> <appellation>"""
import sys, os, json, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src, slug, region, sub, app = sys.argv[1:6]
dst = os.path.join(ROOT, "decrees", slug + ".pdf")
shutil.copyfile(src, dst)
mp = os.path.join(ROOT, "manifest.json"); man = json.load(open(mp))
f = "decrees/%s.pdf" % slug
man = [m for m in man if m["file"] != f]
man.append({"region": region, "sub": sub, "appellation": app, "file": f,
            "sizeKB": round(os.path.getsize(dst) / 1024), "en": ""})
json.dump(man, open(mp, "w"), ensure_ascii=False, indent=0)
print("added", f)
