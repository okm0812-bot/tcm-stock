# monte_carlo_simulation.py
# Monte Carlo 模擬 - 預測投資組合未來多種情境
# 模擬 10,000 種可能的未來，計算 VaR、預期報酬、破產機率

import yfinance as yf
import numpy as np
import pandas as pd
import sys
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print('=' * 70)
print('Monte Carlo 投資組合模擬系統')
print('Monte Carlo Simulation for Portfolio Forecasting')
print('=' * 70)
print(f'分析時間: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print()

# 你的持倉
portfolio = {
    '1101.TW': {'name': '台泥', 'shares': 19000, 'cost': 34.56, 'weight': 0.25},
    '2352.TW': {'name': '佳世達', 'shares': 11000, 'cost': 53.78, 'weight': 0.20},
    '2409.TW': {'name': '友達', 'shares': 9000, 'cost': 16.20, 'weight': 0.15},
    '6919.TW': {'name': '康霈', 'shares': 300, 'cost': 102.36, 'weight': 0.10},
    'BOND': {'name': '美債ETF組合', 'value': 1986690, 'weight': 0.30, 'return': 0.03, 'volatility': 0.08},
}

# 抓取歷史數據
def fetch_returns(ticker, period='2y'):
    """抓取股票歷史報酬率"""
    try:
        if ticker == 'BOND':
            return None, portfolio['BOND']['return'], portfolio['BOND']['volatility']
        
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if len(hist) < 60:
            return None, 0, 0
        
        # 計算日報酬率
        returns = hist['Close'].pct_change().dropna()
        
        # 年化報酬率和波動率
        annual_return = returns.mean() * 252
        annual_volatility = returns.std() * np.sqrt(252)
        
        return returns, annual_return, annual_volatility
        
    except Exception as e:
        return None, 0, 0

print('【步驟 1】抓取歷史數據計算參數')
print('-' * 70)

assets = []
for ticker, info in portfolio.items():
    returns, ann_return, ann_vol = fetch_returns(ticker)
    
    if ticker != 'BOND':
        data = yf.Ticker(ticker).info
        current_price = data.get('regularMarketPrice', 0)
        position_value = current_price * info['shares']
    else:
        current_price = 0
        position_value = info['value']
    
    assets.append({
        'ticker': ticker,
        'name': info['name'],
        'weight': info['weight'],
        'current_value': position_value,
        'expected_return': ann_return,
        'volatility': ann_vol,
        'returns': returns
    })
    
    print(f'{info["name"]:<12} 預期報酬: {ann_return*100:>6.1f}%  波動率: {ann_vol*100:>6.1f}%')

print()

# Monte Carlo 模擬參數
print('【步驟 2】Monte Carlo 模擬參數設定')
print('-' * 70)

n_simulations = 10000  # 模擬次數
n_days = 252  # 模擬 1 年（252 交易日）
initial_portfolio_value = sum([a['current_value'] for a in assets])

print(f'模擬次數: {n_simulations:,} 次')
print(f'模擬期間: {n_days} 天（約 1 年）')
print(f'初始投資組合價值: {initial_portfolio_value:,.0f} 元')
print()

# 計算投資組合的預期報酬和波動率
portfolio_return = sum([a['weight'] * a['expected_return'] for a in assets])

# 簡化：假設相關性為 0.5（實際應計算共變異數矩陣）
portfolio_volatility = np.sqrt(sum([a['weight']**2 * a['volatility']**2 for a in assets]))

print(f'投資組合預期年化報酬: {portfolio_return*100:.1f}%')
print(f'投資組合預期年化波動: {portfolio_volatility*100:.1f}%')
print()

# 執行 Monte Carlo 模擬
print('【步驟 3】執行 Monte Carlo 模擬...')
print('-' * 70)

np.random.seed(42)  # 設定隨機種子，結果可重現

# 產生隨機報酬路徑
random_returns = np.random.normal(
    portfolio_return / 252,  # 日預期報酬
    portfolio_volatility / np.sqrt(252),  # 日波動率
    (n_simulations, n_days)
)

# 計算累積報酬
cumulative_returns = np.cumprod(1 + random_returns, axis=1)

# 最終投資組合價值
final_values = initial_portfolio_value * cumulative_returns[:, -1]

print(f'模擬完成！計算 {n_simulations:,} 條路徑')
print()

# 分析結果
print('【步驟 4】模擬結果分析')
print('=' * 70)

# 基本統計
mean_final = np.mean(final_values)
median_final = np.median(final_values)
std_final = np.std(final_values)

print(f'初始投資組合價值: {initial_portfolio_value:>15,.0f} 元')
print(f'平均最終價值:     {mean_final:>15,.0f} 元 ({(mean_final/initial_portfolio_value-1)*100:+.1f}%)')
print(f'中位數最終價值:   {median_final:>15,.0f} 元 ({(median_final/initial_portfolio_value-1)*100:+.1f}%)')
print(f'標準差:           {std_final:>15,.0f} 元')
print()

# 百分位數分析
percentiles = [5, 10, 25, 50, 75, 90, 95]
print('【情境分析】不同機率下的投資組合價值')
print('-' * 70)
print(f'{'機率':<8} {'投資組合價值':>15} {'報酬率':>12} {'情境':<20}')
print('-' * 70)

for p in percentiles:
    value = np.percentile(final_values, p)
    return_pct = (value / initial_portfolio_value - 1) * 100
    
    if p <= 10:
        scenario = '極度悲觀（黑天鵝）'
    elif p <= 25:
        scenario = '悲觀情境'
    elif p <= 50:
        scenario = '中性偏弱'
    elif p <= 75:
        scenario = '中性偏強'
    elif p <= 90:
        scenario = '樂觀情境'
    else:
        scenario = '極度樂觀（大牛市）'
    
    print(f'{p:>3}%     {value:>15,.0f} 元   {return_pct:>+10.1f}%   {scenario}')

print()

# 風險指標
print('【風險指標】')
print('-' * 70)

# VaR (Value at Risk)
var_95 = np.percentile(final_values, 5)
var_99 = np.percentile(final_values, 1)

print(f'VaR (95%): {var_95:,.0f} 元')
print(f'  → 有 5% 機率，1 年後投資組合價值低於 {var_95:,.0f} 元')
print(f'  → 相當於虧損 {initial_portfolio_value - var_95:,.0f} 元 ({(var_95/initial_portfolio_value-1)*100:.1f}%)')
print()

print(f'VaR (99%): {var_99:,.0f} 元')
print(f'  → 有 1% 機率，1 年後投資組合價值低於 {var_99:,.0f} 元')
print(f'  → 相當於虧損 {initial_portfolio_value - var_99:,.0f} 元 ({(var_99/initial_portfolio_value-1)*100:.1f}%)')
print()

# 破產機率（價值低於某個門檻）
bankruptcy_threshold = initial_portfolio_value * 0.5  # 虧損 50%
bankruptcy_prob = np.mean(final_values < bankruptcy_threshold) * 100

print(f'破產機率（虧損 >50%）: {bankruptcy_prob:.1f}%')
print(f'  → 有 {bankruptcy_prob:.1f}% 的機率，1 年後投資組合價值低於 {bankruptcy_threshold:,.0f} 元')
print()

# 獲利機率
profit_prob = np.mean(final_values > initial_portfolio_value) * 100
print(f'獲利機率（不賠不賺以上）: {profit_prob:.1f}%')
print()

# 大賺機率（報酬 >20%）
big_gain_prob = np.mean(final_values > initial_portfolio_value * 1.2) * 100
print(f'大賺機率（報酬 >20%）: {big_gain_prob:.1f}%')
print()

print('=' * 70)
print('Monte Carlo 模擬完成')
print('=' * 70)
print()
print('免責聲明：')
print('• 此模擬基於歷史波動率，未來實際結果可能不同')
print('• Monte Carlo 模擬僅供參考，不構成投資建議')
print('• 過去績效不代表未來表現')
