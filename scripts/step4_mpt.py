# -*- coding: utf-8 -*-
"""
階段 4: MPT 現代投資組合理論優化
"""
import json, math

def portfolio_stats(weights, returns_list, cov_matrix):
    """計算投資組合統計"""
    n = len(weights)
    
    # 年化報酬率
    port_return = sum(weights[i] * returns_list[i] for i in range(n)) * 252
    
    # 年化波動率
    port_var = 0
    for i in range(n):
        for j in range(n):
            port_var += weights[i] * weights[j] * cov_matrix[i][j]
    port_var *= 252
    port_std = math.sqrt(port_var)
    
    # 夏普比率（無風險利率 4.3%）
    rf = 0.043
    sharpe = (port_return - rf) / port_std if port_std > 0 else 0
    
    return port_return, port_std, sharpe

def calc_returns(prices):
    """計算日報酬率"""
    returns = []
    for i in range(1, len(prices)):
        if prices[i-1] > 0:
            returns.append((prices[i] - prices[i-1]) / prices[i-1])
    return returns

def calc_cov_matrix(returns_lists):
    """計算共變異數矩陣"""
    n = len(returns_lists)
    min_len = min(len(r) for r in returns_lists)
    
    # 截取相同長度
    returns_lists = [r[-min_len:] for r in returns_lists]
    
    means = [sum(r) / len(r) for r in returns_lists]
    
    cov = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            cov_sum = sum(
                (returns_lists[i][k] - means[i]) * (returns_lists[j][k] - means[j])
                for k in range(min_len)
            )
            cov[i][j] = cov_sum / min_len
    
    return cov

print("=== 階段 4: MPT 投資組合優化 ===")

with open('market_data_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 定義候選資產
assets = [
    ('0050.TW',  '元大台灣50'),
    ('00919.TW', '群益高息'),
    ('VOO',      'Vanguard S&P500'),
    ('00878.TW', '國泰高股息'),
]

# 計算各資產報酬率
returns_data = {}
for code, name in assets:
    if code in data and 'hist_close' in data[code]:
        prices = data[code]['hist_close']
        returns_data[code] = calc_returns(prices)
        mean_r = sum(returns_data[code]) / len(returns_data[code]) * 252
        std_r = math.sqrt(sum((r - mean_r/252)**2 for r in returns_data[code]) / len(returns_data[code])) * math.sqrt(252)
        print(f"  {name}: 年化報酬 {mean_r*100:.2f}%, 年化波動 {std_r*100:.2f}%")

# 計算共變異數矩陣
codes = [c for c, _ in assets if c in returns_data]
names = [n for c, n in assets if c in returns_data]
returns_lists = [returns_data[c] for c in codes]
cov_matrix = calc_cov_matrix(returns_lists)

# 隨機模擬 50,000 個投資組合
import random
random.seed(42)

best_sharpe = {'sharpe': -999, 'weights': None, 'return': 0, 'std': 0}
best_return = {'return': -999, 'weights': None, 'sharpe': 0, 'std': 0}
min_vol = {'std': 999, 'weights': None, 'return': 0, 'sharpe': 0}

mean_returns = [sum(r) / len(r) for r in returns_lists]

portfolios = []
for _ in range(50000):
    # 隨機權重
    w = [random.random() for _ in range(len(codes))]
    total = sum(w)
    w = [x / total for x in w]
    
    ret, std, sharpe = portfolio_stats(w, mean_returns, cov_matrix)
    portfolios.append({'weights': w, 'return': ret, 'std': std, 'sharpe': sharpe})
    
    if sharpe > best_sharpe['sharpe']:
        best_sharpe = {'sharpe': sharpe, 'weights': w, 'return': ret, 'std': std}
    if ret > best_return['return']:
        best_return = {'return': ret, 'weights': w, 'sharpe': sharpe, 'std': std}
    if std < min_vol['std']:
        min_vol = {'std': std, 'weights': w, 'return': ret, 'sharpe': sharpe}

print(f"\n最佳夏普比率組合:")
for i, code in enumerate(codes):
    print(f"  {names[i]}: {best_sharpe['weights'][i]*100:.1f}%")
print(f"  年化報酬: {best_sharpe['return']*100:.2f}%")
print(f"  年化波動: {best_sharpe['std']*100:.2f}%")
print(f"  夏普比率: {best_sharpe['sharpe']:.3f}")

print(f"\n最小波動組合:")
for i, code in enumerate(codes):
    print(f"  {names[i]}: {min_vol['weights'][i]*100:.1f}%")
print(f"  年化報酬: {min_vol['return']*100:.2f}%")
print(f"  年化波動: {min_vol['std']*100:.2f}%")
print(f"  夏普比率: {min_vol['sharpe']:.3f}")

mpt_results = {
    'assets': [{'code': c, 'name': n} for c, n in zip(codes, names)],
    'best_sharpe': best_sharpe,
    'best_return': best_return,
    'min_vol': min_vol,
    'mean_returns': mean_returns,
}

with open('mpt_results.json', 'w', encoding='utf-8') as f:
    json.dump(mpt_results, f, ensure_ascii=False, indent=2)

print(f"\nMPT 完成！")
