# realtime_portfolio.py
# 即時股價抓取 + 投資組合分析 v1.0
# 使用方法: python realtime_portfolio.py

import yfinance as yf
import pandas as pd
import json
import sys
from datetime import datetime

# 解決 Windows CMD 編碼問題
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("  [A] 即時投資組合分析系統 v1.0")
print("=" * 60)
print()

# ============================================================
# 持股資料（可自行修改）
# ============================================================
portfolio = {
    "A帳戶": {
        "國泰20年美債00687B": {"ticker": "00687B.TW", "股數": 11000, "成本均價": 31.22},
        "中信美國公債20年00795B": {"ticker": "00795B.TW", "股數": 14000, "成本均價": 29.89},
        "永豐20年美公債": {"ticker": "00751B.TW", "股數": 5000, "成本均價": 25.08},
        "統一美債20年": {"ticker": "00727B.TW", "股數": 5000, "成本均價": 14.96},
        "群益ESG投等債20+": {"ticker": "00858B.TW", "股數": 8000, "成本均價": 15.77},
        "台泥": {"ticker": "1101.TW", "股數": 19000, "成本均價": 34.56},
        "佳世達": {"ticker": "2352.TW", "股數": 11000, "成本均價": 53.78},
        "友達": {"ticker": "2409.TW", "股數": 9000, "成本均價": 16.20},
        "康霈": {"ticker": "6919.TW", "股數": 300, "成本均價": 102.36},
    },
    "B帳戶": {
        "中信美國公債20年00795B(B)": {"ticker": "00795B.TW", "股數": 58000, "成本均價": 29.89},
        "國泰20年美債00687B(B)": {"ticker": "00687B.TW", "股數": 9000, "成本均價": 19.57},
        "元大AAA至A公司債": {"ticker": "00751B.TW", "股數": 2000, "成本均價": 34.26},
        "統一美債10年Aa-A": {"ticker": "00853B.TW", "股數": 1000, "成本均價": 28.56},
        "國泰10Y+金融債": {"ticker": "00933B.TW", "股數": 2000, "成本均價": 16.67},
    }
}

cash = 2_000_000  # 現金 200萬

# ============================================================
# 抓取即時股價
# ============================================================
print("🔍 抓取即時股價中...")
print()

all_tickers = set()
for account_data in portfolio.values():
    for stock_info in account_data.values():
        all_tickers.add(stock_info["ticker"])

# 批量抓取
ticker_list = list(all_tickers)
print(f"   抓取 {len(ticker_list)} 檔股票...")

try:
    # 先嘗試批量抓取
    data = yf.download(ticker_list, period="5d", progress=False, auto_adjust=True)
    price_data = {}
    for t in ticker_list:
        try:
            if len(ticker_list) == 1:
                close_prices = data['Close']
            else:
                close_prices = data['Close'][t]
            if close_prices is not None and len(close_prices) > 0:
                price_data[t] = close_prices.iloc[-1]
        except:
            # 個別抓取
            t_data = yf.Ticker(t)
            info = t_data.info
            price_data[t] = info.get('regularMarketPrice', 0)
except Exception as e:
    print(f"   批量抓取失敗，改用個別抓取...")
    for t in ticker_list:
        try:
            t_data = yf.Ticker(t)
            info = t_data.info
            price_data[t] = info.get('regularMarketPrice', 0)
        except:
            price_data[t] = 0

print()

# ============================================================
# 分析輸出
# ============================================================
total_market_value = 0
total_cost = 0
all_stocks = []

print("=" * 60)
print("  📋 A 帳戶 持股分析")
print("=" * 60)
print(f"{'名稱':<20} {'股數':>7} {'成本均價':>8} {'市價':>7} {'市值':>10} {'成本':>10} {'損益':>10} {'報酬率':>8}")
print("-" * 100)

for name, info in portfolio["A帳戶"].items():
    ticker = info["ticker"]
    shares = info["股數"]
    cost_avg = info["成本均價"]
    
    market_price = price_data.get(ticker, 0)
    market_value = shares * market_price
    total_cost_stock = shares * cost_avg
    unrealized_pl = market_value - total_cost_stock
    return_rate = (unrealized_pl / total_cost_stock * 100) if total_cost_stock > 0 else 0
    
    total_market_value += market_value
    total_cost += total_cost_stock
    
    trend = "▲" if unrealized_pl > 0 else "▼" if unrealized_pl < 0 else "─"
    color = "🟢" if unrealized_pl > 0 else "🔴" if unrealized_pl < 0 else "⚪"
    
    print(f"{name:<18} {shares:>7,} {cost_avg:>8.2f} {market_price:>7.2f} {market_value:>10,.0f} {total_cost_stock:>10,.0f} {trend}{abs(unrealized_pl):>9,.0f} {return_rate:>7.2f}%")
    
    all_stocks.append({
        "帳戶": "A", "名稱": name, "ticker": ticker,
        "股數": shares, "成本均價": cost_avg,
        "市價": market_price, "市值": market_value,
        "成本": total_cost_stock, "損益": unrealized_pl,
        "報酬率": return_rate
    })

print()
print("=" * 60)
print("  📋 B 帳戶 持股分析（純債 ETF）")
print("=" * 60)
print(f"{'名稱':<20} {'股數':>7} {'成本均價':>8} {'市價':>7} {'市值':>10} {'成本':>10} {'損益':>10} {'報酬率':>8}")
print("-" * 100)

for name, info in portfolio["B帳戶"].items():
    ticker = info["ticker"]
    shares = info["股數"]
    cost_avg = info["成本均價"]
    
    market_price = price_data.get(ticker, 0)
    market_value = shares * market_price
    total_cost_stock = shares * cost_avg
    unrealized_pl = market_value - total_cost_stock
    return_rate = (unrealized_pl / total_cost_stock * 100) if total_cost_stock > 0 else 0
    
    total_market_value += market_value
    total_cost += total_cost_stock
    
    trend = "▲" if unrealized_pl > 0 else "▼" if unrealized_pl < 0 else "─"
    
    print(f"{name:<18} {shares:>7,} {cost_avg:>8.2f} {market_price:>7.2f} {market_value:>10,.0f} {total_cost_stock:>10,.0f} {trend}{abs(unrealized_pl):>9,.0f} {return_rate:>7.2f}%")
    
    all_stocks.append({
        "帳戶": "B", "名稱": name, "ticker": ticker,
        "股數": shares, "成本均價": cost_avg,
        "市價": market_price, "市值": market_value,
        "成本": total_cost_stock, "損益": unrealized_pl,
        "報酬率": return_rate
    })

print()

# ============================================================
# 總資產概覽
# ============================================================
total_assets = total_market_value + cash
total_unrealized = total_market_value - total_cost

print("=" * 60)
print("  💰 總資產概覽")
print("=" * 60)
print(f"  股票/ETF 總市值：{total_market_value:>15,.0f} 元")
print(f"  現金部位：       {cash:>15,.0f} 元")
print(f"  總資產：        {total_assets:>15,.0f} 元")
print(f"  總未實現損益：  {total_unrealized:>15,.0f} 元")
print(f"  總報酬率：       {total_unrealized/total_cost*100:>14.2f}%")
print()
print(f"  股票/ETF 佔比： {total_market_value/total_assets*100:>14.1f}%")
print(f"  現金佔比：      {cash/total_assets*100:>14.1f}%")
print()

# ============================================================
# 風險評估
# ============================================================
print("=" * 60)
print("  🚨 風險評估")
print("=" * 60)

stock_value = sum(s["市值"] for s in all_stocks if "債" not in s["名稱"])
bond_value = sum(s["市值"] for s in all_stocks if "債" in s["名稱"])
stock_ratio = stock_value / total_market_value * 100
bond_ratio = bond_value / total_market_value * 100

print(f"  股票部位佔比：   {stock_ratio:>14.1f}%  ({stock_value/total_assets*100:.1f}% 總資產)")
print(f"  債券部位佔比：   {bond_ratio:>14.1f}%  ({bond_value/total_assets*100:.1f}% 總資產)")

# 找出最大虧損
losses = sorted([s for s in all_stocks if s["損益"] < 0], key=lambda x: x["報酬率"])
print()
print("  🔴 前三大虧損：")
for i, s in enumerate(losses[:3], 1):
    print(f"     {i}. {s['名稱']}：{s['報酬率']:.2f}% ({s['損益']:,.0f}元)")

# 找出正報酬
gains = sorted([s for s in all_stocks if s["損益"] > 0], key=lambda x: -x["報酬率"])
print()
print("  🟢 正報酬持倉：")
if gains:
    for i, s in enumerate(gains[:3], 1):
        print(f"     {i}. {s['名稱']}：+{s['報酬率']:.2f}% ({'+'+str(int(s['損益']))}元)")
else:
    print("     目前無正報酬持倉")

print()
print("=" * 60)
print(f"  📅 分析時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# ============================================================
# 儲存結果
# ============================================================
df = pd.DataFrame(all_stocks)
df.to_csv("portfolio_realtime.csv", index=False, encoding="utf-8-sig")
print()
print("✅ 資料已儲存至 portfolio_realtime.csv")
