# stock_analysis.py
# 個股即時分析 + DCF 估值系統 v1.0
# 使用方法: python stock_analysis.py

import yfinance as yf
import pandas as pd
import sys
from datetime import datetime

# 解決 Windows CMD 編碼問題
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def get_stock_info(ticker):
    """抓取個股資訊"""
    try:
        data = yf.Ticker(ticker)
        info = data.info
        return {
            'price': info.get('regularMarketPrice', 0),
            'pe': info.get('trailingPE', 0),
            'eps': info.get('trailingEps', 0),
            'dividend': info.get('dividendRate', 0),
            'market_cap': info.get('marketCap', 0),
            'name': info.get('shortName', ticker),
            'industry': info.get('industry', 'N/A'),
            '52w_high': info.get('fiftyTwoWeekHigh', 0),
            '52w_low': info.get('fiftyTwoWeekLow', 0),
            'volume': info.get('regularVolume', 0),
            'avg_volume': info.get('averageVolume', 0),
            'roe': info.get('returnOnEquity', 0),
            'debt_to_equity': info.get('debtToEquity', 0),
            'profit_margin': info.get('profitMargins', 0),
            'fcf': info.get('freeCashflow', 0),
        }
    except Exception as e:
        return None

def simple_dcf(fcf, growth_rate, discount_rate=0.10, terminal_growth=0.03, years=5):
    """
    簡化版 DCF 估值
    
    參數:
    - fcf: 當前自由現金流
    - growth_rate: 未來5年成長率 (如 0.15 = 15%)
    - discount_rate: 折現率 (預設 10%)
    - terminal_growth: 永續成長率 (預設 3%)
    - years: 預測年數 (預設 5年)
    
    返回: 每股內在價值
    """
    if not fcf or fcf <= 0:
        return None
    
    # 預測未來5年 FCF
    fcf_forecast = []
    for i in range(1, years + 1):
        fcf_forecast.append(fcf * (1 + growth_rate) ** i)
    
    # 折現計算
    pv_fcf = sum([fcf_forecast[i] / (1 + discount_rate) ** (i + 1) for i in range(years)])
    
    # 終值計算 (Gordon Growth Model)
    terminal_fcf = fcf_forecast[-1] * (1 + terminal_growth)
    terminal_value = terminal_fcf / (discount_rate - terminal_growth)
    pv_terminal = terminal_value / (1 + discount_rate) ** years
    
    # 企業價值
    enterprise_value = pv_fcf + pv_terminal
    
    return enterprise_value

def analyze_stock(name, ticker, buy_price=None, shares=0):
    """分析單一股票"""
    print()
    print("=" * 60)
    print(f"  [分析] {name} ({ticker})")
    print("=" * 60)
    
    info = get_stock_info(ticker)
    
    if not info:
        print(f"  無法取得資料")
        return None
    
    print()
    print(f"  基本資訊:")
    print(f"    產業: {info['industry']}")
    print(f"    現價: {info['price']:.2f} 元")
    print(f"    市值: {info['market_cap']/1e8:.2f} 億元" if info['market_cap'] else "    市值: N/A")
    print()
    print(f"  估值指標:")
    print(f"    本益比 (PE): {info['pe']:.2f}x" if info['pe'] else "    本益比 (PE): N/A")
    print(f"    EPS: {info['eps']:.2f} 元" if info['eps'] else "    EPS: N/A")
    print(f"    股利: {info['dividend']:.2f} 元" if info['dividend'] else "    股利: N/A")
    if info['dividend'] and info['price']:
        yield_rate = info['dividend'] / info['price'] * 100
        print(f"    殖利率: {yield_rate:.2f}%")
    print()
    print(f"  財務指標:")
    print(f"    ROE: {info['roe']*100:.2f}%" if info['roe'] else "    ROE: N/A")
    print(f"    負債比: {info['debt_to_equity']:.2f}%" if info['debt_to_equity'] else "    負債比: N/A")
    print(f"    利润率: {info['profit_margin']*100:.2f}%" if info['profit_margin'] else "    利润率: N/A")
    print(f"    自由現金流: {info['fcf']/1e8:.2f} 億元" if info['fcf'] else "    自由現金流: N/A")
    print()
    print(f"  技術面:")
    print(f"    52週高點: {info['52w_high']:.2f} 元" if info['52w_high'] else "    52週高點: N/A")
    print(f"    52週低點: {info['52w_low']:.2f} 元" if info['52w_low'] else "    52週低點: N/A")
    if info['52w_high'] and info['price']:
        distance_from_high = (info['52w_high'] - info['price']) / info['52w_high'] * 100
        print(f"    距離高點: {distance_from_high:.2f}%")
    print()
    
    # 計算殖利率
    if buy_price and shares > 0:
        cost = buy_price * shares
        current_value = info['price'] * shares
        unrealized_pl = current_value - cost
        return_rate = (unrealized_pl / cost * 100) if cost > 0 else 0
        
        print(f"  你的持倉:")
        print(f"    股數: {shares:,} 股")
        print(f"    成本均價: {buy_price:.2f} 元")
        print(f"    成本總額: {cost:,.0f} 元")
        print(f"    目前市值: {current_value:,.0f} 元")
        print(f"    未實現損益: {unrealized_pl:+,.0f} 元 ({return_rate:+.2f}%)")
        
        if unrealized_pl < 0:
            print(f"    建議: 停損/觀望")
        else:
            print(f"    建議: 持有/考慮加碼")
    
    return info

# ============================================================
# 主程式
# ============================================================
print("=" * 60)
print("  [系統] 個股即時分析 + DCF 估值系統 v1.0")
print("=" * 60)
print(f"  分析時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 你的持倉分析
portfolio = [
    {"name": "鴻海", "ticker": "2317.TW", "buy_price": 200.5, "shares": 0},
    {"name": "台泥", "ticker": "1101.TW", "buy_price": 34.56, "shares": 19000},
    {"name": "佳世達", "ticker": "2352.TW", "buy_price": 53.78, "shares": 11000},
    {"name": "友達", "ticker": "2409.TW", "buy_price": 16.20, "shares": 9000},
    {"name": "康霈", "ticker": "6919.TW", "buy_price": 102.36, "shares": 300},
]

# 分析每一檔
for stock in portfolio:
    analyze_stock(stock["name"], stock["ticker"], stock["buy_price"], stock["shares"])

print()
print("=" * 60)
print("  [系統] 分析完成")
print("=" * 60)
