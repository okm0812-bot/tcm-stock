# -*- coding: utf-8 -*-
"""
台股開盤數據
"""
import yfinance as yf

# 台股加權指數
twii = yf.Ticker('^TWII')
data = twii.history(period='5d')

print("\n" + "="*60)
print("【台股加權指數】近5日走勢")
print("="*60)
print(data[['Open', 'High', 'Low', 'Close', 'Volume']].tail())

# 推薦股票
print("\n" + "="*60)
print("【值得關注的股票】")
print("="*60)

recommend = [
    ("2330.TW", "台積電", "護城河強、晶圓代工龍頭"),
    ("2303.TW", "聯電", "成熟製程、殖利率高"),
    ("2884.TW", "玉山金", "金融股、穩定配息"),
    ("2002.TW", "中鋼", "鋼鐵景氣循環、低估值"),
    ("2207.TW", "和泰車", "汽車銷售、高殖利率"),
]

for ticker, name, reason in recommend:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('regularMarketPrice', 'N/A')
        pe = info.get('trailingPE', 'N/A')
        div = info.get('dividendYield', 'N/A')
        
        print(f"\n{ticker} {name}")
        print(f"  現價: {price} 元")
        print(f"  本益比: {pe}")
        print(f"  殖利率: {div}")
        print(f"  理由: {reason}")
    except:
        print(f"\n{ticker} {name} - 資料暫時無法取得")

print("\n" + "="*60)
