import sys,json
sys.path.insert(0,sys.path[0])
from bs4 import BeautifulSoup
from common import targets
soup=BeautifulSoup(open(sys.argv[1]).read(),'html.parser')
loose=[];T=targets(soup.body,[],loose)
d={}
for el in T: d.setdefault(el.decode_contents().strip(),'')
json.dump({'title':soup.title.string,'strings':d},open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
print(len(d),'strings; loose:',[(p.name,p.get('class'),s.strip()[:50]) for p,s in loose][:30])
