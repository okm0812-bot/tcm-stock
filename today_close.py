#!/usr/bin/env python3
import json, urllib.request, ssl, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

stocks = [('1101','台泥'),('2352','佳世達'),('2409','友達'),('3311','閎暉'),('6919','康霈')]

print("=== 今日收盤價 2026-03-24 ===")
for stock_id, name in stocks:
    try:
        url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stock_id}.tw"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            d = json.loads(r.read().decode('utf-8'))['msgArray'][0]
            price = d.get('z','0') if d.get('z') != '-' else d.get('y','0')
            yest = d.get('y','0')
            vol = d.get('v','0')
            p = float(price.replace(',',''))
            y = float(yest.replace(',',''))
            chg = round((p-y)/y*100,2) if y>0 else 0
            print(f"{name} {stock_id}: {p:.2f} ({chg:+.2f}%) 量:{vol}張")
    except Exception as e:
        print(f"{name} {stock_id}: 錯誤 {e}")
