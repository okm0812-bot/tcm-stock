#!/usr/bin/env python3
"""
完整版 8 維度股票分析器 - 含三大法人買賣超
"""

import json
import urllib.request
import ssl
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

def get_recent_trading_date() -> str:
    """取得最近交易日（週一～五）"""
    today = datetime.now()
    # 如果是週末，回退到週五
    if today.weekday() == 5:  # 週六
        today = today - timedelta(days=1)
    elif today.weekday() == 6:  # 週日
        today = today - timedelta(days=2)
    return today.strftime("%Y%m%d")

def fetch_twse_institutional(stock_id: str, date: str = None) -> Optional[Dict]:
    """從證交所抓取三大法人資料"""
    if date is None:
        date = get_recent_trading_date()
    
    try:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        
        url = f"https://www.twse.com.tw/fund/T86?response=json&date={date}&selectType=ALLBUT0999"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=15, context=ctx) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            if data.get('stat') != 'OK':
                return None
            
            # 尋找指定股票
            for row in data.get('data', []):
                if row[0] == stock_id:
                    return {
                        'date': data.get('date'),
                        'stock_id': row[0],
                        'stock_name': row[1].strip(),
                        'foreign_buy': int(row[2].replace(',', '')),
                        'foreign_sell': int(row[3].replace(',', '')),
                        'foreign_net': int(row[4].replace(',', '')),
                        'trust_buy': int(row[8].replace(',', '')),
                        'trust_sell': int(row[9].replace(',', '')),
                        'trust_net': int(row[10].replace(',', '')),
                        'dealer_net': int(row[11].replace(',', '')),
                        'total_net': int(row[18].replace(',', ''))
                    }
    except Exception as e:
        print(f"Error fetching institutional data: {e}")
    return None

def analyze_institutional(data: Dict) -> Dict[str, Any]:
    """分析三大法人動向"""
    if not data:
        return {"score": 0.0, "note": "無法人資料"}
    
    foreign_net = data['foreign_net']
    trust_net = data['trust_net']
    dealer_net = data['dealer_net']
    total_net = data['total_net']
    
    # 計算分數
    score = 0.0
    notes = []
    
    # 外資
    if foreign_net > 10000:
        score += 0.4
        notes.append(f"外資大買 {foreign_net:,} 張")
    elif foreign_net > 0:
        score += 0.2
        notes.append(f"外資小買 {foreign_net:,} 張")
    elif foreign_net < -10000:
        score -= 0.4
        notes.append(f"外資大賣 {abs(foreign_net):,} 張")
    elif foreign_net < 0:
        score -= 0.2
        notes.append(f"外資小賣 {abs(foreign_net):,} 張")
    
    # 投信
    if trust_net > 5000:
        score += 0.3
        notes.append(f"投信大買 {trust_net:,} 張")
    elif trust_net > 0:
        score += 0.15
        notes.append(f"投信小買 {trust_net:,} 張")
    elif trust_net < -5000:
        score -= 0.3
        notes.append(f"投信大賣 {abs(trust_net):,} 張")
    elif trust_net < 0:
        score -= 0.15
        notes.append(f"投信小賣 {abs(trust_net):,} 張")
    
    # 自營商
    if abs(dealer_net) > 5000:
        notes.append(f"自營商 {dealer_net:,} 張")
    
    return {
        "date": data['date'],
        "外資買賣超": foreign_net,
        "投信買賣超": trust_net,
        "自營商買賣超": dealer_net,
        "三大法人合計": total_net,
        "score": round(score, 2),
        "分析": "; ".join(notes) if notes else "法人動向中性"
    }

def analyze_stock(stock_id: str, stock_name: str = "") -> Dict[str, Any]:
    """8 維度分析（含三大法人）"""
    
    # 抓取三大法人資料
    inst_data = fetch_twse_institutional(stock_id)
    inst_analysis = analyze_institutional(inst_data)
    
    result = {
        "股票代號": stock_id,
        "股票名稱": stock_name or (inst_data['stock_name'] if inst_data else ""),
        "分析時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "資料日期": inst_data['date'] if inst_data else "無資料",
        
        # 維度 1-3: 價格動能、成交量、長期趨勢（需即時報價 API）
        "價格動能": {"score": 0.0, "note": "需即時報價 API"},
        "成交量分析": {"score": 0.0, "note": "需即時報價 API"},
        "長期趨勢": {"score": 0.0, "note": "需歷史價格"},
        
        # 維度 4: 三大法人（✅ 已抓取）
        "法人動向": inst_analysis,
        
        # 維度 5-8: 待補充
        "基本面": {"score": 0.0, "note": "需財報資料"},
        "籌碼分析": {"score": 0.0, "note": "需集保庫存資料"},
        "技術指標": {"score": 0.0, "note": "需歷史價格計算"},
        "市場情緒": {"score": 0.0, "note": "需大盤資料"}
    }
    
    # 計算總分（目前僅有法人維度）
    total_score = inst_analysis['score']
    
    result["總評分"] = round(total_score, 2)
    result["建議"] = "BUY" if total_score > 0.3 else "HOLD" if total_score > -0.3 else "SELL"
    
    return result

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python stock_analyzer_full.py <股票代號>")
        print("範例: python stock_analyzer_full.py 2330")
        print("")
        print("分析你的持股組合:")
        stocks = ["2330", "1101", "2352", "2409", "3311", "6919", "00687B", "00795B"]
        for s in stocks:
            result = analyze_stock(s)
            print(f"\n{s}: {result['建議']} (法人分數: {result['法人動向']['score']})")
        return
    
    stock_id = sys.argv[1]
    result = analyze_stock(stock_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
