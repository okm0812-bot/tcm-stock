# -*- coding: utf-8 -*-
"""
CEO 分析：ETF 投資建議
"""
import yfinance as yf
from datetime import datetime

print("\n" + "="*70)
print("【CEO 分析：ETF 投資建議】" + datetime.now().strftime('%Y-%m-%d %H:%M'))
print("="*70)

# ETF 清單
etfs = [
    # 被動式 - 市值型
    ("0050.TW", "元大台灣50", "市值型", "被動", "台股龍頭"),
    ("006208.TW", "富邦台50", "市值型", "被動", "台股龍頭"),
    ("00881.TW", "中信關鍵半導體", "產業型", "被動", "半導體"),
    ("00662.TW", "富邦 Nasdaq", "產業型", "被動", "美股科技"),
    
    # 被動式 - 高股息
    ("0056.TW", "元大高股息", "高股息", "被動", "高股息"),
    ("00878.TW", "國泰永續高股息", "高股息", "被動", "高股息+ESG"),
    ("00919.TW", "群益科技高股息", "高股息", "被動", "科技高股息"),
    ("00772.TW", "中信高股息", "高股息", "被動", "高股息"),
    
    # 主動式
    ("0055.TW", "元大龍頭", "市值型", "主動", "主動選股"),
    
    # 債券型
    ("00687B.TW", "國泰20年美債", "債券", "被動", "長天期美債"),
    ("00795B.TW", "中信20年美債", "債券", "被動", "長天期美債"),
    ("00751B.TW", "元大AAA至A公司債", "債券", "被動", "投資級公司債"),
    
    # 美股
    ("VTI", "Vanguard全市場", "市值型", "被動", "美股全市場"),
    ("VOO", "Vanguard S&P500", "市值型", "被動", "美股S&P500"),
    ("VT", "Vanguard全球市場", "市值型", "被動", "全球市場"),
]

print("""
【ETF 分類框架】

1. 主動 vs 被動
   - 被動：追蹤指數，費用低，適合長期持有
   - 主動：經理人選股，費用高，但可能超額報酬

2. 市值型 vs 高股息
   - 市值型：跟隨大盤，成長潛力大
   - 高股息：穩定現金流，適合退休/防禦

3. 台股 vs 美股
   - 台股：了解本地市場，但集中單一市場
   - 美股：分散風險，但有匯率風險
""")

print("="*70)
print("【ETF 詳細分析】")
print("="*70)

results = []

for ticker, name, category, style, desc in etfs:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        price = info.get('regularMarketPrice', 0)
        pe = info.get('trailingPE', 0) or 0
        div_yield = (info.get('dividendYield', 0) or 0) * 100
        expense = info.get('expenseRatio', 0) or 0
        nav = info.get('netAssetValue', 0) or price
        
        # 計算分數
        score = 0
        reasons = []
        
        # 費用率（越低越好）
        if expense and expense < 0.3:
            score += 2
            reasons.append(f"費用率 {expense*100:.2f}%")
        elif expense and expense < 0.5:
            score += 1
            reasons.append(f"費用率 {expense*100:.2f}%")
        
        # PE（本益比）
        if pe and 0 < pe < 20:
            score += 1
            reasons.append(f"PE {pe:.1f}x")
        
        # 殖利率
        if category == "高股息" and div_yield > 5:
            score += 2
            reasons.append(f"殖利率 {div_yield:.1f}%")
        elif category == "高股息" and div_yield > 3:
            score += 1
            reasons.append(f"殖利率 {div_yield:.1f}%")
        
        results.append({
            'ticker': ticker,
            'name': name,
            'category': category,
            'style': style,
            'price': price,
            'pe': pe,
            'div_yield': div_yield,
            'expense': expense * 100,
            'score': score,
            'reasons': reasons,
            'desc': desc
        })
        
    except Exception as e:
        pass

# 按分類排序
print("\n" + "-"*70)
print("【市值型 ETF】")
print("-"*70)
print(f"{'代號':<12} {'名稱':<15} {'現價':>8} {'PE':>6} {'費用':>6} {'評分':>6}")
print("-"*70)

market_cap = [r for r in results if r['category'] == '市值型']
market_cap.sort(key=lambda x: x['score'], reverse=True)

for r in market_cap:
    pe_str = f"{r['pe']:.1f}x" if r['pe'] else "N/A"
    exp_str = f"{r['expense']:.2f}%" if r['expense'] else "N/A"
    print(f"{r['ticker']:<12} {r['name']:<15} {r['price']:>8.2f} {pe_str:>6} {exp_str:>6} {r['score']:>6}")

print("\n" + "-"*70)
print("【高股息 ETF】")
print("-"*70)
print(f"{'代號':<12} {'名稱':<15} {'現價':>8} {'殖利率':>8} {'費用':>6} {'評分':>6}")
print("-"*70)

high_div = [r for r in results if r['category'] == '高股息']
high_div.sort(key=lambda x: x['score'], reverse=True)

for r in high_div:
    div_str = f"{r['div_yield']:.1f}%" if r['div_yield'] else "N/A"
    exp_str = f"{r['expense']:.2f}%" if r['expense'] else "N/A"
    print(f"{r['ticker']:<12} {r['name']:<15} {r['price']:>8.2f} {div_str:>8} {exp_str:>6} {r['score']:>6}")

print("\n" + "-"*70)
print("【產業型 ETF】")
print("-"*70)

industry = [r for r in results if r['category'] == '產業型']
for r in industry:
    print(f"{r['ticker']:<12} {r['name']:<15} {r['price']:>8.2f} {r['desc']:<15} 評分:{r['score']}")

print("\n" + "-"*70)
print("【債券型 ETF】")
print("-"*70)

bonds = [r for r in results if r['category'] == '債券']
for r in bonds:
    div_str = f"{r['div_yield']:.1f}%" if r['div_yield'] else "N/A"
    print(f"{r['ticker']:<12} {r['name']:<15} {r['price']:>8.2f} 殖利率:{div_str:<10} 評分:{r['score']}")

print("\n" + "-"*70)
print("【美股 ETF】")
print("-"*70)

us = [r for r in results if 'TWO' not in r['ticker']]
for r in us:
    pe_str = f"{r['pe']:.1f}x" if r['pe'] else "N/A"
    div_str = f"{r['div_yield']:.1f}%" if r['div_yield'] else "N/A"
    print(f"{r['ticker']:<12} {r['name']:<15} {r['price']:>8.2f} PE:{pe_str:<6} 殖:{div_str:<6} 評分:{r['score']}")

# 比較表格
print("\n" + "="*70)
print("【比較表：主動 vs 被動】")
print("="*70)

print("""
| 項目 | 被動ETF | 主動ETF |
|------|---------|---------|
| 費用率 | 0.1-0.5% | 0.5-1.5% |
| 選股 | 追蹤指數 | 經理人決定 |
| 報酬 | 接近大盤 | 可能超額 |
| 風險 | 分散 | 視經理人 |
| 適合 | 長期持有 | 積極操作 |

結論：【被動ETF】適合大多數投資人
""")

print("="*70)
print("【比較表：市值型 vs 高股息】")
print("="*70)

print("""
| 項目 | 市值型 | 高股息 |
|------|--------|--------|
| 目標 | 成長 | 現金流 |
| 報酬 | 資本利得 | 股息 |
| 波動 | 較高 | 較低 |
| 適合 | 年輕/成長 | 退休/防禦 |
| 代表 | 0050 | 0056/00878 |

結論：
- 年輕人/長期投資 → 市值型（0050）
- 穩定現金流 → 高股息（00878）
""")

# 最終建議
print("\n" + "="*70)
print("【CEO 最終建議】")
print("="*70)

print("""
根據巴菲特 + CEO 分析框架：

【保守型投資人】（你的情況）
- 剛止損佳世達，需要穩定標的
- 建議：高股息 ETF（00878 或 0056）
- 理由：穩定現金流、波动较低

【積極型投資人】
- 追求資本利得
- 建議：市值型 ETF（0050 或 006208）
- 理由：長期成長潛力大

【分散風險】
- 建議配置：
  - 50% 台股高股息（00878）
  - 30% 台股市值型（0050）
  - 20% 美股（VOO 或 VT）

【現在進場時機】
- 台股估值仍高，建議分批買入
- 不要一次all in
- 設停損點 -10%
""")

print("="*70)
print("【Top 3 推薦】")
print("="*70)

print("""
1. 【00878 國泰永續高股息】⭐⭐⭐⭐⭐
   - 殖利率：預估 5-7%
   - 費用率：0.35%
   - 特色：ESG + 高股息
   - 適合：穩定現金流

2. 【0050 元大台灣50】⭐⭐⭐⭐
   - 成長性：跟隨台股大盤
   - 費用率：0.40%
   - 特色：台股龍頭
   - 適合：長期持有

3. 【0056 元大高股息】⭐⭐⭐⭐
   - 殖利率：預估 4-6%
   - 費用率：0.35%
   - 特色：高股息策略
   - 適合：穩健收益
""")

print("="*70)
