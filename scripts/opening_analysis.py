# -*- coding: utf-8 -*-
"""
明天開盤完整分析
"""
import yfinance as yf
import requests
import json
import sys
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding='utf-8')

def get_market_data():
    print("=" * 70)
    print("抓取最新市場數據...")
    print("=" * 70)
    
    # 台股加權
    twii = yf.Ticker("^TWII")
    twii_info = twii.info
    twii_price = twii_info.get('regularMarketPrice', 0) or 0
    twii_prev = twii_info.get('regularMarketPreviousClose', 0) or 0
    twii_chg = (twii_price - twii_prev) / twii_prev * 100 if twii_prev > 0 else 0
    
    # VIX
    vix = yf.Ticker("^VIX")
    vix_info = vix.info
    vix_price = vix_info.get('regularMarketPrice', 0) or 0
    
    # 美10年債
    us10y = yf.Ticker("^TNX")
    us10y_info = us10y.info
    us10y_price = us10y_info.get('regularMarketPrice', 0) or 0
    
    # 美股
    spy = yf.Ticker("SPY")
    spy_info = spy.info
    spy_price = spy_info.get('regularMarketPrice', 0) or 0
    spy_prev = spy_info.get('regularMarketPreviousClose', 0) or 0
    spy_chg = (spy_price - spy_prev) / spy_prev * 100 if spy_prev > 0 else 0
    
    # A股
    ashs = yf.Ticker("ASHS")
    ashs_info = ashs.info
    ashs_price = ashs_info.get('regularMarketPrice', 0) or 0
    ashs_prev = ashs_info.get('regularMarketPreviousClose', 0) or 0
    ashs_chg = (ashs_price - ashs_prev) / ashs_prev * 100 if ashs_prev > 0 else 0
    
    return {
        'TWII': {'price': twii_price, 'prev': twii_prev, 'chg': twii_chg},
        'VIX': {'price': vix_price},
        'US10Y': {'price': us10y_price},
        'SPY': {'price': spy_price, 'prev': spy_prev, 'chg': spy_chg},
        'ASHS': {'price': ashs_price, 'prev': ashs_prev, 'chg': ashs_chg}
    }

def get_twse_institutional(stock_code):
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
                        'foreign': float(row[4].replace(',', '')) if isinstance(row[4], str) else row[4],
                        'trust': float(row[6].replace(',', '')) if isinstance(row[6], str) else row[6],
                        'dealer': float(row[8].replace(',', '')) if isinstance(row[8], str) else row[8],
                        'total': float(row[10].replace(',', '')) if isinstance(row[10], str) else row[10],
                    }
        return None
    except:
        return None

def get_stock_price(code):
    try:
        stock = yf.Ticker(code)
        info = stock.info
        return {
            'price': info.get('regularMarketPrice', 0) or 0,
            'prev_close': info.get('regularMarketPreviousClose', 0) or 0,
            'high_52': info.get('fiftyTwoWeekHigh', 0) or 0,
            'low_52': info.get('fiftyTwoWeekLow', 0) or 0,
        }
    except:
        return None

# 持股資料（從A帳戶）
stocks = [
    {"code": "1101.TW", "name": "台泥", "shares": 19000, "cost": 34.56, "stop_loss": 20.00},
    {"code": "2352.TW", "name": "佳世達", "shares": 6000, "cost": 51.33, "stop_loss": 22.00},
    {"code": "2409.TW", "name": "友達", "shares": 9000, "cost": 16.20, "stop_loss": 12.00},
    {"code": "6919.TW", "name": "康霈", "shares": 300, "cost": 102.36, "stop_loss": 65.00},
]

# 主程式
if __name__ == "__main__":
    from datetime import timedelta
    
    print("\n" + "=" * 70)
    print("  明天開盤完整分析報告")
    print("  " + datetime.now().strftime('%Y-%m-%d %H:%M'))
    print("=" * 70)
    
    # 1. 全球市場
    market = get_market_data()
    print("\n【1. 全球市場概況】")
    print("-" * 70)
    print(f"  台股加權: {market['TWII']['price']:,.0f} 點 ({market['TWII']['chg']:+.2f}%)")
    print(f"  VIX恐慌:  {market['VIX']['price']:.2f} {'🔴 高' if market['VIX']['price'] > 25 else '🟡 中' if market['VIX']['price'] > 20 else '🟢 低'}")
    print(f"  美10年債: {market['US10Y']['price']:.2f}% {'🔴 高' if market['US10Y']['price'] > 4.5 else '🟡 中' if market['US10Y']['price'] > 4 else '🟢 低'}")
    print(f"  S&P 500:  ${market['SPY']['price']:.2f} ({market['SPY']['chg']:+.2f}%)")
    print(f"  A股(YINN): ${market['ASHS']['price']:.2f} ({market['ASHS']['chg']:+.2f}%)")
    
    # 2. 持股分析
    print("\n【2. 持股即時分析】")
    print("-" * 70)
    print(f"{'名稱':<8} {'現價':>8} {'日漲跌':>10} {'距離停損':>10} {'狀態':>10}")
    print("-" * 70)
    
    alerts = []
    for s in stocks:
        data = get_stock_price(s['code'])
        if data:
            price = data['price']
            prev = data['prev_close']
            chg = (price - prev) / prev * 100 if prev > 0 else 0
            distance = price - s['stop_loss']
            distance_pct = distance / price * 100 if price > 0 else 0
            
            if distance_pct <= 3:
                status = "🔴 危險"
                alerts.append(s)
            elif distance_pct <= 5:
                status = "🟡 注意"
                alerts.append(s)
            else:
                status = "🟢 安全"
            
            print(f"{s['name']:<8} {price:>8.2f} {chg:>+9.2f}% {distance_pct:>9.1f}% {status:>10}")
    
    # 3. 三大法人
    print("\n【3. 三大法人動態】")
    print("-" * 70)
    for s in stocks:
        inst = get_twse_institutional(s['code'].replace('.TW', ''))
        if inst:
            print(f"  {s['name']:<6} 外資: {inst['foreign']/1000:>+8.0f}K  投信: {inst['trust']/1000:>+7.0f}K  自營: {inst['dealer']/1000:>+7.0f}K")
        else:
            print(f"  {s['name']:<6} 法人資料讀取失敗")
    
    # 4. 停損警報
    print("\n【4. 停損警報】")
    print("-" * 70)
    if alerts:
        for a in alerts:
            data = get_stock_price(a['code'])
            if data:
                price = data['price']
                distance = price - a['stop_loss']
                print(f"  ⚠️ {a['name']}: 現價 ${price:.2f}，距離停損 ${a['stop_loss']:.2f} 只剩 ${distance:.2f}")
    else:
        print("  ✅ 目前沒有停損警報")
    
    # 5. 明天開盤建議
    print("\n【5. 明天開盤建議】")
    print("=" * 70)
    
    qisda_data = get_stock_price("2352.TW")
    if qisda_data:
        qisda_price = qisda_data['price']
        print(f"\n  🔴 佳世達 2352:")
        print(f"     現價: ${qisda_price:.2f}")
        print(f"     停損: ${22.00:.2f}")
        print(f"     距離: ${qisda_price - 22.00:.2f} ({(qisda_price - 22.00)/qisda_price*100:.1f}%)")
        
        if qisda_price <= 22.00:
            print(f"     → 明日開盤立刻停損！")
            print(f"     → 回收資金: ~{6000 * qisda_price:,.0f} 元")
            print(f"     → 建議投入 0050 或 VOO")
        elif qisda_price <= 22.50:
            print(f"     → 設條件單：22.00 賣出")
            print(f"     → 不要加碼攤平")
    
    print("\n  📊 明日操作優先順序:")
    print("  " + "-" * 50)
    print("  1. 【最高】佳世達：設停損條件單 22.00")
    print("  2. 【高】台泥：續抱，目標 28-30 元減碼")
    print("  3. 【中】友達：續抱，關注面板景氣")
    print("  4. 【中】康霈：續抱，目標 100-110 元")
    print("  5. 【低】美債：續抱，利息入帳")
    print("  6. 【機會】若佳世達停損 → 買 0050")
    
    # 6. 風險評估
    print("\n【6. 風險評估】")
    print("-" * 70)
    print(f"  VIX: {market['VIX']['price']:.2f} - {'🔴 市場恐慌' if market['VIX']['price'] > 25 else '🟡 正常波動' if market['VIX']['price'] > 20 else '🟢 穩定'}")
    print(f"  美10年債: {market['US10Y']['price']:.2f}% - {'🔴 利率壓力大' if market['US10Y']['price'] > 4.5 else '🟡 中等' if market['US10Y']['price'] > 4 else '🟢 正常'}")
    print(f"  美股: {market['SPY']['chg']:+.2f}% - {'🔴 偏弱' if market['SPY']['chg'] < -1 else '🟡 中性' if market['SPY']['chg'] < 1 else '🟢 偏強'}")
    print(f"  A股: {market['ASHS']['chg']:+.2f}% - {'🔴 中國因素注意' if market['ASHS']['chg'] < -2 else '🟡 中性' if market['ASHS']['chg'] < 2 else '🟢 中國利好'}")
    
    print("\n" + "=" * 70)
    print("  報告結束")
    print("=" * 70)
