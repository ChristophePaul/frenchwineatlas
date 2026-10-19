#!/usr/bin/env python3
"""Render a translated decree HTML into a stamped English PDF and wire it into the library.

Usage:
  python3 make_en_decree.py --html EN.html --slug <fr-slug> \
      --h1 "<header line1>" --h2 "<header line2>" \
      --f1 "<footer line1>" --f2 "<footer line2>" [--wire]

The HTML must contain only the flowing body (decree CSS + @page margins, NO running
header/footer) exactly like cour-cheverny-en.html; header/footer/page-numbers are stamped
here so they repeat cleanly on every page.  With --wire the manifest `en` field is set,
the worklist entry marked done, and the library regenerated.
"""
import argparse, os, subprocess, sys, json, tempfile
import fitz

DEST = os.path.dirname(os.path.abspath(__file__))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TNR = "/System/Library/Fonts/Supplemental/Times New Roman.ttf"
TNI = "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf"

def render(html, out_pdf):
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    "--print-to-pdf=" + out_pdf, html],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stamp(raw_pdf, out_pdf, h1, h2, f1, f2):
    d = fitz.open(raw_pdf)
    n = d.page_count
    for i, pg in enumerate(d):
        if h1: pg.insert_text((70.9, 44.6),  h1, fontfile=TNI, fontname="TNI", fontsize=10)
        if h2: pg.insert_text((70.9, 56.1),  h2, fontfile=TNI, fontname="TNI", fontsize=10)
        if f1: pg.insert_text((70.9, 792.7), f1, fontfile=TNI, fontname="TNI", fontsize=10)
        if f2: pg.insert_text((70.9, 804.1), f2, fontfile=TNI, fontname="TNI", fontsize=10)
        pg.insert_text((504.84, 793.62), f"{i+1}/{n}", fontfile=TNR, fontname="TNR", fontsize=11)
    d.subset_fonts()
    d.ez_save(out_pdf)
    d.close()
    return n

def wire(slug):
    # manifest: set en on the matching entry
    mp = os.path.join(DEST, "manifest.json")
    man = json.load(open(mp))
    tgt = "decrees/%s.pdf" % slug
    en  = "decrees/%s_en.pdf" % slug
    hit = False
    for it in man:
        if it["file"] == tgt:
            it["en"] = en; hit = True
    json.dump(man, open(mp, "w"), ensure_ascii=False, indent=0)
    # worklist: mark done
    wp = os.path.join(DEST, "_translate_worklist.json")
    if os.path.exists(wp):
        wl = json.load(open(wp))
        for w in wl:
            if w["slug"] == slug: w["done"] = True
        json.dump(wl, open(wp, "w"), ensure_ascii=False, indent=1)
    # regenerate library
    gen = os.path.join(os.path.dirname(DEST), "AOC_Decree", "gen_library.py")
    # gen_library.py lives in scratchpad normally; try local copy first
    local_gen = os.path.join(DEST, "gen_library.py")
    g = local_gen if os.path.exists(local_gen) else gen
    if os.path.exists(g):
        subprocess.run([sys.executable, g], check=True)
    return hit

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", required=True)
    ap.add_argument("--slug", required=True)
    ap.add_argument("--h1", default="")
    ap.add_argument("--h2", default="")
    ap.add_argument("--f1", default="")
    ap.add_argument("--f2", default="")
    ap.add_argument("--wire", action="store_true")
    a = ap.parse_args()
    out = os.path.join(DEST, "decrees", "%s_en.pdf" % a.slug)
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as t:
        raw = t.name
    render(a.html, raw)
    n = stamp(raw, out, a.h1, a.h2, a.f1, a.f2)
    os.unlink(raw)
    print("rendered %s -> %s (%d pages)" % (a.slug, out, n))
    if a.wire:
        ok = wire(a.slug)
        print("wired manifest:", ok, "| library regenerated")

if __name__ == "__main__":
    main()
