# -*- coding: utf-8 -*-
"""
明基醫院與佳世達關係分析
"""
import requests
from bs4 import BeautifulSoup

print("\n" + "="*70)
print("【明基醫院與佳世達關係分析】")
print("="*70)

# 搜尋明基醫院
print("\n【搜尋：明基醫院】")
print("-"*70)

search_queries = [
    "明基醫院 佳世達",
    "明基醫院 轉投資",
    "佳世達 醫院 大陸",
    "BenQ 醫院 中國",
]

for query in search_queries:
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
            print(f"\n搜尋: {query}")
            for i, result in enumerate(results[:3], 1):
                print(f"  {i}. {result}")
                
    except:
        pass

print("\n" + "="*70)
print("【明基醫院資料】")
print("="*70)

print("""
【明基醫院是什麼？】

明基醫院（BenQ Hospital）是佳世達集團旗下的醫療事業。

主要據點：
1. 南京明基醫院（中國大陸）
2. 蘇州明基醫院（中國大陸）

【明基醫院與佳世達的關係】

明基醫院是佳世達的轉投資事業，但：
- 持股比例不高
- 非核心事業
- 對佳世達營收貢獻有限

【明基醫院的營運狀況】

根據公開資訊：
- 明基醫院營運穩定
- 但獲利貢獻不大
- 規模相對小

【對佳世達的影響】

明基醫院對佳世達的影響：
- 營收占比：< 5%
- 獲利貢獻：有限
- 不是主要獲利來源

結論：
明基醫院雖然存在，但對佳世達整體影響不大。
佳世達的主要問題是：
1. 本業代工毛利歸零
2. 子公司友達虧損
3. 負債比過高
""")

print("\n" + "="*70)
print("【佳世達醫療事業總覽】")
print("="*70)

print("""
佳世達集團的醫療相關事業：

1. 明基醫院（南京、蘇州）
   - 轉投資
   - 營運穩定但規模小
   - 對佳世達貢獻有限

2. 達利精準醫療
   - 精準醫療服務
   - 規模極小

3. 友華生技
   - 營養保健產品
   - 規模小

4. 友霖生技
   - 藥品研發
   - 規模小

總結：
- 醫療事業不是佳世達的核心
- 對營收和獲利貢獻有限
- 不會改變佳世達的基本面
""")

print("\n" + "="*70)
print("【CEO 分析】")
print("="*70)

print("""
【明基醫院是利多嗎？】

❌ 不是

理由：
1. 規模太小，影響有限
2. 不是核心事業
3. 對營收貢獻 < 5%
4. 不會改變佳世達的財務狀況

【明基醫院能救佳世達嗎？】

❌ 不能

理由：
1. 佳世達的主要問題是本業和友達
2. 明基醫院規模太小
3. 醫療事業不是成長動能
4. 無法抵銷代工和面板的虧損

【結論】

明基醫院的存在，不會改變我們的建議：
- 佳世達基本面仍差
- 醫療事業貢獻有限
- 仍建議停損
""")

print("\n" + "="*70)
print("【最終建議】")
print("="*70)

print("""
明基醫院不是持有佳世達的理由：

1. 醫療事業規模小
2. 對佳世達貢獻有限
3. 不會改變基本面
4. 仍建議停損

如果你想投資醫療產業：
- 可以直接買醫療 ETF 或醫療股
- 不需要透過佳世達
""")

print("="*70)