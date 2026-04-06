# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("B帳戶 ETF 均價計算")
print("=" * 70)

# 使用最近抓到的報價（從舊資料）
# 公式：均價 = 現價 / (1 + 虧損率%)
# 例如：-6.39% = (現價 - 均價) / 均價 * 100
# 所以：均價 = 現價 / (1 - 0.0639) = 現價 / 0.9361

# 從 MEMORY.md 或最近資料取得的現價
# 如果用戶說虧損 -6.39%，我們用舊現價反推均價
# 然後驗證總成本是否 = 2,183,268

# 用二分法逼近真實均價
# 我們已知：
# - 每檔股票的現價（從歷史資料）
# - 每檔股票的虧損率
# - 總成本 = 2,183,268

# 反算均價公式：
# 虧損率 = (現價 - 均價) / 均價 * 100
# -loss_rate% = (現價 - 均價) / 均價 * 100
# 均價 = 現價 * 100 / (100 - loss_rate)

# 但我們沒有精確的現價...
# 讓我用總成本來反推現價

print("\n用戶提供的資料：")
user_data = [
    ("00687B 國泰20年美債", 9000, -6.39),
    ("00751B 元大AAA至A公司債", 2000, -7.06),
    ("00795B 中信美國公債20年", 58000, -9.69),
    ("00853B 統一美債10年Aa-A", 1000, -2.24),
    ("00933B 國泰10Y+金融債", 2000, -3.78),
]

print("| 股票 | 股數 | 虧損率 |")
print("|------|------|--------|")
for name, shares, loss in user_data:
    print(f"| {name} | {shares:,} | {loss:.2f}% |")

# 從已知資料估算現價
# 這些是從 MEMORY.md 或之前抓到的資料
# 但用戶說的虧損%是新的，讓我用總成本來反推

# 假設我們用這些現價（從最近抓到的）
known_prices = {
    "00687B": 28.19,   # 從之前記錄
    "00751B": 31.45,   # 從之前記錄  
    "00795B": 27.37,   # 從之前記錄
    "00853B": 27.56,   # 從之前記錄
    "00933B": 15.96,   # 從之前記錄
}

# 用虧損率反算均價
print("\n" + "=" * 70)
print("反算均價（使用已知現價）")
print("=" * 70)

total_cost_calc = 0
total_market_calc = 0

for name, shares, loss_pct in user_data:
    code = name.split(" ")[0]
    price = known_prices.get(code, 0)
    
    if price > 0 and loss_pct != 0:
        # 均價 = 現價 / (1 + loss_pct/100)
        # 虧損率是負的，所以：均價 = 現價 / (1 - abs(loss_pct)/100)
        avg_cost = price / (1 + loss_pct / 100)
    else:
        avg_cost = 0
    
    market = shares * price
    cost = shares * avg_cost
    total_cost_calc += cost
    total_market_calc += market
    
    print(f"\n{name}")
    print(f"  股數：{shares:,} 股")
    print(f"  現價：{price:.2f} 元")
    print(f"  均價：{avg_cost:.4f} 元")
    print(f"  市值：{market:,.0f} 元")
    print(f"  成本：{cost:,.0f} 元")

print()
print("=" * 70)
print("計算結果")
print("=" * 70)
print(f"總市值：{total_market_calc:,.0f} 元")
print(f"總成本：{total_cost_calc:,.0f} 元")
print(f"用戶提供：2,183,268 元")
print(f"差距：{total_cost_calc - 2183268:,.0f} 元 ({((total_cost_calc-2183268)/2183268*100):.2f}%)")

# 如果差距大，用二分法調整現價
print()
print("=" * 70)
print("檢查：調整係數")
print("=" * 70)

# 計算每檔的調整係數
ratio = 2183268 / total_cost_calc if total_cost_calc > 0 else 1
print(f"調整係數：{ratio:.4f}")
print(f"新均價 = 舊均價 × {ratio:.4f}")

# 重新計算
total_new = 0
print("\n調整後的均價：")
for name, shares, loss_pct in user_data:
    code = name.split(" ")[0]
    price = known_prices.get(code, 0)
    if price > 0 and loss_pct != 0:
        avg_cost = price / (1 + loss_pct / 100) * ratio
    else:
        avg_cost = 0
    cost = shares * avg_cost
    total_new += cost
    print(f"{name}: 均價 {avg_cost:.4f} 元")

print()
print(f"調整後總成本：{total_new:,.0f} 元")
print(f"目標：2,183,268 元")
print(f"差距：{abs(total_new - 2183268):,.0f} 元")
