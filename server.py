#!/usr/bin/env python3
"""Local-only FPL LAB server: static UI plus validated cumulative ZIP updates."""
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from email.parser import BytesParser
from email import policy
from pathlib import Path
from tempfile import TemporaryDirectory
from datetime import datetime
import json,os,shutil,sys,webbrowser
from urllib.request import Request,urlopen
from urllib.error import URLError,HTTPError
from threading import Timer
from tools.rebuild import build
from tools.webdata import export_web_data
ROOT=Path(__file__).resolve().parent
os.chdir(ROOT)
HOST='127.0.0.1';PORT=int(os.environ.get('FPL_LAB_PORT','8765'))
class Handler(SimpleHTTPRequestHandler):
 def log_message(self,format,*args):print('[FPL LAB]',format%args)
 def do_GET(self):
  if self.path=='/api/status':
   data={'status':'ready','product':'FPL LAB','server':'local','updates':'manual zip'};return self.respond(200,data)
  if self.path=='/api/fpl/bootstrap-static':return self.proxy_fpl('https://fantasy.premierleague.com/api/bootstrap-static/')
  if self.path=='/api/fpl/fixtures':return self.proxy_fpl('https://fantasy.premierleague.com/api/fixtures/')
  return super().do_GET()
 def proxy_fpl(self,url):
  try:
   req=Request(url,headers={'Accept':'application/json','User-Agent':'FPL-LAB/1.0'})
   with urlopen(req,timeout=10) as r:raw=r.read();status=getattr(r,'status',200)
   self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','public, max-age=300');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(raw)
  except (URLError,HTTPError,TimeoutError) as exc:
   return self.respond(502,{'error':'FPL upstream unavailable','detail':str(exc)[:160]})
 def respond(self,status,payload):
  raw=json.dumps(payload).encode('utf-8');self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(raw)
 def do_POST(self):
  if self.path!='/api/import':return self.respond(404,{'error':'Unknown endpoint'})
  length=int(self.headers.get('content-length','0'))
  if length<=0 or length>95_000_000:return self.respond(413,{'error':'Archive upload must be smaller than 95 MB'})
  ctype=self.headers.get('content-type','')
  if not ctype.startswith('multipart/form-data;'):return self.respond(400,{'error':'Use multipart/form-data'})
  try:
   body=self.rfile.read(length)
   msg=BytesParser(policy=policy.default).parsebytes(('Content-Type: '+ctype+'\r\nMIME-Version: 1.0\r\n\r\n').encode()+body)
   parts={p.get_param('name',header='content-disposition'):p.get_payload(decode=True) for p in msg.iter_parts() if p.get_param('name',header='content-disposition') in ('performance','events')}
   if not parts:return self.respond(400,{'error':'No archive files were uploaded'})
   archive=ROOT/'source_archives';archive.mkdir(exist_ok=True)
   with TemporaryDirectory(prefix='fpl-update-',dir=ROOT) as tmp:
    tmp=Path(tmp);paths={}
    for key,name in [('performance','Premier-League-2026-2027.zip'),('events','EPL_2026_2027_English_Teams_By_Gameweek.zip')]:
     if key in parts:
      path=tmp/name;path.write_bytes(parts[key]);paths[key]=path
     else:
      path=archive/name
      if not path.exists():raise ValueError(f'Existing {key} ZIP not found. Upload both archives.')
      paths[key]=path
    generated=tmp/'data.js'
    stats=build(paths['performance'],paths['events'],generated)
    generated_web=tmp/'web_data'
    export_web_data(generated,generated_web)
    # Commit only after source validation and deploy-data generation both succeeded.
    bak=ROOT/'backups';bak.mkdir(exist_ok=True)
    stamp=datetime.now().strftime('%Y%m%d_%H%M%S')
    if (ROOT/'data.js').exists():shutil.copy2(ROOT/'data.js',bak/f'data_{stamp}.js')
    os.replace(generated,ROOT/'data.js')
    if (ROOT/'web_data').exists():shutil.rmtree(ROOT/'web_data')
    shutil.move(str(generated_web),str(ROOT/'web_data'))
    for key in parts:
     name='Premier-League-2026-2027.zip' if key=='performance' else 'EPL_2026_2027_English_Teams_By_Gameweek.zip'
     os.replace(paths[key],archive/name)
    return self.respond(200,{'ok':True,'stats':stats})
  except Exception as exc:
   print('Import rejected:',repr(exc),file=sys.stderr)
   return self.respond(422,{'ok':False,'error':str(exc)[:500]})
if __name__=='__main__':
 print(f'FPL LAB is available locally at http://{HOST}:{PORT}')
 httpd=ThreadingHTTPServer((HOST,PORT),Handler)
 if '--open' in sys.argv:Timer(1,lambda:webbrowser.open(f'http://{HOST}:{PORT}/')).start()
 httpd.serve_forever()
