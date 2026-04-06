# -*- coding: utf-8 -*-
"""更新 A 帳戶正確資料並重新計算全帳戶"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("A 帳戶完整資料（用戶提供 2026/04/01）")
print("=" * 70)

# ==================== A 帳戶（用戶提供正確資料）====================
a_account = [
    # 債券 ETF
    {"code": "00687B", "name": "國泰20年美債",       "shares": 11000, "cost": 31.22, "price": 28.58, "value": 314256,  "cost_total": 343456,  "pnl": -29200,  "pnl_pct": -8.50,  "type": "債券"},
    {"code": "00795B", "name": "中信美國公債20年",   "shares": 14000, "cost": 29.89, "price": 27.73, "value": 388066,  "cost_total": 418510,  "pnl": -30444,  "pnl_pct": -7.27,  "type": "債券"},
    {"code": "00751B", "name": "永豐20年美公債",     "shares":  5000, "cost": 25.08, "price": 23.81, "value": 119005,  "cost_total": 125468,  "pnl":  -6463,  "pnl_pct": -5.15,  "type": "債券"},
    {"code": "00853B", "name": "統一美債20年",       "shares":  5000, "cost": 14.96, "price": 13.91, "value":  69523,  "cost_total":  74838,  "pnl":  -5315,  "pnl_pct": -7.10,  "type": "債券"},
    {"code": "00933B", "name": "群益ESG投等債20+",   "shares":  8000, "cost": 15.77, "price": 14.87, "value": 118918,  "cost_total": 126126,  "pnl":  -7208,  "pnl_pct": -5.71,  "type": "債券"},
    # 股票
    {"code": "1101",   "name": "台泥",               "shares": 19000, "cost": 34.56, "price": 23.00, "value": 435515,  "cost_total": 656741,  "pnl": -221226, "pnl_pct": -33.69, "type": "股票"},
    {"code": "2352",   "name": "佳世達",             "shares":  6000, "cost": 51.33, "price": 22.75, "value": 136037,  "cost_total": 307996,  "pnl": -171959, "pnl_pct": -55.83, "type": "股票"},
    {"code": "2409",   "name": "友達",               "shares":  9000, "cost": 16.20, "price": 14.50, "value": 130057,  "cost_total": 145858,  "pnl":  -15801, "pnl_pct": -10.83, "type": "股票"},
    {"code": "6919",   "name": "康霈",               "shares":   300, "cost":102.36, "price": 86.30, "value":  25806,  "cost_total":  30718,  "pnl":   -4912, "pnl_pct": -15.99, "type": "股票"},
]

# ==================== 顯示 A 帳戶 ====================
print("\n【A 帳戶 - 債券 ETF】")
print("-" * 70)
a_bond_val = a_bond_cost = a_bond_pnl = 0
for h in a_account:
    if h["type"] == "債券":
        a_bond_val  += h["value"]
        a_bond_cost += h["cost_total"]
        a_bond_pnl  += h["pnl"]
        print(f"  🔴 {h['name']} ({h['code']})  {h['shares']:,}股  均價{h['cost']}→現價{h['price']}  市值{h['value']:,}  損益{h['pnl']:+,}（{h['pnl_pct']:+.2f}%）")
print(f"\n  債券小計：市值 {a_bond_val:,} | 成本 {a_bond_cost:,} | 損益 {a_bond_pnl:+,}（{a_bond_pnl/a_bond_cost*100:+.2f}%）")

print("\n【A 帳戶 - 股票】")
print("-" * 70)
a_stock_val = a_stock_cost = a_stock_pnl = 0
for h in a_account:
    if h["type"] == "股票":
        a_stock_val  += h["value"]
        a_stock_cost += h["cost_total"]
        a_stock_pnl  += h["pnl"]
        print(f"  🔴 {h['name']} ({h['code']})  {h['shares']:,}股  均價{h['cost']}→現價{h['price']}  市值{h['value']:,}  損益{h['pnl']:+,}（{h['pnl_pct']:+.2f}%）")
print(f"\n  股票小計：市值 {a_stock_val:,} | 成本 {a_stock_cost:,} | 損益 {a_stock_pnl:+,}（{a_stock_pnl/a_stock_cost*100:+.2f}%）")

a_total_val  = a_bond_val  + a_stock_val
a_total_cost = a_bond_cost + a_stock_cost
a_total_pnl  = a_bond_pnl  + a_stock_pnl
print(f"\n  A帳戶合計：市值 {a_total_val:,} | 成本 {a_total_cost:,} | 損益 {a_total_pnl:+,}（{a_total_pnl/a_total_cost*100:+.2f}%）")
print(f"  ✅ 用戶提供總損益：-492,528（-22.09%）→ 計算值：{a_total_pnl:+,}（{a_total_pnl/a_total_cost*100:+.2f}%）")

# ==================== B 帳戶（現價用今日實際收盤）====================
b_account = [
    {"code": "00687B", "name": "國泰20年美債",       "shares":  9000, "cost": 30.47, "price": 28.48, "type": "債券"},
    {"code": "00751B", "name": "元大AAA至A公司債",   "shares":  2000, "cost": 34.24, "price": 32.00, "type": "債券"},
    {"code": "00795B", "name": "中信美國公債20年",   "shares": 58000, "cost": 30.66, "price": 27.63, "type": "債券"},
    {"code": "00853B", "name": "統一美債10年Aa-A",   "shares":  1000, "cost": 28.52, "price": 28.02, "type": "債券"},
    {"code": "00933B", "name": "國泰10Y+金融債",     "shares":  2000, "cost": 16.78, "price": 16.15, "type": "債券"},
]

print("\n\n【B 帳戶 - 債券 ETF】")
print("-" * 70)
b_total_val = b_total_cost = b_total_pnl = 0
for h in b_account:
    val  = h["price"] * h["shares"]
    cost = h["cost"]  * h["shares"]
    pnl  = val - cost
    pnl_pct = pnl / cost * 100
    b_total_val  += val
    b_total_cost += cost
    b_total_pnl  += pnl
    icon = "✅" if pnl >= 0 else "🔴"
    print(f"  {icon} {h['name']} ({h['code']})  {h['shares']:,}股  均價{h['cost']}→現價{h['price']}  市值{val:,.0f}  損益{pnl:+,.0f}（{pnl_pct:+.2f}%）")
print(f"\n  B帳戶合計：市值 {b_total_val:,.0f} | 成本 {b_total_cost:,.0f} | 損益 {b_total_pnl:+,.0f}（{b_total_pnl/b_total_cost*100:+.2f}%）")

# ==================== 全帳戶總計 ====================
grand_val  = a_total_val  + b_total_val
grand_cost = a_total_cost + b_total_cost
grand_pnl  = a_total_pnl  + b_total_pnl

print("\n" + "=" * 70)
print("【全帳戶總資產（A + B）修正後】")
print("=" * 70)
print(f"  A帳戶（股票+債券）：市值 {a_total_val:,} | 成本 {a_total_cost:,} | 損益 {a_total_pnl:+,}（{a_total_pnl/a_total_cost*100:+.2f}%）")
print(f"  B帳戶（債券）：     市值 {b_total_val:,.0f} | 成本 {b_total_cost:,.0f} | 損益 {b_total_pnl:+,.0f}（{b_total_pnl/b_total_cost*100:+.2f}%）")
print(f"  ─────────────────────────────────────────────────────────────")
print(f"  總市值：{grand_val:,.0f} 元")
print(f"  總成本：{grand_cost:,.0f} 元")
print(f"  總損益：{grand_pnl:+,.0f} 元（{grand_pnl/grand_cost*100:+.2f}%）")

print("\n" + "=" * 70)
print("【注意】A帳戶數據為用戶提供（收盤前），B帳戶現價為今日收盤價")
print("=" * 70)
