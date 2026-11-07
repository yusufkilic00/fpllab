#!/usr/bin/env bash
set -e
python3 tools/build_cloudflare.py
python3 tools/qa_cloudflare.py
echo "Cloudflare bundle verified in dist/"
