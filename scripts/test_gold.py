# -*- coding: utf-8 -*-
"""
黃金價格 — 直接用 yfinance 測試
"""
import yfinance as yf

print("\n=== Gold Price Test ===\n")

# 測試多種代碼
codes = ['GLD', 'IAU', 'GC=F', 'XAUUSD', '^XAU']

for code in codes:
    try:
        t = yf.Ticker(code)
        h = t.history(period="5d")
        if not h.empty:
            print(f"SUCCESS: {code}")
            print(f"  Close: {h['Close'].iloc[-1]}")
            break
        else:
            print(f"EMPTY: {code}")
    except Exception as e:
        print(f"ERROR {code}: {e}")
