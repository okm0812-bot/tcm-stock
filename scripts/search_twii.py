# -*- coding: utf-8 -*-
import requests
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

PORT = os.environ.get('AUTH_GATEWAY_PORT', '19000')
url = f'http://localhost:{PORT}/proxy/prosearch/search'

queries = [
    '台股 加權指數 2026 展望 回調',
    '美國關稅 台灣 股市 影響 2026',
]

for q in queries:
    data = {'keyword': q, 'cnt': 5}
    try:
        r = requests.post(url, json=data, timeout=15)
        result = r.json()
        if result.get('success'):
            print(f"\n=== {q} ===")
            print(result.get('message', ''))
    except Exception as e:
        print(f"ERROR: {e}")
