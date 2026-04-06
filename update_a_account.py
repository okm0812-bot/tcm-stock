# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 用戶提供的A帳戶資料（2026-04-01 00:04）
a_account = [
    {"name": "國泰20年美債 00687B", "shares": 11000, "avg_cost": 31.22, "price": 28.58, "market": 314256, "cost": 343456, "pnl": -29200, "pct": -8.50},
    {"name": "中信美國公債20年 00795B", "shares": 14000, "avg_cost": 29.89, "price": 27.73, "market": 388066, "cost": 418510, "pnl": -30444, "pct": -7.27},
    {"name": "永豐20年美公債", "shares": 5000, "avg_cost": 25.08, "price": 23.81, "market": 119005, "cost": 125468, "pnl": -6463, "pct": -5.15},
    {"name": "統一美債20年", "shares": 5000, "avg_cost": 14.96, "price": 13.91, "market": 69523, "cost": 74838, "pnl": -5315, "pct": -7.10},
    {"name": "群益ESG投等債20+", "shares": 8000, "avg_cost": 15.77, "price": 14.87, "market": 118918, "cost": 126126, "pnl": -7208, "pct": -5.71},
    {"name": "台泥 1101", "shares": 19000, "avg_cost": 34.56, "price": 23.00, "market": 435515, "cost": 656741, "pnl": -221226, "pct": -33.69},
    {"name": "佳世達 2352", "shares": 6000, "avg_cost": 51.33, "price": 22.75, "market": 136037, "cost": 307996, "pnl": -171959, "pct": -55.83},
    {"name": "友達 2409", "shares": 9000, "avg_cost": 16.20, "price": 14.50, "market": 130057, "cost": 145858, "pnl": -15801, "pct": -10.83},
    {"name": "康霈 6919", "shares": 300, "avg_cost": 102.36, "price": 86.30, "market": 25806, "cost": 30718, "pnl": -4912, "pct": -15.99},
]

# B帳戶資料（已記錄）
b_account = [
    {"name": "00687B 國泰20年美債", "shares": 9000, "avg_cost": 30.47, "price": 28.19, "market": 253710, "cost": 0, "pnl": 0, "pct": -6.39},
    {"name": "00751B 元大AAA至A公司債", "shares": 2000, "avg_cost": 34.24, "price": 31.45, "market": 62900, "cost": 0, "pnl": 0, "pct": -7.06},
    {"name": "00795B 中信美國公債20年", "shares": 58000, "avg_cost": 30.66, "price": 27.37, "market": 1587460, "cost": 0, "pnl": 0, "pct": -9.69},
    {"name": "00853B 統一美債10年Aa-A", "shares": 1000, "avg_cost": 28.52, "price": 27.56, "market": 27560, "cost": 0, "pnl": 0, "pct": -2.24},
    {"name": "00933B 國泰10Y+金融債", "shares": 2000, "avg_cost": 16.78, "price": 15.96, "market": 31920, "cost": 0, "pnl": 0, "pct": -3.78},
]

# A帳戶計算
a_total_market = sum(s["market"] for s in a_account)
a_total_cost = sum(s["cost"] for s in a_account)
a_total_pnl = sum(s["pnl"] for s in a_account)

# B帳戶計算
b_total_market = sum(s["market"] for s in b_account)
b_total_cost = 2183268  # 用戶提供

# 總計
grand_market = a_total_market + b_total_market
grand_cost = a_total_cost + b_total_cost
grand_pnl = a_total_pnl + (b_total_market - b_total_cost)
grand_pct = grand_pnl / grand_cost * 100

print("=" * 80)
print("A帳戶 + B帳戶 總資產（2026-04-01）")
print("=" * 80)

print("\n【A帳戶】")
print("-" * 80)
for s in a_account:
    print(f"{s['name']:<25} {s['shares']:>6,}股 @ {s['price']:>6.2f} = {s['market']:>10,}元 (成本 {s['cost']:>10,} / {s['pnl']:>10,}元)")

print(f"\n{'A帳戶合計':<25} {a_total_market:>10,}元 成本 {a_total_cost:>10,}元 虧損 {a_total_pnl:>10,}元 ({a_total_pnl/a_total_cost*100:.2f}%)")

print("\n【B帳戶】")
print("-" * 80)
for s in b_account:
    print(f"{s['name']:<25} {s['shares']:>6,}股 @ {s['price']:>6.2f} = {s['market']:>10,}元 ({s['pct']:.2f}%)")

print(f"\n{'B帳戶合計':<25} {b_total_market:>10,}元 成本 {b_total_cost:>10,}元")

print("\n" + "=" * 80)
print("【兩帳戶總資產】")
print("=" * 80)
print(f"A帳戶市值：{a_total_market:>15,} 元")
print(f"B帳戶市值：{b_total_market:>15,} 元")
print(f"總市值：    {grand_market:>15,} 元")
print()
print(f"A帳戶成本：{a_total_cost:>15,} 元")
print(f"B帳戶成本：{b_total_cost:>15,} 元")
print(f"總成本：    {grand_cost:>15,} 元")
print()
print(f"A帳戶虧損：{a_total_pnl:>15,} 元")
b_pnl = b_total_market - b_total_cost
print(f"B帳戶虧損：{b_pnl:>15,} 元")
print(f"總虧損：    {grand_pnl:>15,} 元 ({grand_pct:.2f}%)")

print("\n" + "=" * 80)
print("【驗證】")
print("=" * 80)
print(f"用戶提供的A帳戶總現值：1,737,183")
print(f"計算的A帳戶總現值：    {a_total_market:,}")
print(f"差距：                  {abs(a_total_market - 1737183):,} 元 ({(a_total_market - 1737183)/1737183*100:.2f}%)")

print()
print(f"用戶提供的A帳戶總成本：2,229,711")
print(f"計算的A帳戶總成本：    {a_total_cost:,}")
print(f"差距：                  {abs(a_total_cost - 2229711):,} 元")
