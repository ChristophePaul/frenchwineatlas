import re
from bs4 import NavigableString, Tag
BLOCKS={'h1','h2','h3','h4','h5','h6','p','li','td','th','caption','figcaption','blockquote','dt','dd','summary','button','label',
        'div','section','figure','table','tr','tbody','thead','tfoot','ul','ol','dl','nav','header','main','article','aside','footer','details','img','br'}
LET=re.compile(r'[A-Za-z]{2}')
def targets(node,out,loose):
    for ch in node.children:
        if isinstance(ch,NavigableString):
            if LET.search(ch) and not isinstance(ch,(type(None),)) and ch.parent.name not in ('script','style'): loose.append((node,ch))
            continue
        if not isinstance(ch,Tag) or ch.name in ('script','style'): continue
        if not LET.search(ch.get_text()): continue
        if ch.find(lambda t: t.name in BLOCKS and t.name not in ('br',)) is None:
            out.append(ch)
        else:
            targets(ch,out,loose)
    return out
