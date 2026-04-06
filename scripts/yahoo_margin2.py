# -*- coding: utf-8 -*-
"""
融資融券 — Yahoo 解析
"""
import requests
import re

def fetch_margin():
    url = 'https://tw.stock.yahoo.com/margin-balance'
    
    # 使用 web_fetch 風格的 URL
    api_url = 'https://tw.stock.yahoo.com/_td-stock/api/resource/stockdata;po=0;pz=20;spNa=資券餘額'
    
    print(f"\n{'='*60}")
    print(f"[Margin Trading] Yahoo Finance TW")
    print(f"{'='*60}\n")
    
    # 直接用 Yahoo Finance API
    try:
        r = requests.get(url, timeout=15, verify=False)
        
        # 解析數據 - 找 JSON
        text = r.text
        
        # 找日期和數據
        # 格式: "2026/03/27" 後跟數字
        
        dates = re.findall(r'(\d{4}/\d{2}/\d{2})', text)
        
        if dates:
            # 去重並排序
            unique_dates = sorted(set(dates), reverse=True)[:10]
            print(f"Found {len(unique_dates)} dates\n")
            
            # 解析每一行的數據
            # 找 "日期" 後面的連續數字
            
            for date in unique_dates[:5]:
                # 找日期後的數據
                pattern = f'{date}[^0-9]*([0-9,.]+)'
                matches = re.findall(pattern, text)
                
                print(f"[{date}]")
                if matches:
                    for m in matches[:4]:
                        print(f"  Data: {m[:30]}")
                print()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    fetch_margin()
