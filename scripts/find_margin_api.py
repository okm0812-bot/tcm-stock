# -*- coding: utf-8 -*-
"""
融資融券 — 找 CSV API
"""
import requests
import warnings
import re
warnings.filterwarnings('ignore')

def find_margin_api():
    url = 'https://www.twse.com.tw/zh/trading/margin/mi-margn.html'
    
    print(f"\n{'='*60}")
    print(f"[Finding Margin CSV API]")
    print(f"{'='*60}\n")
    
    try:
        r = requests.get(url, timeout=15, verify=False)
        text = r.text
        
        # 直接搜 URL
        urls = re.findall(r'href="(https?://[^"]+)"', text)
        
        print("All URLs found:")
        for u in urls[:20]:
            print(f"  {u[:60]}")
        
        # 找包含 csv 或 margin 或 margn 的
        print("\n--- Relevant URLs ---")
        for u in urls:
            if 'csv' in u.lower() or 'margin' in u.lower() or 'margn' in u.lower() or 'download' in u.lower():
                print(f"  {u}")
        
        # 找 form action
        forms = re.findall(r'action="([^"]+)"', text)
        if forms:
            print("\nForms:")
            for f in forms[:10]:
                print(f"  {f}")
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    find_margin_api()
