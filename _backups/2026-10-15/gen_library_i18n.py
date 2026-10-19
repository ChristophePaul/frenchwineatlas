#!/usr/bin/env python3
import json, os
DEST=r"/Users/chris/Library/CloudStorage/Dropbox/Wines Files InfoComplete/Wine List/A quick Glance at French Wine/2023 Wines Complete/2026 To finish or fucking die/WEB Site/Infos/AOC_Decree"
data=json.load(open(os.path.join(DEST,"manifest.json")))

REGION_ORDER=["Alsace & Lorraine","Champagne","Bourgogne","Beaujolais","Jura","Savoie & Bugey",
 "Loire","Bordeaux","Sud-Ouest","Charente","Rhône","Provence & Corse","Languedoc","Roussillon",
 "Eaux-de-vie & Marcs"]
def rkey(r):
    return REGION_ORDER.index(r) if r in REGION_ORDER else 99
data.sort(key=lambda i:(rkey(i["region"]), i["region"], i["sub"], i["appellation"].lower()))

JSON=json.dumps(data,ensure_ascii=False,separators=(",",":"))

HTML=r'''<!DOCTYPE html>
<html lang="fr">
<head>
<script src="../../assets/copyright.js" defer></script>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title data-fr="Bibliothèque des Décrets AOC" data-en="AOC Decree Library">Bibliothèque des Décrets AOC</title>
<style>
  :root{
    --gold:#d9b36b;--gold-soft:#e7cf9c;--bordeaux:#9b2235;
    --parchment:#f5efe3;--muted:rgba(245,239,227,.62);--faint:rgba(245,239,227,.42);
    --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
    --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI","Helvetica Neue",Arial,sans-serif;
    --glass:rgba(24,5,11,.34);--glass-hi:rgba(38,10,18,.5);
    --hair:rgba(217,179,107,.16);--hair-hi:rgba(217,179,107,.55);
  }
  *{box-sizing:border-box;}
  html{scroll-behavior:smooth;}
  html,body{margin:0;min-height:100%;}
  body{color:var(--parchment);font-family:var(--sans);-webkit-font-smoothing:antialiased;
    background:
      linear-gradient(180deg,rgba(46,4,13,.42) 0%,rgba(46,4,13,.14) 26%,rgba(28,2,8,.55) 100%),
      radial-gradient(130% 90% at 50% -10%,rgba(0,0,0,0) 52%,rgba(18,2,6,.62) 100%),
      url("../../Web_Page_Background.png") center top / cover fixed no-repeat,
      #4d0d18;min-height:100vh;}
  .wrap{max-width:1080px;margin:0 auto;padding:clamp(30px,5vw,60px) clamp(16px,4vw,40px) 64px;}
  .back{display:inline-flex;align-items:center;gap:8px;text-decoration:none;font-size:11px;
    font-weight:600;letter-spacing:.18em;text-transform:uppercase;color:var(--gold);
    border:1px solid var(--hair);border-radius:999px;padding:9px 16px;background:var(--glass);
    transition:border-color .2s,background .2s,transform .2s;}
  .back:hover{border-color:var(--hair-hi);background:var(--glass-hi);transform:translateX(-3px);}
  header{text-align:center;margin:clamp(24px,4vw,44px) 0 clamp(24px,3vw,36px);}
  .eyebrow{text-transform:uppercase;letter-spacing:.5em;font-size:clamp(9px,1.3vw,11px);
    font-weight:600;color:var(--gold);margin:0 0 18px;padding-left:.5em;opacity:.9;}
  h1{font-family:var(--serif);font-weight:500;font-size:clamp(36px,6.5vw,72px);line-height:1;
    margin:0;color:#fff;letter-spacing:-.01em;text-shadow:0 4px 40px rgba(0,0,0,.5);}
  h1 em{font-style:italic;color:var(--gold-soft);}
  .rule{width:64px;height:1px;background:linear-gradient(90deg,transparent,var(--gold),transparent);
    margin:24px auto 20px;}
  .tagline{font-size:clamp(13px,1.6vw,15.5px);line-height:1.65;font-weight:300;
    color:rgba(245,239,227,.82);max-width:620px;margin:0 auto;}
  .tagline b{color:var(--gold-soft);font-weight:600;}

  /* controls */
  .controls{background:var(--glass);border:1px solid var(--hair);border-radius:16px;
    padding:clamp(16px,2.4vw,22px);margin:0 auto clamp(20px,3vw,28px);
    box-shadow:0 18px 50px rgba(10,1,4,.42);display:grid;gap:12px;
    grid-template-columns:1.4fr 1fr 1fr;align-items:end;}
  .field{display:flex;flex-direction:column;gap:6px;min-width:0;}
  .field label{font-size:9.5px;letter-spacing:.2em;text-transform:uppercase;font-weight:600;
    color:var(--gold);opacity:.9;}
  .field input,.field select{width:100%;font-family:var(--sans);font-size:13.5px;color:var(--parchment);
    background:rgba(16,3,7,.5);border:1px solid var(--hair);border-radius:10px;padding:11px 12px;
    outline:none;transition:border-color .18s,background .18s;-webkit-appearance:none;appearance:none;}
  .field select{background-image:url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="12" height="8" viewBox="0 0 12 8"><path d="M1 1l5 5 5-5" fill="none" stroke="%23d9b36b" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>');
    background-repeat:no-repeat;background-position:right 12px center;padding-right:30px;cursor:pointer;}
  .field input:focus,.field select:focus{border-color:var(--hair-hi);background:rgba(24,6,11,.7);}
  .field select:disabled{opacity:.4;cursor:not-allowed;}
  .field input::placeholder{color:var(--faint);}

  .count{font-size:11px;color:var(--faint);letter-spacing:.04em;margin:2px 4px 14px;}
  .count b{color:var(--gold-soft);font-weight:600;}

  /* result rows */
  .rows{display:flex;flex-direction:column;gap:9px;}
  .row{display:flex;align-items:center;gap:14px;background:var(--glass);border:1px solid var(--hair);
    border-radius:12px;padding:14px 16px;box-shadow:0 10px 30px rgba(10,1,4,.34);
    transition:border-color .18s,background .18s;}
  .row:hover{border-color:var(--hair-hi);background:var(--glass-hi);}
  .row .ic{flex:none;width:38px;height:38px;border-radius:10px;display:grid;place-items:center;
    background:rgba(217,179,107,.1);border:1px solid rgba(217,179,107,.2);}
  .row .ic svg{width:19px;height:19px;color:var(--gold-soft);}
  .row .info{flex:1;min-width:0;}
  .row .name{font-family:var(--serif);font-size:17px;color:#fff;margin:0 0 3px;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
  .row .meta{font-size:11px;color:var(--muted);letter-spacing:.03em;}
  .row .meta .en{display:inline-block;margin-left:8px;font-weight:700;font-size:9px;letter-spacing:.1em;
    color:var(--gold-soft);border:1px solid rgba(217,179,107,.4);border-radius:999px;
    padding:1px 6px;background:rgba(217,179,107,.08);text-transform:uppercase;}
  .row .acts{flex:none;display:flex;gap:8px;}
  .row .acts a{font-size:10.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
    text-decoration:none;color:var(--gold);border:1px solid var(--hair);border-radius:999px;
    padding:8px 13px;white-space:nowrap;transition:border-color .18s,background .18s,transform .1s;}
  .row .acts a:hover{border-color:var(--hair-hi);background:rgba(217,179,107,.12);}
  .row .acts a:active{transform:scale(.96);}
  .row .acts a.dl{color:var(--gold-soft);background:rgba(217,179,107,.1);}
  .row .acts a.en{color:var(--parchment);}

  .empty{text-align:center;color:var(--faint);font-size:13px;font-weight:300;padding:40px 10px;line-height:1.7;}
  .empty b{color:var(--gold-soft);font-weight:600;}

  .feat{margin:6px auto 22px;padding:16px 18px;display:flex;align-items:center;gap:14px;
    background:linear-gradient(90deg,rgba(155,34,53,.22),rgba(24,5,11,.34));
    border:1px solid var(--hair);border-radius:14px;}
  .feat .t{flex:1;}
  .feat .t b{color:#fff;font-family:var(--serif);font-size:16px;font-weight:500;}
  .feat .t p{margin:3px 0 0;font-size:11.5px;color:var(--muted);}
  .feat a{flex:none;font-size:10.5px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;
    text-decoration:none;color:var(--gold-soft);border:1px solid var(--hair-hi);border-radius:999px;
    padding:9px 15px;background:rgba(217,179,107,.1);transition:background .2s;}
  .feat a:hover{background:rgba(217,179,107,.2);}
  .row .acts button{font-family:var(--sans);font-size:10.5px;font-weight:600;letter-spacing:.1em;
    text-transform:uppercase;color:var(--gold-soft);background:rgba(217,179,107,.1);
    border:1px solid var(--hair);border-radius:999px;padding:9px 16px;cursor:pointer;white-space:nowrap;
    transition:border-color .18s,background .18s,transform .1s;}
  .row .acts button:hover{border-color:var(--hair-hi);background:rgba(217,179,107,.2);}
  .row .acts button:active{transform:scale(.96);}
  /* language chooser modal */
  .modal{position:fixed;inset:0;z-index:50;display:flex;align-items:center;justify-content:center;
    padding:20px;background:rgba(8,1,4,.66);-webkit-backdrop-filter:blur(4px);backdrop-filter:blur(4px);}
  .modal[hidden]{display:none;}
  .modal .sheet{position:relative;width:100%;max-width:440px;background:#2a0710;
    border:1px solid var(--hair-hi);border-radius:18px;padding:26px 24px 24px;
    box-shadow:0 30px 80px rgba(0,0,0,.6);animation:pop .18s ease;}
  @keyframes pop{from{transform:translateY(8px) scale(.98);opacity:0}to{transform:none;opacity:1}}
  .modal .x{position:absolute;top:14px;right:14px;width:30px;height:30px;border-radius:9px;
    display:grid;place-items:center;background:rgba(217,179,107,.08);border:1px solid var(--hair);
    color:var(--gold-soft);font-size:17px;cursor:pointer;line-height:1;}
  .modal .x:hover{background:rgba(217,179,107,.18);}
  .modal .mk{font-size:9.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--gold);
    font-weight:600;margin:0 0 6px;opacity:.9;}
  .modal h3{font-family:var(--serif);font-weight:500;font-size:24px;color:#fff;margin:0 0 4px;line-height:1.1;}
  .modal .msub{font-size:12px;color:var(--muted);margin:0 0 20px;}
  .langs{display:flex;flex-direction:column;gap:12px;}
  .lang{border:1px solid var(--hair);border-radius:12px;padding:14px 15px;background:rgba(16,3,7,.4);}
  .lang .lh{display:flex;align-items:center;gap:9px;font-size:14px;font-weight:600;color:#fff;margin-bottom:11px;}
  .lang .lh .flag{font-size:17px;}
  .lang .lh .tag{margin-left:auto;font-size:8.5px;letter-spacing:.12em;text-transform:uppercase;
    color:var(--gold-soft);border:1px solid rgba(217,179,107,.4);border-radius:999px;padding:2px 8px;
    background:rgba(217,179,107,.08);font-weight:600;}
  .lang .lb{display:flex;gap:9px;}
  .lang .lb a{flex:1;text-align:center;font-size:11px;font-weight:600;letter-spacing:.08em;
    text-transform:uppercase;text-decoration:none;color:var(--gold);border:1px solid var(--hair);
    border-radius:9px;padding:10px 8px;transition:border-color .18s,background .18s;}
  .lang .lb a:hover{border-color:var(--hair-hi);background:rgba(217,179,107,.12);}
  .lang .lb a.pri{color:var(--gold-soft);background:rgba(217,179,107,.12);}
  .lang.soon{opacity:.6;}
  .lang .soonmsg{font-size:11.5px;color:var(--faint);font-style:italic;}

  footer{margin-top:52px;padding-top:24px;text-align:center;font-size:11px;line-height:1.8;
    color:var(--faint);border-top:1px solid var(--hair);}
  footer b{color:rgba(231,207,156,.85);font-weight:600;}

  @media (max-width:720px){
    .controls{grid-template-columns:1fr;}
    .row{flex-wrap:wrap;}
    .row .acts{width:100%;}
    .row .acts a{flex:1;text-align:center;}
  }
</style>
</head>
<body>
<div class="wrap">
  <a class="back" href="AOC_Decree.html" data-fr="<span>&amp;larr;</span> Anatomie d'un décret" data-en="<span>&amp;larr;</span> Anatomy of a decree"><span>&larr;</span> Anatomie d'un décret</a>

  <header>
    <p class="eyebrow" data-fr="Le Système des Appellations &amp;middot; l'INAO" data-en="The Appellation System &amp;middot; the INAO">Le Système des Appellations &middot; l'INAO</p>
    <h1 data-fr="Bibliothèque des <em>Décrets&amp;nbsp;AOC</em>" data-en="The <em>AOC&amp;nbsp;Decree</em> Library">Bibliothèque des <em>Décrets&nbsp;AOC</em></h1>
    <div class="rule"></div>
    <p class="tagline" data-fr="Le cahier des charges officiel de chaque appellation française &amp;mdash;
      <b class=&quot;ct&quot;>__N__</b> décrets à consulter et télécharger. Choisissez une région, puis l'appellation,
      ou lancez une recherche." data-en="The official cahier des charges (specification) of every French appellation &amp;mdash; <b class=&quot;ct&quot;>__N__</b> decrees to read and download. Choose a region, then the appellation, or run a search.">Le cahier des charges officiel de chaque appellation française &mdash;
      <b class="ct">__N__</b> décrets à consulter et télécharger. Choisissez une région, puis l'appellation,
      ou lancez une recherche.</p>
  </header>

  <div class="feat">
    <div class="t"><b data-fr="Cour-Cheverny &amp;mdash; l'exemple traduit" data-en="Cour-Cheverny &amp;mdash; the translated example">Cour-Cheverny &mdash; l'exemple traduit</b>
      <p data-fr="Décret présenté page à page, en français et en anglais, avec outil de zoom." data-en="The decree shown page by page, in French and English, with a zoom tool.">Décret présenté page à page, en français et en anglais, avec outil de zoom.</p></div>
    <a href="AOC_Decree.html" data-fr="Voir l'exemple &amp;rarr;" data-en="See the example &amp;rarr;">Voir l'exemple &rarr;</a>
  </div>

  <div class="controls">
    <div class="field"><label for="q" data-fr="Recherche" data-en="Search">Recherche</label>
      <input id="q" type="search" placeholder="Nom d'appellation… (ex. Chinon, Pauillac)" data-fr-ph="Nom d'appellation… (ex. Chinon, Pauillac)" data-en-ph="Appellation name… (e.g. Chinon, Pauillac)" autocomplete="off"></div>
    <div class="field"><label for="reg" data-fr="Région" data-en="Region">Région</label>
      <select id="reg"></select></div>
    <div class="field"><label for="sub" data-fr="Sous-région" data-en="Sub-region">Sous-région</label>
      <select id="sub" disabled></select></div>
  </div>

  <p class="count" id="count"></p>
  <div class="rows" id="rows"></div>

  <div class="modal" id="modal" hidden>
    <div class="sheet">
      <button class="x" id="mx" aria-label="Fermer">&times;</button>
      <p class="mk" data-fr="Cahier des charges &amp;middot; choisir la langue" data-en="Specification &amp;middot; choose a language">Cahier des charges &middot; choisir la langue</p>
      <h3 id="mName"></h3>
      <p class="msub" id="mSub"></p>
      <div class="langs">
        <div class="lang">
          <div class="lh"><span class="flag">&#127467;&#127479;</span> <span data-fr="Français" data-en="French">Français</span>
            <span class="tag">Original</span></div>
          <div class="lb"><a id="mFrOpen" class="pri" target="_blank" rel="noopener" data-fr="Ouvrir" data-en="Open">Ouvrir</a>
            <a id="mFrDl" download data-fr="Télécharger &amp;darr;" data-en="Download &amp;darr;">Télécharger &darr;</a></div>
        </div>
        <div class="lang" id="mEnBox">
          <div class="lh"><span class="flag">&#127468;&#127463;</span> <span data-fr="Anglais" data-en="English">Anglais</span>
            <span class="tag" id="mEnTag">Traduction</span></div>
          <div class="lb" id="mEnActions"></div>
        </div>
      </div>
    </div>
  </div>

  <footer data-fr="<b>A Quick Glance at French Wine</b> &amp;middot; Cahiers des charges &amp;mdash; documents publics INAO.<br>
    <span id=&quot;tot&quot;>__N__</span> appellations. Le texte français original fait foi." data-en="<b>A Quick Glance at French Wine</b> &amp;middot; Cahiers des charges &amp;mdash; public INAO documents.<br>
    <span id=&quot;tot&quot;>__N__</span> appellations. Only the original French text is legally binding.">
    <b>A Quick Glance at French Wine</b> &middot; Cahiers des charges &mdash; documents publics INAO.<br>
    <span id="tot">__N__</span> appellations. Le texte français original fait foi.
  </footer>
</div>

<script>
const DATA=__DATA__;
const norm=s=>s.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase();
const REG=[]; const SUBS={};
DATA.forEach(d=>{ if(!REG.includes(d.region))REG.push(d.region);
  (SUBS[d.region]=SUBS[d.region]||[]).includes(d.sub)||SUBS[d.region].push(d.sub); });

const $=id=>document.getElementById(id);
// FR/EN: the site menu sets <html lang>; dynamic text follows it (re-rendered when it changes)
const isEN=()=>document.documentElement.lang==='en', T=(fr,en)=>isEN()?en:fr;
const REG_EN={"Bourgogne":"Burgundy","Loire":"Loire Valley","Sud-Ouest":"South-West","Rhône":"Rhône Valley",
  "Provence & Corse":"Provence & Corsica","Eaux-de-vie & Marcs":"Brandies & Marcs"};
const regName=r=>isEN()&&REG_EN[r]?REG_EN[r]:r;
const regSel=$('reg'), subSel=$('sub'), q=$('q'), rowsEl=$('rows'), countEl=$('count');
document.querySelector('.ct').textContent=DATA.length;
$('tot').textContent=DATA.length;

function fillRegs(){ const v=regSel.value;
  regSel.innerHTML='<option value="">'+T('Choisir une région…','Choose a region…')+'</option>'
    +REG.map(r=>`<option value="${r}">${regName(r)}</option>`).join('');
  regSel.value=v; }
fillRegs();

function fillSubs(){
  const r=regSel.value, keep=subSel.value;
  const subs=(SUBS[r]||[]).filter(s=>s!=='');
  if(!r||subs.length===0){ subSel.innerHTML='<option value="">—</option>'; subSel.disabled=true; }
  else{ subSel.disabled=false;
    subSel.innerHTML='<option value="">'+T('Toutes les sous-régions','All sub-regions')+'</option>'
      +subs.sort().map(s=>`<option>${s}</option>`).join('');
    if(subs.includes(keep)) subSel.value=keep; }
}

const PDF='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6"/></svg>';

function render(){
  const r=regSel.value, s=subSel.value, term=norm(q.value.trim());
  let list=DATA.filter(d=>(!r||d.region===r)&&(!s||d.sub===s)
      &&(!term||norm(d.appellation).includes(term)));
  if(!r && !term){
    rowsEl.innerHTML='<div class="empty">'+T('Choisissez une <b>région</b> ci-dessus '
      +'ou tapez le nom d\'une appellation pour commencer.<br>Les '+DATA.length
      +' décrets sont disponibles au téléchargement.',
      'Choose a <b>region</b> above or type an appellation name to start.<br>All '+DATA.length
      +' decrees are available to download.')+'</div>';
    countEl.textContent=''; return;
  }
  countEl.innerHTML='<b>'+list.length+'</b> '+(list.length>1?T('décrets','decrees'):T('décret','decree'))
     +(r?' &middot; '+regName(r):'')+(s?' &middot; '+s:'');
  if(list.length===0){ rowsEl.innerHTML='<div class="empty">'+T('Aucun décret ne correspond.','No decree matches.')+'</div>'; return; }
  const esc=t=>t.replace(/&/g,'&amp;').replace(/"/g,'&quot;');
  rowsEl.innerHTML=list.map(d=>{
    const sub=d.sub?d.sub+' &middot; ':'';
    const enBadge=d.en?'<span class="en">FR / EN</span>':'';
    const subline=(d.sub?d.sub+' · ':'')+regName(d.region);
    return `<div class="row"><span class="ic">${PDF}</span>
      <div class="info"><p class="name" title="${esc(d.appellation)}">${d.appellation}</p>
        <div class="meta">${sub}${regName(d.region)} &middot; ${d.sizeKB} ${T('Ko','KB')}${enBadge}</div></div>
      <div class="acts"><button type="button" class="consult" data-name="${esc(d.appellation)}"
        data-sub="${esc(subline)}" data-pdf-fr="${encodeURI(d.file)}"
        data-pdf-en="${d.en?encodeURI(d.en):''}">${T('Consulter','View')} &rsaquo;</button></div></div>`;
  }).join('');
}

// language chooser modal
const modal=$('modal'); let lastOpen=null;
function openChooser(name,sub,fr,en){
  $('mName').textContent=name; $('mSub').textContent=sub;
  $('mFrOpen').href=fr; $('mFrDl').href=fr;
  const box=$('mEnActions'), tag=$('mEnTag'), wrap=$('mEnBox');
  if(en){ wrap.classList.remove('soon'); tag.textContent=T('Traduction','Translation');
    box.innerHTML='<a class="pri" href="'+en+'" target="_blank" rel="noopener">'+T('Ouvrir','Open')+'</a>'
      +'<a href="'+en+'" download>'+T('Télécharger','Download')+' &darr;</a>'; }
  else{ wrap.classList.add('soon'); tag.textContent=T('Bientôt','Coming soon');
    box.innerHTML='<span class="soonmsg">'+T('Traduction anglaise à venir.','English translation coming soon.')+'</span>'; }
  lastOpen=[name,sub,fr,en];
  modal.hidden=false;
}
function closeChooser(){ modal.hidden=true; }
rowsEl.addEventListener('click',e=>{ const b=e.target.closest('.consult'); if(!b)return;
  openChooser(b.dataset.name,b.dataset.sub,b.dataset.pdfFr,b.dataset.pdfEn); });
$('mx').addEventListener('click',closeChooser);
modal.addEventListener('click',e=>{ if(e.target===modal) closeChooser(); });
document.addEventListener('keydown',e=>{ if(e.key==='Escape'&&!modal.hidden) closeChooser(); });

regSel.addEventListener('change',()=>{fillSubs();render();});
subSel.addEventListener('change',render);
q.addEventListener('input',render);
fillSubs(); render();
// re-draw the dynamic parts when the site language changes (the menu sets <html lang> after this script runs)
new MutationObserver(()=>{ fillRegs(); fillSubs(); render();
  if(!modal.hidden&&lastOpen) openChooser(...lastOpen); })
  .observe(document.documentElement,{attributes:true,attributeFilter:['lang']});
</script>
</body>
</html>
'''
HTML=HTML.replace("__DATA__",JSON).replace("__N__",str(len(data)))
open(os.path.join(DEST,"AOC_Library.html"),"w").write(HTML)
print("wrote AOC_Library.html  (",len(HTML),"bytes,",len(data),"entries )")
