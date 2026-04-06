# -*- coding: utf-8 -*-
"""
Monte Carlo 重跑 - 使用 10 年歷史數據（包含 2020 熊市、2008 金融海嘯）
"""
import yfinance as yf
import json, math, random
from datetime import datetime, timezone, timedelta

tz8 = timezone(timedelta(hours=8))
random.seed(42)

print("=== 抓取 10 年歷史數據 ===")

tickers = {
    '^TWII':   '台股加權',
    '0050.TW':'0050元大台灣50',
    '00919.TW':'00919群益高息',
    'VOO':    'VOO S&P500',
}

data_10y = {}
for code, name in tickers.items():
    try:
        t = yf.Ticker(code)
        hist = t.history(period='10y')  # 10年
        data_10y[code] = {
            'name': name,
            'price': hist['Close'].iloc[-1],
            'hist_close': hist['Close'].tolist(),
            'hist_dates': [str(d.date()) for d in hist.index.tolist()],
            'years': len(hist)/252,
        }
        print(f"  {name}: {len(hist)} 天 ({len(hist)/252:.1f} 年)")
    except Exception as e:
        print(f"  FAIL: {name} - {e}")

print(f"\n=== Monte Carlo 模擬（10年歷史，10,000次，1年期）===\n")

def monte_carlo(prices, days=252, sims=10000):
    """Monte Carlo"""
    returns = []
    for i in range(1, len(prices)):
        if prices[i-1] > 0:
            r = math.log(prices[i] / prices[i-1])
            returns.append(r)
    
    mu = sum(returns) / len(returns)
    variance = sum((r - mu)**2 for r in returns) / len(returns)
    sigma = math.sqrt(variance)
    
    last_price = prices[-1]
    results = []
    for _ in range(sims):
        path = [last_price]
        for _ in range(days):
            shock = random.gauss(0, 1)
            drift = mu - 0.5 * variance
            daily_return = math.exp(drift + sigma * shock)
            path.append(path[-1] * daily_return)
        results.append(path[-1])
    
    results.sort()
    n = len(results)
    
    return {
        'mu_annual': mu * 252,
        'sigma_annual': sigma * math.sqrt(252),
        'last_price': last_price,
        'data_years': len(returns) / 252,
        'p5':   results[int(n*0.05)],
        'p10':  results[int(n*0.10)],
        'p25':  results[int(n*0.25)],
        'p50':  results[int(n*0.50)],
        'p75':  results[int(n*0.75)],
        'p90':  results[int(n*0.90)],
        'p95':  results[int(n*0.95)],
        'prob_up':     sum(1 for r in results if r > last_price) / n,
        'prob_up10':   sum(1 for r in results if r > last_price*1.10) / n,
        'prob_up20':   sum(1 for r in results if r > last_price*1.20) / n,
        'prob_down5':  sum(1 for r in results if r < last_price*0.95) / n,
        'prob_down10': sum(1 for r in results if r < last_price*0.90) / n,
        'prob_down20': sum(1 for r in results if r < last_price*0.80) / n,
        'prob_down30': sum(1 for r in results if r < last_price*0.70) / n,
    }

mc_10y = {}
for code, info in data_10y.items():
    prices = info['hist_close']
    result = monte_carlo(prices, days=252, sims=10000)
    mc_10y[code] = {'name': info['name'], **result}
    p = result['last_price']
    print(f"【{info['name']}】")
    print(f"  數據區間: {result['data_years']:.1f} 年")
    print(f"  年化報酬: {result['mu_annual']*100:+.2f}%")
    print(f"  年化波動: {result['sigma_annual']*100:.2f}%")
    print(f"  現價: {p:.2f}")
    print(f"  1年後 P5(最悲觀):  {result['p5']:.2f}  ({(result['p5']/p-1)*100:+.1f}%)")
    print(f"  1年後 P25(悲觀):  {result['p25']:.2f}  ({(result['p25']/p-1)*100:+.1f}%)")
    print(f"  1年後 P50(中位數):{result['p50']:.2f}  ({(result['p50']/p-1)*100:+.1f}%)")
    print(f"  1年後 P75(樂觀):  {result['p75']:.2f}  ({(result['p75']/p-1)*100:+.1f}%)")
    print(f"  1年後 P95(最樂觀):{result['p95']:.2f}  ({(result['p95']/p-1)*100:+.1f}%)")
    print(f"  機率:")
    print(f"    下跌>30%: {result['prob_down30']*100:.1f}%")
    print(f"    下跌>20%: {result['prob_down20']*100:.1f}%")
    print(f"    下跌>10%: {result['prob_down10']*100:.1f}%")
    print(f"    持平(-5~+5%): {result['prob_up']*100 - result['prob_up10']*100:.1f}%")
    print(f"    上漲>10%: {result['prob_up10']*100:.1f}%")
    print(f"    上漲>20%: {result['prob_up20']*100:.1f}%")
    print()

# 同時用 3 年數據對比
print("=== 對比：3年數據 vs 10年數據 ===\n")

with open('market_data_raw.json', 'r', encoding='utf-8') as f:
    data_3y = json.load(f)

for code in ['^TWII', '0050.TW']:
    if code not in mc_10y:
        continue
    name = mc_10y[code]['name']
    
    # 3年
    hist_3y = data_3y.get(code, {}).get('hist_close', [])
    if hist_3y:
        result_3y = monte_carlo(hist_3y, days=252, sims=10000)
        p3 = result_3y['last_price']
    
    # 10年
    result_10y = mc_10y[code]
    p10 = result_10y['last_price']
    
    print(f"【{name}】")
    print(f"  現價: {p10:.2f}")
    print(f"  | 情境 |  3年數據  |  10年數據  |")
    print(f"  |------|----------|----------|")
    print(f"  | 年化報酬 | {result_3y['mu_annual']*100:+.1f}%  | {result_10y['mu_annual']*100:+.1f}%  |")
    print(f"  | 年化波動 | {result_3y['sigma_annual']*100:.1f}%   | {result_10y['sigma_annual']*100:.1f}%   |")
    print(f"  | P5(最悲) | {(result_3y['p5']/p3-1)*100:+.1f}%  | {(result_10y['p5']/p10-1)*100:+.1f}%  |")
    print(f"  | P25(悲) | {(result_3y['p25']/p3-1)*100:+.1f}%  | {(result_10y['p25']/p10-1)*100:+.1f}%  |")
    print(f"  | P50(中) | {(result_3y['p50']/p3-1)*100:+.1f}%  | {(result_10y['p50']/p10-1)*100:+.1f}%  |")
    print(f"  | P95(最樂) | {(result_3y['p95']/p3-1)*100:+.1f}% | {(result_10y['p95']/p10-1)*100:+.1f}% |")
    print(f"  | 下跌>20%機率 | {result_3y['prob_down20']*100:.1f}%  | {result_10y['prob_down20']*100:.1f}%  |")
    print(f"  | 上漲>10%機率 | {result_3y['prob_up10']*100:.1f}%  | {result_10y['prob_up10']*100:.1f}%  |")
    print()

with open('monte_carlo_10y.json', 'w', encoding='utf-8') as f:
    json.dump(mc_10y, f, ensure_ascii=False, indent=2)

print("完成！已儲存 monte_carlo_10y.json")
