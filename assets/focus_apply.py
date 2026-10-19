import sys
WRAP="""// focus mode: while an appellation is located, every other appellation fill fades to 10 %
  var FOCUS_CODES=null;
  function setFocus(set){ FOCUS_CODES=(set&&set.size)?set:null; communeLayer.setStyle(baseStyle);
    var sp=map.getPane('secteurPane'); if(sp) sp.style.opacity=FOCUS_CODES?'0.1':''; }
  function baseStyle(f){ const st=baseStyle0(f);
    if(FOCUS_CODES && !FOCUS_CODES.has(f.properties.code) && st.fillOpacity<1)
      return Object.assign({},st,{color:'#c9bfa6',weight:0.4,fillOpacity:0.1});
    return st; }
  function baseStyle0(f){ const code=f.properties.code;"""
for f in sys.argv[1:]:
    s=open(f,encoding='utf-8').read()
    if 'function setFocus(' in s: print('skip',f); continue
    def rep(a,b,n=1):
        global s
        assert s.count(a)==n,(f,a[:60],s.count(a)); s=s.replace(a,b)
    rep("function baseStyle(f){ const code=f.properties.code;",WRAP)
    rep("function clearHighlight(){ ","function clearHighlight(){ if(FOCUS_CODES) setFocus(null); ")
    if 'function highlightAppel(' in s:
        rep("    var set=APPEL_CODES[name]; if(!set) return;\n","    var set=APPEL_CODES[name]; if(!set) return;\n    setFocus(set);\n")
    if 'function highlightFill(' in s:
        rep("var set={}; codes.forEach(function(c){set[c]=1;});","var set={}; codes.forEach(function(c){set[c]=1;}); setFocus(new Set(codes));")
    if 'function highlightRegional(' in s:
        rep("var st=APPEL_CODES[name]; if(!st||!st.size) return;","var st=APPEL_CODES[name]; if(!st||!st.size) return;\n    setFocus(st);")
    open(f,'w',encoding='utf-8').write(s); print('ok',f)
