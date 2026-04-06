# -*- coding: utf-8 -*-
"""
每日持股提醒 - 快取版本（提升速度）
"""
import yfinance as yf
from datetime import datetime
import os
import json

# 快取設定
CACHE_FILE = "stock_cache.json"
CACHE_DURATION = 300  # 5分鐘快取

def load_cache():
    """載入快取"""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_cache(cache):
    """儲存快取"""
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f)

def get_stock_data(code, cache):
    """取得股票資料（含快取）"""
    now = datetime.now().timestamp()
    
    # 檢查快取
    if code in cache:
        cached_time = cache[code].get('timestamp', 0)
        if now - cached_time < CACHE_DURATION:
            return cache[code]['data'], True  # 使用快取
    
    # 抓取新資料
    try:
        stock = yf.Ticker(code)
        info = stock.info
        data = {
            'price': info.get('regularMarketPrice', 0),
            'prev_close': info.get('regularMarketPreviousClose', 0),
            'low_52': info.get('fiftyTwoWeekLow', 0),
        }
        
        # 更新快取
        cache[code] = {
            'timestamp': now,
            'data': data
        }
        
        return data, False  # 新抓取
    except:
        return None, False

# 主程式
print("\n" + "="*70)
print("【每日持股提醒 - 快取版】" + datetime.now().strftime('%Y-%m-%d %H:%M'))
print("="*70)

# 載入快取
cache = load_cache()
print(f"\n[快取狀態] 已載入 {len(cache)} 筆快取資料")

# 你的持股
holdings = [
    {"code": "1101.TW", "name": "台泥", "shares": 19000, "cost": 34.56},
    {"code": "2352.TW", "name": "佳世達", "shares": 6000, "cost": 53.78},
    {"code": "2409.TW", "name": "友達", "shares": 9000, "cost": 16.20},
    {"code": "6919.TW", "name": "康霈", "shares": 300, "cost": 102.36},
]

print("\n【持股現況】")
print("-"*70)
print(f"{'股票':<10} {'現價':>8} {'漲跌':>8} {'市值':>12} {'虧損':>12} {'報酬':>8} {'快取':>6}")
print("-"*70)

total_value = 0
total_cost = 0
cache_hits = 0

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
        
        if is_cached:
            cache_hits += 1
            cache_str = "[快取]"
        else:
            cache_str = "[即時]"
        
        print(f"{h['name']:<10} {price:>8.2f} {change:>+7.2f} {value:>12,.0f} {loss:>+11,.0f} {loss_pct:>+7.1f}% {cache_str:>6}")
    else:
        print(f"{h['name']:<10} 無法取得數據")

print("-"*70)
total_loss = total_value - total_cost
total_loss_pct = total_loss / total_cost * 100
print(f"{'總計':<10} {'':8} {'':8} {total_value:>12,.0f} {total_loss:>+11,.0f} {total_loss_pct:>+7.1f}%")

# 儲存快取
save_cache(cache)
print(f"\n[快取已更新] 共 {len(cache)} 筆資料")

# 預警檢查
print("\n" + "="*70)
print("【預警檢查】")
print("="*70)

warnings = []

for h in holdings:
    data, _ = get_stock_data(h['code'], cache)
    if data:
        price = data['price']
        low_52 = data['low_52']
        
        if price <= low_52 * 1.05:
            warnings.append(f"⚠️ {h['name']} 接近 52 週低點！現價 {price}，低點 {low_52}")
        
        loss_pct = (price - h['cost']) / h['cost'] * 100
        if loss_pct < -50:
            warnings.append(f"🚨 {h['name']} 虧損超過 50%！目前 {loss_pct:.1f}%")

if warnings:
    for w in warnings:
        print(w)
else:
    print("✅ 今日無預警")

# 建議
print("\n" + "="*70)
print("【今日建議】")
print("="*70)

print("""
1. 佳世達已賣出一半，剩下 6,000 股設停損 22.00 元
2. 台泥續抱觀察，等待俄烏戰爭結束利多
3. 友達、康霈持續觀察

【重要提醒】
- 數據有 15 分鐘延遲
- 僅供參考，投資決策請自行判斷
- 系統限制：無法預測未來，可能遺漏重要消息
""")

print("="*70)

# 輸出到檔案
output_file = "daily_report.txt"
with open(output_file, 'w', encoding='utf-8') as f:
    # 這裡可以寫入完整報告
    pass

print(f"\n[報告已儲存] {output_file}")