# -*- coding: utf-8 -*-
"""
佳世達 分批賣出策略分析
"""
from datetime import datetime

print("\n" + "="*70)
print(f"【佳世達 2352 賣出策略分析】{datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("="*70)

# 持股資料
shares = 11000
cost = 53.78
price = 23.65
total_cost = shares * cost
market_value = shares * price
loss_pct = (price - cost) / cost * 100

print(f"\n【持股狀況】")
print(f"  總股數: {shares:,} 股")
print(f"  成本: {cost} 元")
print(f"  現價: {price} 元")
print(f"  總成本: {total_cost:,.0f} 元")
print(f"  目前市值: {market_value:,.0f} 元")
print(f"  帳面虧損: {market_value - total_cost:,.0f} 元 ({loss_pct:.2f}%)")

print("\n" + "="*70)
print("【方案 A：全部賣出（11,000 股）】")
print("="*70)

sell_all_value = shares * price
sell_all_loss = sell_all_value - total_cost

print(f"\n  賣出股數: {shares:,} 股")
print(f"  回收金額: {sell_all_value:,.0f} 元")
print(f"  實現虧損: {sell_all_loss:,.0f} 元 ({loss_pct:.2f}%)")

print("\n優點:")
print("  1. 一次性解決，不再糾結")
print("  2. 避免『越套越深』")
print("  3. 立即回收 26 萬現金")
print("  4. 心理負擔歸零")

print("\n缺點:")
print("  1. 虧損確定實現（-33 萬）")
print("  2. 若反彈會後悔")
print("  3. 賣壓可能影響成交價（量大）")

print("\n" + "="*70)
print("【方案 B：先賣一半（5,500 股）】")
print("="*70)

half_shares = shares // 2
sell_half_value = half_shares * price
remaining_shares = shares - half_shares
remaining_value = remaining_shares * price
remaining_cost = remaining_shares * cost

print(f"\n  第一次賣出: {half_shares:,} 股")
print(f"  回收金額: {sell_half_value:,.0f} 元")
print(f"  實現虧損: {sell_half_value - (total_cost/2):,.0f} 元")

print(f"\n  剩餘持股: {remaining_shares:,} 股")
print(f"  剩餘市值: {remaining_value:,.0f} 元")
print(f"  剩餘成本: {remaining_cost:,.0f} 元")

print("\n優點:")
print("  1. 降低風險（一半停損）")
print("  2. 保留反彈機會（一半留著）")
print("  3. 心理上『兩邊押注』，較不糾結")
print("  4. 成交較容易（量減半）")

print("\n缺點:")
print("  1. 若續跌，另一半也賠")
print("  2. 若反彈，可能後悔賣太少")
print("  3. 還要繼續關注這檔股票")

print("\n  後續策略:")
print("  - 若反彈至 24 元以上：賣出剩餘 5,500 股")
print("  - 若跌破 22.5 元：立即停損剩餘 5,500 股")

print("\n" + "="*70)
print("【方案 C：分三批賣出（3,700 + 3,700 + 3,600）】")
print("="*70)

batch1 = 3700
batch2 = 3700
batch3 = 3600

batch1_value = batch1 * price
batch2_value = batch2 * price
batch3_value = batch3 * price

print(f"\n  第一批: {batch1:,} 股 → 回收 {batch1_value:,.0f} 元")
print(f"  第二批: {batch2:,} 股 → 回收 {batch2_value:,.0f} 元")
print(f"  第三批: {batch3:,} 股 → 回收 {batch3_value:,.0f} 元")

print("\n優點:")
print("  1. 平均成本，分散風險")
print("  2. 減少『賣在最低點』的機率")

print("\n缺點:")
print("  1. 操作複雜")
print("  2. 若持續下跌，後兩批可能賣更低")
print("  3. 手續費增加")

print("\n" + "="*70)
print("【情境模擬】")
print("="*70)

scenarios = [
    ("續跌至 22 元", 22.0, "全部賣虧最少"),
    ("持平 23.65 元", 23.65, "差不多"),
    ("反彈至 25 元", 25.0, "先賣一半較好"),
    ("反彈至 27 元", 27.0, "不賣最好"),
]

print(f"\n{'情境':<20} {'全部賣':>15} {'先賣一半':>15} {'差異':>15}")
print("-"*70)

for scenario, target_price, note in scenarios:
    all_value = shares * target_price
    half_value = (half_shares * price) + (remaining_shares * target_price)
    diff = half_value - all_value
    
    print(f"{scenario:<20} {all_value:>15,.0f} {half_value:>15,.0f} {diff:>+15,.0f}")

print("\n" + "="*70)
print("【綜合評估】")
print("="*70)

print("\n技術面: 偏空（股價 < 5MA < 10MA）")
print("基本面: 差（負債比 138%、無護城河）")
print("量能: 縮量（買盤不足）")
print("風險: 若跌破 22.55 可能加速下跌")

print("\n" + "="*70)
print("【最終建議】")
print("="*70)

print("\n考慮因素:")
print("  1. 佳世達基本面差，長期趨勢偏空")
print("  2. 技術面尚未見底，反彈機會低")
print("  3. 虧損已重（-56%），再跌風險大")
print("  4. 心理負擔重，影響決策")

print("\n建議: 【先賣一半】")
print("\n理由:")
print("  1. 兩邊押注，心理較平衡")
print("  2. 降低風險（至少回收 13 萬）")
print("  3. 保留反彈機會（另一半留著）")
print("  4. 若跌破 22.5，另一半立即停損")

print("\n執行方式:")
print("  Step 1: 今日賣出 5,500 股 @ 23.65")
print("  Step 2: 設停損點 22.5 元（剩餘 5,500 股）")
print("  Step 3: 若反彈至 24 元以上，賣出剩餘")

print("\n" + "="*70)
