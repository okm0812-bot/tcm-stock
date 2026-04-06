import yfinance as yf
import numpy as np
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print('=' * 70)
print('台股趨勢分析 - 2026-03-31')
print('=' * 70)

twii = yf.Ticker('^TWII')
hist = twii.history(period='2y')

price_now = hist['Close'].iloc[-1]
price_1m  = hist['Close'].iloc[-22]
price_3m  = hist['Close'].iloc[-66]
price_6m  = hist['Close'].iloc[-132]
price_1y  = hist['Close'].iloc[-252]

print(f'台股加權指數現價: {price_now:.0f}')
print()
print('各時間段漲跌:')
print(f'  近1個月: {(price_now/price_1m-1)*100:+.1f}%  ({price_1m:.0f} -> {price_now:.0f})')
print(f'  近3個月: {(price_now/price_3m-1)*100:+.1f}%  ({price_3m:.0f} -> {price_now:.0f})')
print(f'  近6個月: {(price_now/price_6m-1)*100:+.1f}%  ({price_6m:.0f} -> {price_now:.0f})')
print(f'  近1年:   {(price_now/price_1y-1)*100:+.1f}%  ({price_1y:.0f} -> {price_now:.0f})')
print()

# 均線分析
ma20  = hist['Close'].tail(20).mean()
ma60  = hist['Close'].tail(60).mean()
ma120 = hist['Close'].tail(120).mean()
ma240 = hist['Close'].tail(240).mean()

def above_below(price, ma):
    return '高於' if price > ma else '低於'

print('均線分析:')
print(f'  MA20  (月線): {ma20:.0f}  現價{above_below(price_now, ma20)}月線 {abs(price_now/ma20-1)*100:.1f}%')
print(f'  MA60  (季線): {ma60:.0f}  現價{above_below(price_now, ma60)}季線 {abs(price_now/ma60-1)*100:.1f}%')
print(f'  MA120 (半年): {ma120:.0f}  現價{above_below(price_now, ma120)}半年線 {abs(price_now/ma120-1)*100:.1f}%')
print(f'  MA240 (年線): {ma240:.0f}  現價{above_below(price_now, ma240)}年線 {abs(price_now/ma240-1)*100:.1f}%')
print()

# 趨勢判斷
bearish = 0
if price_now < ma20:    bearish += 1
if price_now < ma60:    bearish += 1
if price_now < ma120:   bearish += 1
if price_now < ma240:   bearish += 1
if price_now < price_1m: bearish += 1
if price_now < price_3m: bearish += 1

print(f'空頭信號: {bearish}/6')
if bearish >= 5:
    print('趨勢判斷: 強烈空頭，明確下跌趨勢')
elif bearish >= 3:
    print('趨勢判斷: 偏空，下跌趨勢中')
elif bearish >= 1:
    print('趨勢判斷: 中性偏空，需觀察')
else:
    print('趨勢判斷: 多頭，上漲趨勢')

# 52週高低
high_52w = hist['High'].tail(252).max()
low_52w  = hist['Low'].tail(252).min()
print()
print(f'52週高點: {high_52w:.0f}')
print(f'52週低點: {low_52w:.0f}')
print(f'現價距高點: {(price_now/high_52w-1)*100:.1f}%')
print(f'現價距低點: {(price_now/low_52w-1)*100:+.1f}%')
