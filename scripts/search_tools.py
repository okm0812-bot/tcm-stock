# -*- coding: utf-8 -*-
import sys, json, urllib.request, os
sys.stdout.reconfigure(encoding='utf-8')

port = os.environ.get('AUTH_GATEWAY_PORT', '19000')

queries = [
    'best AI tools retail investor stock analysis 2026',
    'quantitative investment tools individual investor ETF',
    'Taiwan stock analysis software tool recommendation'
]

for q in queries:
    try:
        data = json.dumps({'q': q, 'num': 3}).encode()
        req = urllib.request.Request(
            f'http://localhost:{port}/proxy/prosearch/search',
            data=data,
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            result = json.loads(r.read())
            print(f'=== {q} ===')
            print(json.dumps(result, ensure_ascii=False, indent=2)[:500])
            print()
    except Exception as e:
        print(f'搜尋失敗: {type(e).__name__}: {e}')
