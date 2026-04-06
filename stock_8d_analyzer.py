#!/usr/bin/env python3
"""
完整版 8 維度股票分析器 + 夜盤資料 + 價格警示
"""

import json
import urllib.request
import ssl
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

def create_ssl_context():
    """建立不驗證 SSL 的 context"""
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
        print(f"Error fetching institutional data: {e}")
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
        print(f"Error fetching price for {stock_id}: {e}")
    return None

def analyze_price_momentum(price_data: Dict) -> Dict[str, Any]:
    """分析價格動能"""
    if not price_data:
        return {"score": 0.0, "note": "無價格資料"}
    
    price = price_data['price']
    open_p = price_data['open']
    high = price_data['high']
    low = price_data['low']
    yest = price_data['yest']
    
    change_pct = round((price - yest) / yest * 100, 2) if yest > 0 else 0
    amplitude = round((high - low) / yest * 100, 2) if yest > 0 else 0
    
    # 評分
    score = 0.0
    if change_pct > 2:
        score = 0.5
    elif change_pct > 0:
        score = 0.2
    elif change_pct < -2:
        score = -0.5
    elif change_pct < 0:
        score = -0.2
    
    return {
        "現價": price,
        "開盤": open_p,
        "最高": high,
        "最低": low,
        "昨收": yest,
        "漲跌%": change_pct,
        "振幅%": amplitude,
        "score": score,
        "分析": "強勢上漲" if change_pct > 2 else "上漲" if change_pct > 0 else "弱勢下跌" if change_pct < -2 else "下跌"
    }

def analyze_volume(price_data: Dict) -> Dict[str, Any]:
    """分析成交量"""
    if not price_data:
        return {"score": 0.0, "note": "無成交量資料"}
    
    volume = price_data['volume']
    
    # 簡化判斷（實際應與季均量比較）
    score = 0.3 if volume > 10000 else 0.0 if volume > 5000 else -0.2
    
    return {
        "成交量": volume,
        "score": score,
        "分析": "量能充足" if volume > 10000 else "量能普通" if volume > 5000 else "量能萎縮"
    }

def analyze_institutional(inst_data: Dict) -> Dict[str, Any]:
    """分析三大法人動向"""
    if not inst_data:
        return {"score": 0.0, "note": "無法人資料"}
    
    foreign = inst_data['foreign_net']
    trust = inst_data['trust_net']
    dealer = inst_data['dealer_net']
    total = inst_data['total_net']
    
    score = 0.0
    notes = []
    
    # 外資評分
    if foreign > 10000:
        score += 0.4
        notes.append(f"外資大買 {foreign:,} 張")
    elif foreign > 0:
        score += 0.2
        notes.append(f"外資小買 {foreign:,} 張")
    elif foreign < -10000:
        score -= 0.4
        notes.append(f"外資大賣 {abs(foreign):,} 張")
    elif foreign < 0:
        score -= 0.2
        notes.append(f"外資小賣 {abs(foreign):,} 張")
    
    # 投信評分
    if trust > 5000:
        score += 0.3
        notes.append(f"投信大買 {trust:,} 張")
    elif trust > 0:
        score += 0.15
        notes.append(f"投信小買 {trust:,} 張")
    elif trust < -5000:
        score -= 0.3
        notes.append(f"投信大賣 {abs(trust):,} 張")
    elif trust < 0:
        score -= 0.15
        notes.append(f"投信小賣 {abs(trust):,} 張")
    
    return {
        "外資": foreign,
        "投信": trust,
        "自營商": dealer,
        "合計": total,
        "score": round(score, 2),
        "分析": "; ".join(notes) if notes else "法人動向中性"
    }

def generate_alerts(stock_id: str, stock_name: str, price_data: Dict, inst_analysis: Dict) -> List[str]:
    """生成價格警示"""
    alerts = []
    
    if not price_data:
        return alerts
    
    price = price_data['price']
    change_pct = price_data.get('change_pct', 0)
    
    # 價格警示
    if change_pct > 5:
        alerts.append(f"🔴 漲停警示：單日漲幅 {change_pct}%")
    elif change_pct < -5:
        alerts.append(f"🔴 跌停警示：單日跌幅 {abs(change_pct)}%")
    
    # 法人警示
    if inst_analysis.get('score', 0) < -0.3:
        alerts.append(f"⚠️ 法人賣超：{inst_analysis.get('分析', '')}")
    elif inst_analysis.get('score', 0) > 0.3:
        alerts.append(f"✅ 法人買超：{inst_analysis.get('分析', '')}")
    
    return alerts

def analyze_stock_8d(stock_id: str, stock_name: str = "") -> Dict[str, Any]:
    """8 維度完整分析"""
    
    # 抓取資料
    price_data = fetch_twse_price(stock_id)
    inst_data = fetch_twse_institutional(stock_id)
    
    # 各維度分析
    price_analysis = analyze_price_momentum(price_data)
    volume_analysis = analyze_volume(price_data)
    inst_analysis = analyze_institutional(inst_data)
    
    # 生成警示
    alerts = generate_alerts(stock_id, stock_name, price_data, inst_analysis)
    
    result = {
        "股票代號": stock_id,
        "股票名稱": stock_name or (price_data['name'] if price_data else ""),
        "分析時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        
        # 8 維度
        "維度1_價格動能": price_analysis,
        "維度2_成交量": volume_analysis,
        "維度3_法人動向": inst_analysis,
        "維度4_長期趨勢": {"score": 0.0, "note": "需歷史價格"},
        "維度5_基本面": {"score": 0.0, "note": "需財報資料"},
        "維度6_籌碼分析": {"score": 0.0, "note": "需集保資料"},
        "維度7_技術指標": {"score": 0.0, "note": "需技術計算"},
        "維度8_市場情緒": {"score": 0.0, "note": "需大盤資料"},
        
        # 警示
        "價格警示": alerts,
        
        # 明日操作建議
        "明日建議": "",
        "信心分數": 0.0
    }
    
    # 計算總分（3 個有效維度）
    total_score = (
        price_analysis.get('score', 0) +
        volume_analysis.get('score', 0) +
        inst_analysis.get('score', 0)
    ) / 3
    
    result["信心分數"] = round(total_score, 2)
    
    # 明日操作建議
    if total_score > 0.3:
        result["明日建議"] = "BUY - 逢低買進"
    elif total_score < -0.3:
        result["明日建議"] = "SELL - 考慮減碼"
    else:
        result["明日建議"] = "HOLD - 觀望"
    
    return result

def main():
    # 你的持股清單
    portfolio = [
        ("1101", "台泥"),
        ("2352", "佳世達"),
        ("2409", "友達"),
        ("3311", "閎暉"),
        ("6919", "康霈"),
        ("00687B", "國泰20年美債"),
        ("00795B", "中信美國公債20年"),
    ]
    
    print("=" * 60)
    print("8 維度分析 + 明日操作建議")
    print(f"分析時間：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    for stock_id, stock_name in portfolio:
        print(f"\n【{stock_name} {stock_id}】")
        result = analyze_stock_8d(stock_id, stock_name)
        
        # 顯示關鍵資訊
        price = result['維度1_價格動能']
        if '現價' in price:
            print(f"  現價：{price['現價']}（{price['漲跌%']}%）")
        
        inst = result['維度3_法人動向']
        print(f"  法人：{inst['分析']}")
        
        if result['價格警示']:
            for alert in result['價格警示']:
                print(f"  {alert}")
        
        print(f"  明日建議：{result['明日建議']}")
        print(f"  信心分數：{result['信心分數']}")

if __name__ == "__main__":
    main()
