# -*- coding: utf-8 -*-
"""
階段 1: 抓取所有需要的歷史數據
"""
import yfinance as yf
import json
from datetime import datetime, timezone, timedelta

tz8 = timezone(timedelta(hours=8))

print("=== 階段 1: 抓取歷史數據 ===")

tickers = {
    '^TWII':    '台股加權',
    '0050.TW':  '元大台灣50',
    '00878.TW': '國泰高股息',
    '00919.TW': '群益高息',
    'VOO':      'Vanguard S&P500',
    '1101.TW':  '台泥',
    '2352.TW':  '佳世達',
    '2409.TW':  '友達',
    '6919.TW':  '康霈',
    '^GSPC':    'S&P500',
    '^VIX':     'VIX',
    '^TNX':     '美10年債',
}

data = {}
for code, name in tickers.items():
    try:
        t = yf.Ticker(code)
        # 抓 3 年歷史
        hist = t.history(period='3y')
        info = t.info
        data[code] = {
            'name': name,
            'price': info.get('regularMarketPrice', 0),
            'prev': info.get('regularMarketPreviousClose', 0),
            'h52': info.get('fiftyTwoWeekHigh', 0),
            'l52': info.get('fiftyTwoWeekLow', 0),
            'hist_len': len(hist),
            'hist_close': hist['Close'].tolist()[-252:],  # 最近一年
            'hist_dates': [str(d.date()) for d in hist.index.tolist()[-252:]],
        }
        print(f"  OK: {name} ({code}) - {len(hist)} 天歷史")
    except Exception as e:
        print(f"  FAIL: {name} ({code}) - {e}")
        data[code] = {'name': name, 'error': str(e)}

with open('market_data_raw.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n完成！已儲存 market_data_raw.json")
print(f"成功: {sum(1 for v in data.values() if 'error' not in v)} / {len(tickers)}")
