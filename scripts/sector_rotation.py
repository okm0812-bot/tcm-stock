import yfinance as yf
import numpy as np
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 台灣各產業代表標的
sectors = {
    '半導體':   '00881.TW',
    '台灣50':   '0050.TW',
    '高股息':   '0056.TW',
    '金融':     '0055.TW',
    '科技':     '0052.TW',
    '電子(鴻海)': '2317.TW',
    '面板(友達)': '2409.TW',
    '水泥(台泥)': '1101.TW',
    '生技(康霈)': '6919.TW',
}

# 美國各產業 ETF（對照）
us_sectors = {
    '美科技 QQQ':  'QQQ',
    '美金融 XLF':  'XLF',
    '美能源 XLE':  'XLE',
    '美醫療 XLV':  'XLV',
    '美半導體 SOXX': 'SOXX',
}

print('=' * 65)
print('產業輪動分析系統')
print('=' * 65)
print()

def analyze_sector(name, ticker):
    try:
        hist = yf.Ticker(ticker).history(period='3mo')
        if len(hist) < 10:
            return None
        p_now = hist['Close'].iloc[-1]
        p_1w  = hist['Close'].iloc[-5]  if len(hist) >= 5  else hist['Close'].iloc[0]
        p_1m  = hist['Close'].iloc[-22] if len(hist) >= 22 else hist['Close'].iloc[0]
        p_3m  = hist['Close'].iloc[0]

        r1w = (p_now / p_1w - 1) * 100
        r1m = (p_now / p_1m - 1) * 100
        r3m = (p_now / p_3m - 1) * 100

        # 動能評分（1週+1月+3月加權）
        momentum = r1w * 0.5 + r1m * 0.3 + r3m * 0.2

        return {'name': name, 'ticker': ticker,
                'r1w': r1w, 'r1m': r1m, 'r3m': r3m,
                'momentum': momentum, 'price': p_now}
    except:
        return None

print('【台灣產業輪動】')
print(f'{"產業":<14} {"1週":>8} {"1月":>8} {"3月":>8} {"動能分":>8}  {"訊號"}')
print('-' * 65)

tw_results = []
for name, ticker in sectors.items():
    r = analyze_sector(name, ticker)
    if r:
        tw_results.append(r)

# 按動能排序
tw_results.sort(key=lambda x: x['momentum'], reverse=True)

for r in tw_results:
    if r['r1m'] > 2 and r['r1w'] > 0:
        sig = '🟢🟢 強勢流入'
    elif r['r1m'] > 0:
        sig = '🟢 偏強'
    elif r['r1m'] > -5:
        sig = '🟡 中性'
    elif r['r1m'] > -10:
        sig = '🔴 偏弱'
    else:
        sig = '🔴🔴 強勢流出'

    print(f'{r["name"]:<14} {r["r1w"]:>+7.1f}% {r["r1m"]:>+7.1f}% {r["r3m"]:>+7.1f}%  {r["momentum"]:>+6.1f}  {sig}')

print()
print('【美國產業輪動（對照）】')
print(f'{"產業":<16} {"1週":>8} {"1月":>8} {"3月":>8} {"動能分":>8}  {"訊號"}')
print('-' * 65)

us_results = []
for name, ticker in us_sectors.items():
    r = analyze_sector(name, ticker)
    if r:
        us_results.append(r)

us_results.sort(key=lambda x: x['momentum'], reverse=True)

for r in us_results:
    if r['r1m'] > 2 and r['r1w'] > 0:
        sig = '🟢🟢 強勢'
    elif r['r1m'] > 0:
        sig = '🟢 偏強'
    elif r['r1m'] > -5:
        sig = '🟡 中性'
    elif r['r1m'] > -10:
        sig = '🔴 偏弱'
    else:
        sig = '🔴🔴 強勢流出'

    print(f'{r["name"]:<16} {r["r1w"]:>+7.1f}% {r["r1m"]:>+7.1f}% {r["r3m"]:>+7.1f}%  {r["momentum"]:>+6.1f}  {sig}')

print()
print('=' * 65)
print('產業輪動解讀')
print('=' * 65)

if tw_results:
    top3 = tw_results[:3]
    bot3 = tw_results[-3:]

    print()
    print('資金流入（強勢）前3名：')
    for r in top3:
        print(f'  {r["name"]:<14} 動能: {r["momentum"]:+.1f}  1月: {r["r1m"]:+.1f}%')

    print()
    print('資金流出（弱勢）後3名：')
    for r in bot3:
        print(f'  {r["name"]:<14} 動能: {r["momentum"]:+.1f}  1月: {r["r1m"]:+.1f}%')

    print()
    # 判斷整體市場氣氛
    avg_momentum = sum(r['momentum'] for r in tw_results) / len(tw_results)
    positive_count = sum(1 for r in tw_results if r['r1m'] > 0)

    print(f'整體市場動能: {avg_momentum:+.1f}')
    print(f'上漲產業數: {positive_count}/{len(tw_results)}')

    if avg_momentum > 3:
        print('市場氣氛: 🟢 整體偏多，資金積極進場')
    elif avg_momentum > 0:
        print('市場氣氛: 🟡 整體中性，選股重於選市')
    elif avg_momentum > -5:
        print('市場氣氛: 🟡 整體偏弱，謹慎為主')
    else:
        print('市場氣氛: 🔴 整體偏空，資金撤退中')

    print()
    print('【對你的建議】')
    print('你的持股產業排名：')
    your_stocks = ['水泥(台泥)', '面板(友達)', '生技(康霈)']
    for r in tw_results:
        if r['name'] in your_stocks:
            rank = tw_results.index(r) + 1
            print(f'  {r["name"]}: 第 {rank}/{len(tw_results)} 名  動能 {r["momentum"]:+.1f}')

print()
print('=' * 65)
print('分析完成')
print('=' * 65)
