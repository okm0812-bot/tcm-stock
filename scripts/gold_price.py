# -*- coding: utf-8 -*-
"""
黃金價格 — SPDR黃金ETF (GLD)
"""
import sys
import yfinance as yf

print("[Gold Price Test]")

try:
    gld = yf.Ticker("GLD")
    hist = gld.history(period="5d")
    
    if hist is not None and not hist.empty:
        price = float(hist['Close'].iloc[-1])
        prev = float(hist['Close'].iloc[-2]) if len(hist) > 1 else price
        change = price - prev
        pct = (change / prev) * 100 if prev else 0
        
        print(f"\n[GLD] SPDR Gold ETF")
        print(f"  Price: ${price:.2f}")
        print(f"  Change: ${change:+.2f} ({pct:+.2f}%)")
        
        if pct > 1:
            print("  Sentiment: Risk-Off (避險需求上升)")
        elif pct < -1:
            print("  Sentiment: Risk-On (風險偏好上升)")
        else:
            print("  Sentiment: Neutral (中性)")
    else:
        print("[Error] No data")
except Exception as e:
    print(f"[Error] {e}")
