# -*- coding: utf-8 -*-
import yfinance as yf
import sys
sys.stdout.reconfigure(encoding="utf-8")

print("=" * 70)
print("台股今日收盤數據（2026-04-01）")
print("=" * 70)

# 持股
stocks = {
    "1101.TW": "台泥",
    "2352.TW": "佳世達",
    "2409.TW": "友達",
    "6919.TW": "康霈",
    "0050.TW": "0050",
    "^TWII": "台股加權"
}

print("\n【個股/指數收盤】")
print("-" * 70)
print(f"{'名稱':<12} {'昨日收':>10} {'今日收':>10} {'漲跌':>10} {'%':>8}")
print("-" * 70)

results = {}
for code, name in stocks.items():
    try:
        t = yf.Ticker(code)
        info = t.info
        price = info.get("regularMarketPrice", 0) or 0
        prev = info.get("regularMarketPreviousClose", 0) or 0
        if price > 0 and prev > 0:
            chg = price - prev
            chg_pct = chg / prev * 100
            results[name] = {"price": price, "prev": prev, "chg": chg, "chg_pct": chg_pct}
            arrow = "▲" if chg > 0 else "▼" if chg < 0 else "-"
            print(f"{name:<12} {prev:>10.2f} {price:>10.2f} {arrow}{abs(chg):>9.2f} {chg_pct:>+7.2f}%")
        else:
            print(f"{name:<12} 無法取得數據")
    except Exception as e:
        print(f"{name:<12} 錯誤: {e}")

print()

# 持股狀態
print("\n【持股今日狀態】")
print("-" * 70)

# A帳戶持股
holdings = [
    {"name": "台泥 1101", "shares": 19000, "cost": 34.56, "prev": 23.00},
    {"name": "佳世達 2352", "shares": 6000, "cost": 51.33, "prev": 22.75},
    {"name": "友達 2409", "shares": 9000, "cost": 16.20, "prev": 14.50},
    {"name": "康霈 6919", "shares": 300, "cost": 102.36, "prev": 86.30},
]

total_pnl_today = 0
for h in holdings:
    name = h["name"].split()[0]
    if name in results:
        price = results[name]["price"]
        prev = results[name]["prev"]
        chg = results[name]["chg"]
        market = price * h["shares"]
        cost = h["cost"] * h["shares"]
        pnl = market - cost
        pnl_today = chg * h["shares"]
        total_pnl_today += pnl_today
        
        arrow = "▲" if chg > 0 else "▼"
        print(f"\n{h['name']}")
        print(f"  今日：{prev:.2f} → {price:.2f} ({arrow}{abs(results[name]['chg_pct']):.2f}%)")
        print(f"  市值：{market:,.0f} 元")
        print(f"  成本：{cost:,.0f} 元")
        print(f"  虧損：{pnl:,.0f} 元 ({pnl/cost*100:.1f}%)")
        print(f"  今日損益：{pnl_today:>+,.0f} 元")

# 0050分析
if "0050" in results:
    print(f"\n【0050 替代標的】")
    r = results["0050"]
    arrow = "▲" if r["chg"] > 0 else "▼"
    print(f"  0050：{r['prev']:.2f} → {r['price']:.2f} ({arrow}{abs(r['chg_pct']):.2f}%)")
    print(f"  如果佳世達停損，可買入 0050")

print("\n" + "=" * 70)
print(f"【持股今日總損益】")
print("=" * 70)
arrow = "▲" if total_pnl_today > 0 else "▼"
print(f"今日總損益：{arrow}{abs(total_pnl_today):,.0f} 元")
