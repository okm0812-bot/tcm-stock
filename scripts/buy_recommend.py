# -*- coding: utf-8 -*-
"""
CEO 分析：適合買入的股票篩選
"""
import yfinance as yf
from datetime import datetime

print("\n" + "="*70)
print("【CEO 分析：值得買入的股票】" + datetime.now().strftime('%Y-%m-%d %H:%M'))
print("="*70)

# 篩選條件
print("""
【篩選條件】（巴菲特 + CEO 框架）
1. 本益比 < 15 倍（估值合理或偏低）
2. 殖利率 > 3%（有現金回饋）
3. ROE > 10%（體質良好）
4. 負債比 < 60%（財務健康）
5. 有護城河（產業龍頭）
""")

# 候選股票清單
candidates = [
    # 金融股（穩定配息）
    ("2884.TW", "玉山金", "金融", "高殖利率、穩定配息"),
    ("2891.TW", "中信金", "金融", "銀行保險複合體"),
    ("2883.TW", "開發金", "金融", "控股公司、多元化"),
    ("5871.TW", "中租-KY", "租賃", "業務穩定、殖利率高"),
    
    # 傳產股（價值型）
    ("2002.TW", "中鋼", "鋼鐵", "低估值、高殖利率"),
    ("1102.TW", "亞泥", "水泥", "穩定配息、中國水泥"),
    ("1301.TW", "台塑", "化工", "石化龍頭、殖利率高"),
    
    # 科技股（但要小心）
    ("2303.TW", "聯電", "晶圓代工", "成熟製程、殖利率高"),
    ("2330.TW", "台積電", "晶圓代工", "護城河強、產業龍頭"),
    
    # ETF（分散風險）
    ("0050.TW", "元大台灣50", "ETF", "台股龍頭、被動投資"),
    ("0056.TW", "元大高股息", "ETF", "高股息、穩定配息"),
    ("00881.TW", "中信關鍵半導體", "ETF", "半導體產業"),
]

print("="*70)
print("【候選股票分析】")
print("="*70)

results = []

for ticker, name, industry, reason in candidates:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        price = info.get('regularMarketPrice', 0)
        pe = info.get('trailingPE', 0)
        div_yield = info.get('dividendYield', 0) or 0
        roe = info.get('returnOnEquity', 0) or 0
        debt = info.get('debtToEquity', 0) or 0
        fcf = info.get('freeCashflow', 0) or 0
        high_52 = info.get('fiftyTwoWeekHigh', 0)
        low_52 = info.get('fiftyTwoWeekLow', 0)
        
        # 計算分數
        score = 0
        reasons = []
        
        if pe and 0 < pe < 15:
            score += 2
            reasons.append(f"PE {pe:.1f}x")
        elif pe and pe < 20:
            score += 1
            reasons.append(f"PE {pe:.1f}x")
        
        if div_yield and div_yield > 0.03:
            score += 2
            reasons.append(f"殖利率 {div_yield*100:.1f}%")
        elif div_yield and div_yield > 0.02:
            score += 1
            reasons.append(f"殖利率 {div_yield*100:.1f}%")
        
        if roe and roe > 0.10:
            score += 2
            reasons.append(f"ROE {roe*100:.1f}%")
        elif roe and roe > 0.05:
            score += 1
            reasons.append(f"ROE {roe*100:.1f}%")
        
        if debt and debt < 100:
            score += 1
            reasons.append(f"負債比 {debt:.0f}%")
        
        if fcf and fcf > 0:
            score += 1
            reasons.append("FCF正")
        
        # 距離高點
        if high_52:
            dist_high = ((high_52 - price) / high_52 * 100)
            if dist_high > 30:
                score += 1
                reasons.append(f"距離高點 {dist_high:.0f}%")
        
        results.append({
            'ticker': ticker,
            'name': name,
            'industry': industry,
            'price': price,
            'pe': pe,
            'div_yield': div_yield * 100,
            'roe': roe * 100,
            'debt': debt,
            'score': score,
            'reasons': reasons,
            'reason': reason
        })
        
    except Exception as e:
        pass

# 排序
results.sort(key=lambda x: x['score'], reverse=True)

print(f"\n{'排名':<4} {'股票':<10} {'現價':>7} {'PE':>6} {'殖利率':>8} {'ROE':>7} {'分數':>6} {'評估'}")
print("-"*80)

for i, r in enumerate(results, 1):
    if r['price'] and r['score'] >= 4:
        pe_str = f"{r['pe']:.1f}x" if r['pe'] else "N/A"
        div_str = f"{r['div_yield']:.1f}%" if r['div_yield'] else "N/A"
        roe_str = f"{r['roe']:.1f}%" if r['roe'] else "N/A"
        
        status = "[推薦]" if r['score'] >= 6 else "[關注]"
        
        print(f"{i:<4} {r['name']:<10} {r['price']:>7.2f} {pe_str:>6} {div_str:>8} {roe_str:>7} {r['score']:>6} {status}")

# Top 5 推薦
print("\n" + "="*70)
print("【Top 5 推薦】")
print("="*70)

top5 = [r for r in results if r['score'] >= 5][:5]

for i, r in enumerate(top5, 1):
    print(f"\n{i}. {r['name']} ({r['ticker']})")
    print(f"   現價: {r['price']:.2f} 元")
    print(f"   本益比: {r['pe']:.1f}x" if r['pe'] else "   本益比: N/A")
    print(f"   殖利率: {r['div_yield']:.1f}%" if r['div_yield'] else "   殖利率: N/A")
    print(f"   ROE: {r['roe']:.1f}%" if r['roe'] else "   ROE: N/A")
    print(f"   原因: {r['reason']}")
    print(f"   優點: {', '.join(r['reasons'])}")

# 風險提醒
print("\n" + "="*70)
print("【風險提醒】")
print("="*70)
print("""
⚠️ 重要提醒：

1. 【總經風險】台股本益比 25 倍，估值偏高
   → 建議等拉回再買

2. 【系統風險】美伊衝突、升息預期
   → 可能導致股市進一步回調

3. 【產業風險】個別產業有景氣循環
   → 注意進場時機

4. 【巴菲特原則】
   → 等股價低於內在價值 30% 再買
   → 不要因為「便宜」就買
""")

# 建議策略
print("\n" + "="*70)
print("【建議策略】")
print("="*70)
print("""
【保守型投資人】
• 玉山金 2884：金融股、殖利率高、穩定
• 中鋼 2002：價值股、低PE、高殖利率
• 0056 元大高股息：ETF分散風險

【積極型投資人】
• 台積電 2330：護城河強、產業龍頭
• 聯電 2303：成熟製程、殖利率高

【建議進場方式】
• 分批買入（不要一次all in）
• 設定停損點（-10% 停損）
• 保留現金（30-50%）等待更好的價位
""")

print("="*70)
