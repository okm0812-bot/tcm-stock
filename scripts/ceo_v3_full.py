# -*- coding: utf-8 -*-
"""
CEO 分析系統 v3.0 - 完整升級版
包含：自動排程 + 異常通知 + 歷史追蹤
"""
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import json
import subprocess

# ============ 設定 ============
CACHE_FILE = "stock_cache.json"
HISTORY_FILE = "portfolio_history.json"
ALERT_CONFIG = {
    "stop_loss": {  # 停損設定
        "2352.TW": 22.00,  # 佳世達
    },
    "target_profit": {},  # 獲利了結價
    "volume_spike": 2.0,  # 成交量爆量倍數
}
CACHE_DURATION = 300  # 5分鐘

# ============ 快取功能 ============
def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f)

def get_stock_data(code, cache):
    now = datetime.now().timestamp()
    if code in cache:
        cached_time = cache[code].get('timestamp', 0)
        if now - cached_time < CACHE_DURATION:
            return cache[code]['data'], True
    
    try:
        stock = yf.Ticker(code)
        info = stock.info
        data = {
            'price': info.get('regularMarketPrice', 0),
            'prev_close': info.get('regularMarketPreviousClose', 0),
            'low_52': info.get('fiftyTwoWeekLow', 0),
            'high_52': info.get('fiftyTwoWeekHigh', 0),
            'volume': info.get('regularMarketVolume', 0),
            'avg_volume': info.get('averageVolume', 0),
            'inst_hold': info.get('heldPercentInstitutions', 0),
        }
        cache[code] = {'timestamp': now, 'data': data}
        return data, False
    except:
        return None, False

# ============ 歷史追蹤 ============
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)

def record_portfolio(holdings, cache):
    """記錄今日持股狀況"""
    history = load_history()
    
    record = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.now().strftime('%H:%M'),
        'holdings': []
    }
    
    total_value = 0
    total_cost = 0
    
    for h in holdings:
        data, _ = get_stock_data(h['code'], cache)
        if data:
            price = data['price']
            value = price * h['shares']
            cost = h['cost'] * h['shares']
            loss = value - cost
            loss_pct = (price - h['cost']) / h['cost'] * 100
            
            total_value += value
            total_cost += cost
            
            record['holdings'].append({
                'name': h['name'],
                'price': price,
                'shares': h['shares'],
                'value': value,
                'loss': loss,
                'loss_pct': loss_pct
            })
    
    record['total_value'] = total_value
    record['total_cost'] = total_cost
    record['total_loss'] = total_value - total_cost
    record['total_loss_pct'] = (total_value - total_cost) / total_cost * 100
    
    history.append(record)
    
    # 只保留最近 90 天
    if len(history) > 90:
        history = history[-90:]
    
    save_history(history)
    return record

# ============ 異常通知 ============
def check_alerts(holdings, cache):
    """檢查異常情況"""
    alerts = []
    
    for h in holdings:
        data, _ = get_stock_data(h['code'], cache)
        if not data:
            continue
        
        price = data['price']
        code = h['code']
        name = h['name']
        
        # 1. 停損檢查
        if code in ALERT_CONFIG['stop_loss']:
            stop_price = ALERT_CONFIG['stop_loss'][code]
            if price <= stop_price:
                alerts.append({
                    'level': 'CRITICAL',
                    'type': 'STOP_LOSS',
                    'stock': name,
                    'message': f'{name} 觸及停損價 {stop_price}！現價 {price}'
                })
        
        # 2. 52週低點檢查
        low_52 = data['low_52']
        if price <= low_52 * 1.05:
            alerts.append({
                'level': 'WARNING',
                'type': 'NEAR_52W_LOW',
                'stock': name,
                'message': f'{name} 接近 52 週低點！現價 {price}，低點 {low_52}'
            })
        
        # 3. 虧損超過 50% 檢查
        loss_pct = (price - h['cost']) / h['cost'] * 100
        if loss_pct < -50:
            alerts.append({
                'level': 'CRITICAL',
                'type': 'MAJOR_LOSS',
                'stock': name,
                'message': f'{name} 虧損超過 50%！目前 {loss_pct:.1f}%'            })
        
        # 4. 成交量爆量檢查
        volume = data['volume']
        avg_volume = data['avg_volume']
        if avg_volume and volume > avg_volume * ALERT_CONFIG['volume_spike']:
            alerts.append({
                'level': 'INFO',
                'type': 'VOLUME_SPIKE',
                'stock': name,
                'message': f'{name} 成交量爆量！{volume/avg_volume:.1f} 倍於平均'
            })
    
    return alerts

# ============ 新聞摘要 ============
def search_news(keyword, max_results=2):
    try:
        url = f"https://news.google.com/rss/search?q={keyword}+when:1d&hl=zh-TW"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')[:max_results]
        
        news_list = []
        for item in items:
            title = item.title.text if item.title else ""
            news_list.append(title)
        return news_list
    except:
        return []

# ============ 主程式 ============
def main():
    lines = []
    def add(text):
        lines.append(text)
    
    # 標題
    add("")
    add("="*70)
    add("CEO ANALYSIS SYSTEM v3.0 - DAILY REPORT")
    add("Features: Auto-schedule + Alerts + History")
    add("="*70)
    add(f"Report Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # 載入快取
    cache = load_cache()
    
    # 持股資料
    holdings = [
        {"code": "1101.TW", "name": "TAIWAN CEMENT", "shares": 19000, "cost": 34.56},
        {"code": "2352.TW", "name": "QISDA", "shares": 6000, "cost": 53.78},
        {"code": "2409.TW", "name": "AUO", "shares": 9000, "cost": 16.20},
        {"code": "6919.TW", "name": "CAMBER", "shares": 300, "cost": 102.36},
    ]
    
    # 一、持股現況
    add("\n[1. PORTFOLIO STATUS]")
    add("-"*70)
    add(f"{'STOCK':<15} {'PRICE':>8} {'CHANGE':>8} {'VALUE':>12} {'P&L':>12} {'RETURN':>8}")
    add("-"*70)
    
    total_value = 0
    total_cost = 0
    
    for h in holdings:
        data, is_cached = get_stock_data(h['code'], cache)
        if data:
            price = data['price']
            prev_close = data['prev_close']
            change = price - prev_close if prev_close else 0
            value = price * h['shares']
            cost = h['cost'] * h['shares']
            loss = value - cost
            loss_pct = (price - h['cost']) / h['cost'] * 100
            total_value += value
            total_cost += cost
            cache_str = "[C]" if is_cached else "[L]"
            add(f"{h['name']:<15} {price:>8.2f} {change:>+7.2f} {value:>12,.0f} {loss:>+11,.0f} {loss_pct:>+7.1f}% {cache_str}")
    
    add("-"*70)
    total_loss = total_value - total_cost
    total_loss_pct = total_loss / total_cost * 100
    add(f"{'TOTAL':<15} {'':8} {'':8} {total_value:>12,.0f} {total_loss:>+11,.0f} {total_loss_pct:>+7.1f}%")
    
    save_cache(cache)
    
    # 二、記錄歷史
    add("\n" + "="*70)
    add("[2. HISTORY TRACKING]")
    add("="*70)
    
    record = record_portfolio(holdings, cache)
    history = load_history()
    
    add(f"Today's record saved. Total records: {len(history)}")
    
    # 顯示最近 5 天總資產變化
    if len(history) >= 2:
        add("\nRecent 5-day total value trend:")
        for h_rec in history[-5:]:
            add(f"  {h_rec['date']}: ${h_rec['total_value']:,.0f} ({h_rec['total_loss_pct']:+.1f}%)")
    
    # 三、異常通知
    add("\n" + "="*70)
    add("[3. ALERTS]")
    add("="*70)
    
    alerts = check_alerts(holdings, cache)
    
    critical_alerts = [a for a in alerts if a['level'] == 'CRITICAL']
    warning_alerts = [a for a in alerts if a['level'] == 'WARNING']
    info_alerts = [a for a in alerts if a['level'] == 'INFO']
    
    if critical_alerts:
        add("\n!!! CRITICAL ALERTS !!!")
        for a in critical_alerts:
            add(f"  [CRITICAL] {a['message']}")
    
    if warning_alerts:
        add("\n! WARNING ALERTS !")
        for a in warning_alerts:
            add(f"  [WARNING] {a['message']}")
    
    if info_alerts:
        add("\nINFO:")
        for a in info_alerts:
            add(f"  [INFO] {a['message']}")
    
    if not alerts:
        add("[OK] No alerts today")
    
    # 四、新聞摘要
    add("\n" + "="*70)
    add("[4. NEWS SUMMARY]")
    add("="*70)
    
    news_keywords = [
        ("TAIWAN CEMENT", "台泥 水泥"),
        ("QISDA", "佳世達"),
        ("AUO", "友達 面板"),
        ("MARKET", "台股 加權指數")
    ]
    
    for name, keyword in news_keywords:
        news = search_news(keyword)
        if news:
            add(f"\n{name}:")
            for i, n in enumerate(news[:2], 1):
                add(f"  {i}. {n[:50]}...")
        else:
            add(f"\n{name}: No major news today")
    
    # 五、今日建議
    add("\n" + "="*70)
    add("[5. TODAY'S RECOMMENDATIONS]")
    add("="*70)
    
    if critical_alerts:
        add("ACTION REQUIRED:")
        for a in critical_alerts:
            add(f"  - {a['message']}")
    
    add("""
Regular recommendations:
1. QISDA: Stop loss at 22.00 for remaining 6,000 shares
2. TAIWAN CEMENT: Hold, wait for Russia-Ukraine war end catalyst
3. AUO & CAMBER: Continue monitoring
4. Check broker APP for institutional trading data daily
""")
    
    # 系統資訊
    add("\n" + "="*70)
    add("[SYSTEM INFO]")
    add("="*70)
    add(f"Cache: Enabled (5min)")
    add(f"History: {len(history)} days tracked")
    add(f"Alerts: {len(alerts)} active")
    add(f"Next auto-run: Tomorrow 09:00")
    add("""
Data delay: 15min
News source: Google News RSS
Institutional: Yahoo Finance T+1
Limitations: Cannot predict future, may miss important news
""")
    
    add("="*70)
    add("END OF REPORT v3.0")
    add("="*70)
    
    # 寫入檔案
    output_file = "daily_report_v3.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    # 如果有重要警報，額外輸出到 alert.txt
    if critical_alerts:
        with open('CRITICAL_ALERT.txt', 'w', encoding='utf-8') as f:
            f.write("CRITICAL ALERTS - ACTION REQUIRED\n")
            f.write("="*70 + "\n\n")
            for a in critical_alerts:
                f.write(f"[!] {a['message']}\n")
            f.write(f"\nTime: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
            f.write("Check daily_report_v3.txt for full details.\n")
    
    print(f"Report saved: {output_file}")
    print(f"History tracked: {len(history)} days")
    print(f"Alerts: {len(alerts)} ({len(critical_alerts)} critical)")
    
    if critical_alerts:
        print("\n!!! CRITICAL ALERTS - CHECK CRITICAL_ALERT.txt !!!")

if __name__ == "__main__":
    main()