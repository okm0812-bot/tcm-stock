# -*- coding: utf-8 -*-
"""
佳世達 2352 配息分析
"""
import yfinance as yf
from datetime import datetime

print("\n" + "="*70)
print("【佳世達 2352 配息分析】" + datetime.now().strftime('%Y-%m-%d %H:%M'))
print("="*70)

try:
    stock = yf.Ticker('2352.TW')
    info = stock.info
    
    price = info.get('regularMarketPrice', 0)
    div_yield = info.get('dividendYield', 0) or 0
    
    print(f"\n【基本資料】")
    print(f"現價: {price} 元")
    print(f"殖利率: {div_yield*100:.2f}%")
    
    # 歷史配息
    print(f"\n【歷史配息】")
    print("-"*70)
    
    # 嘗試取得配息歷史
    try:
        dividends = stock.dividends
        if len(dividends) > 0:
            print(f"{'年份':<8} {'配息':>8} {'除息日':<15}")
            print("-"*40)
            for idx, div in dividends.tail(5).items():
                year = idx.year
                date_str = idx.strftime('%Y-%m-%d')
                print(f"{year:<8} {div:>8.2f} {date_str:<15}")
        else:
            print("無法取得配息歷史")
    except:
        print("無法取得配息歷史")
    
    # 預估配息
    print(f"\n【2026年配息預估】")
    print("-"*70)
    
    # 根據歷史推估
    print("""
佳世達配息時程（根據歷史）：

除息日：通常在 7-8 月
發放日：通常在 8-9 月

2025年配息：約 3.55 元
2026年預估：約 2-4 元（視獲利狀況）

注意：佳世達 2025年獲利下滑，2026年配息可能減少。
""")
    
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*70)
print("【等配息 vs 現在賣】")
print("="*70)

print("""
假設情境：

【方案A：現在賣】
- 賣價：23.2 元
- 回收：25.5 萬
- 虧損：-33 萬（-56%）
- 資金可立即運用

【方案B：等配息再賣】
- 除息日：約 2026年7-8月
- 預估配息：2-4 元/股
- 配息收入：11,000股 × 3元 = 33,000元
- 除息後股價：23.2 - 3 = 20.2 元
- 賣價：約 20 元
- 總回收：20×11,000 + 33,000 = 253,000元

比較：
- 現在賣：255,200元
- 等配息：253,000元
- 差異：-2,200元（等配息反而少）

原因：除息後股價會下跌，配息只是左手換右手
""")

print("\n" + "="*70)
print("【關鍵計算】")
print("="*70)

# 計算
price_now = 23.2
shares = 11000
cost = 53.78
div_est = 3.5  # 預估配息

sell_now = price_now * shares
wait_div = (price_now - div_est) * shares + div_est * shares
loss_now = sell_now - cost * shares
loss_wait = wait_div - cost * shares

print(f"""
現價：{price_now} 元
持股：{shares:,} 股
成本：{cost} 元
預估配息：{div_est} 元

【現在賣】
回收：{sell_now:,.0f} 元
虧損：{loss_now:,.0f} 元

【等配息再賣】
除息後股價：{price_now - div_est} 元
配息收入：{div_est * shares:,.0f} 元
賣股收入：{(price_now - div_est) * shares:,.0f} 元
總回收：{wait_div:,.0f} 元
虧損：{loss_wait:,.0f} 元

差異：{wait_div - sell_now:,.0f} 元
""")

print("\n" + "="*70)
print("【結論】")
print("="*70)

print("""
❌ 等配息再賣沒有好處

原因：
1. 除息後股價會下跌（除息參考價 = 前收盤 - 配息）
2. 配息只是「左手換右手」，總價值不變
3. 還要等 4-5 個月（7-8月除息）
4. 這段時間股價可能續跌
5. 資金卡住，無法運用

✅ 建議：現在就賣

理由：
1. 配息不會讓你少虧
2. 早點回收資金，轉向更好的標的
3. 買 ETF 也有配息（00878 殖利率 5-7%）
4. 時間成本：4-5個月可以賺更多
""")

print("\n" + "="*70)
print("【配息的迷思】")
print("="*70)

print("""
很多人以為：
「等配息可以少虧一點」→ 錯！

真相：
配息 = 公司把錢發給股東
股價會等額下跌
總價值不變

舉例：
除息前：股價 23.2 元，持有 1 股 = 價值 23.2 元
除息後：股價 20.2 元，拿到 3 元現金 = 價值 23.2 元

沒有變多，也沒有變少，只是形式改變。

而且：
- 若這 4-5 個月股價續跌，你虧更多
- 若這 4-5 個月大盤反彈，你錯過機會
""")

print("="*70)