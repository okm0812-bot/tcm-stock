# -*- coding: utf-8 -*-
import yfinance as yf
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("B帳戶 ETF 均價計算")
print("=" * 70)

# 抓取最新報價
etfs = [
    ("00687B", "00687B.TW"),
    ("00751B", "00751B.TW"),
    ("00795B", "00795B.TW"),
    ("00853B", "00853B.TW"),
    ("00933B", "00933B.TW"),
]

prices = {}
for name, code in etfs:
    try:
        ticker = yf.Ticker(code)
        info = ticker.info
        price = info.get('regularMarketPrice', 0) or info.get('navPrice', 0)
        prices[name] = price
        print(f"{name}: {price:.2f} 元")
    except Exception as e:
        print(f"{name}: 無法取得報價 ({e})")
        prices[name] = 0

print()

# 用戶提供的資料反算均價
# 虧損% = (現價 - 均價) / 均價 * 100
# 虧損% = -6.39% 表示現價比均價低 6.39%
# 所以：現價 = 均價 * (1 - 6.39%) = 均價 * 0.9361
# 均價 = 現價 / 0.9361

user_data = [
    ("00687B 國泰20年美債", 9000, -6.39),
    ("00751B 元大AAA至A公司債", 2000, -7.06),
    ("00795B 中信美國公債20年", 58000, -9.69),
    ("00853B 統一美債10年Aa-A", 1000, -2.24),
    ("00933B 國泰10Y+金融債", 2000, -3.78),
]

print("=" * 70)
print("均價反算")
print("公式：均價 = 現價 / (1 + 虧損率%)")
print("=" * 70)

total_cost = 0
total_market = 0

results = []
for name, shares, loss_pct in user_data:
    price = prices.get(name[:6], 0)
    if price > 0 and loss_pct != 0:
        # 虧損率是負的，所以要用 1 + loss_pct/100
        # 例如 -6.39% -> 1 + (-0.0639) = 0.9361
        avg_cost = price / (1 + loss_pct / 100)
    else:
        avg_cost = 0
    
    market = shares * price
    cost = shares * avg_cost
    total_cost += cost
    total_market += market
    
    results.append({
        "name": name,
        "shares": shares,
        "price": price,
        "avg_cost": avg_cost,
        "market": market,
        "cost": cost,
        "loss": cost - market,
        "loss_pct": loss_pct
    })
    
    print(f"\n{name}")
    print(f"  股數：{shares:,} 股")
    print(f"  現價：{price:.2f} 元")
    print(f"  均價：{avg_cost:.4f} 元")
    print(f"  市值：{market:,.0f} 元")
    print(f"  成本：{cost:,.0f} 元")
    print(f"  虧損：{cost-market:,.0f} 元 ({loss_pct:.2f}%)")

print()
print("=" * 70)
print("B帳戶總計")
print("=" * 70)
print(f"總市值：{total_market:,.0f} 元")
print(f"總成本：{total_cost:,.0f} 元")
print(f"總虧損：{total_cost - total_market:,.0f} 元 ({((total_cost-total_market)/total_cost*100):.2f}%)")

# 驗證是否等於 2183268
print()
print(f"用戶提供總成本：2,183,268 元")
print(f"計算總成本：{total_cost:,.0f} 元")
diff = abs(2183268 - total_cost)
print(f"差額：{diff:,.0f} 元 ({diff/2183268*100:.2f}%)")

# 輸出用於更新 MEMORY.md
print()
print("=" * 70)
print("用於更新 MEMORY.md 的格式")
print("=" * 70)
for r in results:
    print(f"| {r['name']} | {r['shares']:,} | {r['avg_cost']:.4f} | {r['price']:.2f} | {r['market']:,.0f} | {r['loss']:,.0f} | {r['loss_pct']:.2f}% |")
