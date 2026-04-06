# black_scholes_options.py
# Black-Scholes 選擇權定價模型
# 計算權證、選擇權的理論價格，評估是否被高估或低估

import numpy as np
from scipy.stats import norm
import sys
from datetime import datetime, timedelta

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def black_scholes_call(S, K, T, r, sigma):
    """
    Black-Scholes 買權定價公式
    
    參數:
    S: 標的資產現價
    K: 履約價格
    T: 到期時間（年）
    r: 無風險利率
    sigma: 波動率
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    
    return call_price, d1, d2

def black_scholes_put(S, K, T, r, sigma):
    """
    Black-Scholes 賣權定價公式
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    return put_price, d1, d2

def calculate_greeks(S, K, T, r, sigma, option_type='call'):
    """
    計算選擇權 Greeks（風險指標）
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        delta = norm.cdf(d1)
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) 
                 - r * K * np.exp(-r * T) * norm.cdf(d2)) / 365
    else:
        delta = norm.cdf(d1) - 1
        theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) 
                 + r * K * np.exp(-r * T) * norm.cdf(-d2)) / 365
    
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T) / 100  # 波動率變動 1% 的影響
    
    return {
        'delta': delta,
        'gamma': gamma,
        'theta': theta,
        'vega': vega
    }

print('=' * 70)
print('Black-Scholes 選擇權定價模型')
print('Black-Scholes Option Pricing Model')
print('=' * 70)
print(f'分析時間: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print()

# 範例：假設你持有台泥的認購權證（Call Warrant）
print('【範例分析】台泥認購權證評估')
print('-' * 70)

# 參數設定
S = 22.55  # 台泥現價
K = 25.0   # 履約價格（假設）
T = 0.5    # 到期時間：6 個月 = 0.5 年
r = 0.015  # 無風險利率：1.5%（台灣定存利率）
sigma = 0.40  # 波動率：40%（台泥歷史波動率約 35-45%）

print(f'標的資產現價 (S): {S} 元')
print(f'履約價格 (K): {K} 元')
print(f'到期時間 (T): {T} 年（約 {int(T*365)} 天）')
print(f'無風險利率 (r): {r*100}%')
print(f'波動率 (σ): {sigma*100}%')
print()

# 計算理論價格
call_price, d1, d2 = black_scholes_call(S, K, T, r, sigma)
put_price, _, _ = black_scholes_put(S, K, T, r, sigma)

print('【理論價格計算結果】')
print('-' * 70)
print(f'認購權證（Call）理論價格: {call_price:.3f} 元')
print(f'認售權證（Put）理論價格: {put_price:.3f} 元')
print()

# 計算 Greeks
call_greeks = calculate_greeks(S, K, T, r, sigma, 'call')

print('【風險指標 Greeks】')
print('-' * 70)
print(f"Delta (Δ): {call_greeks['delta']:.4f}")
print(f'  → 標的股價變動 1 元，權證價格變動約 {call_greeks["delta"]:.2f} 元')
print()
print(f"Gamma (Γ): {call_greeks['gamma']:.4f}")
print(f'  → Delta 的變化速度，衡量凸性風險')
print()
print(f"Theta (Θ): {call_greeks['theta']:.4f} 元/天")
print(f'  → 時間流逝，每天權證價值減少約 {abs(call_greeks["theta"]):.3f} 元')
print(f'  → 時間是選擇權買方最大的敵人！')
print()
print(f"Vega (V): {call_greeks['vega']:.4f}")
print(f'  → 波動率變動 1%，權證價格變動約 {call_greeks["vega"]:.2f} 元')
print()

# 情境分析
print('【情境分析】不同股價下的權證價值')
print('-' * 70)
print(f'{'台泥股價':<12} {'權證價格':<12} {'內含價值':<12} {'時間價值':<12}')
print('-' * 70)

for price in [18, 20, 22, 22.55, 25, 28, 30]:
    call_p, _, _ = black_scholes_call(price, K, T, r, sigma)
    intrinsic = max(0, price - K)  # 內含價值
    time_value = call_p - intrinsic  # 時間價值
    
    print(f'{price:<12.2f} {call_p:<12.3f} {intrinsic:<12.3f} {time_value:<12.3f}')

print()

# 損益平衡點
breakeven = K + call_price
print(f'【損益分析】')
print('-' * 70)
print(f'權證成本: {call_price:.3f} 元')
print(f'履約價格: {K} 元')
print(f'損益平衡點: {breakeven:.2f} 元')
print(f'  → 台泥股價必須漲到 {breakeven:.2f} 元以上，權證才有獲利')
print(f'  → 目前股價 {S} 元，需要漲幅 {(breakeven/S-1)*100:.1f}%')
print()

# 隱含波動率計算（如果知道市場價格）
print('【隱含波動率計算】')
print('-' * 70)
print('如果你知道市場上權證的實際交易價格，可以反推隱含波動率')
print('範例：假設市場價格 2.5 元，計算隱含波動率...')

market_price = 2.5  # 假設市場價格

# 簡單的隱含波動率計算（二分搜尋）
def implied_volatility(S, K, T, r, market_price, option_type='call'):
    """計算隱含波動率"""
    sigma_low = 0.001
    sigma_high = 5.0
    
    for _ in range(100):  # 最多迭代 100 次
        sigma_mid = (sigma_low + sigma_high) / 2
        
        if option_type == 'call':
            price, _, _ = black_scholes_call(S, K, T, r, sigma_mid)
        else:
            price, _, _ = black_scholes_put(S, K, T, r, sigma_mid)
        
        if abs(price - market_price) < 0.0001:
            return sigma_mid
        
        if price < market_price:
            sigma_low = sigma_mid
        else:
            sigma_high = sigma_mid
    
    return (sigma_low + sigma_high) / 2

iv = implied_volatility(S, K, T, r, market_price)
print(f'隱含波動率: {iv*100:.1f}%')
print(f'  → 若隱含波動率 > 歷史波動率（{sigma*100}%），權證可能被高估')
print(f'  → 若隱含波動率 < 歷史波動率，權證可能被低估')
print()

print('=' * 70)
print('Black-Scholes 模型分析完成')
print('=' * 70)
print()
print('應用場景：')
print('• 評估權證是否被高估/低估')
print('• 計算損益平衡點，決定是否進場')
print('• 了解時間價值衰減速度（Theta）')
print('• 評估波動率風險（Vega）')
print()
print('注意：Black-Scholes 模型假設：')
print('• 股價服從對數常態分布')
print('• 波動率恆定（實際上會變動）')
print('• 無交易成本、無股息（需調整）')
