# -*- coding: utf-8 -*-
"""
融資融券餘額查詢 — TWSE 公開資料
資料來源：台灣證券交易所
指令：uv run --with requests python scripts/margin_balance.py [stock_code] [date]
"""
import requests
import warnings
warnings.filterwarnings('ignore')
import sys
import json
import re

def fetch_margin_balance(stock_code='2409', date='20260326'):
    """抓取融資融券餘額"""
    
    print(f"\n{'='*80}")
    print(f"[Margin & Short Sale Balance] {stock_code} - {date[:4]}/{date[4:6]}/{date[6:8]}")
    print(f"{'='*80}\n")
    
    # TWSE 融資融券 API
    # 嘗試多個可能的端點
    urls = [
        # 端點 1：融資融券日報
        f'https://www.twse.com.tw/rwd/en/fund/MI_MARGN?date={date}&response=json&selectType=ALL',
        # 端點 2：融資融券統計
        f'https://www.twse.com.tw/rwd/en/stat/MI_MARGNSTAT?date={date}&response=json',
    ]
    
    for i, url in enumerate(urls):
        print(f"Trying endpoint {i+1}...")
        
        try:
            r = requests.get(
                url, 
                headers={'User-Agent': 'Mozilla/5.0'}, 
                verify=False, 
                timeout=15
            )
            
            print(f"  Status: {r.status_code}")
            
            if r.status_code == 200:
                try:
                    data = r.json()
                    
                    if data.get('stat') == 'OK':
                        print(f"  [SUCCESS] Got data!\n")
                        
                        # 顯示標題
                        if 'title' in data:
                            print(f"Title: {data['title']}\n")
                        
                        # 解析數據
                        if 'data' in data:
                            # 找目標股票
                            for row in data['data']:
                                if len(row) > 0 and row[0] == stock_code:
                                    print(f"[{stock_code}]")
                                    print(f"  Margin Buy:    {row[1] if len(row) > 1 else 'N/A'}")
                                    print(f"  Margin Sell:   {row[2] if len(row) > 2 else 'N/A'}")
                                    print(f"  Margin Balance:{row[3] if len(row) > 3 else 'N/A'}")
                                    if len(row) > 6:
                                        print(f"  Short Balance:  {row[6]}")
                                    return
                            
                            # 如果沒找到，顯示前幾筆
                            print(f"Stock {stock_code} not in top results")
                            print(f"Sample data (first 3 rows):")
                            for row in data['data'][:3]:
                                print(f"  {row[:5]}")
                        else:
                            print(f"  No 'data' field in response")
                            print(f"  Keys: {list(data.keys())}")
                    
                    else:
                        print(f"  Status: {data.get('stat', 'Unknown')}")
                
                except json.JSONDecodeError:
                    print(f"  Not JSON, showing HTML snippet:")
                    print(f"  {r.text[:300]}")
        
        except Exception as e:
            print(f"  Error: {e}")
    
    print(f"\n{'='*80}")
    print("Note: TWSE margin data may require specific parameters")
    print("Alternative: Check Goodinfo manually")
    print(f"{'='*80}\n")

if __name__ == '__main__':
    code = sys.argv[1] if len(sys.argv) > 1 else '2409'
    date = sys.argv[2] if len(sys.argv) > 2 else '20260326'
    fetch_margin_balance(code, date)
