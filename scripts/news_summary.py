# -*- coding: utf-8 -*-
"""
自動新聞摘要系統
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

print("\n" + "="*70)
print("【自動新聞摘要】" + datetime.now().strftime('%Y-%m-%d %H:%M'))
print("="*70)

# 你的持股
stocks = [
    {"code": "1101", "name": "台泥", "keywords": ["台泥", "水泥", "中國水泥"]},
    {"code": "2352", "name": "佳世達", "keywords": ["佳世達", "Qisda", "明基"]},
    {"code": "2409", "name": "友達", "keywords": ["友達", "AUO", "面板"]},
    {"code": "6919", "name": "康霈", "keywords": ["康霈", "Camber", "新藥"]},
]

def search_news(keyword, max_results=3):
    """搜尋新聞"""
    try:
        # 使用 Google News RSS
        url = f"https://news.google.com/rss/search?q={keyword}+when:1d&hl=zh-TW"
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'xml')
        
        items = soup.find_all('item')[:max_results]
        news_list = []
        
        for item in items:
            title = item.title.text if item.title else ""
            link = item.link.text if item.link else ""
            pub_date = item.pubDate.text if item.pubDate else ""
            
            # 簡單摘要（取前 50 字）
            summary = title[:50] + "..." if len(title) > 50 else title
            
            news_list.append({
                'title': title,
                'summary': summary,
                'link': link,
                'date': pub_date
            })
        
        return news_list
    except Exception as e:
        return []

def analyze_sentiment(title):
    """簡單情緒分析"""
    positive_words = ['利多', '上漲', '成長', '獲利', '營收', '創高', '買超', '看好']
    negative_words = ['利空', '下跌', '虧損', '衰退', '賣超', '看淡', '裁員', '減產']
    
    title_lower = title.lower()
    
    pos_count = sum(1 for w in positive_words if w in title_lower)
    neg_count = sum(1 for w in negative_words if w in title_lower)
    
    if pos_count > neg_count:
        return "偏多"
    elif neg_count > pos_count:
        return "偏空"
    else:
        return "中性"

# 搜尋每支股票的新聞
all_news = []

for stock in stocks:
    print(f"\n【{stock['name']}】搜尋中...")
    
    # 用第一個關鍵字搜尋
    news = search_news(stock['keywords'][0])
    
    if news:
        print(f"  找到 {len(news)} 則新聞")
        for i, n in enumerate(news[:2], 1):  # 只顯示前 2 則
            sentiment = analyze_sentiment(n['title'])
            print(f"  {i}. {n['summary']}")
            print(f"     情緒: {sentiment}")
            all_news.append({
                'stock': stock['name'],
                'title': n['title'],
                'sentiment': sentiment
            })
    else:
        print(f"  今日無相關新聞")

# 總結
print("\n" + "="*70)
print("【新聞摘要總結】")
print("="*70)

if all_news:
    # 統計情緒
    sentiment_count = {"偏多": 0, "偏空": 0, "中性": 0}
    for n in all_news:
        sentiment_count[n['sentiment']] += 1
    
    print(f"\n今日新聞情緒統計:")
    print(f"  偏多: {sentiment_count['偏多']} 則")
    print(f"  偏空: {sentiment_count['偏空']} 則")
    print(f"  中性: {sentiment_count['中性']} 則")
    
    # 重要新聞
    print(f"\n重要新聞:")
    for n in all_news[:5]:
        print(f"  [{n['stock']}] {n['sentiment']}: {n['title'][:40]}...")
else:
    print("\n今日無重大新聞")

print("\n" + "="*70)
print("【系統限制】")
print("="*70)
print("""
- 新聞來源: Google News RSS
- 更新頻率: 即時
- 情緒分析: 簡單關鍵字比對，僅供參考
- 可能遺漏: 部分新聞可能未收錄
""")

print("="*70)