# -*- coding: utf-8 -*-
import requests
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

PORT = os.environ.get('AUTH_GATEWAY_PORT', '19000')
url = f'http://localhost:{PORT}/proxy/prosearch/search'

data = {
    'keyword': '6147.TWO 友銓電子 業務 產品',
    'cnt': 10
}

try:
    response = requests.post(url, json=data, timeout=15)
    result = response.json()
    
    with open('search_result_6147_name.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    if result.get('success'):
        print("SUCCESS")
        print(result.get('message', ''))
    else:
        print(f"FAIL: {result.get('message', '未知錯誤')}")
except Exception as e:
    print(f"ERROR: {e}")