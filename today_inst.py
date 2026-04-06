#!/usr/bin/env python3
import json, urllib.request, ssl, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 三大法人
url = "https://www.twse.com.tw/fund/T86?response=json&date=20260324&selectType=ALLBUT0999"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
        data = json.loads(r.read().decode('utf-8'))
        if data.get('stat') == 'OK':
            print(f"=== 三大法人 {data.get('date')} ===")
            targets = ['1101','2352','2409','3311','6919','00687B','00795B','0050','0052']
            for row in data.get('data',[]):
                if row[0] in targets:
                    print(f"{row[1].strip()} {row[0]}: 外資{int(row[4].replace(',','')):+,.0f} 投信{int(row[10].replace(',','')):+,.0f} 合計{int(row[18].replace(',','')):+,.0f}")
        else:
            print(f"無資料: {data.get('stat')}")
except Exception as e:
    print(f"錯誤: {e}")
