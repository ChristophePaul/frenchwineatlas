# -*- coding: utf-8 -*-
"""Adds a `#climat=<name>` deep link to every Burgundy climats map (Bourgogne Regions/Bourgogne climats/*.html):
on load it clicks the matching legend row (zoom + popup) and highlights it. Idempotent (<!--fw-climat:start/end--> markers).
Rerun after rebuilding those map pages: python3 climat_link_apply.py"""
import glob, re
from pathlib import Path
DIR = Path(__file__).resolve().parents[3] / 'Bourgogne Regions' / 'Bourgogne climats'
SNIP = r'''<!--fw-climat:start--><style>.row.fw-hit{outline:2px solid #d9b36b;outline-offset:2px;border-radius:6px;background:rgba(217,179,107,.18);}</style>
<script>(function(){function n(s){return (s||'').normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[’']/g,"'").replace(/\s+/g,' ').trim();}
function go(){var m=location.hash.match(/^#climat=(.+)$/);if(!m)return;var t=n(decodeURIComponent(m[1]));
var rows=document.querySelectorAll('#grp-gc .row, #grp-pc .row');
for(var i=0;i<rows.length;i++){var nm=rows[i].querySelector('.nm');if(!nm)continue;var c=nm.cloneNode(true);var tg=c.querySelector('.nbtag');if(tg)tg.remove();
if(n(c.textContent)===t){var old=document.querySelectorAll('.row.fw-hit');for(var j=0;j<old.length;j++)old[j].classList.remove('fw-hit');
rows[i].classList.add('fw-hit');try{rows[i].scrollIntoView({block:'center'});}catch(e){}rows[i].click();return;}}}
window.addEventListener('load',function(){setTimeout(go,350);});window.addEventListener('hashchange',go);})();</script><!--fw-climat:end-->
'''
n = 0
for f in sorted(DIR.glob('*.html')):
    s = f.read_text()
    s = re.sub(r'<!--fw-climat:start-->.*?<!--fw-climat:end-->\n?', '', s, flags=re.S)
    s = s.replace('</body>', SNIP + '</body>', 1)
    f.write_text(s); n += 1
print('patched', n, 'pages')
