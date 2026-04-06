#!/usr/bin/env python3
import json, urllib.request, ssl, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 今日是 2026-03-25，抓三大法人
url = "https://www.twse.com.tw/fund/T86?response=json&date=20260325&selectType=ALLBUT0999"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15, context=ctx) as r:
        data = json.loads(r.read().decode('utf-8'))
        if data.get('stat') == 'OK':
            print(f"=== 三大法人 {data.get('date')} ===")
            targets = ['1101','2352','2409','3311','6919','00687B','00795B','0050','0052']
            for row in data.get('data',[]):
                if row[0] in targets:
                    f = int(row[4].replace(',',''))
                    t = int(row[10].replace(',',''))
                    tot = int(row[18].replace(',',''))
                    print(f"{row[1].strip()} {row[0]}: 外資{f:+,.0f} 投信{t:+,.0f} 合計{tot:+,.0f}")
        else:
            print(f"法人無資料: {data.get('stat')}")
except Exception as e:
    print(f"法人錯誤: {e}")

print()

# 個股報價
stocks = [('1101','台泥'),('2352','佳世達'),('2409','友達'),('3311','閎暉'),('6919','康霈')]
for sid, name in stocks:
    try:
        url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{sid}.tw"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as r:
            d = json.loads(r.read().decode('utf-8'))['msgArray'][0]
            p = float(d.get('z', d.get('y','0')).replace(',',''))
            y = float(d.get('y','0').replace(',',''))
            chg = round((p-y)/y*100,2) if y>0 else 0
            print(f"{name} {sid}: {p:.2f} ({chg:+.2f}%)")
    except Exception as e:
        print(f"{name}: 錯誤")
