# -*- coding: utf-8 -*-
"""
康霈、佳世達 賣出分析
"""
import yfinance as yf
from datetime import datetime

print("\n" + "="*70)
print(f"【賣出分析】{datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("="*70)

# 康霈 6919
print("\n【康霈 6919.TW】")
print("-"*70)
try:
    stock = yf.Ticker("6919.TW")
    info = stock.info
    
    price = info.get('regularMarketPrice', 0)
    high_52 = info.get('fiftyTwoWeekHigh', 0)
    low_52 = info.get('fiftyTwoWeekLow', 0)
    volume = info.get('regularMarketVolume', 0)
    avg_volume = info.get('averageVolume', 0)
    
    print(f"現價: {price} 元")
    print(f"52週高點: {high_52} 元（距離: {((high_52 - price) / high_52 * 100):.1f}%）")
    print(f"52週低點: {low_52} 元（距離: {((price - low_52) / low_52 * 100):.1f}%）")
    print(f"成交量: {volume:,}")
    print(f"均量: {avg_volume:,}")
    
    if volume > avg_volume * 1.5:
        print("量能: 放量（>1.5倍均量）⚠️")
    elif volume < avg_volume * 0.5:
        print("量能: 縮量（<0.5倍均量）")
    else:
        print("量能: 正常")
    
    # 技術面判斷
    print("\n【技術面判斷】")
    if price < low_52 * 1.2:
        print("  ✅ 接近52週低點，技術面支撐區")
    
    # 你的持股
    cost = 102.36
    shares = 300
    loss_pct = ((price - cost) / cost) * 100
    
    print(f"\n【你的持股】")
    print(f"  成本: {cost} 元")
    print(f"  現價: {price} 元")
    print(f"  虧損: {loss_pct:.2f}%")
    print(f"  市值: {price * shares:,.0f} 元（只剩 {shares} 股）")
    
    print(f"\n【賣出建議】")
    if shares <= 300:
        print("  🟡 觀望")
        print("  理由: 剩餘持股少（300股），影響不大")
        print("  策略: 等三期臨床結果，賭看看")
    
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*70)

# 佳世達 2352
print("\n【佳世達 2352.TW】")
print("-"*70)
try:
    stock = yf.Ticker("2352.TW")
    info = stock.info
    
    price = info.get('regularMarketPrice', 0)
    high_52 = info.get('fiftyTwoWeekHigh', 0)
    low_52 = info.get('fiftyTwoWeekLow', 0)
    volume = info.get('regularMarketVolume', 0)
    avg_volume = info.get('averageVolume', 0)
    pe = info.get('trailingPE', 0)
    debt = info.get('debtToEquity', 0)
    
    print(f"現價: {price} 元")
    print(f"52週高點: {high_52} 元（距離: {((high_52 - price) / high_52 * 100):.1f}%）")
    print(f"52週低點: {low_52} 元（距離: {((price - low_52) / low_52 * 100):.1f}%）")
    print(f"成交量: {volume:,}")
    print(f"均量: {avg_volume:,}")
    print(f"本益比: {pe:.2f}x")
    print(f"負債比: {debt:.2f}%")
    
    if volume > avg_volume * 1.5:
        print("量能: 放量（>1.5倍均量）⚠️")
    elif volume < avg_volume * 0.5:
        print("量能: 縮量（<0.5倍均量）")
    else:
        print("量能: 正常")
    
    # 技術面判斷
    print("\n【技術面判斷】")
    if price > low_52 * 1.05 and price < low_52 * 1.15:
        print("  ⚠️ 接近52週低點，但尚未破底")
    
    # 你的持股
    cost = 53.78
    shares = 11000
    loss_pct = ((price - cost) / cost) * 100
    market_value = price * shares
    
    print(f"\n【你的持股】")
    print(f"  成本: {cost} 元")
    print(f"  現價: {price} 元")
    print(f"  虧損: {loss_pct:.2f}%")
    print(f"  市值: {market_value:,.0f} 元（{shares:,} 股）")
    
    print(f"\n【賣出建議】")
    print("  🔴 建議停損")
    print("  理由:")
    print("    1. 虧損 -56%，嚴重套牢")
    print("    2. 負債比 138%，財務風險高")
    print("    3. 無護城河，代工毛利歸零")
    print("    4. DCF 估值雖低估，但基本面差")
    print(f"  預估回收: {market_value:,.0f} 元")
    
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*70)
print("【最終結論】")
print("="*70)
print("\n康霈 6919: 🟡 觀望（剩300股，影響小）")
print("佳世達 2352: 🔴 建議停損（虧損大、基本面差）")
print("\n" + "="*70)
