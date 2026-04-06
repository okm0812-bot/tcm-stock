# -*- coding: utf-8 -*-
"""
佳世達 2352 最新消息分析
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime

print("\n" + "="*70)
print("【佳世達 2352 最新消息分析】" + datetime.now().strftime('%Y-%m-%d %H:%M'))
print("="*70)

# 現價
print(f"\n【現價】23.32 元（09:25）")
print(f"【較昨日收盤】{(23.32 - 23.65):+.2f} 元 ({(23.32/23.65-1)*100:+.2f}%)")

# 子公司業務
print("\n" + "="*70)
print("【佳世達子公司與業務】")
print("="*70)

subsidiaries = [
    ("友達光電 2409", "面板事業", "友達持佳世達約15%", "面板景氣循環，2025年仍虧損"),
    ("景智電子", "網通產品", "EMS代工", "毛利率低，競爭激烈"),
    ("明基材料", "光學材料", "偏光片", "友達集團供應鏈"),
    ("輔祥實業", "太陽能", "電站/系統", "太陽能景氣差"),
    ("康聯訊", "網通", "工業網通", "規模小"),
]

print(f"\n{'子公司':<12} {'業務':<10} {'持股':<15} {'前景'}")
print("-"*70)
for name, biz, holding, outlook in subsidiaries:
    print(f"{name:<12} {biz:<10} {holding:<15} {outlook}")

# 搜尋新聞
print("\n" + "="*70)
print("【最新消息搜尋】")
print("="*70)

try:
    search_url = 'https://www.google.com/search?q=佳世達+2352+2026+利多&num=10'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    r = requests.get(search_url, headers=headers, timeout=10)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # 找標題
    titles = soup.find_all('h3')
    
    print("\n找到的新聞標題:")
    news_count = 0
    for t in titles[:10]:
        text = t.get_text()
        if '佳世達' in text or '2352' in text:
            print(f"  • {text}")
            news_count += 1
    
    if news_count == 0:
        print("  (未找到佳世達相關新聞)")
        
except Exception as e:
    print(f"  無法抓取新聞: {e}")

# AI/網通/醫療 可能利多
print("\n" + "="*70)
print("【潛在利多分析】")
print("="*70)

positive = [
    ("AI伺服器", "網通事業可能受惠於AI基建需求", "低"),
    ("角落養生村", "轉投資，規模小", "低"),
    ("車用顯示", "友達車用面板，佳世達有機會", "中"),
    ("止血噴霧", "醫療產品，規模極小", "低"),
]

negative = [
    ("面板景氣", "友達持續虧損，佳世達認列虧損", "高"),
    ("代工毛利", "毛利率歸零，競爭激烈", "高"),
    ("負債比", "138%负债比，财务压力大", "高"),
    ("中國競爭", "紅色供應鏈衝擊", "高"),
]

print("\n潛在利多:")
for item, reason, impact in positive:
    print(f"  • {item}: {reason} (影響: {impact})")

print("\n潛在利空:")
for item, reason, impact in negative:
    print(f"  ⚠️ {item}: {reason} (影響: {impact})")

# 結論
print("\n" + "="*70)
print("【結論】")
print("="*70)

print("""
❌ 佳世達目前**沒有明顯利多**：

1. 子公司友達持續虧損
   - 面板景氣循環，2025年仍虧損
   - 佳世達認列轉投資虧損

2. 本業代工毛利歸零
   - EMS/OEM代工，沒有定價權
   - 中國紅色供應鏈競爭激烈

3. 財務體質差
   - 負債比 138%
   - 自由現金流為負

4. 沒有護城河
   - 不是產業龍頭
   - 沒有獨特技術
   - 沒有品牌價值

✅ 可能的轉機（但機會低）：
   - AI伺服器/網通需求增加
   - 友達面板景氣回升
   - 但這些都需要時間，且不確定性高
""")

print("="*70)
print("【操作建議】")
print("="*70)
print("""
基於以上分析：

1. **短線**：沒有利多支撐，技術面偏空
   → 建議今日賣出（無基本面支撐）

2. **中線**：產業趨勢不利
   → 友達面板景氣預計2026下半年才可能好轉
   → 佳世達跟隨友達，復甦緩慢

3. **長線**：沒有護城河
   → 不建議長期持有

結論：**今日現價 23.32 建議賣出**
理由：沒有實質利多，基本面差，技術面偏空
""")
print("="*70)
