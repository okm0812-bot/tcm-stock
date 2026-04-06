# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("A 帳戶完整資料（用戶提供 2026/04/01 收盤後）")
print("=" * 70)

# ==================== A 帳戶（收盤後正確資料）====================
a_account = [
    # 債券 ETF
    {"code": "00687B", "name": "國泰20年美債",       "shares": 11000, "cost": 31.22, "price": 28.48, "value": 313157,  "cost_total": 343456,  "pnl": -30299, "pnl_pct": -8.82,  "type": "債券"},
    {"code": "00795B", "name": "中信美國公債20年",   "shares": 14000, "cost": 29.89, "price": 27.63, "value": 386666,  "cost_total": 418510,  "pnl": -31844, "pnl_pct": -7.61,  "type": "債券"},
    {"code": "00857B", "name": "永豐20年美公債",     "shares":  5000, "cost": 25.08, "price": 23.71, "value": 118505,  "cost_total": 125468,  "pnl":  -6963, "pnl_pct": -5.55,  "type": "債券"},
    {"code": "00853B", "name": "統一美債20年",       "shares":  5000, "cost": 14.96, "price": 13.86, "value":  69273,  "cost_total":  74838,  "pnl":  -5565, "pnl_pct": -7.44,  "type": "債券"},
    {"code": "00933B", "name": "群益ESG投等債20+",   "shares":  8000, "cost": 15.77, "price": 14.93, "value": 119398,  "cost_total": 126126,  "pnl":  -6728, "pnl_pct": -5.33,  "type": "債券"},
    # 股票
    {"code": "1101",   "name": "台泥",               "shares": 19000, "cost": 34.56, "price": 23.70, "value": 448771,  "cost_total": 656741,  "pnl": -207970, "pnl_pct": -31.67, "type": "股票"},
    {"code": "2352",   "name": "佳世達",             "shares":  6000, "cost": 51.33, "price": 23.30, "value": 139326,  "cost_total": 307996,  "pnl": -168670, "pnl_pct": -54.76, "type": "股票"},
    {"code": "2409",   "name": "友達",               "shares":  9000, "cost": 16.20, "price": 15.95, "value": 143063,  "cost_total": 145858,  "pnl":   -2795, "pnl_pct":  -1.92, "type": "股票"},
    {"code": "6919",   "name": "康霈",               "shares":   300, "cost":102.36, "price": 94.90, "value":  28377,  "cost_total":  30718,  "pnl":   -2341, "pnl_pct":  -7.62, "type": "股票"},
]

# ==================== 顯示 ====================
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

# 驗證
user_val  = 1766536
user_pnl  = -463175
user_cost = 2229711
user_pct  = -20.77
print(f"\n  ── 驗證 ──")
print(f"  用戶提供：現值 {user_val:,} | 成本 {user_cost:,} | 損益 {user_pnl:+,}（{user_pct}%）")
print(f"  計算結果：現值 {a_total_val:,} | 成本 {a_total_cost:,} | 損益 {a_total_pnl:+,}（{a_total_pnl/a_total_cost*100:+.2f}%）")
val_ok  = "✅" if abs(a_total_val  - user_val)  < 500 else "❌"
pnl_ok  = "✅" if abs(a_total_pnl  - user_pnl)  < 500 else "❌"
cost_ok = "✅" if abs(a_total_cost - user_cost) < 500 else "❌"
print(f"  現值 {val_ok} | 損益 {pnl_ok} | 成本 {cost_ok}")

# ==================== B 帳戶 ====================
b_account = [
    {"code": "00687B", "name": "國泰20年美債",       "shares":  9000, "cost": 30.47, "price": 28.48},
    {"code": "00751B", "name": "元大AAA至A公司債",   "shares":  2000, "cost": 34.24, "price": 32.00},
    {"code": "00795B", "name": "中信美國公債20年",   "shares": 58000, "cost": 30.66, "price": 27.63},
    {"code": "00853B", "name": "統一美債10年Aa-A",   "shares":  1000, "cost": 28.52, "price": 28.02},
    {"code": "00933B", "name": "國泰10Y+金融債",     "shares":  2000, "cost": 16.78, "price": 16.15},
]

print("\n\n【B 帳戶 - 債券 ETF】")
print("-" * 70)
b_val = b_cost = b_pnl = 0
for h in b_account:
    v = h["price"] * h["shares"]
    c = h["cost"]  * h["shares"]
    p = v - c
    b_val += v; b_cost += c; b_pnl += p
    icon = "✅" if p >= 0 else "🔴"
    print(f"  {icon} {h['name']} ({h['code']})  {h['shares']:,}股  均價{h['cost']}→現價{h['price']}  市值{v:,.0f}  損益{p:+,.0f}（{p/c*100:+.2f}%）")
print(f"\n  B帳戶合計：市值 {b_val:,.0f} | 成本 {b_cost:,.0f} | 損益 {b_pnl:+,.0f}（{b_pnl/b_cost*100:+.2f}%）")

# ==================== 全帳戶 ====================
grand_val  = a_total_val  + b_val
grand_cost = a_total_cost + b_cost
grand_pnl  = a_total_pnl  + b_pnl

print("\n" + "=" * 70)
print("【全帳戶總資產（A + B）最終版】")
print("=" * 70)
print(f"  A帳戶：市值 {a_total_val:,} | 成本 {a_total_cost:,} | 損益 {a_total_pnl:+,}（{a_total_pnl/a_total_cost*100:+.2f}%）")
print(f"  B帳戶：市值 {b_val:,.0f} | 成本 {b_cost:,.0f} | 損益 {b_pnl:+,.0f}（{b_pnl/b_cost*100:+.2f}%）")
print(f"  ─────────────────────────────────────────────────────────────")
print(f"  總市值：{grand_val:,.0f} 元")
print(f"  總成本：{grand_cost:,.0f} 元")
print(f"  總損益：{grand_pnl:+,.0f} 元（{grand_pnl/grand_cost*100:+.2f}%）")
print("=" * 70)
