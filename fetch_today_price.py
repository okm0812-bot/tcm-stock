#!/usr/bin/env python3
import json
import urllib.request
import ssl
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

stocks = [
    ('1101', '台泥'),
    ('2352', '佳世達'),
    ('2409', '友達'),
    ('3311', '閎暉'),
    ('6919', '康霈'),
]

print("=" * 80)
print("今日即時股價 - 2026-03-24 08:46")
print("=" * 80)
print()

for stock_id, stock_name in stocks:
    try:
        url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stock_id}.tw"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('msgArray'):
                d = data['msgArray'][0]
                price = float(d.get('z', '0').replace(',', '')) if d.get('z') != '-' else 0
                yest = float(d.get('y', '0').replace(',', '')) if d.get('y') else 0
                open_p = float(d.get('o', '0').replace(',', '')) if d.get('o') else 0
                high = float(d.get('h', '0').replace(',', '')) if d.get('h') else 0
                low = float(d.get('l', '0').replace(',', '')) if d.get('l') else 0
                volume = int(d.get('v', '0').replace(',', '')) if d.get('v') else 0
                
                change = price - yest if yest > 0 else 0
                change_pct = (change / yest * 100) if yest > 0 else 0
                
                print(f"【{stock_name} {stock_id}】")
                print(f"  現價：{price:.2f} 元")
                print(f"  昨收：{yest:.2f} 元")
                print(f"  漲跌：{change:+.2f} 元（{change_pct:+.2f}%）")
                print(f"  開盤：{open_p:.2f} 元")
                print(f"  最高：{high:.2f} 元")
                print(f"  最低：{low:.2f} 元")
                print(f"  成交量：{volume:,} 張")
                print()
    except Exception as e:
        print(f"【{stock_name} {stock_id}】 - 錯誤：{e}")
        print()
