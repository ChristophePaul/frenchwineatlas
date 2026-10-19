"""apply.py page.html keys.json fr.txt out.html — add data-fr/data-en to every translated text block; French becomes the default."""
import sys,json,re
sys.path.insert(0,sys.path[0])
from bs4 import BeautifulSoup
from common import targets
page,keysf,frf,out=sys.argv[1:5]
keys=json.load(open(keysf))
fr={}
for line in open(frf,encoding='utf-8'):
    line=line.rstrip('\n')
    if not line.strip(): continue
    i,t=line.split('\t',1); fr[int(i)]=t
missing=[i for i in range(len(keys)) if i not in fr]
assert not missing, ('missing',missing[:20])
def compress(x):
    x=re.sub(r'\s+',' ',x).strip()
    x=re.sub(r'<a href="(https?[^"]*)"[^>]*>',r'<a {\1}>',x)
    return x
def expand(t,orig):
    t=re.sub(r'<a \{([^}]*)\}>',lambda m:'<a href="%s" rel="noopener noreferrer" target="_blank">'%m.group(1),t)
    o=orig.strip()
    if o.startswith('<strong>') and o.endswith('</strong>') and o.count('<strong>')==1 and not t.startswith('<strong>'):
        t='<strong>'+t+'</strong>'
    return t
# compare without <strong> wrappers where the key list stored them stripped
m={}
for i,k in enumerate(keys[1:],1):
    if fr[i].strip()!='=': m[compress(k)]=fr[i]
soup=BeautifulSoup(open(page,encoding='utf-8').read(),'html.parser')
done=0;left=[]
for el in targets(soup.body,[],[]):
    orig=el.decode_contents().strip()
    c=compress(orig)
    if c not in m:
        txt=re.sub(r'<[^>]+>','',c)
        if re.search(r'\d[.,]\d',txt) and not re.search(r'[A-Za-z]{4,}',txt.replace('variable','')):
            f=re.sub(r'(\d),(\d{3})',lambda q:q.group(1)+' '+q.group(2),orig)
            f=re.sub(r'(\d)\.(\d)',r'\1,\2',f)
            if f!=orig:
                el['data-en']=orig; el['data-fr']=f; el.clear(); el.append(BeautifulSoup(f,'html.parser')); done+=1
            continue
        if re.search(r'[a-z]{3}',re.sub(r'<[^>]+>','',c)) and re.search(r'[A-Za-z]{3,}',c): left.append(c[:80])
        continue
    f=expand(m[c],orig)
    el['data-en']=orig; el['data-fr']=f
    el.clear(); el.append(BeautifulSoup(f,'html.parser'))
    done+=1
soup.title['data-en']=soup.title.string; soup.title['data-fr']=fr[0]; soup.title.string=fr[0]
soup.html['lang']='fr'
open(out,'w',encoding='utf-8').write(str(soup))
print('translated',done,'| untranslated with words:',len(left)); print('\n'.join(left))
