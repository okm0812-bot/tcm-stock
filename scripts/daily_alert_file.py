# -*- coding: utf-8 -*-
"""
每日持股提醒 - 輸出到檔案（避免亂碼）
"""
import yfinance as yf
from datetime import datetime
import os

# 設定輸出檔案
output_file = "daily_report.txt"

# 收集輸出內容
lines = []

def add_line(text):
    lines.append(text)

LINE = "=" * 70
DASH = "-" * 70

add_line("")
add_line(LINE)
add_line("【每日持股提醒】" + datetime.now().strftime('%Y-%m-%d %H:%M'))
add_line(LINE)

# 你的持股
holdings = [
    {"code": "1101.TW", "name": "台泥", "shares": 19000, "cost": 34.56},
    {"code": "2352.TW", "name": "佳世達", "shares": 6000, "cost": 53.78},
    {"code": "2409.TW", "name": "友達", "shares": 9000, "cost": 16.20},
    {"code": "6919.TW", "name": "康霈", "shares": 300, "cost": 102.36},
]

add_line("")
add_line("【持股現況】")
add_line(DASH)
add_line(f"{'股票':<10} {'現價':>8} {'漲跌':>8} {'市值':>12} {'虧損':>12} {'報酬':>8}")
add_line(DASH)

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
        
        add_line(f"{h['name']:<10} {price:>8.2f} {change:>+7.2f} {value:>12,.0f} {loss:>+11,.0f} {loss_pct:>+7.1f}%")
        
    except Exception as e:
        add_line(f"{h['name']:<10} 無法取得數據")

add_line(DASH)
total_loss = total_value - total_cost
total_loss_pct = total_loss / total_cost * 100
add_line(f"{'總計':<10} {'':8} {'':8} {total_value:>12,.0f} {total_loss:>+11,.0f} {total_loss_pct:>+7.1f}%")

# 預警檢查
add_line("")
add_line(LINE)
add_line("【預警檢查】")
add_line(LINE)

warnings = []

for h in holdings:
    try:
        stock = yf.Ticker(h['code'])
        info = stock.info
        price = info.get('regularMarketPrice', 0)
        low_52 = info.get('fiftyTwoWeekLow', 0)
        
        if price <= low_52 * 1.05:
            warnings.append(f"⚠️ {h['name']} 接近 52 週低點！現價 {price}，低點 {low_52}")
        
        loss_pct = (price - h['cost']) / h['cost'] * 100
        if loss_pct < -50:
            warnings.append(f"🚨 {h['name']} 虧損超過 50%！目前 {loss_pct:.1f}%")
            
    except:
        pass

if warnings:
    for w in warnings:
        add_line(w)
else:
    add_line("✅ 今日無預警")

# 建議
add_line("")
add_line(LINE)
add_line("【今日建議】")
add_line(LINE)

add_line("""
1. 佳世達已賣出一半，剩下 6,000 股設停損 22.00 元
2. 台泥續抱觀察，等待俄烏戰爭結束利多
3. 友達、康霈持續觀察

【重要提醒】
- 數據有 15 分鐘延遲
- 僅供參考，投資決策請自行判斷
- 系統限制：無法預測未來，可能遺漏重要消息
""")

add_line(LINE)

# 寫入檔案
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"報告已儲存至: {os.path.abspath(output_file)}")
print(f"請用記事本或 VS Code 開啟查看")

# 同時顯示在終端（可能亂碼）
print("\n" + "="*50)
print("[終端預覽 - 可能亂碼，請看檔案]")
print("="*50)
for line in lines[:10]:
    print(line)
print("...")
print(f"[完整內容請查看 {output_file}]")