# -*- coding: utf-8 -*-
import yfinance as yf
from datetime import datetime

t = yf.Ticker('^TWII')
i = t.info

price = i.get('regularMarketPrice', 0)
prev = i.get('regularMarketPreviousClose', 0)
high52 = i.get('fiftyTwoWeekHigh', 0)
low52 = i.get('fiftyTwoWeekLow', 0)
mkt_time = i.get('regularMarketTime', 0)

from datetime import timezone, timedelta
tz = timezone(timedelta(hours=8))
if mkt_time:
    dt = datetime.fromtimestamp(mkt_time, tz=tz)
    time_str = dt.strftime('%Y-%m-%d %H:%M:%S')
else:
    time_str = 'N/A'

print(f"台股加權指數 ^TWII")
print(f"現價:     {price:,.0f}")
print(f"昨收:     {prev:,.0f}")
print(f"漲跌:     {price-prev:+,.0f} ({(price-prev)/prev*100:+.2f}%)" if prev else "")
print(f"52週高:   {high52:,.0f}")
print(f"52週低:   {low52:,.0f}")
print(f"資料時間: {time_str}")
print(f"資料來源: Yahoo Finance (15分鐘延遲)")
