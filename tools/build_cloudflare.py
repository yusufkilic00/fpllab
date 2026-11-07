#!/usr/bin/env python3
"""Build Cloudflare Pages static output from committed web_data chunks."""
from __future__ import annotations
import json, shutil
from pathlib import Path
from webdata import SAFE_ASSET_LIMIT, reconstruct_web_data

ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/'dist'
WEB_DATA=ROOT/'web_data'


def coverage_label(gws):
    lo,hi=min(gws),max(gws)
    return f"GW {lo:02d} — {hi:02d}", f"{len(gws):02d} GW", f"{lo}–{hi}"


def production_index(data):
    html=(ROOT/'index.html').read_text(encoding='utf-8')
    gw_label,gw_count,gw_short=coverage_label([int(x) for x in data['gws']])
    html=html.replace('<html lang="en">','<html class="production" lang="en">',1)
    html=html.replace('LOCAL ANALYTICS WORKSPACE','FOOTBALL ANALYTICS PLATFORM')
    html=html.replace('Monitor your dataset and apply verified local updates.','Monitor dataset coverage, integrity and published updates.')
    html=html.replace('GW 01 — 09',gw_label).replace('09 GW',gw_count)
    html=html.replace('GW 01–09',gw_label.replace(' — ','–')).replace('GW 01—09',gw_label.replace(' — ','—'))
    html=html.replace('Indexed (1–9)',f'Indexed ({gw_short})')
    html=html.replace('<div class="upload-zone">','<div class="upload-zone" data-local-only>',1)
    html=html.replace('<article class="pane import-pane" id="importPanel">','<article class="pane import-pane" data-local-only id="importPanel">',1)
    old='<script src="data.js"></script><script src="app.js"></script><script src="jszip.min.js"></script><script src="updates.js"></script>'
    if old not in html: raise SystemExit('Could not locate local script bundle in index.html')
    return html.replace(old,'<script src="data-loader.js"></script>')


def loader_js():
 return r'''(() => {
'use strict';
const boot=document.createElement('div');boot.id='fplBoot';boot.setAttribute('role','status');boot.innerHTML='<div><strong>FPL LAB</strong><span id="fplBootText">Loading analytics data…</span></div>';document.body.appendChild(boot);
const status=t=>{const el=document.getElementById('fplBootText');if(el)el.textContent=t;};
const getJson=async url=>{const r=await fetch(url,{cache:'default'});if(!r.ok)throw Error(`${url}: HTTP ${r.status}`);return r.json();};
const loadScript=src=>new Promise((resolve,reject)=>{const s=document.createElement('script');s.src=src;s.onload=resolve;s.onerror=()=>reject(Error(`Could not load ${src}`));document.body.appendChild(s);});
const mergeNested=(target,source)=>{for(const [id,weeks] of Object.entries(source||{})){if(!target[id])target[id]={};Object.assign(target[id],weeks);}};
(async()=>{try{const manifest=await getJson('data/manifest.json');status(`Loading ${manifest.gameweeks.length} indexed gameweeks…`);const core=await getJson('data/'+manifest.core.file);core.snapshots={};core.playerMatch={};core.eventPlayer={};core.events=[];const chunks=await Promise.all(manifest.gameweeks.map(g=>getJson('data/'+g.file)));chunks.sort((a,b)=>Number(a.gw)-Number(b.gw));for(const chunk of chunks){mergeNested(core.snapshots,chunk.snapshots);mergeNested(core.playerMatch,chunk.playerMatch);mergeNested(core.eventPlayer,chunk.eventPlayer);core.events.push(...(chunk.events||[]));}window.FPL_V2=core;status('Starting analytics workspace…');await loadScript('app.js');boot.remove();}catch(err){console.error(err);status('Could not load the published dataset. Refresh the page or contact the site administrator.');boot.classList.add('error');}})();
})();
'''


def main():
    data,manifest=reconstruct_web_data(WEB_DATA)
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    shutil.copytree(WEB_DATA,DIST/'data')
    for name in ('app.js','styles.css'): shutil.copy2(ROOT/name,DIST/name)
    if (ROOT/'assets').exists(): shutil.copytree(ROOT/'assets',DIST/'assets')
    (DIST/'index.html').write_text(production_index(data),encoding='utf-8')
    (DIST/'404.html').write_text(production_index(data),encoding='utf-8')
    (DIST/'data-loader.js').write_text(loader_js(),encoding='utf-8')
    (DIST/'_headers').write_text("""/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n\n/data/manifest.json\n  Cache-Control: no-cache\n\n/data/*.json\n  Cache-Control: public, max-age=31536000, immutable\n\n/data-loader.js\n  Cache-Control: no-cache\n\n/app.js\n  Cache-Control: no-cache\n""",encoding='utf-8')
    css=DIST/'styles.css';css.write_text(css.read_text(encoding='utf-8')+'''\n\n/* Cloudflare production shell */\n.production [data-local-only]{display:none!important}\n#fplBoot{position:fixed;inset:0;z-index:99999;display:grid;place-items:center;background:var(--bg,#0f1512);color:var(--text,#f4f6f5);font-family:Inter,system-ui,sans-serif}\n#fplBoot>div{display:grid;gap:.55rem;text-align:center;padding:1.4rem 1.7rem;border:1px solid rgba(255,255,255,.12);border-radius:14px;background:rgba(255,255,255,.04)}\n#fplBoot strong{letter-spacing:.14em;font-size:.88rem}#fplBoot span{opacity:.72;font-size:.82rem}#fplBoot.error span{color:#e6a09f;opacity:1}\n''',encoding='utf-8')
    largest=[]
    for path in DIST.rglob('*'):
      if path.is_file():
       size=path.stat().st_size
       if size>SAFE_ASSET_LIMIT: raise SystemExit(f'Output asset exceeds safe limit: {path.relative_to(DIST)} = {size:,} bytes')
       largest.append((size,str(path.relative_to(DIST))))
    largest.sort(reverse=True)
    print(json.dumps({'ok':True,'build':manifest['build'],'gameweeks':data['gws'],'files':sum(1 for p in DIST.rglob('*') if p.is_file()),'largest_assets':[{'file':n,'bytes':s} for s,n in largest[:8]]},indent=2))

if __name__=='__main__': main()
