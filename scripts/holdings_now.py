# -*- coding: utf-8 -*-
"""
持股現價 09:05
"""
import yfinance as yf
from datetime import datetime

print("\n" + "="*60)
print(f"【持股現價】{datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("="*60)

stocks = [
    ("1101.TW", "台泥", 34.56, 19000),
    ("2352.TW", "佳世達", 53.78, 11000),
    ("2409.TW", "友達", 16.20, 9000),
    ("6919.TW", "康霈", 102.36, 300),
]

print(f"\n{'股票':<10} {'現價':>8} {'成本':>8} {'漲跌':>10} {'報酬率':>10} {'市值':>12}")
print("-"*70)

total_value = 0
total_cost = 0

for ticker, name, cost, shares in stocks:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('regularMarketPrice', 0)
        
        if price and price > 0:
            change_pct = ((price - cost) / cost) * 100
            market_value = price * shares
            cost_total = cost * shares
            
            total_value += market_value
            total_cost += cost_total
            
            change_str = f"{change_pct:+.2f}%"
            
            print(f"{name:<10} {price:>8.2f} {cost:>8.2f} {change_str:>10} {change_str:>10} {market_value:>12,.0f}")
    except:
        print(f"{name:<10} {'N/A':>8} {cost:>8.2f} {'N/A':>10} {'N/A':>10} {'N/A':>12}")

print("-"*70)

if total_value > 0:
    total_pl = total_value - total_cost
    total_pct = (total_pl / total_cost) * 100
    print(f"\n總市值: {total_value:,.0f} 元")
    print(f"總成本: {total_cost:,.0f} 元")
    print(f"總損益: {total_pl:+,.0f} 元 ({total_pct:+.2f}%)")

print("\n" + "="*60)
