# -*- coding: utf-8 -*-
"""債券ETF 完整修正計算"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("債券ETF 完整修正計算（2026/04/01 收盤）")
print("=" * 70)

# ==================== 正確現價（今日實際收盤）====================
prices = {
    "00687B": 28.48,   # 國泰20年美債
    "00795B": 27.63,   # 中信美國公債20年
    "00751B": 32.00,   # 元大AAA至A公司債
    "00853B": 28.02,   # 統一美債10年Aa-A
    "00933B": 16.15,   # 國泰10Y+金融債
}

# ==================== A帳戶（修正後）====================
a_account = [
    {"code": "00687B", "name": "國泰20年美債",       "shares": 11000, "cost": 31.22},
    {"code": "00795B", "name": "中信美國公債20年",   "shares": 14000, "cost": 29.89},
    {"code": "00751B", "name": "元大AAA至A公司債",   "shares":  5000, "cost": 25.08},
    {"code": "00853B", "name": "統一美債10年Aa-A",   "shares":  5000, "cost": 14.96},
    {"code": "00933B", "name": "群益ESG投等債20+",   "shares":  8000, "cost": 15.77},
]

# ==================== B帳戶 ====================
b_account = [
    {"code": "00687B", "name": "國泰20年美債",       "shares":  9000, "cost": 30.47},
    {"code": "00751B", "name": "元大AAA至A公司債",   "shares":  2000, "cost": 34.24},
    {"code": "00795B", "name": "中信美國公債20年",   "shares": 58000, "cost": 30.66},
    {"code": "00853B", "name": "統一美債10年Aa-A",   "shares":  1000, "cost": 28.52},
    {"code": "00933B", "name": "國泰10Y+金融債",     "shares":  2000, "cost": 16.78},
]

def calc_account(name, holdings):
    print(f"\n【{name} 債券ETF】")
    print("-" * 70)
    total_value = 0
    total_cost = 0
    for h in holdings:
        price = prices[h["code"]]
        value = price * h["shares"]
        cost_total = h["cost"] * h["shares"]
        pnl = value - cost_total
        pnl_pct = pnl / cost_total * 100
        total_value += value
        total_cost += cost_total
        status = "✅" if pnl >= 0 else "🔴"
        print(f"  {status} {h['name']} ({h['code']})")
        print(f"     {h['shares']:,}股 × 均價{h['cost']} → 現價{price} = 市值{value:,.0f}元  損益{pnl:+,.0f}元（{pnl_pct:+.2f}%）")
    print(f"\n  小計：市值 {total_value:,.0f} 元 | 成本 {total_cost:,.0f} 元 | 損益 {total_value-total_cost:+,.0f} 元（{(total_value-total_cost)/total_cost*100:+.2f}%）")
    return total_value, total_cost

a_val, a_cost = calc_account("A帳戶", a_account)
b_val, b_cost = calc_account("B帳戶", b_account)

total_val = a_val + b_val
total_cost = a_cost + b_cost
total_pnl = total_val - total_cost

print("\n" + "=" * 70)
print("【A+B 帳戶 債券ETF 總計（修正後）】")
print("=" * 70)
print(f"  A帳戶市值：{a_val:,.0f} 元  成本：{a_cost:,.0f} 元  損益：{a_val-a_cost:+,.0f} 元（{(a_val-a_cost)/a_cost*100:+.2f}%）")
print(f"  B帳戶市值：{b_val:,.0f} 元  成本：{b_cost:,.0f} 元  損益：{b_val-b_cost:+,.0f} 元（{(b_val-b_cost)/b_cost*100:+.2f}%）")
print(f"  ─────────────────────────────────────────────────────")
print(f"  合計市值：{total_val:,.0f} 元")
print(f"  合計成本：{total_cost:,.0f} 元")
print(f"  合計損益：{total_pnl:+,.0f} 元（{total_pnl/total_cost*100:+.2f}%）")

# ==================== 加入股票部位 ====================
print("\n" + "=" * 70)
print("【全帳戶總資產（股票 + 債券）】")
print("=" * 70)

# A帳戶股票（記憶數據）
stock_a_value = 762120   # 台泥+佳世達+友達+康霈
stock_a_cost  = 1141128

# B帳戶無股票（全是債券ETF）
stock_b_value = 0
stock_b_cost  = 0

grand_value = total_val + stock_a_value
grand_cost  = total_cost + stock_a_cost
grand_pnl   = grand_value - grand_cost

print(f"\n  A帳戶股票：市值 {stock_a_value:,.0f} 元 | 成本 {stock_a_cost:,.0f} 元 | 損益 {stock_a_value-stock_a_cost:+,.0f} 元（{(stock_a_value-stock_a_cost)/stock_a_cost*100:+.2f}%）")
print(f"  A帳戶債券：市值 {a_val:,.0f} 元 | 成本 {a_cost:,.0f} 元 | 損益 {a_val-a_cost:+,.0f} 元（{(a_val-a_cost)/a_cost*100:+.2f}%）")
print(f"  B帳戶債券：市值 {b_val:,.0f} 元 | 成本 {b_cost:,.0f} 元 | 損益 {b_val-b_cost:+,.0f} 元（{(b_val-b_cost)/b_cost*100:+.2f}%）")
print(f"  ─────────────────────────────────────────────────────")
print(f"  總市值：{grand_value:,.0f} 元")
print(f"  總成本：{grand_cost:,.0f} 元")
print(f"  總損益：{grand_pnl:+,.0f} 元（{grand_pnl/grand_cost*100:+.2f}%）")

print("\n" + "=" * 70)
print("【反算驗證】✅")
print("=" * 70)
print(f"  A帳戶債券成本反算：")
for h in a_account:
    print(f"    {h['code']} {h['shares']:,}股 × {h['cost']} = {h['shares']*h['cost']:,.0f} 元")
print(f"  A帳戶債券成本合計：{a_cost:,.0f} 元")
