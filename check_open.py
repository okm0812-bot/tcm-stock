# -*- coding: utf-8 -*-
import yfinance as yf
import sys
sys.stdout.reconfigure(encoding="utf-8")

print("=" * 60)
print("台股開盤初期數據（09:00）")
print("=" * 60)

# 嘗試抓取即時數據
tickers = {
    "^TWII": "台股加權",
    "1101.TW": "台泥",
    "2352.TW": "佳世達",
    "2409.TW": "友達",
    "6919.TW": "康霈",
    "0050.TW": "0050"
}

for code, name in tickers.items():
    try:
        t = yf.Ticker(code)
        info = t.info
        price = info.get("regularMarketPrice", 0) or 0
        prev = info.get("regularMarketPreviousClose", 0) or 0
        open_p = info.get("regularMarketOpen", 0) or 0
        if price > 0:
            chg = (price - prev) / prev * 100 if prev > 0 else 0
            print(f"{name}: 開盤 {open_p:.2f} / 現價 {price:.2f} ({chg:+.2f}%)")
        else:
            print(f"{name}: 無即時數據 (可能15分鐘延遲)")
    except Exception as e:
        print(f"{name}: 錯誤 - {e}")

print()
print("注意：Yahoo Finance有15分鐘延遲")
print("開盤後要等到09:15才有第一筆更新")
