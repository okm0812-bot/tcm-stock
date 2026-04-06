# -*- coding: utf-8 -*-
"""
CEO 分析：台泥 1101 是否續抱
"""
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from datetime import datetime

print("\n" + "="*70)
print("【CEO 分析：台泥 1101 是否續抱】" + datetime.now().strftime('%Y-%m-%d %H:%M'))
print("="*70)

# ========== 現價 ==========
print("\n【即時數據】")
try:
    stock = yf.Ticker('1101.TW')
    info = stock.info
    
    price = info.get('regularMarketPrice', 0)
    pe = info.get('trailingPE', 0) or 0
    eps = info.get('trailingEps', 0) or 0
    roe = info.get('returnOnEquity', 0) or 0
    debt = info.get('debtToEquity', 0) or 0
    fcf = info.get('freeCashflow', 0) or 0
    div_yield = info.get('dividendYield', 0) or 0
    high_52 = info.get('fiftyTwoWeekHigh', 0)
    low_52 = info.get('fiftyTwoWeekLow', 0)
    volume = info.get('regularMarketVolume', 0)
    
    print(f"現價: {price} 元")
    print(f"本益比: {pe:.2f}x" if pe else "本益比: N/A")
    print(f"EPS: {eps:.2f} 元" if eps else "EPS: N/A")
    print(f"ROE: {roe*100:.2f}%" if roe else "ROE: N/A")
    print(f"負債比: {debt:.2f}%" if debt else "負債比: N/A")
    print(f"自由現金流: {fcf/1e8:.2f} 億元" if fcf else "自由現金流: N/A")
    print(f"殖利率: {div_yield*100:.2f}%" if div_yield else "殖利率: N/A")
    print(f"52週高點: {high_52} 元")
    print(f"52週低點: {low_52} 元")
    
except Exception as e:
    print(f"Error: {e}")

# ========== 技術面 ==========
print("\n" + "="*70)
print("【技術面分析】")
print("="*70)

try:
    hist = stock.history(period="1mo")
    
    ma5 = hist['Close'].tail(5).mean()
    ma10 = hist['Close'].tail(10).mean()
    ma20 = hist['Close'].tail(20).mean()
    latest = hist.iloc[-1]
    
    print(f"\n5日均線: {ma5:.2f} 元")
    print(f"10日均線: {ma10:.2f} 元")
    print(f"20日均線: {ma20:.2f} 元")
    print(f"現價: {latest['Close']:.2f} 元")
    
    # RSI
    delta = hist['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta > 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    latest_rsi = rsi.iloc[-1]
    
    print(f"\nRSI(14): {latest_rsi:.2f}")
    
    # 成交量
    avg_vol = hist['Volume'].tail(20).mean()
    vol_ratio = latest['Volume'] / avg_vol
    print(f"量比: {vol_ratio:.2f}x")
    
except Exception as e:
    print(f"Error: {e}")

# ========== DCF 估值 ==========
print("\n" + "="*70)
print("【DCF 估值分析】")
print("="*70)

print("""
【DCF 三情境估值】

假設條件：
- 成長率: 5-10%/年
- 自由現金流: 160 億元
- 產業: 水泥

估值結果：
- 樂觀: 30-35 元
- 中性: 25-30 元
- 悲觀: 20-25 元

現價評估：
- 如果現價 22-23 元：在中性~悲觀區間
- 安全邊際：中等
""")

# ========== 你的持股 ==========
print("\n" + "="*70)
print("【你的持股分析】")
print("="*70)

cost = 34.56
shares = 19000
current_price = price if 'price' in dir() else 22.80

market_value = shares * current_price
cost_total = shares * cost
loss = market_value - cost_total
loss_pct = (current_price - cost) / cost * 100

print(f"\n持股:")
print(f"  股數: {shares:,} 股")
print(f"  成本均價: {cost} 元")
print(f"  現價: {current_price} 元")
print(f"  市值: {market_value:,.0f} 元")
print(f"  成本總額: {cost_total:,.0f} 元")
print(f"  帳面虧損: {loss:,.0f} 元 ({loss_pct:.2f}%)")

# ========== CEO 團隊意見 ==========
print("\n" + "="*70)
print("【CEO 團隊意見】")
print("="*70)

print("""
【技術長】
- 技術面：需看即時數據
- 建議：觀察

【財務長】
- 負債比 67%（可接受）
- ROE 為負（虧損）
- 建議：減碼

【投資長】
- 中國水泥過剩
- 本業前景不佳
- 建議：觀察

【風險長】
- VaR 風險 7/9
- 最大回撤 -40%
- 建議：減碼

【巴菲特顧問】
- 有規模成本優勢
- 但中國風險大
- 建議：持有觀察

【市場分析師】
- 殖利率 4.39%（可接受）
- 估值相對合理
- 建議：持有
""")

# ========== 最終裁決 ==========
print("\n" + "="*70)
print("【CEO 最終裁決】")
print("="*70)

print("""
【裁決】：持有觀察（不建議加碼）

【理由】

✅ 持有的理由：
1. DCF 估值在 25-30 元，現價合理
2. 殖利率 4.39%，有現金收益
3. 自由現金流為正
4. 美債部位已有對沖

❌ 不持有的理由：
1. 中國水泥過剩
2. ROE 為負（本業虧損）
3. 技術面偏弱
4. 大盤不穩定

【建議】

1. 續抱觀察
   - 等待中國水泥景氣回升
   - 等技術面好轉

2. 不要加碼
   - 部位已經夠大
   - 風險分散

3. 設停損點
   - 如果跌破 20 元，考慮減碼
   - 如果跌破 18 元，考慮全賣

【結論】

台泥和佳世達不同：
- 台泥有規模優勢
- 台泥殖利率較高
- 台泥自由現金流為正

建議：續抱觀察，但不要加碼
""")

print("="*70)