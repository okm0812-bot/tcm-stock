# -*- coding: utf-8 -*-
"""
即時新聞情緒警示 — 使用 agent-reach 搜尋最新新聞
資料來源：Google News / 財經新聞
指令：uv run --with requests python scripts/news_sentiment.py [stock_code]
"""
import requests
import warnings
warnings.filterwarnings('ignore')
import sys
from datetime import datetime, timedelta

def fetch_news_sentiment(stock_code='2409'):
    """抓取最新新聞並判斷情緒"""
    
    print(f"\n{'='*70}")
    print(f"[News Sentiment Alert] {stock_code}")
    print(f"{'='*70}\n")
    
    # 使用 Google News API (無需 API key)
    # 或使用 NewsAPI 免費版
    
    # 方案 1: 使用 Exa 搜尋（如果有 API key）
    # 方案 2: 使用 Google News RSS
    
    url = f'https://news.google.com/rss/search?q={stock_code}%20stock&hl=en&gl=US&ceid=US:en'
    
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        
        if r.status_code == 200:
            print("[SUCCESS] Fetched Google News RSS")
            print(f"Response length: {len(r.text)} chars\n")
            
            # 簡單的 XML 解析
            import xml.etree.ElementTree as ET
            try:
                root = ET.fromstring(r.text)
                items = root.findall('.//item')
                
                print(f"Found {len(items)} news items:\n")
                
                for i, item in enumerate(items[:5]):
                    title = item.find('title')
                    link = item.find('link')
                    pubDate = item.find('pubDate')
                    
                    if title is not None:
                        title_text = title.text
                        print(f"[{i+1}] {title_text[:70]}")
                        
                        # 簡單情緒判斷
                        negative_words = ['down', 'loss', 'decline', 'fall', 'crash', 'risk', 'concern']
                        positive_words = ['up', 'gain', 'rise', 'surge', 'strong', 'growth', 'bullish']
                        
                        title_lower = title_text.lower()
                        neg_count = sum(1 for w in negative_words if w in title_lower)
                        pos_count = sum(1 for w in positive_words if w in title_lower)
                        
                        if neg_count > pos_count:
                            sentiment = "[BEARISH]"
                        elif pos_count > neg_count:
                            sentiment = "[BULLISH]"
                        else:
                            sentiment = "[NEUTRAL]"
                        
                        print(f"    Sentiment: {sentiment}")
                        if pubDate is not None:
                            print(f"    Date: {pubDate.text[:20]}")
                        print()
                
            except Exception as e:
                print(f"XML parse error: {e}")
        else:
            print(f"[ERROR] Status {r.status_code}")
    
    except Exception as e:
        print(f"[ERROR] {e}")
    
    print(f"\n{'='*70}")
    print("Note: For production use, integrate with:")
    print("  - NewsAPI (newsapi.org)")
    print("  - Exa Search API")
    print("  - CMoney / Goodinfo news feeds")
    print(f"{'='*70}\n")

if __name__ == '__main__':
    code = sys.argv[1] if len(sys.argv) > 1 else '2409'
    fetch_news_sentiment(code)
