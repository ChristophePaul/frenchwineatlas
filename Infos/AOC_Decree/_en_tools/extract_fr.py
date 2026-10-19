#!/usr/bin/env python3
"""Dump a French decree PDF as compact text for translation.

Usage: python3 extract_fr.py <slug> [--raw]
Prints the running header/footer once, then the body page by page with
bold lines prefixed by '**' and italic lines by '//', blocks joined into paragraphs,
tables rendered as '| a | b |' rows.
"""
import sys, os, re, collections
import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
DEC = os.path.join(os.path.dirname(HERE), "decrees")

def main():
    slug = sys.argv[1]
    d = fitz.open(os.path.join(DEC, slug + ".pdf"))
    if len(sys.argv) > 2 and "-" in sys.argv[2]:          # page range, e.g. 1-13
        a, b = map(int, sys.argv[2].split("-")); d.select(list(range(a - 1, b)))
    H = d[0].rect.height
    # running header/footer = lines repeated on most pages within top/bottom bands
    band = collections.Counter()
    for p in d:
        seen = set()
        for b in p.get_text("blocks"):
            y0, y1 = b[1], b[3]
            if y1 < 75 or y0 > H - 75:
                t = re.sub(r"\d+\s*/\s*\d+", "#", b[4]).strip()
                t = re.sub(r"\s+", " ", t)
                if t and t not in seen:
                    seen.add(t); band[t] += 1
    rep = {t for t, c in band.items() if c >= max(2, d.page_count // 2)}
    print("RUNNING:", " || ".join(sorted(rep)) or "-")
    for pi, p in enumerate(d):
        print(f"\n=== p{pi+1}")
        tabs = p.find_tables().tables
        trects = [fitz.Rect(t.bbox) for t in tabs]
        strikes = []
        for dr in p.get_drawings():
            for it in dr["items"]:
                if it[0] == "l" and abs(it[1].y - it[2].y) < 1.0 and abs(it[2].x - it[1].x) > 3:
                    strikes.append((min(it[1].x, it[2].x), max(it[1].x, it[2].x), it[1].y))
                elif it[0] == "re" and it[1].height < 1.6 and it[1].width > 3:
                    strikes.append((it[1].x0, it[1].x1, (it[1].y0 + it[1].y1) / 2))
        def struck(bb):
            h = bb[3] - bb[1]
            for x0, x1, y in strikes:
                cx = (bb[0] + bb[2]) / 2
                if bb[1] + .3 * h < y < bb[3] - .2 * h and x0 <= cx <= x1:
                    return True
            return False
        out = []
        def cell_text(rect):
            parts = []
            for bl in p.get_text("rawdict", clip=fitz.Rect(rect))["blocks"]:
                for ln in bl.get("lines", []):
                    for sp in ln["spans"]:
                        for ch in sp["chars"]:
                            cx = (ch["bbox"][0] + ch["bbox"][2]) / 2; cy = (ch["bbox"][1] + ch["bbox"][3]) / 2
                            if not fitz.Rect(rect).contains(fitz.Point(cx, cy)): continue
                            c = ch["c"]
                            if strikes and c.strip() and struck(ch["bbox"]): c = "\x01" + c + "\x02"
                            parts.append(c)
                    parts.append(" ")
            t = re.sub(r"\s+", " ", "".join(parts)).strip()
            return re.sub(r"\x02(\s*)\x01", r"\1", t).replace("\x01", "~~").replace("\x02", "~~")
        for t in tabs:
            rows = []
            for r in t.rows:
                rows.append("| " + " | ".join(cell_text(cb) if cb else "" for cb in r.cells) + " |")
            out.append((t.bbox[1], "\n".join(rows)))
        def intable(bb):
            cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
            return any(tr.contains(fitz.Point(cx, cy)) for tr in trects)
        for b in p.get_text("rawdict")["blocks"]:
            if b["type"] != 0: continue
            r = fitz.Rect(b["bbox"])
            lines = []
            for l in b["lines"]:
                if intable(l["bbox"]): continue
                parts = []
                for sp in l["spans"]:
                    for ch in sp["chars"]:
                        c = ch["c"]
                        if strikes and c.strip() and struck(ch["bbox"]): c = "\x01" + c + "\x02"
                        parts.append(c)
                    sp["text"] = "".join(x["c"] for x in sp["chars"])
                s = "".join(parts).strip()
                s = re.sub(r"\x02(\s*)\x01", r"\1", s).replace("\x01", "~~").replace("\x02", "~~")
                if not s: continue
                sp = max(l["spans"], key=lambda x: len(x["text"].strip()))
                bold = sp["flags"] & 16 or "Bold" in sp["font"]
                ital = sp["flags"] & 2 or "Italic" in sp["font"]
                lines.append((s, bold, ital, l["bbox"][1]))
            if not lines: continue
            txt = " ".join(x[0] for x in lines)
            txt = re.sub(r"\s+", " ", txt).strip()
            key = re.sub(r"\d+\s*/\s*\d+", "#", txt)
            if (r.y1 < 75 or r.y0 > H - 75) and (key in rep or re.fullmatch(r"[\d\s/]+", txt)):
                continue
            pre = "**" if all(x[1] for x in lines) else ("//" if all(x[2] for x in lines) else "")
            out.append((lines[0][3], pre + txt))
        for _, t in sorted(out, key=lambda x: x[0]):
            print(t)

if __name__ == "__main__":
    main()
