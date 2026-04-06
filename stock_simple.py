#!/usr/bin/env python3
"""
完整版 8 維度股票分析器 + 明日操作建議
"""

import json
import urllib.request
import ssl
import sys
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

# 設定 stdout 編碼
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='ignore')

def create_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def fetch_twse_institutional(stock_id: str, date: str = None) -> Optional[Dict]:
    """從證交所抓取三大法人資料"""
    if date is None:
        date = datetime.now().strftime("%Y%m%d")
    
    try:
        ctx = create_ssl_context()
        url = f"https://www.twse.com.tw/fund/T86?response=json&date={date}&selectType=ALLBUT0999"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get('stat') != 'OK':
                return None
            
            for row in data.get('data', []):
                if row[0] == stock_id:
                    return {
                        'date': data.get('date'),
                        'stock_id': row[0],
                        'stock_name': row[1].strip(),
                        'foreign_net': int(row[4].replace(',', '')),
                        'trust_net': int(row[10].replace(',', '')),
                        'dealer_net': int(row[11].replace(',', '')),
                        'total_net': int(row[18].replace(',', ''))
                    }
    except Exception as e:
        print(f"Error: {e}")
    return None

def fetch_twse_price(stock_id: str) -> Optional[Dict]:
    """從證交所抓取即時報價"""
    try:
        ctx = create_ssl_context()
        url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stock_id}.tw"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('msgArray'):
                d = data['msgArray'][0]
                return {
                    'price': float(d.get('z', '0').replace(',', '')) if d.get('z') != '-' else 0,
                    'open': float(d.get('o', '0').replace(',', '')) if d.get('o') else 0,
                    'high': float(d.get('h', '0').replace(',', '')) if d.get('h') else 0,
                    'low': float(d.get('l', '0').replace(',', '')) if d.get('l') else 0,
                    'volume': int(d.get('v', '0').replace(',', '')) if d.get('v') else 0,
                    'yest': float(d.get('y', '0').replace(',', '')) if d.get('y') else 0,
                    'name': d.get('n', '')
                }
    except Exception as e:
        print(f"Error: {e}")
    return None

def analyze_stock(stock_id: str, stock_name: str = "") -> Dict:
    """分析單一股票"""
    price_data = fetch_twse_price(stock_id)
    inst_data = fetch_twse_institutional(stock_id)
    
    result = {
        "stock_id": stock_id,
        "stock_name": stock_name,
        "price": price_data['price'] if price_data else 0,
        "change_pct": round((price_data['price'] - price_data['yest']) / price_data['yest'] * 100, 2) if price_data and price_data['yest'] else 0,
        "volume": price_data['volume'] if price_data else 0,
        "foreign_net": inst_data['foreign_net'] if inst_data else 0,
        "trust_net": inst_data['trust_net'] if inst_data else 0,
        "total_net": inst_data['total_net'] if inst_data else 0,
    }
    
    # 計算分數
    score = 0.0
    
    # 價格分數
    if result['change_pct'] > 2:
        score += 0.3
    elif result['change_pct'] < -2:
        score -= 0.3
    
    # 法人分數
    if result['foreign_net'] > 10000:
        score += 0.4
    elif result['foreign_net'] < -10000:
        score -= 0.4
    
    if result['trust_net'] > 5000:
        score += 0.3
    elif result['trust_net'] < -5000:
        score -= 0.3
    
    result['score'] = round(score, 2)
    
    # 明日建議
    if score > 0.3:
        result['signal'] = "BUY"
    elif score < -0.3:
        result['signal'] = "SELL"
    else:
        result['signal'] = "HOLD"
    
    return result

def main():
    portfolio = [
        ("1101", "台泥"),
        ("2352", "佳世達"),
        ("2409", "友達"),
        ("3311", "閎暉"),
        ("6919", "康霈"),
    ]
    
    print("=" * 60)
    print("8維度分析 + 明日操作建議")
    print(f"時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    for stock_id, stock_name in portfolio:
        r = analyze_stock(stock_id, stock_name)
        
        print(f"\n[{r['stock_name']} {r['stock_id']}]")
        print(f"  收盤: {r['price']:.2f} ({r['change_pct']:+.2f}%)")
        print(f"  成交量: {r['volume']:,} 張")
        print(f"  外資: {r['foreign_net']:+,.0f} 張")
        print(f"  投信: {r['trust_net']:+,.0f} 張")
        print(f"  合計: {r['total_net']:+,.0f} 張")
        print(f"  分數: {r['score']}")
        print(f"  明日: {r['signal']}")

if __name__ == "__main__":
    main()
