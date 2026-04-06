# -*- coding: utf-8 -*-
import sys, json, math
sys.stdout.reconfigure(encoding='utf-8')

def calc_returns(prices):
    returns = []
    for i in range(1, len(prices)):
        if prices[i-1] > 0:
            returns.append((prices[i] - prices[i-1]) / prices[i-1])
    return returns

def multi_regression(X_cols, y):
    n = len(y)
    k = len(X_cols)
    X_means = [sum(col) / n for col in X_cols]
    X_stds = [math.sqrt(sum((x - X_means[i])**2 for x in X_cols[i]) / n) for i in range(k)]
    X_norm = []
    for i in range(k):
        if X_stds[i] > 0:
            X_norm.append([(x - X_means[i]) / X_stds[i] for x in X_cols[i]])
        else:
            X_norm.append([0] * n)
    y_mean = sum(y) / n
    y_std = math.sqrt(sum((yi - y_mean)**2 for yi in y) / n)
    y_norm = [(yi - y_mean) / y_std if y_std > 0 else 0 for yi in y]
    betas = [0.0] * k
    alpha = 0.0
    lr = 0.01
    for _ in range(1000):
        preds = [alpha + sum(betas[j] * X_norm[j][i] for j in range(k)) for i in range(n)]
        errors = [preds[i] - y_norm[i] for i in range(n)]
        alpha -= lr * sum(errors) / n
        for j in range(k):
            betas[j] -= lr * sum(errors[i] * X_norm[j][i] for i in range(n)) / n
    real_betas = [betas[j] * y_std / X_stds[j] if X_stds[j] > 0 else 0 for j in range(k)]
    real_alpha = y_mean - sum(real_betas[j] * X_means[j] for j in range(k))
    preds_real = [real_alpha + sum(real_betas[j] * X_cols[j][i] for j in range(k)) for i in range(n)]
    ss_res = sum((y[i] - preds_real[i])**2 for i in range(n))
    ss_tot = sum((y[i] - y_mean)**2 for i in range(n))
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return real_alpha, real_betas, r2

print("=== 階段 5: Fama-French 因子分析 ===")

with open('market_data_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

rf_daily = 0.043 / 252

twii_prices = data.get('^TWII', {}).get('hist_close', [])
twii_returns = calc_returns(twii_prices)
mkt_factor = [r - rf_daily for r in twii_returns]

etf50_prices = data.get('0050.TW', {}).get('hist_close', [])
etf919_prices = data.get('00919.TW', {}).get('hist_close', [])
etf50_returns = calc_returns(etf50_prices)
etf919_returns = calc_returns(etf919_prices)

min_len = min(len(mkt_factor), len(etf50_returns), len(etf919_returns))
mkt_factor = mkt_factor[-min_len:]
etf50_returns = etf50_returns[-min_len:]
etf919_returns = etf919_returns[-min_len:]
smb_factor = [etf919_returns[i] - etf50_returns[i] for i in range(min_len)]

etf878_prices = data.get('00878.TW', {}).get('hist_close', [])
voo_prices = data.get('VOO', {}).get('hist_close', [])
etf878_returns = calc_returns(etf878_prices)
voo_returns = calc_returns(voo_prices)

min_len2 = min(len(mkt_factor), len(etf878_returns), len(voo_returns))
mkt_f = mkt_factor[-min_len2:]
smb_f = smb_factor[-min_len2:]
etf878_r = etf878_returns[-min_len2:]
voo_r = voo_returns[-min_len2:]
hml_factor = [etf878_r[i] - voo_r[i] for i in range(min_len2)]

print(f"  因子數據長度: {min_len2} 天")

stocks = [
    ('1101.TW', '台泥'),
    ('2352.TW', '佳世達'),
    ('2409.TW', '友達'),
    ('6919.TW', '康霈'),
    ('0050.TW', '元大台灣50'),
    ('00919.TW', '群益高息'),
]

ff_results = {}

for code, name in stocks:
    if code not in data or 'hist_close' not in data[code]:
        continue
    prices = data[code]['hist_close']
    returns = calc_returns(prices)
    min_l = min(len(returns), min_len2)
    excess_returns = [returns[-min_l:][i] - rf_daily for i in range(min_l)]
    mkt_use = mkt_f[-min_l:]
    smb_use = smb_f[-min_l:]
    hml_use = hml_factor[-min_l:]
    alpha, betas, r2 = multi_regression([mkt_use, smb_use, hml_use], excess_returns)
    alpha_annual = alpha * 252
    ff_results[code] = {
        'name': name,
        'alpha': alpha_annual,
        'beta_mkt': betas[0],
        'beta_smb': betas[1],
        'beta_hml': betas[2],
        'r2': r2,
    }
    print(f"\n  {name}:")
    print(f"    Alpha (年化): {alpha_annual*100:+.2f}%")
    print(f"    Beta 市場: {betas[0]:.3f}")
    print(f"    Beta SMB: {betas[1]:.3f}")
    print(f"    Beta HML: {betas[2]:.3f}")
    print(f"    R2: {r2:.3f}")

with open('fama_french_results.json', 'w', encoding='utf-8') as f:
    json.dump(ff_results, f, ensure_ascii=False, indent=2)

print(f"\nFama-French 完成！")
