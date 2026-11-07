#!/usr/bin/env python3
import json
from pathlib import Path
from webdata import load_data_js, reconstruct_web_data
ROOT=Path(__file__).resolve().parents[1]
web,manifest=reconstruct_web_data(ROOT/'web_data')
result={'ok':True,'build':manifest['build'],'events':len(web['events']),'gameweeks':web['gws']}
if (ROOT/'data.js').exists():
 src=load_data_js(ROOT/'data.js'); failed=[k for k in src if src.get(k)!=web.get(k)]
 if failed: raise SystemExit('web_data mismatch: '+', '.join(failed))
 result['source_match']=True;result['checked_keys']=len(src)
print(json.dumps(result,indent=2))
