# -*- coding: utf-8 -*-
"""
融資融券 — TWSE POST 請求測試
"""
import requests
import warnings
warnings.filterwarnings('ignore')

def try_margin_post():
    # TWSE API 測試
    urls_to_try = [
        # 嘗試各種可能的 API
        ('https://www.twse.com.tw/rwd/zh/trading/margin/MI_MARGN', {'date': '20260327'}),
        ('https://www.twse.com.tw/rwd/zh/trading/margin/MI_MARGN', {'date': '20260327', 'response': 'csv'}),
        ('https://www.twse.com.tw/rwd/zh/fund/MI_MARGN', {'date': '20260327'}),
    ]
    
    print(f"\n{'='*60}")
    print(f"[Margin - POST Tests]")
    print(f"{'='*60}\n")
    
    for url, data in urls_to_try:
        print(f"Testing: {url}")
        
        try:
            # GET
            r = requests.get(url, params=data, timeout=10, verify=False)
            print(f"  GET Status: {r.status_code}")
            if r.status_code == 200:
                print(f"  Length: {len(r.text)}")
                print(f"  First 200: {r.text[:200]}")
        
        except Exception as e:
            print(f"  GET Error: {e}")
        
        try:
            # POST
            r = requests.post(url, data=data, timeout=10, verify=False)
            print(f"  POST Status: {r.status_code}")
            if r.status_code == 200:
                print(f"  Length: {len(r.text)}")
                print(f"  First 200: {r.text[:200]}")
        
        except Exception as e:
            print(f"  POST Error: {e}")
        
        print()

    # 嘗試 TAIEX 格式
    print(f"\n{'='*60}")
    print(f"[Try TAIEX-style format]")
    print(f"{'='*60}\n")
    
    # 類似期貨的格式
    twse_margin = 'https://www.twse.com.tw/cht/3/futContractsDateDown'
    # 改成 margin
    margin_url = twse_margin.replace('futContractsDateDown', 'marginDownload')
    
    print(f"Trying: {margin_url}")
    r = requests.get(margin_url, timeout=10, verify=False)
    print(f"Status: {r.status_code}")

if __name__ == '__main__':
    try_margin_post()
