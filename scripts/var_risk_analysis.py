# var_risk_analysis.py
# VaR 風險價值 + 歷史回測計算系統
# 計算每檔股票的：VaR、Sharpe Ratio、最大回撤、勝率

import yfinance as yf
import numpy as np
import pandas as pd
import sys
from datetime import datetime, timedelta

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def calculate_var(returns, confidence=0.95):
    """計算 VaR (Value at Risk)"""
    return np.percentile(returns, (1 - confidence) * 100)

def calculate_sharpe(returns, risk_free_rate=0.02):
    """計算夏普比率"""
    if len(returns) == 0 or returns.std() == 0:
        return 0
    excess_returns = returns - risk_free_rate / 252
    return np.sqrt(252) * excess_returns.mean() / returns.std()

def calculate_max_drawdown(prices):
    """計算最大回撤"""
    peak = prices.expanding().max()
    drawdown = (prices - peak) / peak
    return drawdown.min() * 100

def calculate_win_rate(returns):
    """計算勝率"""
    if len(returns) == 0:
        return 0
    wins = (returns > 0).sum()
    return wins / len(returns) * 100

def calculate_volatility(returns):
    """計算年化波動率"""
    if len(returns) == 0:
        return 0
    return returns.std() * np.sqrt(252) * 100

def analyze_stock_risk(ticker, name, buy_price=None, shares=0, period='2y'):
    """分析個股風險"""
    print()
    print("=" * 60)
    print(f"  [風險分析] {name} ({ticker})")
    print("=" * 60)
    
    try:
        # 抓取歷史數據
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        
        if len(hist) < 60:  # 需要至少60天數據
            print(f"  數據不足，無法計算風險指標")
            return None
        
        # 計算日報酬率
        returns = hist['Close'].pct_change().dropna()
        
        # 基本風險指標
        current_price = hist['Close'].iloc[-1]
        var_95 = calculate_var(returns, 0.95)
        var_99 = calculate_var(returns, 0.99)
        sharpe = calculate_sharpe(returns)
        volatility = calculate_volatility(returns)
        max_dd = calculate_max_drawdown(hist['Close'])
        win_rate = calculate_win_rate(returns)
        
        # 計算持有期間報酬（假設持有）
        if buy_price:
            holding_return = (current_price - buy_price) / buy_price * 100
            days_held = (datetime.now() - datetime.now().replace(day=1)).days or 30
            annualized_return = holding_return * (365 / max(days_held, 1))
        
        print()
        print(f"  【風險指標】")
        print(f"    VaR (95%): {var_95*100:.2f}%")
        print(f"      → 單日最大虧損有5%機率超過 {abs(var_95)*100:.2f}%")
        print(f"    VaR (99%): {var_99*100:.2f}%")
        print(f"      → 單日最大虧損有1%機率超過 {abs(var_99)*100:.2f}%")
        print()
        print(f"  【績效指標】")
        print(f"    年化波動率: {volatility:.2f}%")
        print(f"    夏普比率: {sharpe:.3f}")
        print(f"      → {'優秀 (>1.0)' if sharpe > 1 else '普通 (0.5-1.0)' if sharpe > 0.5 else '較差 (<0.5)'}")
        print(f"    最大回撤: {max_dd:.2f}%")
        print(f"      → 過去2年最大跌幅 {abs(max_dd):.2f}%")
        print(f"    日勝率: {win_rate:.1f}%")
        print(f"      → {'勝率佳 (>55%)' if win_rate > 55 else '普通 (45-55%)' if win_rate > 45 else '勝率低 (<45%)'}")
        print()
        
        if buy_price:
            holding_return = (current_price - buy_price) / buy_price * 100
            print(f"  【持有分析】")
            print(f"    買入成本: {buy_price:.2f} 元")
            print(f"    目前價格: {current_price:.2f} 元")
            print(f"    持有損益: {holding_return:+.2f}%")
            print(f"      → {'▲ 獲利' if holding_return > 0 else '▼ 虧損'}")
            
            # 計算 VaR 金額（以持有股數計算）
            position_value = buy_price * shares
            var_amount = position_value * abs(var_95)
            print()
            print(f"  【風險金額】")
            print(f"    持有市值: {position_value:,.0f} 元")
            print(f"    VaR (95%) 金額: {var_amount:,.0f} 元")
            print(f"      → 在正常市況下，有5%機率單日虧損超過 {var_amount:,.0f} 元")
        
        # 風險評級
        print()
        print(f"  【風險評級】")
        risk_score = 0
        if abs(max_dd) > 30: risk_score += 3
        elif abs(max_dd) > 20: risk_score += 2
        elif abs(max_dd) > 10: risk_score += 1
        
        if volatility > 30: risk_score += 3
        elif volatility > 20: risk_score += 2
        elif volatility > 10: risk_score += 1
        
        if sharpe < 0: risk_score += 2
        elif sharpe < 0.5: risk_score += 1
        
        if risk_score >= 7:
            risk_level = "🔴 極高風險"
        elif risk_score >= 5:
            risk_level = "🟠 高風險"
        elif risk_score >= 3:
            risk_level = "🟡 中等風險"
        else:
            risk_level = "🟢 低風險"
        
        print(f"    綜合風險評級: {risk_level}")
        print(f"    風險分數: {risk_score}/9")
        
        return {
            'name': name,
            'ticker': ticker,
            'var_95': var_95,
            'var_99': var_99,
            'sharpe': sharpe,
            'volatility': volatility,
            'max_drawdown': max_dd,
            'win_rate': win_rate,
            'risk_score': risk_score,
            'current_price': current_price
        }
        
    except Exception as e:
        print(f"  計算錯誤: {e}")
        return None

# ============================================================
# 主程式
# ============================================================
print("=" * 60)
print("  [系統] VaR 風險價值 + 歷史回測分析")
print("=" * 60)
print(f"  分析時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 你的持倉
portfolio = [
    {"name": "鴻海", "ticker": "2317.TW", "buy_price": 200.5, "shares": 0},
    {"name": "台泥", "ticker": "1101.TW", "buy_price": 34.56, "shares": 19000},
    {"name": "佳世達", "ticker": "2352.TW", "buy_price": 53.78, "shares": 11000},
    {"name": "友達", "ticker": "2409.TW", "buy_price": 16.20, "shares": 9000},
    {"name": "康霈", "ticker": "6919.TW", "buy_price": 102.36, "shares": 300},
]

results = []
for stock in portfolio:
    result = analyze_stock_risk(stock["ticker"], stock["name"], 
                                 stock["buy_price"], stock["shares"])
    if result:
        results.append(result)

# 風險排名
print()
print("=" * 60)
print("  [風險排名] 從最危險到最安全")
print("=" * 60)
results_sorted = sorted(results, key=lambda x: x['risk_score'], reverse=True)
for i, r in enumerate(results_sorted, 1):
    print(f"  {i}. {r['name']}: 風險分數 {r['risk_score']}/9, VaR(95%) {abs(r['var_95'])*100:.2f}%")

print()
print("=" * 60)
print(f"  分析完成")
print("=" * 60)
