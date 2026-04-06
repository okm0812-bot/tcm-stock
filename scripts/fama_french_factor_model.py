# fama_french_factor_model.py
# Fama-French 三因子/五因子選股模型
# 分析股票的超額報酬來源：市場因子、規模因子、價值因子、獲利因子、投資因子

import yfinance as yf
import numpy as np
import pandas as pd
import sys
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print('=' * 70)
print('Fama-French 多因子選股模型')
print('Fama-French Three-Factor / Five-Factor Model')
print('=' * 70)
print(f'分析時間: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
print()

print('【模型說明】')
print('-' * 70)
print("""
Fama-French 模型認為股票報酬不僅來自市場風險，還來自其他因子：

三因子模型（1993）：
1. 市場因子 (Market Risk Premium): 承擔股市風險的報酬
2. 規模因子 (SMB - Small Minus Big): 小市值股票溢價
3. 價值因子 (HML - High Minus Low): 高淨值比（價值股）溢價

五因子模型（2015）新增：
4. 獲利因子 (RMW - Robust Minus Weak): 高獲利能力溢價
5. 投資因子 (CMA - Conservative Minus Aggressive): 保守投資溢價

應用：
• 分析股票報酬的來源
• 評估基金經理人的選股能力（Alpha）
• 建構因子投資策略
""")

# 分析標的
stocks = {
    '1101.TW': '台泥',
    '2352.TW': '佳世達',
    '2409.TW': '友達',
    '6919.TW': '康霈',
    '2330.TW': '台積電',  # 對照組
    '0050.TW': '元大台灣50',  # 大盤基準
}

print('【步驟 1】抓取股票數據計算因子暴露')
print('-' * 70)

factor_data = {}

for ticker, name in stocks.items():
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # 抓取 3 年歷史數據
        hist = stock.history(period='3y')
        
        if len(hist) < 200:
            print(f'{name:<12} 資料不足，跳過')
            continue
        
        # 計算日報酬率
        returns = hist['Close'].pct_change().dropna()
        
        # 抓取大盤（台灣加權指數，用 0050 代替）
        market = yf.Ticker('0050.TW')
        market_hist = market.history(period='3y')
        market_returns = market_hist['Close'].pct_change().dropna()
        
        # 對齊日期
        aligned_data = pd.concat([returns, market_returns], axis=1).dropna()
        aligned_data.columns = ['stock', 'market']
        
        # 計算 Beta（市場因子暴露）
        covariance = aligned_data['stock'].cov(aligned_data['market'])
        market_variance = aligned_data['market'].var()
        beta = covariance / market_variance if market_variance > 0 else 1
        
        # 計算 Alpha（超額報酬）
        stock_mean_return = aligned_data['stock'].mean() * 252
        market_mean_return = aligned_data['market'].mean() * 252
        risk_free_rate = 0.015  # 假設無風險利率 1.5%
        
        alpha = stock_mean_return - (risk_free_rate + beta * (market_mean_return - risk_free_rate))
        
        # 計算其他因子代理變數
        market_cap = info.get('marketCap', 0) / 1e8  # 億元
        
        # 淨值比 (P/B)
        pb_ratio = info.get('priceToBook', 0)
        
        # 本益比 (P/E)
        pe_ratio = info.get('trailingPE', 0)
        
        # ROE（獲利能力代理）
        roe = info.get('returnOnEquity', 0) * 100 if info.get('returnOnEquity') else 0
        
        # 年化波動率
        volatility = returns.std() * np.sqrt(252) * 100
        
        factor_data[ticker] = {
            'name': name,
            'beta': beta,
            'alpha': alpha,
            'market_cap': market_cap,
            'pb_ratio': pb_ratio,
            'pe_ratio': pe_ratio,
            'roe': roe,
            'volatility': volatility,
            'annual_return': stock_mean_return * 100
        }
        
        print(f'{name:<12} Beta: {beta:.2f}  Alpha: {alpha*100:>6.1f}%  市值: {market_cap:>8.0f}億')
        
    except Exception as e:
        print(f'{name:<12} 錯誤: {e}')

print()

# 因子分析
print('【步驟 2】因子暴露分析')
print('=' * 70)

print('\n1. 市場因子 (Beta)')
print('-' * 70)
print(f'{'股票':<12} {'Beta':<8} {'解讀':<40}')
print('-' * 70)

for ticker, data in factor_data.items():
    beta = data['beta']
    if beta > 1.2:
        interpretation = '高波動，大漲大跌'
    elif beta > 0.8:
        interpretation = '與大盤連動性高'
    elif beta > 0.5:
        interpretation = '低波動，防禦型'
    else:
        interpretation = '極低波動，與大盤脫鉤'
    
    print(f'{data["name"]:<12} {beta:<8.2f} {interpretation:<40}')

print()
print('2. 規模因子 (Size Factor)')
print('-' * 70)
print(f'{'股票':<12} {'市值':<12} {'規模分類':<15} {'預期溢價':<15}')
print('-' * 70)

# 計算市值中位數
market_caps = [d['market_cap'] for d in factor_data.values()]
median_cap = np.median(market_caps)

for ticker, data in factor_data.items():
    cap = data['market_cap']
    if cap > median_cap * 2:
        size_class = '大型股'
        premium = '低（規模溢價小）'
    elif cap > median_cap * 0.5:
        size_class = '中型股'
        premium = '中'
    else:
        size_class = '小型股'
        premium = '高（小市值溢價）'
    
    print(f'{data["name"]:<12} {cap:>10.0f}億 {size_class:<15} {premium:<15}')

print()
print('3. 價值因子 (Value Factor)')
print('-' * 70)
print(f'{'股票':<12} {'P/B':<8} {'P/E':<8} {'價值分類':<15} {'預期溢價':<15}')
print('-' * 70)

for ticker, data in factor_data.items():
    pb = data['pb_ratio']
    pe = data['pe_ratio']
    
    if pb > 0 and pb < 1:
        value_class = '深度價值股'
        premium = '高（價值溢價）'
    elif pb > 0 and pb < 2:
        value_class = '價值股'
        premium = '中高'
    elif pb > 0 and pb < 4:
        value_class = '合理價位'
        premium = '中'
    else:
        value_class = '成長股/昂貴'
        premium = '低（價值溢價小）'
    
    pe_str = f'{pe:.1f}' if pe > 0 else 'N/A'
    print(f'{data["name"]:<12} {pb:<8.2f} {pe_str:<8} {value_class:<15} {premium:<15}')

print()
print('4. 獲利因子 (Profitability Factor)')
print('-' * 70)
print(f'{'股票':<12} {'ROE':<8} {'獲利分類':<15} {'預期溢價':<15}')
print('-' * 70)

for ticker, data in factor_data.items():
    roe = data['roe']
    
    if roe > 15:
        profit_class = '高獲利'
        premium = '高（獲利溢價）'
    elif roe > 8:
        profit_class = '穩定獲利'
        premium = '中'
    elif roe > 0:
        profit_class = '低獲利'
        premium = '低'
    else:
        profit_class = '虧損'
        premium = '負面（避開）'
    
    roe_str = f'{roe:.1f}%' if roe != 0 else 'N/A'
    print(f'{data["name"]:<12} {roe_str:<8} {profit_class:<15} {premium:<15}')

print()

# 綜合評分
print('【步驟 3】Fama-French 綜合評分')
print('=' * 70)

print(f'{'股票':<12} {'市場':<8} {'規模':<8} {'價值':<8} {'獲利':<8} {'總分':<8} {'評級':<10}')
print('-' * 70)

for ticker, data in factor_data.items():
    # 市場因子評分 (Beta 接近 1 較好)
    market_score = max(0, 10 - abs(data['beta'] - 1) * 10)
    
    # 規模因子評分 (小市值較好，但不要太小)
    cap = data['market_cap']
    if cap > 1000:  # 大型股
        size_score = 5
    elif cap > 100:  # 中型股
        size_score = 8
    else:  # 小型股
        size_score = 7
    
    # 價值因子評分 (低 P/B 較好)
    pb = data['pb_ratio']
    if pb > 0 and pb < 1:
        value_score = 10
    elif pb > 0 and pb < 2:
        value_score = 8
    elif pb > 0 and pb < 4:
        value_score = 5
    else:
        value_score = 3
    
    # 獲利因子評分 (高 ROE 較好)
    roe = data['roe']
    if roe > 15:
        profit_score = 10
    elif roe > 8:
        profit_score = 7
    elif roe > 0:
        profit_score = 4
    else:
        profit_score = 0
    
    total_score = (market_score + size_score + value_score + profit_score) / 4
    
    if total_score >= 8:
        rating = 'A級'
    elif total_score >= 6:
        rating = 'B級'
    elif total_score >= 4:
        rating = 'C級'
    else:
        rating = 'D級'
    
    print(f'{data["name"]:<12} {market_score:<8.0f} {size_score:<8.0f} {value_score:<8.0f} {profit_score:<8.0f} {total_score:<8.1f} {rating:<10}')

print()

# 你的持股分析
print('【你的持股 Fama-French 分析】')
print('=' * 70)

your_stocks = ['1101.TW', '2352.TW', '2409.TW', '6919.TW']

print('\n優點：')
for ticker in your_stocks:
    if ticker in factor_data:
        data = factor_data[ticker]
        if data['pb_ratio'] > 0 and data['pb_ratio'] < 1.5:
            print(f'• {data["name"]}: P/B {data["pb_ratio"]:.2f}，具價值股特質')
        if data['market_cap'] < 1000:
            print(f'• {data["name"]}: 市值 {data["market_cap"]:.0f}億，具規模溢價潛力')

print('\n缺點：')
for ticker in your_stocks:
    if ticker in factor_data:
        data = factor_data[ticker]
        if data['roe'] < 5:
            print(f'• {data["name"]}: ROE {data["roe"]:.1f}%，獲利能力弱（獲利因子負面）')
        if data['beta'] > 1.3:
            print(f'• {data["name"]}: Beta {data["beta"]:.2f}，波動過高')

print()
print('=' * 70)
print('Fama-French 多因子分析完成')
print('=' * 70)
print()
print('應用建議：')
print('• 根據因子暴露調整投資組合（例如增加價值股比重）')
print('• 避免單一因子過度集中（例如全買高 Beta 股）')
print('• 長期持有高品質因子組合（低 P/B、高 ROE、小市值）')
print('• 定期檢視因子績效，因子輪動時調整配置')
