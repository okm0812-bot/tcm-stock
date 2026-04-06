# -*- coding: utf-8 -*-
"""
融資融券 — 找正確的下載API
"""
import requests
import warnings
warnings.filterwarnings('ignore')

def find_margin_api():
    # 找TWSE的下載API
    base = 'https://www.twse.com.tw'
    
    apis = [
        # 嘗試各種可能的下載路徑
        '/rwd/zh/fund/MI_MARGN?download&response=csv',
        '/rwd/zh/fund/MI_MARGN?download=csv',
        '/rwd/zh/trading/margin/MI_MARGN?download',
        '/rwd/zh/trading/margin/MI_MARGNCSV',
        '/rwd/zh/trading/margin/MI_MARGNCsv',
    ]
    
    print(f"\n{'='*60}")
    print(f"[Finding Margin API]")
    print(f"{'='*60}\n")
    
    for api in apis:
        url = base + api
        print(f"Testing: {api}")
        
        try:
            r = requests.get(url, timeout=10, verify=False)
            print(f"  Status: {r.status_code}")
            
            if r.status_code == 200 and len(r.text) > 500:
                print(f"  Length: {len(r.text)}")
                print(f"  First 300: {r.text[:300]}")
                print(f"  -> SUCCESS!")
                break
                
        except Exception as e:
            print(f"  Error: {e}")
        print()
    
    print(f"{'='*60}\n")

if __name__ == '__main__':
    find_margin_api()
