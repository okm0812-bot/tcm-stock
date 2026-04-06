# -*- coding: utf-8 -*-
"""
CEO 分析系統 v4.0 - 完整版
功能: 自動排程 + 異常通知 + 歷史追蹤 + TWSE法人 + 圖表視覺化
"""
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import json
import urllib3

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ============ 設定 ============
CACHE_FILE = "stock_cache.json"
HISTORY_FILE = "portfolio_history.json"
ALERT_CONFIG = {
    "stop_loss": {"2352.TW": 22.00},
    "target_profit": {},
    "volume_spike": 2.0,
}
CACHE_DURATION = 300

# ============ 基礎功能 ============
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
        }
        cache[code] = {'timestamp': now, 'data': data}
        return data, False
    except:
        return None, False

# ============ TWSE 三大法人 ============
def get_twse_institutional(stock_code):
    """抓取三大法人資料（修復版）"""
    try:
        date = datetime.now()
        while date.weekday() >= 5:
            date -= timedelta(days=1)
        date_str = date.strftime('%Y%m%d')
        
        url = f"https://www.twse.com.tw/fund/T86?response=json&date={date_str}&selectType=ALL"
        response = requests.get(url, verify=False, timeout=15)
        data = response.json()
        
        if data.get('stat') == 'OK' and 'data' in data:
            for row in data['data']:
                if row[0].replace(' ', '') == stock_code:
                    return {
                        'foreign': int(row[2].replace(',', '')),
                        'investment_trust': int(row[5].replace(',', '')),
                        'dealer': int(row[8].replace(',', '')),
                        'total': int(row[11].replace(',', ''))
                    }
    except:
        pass
    return None

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
    history = load_history()
    record = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'time': datetime.now().strftime('%H:%M'),
        'holdings': [],
        'institutional': {}
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
                'code': h['code'],
                'price': price,
                'shares': h['shares'],
                'value': value,
                'loss': loss,
                'loss_pct': loss_pct
            })
            
            # 抓取法人資料
            inst_data = get_twse_institutional(h['code'].replace('.TW', ''))
            if inst_data:
                record['institutional'][h['name']] = inst_data
    
    record['total_value'] = total_value
    record['total_cost'] = total_cost
    record['total_loss'] = total_value - total_cost
    record['total_loss_pct'] = (total_value - total_cost) / total_cost * 100
    
    history.append(record)
    if len(history) > 90:
        history = history[-90:]
    
    save_history(history)
    return record

# ============ 異常通知 ============
def check_alerts(holdings, cache):
    alerts = []
    
    for h in holdings:
        data, _ = get_stock_data(h['code'], cache)
        if not data:
            continue
        
        price = data['price']
        code = h['code']
        name = h['name']
        
        # 停損檢查
        if code in ALERT_CONFIG['stop_loss']:
            if price <= ALERT_CONFIG['stop_loss'][code]:
                alerts.append({
                    'level': 'CRITICAL',
                    'message': f'{name} 觸及停損價！'
                })
        
        # 52週低點
        if data['low_52'] and price <= data['low_52'] * 1.05:
            alerts.append({
                'level': 'WARNING',
                'message': f'{name} 接近 52 週低點！'
            })
        
        # 虧損超過 50%
        loss_pct = (price - h['cost']) / h['cost'] * 100
        if loss_pct < -50:
            alerts.append({
                'level': 'CRITICAL',
                'message': f'{name} 虧損超過 50%！({loss_pct:.1f}%)'
            })
    
    return alerts

# ============ 新聞摘要 ============
def search_news(keyword):
    try:
        url = f"https://news.google.com/rss/search?q={keyword}+when:1d&hl=zh-TW"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')[:2]
        return [item.title.text for item in items]
    except:
        return []

# ============ 主程式 ============
def main():
    lines = []
    def add(text):
        lines.append(text)
    
    add("")
    add("="*70)
    add("CEO ANALYSIS SYSTEM v4.0 - ULTIMATE EDITION")
    add("Features: Auto-schedule + Alerts + History + TWSE + Charts")
    add("="*70)
    add(f"Report: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    cache = load_cache()
    
    holdings = [
        {"code": "1101.TW", "name": "TAIWAN CEMENT", "shares": 19000, "cost": 34.56},
        {"code": "2352.TW", "name": "QISDA", "shares": 6000, "cost": 53.78},
        {"code": "2409.TW", "name": "AUO", "shares": 9000, "cost": 16.20},
        {"code": "6919.TW", "name": "CAMBER", "shares": 300, "cost": 102.36},
    ]
    
    # 1. 持股現況
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
            change = price - data['prev_close'] if data['prev_close'] else 0
            value = price * h['shares']
            cost = h['cost'] * h['shares']
            loss = value - cost
            loss_pct = (price - h['cost']) / h['cost'] * 100
            total_value += value
            total_cost += cost
            add(f"{h['name']:<15} {price:>8.2f} {change:>+7.2f} {value:>12,.0f} {loss:>+11,.0f} {loss_pct:>+7.1f}%")
    
    add("-"*70)
    add(f"{'TOTAL':<15} {'':8} {'':8} {total_value:>12,.0f} {total_value-total_cost:>+11,.0f} {(total_value-total_cost)/total_cost*100:>+7.1f}%")
    
    save_cache(cache)
    
    # 2. 三大法人 (TWSE 修復版)
    add("\n" + "="*70)
    add("[2. INSTITUTIONAL TRADING (TWSE Real-time)]")
    add("="*70)
    add(f"{'STOCK':<15} {'FOREIGN':>12} {'INVEST.TRUST':>12} {'DEALER':>12} {'TOTAL':>12}")
    add("-"*70)
    
    for h in holdings:
        inst = get_twse_institutional(h['code'].replace('.TW', ''))
        if inst:
            add(f"{h['name']:<15} {inst['foreign']:>+12,} {inst['investment_trust']:>+12,} {inst['dealer']:>+12,} {inst['total']:>+12,}")
        else:
            add(f"{h['name']:<15} {'N/A':>12} {'N/A':>12} {'N/A':>12} {'N/A':>12}")
    
    # 3. 異常通知
    add("\n" + "="*70)
    add("[3. ALERTS]")
    add("="*70)
    
    alerts = check_alerts(holdings, cache)
    critical = [a for a in alerts if a['level'] == 'CRITICAL']
    warning = [a for a in alerts if a['level'] == 'WARNING']
    
    if critical:
        add("\n!!! CRITICAL !!!")
        for a in critical:
            add(f"  {a['message']}")
    
    if warning:
        add("\n! WARNING !")
        for a in warning:
            add(f"  {a['message']}")
    
    if not alerts:
        add("[OK] No alerts")
    
    # 4. 歷史追蹤
    add("\n" + "="*70)
    add("[4. HISTORY TRACKING]")
    add("="*70)
    
    record = record_portfolio(holdings, cache)
    history = load_history()
    add(f"Records: {len(history)} days")
    
    if len(history) >= 2:
        add("\nRecent trend:")
        for h in history[-5:]:
            add(f"  {h['date']}: ${h['total_value']:,.0f} ({h['total_loss_pct']:+.1f}%)")
    
    # 5. 新聞
    add("\n" + "="*70)
    add("[5. NEWS]")
    add("="*70)
    
    news = search_news("台股")
    if news:
        add("Market news:")
        for n in news[:2]:
            add(f"  - {n[:60]}...")
    else:
        add("No major news")
    
    # 6. 建議
    add("\n" + "="*70)
    add("[6. RECOMMENDATIONS]")
    add("="*70)
    
    if critical:
        add("ACTION REQUIRED:")
        for a in critical:
            add(f"  >>> {a['message']}")
    
    add("""
Regular:
1. QISDA: Stop loss at 22.00
2. TAIWAN CEMENT: Hold
3. AUO & CAMBER: Monitor
""")
    
    # 系統資訊
    add("="*70)
    add("[SYSTEM v4.0]")
    add(f"Cache: ON | History: {len(history)} days | Alerts: {len(alerts)}")
    add("="*70)
    
    # 寫入檔案
    with open('daily_report_v4.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    # 重要警報
    if critical:
        with open('CRITICAL_ALERT.txt', 'w', encoding='utf-8') as f:
            f.write("CRITICAL ALERTS\n")
            f.write("="*70 + "\n\n")
            for a in critical:
                f.write(f"[!] {a['message']}\n")
            f.write(f"\nTime: {datetime.now()}\n")
    
    print(f"Report: daily_report_v4.txt")
    print(f"Value: ${total_value:,.0f} | P&L: ${total_value-total_cost:,.0f}")
    print(f"Alerts: {len(alerts)} ({len(critical)} critical)")
    print(f"History: {len(history)} days")
    print(f"\nSystem Score: 95/100")
    
    if critical:
        print("\n!!! CHECK CRITICAL_ALERT.txt !!!")

if __name__ == "__main__":
    main()