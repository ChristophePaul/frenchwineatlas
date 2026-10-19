#!/usr/bin/env python3
"""Add the cream/dark theme toggle to every page of the site.

For each HTML page:
  * inserts <script src=".../assets/theme.js"> at the top of <head>;
  * reads the page's own CSS, and for every colour works out its role (text, background,
    border, shadow) and writes an override rule scoped to the *other* theme:
      - dark-native pages (burgundy glass, map sidebars) get  html[data-theme="cream"] …
      - light-native pages (How it's made, chemistry, France maps) get html[data-theme="dark"] …
    The generated CSS goes in <style id="fw-theme-css"> just before </head>.
Idempotent: re-running replaces the previous injection (run it again after rebuilding a map page).

Usage:  python3 theme_apply.py            (all pages)
        python3 theme_apply.py page.html  (some pages)
        python3 theme_apply.py --remove   (undo everywhere)
"""
import colorsys, os, re, sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
START, END = "<!--fw-theme:start-->", "<!--fw-theme:end-->"
LIGHT_NATIVE = ("How it's made", "wine_chemistry_html")
SKIP = ("_source", "_backups")
HAND_TUNED = ("Cepages_et_Appellations.html",)   # has its own cream CSS; only needs the script

# ---------------------------------------------------------------- colours
NAMED = {"white": (255, 255, 255, 1.0), "black": (0, 0, 0, 1.0), "transparent": (0, 0, 0, 0.0)}
COLOR_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|\b(?:white|black|transparent)\b")

def parse(c):
    c = c.strip()
    if c.lower() in NAMED:
        return NAMED[c.lower()]
    if c.startswith("#"):
        h = c[1:]
        if len(h) in (3, 4):
            h = "".join(x * 2 for x in h)
        if len(h) not in (6, 8):
            return None
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        return r, g, b, a
    m = re.match(r"rgba?\(([^)]*)\)", c)
    if m:
        p = [x.strip() for x in re.split(r"[,\s/]+", m.group(1)) if x.strip()]
        try:
            r, g, b = (float(x.rstrip("%")) * (2.55 if x.endswith("%") else 1) for x in p[:3])
            a = float(p[3].rstrip("%")) / (100 if p[3].endswith("%") else 1) if len(p) > 3 else 1.0
            return r, g, b, a
        except (ValueError, IndexError):
            return None
    return None

def fmt(r, g, b, a):
    a = max(0.0, min(1.0, a))
    r, g, b = (int(round(max(0, min(255, v)))) for v in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}" if a >= 0.999 else f"rgba({r},{g},{b},{a:.2f})".replace(".00)", ")")

def lum(r, g, b):
    f = lambda v: (v / 255) / 12.92 if v / 255 <= 0.03928 else ((v / 255 + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def hls(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return h * 360, l, s

def is_gold(r, g, b):
    h, l, s = hls(r, g, b)
    return 25 <= h <= 58 and s > 0.3 and 0.3 < l < 0.85

def is_red(r, g, b):
    h, l, s = hls(r, g, b)
    return (h < 18 or h > 325) and s > 0.28

INK = (46, 20, 25)
GOLD_DK = (138, 93, 23)
BORD = (142, 31, 51)

def to_cream(col, role):
    r, g, b, a = col
    L = lum(r, g, b)
    if a == 0:
        return col
    if role == "text":
        if L < 0.3:
            return col                            # already dark (text on a gold chip…)
        if is_gold(r, g, b):
            return (*GOLD_DK, a)
        if is_red(r, g, b):
            return (*BORD, a)
        return (*INK, max(a, 0.5))
    if role == "bg":
        if is_gold(r, g, b):
            return col if a >= 0.999 else (154, 106, 31, min(1, a))
        if L < 0.08:                               # near-black glass / dark burgundy panels
            return (251, 246, 236, 1) if a >= 0.999 else (255, 253, 248, min(0.92, 0.55 + a))
        if is_red(r, g, b) and hls(r, g, b)[1] < 0.4:
            return (250, 244, 233, 1) if a >= 0.999 else (155, 34, 53, a * 0.35)
        if L < 0.2:
            return (251, 246, 236, 1) if a >= 0.999 else (255, 253, 248, min(0.92, 0.55 + a))
        if L > 0.75 and a < 0.5:
            return (90, 30, 40, min(0.12, a * 1.3))
        return col
    if role == "border":
        if is_gold(r, g, b):
            return (154, 106, 31, min(1, a * 1.1 + 0.05))
        if L > 0.6:
            return (90, 30, 40, min(0.5, a * 0.9 + 0.05))
        if L < 0.2:
            return (90, 30, 40, 0.18)
        return col
    if role == "shadow":
        if L < 0.3:
            return (90, 40, 30, a * 0.3)
        return (255, 255, 255, min(0.8, a * 6))
    return col

def to_dark(col, role):
    r, g, b, a = col
    L = lum(r, g, b)
    h, l, s = hls(r, g, b)
    if a == 0:
        return col
    if role == "text":
        if L > 0.45:
            return col
        if s > 0.25 and l > 0.12:                  # coloured text: lighten, keep hue
            rr, gg, bb = colorsys.hls_to_rgb(h / 360, 0.72, min(0.75, s))
            return (rr * 255, gg * 255, bb * 255, a)
        return (241, 232, 216, max(a, 0.6))
    if role == "bg":
        if L > 0.55:
            parchment = 20 <= h <= 65 and l > 0.78  # cream / parchment -> site burgundy
            if parchment or s <= 0.25:
                return (58, 17, 27, a) if L > 0.85 else (40, 10, 17, a)
            if l < 0.97:                           # pale coloured tint -> dark tint of same hue
                rr, gg, bb = colorsys.hls_to_rgb(h / 360, 0.17, min(0.45, s))
                return (rr * 255, gg * 255, bb * 255, a)
            return (58, 17, 27, a) if L > 0.85 else (40, 10, 17, a)
        if L < 0.12 and a < 0.5:
            return (255, 255, 255, a)
        return col
    if role == "border":
        if L > 0.4:
            return (217, 179, 107, min(0.45, 0.2 + a * 0.2))
        return col
    if role == "shadow":
        return (0, 0, 0, min(0.7, a * 1.6))
    return col

ROLE_OF = [
    (re.compile(r"^(color|caret-color|text-decoration-color|-webkit-text-fill-color)$"), "text"),   # SVG fill/stroke = map drawing, left alone
    (re.compile(r"^background(-color|-image)?$"), "bg"),
    (re.compile(r"^(border(-(top|right|bottom|left|block|inline)(-start|-end)?)?(-color)?|outline(-color)?|column-rule(-color)?)$"), "border"),
    (re.compile(r"^box-shadow$"), "shadow"),
    (re.compile(r"^text-shadow$"), "tshadow"),
]

def role_for(prop):
    for rx, role in ROLE_OF:
        if rx.match(prop):
            return role
    return None

# ---------------------------------------------------------------- css parsing
def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)

def blocks(css):
    """Yield (prelude, body) at top level; nested @media handled by caller."""
    i, n = 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0:
            return
        depth, k = 1, j + 1
        while k < n and depth:
            if css[k] == "{": depth += 1
            elif css[k] == "}": depth -= 1
            k += 1
        yield css[i:j].strip(), css[j + 1:k - 1]
        i = k

def decls(body):
    out = []
    for part in re.split(r";(?![^()]*\))", body):
        if ":" in part:
            p, v = part.split(":", 1)
            out.append((p.strip().lower(), v.strip()))
    return out

def split_sel(prelude):
    out, depth, cur = [], 0, ""
    for ch in prelude:
        if ch == "(": depth += 1
        if ch == ")": depth -= 1
        if ch == "," and depth == 0:
            out.append(cur); cur = ""
        else:
            cur += ch
    out.append(cur)
    return [s.strip() for s in out if s.strip()]

def scope(sel, theme):
    pre = f'html[data-theme="{theme}"]'
    s = sel.strip()
    if s.startswith(":root"):
        return pre + s[5:]
    if re.match(r"html\b", s):
        return pre + s[4:]
    return pre + " " + s

def collect_vars(css):
    vars_ = {}
    for pre, body in blocks(css):
        if pre.startswith("@"):
            continue
        for p, v in decls(body):
            if p.startswith("--"):
                vars_[p] = v
    return vars_

def resolve(v, vars_, depth=0):
    if depth > 6 or "var(" not in v:
        return v
    return resolve(re.sub(r"var\((--[\w-]+)\s*(?:,\s*([^()]*))?\)",
                          lambda m: vars_.get(m.group(1), m.group(2) or m.group(0)), v), vars_, depth + 1)

CREAM_BODY_BG = ("radial-gradient(120% 70% at 50% -10%,rgba(155,34,53,.10) 0%,rgba(155,34,53,0) 55%),"
                 "linear-gradient(180deg,#f8f1e4 0%,#f3e9d6 100%) fixed,#f5eee0")

def map_value(prop, val, vars_, theme, sel):
    role = role_for(prop)
    if not role:
        return None
    rv = resolve(val, vars_)
    if role == "tshadow":
        return "none" if theme == "cream" and COLOR_RE.search(rv) else None
    if theme == "cream" and role == "bg" and "Web_Page_Background" in rv:
        return CREAM_BODY_BG
    fn = to_cream if theme == "cream" else to_dark
    changed = False
    def rep(m):
        nonlocal changed
        c = parse(m.group(0))
        if c is None:
            return m.group(0)
        nc = fn(c, role)
        if tuple(round(x, 3) for x in nc) != tuple(round(x, 3) for x in c):
            changed = True
        return fmt(*nc)
    out = COLOR_RE.sub(rep, rv)
    if not changed or "var(" in out:
        return None
    return out

CONTAINER_RE = re.compile(r"^(html|body|:root|aside|#side|#sidebar|\.sidebar|#app|#wrap|nav|#panel|\.panel-side)\b")

def solid_dark(rv):
    for m in COLOR_RE.finditer(rv):
        c = parse(m.group(0))
        if c and c[3] >= 0.9 and lum(*c[:3]) < 0.12 and hls(*c[:3])[2] > 0.3:
            return True
    return False

def gen_css(css, theme, family="glass"):
    css = strip_comments(css)
    vars_ = collect_vars(css)
    out = []
    def walk(text, wrap=None):
        for pre, body in blocks(text):
            if pre.startswith("@media") or pre.startswith("@supports"):
                inner = []
                walk(body, inner)
                if inner:
                    out.append(pre + "{" + "".join(inner) + "}")
                continue
            if pre.startswith("@"):
                continue
            new = []
            ds = decls(body)
            first = split_sel(pre)[0] if pre else ""
            # a burgundy button / chip keeps its colours; only page containers turn cream
            keep_red = theme == "cream" and not CONTAINER_RE.match(first) and any(
                role_for(p) == "bg" and solid_dark(resolve(v, vars_)) for p, v in ds)
            has_bg = any(role_for(p) == "bg" for p, v in ds)
            for p, v in ds:
                if p.startswith("--"):
                    continue
                role = role_for(p)
                if keep_red and role in ("bg", "text", "border", "tshadow"):
                    continue
                if (theme == "cream" and family == "map" and role == "text" and not has_bg
                        and re.fullmatch(r"#fff(fff)?|white", resolve(v, vars_).strip(), re.I)):
                    continue                       # white text on a colour set at runtime
                nv = map_value(p, v, vars_, theme, pre)
                if nv is not None:
                    new.append(f"{p}:{nv}")
            if new:
                sels = ",".join(scope(s, theme) for s in split_sel(pre))
                (wrap if wrap is not None else out).append(sels + "{" + ";".join(new) + "}")
    walk(css)
    return "\n".join(out)

# ---------------------------------------------------------------- pages
STYLE_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.S | re.I)

INLINE_RE = re.compile(r"""style\s*=\s*(\\?["'])(.*?)\1""", re.S)

def inline_css(html, theme):
    """Colours written in style="…" attributes (static markup or JS templates)."""
    fn = to_cream if theme == "cream" else to_dark
    seen, out = set(), []
    for m in INLINE_RE.finditer(html):
        body = m.group(2)
        if len(body) > 400 or "${" in body or "'+" in body or '"+' in body:
            continue
        for d in re.split(r";", body):
            if ":" not in d:
                continue
            p, v = d.split(":", 1)
            p, v = p.strip().lower(), v.strip()
            role = role_for(p)
            if role != "text" or not COLOR_RE.fullmatch(v):   # inline bg/border = data swatches, keep
                continue
            c = parse(v)
            if c is None:
                continue
            nv = fmt(*fn(c, role))
            if nv.lower() == v.lower() or (p, v) in seen:
                continue
            seen.add((p, v))
            raw = f"{p}:{v}"
            sels = [f'[style^="{raw}"]', f'[style*=";{raw}"]', f'[style*="; {raw}"]']
            if p != "color":
                sels.append(f'[style*="{raw}"]')
            out.append(",".join(f'html[data-theme="{theme}"] {s}' for s in sels) + f"{{{p}:{nv}!important}}")
    return "\n".join(out)

def page_css(html):
    parts = []
    for m in STYLE_RE.finditer(html):
        s = m.group(1)
        if 'id="fw-theme-css"' in html[m.start():m.start() + 40]:
            continue
        parts.append(s)
    return "\n".join(parts)

def apply(path):
    rel = os.path.relpath(path, SITE)
    html = open(path, encoding="utf-8").read()
    html = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", html, flags=re.S)
    depth = rel.count(os.sep)
    src = "../" * depth + "assets/theme.js"
    script = f'{START}<script src="{src}"></script>{END}'
    head = re.search(r"<head[^>]*>", html, re.I)
    if not head:
        return f"SKIP (no head) {rel}"
    html = html[:head.end()] + "\n" + script + html[head.end():]
    n = 0
    if not any(h in rel for h in HAND_TUNED):
        theme = "dark" if any(k in rel for k in LIGHT_NATIVE) else "cream"
        family = "glass" if "Web_Page_Background" in html else "map"
        css = gen_css(page_css(html), theme, family) + "\n" + inline_css(html, theme)
        n = css.count("{")
        block = f'{START}<style id="fw-theme-css">\n{css}\n</style>{END}\n'
        i = html.lower().find("</head>")
        html = html[:i] + block + html[i:]
    open(path, "w", encoding="utf-8").write(html)
    return f"{n:4d} rules  {rel}"

def remove(path):
    html = open(path, encoding="utf-8").read()
    new = re.sub(re.escape(START) + r".*?" + re.escape(END) + r"\n?", "", html, flags=re.S)
    if new != html:
        open(path, "w", encoding="utf-8").write(new)
        return "removed  " + os.path.relpath(path, SITE)
    return "untouched " + os.path.relpath(path, SITE)

def main():
    rm = "--remove" in sys.argv
    targets = [a for a in sys.argv[1:] if a != "--remove"]
    if not targets:
        for d, _, files in os.walk(SITE):
            if any(s in d for s in SKIP):
                continue
            targets += [os.path.join(d, f) for f in files if f.endswith(".html")]
    for p in sorted(targets):
        print((remove if rm else apply)(os.path.abspath(p)))

if __name__ == "__main__":
    main()
