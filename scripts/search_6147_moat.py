# -*- coding: utf-8 -*-
import requests
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

PORT = os.environ.get('AUTH_GATEWAY_PORT', '19000')
url = f'http://localhost:{PORT}/proxy/prosearch/search'

data = {
    'keyword': '頎邦 6147 護城河 競爭優勢 LCD驅動IC 封裝',
    'cnt': 10
}

try:
    response = requests.post(url, json=data, timeout=15)
    result = response.json()
    
    if result.get('success'):
        print("SUCCESS")
        print(result.get('message', ''))
    else:
        print(f"FAIL: {result.get('message', '未知錯誤')}")
except Exception as e:
    print(f"ERROR: {e}")