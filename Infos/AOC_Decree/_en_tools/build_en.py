#!/usr/bin/env python3
"""Build an English decree PDF from compact markup in _en_src/<slug>.txt.

Usage: python3 build_en.py <slug> [<slug> ...] [--alias dup_slug=src_slug ...] [--nowire]

Markup (one paragraph per line, blank lines ignored):
  @h1 / @h2 text   running header lines      @f1 / @f2 text   running footer lines
  @title text      centred bold              @center text     centred plain
  # text           chapter (centred bold)    ## text          section heading (bold)
  ### text         sub-heading (italic)      #### text        minor heading (bold italic)
  > text           indented paragraph        @pb              page break
  | a | b |        table row (first row of a table = bold header; '@nohead' line before
                   the table disables that).  Cell starting with '<' = left-merged into
                   previous cell (colspan).
  inline: **bold**  *italic*  ^sup^
Output: decrees/<slug>_en.pdf, manifest `en` set, library regenerated.
"""
import sys, os, re, html, json, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import make_en_decree as M

CSS = """
@page { size: A4; margin: 78pt 70.9pt 72pt 70.9pt; }
body { font-family: "Times New Roman", Times, serif; font-size: 11pt; line-height: 1.22;
       text-align: justify; color: #000; margin: 0; }
p { margin: 0 0 7pt; }
.title { text-align: center; font-weight: bold; margin: 6pt 0 10pt; }
.center { text-align: center; margin: 0 0 10pt; }
h1 { text-align: center; font-size: 11pt; font-weight: bold; margin: 12pt 0 10pt; }
h2 { font-size: 11pt; font-weight: bold; margin: 12pt 0 6pt; page-break-after: avoid; }
h3 { font-size: 11pt; font-weight: normal; font-style: italic; margin: 9pt 0 4pt; page-break-after: avoid; }
h4 { font-size: 11pt; font-weight: bold; font-style: italic; margin: 8pt 0 4pt; page-break-after: avoid; }
.ind { margin-left: 24pt; }
table { border-collapse: collapse; width: 100%; margin: 4pt 0 10pt; font-size: 10pt;
        text-align: left; page-break-inside: auto; }
td, th { border: 0.6pt solid #000; padding: 3pt 5pt; vertical-align: top; }
th { font-weight: bold; }
tr { page-break-inside: avoid; }
sup { font-size: 7pt; }
.pb { page-break-after: always; }
"""

def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
    s = re.sub(r"\^(.+?)\^", r"<sup>\1</sup>", s)
    return s

def expand(src):
    """Macros: '@define NAME' ... '@enddef' blocks; '@@NAME a | b' expands with {1}, {2}... (recursive)"""
    macros, body, cur = {}, [], None
    for line in src.splitlines():
        if cur is not None:
            if line.strip() == "@enddef": cur = None
            else: macros[cur].append(line)
            continue
        m = re.match(r"@define\s+(\w+)", line)
        if m: cur = m.group(1); macros[cur] = []; continue
        body.append(line)
    import unicodedata
    def skey(x):
        x = re.sub(r"^(L’|L'|La |Le |Les )", "", x.strip())
        return unicodedata.normalize("NFKD", x).encode("ascii", "ignore").decode().lower()
    def listop(spec):
        parts = [p.strip() for p in spec.split("|")]
        line = " ".join(macros[parts[0]]).strip()
        m = re.match(r"(.*?:\s*)(.*?)\.?$", line)
        pre, items = m.group(1), m.group(2)
        items = re.split(r",\s*|\s+and\s+", items)
        for op in parts[1:]:
            if op.startswith("-"):
                if op[1:] not in items: raise KeyError("listop: missing " + op[1:])
                items.remove(op[1:])
            elif op.startswith("+"):
                items.append(op[1:]); items.sort(key=skey)
        return pre + ", ".join(items[:-1]) + " and " + items[-1] + "."
    def run(lines, depth=0):
        out = []
        for line in lines:
            if line.startswith("@listop "):
                out.append(listop(line[8:])); continue
            m = re.match(r"@@(\w+)\s*(.*)", line)
            if not m: out.append(line); continue
            if m.group(1) not in macros: raise KeyError("undefined macro " + m.group(1))
            args = [a.strip() for a in m.group(2).split("|")] if m.group(2).strip() else []
            sub = []
            for ml in macros[m.group(1)]:
                for i, a in enumerate(args, 1): ml = ml.replace("{%d}" % i, a)
                sub.append(ml)
            out.extend(run(sub, depth + 1) if depth < 8 else sub)
        return out
    return "\n".join(run(body))

def parse(src):
    src = expand(src)
    meta = {"h1": "", "h2": "", "f1": "", "f2": ""}
    body, table, nohead = [], None, False
    def flush():
        nonlocal table, nohead
        if table is None: return
        rows = []
        for ri, cells in enumerate(table):
            tag = "th" if ri == 0 and not nohead else "td"
            out, span = [], []
            for c in cells:
                if c.startswith("<") and out:
                    span[-1] += 1; continue
                out.append(c); span.append(1)
            tds = "".join(f'<{tag}{" colspan=%d" % n if n > 1 else ""}>{inline(c)}</{tag}>' for c, n in zip(out, span))
            rows.append(f"<tr>{tds}</tr>")
        if not nohead and rows:
            body.append("<table><thead>" + rows[0] + "</thead><tbody>" + "".join(rows[1:]) + "</tbody></table>")
        else:
            body.append("<table>" + "".join(rows) + "</table>")
        table, nohead = None, False
    for raw in src.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("|"):
            if table is None: table = []
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?", c) for c in cells if c): continue
            table.append(cells); continue
        flush()
        m = re.match(r"@(h1|h2|f1|f2)\s+(.*)", line)
        if m: meta[m.group(1)] = m.group(2).strip(); continue
        if line.strip() == "@nohead": nohead = True; continue
        if line.strip() == "@pb": body.append('<div class="pb"></div>'); continue
        if line.startswith("@title "): body.append(f'<p class="title">{inline(line[7:])}</p>'); continue
        if line.startswith("@center "): body.append(f'<p class="center">{inline(line[8:])}</p>'); continue
        m = re.match(r"(#{1,4}) (.*)", line)
        if m:
            n = len(m.group(1)); body.append(f"<h{n}>{inline(m.group(2))}</h{n}>"); continue
        if line.startswith("> "): body.append(f'<p class="ind">{inline(line[2:])}</p>'); continue
        body.append(f"<p>{inline(line.strip())}</p>")
    flush()
    return meta, "\n".join(body)

def build(slug, wire=True):
    import glob
    one = os.path.join(ROOT, "_en_src", slug + ".txt")
    parts = [one] if os.path.exists(one) else sorted(glob.glob(os.path.join(ROOT, "_en_src", slug + ".part*.txt")))
    src = "\n".join(open(x, encoding="utf-8").read() for x in parts)
    # @include NAME  -> _en_src/_shared/NAME.txt
    src = re.sub(r"(?m)^@include\s+(\S+)\s*$", lambda m: open(os.path.join(ROOT, "_en_src", "_shared", m.group(1) + ".txt"), encoding="utf-8").read(), src)
    meta, body = parse(src)
    doc = f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{slug} EN</title><style>{CSS}</style></head><body>{body}</body></html>'
    tmpd = tempfile.mkdtemp()
    h = os.path.join(tmpd, slug + "_en.html"); open(h, "w", encoding="utf-8").write(doc)
    raw = os.path.join(tmpd, "raw.pdf")
    M.render(h, raw)
    out = os.path.join(ROOT, "decrees", slug + "_en.pdf")
    n = M.stamp(raw, out, meta["h1"], meta["h2"], meta["f1"], meta["f2"])
    print(f"{slug}: {n} pages")
    return out

def set_en(pairs):
    mp = os.path.join(ROOT, "manifest.json")
    man = json.load(open(mp))
    for slug, en_slug in pairs:
        hit = False
        for it in man:
            if it["file"] == f"decrees/{slug}.pdf":
                it["en"] = f"decrees/{en_slug}_en.pdf"; hit = True
        if not hit: print("!! not in manifest:", slug)
    json.dump(man, open(mp, "w"), ensure_ascii=False, indent=0)
    subprocess.run([sys.executable, os.path.join(ROOT, "gen_library.py")], check=True)

def main():
    args = sys.argv[1:]
    wire = "--nowire" not in args
    slugs, aliases = [], []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--alias": d, s = args[i + 1].split("="); aliases.append((d, s)); i += 2; continue
        if not a.startswith("--"): slugs.append(a)
        i += 1
    for s in slugs: build(s)
    if wire: set_en([(s, s) for s in slugs] + aliases)

if __name__ == "__main__":
    main()
