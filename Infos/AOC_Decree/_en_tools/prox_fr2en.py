"""prox_fr2en.py slug [pages] — render the French 'aire de proximité immédiate' department lists as English lines
(proposed text: struck items dropped). Prints '- X department: a, b and c;' lines."""
import re, sys, subprocess
slug = sys.argv[1]
import os
if os.path.isfile(slug):
    t = open(slug, encoding='utf-8').read()
else:
    args = ['python3', '_en_tools/extract_fr.py', slug] + sys.argv[2:3]
    t = subprocess.run(args, capture_output=True, text=True).stdout
t = re.sub(r'[ \t\u00a0]+', ' ', t)
a = re.search(r'proximité\s+immédiate,?\s*définie', t).start()
a = t.index('- Département', a)
m = re.search(r'\*\*V\.|V\. ?-|V\.-|V\. Encépagement|\bV - Encépagement', t[a:])
s = t[a:a + m.start()]
s = re.sub(r'=== p\d+', ' ', s)
s = re.sub(r'(?m)^RUNNING:.*$', ' ', s)
s = re.sub(r"(?:/?/?)Procédure nationale d[’']opposition.*?(?:\d{2}/\d{2}/\d{4}|\d{1,2} \w+ \d{4})", ' ', s, flags=re.S)
s = re.sub(r'~~[^~]*~~', '', s)
s = re.sub(r'Publié au [^0-9]*\d{1,2}/\d{2}/\d{4}\.?', ' ', s)
s = re.sub(r'Publié au BO[^0-9]*\d{1,2} \w+ \d{4}', ' ', s)
s = re.sub(r'\s+', ' ', s.replace('\n', ' '))
s = s.replace('uniquement en ce qui concerne le territoire', 'pour la partie du territoire')
s = re.sub(r'- (\w)', r'- \1', s)
s = s.replace('-  ', '- ').replace('**', '').replace('//', ' ')
s = re.sub(r'(\w)- (\w)', r'\1-\2', s)
s = re.sub(r'commune-?de-? ?', 'commune de ', s).replace('communes-de-', 'communes de ').replace('pour-la-partie', 'pour la partie').replace('pour-la- partie', 'pour la partie')
fix = {'Dareize': 'Dareizé', 'les Olmes': 'Les Olmes', 'Saint loup': 'Saint-Loup'}
def one(m): return f'(for the part of the territory corresponding to the former commune of {m.group(1).strip()})'
def many(m):
    n = [fix.get(x.strip(), x.strip()) for x in m.group(1).replace(' et ', ', ').split(',') if x.strip()]
    return '(for the part of the territory corresponding to the former communes of ' + ', '.join(n[:-1]) + ' and ' + n[-1] + ')'
s = re.sub(r"\(pour la partie du territoire correspondant à l['’]ancienne commune de ([^)]*)\)", one, s)
s = re.sub(r"\(pour la partie du territoire correspondant aux anciennes communes de ([^)]*)\)", many, s)
s = s.replace('Vindry sur Turdine', 'Vindry-sur-Turdine')
parts = re.split(r"-\s*(?:Dans le )?[Dd]épartement (?:de la |du |de l['’]|de )", s)[1:]
names = {"Côte-d'Or": 'Côte-d’Or', 'Côte-d’Or': 'Côte-d’Or', 'Rhône': 'Rhône', 'Saône-et-Loire': 'Saône-et-Loire', 'Yonne': 'Yonne'}
out = []
for i, p in enumerate(parts):
    name, rest = p.split(':', 1)
    name = names.get(name.strip(), name.strip())
    rest = re.sub(r'\s+', ' ', rest).strip().rstrip(';.').strip()
    prot = re.sub(r'\([^)]*\)', lambda m: m.group(0).replace(',', '\x00').replace(' and ', '\x01'), rest)
    items = [x.strip().replace('\x00', ',').replace('\x01', ' and ') for x in re.split(r',| et ', prot) if x.strip()]
    items = [re.sub(r'(\w)- (\w)', r'\1-\2', x.replace("'", '’')) for x in items]
    body = ', '.join(items[:-1]) + ' and ' + items[-1]
    out.append(f'- {name} department: {body}' + ('.' if i == len(parts) - 1 else ';'))
print('\n'.join(out))
