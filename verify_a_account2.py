# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 80)
print("A帳戶資料驗證（修正版）")
print("=" * 80)

# A帳戶股票（用戶提供）
stocks = [
    ("國泰20年美債 00687B", 11000, 31.22, 28.58, 314256, 343456, -29200, -8.50),
    ("中信美國公債20年 00795B", 14000, 29.89, 27.73, 388066, 418510, -30444, -7.27),
    ("永豐20年美公債", 5000, 25.08, 23.81, 119005, 125468, -6463, -5.15),
    ("統一美債20年", 5000, 14.96, 13.91, 69523, 74838, -5315, -7.10),
    ("群益ESG投等債20+", 8000, 15.77, 14.87, 118918, 126126, -7208, -5.71),
    ("台泥 1101", 19000, 34.56, 23.00, 435515, 656741, -221226, -33.69),
    ("佳世達 2352", 6000, 51.33, 22.75, 136037, 307996, -171959, -55.83),
    ("友達 2409", 9000, 16.20, 14.50, 130057, 145858, -15801, -10.83),
    ("康霈 6919", 300, 102.36, 86.30, 25806, 30718, -4912, -15.99),
]

print("\n【逐項驗證】")
print("-" * 80)

total_market_calc = 0
total_cost_calc = 0
total_pnl_calc = 0

for name, shares, avg_cost, price, market_user, cost_user, pnl_user, pct_user in stocks:
    # 驗證計算
    market_calc = shares * price
    cost_calc = shares * avg_cost
    pnl_calc = cost_calc - market_calc
    pnl_pct_calc = pnl_calc / cost_calc * 100
    
    total_market_calc += market_calc
    total_cost_calc += cost_calc
    total_pnl_calc += pnl_calc
    
    # 檢查
    market_ok = abs(market_calc - market_user) < 100
    cost_ok = abs(cost_calc - cost_user) < 100
    pnl_ok = abs(abs(pnl_calc) - abs(pnl_user)) < 100
    
    status = "✅" if (market_ok and cost_ok and pnl_ok) else "⚠️"
    
    print(f"\n{name}")
    print(f"  股數：{shares:,} 股")
    print(f"  均價：計算 {avg_cost:.2f} vs 用戶 {cost_user/shares:.2f} {status}")
    print(f"  現價：{price:.2f}")
    print(f"  市值：計算 {market_calc:,} vs 用戶 {market_user:,} {status}")
    print(f"  成本：計算 {cost_calc:,} vs 用戶 {cost_user:,} {status}")
    print(f"  虧損：計算 {pnl_calc:,.0f} vs 用戶 {pnl_user:,} {status}")
    print(f"  虧損%：計算 {pnl_pct_calc:.2f}% vs 用戶 {pct_user}% {status}")

print("\n" + "=" * 80)
print("【總計驗證】")
print("=" * 80)

pnl_pct_calc = total_pnl_calc / total_cost_calc * 100

print(f"總市值：計算 {total_market_calc:,} vs 用戶 1,737,183 → 差距 {total_market_calc - 1737183:,}")
print(f"總成本：計算 {total_cost_calc:,} vs 用戶 2,229,711 → 差距 {total_cost_calc - 2229711:,}")
print(f"總虧損：計算 {total_pnl_calc:,.0f} vs 用戶 -492,528 → 差距 {total_pnl_calc - (-492528):,}")
print(f"總虧損%：計算 {pnl_pct_calc:.2f}% vs 用戶 -22.09%")

print()
print("=" * 80)
print("【結論】")
print("=" * 80)
if abs(total_market_calc - 1737183) < 1000 and abs(total_cost_calc - 2229711) < 1000:
    print("✅ 資料驗證通過！與用戶提供的數字吻合")
else:
    print("❌ 有差距，需要檢查")

# 重要發現
print()
print("=" * 80)
print("【重要發現】")
print("=" * 80)
print("佳世達均價：53.78 → 51.33（已更新）")
print("這表示之前有交易記錄改變了均價")
print()
print("佳世達歷史：")
print("  原始買入：11,000 股 @ 53.78")
print("  2026-03-26：賣出 5,000 股 @ 24.05")
print("  2026-03-27：錯誤買入 1,000 股 @ 33.50（後來賣出）")
print("  2026-03-27：錯誤買入後賣出 1,000 股 @ 32.15")
print("  目前持有：6,000 股 @ 51.33")
