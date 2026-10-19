#!/usr/bin/env python3
"""Category filter for « Vignobles de France — Carte des IGP.html ».

  python3 assets/igp_filter_apply.py     # (re)insert; idempotent (markers fw-igpfilter)

URL hash #cat=reg|dep|zone|spir shows only that category (home-page chips link there);
no hash = everything. Adds a « Toutes les IGP et IG » button on the map and makes the
legend entries clickable filters. Rerun after the IGP page is rebuilt.
"""
import os, re
SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(SITE, 'Vignobles de France — Carte des IGP.html')

CSS = r'''<!--fw-igpfilter:start--><style id="fw-igpfilter-css">
#allIgp{position:absolute;left:12px;top:12px;z-index:6;display:inline-flex;align-items:center;gap:7px;padding:7px 13px;border-radius:8px;
 font:600 12.5px "Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;letter-spacing:.02em;cursor:pointer;
 background:var(--wine);color:var(--parch);border:1px solid var(--gold);box-shadow:0 2px 8px rgba(0,0,0,.18)}
#allIgp:hover{background:var(--wine2)}
#allIgp .sws{display:inline-flex;gap:2px}#allIgp .sws i{width:7px;height:11px;border-radius:2px;display:block}
#allIgp.on{opacity:.55;cursor:default}
#filtNote{display:none;margin:8px 12px 0;padding:6px 10px;border-radius:6px;font-size:12.5px;border:1px solid rgba(201,162,75,.5);background:rgba(201,162,75,.12)}
#filtNote .sw{display:inline-block;width:11px;height:11px;border-radius:3px;margin-right:6px;vertical-align:-1px;border:1px solid rgba(0,0,0,.3)}
#legend .li{cursor:pointer;border-radius:4px;padding:1px 4px;margin:1px -4px}
#legend .li:hover{background:rgba(94,16,32,.08)}
#legend .li.off{opacity:.35}
#legend .li.cur{font-weight:700}
.grp.fhide{display:none}
html[data-theme="cream"] #filtNote{border-color:rgba(154,106,31,.45);background:rgba(154,106,31,.08)}
@media (max-width:700px){#allIgp{top:auto;bottom:12px;left:auto;right:12px;font-size:12px;padding:6px 10px}}
</style><!--fw-igpfilter:end-->
'''

JS = r'''/*fw-igpfilter:start*/
(function(){
  const NAMES={reg:['IGP Régionales','Regional IGPs'],dep:['IGP Départementales','Département IGPs'],
    zone:['IGP de Zones et Terroirs','Zone & Terroir IGPs'],spir:['IG Eaux-de-vie et Marcs','Spirits & Marcs IGs']};
  const T={all:['Toutes les IGP et IG','All IGPs & IGs'],shown:['Affichage :','Showing:']};
  const en=()=>document.documentElement.lang==='en', L=p=>p[en()?1:0];
  let cur=null;
  const btn=document.createElement('button');btn.id='allIgp';
  btn.innerHTML='<span class="sws">'+CATORDER.map(c=>'<i style="background:'+CATCOL[c]+'"></i>').join('')+'</span><span class="t"></span>';
  stage.appendChild(btn);
  const note=document.createElement('div');note.id='filtNote';
  document.getElementById('search').insertAdjacentElement('beforebegin',note);
  const groups={};document.querySelectorAll('#list .grp').forEach((g,i)=>{const c=CATORDER.filter(k=>DATA.some(a=>a.cat==k))[i];if(c)groups[c]=g;});
  const legItems={};document.querySelectorAll('#legend .li').forEach((li,i)=>{const c=CATORDER.filter(k=>DATA.some(a=>a.cat==k))[i];if(c){legItems[c]=li;
    li.title='';li.onclick=()=>go(cur===c?null:c);}});
  function label(){btn.querySelector('.t').textContent=L(T.all);
    note.innerHTML=cur?'<span class="sw" style="background:'+CATCOL[cur]+'"></span>'+L(T.shown)+' <b>'+L(NAMES[cur])+'</b>':'';}
  function apply(c){if(c&&!NAMES[c])c=null;cur=c;
    CATORDER.forEach(k=>{const show=!c||k===c;hidden[k]=!show;
      DATA.filter(a=>a.cat==k).forEach(a=>a._el.forEach(e=>e.style.display=show?'':'none'));
      const g=groups[k];if(g){g.classList.toggle('fhide',!show);g.classList.remove('hidecat');const eye=g.querySelector('.eye');if(eye)eye.textContent='◉';}
      const li=legItems[k];if(li){li.classList.toggle('off',!show);li.classList.toggle('cur',!!c&&show);}});
    if(selIdx>=0&&byIdx[selIdx]&&hidden[byIdx[selIdx].cat])clearSel();
    btn.classList.toggle('on',!c);btn.disabled=!c;note.style.display=c?'block':'none';label();}
  function fromHash(){const m=location.hash.match(/(?:^#|[&#])cat=(\w+)/);return m?m[1]:null;}
  function go(c){history.replaceState(null,'',c?'#cat='+c:location.pathname+location.search);apply(c);}
  btn.onclick=()=>go(null);
  window.addEventListener('hashchange',()=>apply(fromHash()));
  new MutationObserver(label).observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
  apply(fromHash());
})();
/*fw-igpfilter:end*/
'''

s = open(P, encoding='utf-8').read()
s = re.sub(r'<!--fw-igpfilter:start-->.*?<!--fw-igpfilter:end-->\n?', '', s, flags=re.S)
s = re.sub(r'/\*fw-igpfilter:start\*/.*?/\*fw-igpfilter:end\*/\n?', '', s, flags=re.S)
k = s.find('</head>'); s = s[:k] + CSS + s[k:]
k = s.find('</script><!--fw-i18n:start-->'); assert k > 0
s = s[:k] + JS + s[k:]
open(P, 'w', encoding='utf-8').write(s); print('ok', os.path.basename(P))
