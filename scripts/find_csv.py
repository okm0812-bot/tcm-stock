# -*- coding: utf-8 -*-
"""
融資融券 — 找 CSV 下載連結
"""
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')

def find_csv_links():
    # WantGoo
    urls = [
        ('WantGoo', 'https://www.wantgoo.com/stock/margin-trading/market-price/taiex'),
        ('TWSE', 'https://www.twse.com.tw/zh/trading/margin/mi-margn.html'),
    ]
    
    for name, url in urls:
        print(f"\n{'='*60}")
        print(f"[{name}]")
        print(f"{'='*60}\n")
        
        try:
            r = requests.get(url, timeout=15, verify=False)
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # 找所有連結
            links = soup.find_all('a')
            
            csv_links = []
            for link in links:
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                # 找 CSV 相關連結
                if 'csv' in href.lower() or 'csv' in text.lower() or 'download' in href.lower() or '下載' in text:
                    csv_links.append((text, href))
            
            if csv_links:
                print("Found CSV/Download links:")
                for text, href in csv_links[:10]:
                    print(f"  Text: {text[:30]}")
                    print(f"  URL: {href[:80]}")
                    print()
            else:
                print("No CSV links found")
                # 顯示所有連結
                print("\nAll links:")
                for link in links[:15]:
                    href = link.get('href', '')
                    text = link.get_text(strip=True)[:30]
                    if href:
                        print(f"  {text}: {href[:50]}")
        
        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    find_csv_links()
