# -*- coding: utf-8 -*-
"""
融資融券 — TWSE 正確格式測試
"""
import requests
import warnings
warnings.filterwarnings('ignore')

def test_margin():
    # 類似期貨格式，但用 margin
    # 期貨: https://www.taifex.com.tw/cht/3/futContractsDateDown
    # 融資融券可能是類似的
    
    base = 'https://www.twse.com.tw'
    
    # 測試各種可能的下載 URL
    urls = [
        # 期貨格式替換
        base + '/cht/3/marginDownload',
        base + '/cht/3/marginData',
        base + '/cht/3/margin',
        # 官網格式
        base + '/zh/trading/margin/marginDownload',
        base + '/zh/trading/margin/MI_MARGN',
        base + '/rwd/zh/trading/margin/MI_MARGNCsv',
        base + '/rwd/zh/fund/MI_MARGNCsv',
    ]
    
    print(f"\n{'='*60}")
    print(f"[Testing Margin URLs]")
    print(f"{'='*60}\n")
    
    for url in urls:
        print(f"Testing: {url.split('/')[-1]}")
        
        try:
            r = requests.get(url, timeout=10, verify=False)
            print(f"  Status: {r.status_code}")
            
            if r.status_code == 200 and len(r.text) > 100:
                # 檢查類型
                if 'html' in r.headers.get('Content-Type', '').lower():
                    print(f"  Type: HTML (not CSV)")
                elif 'csv' in r.headers.get('Content-Type', '').lower():
                    print(f"  Type: CSV!")
                    print(f"  Content: {r.text[:200]}")
                    return url
                else:
                    # 檢查內容
                    if '<html' in r.text[:50].lower():
                        print(f"  Type: HTML")
                    elif ',' in r.text[:100]:
                        print(f"  Type: CSV-like")
                        print(f"  Content: {r.text[:300]}")
                        return url
                    else:
                        print(f"  Type: Unknown")
        
        except Exception as e:
            print(f"  Error: {e}")
        
        print()

if __name__ == '__main__':
    test_margin()
