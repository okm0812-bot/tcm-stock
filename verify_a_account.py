# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("A帳戶資料驗證")
print("=" * 80)

# A帳戶股票（用戶提供）
stocks = [
    ("國泰20年美債 00687B", 11000, 31.22, 28.58, -29200),
    ("中信美國公債20年 00795B", 14000, 29.89, 27.73, -30444),
    ("永豐20年美公債", 5000, 25.08, 23.81, -6463),
    ("統一美債20年", 5000, 14.96, 13.91, -5315),
    ("群益ESG投等債20+", 8000, 15.77, 14.87, -7208),
    ("台泥 1101", 19000, 34.56, 23.00, -221226),
    ("佳世達 2352", 6000, 51.33, 22.75, -171959),
    ("友達 2409", 9000, 16.20, 14.50, -15801),
    ("康霈 6919", 300, 102.36, 86.30, -4912),
]

print("\n【驗證計算】")
print("-" * 80)
print(f"{'名稱':<25} {'股數':>8} {'均價':>8} {'現價':>8} {'驗證市值':>12} {'用戶市值':>12} {'驗證':>6}")
print("-" * 80)

total_market = 0
total_cost = 0
total_pnl = 0

for name, shares, avg_cost, price, pnl_user in stocks:
    market = shares * price
    cost = shares * avg_cost
    pnl = cost - market
    total_market += market
    total_cost += cost
    total_pnl += pnl
    
    # 驗證
    pnl_check = abs(pnl - abs(pnl_user)) < 10  # 差距10元以內
    market_check = abs(market - pnl_user - cost) < 10
    check = "✅" if pnl_check else "❌"
    
    print(f"{name:<25} {shares:>8,} {avg_cost:>8.2f} {price:>8.2f} {market:>12,.0f} {pnl_user:>12,.0f} {check:>6}")

print("-" * 80)
print(f"{'合計':<25} {'':>8} {'':>8} {'':>8} {total_market:>12,.0f} {total_pnl:>12,.0f}")
print()

# 用戶提供的數字
print("【用戶提供的數字】")
print(f"總現值：1,737,183")
print(f"總成本：2,229,711")
print(f"總損益：-492,528")
print(f"總報酬率：-22.09%")

print()
print("【計算結果】")
print(f"總現值：{total_market:,.0f}")
print(f"總成本：{total_cost:,.0f}")
print(f"總損益：{total_pnl:,.0f}")
print(f"總報酬率：{total_pnl/total_cost*100:.2f}%")

print()
print("【差距】")
print(f"現值差距：{total_market - 1737183:,} 元")
print(f"成本差距：{total_cost - 2229711:,} 元")
print(f"損益差距：{total_pnl - (-492528):,} 元")

# 重要發現：佳世達均價不同！
print()
print("=" * 80)
print("重要發現：佳世達均價不同！")
print("=" * 80)
print("舊記錄：均價 53.78，成本 322,680")
print("新資料：均價 51.33，成本 307,996")
print("差額：-14,684 元")
