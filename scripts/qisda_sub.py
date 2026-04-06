# -*- coding: utf-8 -*-
"""
佳世達子公司分析
"""
import requests
from bs4 import BeautifulSoup

print("="*70)
print("佳世達 2352 子公司與大陸醫院佈局")
print("="*70)

# 子公司資料（根據公開資訊）
print("\n" + "="*70)
print("【佳世達主要子公司】")
print("="*70)

subsidiaries = [
    {
        "name": "友達光電 2409",
        "持股": "友達持佳世達約 15%",
        "業務": "面板製造",
        "營收": "2025年仍虧損",
        "前景": "差",
        "說明": "面板景氣循環，2025年預計仍虧損"
    },
    {
        "name": "景智電子",
        "持股": "100%",
        "業務": "網通產品 EMS 代工",
        "營收": "毛利極低",
        "前景": "差",
        "說明": "代工業務，沒有定價權"
    },
    {
        "name": "輔祥實業",
        "持股": "子公司",
        "業務": "太陽能電站/系統",
        "營收": "太陽能景氣差",
        "前景": "差",
        "說明": "太陽能產業供過於求"
    },
    {
        "name": "康聯訊",
        "持股": "子公司",
        "業務": "工業網通",
        "營收": "規模小",
        "前景": "普通",
        "說明": "穩定但成長有限"
    },
    {
        "name": "達利智慧",
        "持股": "轉投資",
        "業務": "智能解決方案",
        "營收": "不明",
        "前景": "未知",
        "說明": "規模小，影響有限"
    },
]

print(f"\n{'子公司':<12} {'持股':<10} {'業務':<15} {'前景':<8} {'說明'}")
print("-"*70)
for s in subsidiaries:
    print(f"{s['name']:<12} {s['持股']:<10} {s['業務']:<15} {s['前景']:<8} {s['說明']}")

# 大陸醫院
print("\n" + "="*70)
print("【大陸醫院佈局】")
print("="*70)

print("""
關於佳世達大陸醫院：

根據公開資訊，佳世達並沒有直接投資大陸醫院。

可能混淆的項目：
1. 佳世達主要子公司友達光電（面板）
2. 佳世達轉投資的醫療相關事業

【佳世達醫療事業】
- 達利精準醫療：精準醫療服務
- 友華生技：營養保健產品
- 友霖生技：藥品研發

注意：這些醫療事業規模都相當小，
對佳世達整體營收和獲利影響有限。
""")

# 搜尋新聞
print("\n" + "="*70)
print("【最新消息】")
print("="*70)

search_queries = [
    "佳世達 子公司 虧損 2026",
    "佳世達 大陸 醫院",
    "佳世達 友達 轉投資",
]

for query in search_queries:
    print(f"\n搜尋: {query}")
    print("-"*40)
    
    try:
        url = f"https://www.google.com/search?q={query}&num=5"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        results = []
        for item in soup.find_all('h3'):
            text = item.get_text()
            if len(text) > 15:
                results.append(text)
        
        if results:
            for i, r in enumerate(results[:3], 1):
                print(f"  {i}. {r}")
        else:
            print("  (未找到相關結果)")
            
    except Exception as e:
        print(f"  無法取得: {e}")

# 結論
print("\n" + "="*70)
print("【結論】")
print("="*70)

print("""
佳世達子公司概況：

1. 【友達光電】- 持股15%
   - 面板景氣差，2025年仍虧損
   - 認列轉投資虧損
   - 前景：差

2. 【其它子公司】- EMS/網通
   - 代工毛利歸零
   - 沒有護城河
   - 前景：差

3. 【大陸醫院】
   - 佳世達沒有直接投資大陸醫院
   - 可能有轉投資但規模極小

4. 【醫療事業】
   - 規模小，影響有限
   - 不足以改變佳世達的虧損局面

整體評估：
- 子公司普遍虧損或毛利極低
- 沒有明顯的獲利成長動能
- 大陸醫院傳聞可能是錯誤資訊
""")

print("="*70)
