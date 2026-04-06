# -*- coding: utf-8 -*-
"""
三大法人資料 - 使用 Yahoo Finance 替代方案
"""
import yfinance as yf
from datetime import datetime

print("\n" + "="*70)
print("【三大法人資料】" + datetime.now().strftime('%Y-%m-%d %H:%M'))
print("="*70)

print("\n【資料來源說明】")
print("- TWSE 官方 API: 需要 SSL 憑證，目前無法連線")
print("- 替代方案: Yahoo Finance (T+1 資料)")
print("- 建議: 盤後查看券商 APP 或財經網站取得即時法人資料")
print("="*70)

# 你的持股
stocks = [
    {"code": "1101.TW", "name": "台泥"},
    {"code": "2352.TW", "name": "佳世達"},
    {"code": "2409.TW", "name": "友達"},
    {"code": "6919.TW", "name": "康霈"},
]

print("\n【從 Yahoo Finance 取得資料】")
print("-"*70)
print(f"{'股票':<10} {'成交量':>12} {'機構持有%':>12} {'建議查詢':>20}")
print("-"*70)

for stock in stocks:
    try:
        ticker = yf.Ticker(stock['code'])
        info = ticker.info
        
        volume = info.get('regularMarketVolume', 0)
        inst_hold = info.get('heldPercentInstitutions', 0)
        
        print(f"{stock['name']:<10} {volume:>12,} {inst_hold*100:>11.2f}% {'券商APP法人資料':>20}")
        
    except Exception as e:
        print(f"{stock['name']:<10} {'無法取得':>12} {'N/A':>12} {'券商APP法人資料':>20}")

print("-"*70)

print("\n【如何查詢三大法人資料】")
print("""
方法 1: 券商 APP
- 打開你的券商 APP
- 搜尋股票代號
- 查看「法人買賣超」或「三大法人」

方法 2: 財經網站
- Goodinfo! 台灣股市資訊網
- Yahoo奇摩股市
- 證交所網站 (盤後公布)

方法 3: 盤中看盤軟體
- 元大證券 e 櫃檯
- 其他券商看盤軟體
""")

print("\n【三大法人判讀重點】")
print("""
1. 外資 (外國機構投資人)
   - 影響力最大，通常主導股價方向
   - 連續買超 = 看多
   - 連續賣超 = 看空

2. 投信 (國內投信基金)
   - 影響力次之
   - 通常有季節性布局

3. 自營商 (證券商自營部)
   - 影響力較小
   - 常做短線操作

判讀原則:
- 三大法人同步買超 = 強烈看多訊號
- 三大法人同步賣超 = 強烈看空訊號
- 外資買超 + 投信賣超 = 觀察，可能短多長空
""")

print("\n【系統限制】")
print("- TWSE API 因 SSL 憑證問題暫時無法連線")
print("- Yahoo Finance 法人資料為 T+1")
print("- 建議搭配券商 APP 使用")

print("="*70)