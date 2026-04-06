# -*- coding: utf-8 -*-
"""確認債券ETF現價"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

try:
    import yfinance as yf
    import datetime

    codes = ["00687B.TW", "00795B.TW", "00751B.TW", "00853B.TW", "00933B.TW"]

    print("=" * 60)
    print("債券ETF 現價確認")
    print("=" * 60)

    for code in codes:
        try:
            t = yf.Ticker(code)
            hist = t.history(period="5d")
            if not hist.empty:
                last_close = hist['Close'].iloc[-1]
                last_date = hist.index[-1].strftime('%Y-%m-%d')
                prev_close = hist['Close'].iloc[-2] if len(hist) >= 2 else last_close
                change = last_close - prev_close
                change_pct = change / prev_close * 100
                print(f"\n{code}")
                print(f"  最新收盤：{last_close:.2f} 元（{last_date}）")
                print(f"  前日收盤：{prev_close:.2f} 元")
                print(f"  漲跌：{change:+.2f} 元（{change_pct:+.2f}%）")
            else:
                print(f"\n{code}: 無法取得歷史數據")
        except Exception as e:
            print(f"\n{code}: 錯誤 - {e}")

    print("\n" + "=" * 60)

except Exception as e:
    print(f"錯誤: {e}")
