# -*- coding: utf-8 -*-
"""
先賣一半策略分析
"""
from datetime import datetime

print("\n" + "="*70)
print("【先賣一半策略分析】" + datetime.now().strftime('%Y-%m-%d %H:%M'))
print("="*70)

price = 23.15  # 現價
shares = 11000
cost = 53.78

# 計算
half_shares = shares // 2
sell_money = half_shares * price
remaining_value = half_shares * price
remaining_cost = half_shares * cost

print(f"""
現價: {price} 元
持股: {shares:,} 股
成本: {cost} 元

【方案：先賣一半】

賣出：
- 股數: {half_shares:,} 股
- 價格: {price} 元
- 回收: {sell_money:,.0f} 元
- 虧損: {sell_money - (half_shares * cost):,.0f} 元

剩下：
- 股數: {half_shares:,} 股
- 市值: {remaining_value:,.0f} 元
- 成本: {remaining_cost:,.0f} 元
- 帳面虧損: {remaining_value - remaining_cost:,.0f} 元

【優點】
1. 降低風險（一半先止血）
2. 保留機會（一半留著）
3. 心理平衡（不會後悔太多）
4. 成交容易（量較小）

【缺點】
1. 另一半仍承擔風險
2. 如果續跌，另一半也會虧
3. 如果反彈，可能後悔賣太少

【後續策略】

如果續跌（跌破 22.5 元）：
- 停損剩下的 {half_shares:,} 股
- 認列全部虧損

如果反彈（漲到 24 元以上）：
- 賣出剩下的 {half_shares:,} 股
- 減少部分虧損

【結論】

先賣一半是「折中方案」：

好處：
- 降低一半風險
- 心裡比較能接受
- 不會完全錯過反彈

壞處：
- 另一半仍有風險
- 仍要繼續關注
- 決定變得複雜

【CEO 建議】

如果你「真的很糾結」：
- 先賣一半是可以的
- 起碼降低一半風險
- 但另一半要設停損點

執行：
- 今天先賣 {half_shares:,} 股 @ {price}
- 設定停損：22.50 元
- 如果跌破，立即賣出剩下的一半
""")

print("\n" + "="*70)
print("【最終建議】")
print("="*70)

print("""
好的，先賣一半是合理的選擇！

執行：
1. 今天賣出 5,500 股 @ 23.15 元
2. 回收約 127,325 元
3. 剩下 5,500 股，設停損點 22.50 元

這樣：
- 降低一半風險
- 保留一半機會
- 心裡也比較能接受
""")

print("="*70)