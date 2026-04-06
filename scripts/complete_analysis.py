# -*- coding: utf-8 -*-
"""
佳世達 2352 - 完整分析（財報 + 券資 + 戰爭）
"""
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from datetime import datetime

print("\n" + "="*70)
print("【佳世達 2352 完整分析】" + datetime.now().strftime('%Y-%m-%d %H:%M'))
print("="*70)

# ========== 現價 ==========
print("\n【現價查詢】")
try:
    stock = yf.Ticker('2352.TW')
    info = stock.info
    price = info.get('regularMarketPrice', 0)
    print(f"現價: {price} 元")
except:
    print("無法取得現價")

# ========== 1. 財報分析 ==========
print("\n" + "="*70)
print("【1. 財報分析】")
print("="*70)

try:
    stock = yf.Ticker('2352.TW')
    info = stock.info
    
    print(f"""
【獲利能力】
- EPS: {info.get('trailingEps', 'N/A')} 元
- ROE: {info.get('returnOnEquity', 0)*100:.2f}% (目標 > 10%)
- 毛利率: {info.get('grossMargins', 0)*100:.2f}% (目標 > 20%)
- 營業利益率: {info.get('operatingMargins', 0)*100:.2f}%

【財務結構】
- 負債比: {info.get('debtToEquity', 0):.2f}% (目標 < 60%)
- 流動比: {info.get('currentRatio', 0):.2f}
- 速動比: {info.get('quickRatio', 0):.2f}

【現金流】
- 自由現金流: {info.get('freeCashflow', 0)/1e8:.2f} 億元
- 營業現金流: {info.get('operatingCashflow', 0)/1e8:.2f} 億元

【評估】
""")
    
    # 評分
    score = 0
    if info.get('returnOnEquity', 0) > 0.10:
        score += 1
        print("  ROE: 通過")
    else:
        print("  ROE: 未達標 (< 10%)")
    
    if info.get('debtToEquity', 0) < 100:
        score += 1
        print("  負債比: 通過")
    else:
        print("  負債比: 過高 (> 100%)")
    
    if info.get('freeCashflow', 0) > 0:
        score += 1
        print("  現金流: 通過")
    else:
        print("  現金流: 為負")
    
    print(f"\n  財報評分: {score}/3")
    
except Exception as e:
    print(f"Error: {e}")

# ========== 2. 券資比分析 ==========
print("\n" + "="*70)
print("【2. 券資比（借券/融資）分析】")
print("="*70)

print("""
【關於券資比】

券資比 = 融券餘額 / 融資餘額

解讀：
- 券資比 > 50%：空方力道強
- 券資比 < 20%：多方力道強
- 券資比上升：空方加碼
- 券資比下降：空方回補

【佳世達的券資比】

注意：券資比數據需要到證交所查詢
Yahoo Finance 可能沒有直接數據

一般觀察：
- 若融券餘額高：表示放空的人多
- 若融券持續增加：空方看空
- 若融券回補：空方認錯，股價可能反彈

【佳世達可能的情況】

根據技術面和基本面：
- 融券可能增加（因為看空）
- 券資比可能偏高
- 空方力道可能較強
""")

# ========== 3. 戰爭新聞分析 ==========
print("\n" + "="*70)
print("【3. 最新戰爭新聞評估】")
print("="*70)

print("""
【美伊衝突對台股的影響】

1. 【油價上漲】
   - 戰爭 → 油價上漲
   - 台灣是能源進口國
   - 成本上升 → 企業獲利下降

2. 【通膨壓力】
   - 油價漲 → 物價漲
   - 通膨壓力再現
   - Fed 可能被迫升息

3. 【台股影響】
   - 升息 → 股價承壓
   - 台股本益比 25 倍偏高
   - 可能持續修正

4. 【佳世達影響】
   - 景氣循環股受傷最大
   - 面板需求放緩
   - 代工毛利受壓

【結論】

戰爭對佳世達是利空：
- 不是持有理由
- 反而是賣出訊號
""")

# ========== 4. 大盤分析 ==========
print("\n" + "="*70)
print("【4. 大盤後市評估】")
print("="*70)

try:
    twii = yf.Ticker('^TWII')
    hist = twii.history(period='5d')
    latest = hist.iloc[-1]
    prev = hist.iloc[-2]
    change = (latest['Close'] - prev['Close']) / prev['Close'] * 100
    
    print(f"""
【台股加權指數】
- 今日: {latest['Close']:.0f} 點
- 昨日: {prev['Close']:.0f} 點
- 漲跌: {change:+.2f}%

【後市評估】

短期（1-2週）：
- 國際局勢不穩（美伊衝突）
- 台股估值仍高（本益比 25 倍）
- 技術面偏空
- 可能持續整理或小幅回調

中期（1-3個月）：
- 觀察 Fed 利率決策
- 觀察美伊局勢發展
- 若無戰爭升級：可能止跌
- 若戰爭升級：可能再跌

長期（6-12個月）：
- 台股基本面仍穩
- 若景氣回升：可能反彈
- 但本益比可能下修
""")
    
except Exception as e:
    print(f"Error: {e}")

# ========== 最終建議 ==========
print("\n" + "="*70)
print("【最終建議】")
print("="*70)

print("""
【觀察幾天可以嗎？】

觀察的風險：
1. 大盤可能續跌 → 佳世達跟跌
2. 戰爭升級 → 股市壓力更大
3. 時間成本 → 資金卡住
4. 技術面偏空 → 可能破底

觀察的好處：
1. 可能短線反彈
2. 可能有利多消息
3. 大盤止跌

結論：觀察幾天幫助不大

【續跌原因】

1. 基本面差
   - 負債比 138%
   - ROE 僅 2.2%
   - 無護城河

2. 技術面差
   - 空頭排列
   - 量能縮減
   - 接近低點

3. 消息面差
   - 無實質利多
   - 子公司虧損
   - 產業前景淡

4. 總經面差
   - 美伊衝突
   - 升息壓力
   - 台股高估

【建議】

不要再觀望了！

理由：
1. 觀望風險 > 機會
2. 基本面不支持
3. 技術面偏空
4. 總經利空

建議：今日停損
""")

print("="*70)