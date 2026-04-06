#!/usr/bin/env python3
import json
import urllib.request
import ssl
from datetime import datetime

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 抓取今日三大法人資料
url = "https://www.twse.com.tw/fund/T86?response=json&date=20260324&selectType=ALLBUT0999"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
        data = json.loads(response.read().decode('utf-8'))
        
        if data.get('stat') == 'OK':
            print("=" * 80)
            print("今日三大法人買賣超資料 - 2026-03-24")
            print("=" * 80)
            print(f"資料日期：{data.get('date')}")
            print()
            
            # 查詢你的持股
            stocks = ['1101', '2352', '2409', '3311', '6919', '00687B', '00795B']
            
            for row in data.get('data', []):
                if row[0] in stocks:
                    stock_id = row[0]
                    stock_name = row[1].strip()
                    foreign_net = int(row[4].replace(',', ''))
                    trust_net = int(row[10].replace(',', ''))
                    total_net = int(row[18].replace(',', ''))
                    
                    print(f"【{stock_name} {stock_id}】")
                    print(f"  外資：{foreign_net:+,.0f} 張")
                    print(f"  投信：{trust_net:+,.0f} 張")
                    print(f"  合計：{total_net:+,.0f} 張")
                    print()
        else:
            print(f"無法取得資料：{data.get('stat')}")
except Exception as e:
    print(f"錯誤：{e}")
