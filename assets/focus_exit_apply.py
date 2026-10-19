import sys,re
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'function focusToggle(' in s: print('skip',f); continue
    def rep(a,b,n=1):
        global s
        assert s.count(a)==n,(f,a[:70],s.count(a)); s=s.replace(a,b)
    # remember which appellation is in focus; clicking it again (sidebar row / popup line) leaves focus mode
    rep("  var FOCUS_CODES=null;\n  function setFocus(set){ FOCUS_CODES=(set&&set.size)?set:null;",
        "  var FOCUS_CODES=null, FOCUS_NAME=null, FOCUS_NEXT=null;\n"
        "  function focusToggle(name){ if(FOCUS_CODES&&FOCUS_NAME===name){ clearHighlight(); return true; } FOCUS_NEXT=name; return false; }\n"
        "  document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&FOCUS_CODES) clearHighlight(); });\n"
        "  function setFocus(set){ FOCUS_CODES=(set&&set.size)?set:null; FOCUS_NAME=FOCUS_CODES?FOCUS_NEXT:null;")
    for fn in [x for x in ['highlightAppel','highlightFill','highlightRegional'] if 'function '+x+'(' in s]:
        pat=re.compile(r"(function "+fn+r"\(name(?:,color)?\)\{\n)(\s*)clearHighlight\(\);")
        assert len(pat.findall(s))==1,(f,fn)
        s=pat.sub(lambda m: m.group(1)+m.group(2)+"if(focusToggle(name)) return;\n"+m.group(2)+"clearHighlight(); FOCUS_NEXT=name;",s)
    # clicking a faded commune (outside the focused appellation) also leaves focus mode
    if 'if(SEL_DENOM.size && !SEL_DENOM.has(code)) clearHighlight();' in s:
        rep('if(SEL_DENOM.size && !SEL_DENOM.has(code)) clearHighlight();',
            'if((SEL_DENOM.size && !SEL_DENOM.has(code)) || (FOCUS_CODES && !FOCUS_CODES.has(code))) clearHighlight();')
    else:
        rep("lyr.on('click',function(e){ L.DomEvent.stop(e); pinTip(code,nom,e);",
            "lyr.on('click',function(e){ L.DomEvent.stop(e); if(FOCUS_CODES && !FOCUS_CODES.has(code)) clearHighlight(); pinTip(code,nom,e);")
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
