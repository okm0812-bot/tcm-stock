# -*- coding: utf-8 -*-
"""
融資融券 — WantGoo 解析
URL: https://www.wantgoo.com/stock/margin-trading/market-price/taiex
"""
import requests
import warnings
warnings.filterwarnings('ignore')
import re

def fetch_wantgoo_margin():
    url = 'https://www.wantgoo.com/stock/margin-trading/market-price/taiex'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
    
    print(f"\n{'='*60}")
    print(f"[Margin Trading] WantGoo")
    print(f"{'='*60}\n")
    
    try:
        r = requests.get(url, headers=headers, verify=False, timeout=20)
        text = r.text
        
        print(f"Status: {r.status_code}")
        print(f"Length: {len(text)}")
        
        # 找數字
        numbers = re.findall(r'(\d{4,8})', text)
        unique = sorted(set(numbers), key=lambda x: -int(x))[:20]
        print(f"\nLarge numbers: {unique[:15]}")
        
        # 找 "融資" 或 "融券" 相關
        if '融資' in text:
            print("\n[OK] Found 融資 (Margin) data")
        if '融券' in text:
            print("[OK] Found 融券 (Short Sale) data")
        
        # 找表格
        if '<table' in text:
            print("\n[OK] Found table(s)")
            
    except Exception as e:
        print(f"Error: {e}")
    
    print(f"\n{'='*60}\n")

if __name__ == '__main__':
    fetch_wantgoo_margin()
