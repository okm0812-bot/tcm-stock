# -*- coding: utf-8 -*-
"""
TWSE API 修復嘗試 - 三大法人資料抓取
"""
import requests
import urllib3
from datetime import datetime, timedelta
import json

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("="*70)
print("TWSE API 修復測試")
print("="*70)

def get_twse_data(stock_code, date=None):
    """
    嘗試多種方法抓取三大法人資料
    """
    if date is None:
        date = datetime.now()
    
    # 調整到交易日
    while date.weekday() >= 5:
        date -= timedelta(days=1)
    
    date_str = date.strftime('%Y%m%d')
    
    results = {}
    
    # 方法 1: 證交所 API (不驗證 SSL)
    try:
        url1 = f"https://www.twse.com.tw/fund/T86?response=json&date={date_str}&selectType=ALL"
        response = requests.get(url1, verify=False, timeout=15)
        data = response.json()
        
        if data.get('stat') == 'OK' and 'data' in data:
            for row in data['data']:
                if row[0].replace(' ', '') == stock_code:
                    results['method1'] = {
                        'date': date_str,
                        'foreign': int(row[2].replace(',', '')),
                        'investment_trust': int(row[5].replace(',', '')),
                        'dealer': int(row[8].replace(',', '')),
                        'total': int(row[11].replace(',', ''))
                    }
                    break
    except Exception as e:
        results['method1_error'] = str(e)
    
    # 方法 2: 證交所替代端點
    try:
        url2 = f"https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date={date_str}&stockNo={stock_code}"
        response = requests.get(url2, verify=False, timeout=15)
        # 這個端點沒有法人資料，只是測試連線
        results['method2'] = "Endpoint available but no institutional data"
    except Exception as e:
        results['method2_error'] = str(e)
    
    # 方法 3: 使用 FinMind (需要 API key)
    # 這裡只是示範，實際需要申請 API key
    results['method3'] = "FinMind API - requires API key (free registration)"
    
    return results

# 測試股票
test_stocks = ["1101", "2352", "2409"]

print("\n測試抓取三大法人資料...")
print("-"*70)

for stock in test_stocks:
    print(f"\n股票: {stock}")
    results = get_twse_data(stock)
    
    if 'method1' in results:
        data = results['method1']
        print(f"  外資: {data['foreign']:+,.0f} 張")
        print(f"  投信: {data['investment_trust']:+,.0f} 張")
        print(f"  自營商: {data['dealer']:+,.0f} 張")
        print(f"  合計: {data['total']:+,.0f} 張")
    else:
        print(f"  方法 1 失敗: {results.get('method1_error', 'Unknown')}")
        print(f"  方法 2: {results.get('method2', 'N/A')}")
        print(f"  方法 3: {results.get('method3', 'N/A')}")

print("\n" + "="*70)
print("解決方案建議")
print("="*70)

print("""
方案 A: 使用不驗證 SSL (當前測試)
- 優點: 可能可以連上
- 缺點: 安全性較低
- 狀態: 測試中

方案 B: 使用 FinMind API
- 優點: 資料完整、穩定
- 缺點: 需要註冊 API key
- 網址: https://finmindtrade.com/
- 費用: 免費版有限額度

方案 C: 使用證交所替代資料
- 優點: 官方資料
- 缺點: 可能需要不同端點
- 狀態: 需要研究

方案 D: 維持現況 (Yahoo Finance T+1)
- 優點: 穩定、無需額外設定
- 缺點: 資料延遲一天
- 建議: 搭配券商 APP 使用
""")

print("="*70)