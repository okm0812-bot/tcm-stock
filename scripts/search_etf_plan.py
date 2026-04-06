# -*- coding: utf-8 -*-
import requests, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

PORT = os.environ.get('AUTH_GATEWAY_PORT', '19000')
url = f'http://localhost:{PORT}/proxy/prosearch/search'

queries = [
    ('台股 2026 高點 風險 回調 展望', '台股展望'),
    ('美國關稅 2026 台灣 科技股 影響', '關稅影響'),
    ('0050 ETF 現在買 時機 2026', '0050買點'),
    ('00878 00919 高股息ETF 比較 2026', '高股息ETF'),
    ('VOO VT 美股ETF 台灣人 投資 2026', '美股ETF'),
    ('台股 換股 策略 停損 ETF 2026', '換股策略'),
]

results = {}
for keyword, label in queries:
    try:
        r = requests.post(url, json={'keyword': keyword}, timeout=15)
        data = r.json()
        results[label] = data.get('message', '') if data.get('success') else f"搜尋失敗: {data.get('message','')}"
    except Exception as e:
        results[label] = f"錯誤: {e}"

with open('search_results_etf.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

for label, msg in results.items():
    print(f"\n{'='*50}")
    print(f"【{label}】")
    print(msg[:800])
