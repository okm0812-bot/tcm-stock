# -*- coding: utf-8 -*-
"""
大盤跌勢下，佳世達是否該觀望？
"""
import yfinance as yf
from datetime import datetime

print("\n" + "="*70)
print("【大盤跌勢分析】" + datetime.now().strftime('%Y-%m-%d %H:%M'))
print("="*70)

# 取得大盤資料
print("\n【台股加權指數近5日】")
print("-"*70)

try:
    twii = yf.Ticker('^TWII')
    hist = twii.history(period='5d')
    
    print(f"{'日期':<12} {'開盤':>8} {'最高':>8} {'最低':>8} {'收盤':>8} {'漲跌':>8}")
    print("-"*70)
    
    for idx, row in hist.iterrows():
        date_str = idx.strftime('%m/%d')
        change = ""
        if idx != hist.index[0]:
            prev_close = hist.loc[:idx].iloc[-2]['Close']
            change = f"{(row['Close'] - prev_close) / prev_close * 100:+.2f}%"
        print(f"{date_str:<12} {row['Open']:>8.0f} {row['High']:>8.0f} {row['Low']:>8.0f} {row['Close']:>8.0f} {change:>8}")
    
    latest = hist.iloc[-1]
    prev = hist.iloc[-2]
    change_pct = (latest['Close'] - prev['Close']) / prev['Close'] * 100
    
    print(f"\n上週五收盤: {latest['Close']:.0f} 點")
    print(f"近5日變化: {change_pct:+.2f}%")
    
except Exception as e:
    print(f"無法取得大盤資料: {e}")

# 佳世達 vs 大盤
print("\n" + "="*70)
print("【佳世達 2352 vs 大盤】")
print("="*70)

try:
    qisda = yf.Ticker('2352.TW')
    q_hist = qisda.history(period='5d')
    
    print(f"\n{'日期':<12} {'佳世達收盤':>12} {'成交量':>12}")
    print("-"*50)
    
    for idx, row in q_hist.iterrows():
        date_str = idx.strftime('%m/%d')
        print(f"{date_str:<12} {row['Close']:>12.2f} {int(row['Volume']):>12,}")
    
    q_latest = q_hist.iloc[-1]
    q_prev = q_hist.iloc[-2]
    q_change = (q_latest['Close'] - q_prev['Close']) / q_prev['Close'] * 100
    
    print(f"\n佳世達近1日變化: {q_change:+.2f}%")
    
except Exception as e:
    print(f"無法取得佳世達資料: {e}")

print("\n" + "="*70)
print("【系統性風險 vs 個股風險】")
print("="*70)

print("""
當大盤跌時，要區分兩種情況：

1. 【系統性風險】（大盤跌）
   - 所有股票都跌
   - 這是市場風險，無法避免
   - 好公司跌後會反彈

2. 【個股風險】（基本面差）
   - 公司本身有問題
   - 大盤跌時跌更多
   - 大盤漲時漲比較少

佳世達的情況：
- 大盤跌 → 佳世達跟著跌
- 大盤漲 → 佳世達漲比較少（因為基本面差）
- 結論：無論大盤如何，佳世達都弱勢
""")

print("\n" + "="*70)
print("【觀望的理由分析】")
print("="*70)

print("""
✅ 可以觀望的理由：
1. 大盤跌勢可能結束，反彈在即
2. 佳世達可能跟著大盤反彈
3. 不想賣在相對低點

❌ 不該觀望的理由：
1. 佳世達基本面差，反彈幅度有限
2. 即使反彈，也不會回到你的成本（53.78）
3. 時間成本，資金卡住
4. 若大盤續跌，佳世達會跌更多
""")

print("\n" + "="*70)
print("【情境模擬】")
print("="*70)

print("""
假設大盤走勢：

情境A：大盤反彈 +5%
  → 佳世達可能反彈 +3%（弱勢股）
  → 從 23.3 漲到 24.0
  → 你仍虧損 -55%
  → 值得等嗎？

情境B：大盤續跌 -5%
  → 佳世達可能跌 -8%（弱勢股跌更多）
  → 從 23.3 跌到 21.4
  → 你虧損擴大到 -60%
  → 後悔沒早賣

情境C：大盤持平
  → 佳世達可能緩跌（量縮）
  → 時間成本，資金卡住
""")

print("\n" + "="*70)
print("【CEO 建議】")
print("="*70)

print("""
關鍵問題：你是在等「反彈」還是「回到成本」？

1. 如果等反彈（23 → 24）：
   - 可能等得到，但意義不大
   - 虧損仍 -55%

2. 如果等回到成本（23 → 53）：
   - 機率極低
   - 需要漲 +128%
   - 可能要等數年

結論：
- 大盤跌勢下，佳世達會跌更多
- 大盤反彈時，佳世達漲比較少
- **基本面差的股票，不該觀望**
- **及時止損，資金轉向更好的標的**

建議：
- 今日賣出佳世達
- 回收資金買 ETF（00878 或 0050）
- ETF 跟隨大盤，反彈時能跟上
""")

print("="*70)