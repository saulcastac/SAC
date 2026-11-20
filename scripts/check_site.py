"""Structural, routing and native-form regression checks. No real submissions."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import urlopen
import json
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent.parent
config=json.loads((ROOT/'vercel.json').read_text())
routes={r['source']:r['destination'].lstrip('/') for r in config['rewrites']}
origin=json.loads((ROOT/'site-config.json').read_text())['origin']
class Page(HTMLParser):
 def __init__(self):super().__init__();self.nodes=[]
 def handle_starttag(self,tag,attrs):self.nodes.append((tag,dict(attrs)))
 def handle_startendtag(self,tag,attrs):self.handle_starttag(tag,attrs)

pages={}
for file in [ROOT/'index.html',ROOT/'gracias.html',ROOT/'privacidad.html',*sorted((ROOT/'servicios').glob('*.html'))]:
 page=Page();page.feed(file.read_text());pages[file.relative_to(ROOT).as_posix()]=page
 ids=[a['id'] for _,a in page.nodes if 'id' in a]
 assert len(ids)==len(set(ids)),f'Duplicate ids in {file}'
 assert sum(tag=='h1' for tag,_ in page.nodes)==1,f'H1 in {file}'
 titles=[a for tag,a in page.nodes if tag=='title'];assert len(titles)==1
 for tag,a in page.nodes:
  if tag in ('a','link','script','img'):
   url=a.get('href',a.get('src',''));parts=urlsplit(url)
   if parts.scheme or parts.netloc:continue
   if parts.path:
    target=parts.path.lstrip('/') if parts.path.startswith('/') else str(file.relative_to(ROOT).parent / parts.path)
    target=routes.get('/'+target,target)
    if target in ('','.'):target='index.html'
    assert (ROOT/target).exists(),f'Broken resource {file}: {url}'
   elif parts.fragment:target=file.relative_to(ROOT).as_posix()
   else:continue
   if parts.fragment:
    target_page=Page();target_page.feed((ROOT/target).read_text())
    assert any(a.get('id')==parts.fragment for _,a in target_page.nodes),f'Broken anchor {file}: {url}'
 if file.name not in ('gracias.html','privacidad.html'):
  forms=[a for tag,a in page.nodes if tag=='form'];assert len(forms)==1
  assert forms[0]['method']=='POST' and forms[0]['action']=='https://formsubmit.co/saulcastac@gmail.com'
  inputs={a.get('name'):a for tag,a in page.nodes if tag in ('input','textarea')}
  for name in ['nombre','email','mensaje','consentimiento']:assert 'required' in inputs[name]
  assert 'required' not in inputs['empresa']
  for name in ['_subject','_template','_next','_honey','servicio_origen','landing_origen','utm_source','utm_medium','utm_campaign','utm_content','utm_term']:assert name in inputs,name
  assert inputs['_next']['value']==origin+'/gracias.html'
  assert '_captcha' not in inputs
 if file.parent.name=='servicios':
  assert any(a.get('rel')=='canonical' and a.get('href')==origin+'/servicios/'+file.stem for _,a in page.nodes)
  for key in ['og:title','og:description','og:image','og:url']:assert any(a.get('property')==key for _,a in page.nodes)
  assert inputs['servicio_origen']['value']==file.stem
  assert file.stem in forms[0]['data-service']
  assert len([a for tag,a in page.nodes if tag=='details'])>=4
assert not config.get('buildCommand') and not config.get('installCommand') and config['outputDirectory']=='.'
assert len(routes)==4
ET.parse(ROOT/'sitemap.xml')
for path in ['/',*routes,'/privacidad.html','/gracias.html','/styles.css','/main.js','/analytics.js','/og-image.png','/sitemap.xml','/robots.txt']:
 with urlopen('http://127.0.0.1:8000'+path) as response:
  assert response.status==200,path
print('PASS: 7 pages; 4 clean routes; internal links/anchors/assets; metadata; native forms; sitemap; HTTP resources; buildless Vercel configuration.')
