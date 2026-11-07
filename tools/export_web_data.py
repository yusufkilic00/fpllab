#!/usr/bin/env python3
import json, sys
from pathlib import Path
from webdata import export_web_data
ROOT=Path(__file__).resolve().parents[1]
src=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else ROOT/'data.js'
out=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else ROOT/'web_data'
manifest=export_web_data(src,out)
print(json.dumps({'ok':True,'build':manifest['build'],'gameweeks':[x['gw'] for x in manifest['gameweeks']],'totals':manifest['totals']},indent=2))
