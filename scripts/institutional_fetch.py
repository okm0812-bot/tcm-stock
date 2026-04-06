# -*- coding: utf-8 -*-
"""
三大法人資料自動抓取
資料來源: 台灣證券交易所 (TWSE)
"""
import requests
from datetime import datetime, timedelta
import json
import os

def get_twse_date_str(date):
    """轉換日期格式為 TWSE 格式 (YYYYMMDD)"""
    return date.strftime('%Y%m%d')

def fetch_institutional_data(stock_code, date=None):
    """
    抓取三大法人買賣超資料
    資料來源: 證交所每日收盤資料
    """
    if date is None:
        date = datetime.now()
    
    # 如果是周末，往前推到周五
    while date.weekday() >= 5:  # 5=周六, 6=周日
        date -= timedelta(days=1)
    
    date_str = get_twse_date_str(date)
    
    try:
        # TWSE API endpoint
        url = f"https://www.twse.com.tw/fund/T86?response=json&date={date_str}&selectType=ALL"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        
        if data['stat'] == 'OK' and 'data' in data:
            # 尋找指定股票
            for row in data['data']:
                if row[0].replace(' ', '') == stock_code:
                    return {
                        'date': date_str,
                        'stock_code': stock_code,
                        'foreign': int(row[2].replace(',', '')),      # 外資
                        'investment_trust': int(row[5].replace(',', '')),  # 投信
                        'dealer': int(row[8].replace(',', '')),       # 自營商
                        'total': int(row[11].replace(',', ''))        # 合計
                    }
        
        return None
        
    except Exception as e:
        print(f"抓取失敗: {e}")
        return None

def analyze_institutional(data):
    """分析三大法人動向"""
    if not data:
        return "無資料"
    
    total = data['total']
    
    if total > 1000:
        return "強力買超"
    elif total > 0:
        return "買超"
    elif total > -1000:
        return "賣超"
    else:
        return "強力賣超"

# 主程式
print("\n" + "="*70)
print("【三大法人資料抓取】" + datetime.now().strftime('%Y-%m-%d %H:%M'))
print("="*70)
print("\n資料來源: 台灣證券交易所")
print("更新時間: 每日收盤後 15:00")
print("="*70)

# 你的持股
stocks = [
    {"code": "1101", "name": "台泥"},
    {"code": "2352", "name": "佳世達"},
    {"code": "2409", "name": "友達"},
    {"code": "6919", "name": "康霈"},
]

print("\n【今日三大法人買賣超】")
print("-"*70)
print(f"{'股票':<10} {'外資':>10} {'投信':>10} {'自營商':>10} {'合計':>10} {'判讀':>10}")
print("-"*70)

for stock in stocks:
    data = fetch_institutional_data(stock['code'])
    
    if data:
        analysis = analyze_institutional(data)
        print(f"{stock['name']:<10} {data['foreign']:>+10,} {data['investment_trust']:>+10,} {data['dealer']:>+10,} {data['total']:>+10,} {analysis:>10}")
    else:
        print(f"{stock['name']:<10} {'無資料':>10} {'無資料':>10} {'無資料':>10} {'無資料':>10} {'無資料':>10}")

print("-"*70)

print("\n【說明】")
print("- 外資: 外國機構投資人")
print("- 投信: 國內投信基金")
print("- 自營商: 證券商自營部門")
print("- 合計: 三大法人總和")
print("- 單位: 張 (1張 = 1,000股)")

print("\n【判讀標準】")
print("- 強力買超: 合計 > 1,000張")
print("- 買超: 合計 > 0張")
print("- 賣超: 合計 < 0張")
print("- 強力賣超: 合計 < -1,000張")

print("\n【系統限制】")
print("- 資料來源: TWSE 官方 API")
print("- 更新時間: 每日收盤後")
print("- 假日無資料")
print("- 可能因網路問題抓取失敗")

print("="*70)