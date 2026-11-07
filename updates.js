(() => {
'use strict';
const byId=x=>document.getElementById(x);
const status=byId('importResult');
const say=t=>{if(status)status.textContent=t;};
const ALIASES={'afc bournemouth':'bournemouth','brighton hove albion':'brighton','leeds united':'leeds','manchester city':'man city','manchester united':'man utd','newcastle united':'newcastle','nottingham forest':"nott'm forest",'tottenham hotspur':'spurs'};
const norm=s=>String(s||'').toLowerCase().replace(/[._-]+/g,' ').replace(/[^a-z0-9 '&]+/g,' ').replace(/\s+/g,' ').trim();
function saveLocalCrest(id,src){try{localStorage.setItem('fpl-crest-'+id,src);return true}catch{return false}}
async function loadClubCrests(file){if(!window.JSZip)throw Error('ZIP engine missing from installation.');const zip=await JSZip.loadAsync(file);const D=window.FPL_V2;let count=0,skipped=0;let storageSkipped=0;for(const [name,entry] of Object.entries(zip.files)){
 if(entry.dir||!/(png|webp|jpg|jpeg)$/i.test(name))continue;
 const fileName=name.split('/').at(-1).replace(/\.(png|webp|jpg|jpeg)$/i,'').replace(/[_-]?ClubLogo/i,'');
 const key=norm(fileName);const mapped=ALIASES[key]||key;
 const team=D.teams.find(t=>norm(t.name)===mapped||norm(t.short)===mapped);
 if(!team){skipped++;continue}
 const mime=/\.webp$/i.test(name)?'image/webp':/\.jpe?g$/i.test(name)?'image/jpeg':'image/png';
 const bytes=await entry.async('uint8array');if(bytes.length>120_000){storageSkipped++;continue}
 // Process in chunks; String.fromCharCode(...large array) would exceed argument limit.
 let binary='';for(let i=0;i<bytes.length;i+=12000)binary+=String.fromCharCode(...bytes.subarray(i,i+12000));
 if(saveLocalCrest(String(team.id),'data:'+mime+';base64,'+btoa(binary)))count++;else storageSkipped++;
 }
 return {count,skipped,storageSkipped};
}
async function sendDataFiles(performance,events){const fd=new FormData();if(performance)fd.set('performance',performance);if(events)fd.set('events',events);const controller=new AbortController();const res=await fetch('/api/import',{method:'POST',body:fd,signal:controller.signal});const payload=await res.json();if(!res.ok)throw Error(payload.error||`Update failed (${res.status})`);return payload;}
byId('applyDataUpdates')?.addEventListener('click',async()=>{
 const performance=byId('uploadPerformance').files[0],events=byId('uploadEvents').files[0],crests=byId('uploadCrests').files[0];
 if(!performance&&!events&&!crests){say('Choose at least one ZIP archive.');return}
 for(const file of [performance,events,crests])if(file&&!file.name.toLowerCase().endsWith('.zip')){say('ZIP archive required: '+file.name);return}
 const btn=byId('applyDataUpdates');btn.disabled=true;
 try{
  if(performance||events){say('Validating source ZIPs and rebuilding the local data…');const result=await sendDataFiles(performance,events);say(`Validated ${result.stats.fixtures} matches, ${result.stats.players} players and ${result.stats.events.toLocaleString()} events. Refreshing…`);}
  if(crests){const r=await loadClubCrests(crests);say(`Imported ${r.count} authentic local crests; ${r.skipped} unmatched and ${r.storageSkipped} skipped because the image was over 120 KB or browser storage was full. Refreshing…`);}
  setTimeout(()=>location.reload(),900);
 }catch(err){say('Update not applied: '+err.message+'. For updates use the included local server (python server.py).');console.error(err)}finally{btn.disabled=false}
});
byId('exportDataInfo')?.addEventListener('click',()=>{
 const D=window.FPL_V2;const obj={season:D.season,gameweeks:D.gws,teams:D.teams,players:D.players.length,fixtures:D.fixtures.length,events:D.events.length,metrics:D.metrics.map(({key,label,source,mode,kind,category,help})=>({key,label,source,mode,kind,category,help})),note:'Cumulative FPL snapshot values are not per-GW aggregates.'};
 const url=URL.createObjectURL(new Blob([JSON.stringify(obj,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='FPL_LAB_Data_Catalog.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),800);
});
})();
