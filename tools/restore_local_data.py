#!/usr/bin/env python3
import json
from pathlib import Path
from webdata import compact_json, reconstruct_web_data
ROOT=Path(__file__).resolve().parents[1]
data,manifest=reconstruct_web_data(ROOT/'web_data')
(ROOT/'data.js').write_bytes(b'window.FPL_V2='+compact_json(data)+b';')
print(json.dumps({'ok':True,'restored':'data.js','build':manifest['build'],'events':len(data['events'])},indent=2))
