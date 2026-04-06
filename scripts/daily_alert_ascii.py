# -*- coding: utf-8 -*-
"""
每日持股提醒 - ASCII 版本（最穩定）
"""
import yfinance as yf
from datetime import datetime

# 使用 ASCII 字符避免編碼問題
LINE = "=" * 70
DASH = "-" * 70

print("")
print(LINE)
print("DAILY PORTFOLIO ALERT - " + datetime.now().strftime('%Y-%m-%d %H:%M'))
print(LINE)

# 你的持股
holdings = [
    {"code": "1101.TW", "name": "TAIWAN CEMENT", "shares": 19000, "cost": 34.56},
    {"code": "2352.TW", "name": "QISDA", "shares": 6000, "cost": 53.78},
    {"code": "2409.TW", "name": "AUO", "shares": 9000, "cost": 16.20},
    {"code": "6919.TW", "name": "CAMBER", "shares": 300, "cost": 102.36},
]

print("")
print("[PORTFOLIO STATUS]")
print(DASH)
print(f"{'STOCK':<15} {'PRICE':>8} {'CHANGE':>8} {'VALUE':>12} {'P&L':>12} {'RETURN':>8}")
print(DASH)

total_value = 0
total_cost = 0

for h in holdings:
    try:
        stock = yf.Ticker(h['code'])
        info = stock.info
        price = info.get('regularMarketPrice', 0)
        prev_close = info.get('regularMarketPreviousClose', 0)
        
        change = price - prev_close if prev_close else 0
        
        value = price * h['shares']
        cost = h['cost'] * h['shares']
        loss = value - cost
        loss_pct = (price - h['cost']) / h['cost'] * 100
        
        total_value += value
        total_cost += cost
        
        print(f"{h['name']:<15} {price:>8.2f} {change:>+7.2f} {value:>12,.0f} {loss:>+11,.0f} {loss_pct:>+7.1f}%")
        
    except Exception as e:
        print(f"{h['name']:<15} DATA ERROR")

print(DASH)
total_loss = total_value - total_cost
total_loss_pct = total_loss / total_cost * 100
print(f"{'TOTAL':<15} {'':8} {'':8} {total_value:>12,.0f} {total_loss:>+11,.0f} {total_loss_pct:>+7.1f}%")

# 預警檢查
print("")
print(LINE)
print("[ALERTS]")
print(LINE)

warnings = []

for h in holdings:
    try:
        stock = yf.Ticker(h['code'])
        info = stock.info
        price = info.get('regularMarketPrice', 0)
        low_52 = info.get('fiftyTwoWeekLow', 0)
        
        # 檢查是否接近 52 週低點
        if price <= low_52 * 1.05:
            warnings.append(f"[WARNING] {h['name']} near 52W LOW! Price {price}, Low {low_52}")
        
        # 檢查虧損幅度
        loss_pct = (price - h['cost']) / h['cost'] * 100
        if loss_pct < -50:
            warnings.append(f"[ALERT] {h['name']} loss > 50%! Current {loss_pct:.1f}%")
            
    except:
        pass

if warnings:
    for w in warnings:
        print(w)
else:
    print("[OK] No alerts today")

# 建議
print("")
print(LINE)
print("[TODAY'S RECOMMENDATIONS]")
print(LINE)

print("""
1. QISDA: Sold half, remaining 6,000 shares. Set stop loss at 22.00
2. TAIWAN CEMENT: Hold and observe. Wait for Russia-Ukraine war end catalyst
3. AUO & CAMBER: Continue monitoring

[IMPORTANT NOTES]
- Data delayed by 15 minutes
- For reference only. Investment decisions are your responsibility
- System limitations: Cannot predict future, may miss important news
""")

print(LINE)
print("END OF REPORT")
print(LINE)