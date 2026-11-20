"""Local static preview mirroring Vercel's exact rewrites; never handles POST."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import json

ROOT = Path(__file__).resolve().parent.parent
routes = {r['source']: r['destination'] for r in json.loads((ROOT / 'vercel.json').read_text()).get('rewrites', [])}
class Handler(SimpleHTTPRequestHandler):
 def do_GET(self):
  path=urlsplit(self.path).path
  if path in routes:
   self.path=routes[path]
  super().do_GET()
 def do_HEAD(self):
  path=urlsplit(self.path).path
  if path in routes:self.path=routes[path]
  super().do_HEAD()

if __name__ == '__main__':
 print('Local: http://127.0.0.1:8000',flush=True)
 ThreadingHTTPServer(('127.0.0.1',8000),partial(Handler,directory=str(ROOT))).serve_forever()
