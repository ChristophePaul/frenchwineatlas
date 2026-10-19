# -*- coding: utf-8 -*-
"""Build WEB Site/Infos/Categories_of_French_Wines.html from content.json (text of the verified DOCX, FR + EN, + sources).
Edit content.json or page_template.html, then: python3 Infos/_source/categories/gen_page.py"""
import ast, html, json, os, re, shutil, sys

SCR = os.path.dirname(os.path.abspath(__file__))
SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.abspath(os.path.join(SCR, "..", "..", ".."))
OUT = os.path.join(SITE, "Infos", "Categories_of_French_Wines.html")
IMGDIR = os.path.join(SITE, "Infos", "Categories_img")

C = json.load(open(os.path.join(SCR, "content.json")))
EN, FR = C["en"], C["fr"]


def sources(path):
    s = open(path).read()
    a = s.index("SOURCES = [")
    b = s.index("\n]\n", a) + 2
    return ast.literal_eval(s[a + len("SOURCES = "):b])


SRC_EN, SRC_FR = C["sources_en"], C["sources_fr"]
assert len(SRC_EN) == len(SRC_FR) == 31

# ---------------------------------------------------------------- images
os.makedirs(IMGDIR, exist_ok=True)
MEDIA = os.path.join(SCR, "cat", "word", "media")
for src, dst in ([] if not os.path.isdir(MEDIA) else (("image2.jpeg", "eu_flag.jpg"), ("image1.jpeg", "fr_flag.jpg"), ("image8.jpeg", "franceagrimer.jpg"),
                 ("image3.png", "aop_seal.png"), ("image7.png", "igp_seal.png"))):
    shutil.copyfile(os.path.join(MEDIA, src), os.path.join(IMGDIR, dst))


# ---------------------------------------------------------------- text helpers
def fr_typo(t):
    t = re.sub(r" ([:;!?%])", "\u00a0\\1", t)
    t = t.replace("« ", "«\u00a0").replace(" »", "\u00a0»")
    t = re.sub(r"(\d) (\d{3})", "\\1\u00a0\\2", t)
    return t


def md(t, lang):
    if lang == "fr":
        t = fr_typo(t)
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w/])_([^_]+)_(?![\w])", r"<em>\1</em>", t)
    t = re.sub(r"\[(\d+)\]", r'<sup class="ref"><a href="#src-\1">\1</a></sup>', t)
    t = t.replace("</sup><sup class=\"ref\">", "</sup><sup class=\"ref\">")
    t = re.sub(r"(\d)(er|e)\b(?= )", lambda m: m.group(1) + "<sup>" + m.group(2) + "</sup>", t) if lang == "fr" else t
    t = t.replace("XIXe", "XIX<sup>e</sup>").replace("XXe", "XX<sup>e</sup>")
    return t


def esc(t):
    return html.escape(t, quote=True)


def bi(tag, fr, en, cls="", extra=""):
    """Element whose innerHTML is swapped by data-fr / data-en."""
    c = f' class="{cls}"' if cls else ""
    return f'<{tag}{c}{extra} data-fr="{esc(fr)}" data-en="{esc(en)}">{fr}</{tag}>'


def block(b, lang, quote=False):
    kind, val = b
    if kind == "p":
        if quote:
            return f'<blockquote>{md(val, lang)}</blockquote>'
        return f"<p>{md(val, lang)}</p>"
    if kind == "dp":
        return f'<p class="dp">{md(val, lang)}</p>'
    if kind == "h2":
        return f"<h3>{md(val, lang)}</h3>"
    if kind in ("ul", "ol"):
        return f"<{kind}>" + "".join(f"<li>{md(i, lang)}</li>" for i in val) + f"</{kind}>"
    raise ValueError(kind)


def cols(blocks_en, blocks_fr, quote_idx=None, extra_cls=""):
    out = []
    for lang, bl in (("fr", blocks_fr), ("en", blocks_en)):
        inner = "\n".join(block(b, lang, quote=(i == quote_idx)) for i, b in enumerate(bl))
        out.append(f'<div class="cols L {lang} {extra_cls}" lang="{lang}">\n{inner}\n</div>')
    return "\n".join(out)


# ---------------------------------------------------------------- split content into sections
idx_h1 = [i for i, b in enumerate(EN) if b[0] == "h1"]
assert [EN[i][0] for i in idx_h1] == [FR[i][0] for i in idx_h1]
intro_en, intro_fr = EN[0][1], FR[0][1]
secs = []
for k, i in enumerate(idx_h1):
    j = idx_h1[k + 1] if k + 1 < len(idx_h1) else len(EN)
    secs.append((EN[i][1], FR[i][1], EN[i + 1:j], FR[i + 1:j]))
# last h1 section (EU) holds the conclusion after its first two blocks
eu_en, eu_fr = secs[-1][2][:2], secs[-1][3][:2]
concl_en, concl_fr = secs[-1][2][2:], secs[-1][3][2:]
secs[-1] = (secs[-1][0], secs[-1][1], eu_en, eu_fr)
assert len(secs) == 4

SEC_IDS = ["aoc", "histoire", "categories", "europe"]
ICONS = {
    "aoc": '<path d="M12 3 4 7v5c0 4.5 3.4 8 8 9 4.6-1 8-4.5 8-9V7l-8-4Z"/><path d="m9 12 2 2 4-4"/>',
    "histoire": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "categories": '<path d="M12 3 3 20h18L12 3Z"/><path d="M7.5 12h9M5.2 16h13.6"/>',
    "europe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 3.8 5.8 3.8 9S14.5 18.5 12 21C9.5 18.5 8.2 15.2 8.2 12S9.5 5.5 12 3Z"/>',
    "qui": '<circle cx="12" cy="5" r="2.2"/><circle cx="5" cy="19" r="2.2"/><circle cx="12" cy="19" r="2.2"/><circle cx="19" cy="19" r="2.2"/><path d="M12 7.2v4.3M5 16.8V14h14v2.8M12 11.5v5.3"/>',
}


def sec_head(sid, fr, en, kfr=None, ken=None):
    ic = f'<span class="sec-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">{ICONS[sid]}</svg></span>'
    k = bi("p", kfr, ken, "kick") if kfr else ""
    return f'<div class="sec-head">{ic}<div>{k}{bi("h2", fr, en)}</div></div>'


# ---------------------------------------------------------------- visuals
def pyramid():
    lv = [
        ("aoc", "AOC / AOP", "Appellation d’Origine Contrôlée / Protégée", "Appellation d’Origine Contrôlée / Protégée",
         "Une aire strictement délimitée et un cahier des charges détaillé : cépages, rendements, maturité, viticulture, vinification, dégustation d’agrément.",
         "A strictly delimited area and a detailed cahier des charges: varieties, yields, ripeness, viticulture, winemaking, tasting approval.",
         "55", "42", "366 AOP"),
        ("igp", "IGP", "Indication Géographique Protégée", "Indication Géographique Protégée",
         "Une aire définie, des règles plus souples : choix de cépages plus large, rendements plus élevés. Anciens Vins de Pays.",
         "A defined area under broader rules: wider choice of varieties, higher yields. Formerly Vin de Pays.",
         "27", "29", "≈ 75 IGP"),
        ("vsig", "Vin de France", "Vin Sans Indication Géographique (VSIG)", "Vin Sans Indication Géographique (VSIG)",
         "Raisins de toute la France, sans cahier des charges. Cépage et millésime peuvent être indiqués. Ancien Vin de Table.",
         "Grapes from anywhere in France, no cahier des charges. Variety and vintage may be shown. Formerly Vin de Table.",
         "5", "5", ""),
    ]
    levels, notes = [], []
    for i, (cls, short, lfr, len_, dfr, den, area, vol, count) in enumerate(lv):
        levels.append(f'<div class="lvl lvl{i} {cls}"><div class="lvl-in"><b>{short}</b>'
                      f'{bi("span", lfr, len_, "lvl-sub")}</div></div>')
        cnt = f'<span class="cnt">{count}</span>' if count else ""
        notes.append(
            f'<div class="note {cls}"><div class="note-h"><b>{short}</b>{cnt}</div>'
            + bi("p", fr_typo(dfr), den)
            + f'<div class="bars"><div class="bar"><span class="bl" data-fr="Surface" data-en="Area">Surface</span>'
              f'<span class="bt"><i style="width:{area}%"></i></span><span class="bv">{area}&nbsp;%</span></div>'
              f'<div class="bar"><span class="bl" data-fr="Volume" data-en="Volume">Volume</span>'
              f'<span class="bt"><i style="width:{vol}%"></i></span><span class="bv">{vol}&nbsp;%</span></div></div></div>')
    rows = [("AOC / AOP", "404 300 ha", "404,300 ha", "55 %", "15,0 Mhl", "15.0 Mhl", "42 %"),
            ("IGP", "200 300 ha", "200,300 ha", "27 %", "10,6 Mhl", "10.6 Mhl", "29 %"),
            ("Vin de France (VSIG)", "38 700 ha", "38,700 ha", "5 %", "1,7 Mhl", "1.7 Mhl", "5 %"),
            ("Cognac &amp; Armagnac *", "90 300 ha", "90,300 ha", "12 %", "7,8 Mhl", "7.8 Mhl", "22 %")]
    trs = "".join(
        f'<tr><th>{a}</th>{bi("td", fr_typo(b1), b2)}{bi("td", fr_typo(c), c)}{bi("td", d1, d2)}{bi("td", fr_typo(e), e)}</tr>'
        for a, b1, b2, c, d1, d2, e in rows)
    table = (
        '<div class="stats"><table><thead><tr>'
        + bi("th", "Catégorie", "Category") + bi("th", "Surface en production", "Area in production")
        + bi("th", "Part de la surface", "Share of area") + bi("th", "Volume produit", "Volume produced")
        + bi("th", "Part du volume", "Share of volume")
        + f"</tr></thead><tbody>{trs}</tbody></table>"
        + bi("p", fr_typo("* Vins blancs destinés à la distillation en Cognac et en Armagnac. Parts calculées sur ces 4 catégories (≈ 733 600 ha ; ≈ 35 millions d’hl hors usages industriels), arrondies ; elles varient d’une année à l’autre — 2024 fut une petite récolte. Source : FranceAgriMer, Chiffres clés 2025")
             + ' <sup class="ref"><a href="#src-31">31</a></sup>.',
             "* White wines distilled into Cognac and Armagnac. Shares are of these 4 categories (≈ 733,600 ha; ≈ 35 million hl excluding industrial uses), rounded; they vary from year to year — 2024 was a small harvest. Source: FranceAgriMer, Key figures 2025"
             + ' <sup class="ref"><a href="#src-31">31</a></sup>.', "foot")
        + "</div>")
    return (f'<div class="pyr-wrap panel"><div class="pyr">{"".join(levels)}</div>'
            f'<div class="notes">{"".join(notes)}</div></div>'
            + bi("h4", "Le vignoble français en 2024", "The French vineyard in 2024", "stats-h") + table)


def node(img, title_fr, title_en, desc_fr, desc_en, cls="", imgcls=""):
    im = f'<span class="logo {imgcls}"><img src="{img}" alt=""></span>' if img else ""
    return (f'<div class="node {cls}">{im}<div class="nt">{bi("b", title_fr, title_en)}'
            f'{bi("span", fr_typo(desc_fr), desc_en)}</div></div>')


def tree():
    eu = node("Categories_img/eu_flag.jpg", "Union européenne", "European Union",
              "Cadre commun AOP / IGP ; enregistre et protège chaque nom dans toute l’UE.",
              "Common PDO / PGI framework; registers and protects each name across the EU.", "top")
    st = node("Categories_img/fr_flag.jpg", "État français", "French State",
              "Ministère de l’Agriculture : homologue les cahiers des charges par décret ou arrêté et les transmet à Bruxelles.",
              "Ministry of Agriculture: approves each cahier des charges by decree or order and forwards it to Brussels.")
    inao = node("../assets/inao_logo.png", "INAO", "INAO",
                "Institut national de l’origine et de la qualité : reconnaît et suit AOP et IGP, agrée les organismes de contrôle.",
                "National Institute of Origin and Quality: recognises and supervises AOP and IGP, approves the control bodies.",
                imgcls="wide")
    fam = node("Categories_img/franceagrimer.jpg", "FranceAgriMer", "FranceAgriMer",
               "Marchés et aides à la filière, autorisations de plantation, statistiques ; certifie cépage et millésime des Vins de France.",
               "Market and sector aid, planting authorisations, statistics; certifies variety and vintage claims on Vin de France.",
               imgcls="wide")
    ctl = node(None, "DGCCRF &amp; Douanes", "DGCCRF &amp; Customs",
               "Contrôle des fraudes et de l’étiquetage ; déclarations de récolte et de stocks, accises.",
               "Fraud and labelling controls; harvest and stock declarations, excise.", "plain")
    aop = node("Categories_img/aop_seal.png", "AOC / AOP", "AOC / AOP", "≈ 366 appellations", "≈ 366 appellations", "leaf", "seal")
    igp = node("Categories_img/igp_seal.png", "IGP", "IGP", "≈ 75 indications", "≈ 75 indications", "leaf", "seal")
    vdf = node(None, "Vin de France", "Vin de France", "VSIG — pas de logo européen", "VSIG — no EU logo", "leaf vdf")
    return f'''<div class="tree-wrap panel">
<div class="tree"><ul><li>{eu}
  <ul><li>{st}
    <ul>
      <li>{inao}<ul><li>{aop}</li><li>{igp}</li></ul></li>
      <li>{fam}<ul><li>{vdf}</li></ul></li>
      <li>{ctl}</li>
    </ul>
  </li></ul>
</li></ul>
<div class="base"><span class="base-arrow" aria-hidden="true"></span>{node(None, "Vignerons &amp; ODG", "Growers &amp; ODGs",
    "Les organismes de défense et de gestion rédigent le cahier des charges de chaque appellation : la démarche part du terrain.",
    "The growers’ bodies (ODG) draft each appellation’s cahier des charges: the process starts in the vineyard.", "ground")}</div></div>
{bi("p", fr_typo("Les flèches suivent le parcours d’une appellation, de bas en haut : rédigée par les vignerons, instruite par l’INAO, homologuée par l’État, enregistrée par l’Union européenne") + ' <sup class="ref"><a href="#src-1">1</a></sup><sup class="ref"><a href="#src-23">23</a></sup><sup class="ref"><a href="#src-24">24</a></sup>.',
     "The arrows follow an appellation’s path, from the bottom up: drafted by the growers, examined by the INAO, approved by the State, registered by the European Union" + ' <sup class="ref"><a href="#src-1">1</a></sup><sup class="ref"><a href="#src-23">23</a></sup><sup class="ref"><a href="#src-24">24</a></sup>.', "tree-cap")}
</div>'''


def sources_html():
    items = []
    for i, ((lfr, url), (len_, _)) in enumerate(zip(SRC_FR, SRC_EN), 1):
        items.append(f'<li id="src-{i}"><span class="n">{i}</span>'
                     f'{bi("span", esc(fr_typo(lfr)), esc(len_))} '
                     f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(re.sub(r"^https?://(www[.-])?", "", url).split("/")[0])} ↗</a></li>')
    return "<ol class=\"srcs\">" + "".join(items) + "</ol>"


# ---------------------------------------------------------------- assemble
toc = [("aoc", "L’AOC", "The AOC"), ("histoire", "Histoire", "History"), ("categories", "Les 3 catégories", "The 3 categories"),
       ("europe", "L’Europe", "Europe"), ("qui", "Qui encadre ?", "Who regulates?"), ("sources", "Sources", "Sources")]
toc_html = "".join(bi("a", fr_typo(f), e, "chip", f' href="#{i}"') for i, f, e in toc)

body = []
for k, (ten, tfr, ben, bfr) in enumerate(secs):
    sid = SEC_IDS[k]
    q = 1 if sid == "aoc" else None   # INAO definition, rendered as a quotation block (index within section)
    extra = ""
    if sid == "categories":
        extra = pyramid()
    kick = {"aoc": ("Définition", "Definition"), "histoire": ("1863 – 2009", "1863 – 2009"),
            "categories": ("Aujourd’hui", "Today"), "europe": ("AOP · IGP", "PDO · PGI")}[sid]
    body.append(f'<section class="sec" id="{sid}">{sec_head(sid, tfr, ten, *kick)}{extra}{cols(ben, bfr, quote_idx=q)}</section>')

body.append(f'<section class="sec" id="qui">{sec_head("qui", fr_typo("Qui encadre le vin français ?"), "Who Regulates French Wine?", "Hiérarchie", "Hierarchy")}{tree()}</section>')
body.append('<section class="sec concl"><div class="orn" aria-hidden="true">❦</div>'
            + cols(concl_en, concl_fr, extra_cls="c2")
            + '<p class="sig">Christophe PAUL</p></section>')
body.append(f'<section class="sec" id="sources">{sec_head("histoire", "Sources", "Sources", "Références", "References")}'
            + bi("p", "Les nombres en exposant dans le texte renvoient à cette liste. Consultée en octobre 2026.",
                 "Superscript numbers in the text refer to this list. Accessed October 2026.", "src-note")
            + sources_html() + "</section>")

TPL = open(os.path.join(SCR, "page_template.html")).read()
page = (TPL.replace("{{INTRO_FR}}", md(intro_fr, "fr")).replace("{{INTRO_EN}}", md(intro_en, "en"))
        .replace("{{TOC}}", toc_html).replace("{{BODY}}", "\n".join(body)))
open(OUT, "w").write(page)
print("wrote", OUT, len(page) // 1024, "KB")
