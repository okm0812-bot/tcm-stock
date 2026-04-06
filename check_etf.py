#!/usr/bin/env python3
import json
import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.twse.com.tw/fund/T86?response=json&date=20260323&selectType=ALLBUT0999"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})

with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
    data = json.loads(response.read().decode('utf-8'))
    
    if data.get('stat') == 'OK':
        for row in data.get('data', []):
            if row[0] in ['0050', '0052']:
                print(f"{row[0]} {row[1].strip()}")
                print(f"  外資: {int(row[4].replace(',', '')):,.0f}")
                print(f"  投信: {int(row[10].replace(',', '')):,.0f}")
                print(f"  合計: {int(row[18].replace(',', '')):,.0f}")
                print()