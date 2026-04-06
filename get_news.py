# -*- coding: utf-8 -*-
import requests
import sys
sys.stdout.reconfigure(encoding="utf-8")

print("抓取台股大漲原因新聞...")
print()

headers = {"User-Agent": "Mozilla/5.0"}

# 嘗試多個新聞源
urls = [
    ("Yahoo新聞", "https://tw.news.yahoo.com/taiwan-stocks-surge-1451-095000023.html"),
    ("中央社", "https://www.cna.com.tw"),
    ("經濟日報", "https://money.udn.com"),
]

for name, url in urls:
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        print(f"=== {name} ===")
        print(f"Status: {resp.status_code}")
        print(f"URL: {resp.url}")
        print()
    except Exception as e:
        print(f"{name}: 無法取得 - {e}")
