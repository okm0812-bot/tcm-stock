# portfolio_optimization_mpt.py
# 投資組合優化 - Modern Portfolio Theory (MPT)
# 計算最佳資產配置，在給定風險下最大化報酬，或在給定報酬下最小化風險

import yfinance as yf
import numpy as np
import pandas as pd
import sys
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print('=' * 70)
print('投資組合優化系統 - Modern Portfolio Theory (MPT)')
print('Modern Portfolio Theory - Optimal Asset Allocation')
print('=' * 70)
print(f'分析時間: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print()

# 可投資資產（你的選擇範圍）
assets = {
    '1101.TW': {'name': '台泥', 'type': '股票'},
    '2352.TW': {'name': '佳世達', 'type': '股票'},
    '2409.TW': {'name': '友達', 'type': '股票'},
    '6919.TW': {'name': '康霈', 'type': '股票'},
    '00687B.TW': {'name': '國泰美債20年', 'type': '債券'},
    '00795B.TW': {'name': '中信美債20年', 'type': '債券'},
    '2330.TW': {'name': '台積電', 'type': '股票'},  # 對照組
    '0050.TW': {'name': '元大台灣50', 'type': 'ETF'},  # 大盤
}

print('【步驟 1】抓取歷史數據計算預期報酬和風險')
print('-' * 70)

returns_data = {}
valid_assets = []

for ticker, info in assets.items():
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='2y')
        
        if len(hist) < 100:
            print(f'{info["name"]:<12} 資料不足，跳過')
            continue
        
        # 計算日報酬率
        daily_returns = hist['Close'].pct_change().dropna()
        
        # 年化報酬率和波動率
        annual_return = daily_returns.mean() * 252
        annual_volatility = daily_returns.std() * np.sqrt(252)
        
        returns_data[ticker] = {
            'name': info['name'],
            'type': info['type'],
            'return': annual_return,
            'volatility': annual_volatility,
            'sharpe': annual_return / annual_volatility if annual_volatility > 0 else 0,
            'daily_returns': daily_returns
        }
        
        valid_assets.append(ticker)
        
        print(f'{info["name"]:<12} 年化報酬: {annual_return*100:>7.1f}%  波動: {annual_volatility*100:>6.1f}%  夏普: {annual_return/annual_volatility:>5.2f}')
        
    except Exception as e:
        print(f'{info["name"]:<12} 抓取失敗: {e}')

print()

if len(valid_assets) < 3:
    print('可用資產太少，無法進行投資組合優化')
    sys.exit()

# 計算共變異數矩陣
print('【步驟 2】計算資產間相關性')
print('-' * 70)

# 建立報酬率 DataFrame
returns_df = pd.DataFrame({ticker: returns_data[ticker]['daily_returns'] for ticker in valid_assets})
returns_df = returns_df.dropna()

# 計算相關性矩陣
correlation_matrix = returns_df.corr()
print('資產間相關性矩陣：')
print(correlation_matrix.round(2))
print()

# 計算共變異數矩陣（年化）
cov_matrix = returns_df.cov() * 252

# 投資組合優化
print('【步驟 3】投資組合優化計算')
print('-' * 70)

def portfolio_performance(weights, returns, cov_matrix):
    """計算投資組合的報酬和風險"""
    portfolio_return = np.sum(returns * weights)
    portfolio_std = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return portfolio_return, portfolio_std

def generate_random_portfolios(n_portfolios, returns, cov_matrix):
    """產生隨機投資組合"""
    n_assets = len(returns)
    results = np.zeros((3, n_portfolios))
    weights_record = []
    
    for i in range(n_portfolios):
        # 隨機權重
        weights = np.random.random(n_assets)
        weights /= np.sum(weights)  # 標準化為 1
        
        portfolio_return, portfolio_std = portfolio_performance(weights, returns, cov_matrix)
        sharpe = portfolio_return / portfolio_std if portfolio_std > 0 else 0
        
        results[0, i] = portfolio_std
        results[1, i] = portfolio_return
        results[2, i] = sharpe
        
        weights_record.append(weights)
    
    return results, weights_record

# 準備數據
returns = np.array([returns_data[t]['return'] for t in valid_assets])
n_assets = len(valid_assets)

print(f'產生 10,000 個隨機投資組合...')
results, weights_record = generate_random_portfolios(10000, returns, cov_matrix)

# 找到最佳投資組合
max_sharpe_idx = np.argmax(results[2])
min_vol_idx = np.argmin(results[0])

print()
print('【最佳投資組合】')
print('=' * 70)

# 最大夏普比率投資組合
print('\n1. 最大夏普比率投資組合（風險調整後報酬最佳）')
print('-' * 70)
max_sharpe_weights = weights_record[max_sharpe_idx]
print(f'預期年化報酬: {results[1, max_sharpe_idx]*100:.2f}%')
print(f'預期年化波動: {results[0, max_sharpe_idx]*100:.2f}%')
print(f'夏普比率: {results[2, max_sharpe_idx]:.3f}')
print()
print('資產配置：')
for i, ticker in enumerate(valid_assets):
    if max_sharpe_weights[i] > 0.01:  # 只顯示權重 >1% 的
        print(f'  {returns_data[ticker]["name"]:<12} {max_sharpe_weights[i]*100:>6.1f}%')

# 最小風險投資組合
print()
print('2. 最小風險投資組合（適合保守型投資人）')
print('-' * 70)
min_vol_weights = weights_record[min_vol_idx]
print(f'預期年化報酬: {results[1, min_vol_idx]*100:.2f}%')
print(f'預期年化波動: {results[0, min_vol_idx]*100:.2f}%')
print(f'夏普比率: {results[2, min_vol_idx]:.3f}')
print()
print('資產配置：')
for i, ticker in enumerate(valid_assets):
    if min_vol_weights[i] > 0.01:
        print(f'  {returns_data[ticker]["name"]:<12} {min_vol_weights[i]*100:>6.1f}%')

# 效率前緣上的其他選擇
print()
print('【效率前緣分析】')
print('=' * 70)

target_returns = [0.02, 0.05, 0.08, 0.10, 0.12]  # 目標報酬率
print(f'{'目標報酬':<10} {'最小波動':<12} {'夏普比率':<10} {'建議':<30}')
print('-' * 70)

for target in target_returns:
    # 找到最接近目標報酬的投資組合
    diff = np.abs(results[1] - target)
    idx = np.argmin(diff)
    
    volatility = results[0, idx]
    sharpe = results[2, idx]
    
    if sharpe > 0.5:
        suggestion = '可接受'
    elif sharpe > 0.3:
        suggestion = '風險偏高'
    else:
        suggestion = '不建議'
    
    print(f'{target*100:>6.1f}%     {volatility*100:>6.1f}%      {sharpe:>6.2f}    {suggestion}')

print()

# 與你目前持倉比較
print('【與你目前持倉比較】')
print('=' * 70)

# 你目前的配置（簡化版）
your_portfolio = {
    '1101.TW': 0.25,  # 台泥
    '2352.TW': 0.20,  # 佳世達
    '2409.TW': 0.15,  # 友達
    '6919.TW': 0.10,  # 康霈
    'BOND': 0.30,     # 債券（假設平均報酬 3%，波動 8%）
}

# 計算你目前的投資組合表現
your_return = 0
your_volatility = 0

for ticker, weight in your_portfolio.items():
    if ticker in returns_data:
        your_return += weight * returns_data[ticker]['return']
        your_volatility += weight ** 2 * returns_data[ticker]['volatility'] ** 2

your_volatility = np.sqrt(your_volatility)
your_sharpe = your_return / your_volatility if your_volatility > 0 else 0

print(f'\n你目前的投資組合：')
print(f'預期年化報酬: {your_return*100:.2f}%')
print(f'預期年化波動: {your_volatility*100:.2f}%')
print(f'夏普比率: {your_sharpe:.3f}')
print()

print(f'最佳投資組合（最大夏普）：')
print(f'預期年化報酬: {results[1, max_sharpe_idx]*100:.2f}%')
print(f'預期年化波動: {results[0, max_sharpe_idx]*100:.2f}%')
print(f'夏普比率: {results[2, max_sharpe_idx]:.3f}')
print()

if results[2, max_sharpe_idx] > your_sharpe * 1.2:
    print('建議：你的投資組合可以透過資產配置優化提升效率')
    print(f'      夏普比率可從 {your_sharpe:.3f} 提升至 {results[2, max_sharpe_idx]:.3f}')
elif results[2, max_sharpe_idx] > your_sharpe:
    print('建議：你的投資組合還有小幅優化空間')
else:
    print('你的投資組合已經相當接近效率前緣')

print()
print('=' * 70)
print('投資組合優化分析完成')
print('=' * 70)
print()
print('重要提醒：')
print('• MPT 基於歷史數據，未來表現可能不同')
print('• 優化結果對輸入參數敏感，應定期重新計算')
print('• 實務上需考慮交易成本、稅務、流動性等因素')
print('• 建議搭配質化分析（產業前景、公司體質）使用')
