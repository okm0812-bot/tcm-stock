# -*- coding: utf-8 -*-
import yfinance as yf
from datetime import datetime, timezone, timedelta

tz8 = timezone(timedelta(hours=8))

def get(code, name):
    try:
        t = yf.Ticker(code)
        i = t.info
        price = i.get('regularMarketPrice', 0)
        prev  = i.get('regularMarketPreviousClose', 0)
        h52   = i.get('fiftyTwoWeekHigh', 0)
        l52   = i.get('fiftyTwoWeekLow', 0)
        ts    = i.get('regularMarketTime', 0)
        chg   = price - prev if prev else 0
        pct   = chg / prev * 100 if prev else 0
        dist_high = (price - h52) / h52 * 100 if h52 else 0
        time_str = datetime.fromtimestamp(ts, tz=tz8).strftime('%Y-%m-%d %H:%M') if ts else 'N/A'
        return {
            'name': name, 'price': price, 'prev': prev,
            'chg': chg, 'pct': pct, 'h52': h52, 'l52': l52,
            'dist_high': dist_high, 'time': time_str
        }
    except Exception as e:
        return {'name': name, 'error': str(e)}

items = [
    ('^TWII',    '台股加權指數'),
    ('0050.TW',  '元大台灣50 (0050)'),
    ('00878.TW', '國泰永續高股息 (00878)'),
    ('00919.TW', '群益台灣精選高息 (00919)'),
    ('VOO',      'Vanguard S&P500 (VOO)'),
    ('^GSPC',    'S&P 500'),
    ('^VIX',     'VIX 恐慌指數'),
    ('^TNX',     '美國10年債殖利率'),
    ('1101.TW',  '台泥'),
    ('2352.TW',  '佳世達'),
    ('2409.TW',  '友達'),
    ('6919.TW',  '康霈'),
]

results = {code: get(code, name) for code, name in items}

lines = []
def add(t=''): lines.append(t)

add("="*65)
add("CEO 數據核實報告")
add(f"抓取時間: {datetime.now(tz8).strftime('%Y-%m-%d %H:%M:%S')}")
add("來源: Yahoo Finance (盤中15分鐘延遲，收盤後準確)")
add("="*65)

add("\n【大盤 & 指標】")
add("-"*65)
for code in ['^TWII','^GSPC','^VIX','^TNX']:
    r = results[code]
    if 'error' not in r:
        if code == '^VIX':
            add(f"  {r['name']:<25}: {r['price']:.2f}")
        elif code == '^TNX':
            add(f"  {r['name']:<25}: {r['price']:.3f}%")
        else:
            add(f"  {r['name']:<25}: {r['price']:>8,.0f}  ({r['chg']:>+7,.0f}, {r['pct']:>+5.2f}%)  資料:{r['time']}")

add("\n【ETF 現況】")
add("-"*65)
add(f"  {'名稱':<28} {'現價':>8} {'漲跌%':>7} {'距高點':>8} {'資料時間'}")
add("-"*65)
for code in ['0050.TW','00878.TW','00919.TW','VOO']:
    r = results[code]
    if 'error' not in r:
        add(f"  {r['name']:<28} {r['price']:>8.2f} {r['pct']:>+6.2f}% {r['dist_high']:>+7.1f}%  {r['time']}")

add("\n【持股現況】")
add("-"*65)
add(f"  {'名稱':<12} {'現價':>8} {'漲跌%':>7} {'資料時間'}")
add("-"*65)
for code in ['1101.TW','2352.TW','2409.TW','6919.TW']:
    r = results[code]
    if 'error' not in r:
        add(f"  {r['name']:<12} {r['price']:>8.2f} {r['pct']:>+6.2f}%  {r['time']}")

with open('verified_data.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('\n'.join(lines))
