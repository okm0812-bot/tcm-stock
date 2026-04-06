# -*- coding: utf-8 -*-
"""
每日完整報告 v2.0 = 持股 + 新聞 + 法人 + 預警
"""
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import json

# 快取設定
CACHE_FILE = "stock_cache.json"
CACHE_DURATION = 300

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
            'volume': info.get('regularMarketVolume', 0),
            'inst_hold': info.get('heldPercentInstitutions', 0),
        }
        cache[code] = {'timestamp': now, 'data': data}
        return data, False
    except:
        return None, False

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

# 收集輸出
lines = []
def add_line(text):
    lines.append(text)

# 標題
add_line("")
add_line("="*70)
add_line("【每日投資報告 v2.0】" + datetime.now().strftime('%Y-%m-%d %H:%M'))
add_line("="*70)

# 載入快取
cache = load_cache()

# 持股資料
holdings = [
    {"code": "1101.TW", "name": "台泥", "shares": 19000, "cost": 34.56},
    {"code": "2352.TW", "name": "佳世達", "shares": 6000, "cost": 53.78},
    {"code": "2409.TW", "name": "友達", "shares": 9000, "cost": 16.20},
    {"code": "6919.TW", "name": "康霈", "shares": 300, "cost": 102.36},
]

# 一、持股現況
add_line("\n【一、持股現況】")
add_line("-"*70)
add_line(f"{'股票':<10} {'現價':>8} {'漲跌':>8} {'市值':>12} {'虧損':>12} {'報酬':>8}")
add_line("-"*70)

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
        add_line(f"{h['name']:<10} {price:>8.2f} {change:>+7.2f} {value:>12,.0f} {loss:>+11,.0f} {loss_pct:>+7.1f}%")

add_line("-"*70)
total_loss = total_value - total_cost
total_loss_pct = total_loss / total_cost * 100
add_line(f"{'總計':<10} {'':8} {'':8} {total_value:>12,.0f} {total_loss:>+11,.0f} {total_loss_pct:>+7.1f}%")

save_cache(cache)

# 二、新聞摘要
add_line("\n" + "="*70)
add_line("【二、新聞摘要】")
add_line("="*70)

news_keywords = [
    ("台泥", "台泥 水泥"),
    ("佳世達", "佳世達"),
    ("友達", "友達 面板"),
    ("大盤", "台股 加權指數")
]

for name, keyword in news_keywords:
    news = search_news(keyword)
    if news:
        add_line(f"\n{name}:")
        for i, n in enumerate(news[:2], 1):
            add_line(f"  {i}. {n[:50]}...")
    else:
        add_line(f"\n{name}: 今日無重大新聞")

# 三、三大法人資料
add_line("\n" + "="*70)
add_line("【三、三大法人資料】")
add_line("="*70)
add_line("(資料來源: Yahoo Finance T+1，建議搭配券商 APP 查看即時資料)")
add_line("")
add_line(f"{'股票':<10} {'成交量':>12} {'機構持有%':>12} {'查詢建議':>20}")
add_line("-"*70)

for h in holdings:
    data, _ = get_stock_data(h['code'], cache)
    if data:
        volume = data['volume']
        inst_hold = data['inst_hold'] or 0
        add_line(f"{h['name']:<10} {volume:>12,} {inst_hold*100:>11.2f}% {'券商APP法人資料':>20}")

add_line("-"*70)
add_line("\n判讀重點:")
add_line("- 外資連續買超 = 看多訊號")
add_line("- 三大法人同步買超 = 強烈看多")
add_line("- 外資連續賣超 = 看空訊號")

# 四、預警檢查
add_line("\n" + "="*70)
add_line("【四、預警檢查】")
add_line("="*70)

warnings = []
for h in holdings:
    data, _ = get_stock_data(h['code'], cache)
    if data:
        price = data['price']
        low_52 = data['low_52']
        if price <= low_52 * 1.05:
            warnings.append(f"⚠️ {h['name']} 接近 52 週低點！")
        loss_pct = (price - h['cost']) / h['cost'] * 100
        if loss_pct < -50:
            warnings.append(f"🚨 {h['name']} 虧損超過 50%！")

if warnings:
    for w in warnings:
        add_line(w)
else:
    add_line("✅ 今日無預警")

# 五、今日建議
add_line("\n" + "="*70)
add_line("【五、今日建議】")
add_line("="*70)
add_line("""
1. 佳世達：已賣一半，剩 6,000 股設停損 22.00 元
2. 台泥：續抱觀察，等俄烏戰爭結束利多
3. 友達、康霈：持續觀察
4. 每日查看券商 APP 法人買賣超資料
""")

# 系統限制
add_line("\n" + "="*70)
add_line("【系統限制】")
add_line("="*70)
add_line("""
- 數據延遲：15 分鐘
- 新聞來源：Google News RSS
- 法人資料：Yahoo Finance T+1，TWSE API 暫時無法連線
- 快取時間：5 分鐘
- 僅供參考，投資決策請自行判斷
""")

add_line("="*70)

# 寫入檔案
output_file = "daily_report.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"完整報告已儲存: {os.path.abspath(output_file)}")

# 顯示摘要
print("\n" + "="*50)
print("[報告摘要]")
print("="*50)
print(f"總市值: {total_value:,.0f} 元")
print(f"總虧損: {total_loss:,.0f} 元 ({total_loss_pct:.1f}%)")
print(f"預警: {len(warnings)} 項")
print(f"快取: 已啟用 (5分鐘)")
print(f"\n[完整內容請查看 {output_file}]")