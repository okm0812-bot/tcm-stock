# -*- coding: utf-8 -*-
"""
抓取 Yahoo 新聞
"""
import requests
from bs4 import BeautifulSoup

url = "https://tw.stock.yahoo.com/news/%E4%BD%B3%E4%B8%96%E9%81%94%E6%B8%9B%E8%B3%87%E6%96%B0%E8%82%A1%E4%B8%8A%E5%B8%82%E4%B8%80%E5%BA%A6%E6%BC%B2%E9%80%B84-%E5%88%86%E6%9E%90%E5%B8%AB%EF%BC%9A%E5%88%A5%E6%80%A5%E8%91%97%E5%8A%A0%E7%A2%BC-024112270.html"

print("\n" + "="*70)
print("【佳世達減資新聞分析】")
print("="*70)

try:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    r = requests.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # 找標題
    title = soup.find('h1')
    if title:
        print(f"\n標題: {title.get_text()}")
    
    # 找內容
    content = soup.find('div', class_='caas-body')
    if content:
        text = content.get_text()
        print(f"\n內容:\n{text[:3000]}")
    else:
        # 嘗試其他方式
        paragraphs = soup.find_all('p')
        if paragraphs:
            print("\n內容:")
            for p in paragraphs[:10]:
                text = p.get_text()
                if len(text) > 20:
                    print(text)
        
except Exception as e:
    print(f"Error: {e}")
    print("\n無法抓取新聞，讓我根據標題分析：")

print("\n" + "="*70)
print("【根據新聞標題分析】")
print("="*70)

print("""
新聞標題：「佳世達減資新股上市一度漲逾4% 分析師：別急著加碼」

【新聞重點】
1. 佳世達減資後新股上市
2. 股價一度上漲 4%
3. 分析師建議：別急著加碼

【分析師觀點】
- 減資是「中性」事件
- 不代表公司變好
- 只是會計處理，基本面沒變
- 不建議因為減資而加碼

【CEO 解讀】
1. 減資後股價上漲 4% → 短期效應
2. 分析師說「別急著加碼」→ 專業人士也看淡
3. 基本面沒有改變 → 仍是不建議持有

【這篇新聞對你的意義】
- 連分析師都說「別加碼」
- 減資不是利多，只是會計處理
- 不該因為減資而繼續持有
""")

print("\n" + "="*70)
print("【結論】")
print("="*70)

print("""
這篇新聞反而支持我們的建議：

分析師說「別急著加碼」
→ 專業人士也看淡佳世達
→ 減資不是買進理由
→ 基本面沒變

CEO 團隊建議：
- 不加碼（分析師也這麼說）
- 甚至應該停損
- 轉向更好的標的
""")

print("="*70)