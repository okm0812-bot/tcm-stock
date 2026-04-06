# -*- coding: utf-8 -*-
"""
階段 3: Monte Carlo 台股走勢模擬
"""
import json, math, random
from datetime import datetime, timezone, timedelta

tz8 = timezone(timedelta(hours=8))
random.seed(42)

def monte_carlo_simulation(prices, days=252, simulations=10000):
    """Monte Carlo 模擬"""
    import math, random
    
    # 計算日報酬率
    returns = []
    for i in range(1, len(prices)):
        if prices[i-1] > 0:
            r = math.log(prices[i] / prices[i-1])
            returns.append(r)
    
    if not returns:
        return None
    
    mu = sum(returns) / len(returns)
    variance = sum((r - mu)**2 for r in returns) / len(returns)
    sigma = math.sqrt(variance)
    
    last_price = prices[-1]
    results = []
    
    for _ in range(simulations):
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
        'mu_daily': mu,
        'sigma_daily': sigma,
        'mu_annual': mu * 252,
        'sigma_annual': sigma * math.sqrt(252),
        'last_price': last_price,
        'simulations': simulations,
        'days': days,
        'p5':  results[int(n * 0.05)],
        'p10': results[int(n * 0.10)],
        'p25': results[int(n * 0.25)],
        'p50': results[int(n * 0.50)],
        'p75': results[int(n * 0.75)],
        'p90': results[int(n * 0.90)],
        'p95': results[int(n * 0.95)],
        'mean': sum(results) / n,
        'prob_up': sum(1 for r in results if r > last_price) / n,
        'prob_down10': sum(1 for r in results if r < last_price * 0.90) / n,
        'prob_down20': sum(1 for r in results if r < last_price * 0.80) / n,
        'prob_up10': sum(1 for r in results if r > last_price * 1.10) / n,
        'prob_up20': sum(1 for r in results if r > last_price * 1.20) / n,
    }

print("=== 階段 3: Monte Carlo 模擬 ===")

with open('market_data_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

mc_results = {}
targets = ['^TWII', '0050.TW', '00878.TW', '00919.TW', 'VOO']

for code in targets:
    if code in data and 'hist_close' in data[code]:
        prices = data[code]['hist_close']
        name = data[code]['name']
        print(f"  模擬 {name}...")
        result = monte_carlo_simulation(prices, days=252, simulations=10000)
        if result:
            mc_results[code] = {'name': name, **result}
            p = result['last_price']
            print(f"    現價: {p:.2f}")
            print(f"    1年後 P50: {result['p50']:.2f} ({(result['p50']/p-1)*100:+.1f}%)")
            print(f"    上漲機率: {result['prob_up']*100:.1f}%")
        else:
            print(f"    FAIL: 數據不足")

with open('monte_carlo_results.json', 'w', encoding='utf-8') as f:
    json.dump(mc_results, f, ensure_ascii=False, indent=2)

print(f"\nMonte Carlo 完成！")
