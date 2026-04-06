# -*- coding: utf-8 -*-
import yfinance as yf
s = yf.Ticker('2352.TW')
p = s.info.get('regularMarketPrice', 0)
print(f'現價: {p}')
