#!/usr/bin/env python3
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse
DB=os.environ.get('WVT_PLAY_DB', os.path.join(os.path.dirname(__file__), 'devices.json'))
def load():
 try:
  with open(DB) as f:return json.load(f)
 except Exception:return {'WVT-DEMO-1234':{'pin':'1234','playlists':[]}}
def save(d):
 with open(DB,'w') as f:json.dump(d,f)
class H(BaseHTTPRequestHandler):
 def out(self,c,o):
  b=json.dumps(o).encode();self.send_response(c);self.send_header('Content-Type','application/json');self.send_header('Access-Control-Allow-Origin','*');self.send_header('Content-Length',str(len(b)));self.end_headers();self.wfile.write(b)
 def do_OPTIONS(self):
  self.send_response(204);self.send_header('Access-Control-Allow-Origin','*');self.send_header('Access-Control-Allow-Methods','GET,POST,DELETE,OPTIONS');self.send_header('Access-Control-Allow-Headers','Content-Type,X-Device-Pin');self.end_headers()
 def do_GET(self):
  p=urlparse(self.path).path.split('/')
  if len(p)==4 and p[1:3]==['api','devices']:
   key=p[3].upper();data=load();d=data.get(key)
   if not d:
    d={'pin':'','playlists':[]};data[key]=d;save(data)
   return self.out(200,{'device_key':key,'playlists':d['playlists']})
  self.out(404,{'error':'not_found'})
 def do_DELETE(self):
  p=urlparse(self.path).path.split('/')
  if len(p)==6 and p[1:3]==['api','devices'] and p[4]=='playlists':
   data=load();d=data.get(p[3].upper())
   if not d:return self.out(404,{'error':'device_not_found'})
   try:i=int(p[5]);d['playlists'].pop(i)
   except (ValueError,IndexError):return self.out(404,{'error':'playlist_not_found'})
   save(data);return self.out(200,{'ok':True})
  self.out(404,{'error':'not_found'})
 def do_POST(self):
  p=urlparse(self.path).path.split('/');n=int(self.headers.get('Content-Length','0'));body=json.loads(self.rfile.read(n) or '{}')
  if p==['','api','devices']:
   key=str(body.get('device_key','')).strip().upper();pin=str(body.get('pin','')).strip()
   if not key or not pin:return self.out(400,{'error':'device_key_and_pin_required'})
   data=load(); data.setdefault(key,{'pin':pin,'playlists':[]}); data[key]['pin']=pin; save(data)
   return self.out(201,{'device_key':key})
  if len(p)==5 and p[1:3]==['api','devices'] and p[4]=='playlists':
   d=load().get(p[3]);
   if not d:return self.out(404,{'error':'device_not_found'})
   # O portal atual autentica pelo Device Key; PIN legado é aceito quando enviado,
   # mas não bloqueia o novo fluxo sem PIN.
   if 'pin' in body and d.get('pin') and str(body.get('pin',''))!=str(d['pin']):return self.out(401,{'error':'invalid_pin'})
   item={k:body.get(k,'') for k in ('name','kind','source','user','pass')};d['playlists'].append(item);data=load();data[p[3]]=d;save(data);return self.out(201,item)
  self.out(404,{'error':'not_found'})
if __name__=='__main__':ThreadingHTTPServer(('0.0.0.0',8788),H).serve_forever()
