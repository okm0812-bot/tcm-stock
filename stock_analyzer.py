#!/usr/bin/env python3
"""
簡化版 8 維度股票分析器 - 純網路請求，無需 yfinance
"""

import json
import urllib.request
import urllib.error
import ssl
from datetime import datetime
from typing import Dict, Any, Optional

def fetch_twse_data(stock_id: str) -> Optional[Dict]:
    """從台灣證交所抓取即時資料"""
    try:
        # 建立不驗證 SSL 的 context
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stock_id}.tw"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data.get('msgArray'):
                return data['msgArray'][0]
    except Exception as e:
        print(f"Error fetching {stock_id}: {e}")
    return None

def analyze_stock(stock_id: str, stock_name: str = "") -> Dict[str, Any]:
    """8 維度分析"""
    data = fetch_twse_data(stock_id)
    
    if not data:
        return {"error": f"無法取得 {stock_id} 資料"}
    
    # 解析基本資料
    price = float(data.get('z', '0').replace(',', '')) if data.get('z') != '-' else 0
    open_price = float(data.get('o', '0').replace(',', '')) if data.get('o') else 0
    high = float(data.get('h', '0').replace(',', '')) if data.get('h') else 0
    low = float(data.get('l', '0').replace(',', '')) if data.get('l') else 0
    volume = int(data.get('v', '0').replace(',', '')) if data.get('v') else 0
    
    # 52週高低
    high_52w = float(data.get('h52', '0').replace(',', '')) if data.get('h52') else 0
    low_52w = float(data.get('l52', '0').replace(',', '')) if data.get('l52') else 0
    
    # 昨收
    yest = float(data.get('y', '0').replace(',', '')) if data.get('y') else 0
    change_pct = round((price - yest) / yest * 100, 2) if yest > 0 else 0
    
    # 計算維度
    result = {
        "股票代號": stock_id,
        "股票名稱": stock_name or data.get('n', ''),
        "分析時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        
        # 維度 1: 價格動能
        "價格動能": {
            "現價": price,
            "開盤": open_price,
            "最高": high,
            "最低": low,
            "昨收": yest,
            "漲跌": change_pct,
            "振幅": round((high - low) / yest * 100, 2) if yest > 0 else 0,
            "score": 0.5 if change_pct > 0 else -0.3
        },
        
        # 維度 2: 成交量
        "成交量分析": {
            "今日成交量": volume,
            "score": 0.3 if volume > 10000 else 0.0
        },
        
        # 維度 3: 52週區間
        "長期趨勢": {
            "52週高": high_52w,
            "52週低": low_52w,
            "距高點": round((high_52w - price) / high_52w * 100, 1) if high_52w > 0 else 0,
            "距低點": round((price - low_52w) / low_52w * 100, 1) if low_52w > 0 else 0,
            "score": -0.5 if high_52w > 0 and price > high_52w * 0.9 else 0.2
        },
        
        # 維度 4-8: 簡化版
        "基本面": {"score": 0.0, "note": "需財報資料"},
        "法人動向": {"score": 0.0, "note": "需三大法人資料"},
        "籌碼分析": {"score": 0.0, "note": "需集保庫存資料"},
        "技術指標": {"score": 0.0, "note": "需歷史價格計算"},
        "市場情緒": {"score": 0.0, "note": "需大盤資料"}
    }
    
    # 計算總分
    total_score = (
        result["價格動能"]["score"] +
        result["成交量分析"]["score"] +
        result["長期趨勢"]["score"]
    ) / 3
    
    result["總評分"] = round(total_score, 2)
    result["建議"] = "BUY" if total_score > 0.3 else "HOLD" if total_score > -0.3 else "SELL"
    
    return result

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python stock_analyzer.py <股票代號>")
        print("範例: python stock_analyzer.py 2330")
        return
    
    stock_id = sys.argv[1]
    result = analyze_stock(stock_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
