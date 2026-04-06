# -*- coding: utf-8 -*-
"""債券 ETF 分析 - A/B 帳戶"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

try:
    import yfinance as yf
except:
    yf = None

print("=" * 70)
print("債券 ETF 分析 - A/B 帳戶")
print("=" * 70)

# ==================== 持倉資料 ====================
bond_etfs = {
    "A帳戶": [
        {"code": "00687B.TW", "name": "國泰20年美債",     "shares": 11000, "cost": 31.22},
        {"code": "00795B.TW", "name": "中信美國公債20年", "shares": 14000, "cost": 29.89},
        {"code": "00751B.TW", "name": "永豐20年美公債",   "shares":  5000, "cost": 25.08},
        {"code": "00853B.TW", "name": "統一美債20年",     "shares":  5000, "cost": 14.96},
        {"code": "00933B.TW", "name": "群益ESG投等債20+", "shares":  8000, "cost": 15.77},
    ],
    "B帳戶": [
        {"code": "00687B.TW", "name": "國泰20年美債",     "shares":  9000, "cost": 30.47},
        {"code": "00751B.TW", "name": "元大AAA至A公司債", "shares":  2000, "cost": 34.24},
        {"code": "00795B.TW", "name": "中信美國公債20年", "shares": 58000, "cost": 30.66},
        {"code": "00853B.TW", "name": "統一美債10年Aa-A", "shares":  1000, "cost": 28.52},
        {"code": "00933B.TW", "name": "國泰10Y+金融債",   "shares":  2000, "cost": 16.78},
    ],
}

# 已知收盤價（記憶中的數據）
known_prices = {
    "00687B.TW": 28.58,
    "00795B.TW": 27.73,
    "00751B.TW": 23.81,
    "00853B.TW": 13.91,
    "00933B.TW": 14.87,
}

# 嘗試抓即時價格
live_prices = {}
if yf:
    print("\n正在抓取即時價格...")
    for code in known_prices.keys():
        try:
            t = yf.Ticker(code)
            price = t.info.get('regularMarketPrice', 0)
            if price and price > 0:
                live_prices[code] = price
                print(f"  {code}: {price}")
            else:
                live_prices[code] = known_prices[code]
                print(f"  {code}: {known_prices[code]} (使用記憶數據)")
        except Exception as e:
            live_prices[code] = known_prices[code]
            print(f"  {code}: {known_prices[code]} (使用記憶數據)")
else:
    live_prices = known_prices.copy()

# 美10年債殖利率
us10y = 4.317  # 今日數據
if yf:
    try:
        bond = yf.Ticker('^TNX')
        us10y = bond.info.get('regularMarketPrice', 4.317)
    except:
        pass

print(f"\n美10年債殖利率: {us10y}%")

# ==================== 分析 ====================
print("\n" + "=" * 70)
print("【A帳戶 債券ETF 分析】")
print("=" * 70)

a_total_value = 0
a_total_cost = 0

for etf in bond_etfs["A帳戶"]:
    price = live_prices.get(etf["code"], known_prices.get(etf["code"], 0))
    value = price * etf["shares"]
    cost_total = etf["cost"] * etf["shares"]
    pnl = value - cost_total
    pnl_pct = pnl / cost_total * 100
    a_total_value += value
    a_total_cost += cost_total

    print(f"\n  📊 {etf['name']} ({etf['code']})")
    print(f"     持股：{etf['shares']:,} 股")
    print(f"     均價：{etf['cost']} 元 → 現價：{price} 元")
    print(f"     市值：{value:,.0f} 元")
    print(f"     損益：{pnl:+,.0f} 元 ({pnl_pct:+.2f}%)")

print(f"\n  A帳戶債券小計：")
print(f"  市值：{a_total_value:,.0f} 元")
print(f"  成本：{a_total_cost:,.0f} 元")
print(f"  損益：{a_total_value - a_total_cost:+,.0f} 元 ({(a_total_value-a_total_cost)/a_total_cost*100:+.2f}%)")

print("\n" + "=" * 70)
print("【B帳戶 債券ETF 分析】")
print("=" * 70)

b_total_value = 0
b_total_cost = 0

for etf in bond_etfs["B帳戶"]:
    price = live_prices.get(etf["code"], known_prices.get(etf["code"], 0))
    value = price * etf["shares"]
    cost_total = etf["cost"] * etf["shares"]
    pnl = value - cost_total
    pnl_pct = pnl / cost_total * 100
    b_total_value += value
    b_total_cost += cost_total

    print(f"\n  📊 {etf['name']} ({etf['code']})")
    print(f"     持股：{etf['shares']:,} 股")
    print(f"     均價：{etf['cost']} 元 → 現價：{price} 元")
    print(f"     市值：{value:,.0f} 元")
    print(f"     損益：{pnl:+,.0f} 元 ({pnl_pct:+.2f}%)")

print(f"\n  B帳戶債券小計：")
print(f"  市值：{b_total_value:,.0f} 元")
print(f"  成本：{b_total_cost:,.0f} 元")
print(f"  損益：{b_total_value - b_total_cost:+,.0f} 元 ({(b_total_value-b_total_cost)/b_total_cost*100:+.2f}%)")

# ==================== 總計 ====================
total_bond_value = a_total_value + b_total_value
total_bond_cost = a_total_cost + b_total_cost
total_bond_pnl = total_bond_value - total_bond_cost

print("\n" + "=" * 70)
print("【A+B 帳戶 債券ETF 總計】")
print("=" * 70)
print(f"  總市值：{total_bond_value:,.0f} 元")
print(f"  總成本：{total_bond_cost:,.0f} 元")
print(f"  總損益：{total_bond_pnl:+,.0f} 元 ({total_bond_pnl/total_bond_cost*100:+.2f}%)")

# ==================== CEO 裁決 ====================
print("\n" + "=" * 70)
print("【CEO 裁決 - 債券ETF 明日操作建議】")
print("=" * 70)

print(f"""
📌 背景：美10年債殖利率 {us10y}%（偏高）

【核心邏輯】
  債券價格 ↑ ← 殖利率 ↓ ← Fed 降息
  目前殖利率 {us10y}% 仍偏高，債券仍在壓力下

【各ETF 分析】

  00687B / 00795B（20年美債）
  → 最敏感，殖利率每降1%，價格漲約20%
  → 目前虧損 7-10%，等待 Fed 降息訊號
  → 建議：續抱，不加碼，不停損

  00751B（公司債/永豐20年）
  → 信用風險較低，但仍受利率影響
  → 建議：續抱

  00853B（10年美債）
  → 存續期間較短，波動較小
  → 建議：續抱

  00933B（金融債/ESG投等債）
  → 信用利差風險，但品質較高
  → 建議：續抱

【明日操作】
  ✅ 全部債券ETF：續抱，不動
  ✅ 等待 Fed 降息訊號（預計 2026 Q2-Q3）
  ✅ 殖利率若跌破 4.0%，債券ETF 將大幅回升

【潛在催化劑】
  • Fed 降息 → 債券大漲
  • 美國經濟衰退 → 資金逃入債券
  • 關稅戰升溫 → 避險需求增加

【風險】
  • 通膨再起 → 殖利率繼續升 → 債券繼續跌
  • 目前 CPI 仍偏高，需持續觀察
""")

print("=" * 70)
print("分析完成")
print("=" * 70)
