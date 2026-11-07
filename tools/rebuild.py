#!/usr/bin/env python3
"""Rebuild FPL LAB's local dataset from the supplied season ZIPs.

Phase 5 correctness rules:
- no third-party APIs are called;
- duplicate logical CSVs are accepted only when byte-identical;
- completed/part-completed gameweeks are indexed match-by-match (no "must be 10" rule);
- the full 38-GW fixture schedule is preserved separately for planning;
- provider player IDs are cross-walked conservatively using gameweek club history;
- Opta semantics used by FPL LAB are explicit: crosses are not passes, own goals are
  not attacking shots, type 61 is a bad/unsuccessful touch rather than total touches;
- match-stat aggregation is field-aware (sum, max, mean-match-rate, snapshot), and
  all-null/non-aggregate fields are not exposed as usable metrics;
- missing event-derived data is not silently converted to zero.
"""
from __future__ import annotations
import collections,csv,hashlib,io,json,re,sys,zipfile,unicodedata
from pathlib import Path
from datetime import datetime,timezone

ROOT=Path(__file__).resolve().parents[1]
ALIAS={
 'AFC Bournemouth':'Bournemouth','Brighton & Hove Albion':'Brighton','Brighton Hove Albion':'Brighton',
 'Leeds United':'Leeds','Manchester City':'Man City','Manchester United':'Man Utd',
 'Newcastle United':'Newcastle','Nottingham Forest':"Nott'm Forest",'Tottenham Hotspur':'Spurs'
}
# Raw Opta event types supported by the product. Type 1 is split into pass/cross by
# qualifier 2, type 16 with qualifier 28 becomes own_goal, and type 61 is labelled
# bad_touch because it is not a total-touch event.
KIND={1:'pass',13:'shot',14:'shot',15:'shot',16:'shot',7:'tackle',8:'interception',12:'clearance',49:'recovery',44:'aerial',74:'blockedpass',83:'tackle_attempt',61:'bad_touch',4:'foul',3:'take_on',45:'challenge'}
CALC=[('c:xg90','xG /90','attacking'),('c:xa90','xA /90','attacking'),('c:shots90','Shots /90','attacking'),('c:points90','FPL Points /90','fpl'),('c:xgi','xG + xA','attacking'),('c:gi','Goals + assists','attacking'),('c:shotConversion','Shot conversion %','attacking'),('c:goalMinusXg','Goals minus xG','attacking')]
EVKEYS=[
 ('passes','Pass attempts'),('completed_passes','Completed passes'),('crosses','Crosses attempted'),
 ('shots','Shots (events)'),('header_shots','Header shots'),('shots_on_target','Shots on target (events)'),
 ('blocked_shots','Blocked shots (events)'),('recoveries','Recoveries'),('interceptions','Interceptions'),
 ('tackles','Tackles (events)'),('forward_passes','Forward passes (raw coordinate direction)')
]
CAT={
 'attacking':set('goals assists total_shots xg xa xgot shots_on_target big_chances_missed touches_opposition_box touches chances_created expected_goals expected_assists expected_goal_involvements goals_scored threat creativity influence ict_index set_piece_threat offsides'.split()),
 'passing':set('accurate_passes accurate_passes_percent final_third_passes accurate_crosses accurate_crosses_percent accurate_long_balls accurate_long_balls_percent corners'.split()),
 'defending':set('tackles tackles_won tackles_won_percent interceptions recoveries blocks clearances headed_clearances dribbled_past duels_won duels_lost ground_duels_won ground_duels_won_percent aerial_duels_won aerial_duels_won_percent defensive_contributions defensive_contribution clearances_blocks_interceptions'.split()),
 'goalkeeping':set('saves goals_conceded team_goals_conceded xgot_faced goals_prevented sweeper_actions gk_accurate_passes gk_accurate_long_balls high_claim saves_inside_box penalties_saved expected_goals_conceded'.split()),
 'physical':set('top_speed distance_covered walking_distance running_distance sprinting_distance number_of_sprints minutes minutes_played starts starts_per_90'.split()),
 'fpl':set('total_points event_points points_per_game bonus bps form dreamteam_count ep_next ep_this value_form value_season selected_by_percent now_cost cost_change_event cost_change_start transfers_in transfers_in_event transfers_out transfers_out_event'.split()),
 'discipline':set('yellow_cards red_cards own_goals penalties_missed penalties_scored fouls_committed'.split())
}
NON_AGGREGATE={'start_min','finish_min'}
MEAN_RATE_FIELDS={
 'accurate_passes_percent','accurate_crosses_percent','accurate_long_balls_percent',
 'ground_duels_won_percent','aerial_duels_won_percent','successful_dribbles_percent','tackles_won_percent'
}
MAX_FIELDS={'top_speed'}
# Sparse player-match tables use blanks for many true-zero action counts. Only fields
# in this explicit allow-list become zero when the player actually played minutes.
ZERO_WHEN_PLAYED=set('''goals assists total_shots xg xa shots_on_target successful_dribbles big_chances_missed
 touches_opposition_box touches accurate_passes chances_created final_third_passes accurate_crosses
 accurate_long_balls tackles_won interceptions recoveries blocks clearances headed_clearances dribbled_past
 duels_won duels_lost ground_duels_won aerial_duels_won was_fouled fouls_committed saves goals_conceded
 xgot_faced goals_prevented sweeper_actions gk_accurate_passes gk_accurate_long_balls dispossessed high_claim
 corners saves_inside_box offsides xgot tackles team_goals_conceded penalties_scored penalties_missed
 defensive_contributions'''.split())

def n(v,default=0):
 try:return round(float(v),5)
 except:return default

def ni(v):
 try:return int(float(v))
 except:return 0

def clean(v):
 if v in (None,''):return None
 try:return n(v)
 except:return str(v)

def deaccent(v):
 return ''.join(c for c in unicodedata.normalize('NFKD',str(v or '').lower()) if not unicodedata.combining(c))

def tokens(v):return re.findall(r'[a-z0-9]+',deaccent(v).replace("'",''))
def norm(v):return ''.join(tokens(v))

def cat(k):
 if k.endswith(('_rank','_rank_type')) or k.startswith('chance_of_playing'):return 'rankings'
 return next((c for c,items in CAT.items() if k in items),'other')

def label(k):
 return {'xg':'xG','xa':'xA','xgot':'xGOT','bps':'BPS','ict_index':'ICT Index','form':'Form (FPL)','now_cost':'Price (£m)','expected_goals':'Expected Goals','expected_assists':'Expected Assists'}.get(k,k.replace('_',' ').title().replace(' Per 90',' /90'))

def read(z,path):
 try:return list(csv.DictReader(io.StringIO(z.read(path).decode('utf-8-sig',errors='replace'))))
 except KeyError:return []

def inspect_zip(zipobj):
 """Map logical GW/table names and reject conflicting duplicates."""
 found=collections.defaultdict(list)
 for name in zipobj.namelist():
  if not name.lower().endswith('.csv'):continue
  m=re.search(r'(^|/)GW(\d+)/([^/]+)\.csv$',name,re.I)
  if m:found[(int(m.group(2)),m.group(3).lower())].append(name)
 out={};identical_duplicates=0
 for key,names in found.items():
  if len(names)==1:out[key]=names[0];continue
  blobs=[zipobj.read(x) for x in names]
  hashes={hashlib.sha256(b).hexdigest() for b in blobs}
  if len(hashes)>1:
   raise ValueError(f'Conflicting duplicate source files for GW{key[0]}/{key[1]}: '+', '.join(names))
  identical_duplicates+=len(names)-1
  out[key]=min(names,key=lambda x:(x.count('/'),len(x),x))
 return out,identical_duplicates

def finished_fixture(r):
 finished=str(r.get('finished','')).strip().lower()
 if finished in {'true','1','yes'}:return True
 return str(r.get('home_score','')).strip()!='' and str(r.get('away_score','')).strip()!=''

def build(pf,ef,dst):
 with zipfile.ZipFile(pf) as pzip,zipfile.ZipFile(ef) as ezip:
  pnames,duplicate_sources=inspect_zip(pzip)
  allgw=sorted({gw for gw,_ in pnames})
  gws=[]
  for gw in allgw:
   fr=read(pzip,pnames[(gw,'fixtures')]) if (gw,'fixtures') in pnames else []
   lr=read(pzip,pnames[(gw,'player_gameweek_stats')]) if (gw,'player_gameweek_stats') in pnames else []
   final=[r for r in fr if finished_fixture(r)]
   # Partial gameweeks are valid: index every completed match that has player logs.
   if final and lr:gws.append(gw)
  if not gws:raise ValueError('No completed fixtures with player logs were found.')
  latest=gws[-1]
  def rows(gw,kind):return read(pzip,pnames[(gw,kind)]) if (gw,kind) in pnames else []

  rawteams=rows(latest,'teams');rawstats=rows(latest,'playerstats');rawmatch=rows(latest,'playermatchstats')
  if not rawteams or not rawstats:raise ValueError('Missing team/playerstats tables in newest indexed GW.')
  teams=[{'id':str(t['id']),'code':str(t['code']),'name':t['name'],'short':t['short_name']} for t in rawteams]
  bycode={str(t['code']):t for t in teams};byname={t['name']:t for t in teams}

  # Full fixture schedule is independent of completed/indexed gameweeks.
  schedule=[]
  for gw in allgw:
   for rr in rows(gw,'fixtures'):
    h=bycode.get(str(ni(rr.get('home_team'))));a=bycode.get(str(ni(rr.get('away_team'))))
    if not h or not a:continue
    schedule.append({'id':rr.get('match_id',''),'gw':gw,'home':h['id'],'away':a['id'],'date':rr.get('kickoff_time',''),
                     'finished':finished_fixture(rr),'homeScore':ni(rr.get('home_score')) if str(rr.get('home_score','')).strip() else None,
                     'awayScore':ni(rr.get('away_score')) if str(rr.get('away_score','')).strip() else None})

  # Build the player directory from all indexed GWs, not only the latest file.
  directory={};player_history=collections.defaultdict(lambda:collections.defaultdict(list));player_team_history=collections.defaultdict(dict)
  for gw in gws:
   for p in rows(gw,'players'):
    t=bycode.get(str(p.get('team_code','')))
    if not t:continue
    pid=str(p.get('player_id',''))
    item={'id':pid,'code':str(p.get('player_code') or ''),'first':p.get('first_name',''),'last':p.get('second_name',''),'name':p.get('web_name',''),'team':t['id'],'position':p.get('position','')}
    directory[pid]=item
    player_history[gw][t['id']].append(item)
    player_team_history[pid][str(gw)]=t['id']
  players={pid:dict(item) for pid,item in directory.items()}
  for p in rawstats:
   tgt=players.get(str(p.get('id')))
   if tgt:tgt.update(price=n(p.get('now_cost')),total=n(p.get('total_points')),selected=n(p.get('selected_by_percent')),form=n(p.get('form')))

  fixtures=[];logs=[];shots=[];snap=collections.defaultdict(dict);pm=collections.defaultdict(dict);raw_match_presence=collections.Counter()
  ffields=[k for k in rawstats[0] if k not in {'id','player_id','match_id','first_name','second_name','web_name','news','news_added','status','corners_and_indirect_freekicks_text','direct_freekicks_text','penalties_text'}]
  mfields=[k for k in (rawmatch[0].keys() if rawmatch else []) if k not in {'player_id','match_id'}]
  for gw in gws:
   for rr in rows(gw,'fixtures'):
    if not finished_fixture(rr):continue
    h=bycode.get(str(ni(rr['home_team'])));a=bycode.get(str(ni(rr['away_team'])))
    if not h or not a:raise ValueError('Unrecognised club code in fixtures.')
    fixtures.append({'id':rr['match_id'],'gw':gw,'home':h['id'],'away':a['id'],'homeScore':ni(rr['home_score']),'awayScore':ni(rr['away_score']),'date':rr.get('kickoff_time',''),'xgHome':n(rr.get('home_expected_goals_xg')),'xgAway':n(rr.get('away_expected_goals_xg')),'shotsHome':ni(rr.get('home_total_shots')),'shotsAway':ni(rr.get('away_total_shots'))})
   for rr in rows(gw,'player_gameweek_stats'):
    pid=str(rr.get('id'))
    if pid in players:logs.append({'id':pid,'gw':gw,'points':n(rr.get('total_points')),'minutes':n(rr.get('minutes')),'goals':n(rr.get('goals_scored')),'assists':n(rr.get('assists')),'xg':n(rr.get('expected_goals')),'xa':n(rr.get('expected_assists')),'bonus':n(rr.get('bonus')),'def':n(rr.get('defensive_contribution')),'tackles':n(rr.get('tackles')),'recoveries':n(rr.get('recoveries'))})
   for rr in rows(gw,'shots'):
    shots.append({'match':rr.get('match_id'),'gw':gw,'minute':ni(rr.get('minute')),'player':rr.get('player_name',''),'xg':n(rr.get('xg')),'xgot':n(rr.get('xgot')),'outcome':rr.get('outcome',''),'x':n(rr.get('start_x')),'y':n(rr.get('start_y'))})
   for rr in rows(gw,'playerstats'):
    pid=str(rr.get('id'))
    if pid in players:snap[pid][str(gw)]={k:clean(rr.get(k)) for k in ffields if rr.get(k) not in (None,'')}
   for rr in rows(gw,'playermatchstats'):
    pid=str(rr.get('player_id'))
    if pid not in players:continue
    row=pm[pid].setdefault(str(gw),{});avg=row.setdefault('_avg',{});mx=row.setdefault('_max',{})
    mins=n(rr.get('minutes_played'),0)
    for k in mfields:
     if k in NON_AGGREGATE:continue
     raw=rr.get(k)
     if raw not in (None,''):raw_match_presence[k]+=1
     v=clean(raw)
     if v is None and mins>0 and k in ZERO_WHEN_PLAYED:v=0
     if not isinstance(v,(int,float)):continue
     if k in MEAN_RATE_FIELDS:avg.setdefault(k,[]).append(v)
     elif k in MAX_FIELDS:mx[k]=max(mx.get(k,float('-inf')),v)
     else:row[k]=round(row.get(k,0)+v,5)
  for d in pm.values():
   for row in d.values():
    for k,arr in row.pop('_avg',{}).items():
     row[k]=round(sum(arr)/len(arr),5);row['__n_'+k]=len(arr)
    for k,v in row.pop('_max',{}).items():
     if v!=float('-inf'):row[k]=round(v,5)

  def field_coverage(container,field):
   total=hit=0
   for per_player in container.values():
    for r in per_player.values():
     total+=1
     if isinstance(r.get(field),(int,float)):hit+=1
   return hit,total

  # Hide all-null/non-aggregate metrics and attach coverage + explicit aggregation semantics.
  active_f=[];excluded_metrics=[]
  for k in ffields:
   hit,total=field_coverage(snap,k)
   if hit:active_f.append((k,hit,total))
   else:excluded_metrics.append('f:'+k)
  active_m=[]
  for k in mfields:
   if k in NON_AGGREGATE or raw_match_presence.get(k,0)==0:
    excluded_metrics.append('m:'+k);continue
   hit,total=field_coverage(pm,k)
   if hit:active_m.append((k,hit,total))
   else:excluded_metrics.append('m:'+k)

  MET=[]
  for k,hit,total in active_f:
   lab=label(k)
   if k=='assists':lab='FPL assists'
   elif k=='goals_scored':lab='FPL goals'
   elif k=='expected_goals':lab='FPL expected goals (season)'
   elif k=='expected_assists':lab='FPL expected assists (season)'
   MET.append(dict(key='f:'+k,label=lab,field=k,category=cat(k),source='FPL snapshot',mode='snapshot',aggregation='as_of_latest_selected_gw',kind='raw',coverage=round(100*hit/max(1,total),2),help='Latest available FPL snapshot in selected gameweeks. Season-cumulative fields are as-of values and are not restricted to only the selected weeks.'))
  for k,hit,total in active_m:
   mode='average_match' if k in MEAN_RATE_FIELDS else 'max' if k in MAX_FIELDS else 'sum'
   lab=label(k)
   if k=='assists':lab='Match assists'
   elif k=='goals':lab='Match goals'
   elif k=='xg':lab='Match xG'
   elif k=='xa':lab='Match xA'
   help_text='Based on match-level records within selected gameweeks.'
   if k in MEAN_RATE_FIELDS:help_text+=' This is the mean of available match-level percentages, not a reconstructed season-wide weighted percentage.'
   elif k in MAX_FIELDS:help_text+=' The maximum observed match value is used across the selected period.'
   MET.append(dict(key='m:'+k,label=lab,field=k,category=cat(k),source='Player match stats',mode=mode,aggregation=mode,kind='raw',coverage=round(100*hit/max(1,total),2),help=help_text))
  for k,l,c in CALC:MET.append(dict(key=k,label=l,field=k[2:],category=c,source='Calculated / selected weeks',mode='calculated',aggregation='calculated',kind='calculated',coverage=100,help='Derived from available week-level records.'))
  for k,l in EVKEYS:MET.append(dict(key='ev:'+k,label=l,field=k,category='events',source='Player-linked match events',mode='sum',aggregation='sum',kind='event-derived',coverage=None,help='Only events with confidently cross-walked provider player IDs; unmatched events are excluded.'))

  keyfixture={(f['gw'],f['home'],f['away']):f['id'] for f in fixtures};idx={f['id']:i for i,f in enumerate(fixtures)}

  def candidate_score(p,event_name,team_pool):
   et=tokens(event_name);en=norm(event_name)
   if not et or not en:return 0
   ft=tokens(p.get('first',''));lt=tokens(p.get('last',''));wt=tokens(p.get('name',''))
   fn=''.join(ft);ln=''.join(lt);wn=''.join(wt);full=fn+ln
   if en==full:return 100
   if en==wn:return 99
   if en==ln and sum(norm(x.get('last',''))==en for x in team_pool)==1:return 97
   if en==fn and sum(norm(x.get('first',''))==en for x in team_pool)==1:return 94
   if len(et)>=2:
    first=et[0];surname=''.join(et[1:]);all_initials={x[0] for x in ft+lt if x};first_initials={x[0] for x in ft if x}
    if len(first)==1:
     if first in first_initials and surname==ln:return 98
     if first in first_initials and (ln.startswith(surname) or ln.endswith(surname)):return 95
     if first in first_initials and surname==wn:return 97
     if first in all_initials and surname==wn:return 92
    else:
     firstn=norm(first)
     if ft and firstn==ft[0] and (surname==ln or ln.startswith(surname) or ln.endswith(surname) or surname.startswith(ln) or surname.endswith(ln)):return 98
     if firstn==fn and (surname==ln or ln.startswith(surname) or ln.endswith(surname) or surname.startswith(ln) or surname.endswith(ln)):return 98
     if surname==wn and sum(norm(x.get('name',''))==wn for x in team_pool)==1:return 91
   if len(et)==1:
    hits=[x for x in team_pool if en in {norm(x.get('first','')),norm(x.get('last','')),norm(x.get('name',''))}]
    if len(hits)==1 and hits[0]['id']==p['id']:return 93
   return 0

  link_cache={}
  def link_row(gw,team,name):
   cache_key=(gw,team,name)
   if cache_key in link_cache:return link_cache[cache_key]
   pool=player_history.get(gw,{}).get(team,[])
   if not pool:link_cache[cache_key]=(None,0);return link_cache[cache_key]
   scored=sorted(((candidate_score(p,name,pool),p['id']) for p in pool),reverse=True);scored=[x for x in scored if x[0]>0]
   if not scored:link_cache[cache_key]=(None,0);return link_cache[cache_key]
   if len(scored)>1 and scored[1][0]==scored[0][0]:link_cache[cache_key]=(None,0);return link_cache[cache_key]
   link_cache[cache_key]=(scored[0][1],scored[0][0]);return link_cache[cache_key]

  prepared=[];errors=set();matched_fixtures=set();source_supported=0;source_rows=0;bad_coords=0;max_minute=0
  votes=collections.defaultdict(lambda:collections.Counter());ext_names=collections.defaultdict(collections.Counter)
  for path in ezip.namelist():
   if not re.search(r'Gameweek_\d+/[^/]+\.csv$',path,re.I):continue
   for rr in read(ezip,path):
    source_rows+=1
    typ=ni(rr.get('type_id'))
    if typ not in KIND:continue
    gw=ni(rr.get('gameweek'))
    if gw not in gws:continue
    source_supported+=1
    names=[ALIAS.get(rr.get(key,''),rr.get(key,'')) for key in ('home_team','away_team','team_name')]
    if not all(x in byname for x in names):errors.add('Unmatched club in '+path);continue
    h,a,t=[byname[x]['id'] for x in names];fid=keyfixture.get((gw,h,a))
    if not fid:errors.add('No match for '+path);continue
    xy=[clean(rr.get(k)) for k in ('x','y','end_x','end_y')]
    if any(not isinstance(q,(int,float)) or not 0<=q<=100 for q in xy):bad_coords+=1;continue
    try:flags=json.loads(rr.get('qualifier_json') or '{}')
    except:flags={}
    if not isinstance(flags,dict):flags={}
    flags={str(k):v for k,v in flags.items()}
    if typ==16 and '28' in flags:k='own_goal'
    elif typ==1 and '2' in flags:k='cross'
    else:k=KIND[typ]
    ext=str(rr.get('player_id') or '').strip();name=rr.get('player_name','')
    if ext:
     ext_names[ext][name]+=1;pid,score=link_row(gw,t,name)
     if pid:votes[ext][pid]+=max(1,score)
    prepared.append((rr,gw,h,a,t,fid,xy,flags,k,typ,ext,name));matched_fixtures.add(fid);max_minute=max(max_minute,ni(rr.get('minute')))

  if errors:raise ValueError('; '.join(sorted(errors)[:3]))
  if len(matched_fixtures)!=len(fixtures):raise ValueError(f'Only {len(matched_fixtures)} of {len(fixtures)} completed fixtures linked to event archive')

  extmap={};ambiguous_ext=set()
  for ext,counter in votes.items():
   ranked=counter.most_common()
   if not ranked:continue
   top_pid,top_score=ranked[0];second=ranked[1][1] if len(ranked)>1 else 0
   if second and top_score < second*1.35:ambiguous_ext.add(ext);continue
   extmap[ext]=top_pid

  events=[];ec=collections.Counter();ep=collections.defaultdict(dict);seen=set();own_goal_rows=0
  qteam=collections.defaultdict(lambda:{'total':0,'linked':0});qgw=collections.defaultdict(lambda:{'total':0,'linked':0});unmatched_names=collections.Counter()
  linked_event_rows=0;unlinked_event_rows=0
  for rr,gw,h,a,t,fid,xy,flags,k,typ,ext,name in prepared:
   eid=(fid,rr.get('event_id'))
   if eid in seen:continue
   seen.add(eid);person=extmap.get(ext) if ext else None
   if not person and not ext:
    fallback,score=link_row(gw,t,name)
    if score>=96:person=fallback
   qteam[str(t)]['total']+=1;qgw[str(gw)]['total']+=1
   if person:linked_event_rows+=1;qteam[str(t)]['linked']+=1;qgw[str(gw)]['linked']+=1
   else:
    unlinked_event_rows+=1
    if name:unmatched_names[name]+=1
   # 0:gw 1:team 2:type 3:x 4:y 5:ex 6:ey 7:min 8:success 9:name 10:matchIndex
   # 11:seconds 12:period 13:qualifiers 14:source type 15:linked FPL player ID
   row=[gw,t,k,*xy,ni(rr.get('minute')),ni(rr.get('outcome')),name,idx[fid],ni(rr.get('second')),ni(rr.get('period_id')),list(flags.keys()),typ,person or '']
   events.append(row);ec[k]+=1
   if k=='own_goal':own_goal_rows+=1
   if person:
    rec=ep[person].setdefault(str(gw),{})
    def add(field):rec[field]=rec.get(field,0)+1
    if k=='pass':
     add('passes')
     if ni(rr.get('outcome'))==1:add('completed_passes')
     if xy[2]>xy[0]+5:add('forward_passes')
    if k=='cross':add('crosses')
    if k=='shot':
     add('shots')
     if '15' in flags:add('header_shots')
     if typ==15 and '82' in flags:add('blocked_shots')
     if typ==16 or (typ==15 and '82' not in flags):add('shots_on_target')
    if k=='recovery':add('recoveries')
    if k=='interception':add('interceptions')
    if k=='tackle':add('tackles')

  if len(events)<1000:raise ValueError('Too few events; check archive structure')
  quality={
   'eventLinkage':{
    'sourceRows':source_rows,'supportedSourceRows':source_supported,'ignoredUnsupportedRows':max(0,source_rows-source_supported),
    'validCoordinateEvents':len(events),'discardedBadCoordinates':bad_coords,'ownGoalEventsSeparated':own_goal_rows,
    'linkedEvents':linked_event_rows,'unlinkedEvents':unlinked_event_rows,
    'linkedEventPct':round(linked_event_rows/max(1,linked_event_rows+unlinked_event_rows)*100,2),
    'externalPlayerIds':len(ext_names),'mappedExternalPlayerIds':len(extmap),'ambiguousExternalPlayerIds':len(ambiguous_ext),
    'mappedFplPlayerIds':len(set(extmap.values())),
    'method':'Provider player_id crosswalk + gameweek club history + conservative name verification',
    'byTeam':dict(qteam),'byGameweek':dict(qgw),'unmatchedNameSamples':unmatched_names.most_common(20)
   },
   'source':{
    'identicalDuplicateLogicalCsvs':duplicate_sources,'fullScheduleFixtures':len(schedule),
    'indexedCompletedFixtures':len(fixtures),'latestIndexedGameweek':latest,
    'maxIndexedEventMinute':max_minute,'excludedAllNullMetrics':excluded_metrics
   },
   'notes':['Own goals are stored separately and excluded from attacking shot totals.','Crosses are not counted as passes.','Type 61 is labelled bad_touch; it is not a total-touch measure.','Attack-direction normalization remains unverified.','Ambiguous provider player IDs are intentionally left unmatched.']
  }
  base={'season':'2026/27','teams':teams,'players':list(players.values()),'playerTeamHistory':dict(player_team_history),'fixtures':fixtures,'schedule':schedule,'logs':logs,'shots':shots,'photoData':{},'logoData':{},'metrics':MET,'snapshots':snap,'playerMatch':pm,'eventPlayer':ep,'events':events,'eventCounts':ec,'gws':gws,'quality':quality}
  dst=Path(dst);dst.parent.mkdir(parents=True,exist_ok=True)
  dst.write_text('window.FPL_V2='+json.dumps(base,separators=(',',':'),ensure_ascii=False)+';')
  return {'gameweeks':gws,'fixtures':len(fixtures),'schedule_fixtures':len(schedule),'players':len(players),'events':len(events),'source_event_rows':source_rows,'player_logs':len(logs),'metrics':len(MET),'mapped_external_player_ids':len(extmap),'mapped_fpl_player_ids':len(set(extmap.values())),'linked_event_pct':quality['eventLinkage']['linkedEventPct'],'updated':datetime.now(timezone.utc).isoformat()}

if __name__=='__main__':
 if len(sys.argv)!=4:sys.exit('Usage: python tools/rebuild.py <performance.zip> <events.zip> <output-data.js>')
 print(json.dumps(build(*sys.argv[1:]),indent=2))
