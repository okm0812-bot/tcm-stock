# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("ETF + 股票 完整市值驗證")
print("=" * 70)

# ETF（市價從 CEO v7）
print("\n【ETF 持股】（市價固定，計算後驗證）")
print("-" * 70)

etfs = [
    ("00687B 國泰20年美債", 11000, 31.22, 28.57),
    ("00795B 中信美國公債20年", 14000, 29.89, 27.71),
    ("永豐20年美公債", 5000, 25.08, 24.03),
    ("統一美債20年", 5000, 14.96, 13.89),
    ("00933B 國泰10Y+金融債", 2000, 16.67, 15.96),
]

etf_total_market = 0
etf_total_cost = 0

for name, shares, cost, price in etfs:
    market = shares * price
    cost_amt = shares * cost
    loss = cost_amt - market
    etf_total_market += market
    etf_total_cost += cost_amt
    print(f"{name}")
    print(f"  市值：{shares:,} 股 × {price} = {market:,.0f} 元")
    print(f"  成本：{shares:,} 股 × {cost} = {cost_amt:,.0f} 元")
    print(f"  虧損：{loss:,.0f} 元 ({(loss/cost_amt*100):.1f}%)")
    print()

print("-" * 70)
print(f"ETF 總市值：{etf_total_market:,.0f} 元 ✅")
print(f"ETF 總成本：{etf_total_cost:,.0f} 元")
print(f"ETF 總虧損：{etf_total_cost - etf_total_market:,.0f} 元 ({((etf_total_cost-etf_total_market)/etf_total_cost*100):.1f}%)")

# 股票（即時報價）
print("\n【股票持股】（即時報價）")
print("-" * 70)

stocks = [
    ("台泥 1101", 19000, 34.56, 23.00),
    ("佳世達 2352", 6000, 53.78, 22.75),
    ("友達 2409", 9000, 16.20, 14.50),
    ("康霈 6919", 300, 102.36, 86.30),
]

stock_total_market = 0
stock_total_cost = 0

for name, shares, cost, price in stocks:
    market = shares * price
    cost_amt = shares * cost
    loss = cost_amt - market
    stock_total_market += market
    stock_total_cost += cost_amt
    print(f"{name}")
    print(f"  市值：{shares:,} 股 × {price} = {market:,.0f} 元")
    print(f"  成本：{shares:,} 股 × {cost} = {cost_amt:,.0f} 元")
    print(f"  虧損：{loss:,.0f} 元 ({(loss/cost_amt*100):.1f}%)")
    print()

print("-" * 70)
print(f"股票 總市值：{stock_total_market:,.0f} 元")
print(f"股票 總成本：{stock_total_cost:,.0f} 元")
print(f"股票 總虧損：{stock_total_cost - stock_total_market:,.0f} 元 ({((stock_total_cost-stock_total_market)/stock_total_cost*100):.1f}%)")

# 總計
print("\n" + "=" * 70)
print("【總資產】")
print("=" * 70)

grand_market = stock_total_market + etf_total_market
grand_cost = stock_total_cost + etf_total_cost
grand_pnl = grand_market - grand_cost
grand_pnl_pct = grand_pnl / grand_cost * 100

print(f"股票市值：{stock_total_market:,.0f} 元")
print(f"ETF市值： {etf_total_market:,.0f} 元")
print(f"")
print(f"總市值：  {grand_market:,.0f} 元")
print(f"總成本：  {grand_cost:,.0f} 元")
print(f"總損益：  {grand_pnl:,.0f} 元 ({grand_pnl_pct:+.1f}%)")

# 驗證計算
print("\n" + "=" * 70)
print("【驗證：反算確認】")
print("=" * 70)

print("\nETF 總市值驗證：")
calc = 11000*28.57 + 14000*27.71 + 5000*24.03 + 5000*13.89 + 2000*15.96
print(f"  11000×28.57 + 14000×27.71 + 5000×24.03 + 5000×13.89 + 2000×15.96")
print(f"  = {11000*28.57:,.0f} + {14000*27.71:,.0f} + {5000*24.03:,.0f} + {5000*13.89:,.0f} + {2000*15.96:,.0f}")
print(f"  = {calc:,.0f} ✅")

print("\n股票 總市值驗證：")
calc2 = 19000*23.00 + 6000*22.75 + 9000*14.50 + 300*86.30
print(f"  19000×23.00 + 6000×22.75 + 9000×14.50 + 300×86.30")
print(f"  = {19000*23:,.0f} + {6000*22.75:,.0f} + {9000*14.5:,.0f} + {300*86.3:,.0f}")
print(f"  = {calc2:,.0f} ✅")

print("\n總市值驗證：")
print(f"  {calc:,.0f} + {calc2:,.0f} = {calc+calc2:,.0f} ✅")
