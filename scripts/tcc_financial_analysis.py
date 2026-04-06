# tcc_financial_analysis.py
# 台泥集團財務分析腳本

import yfinance as yf
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print('=' * 70)
print('台泥集團主要公司財務分析')
print('=' * 70)

# 台泥本體
try:
    print('\n【台泥本體】1101.TW')
    print('-' * 50)
    stock = yf.Ticker('1101.TW')
    info = stock.info
    
    price = info.get('regularMarketPrice', 0)
    market_cap = info.get('marketCap', 0)
    pe = info.get('trailingPE', 0)
    pb = info.get('priceToBook', 0)
    roe = info.get('returnOnEquity', 0)
    debt = info.get('debtToEquity', 0)
    revenue = info.get('totalRevenue', 0)
    net_income = info.get('netIncomeToCommon', 0)
    
    print(f'  現價: {price:.2f} 元')
    print(f'  市值: {market_cap/1e8:.1f} 億元')
    print(f'  PE: {pe:.2f}x' if pe else '  PE: N/A')
    print(f'  PB: {pb:.2f}x' if pb else '  PB: N/A')
    print(f'  ROE: {roe*100:.2f}%' if roe else '  ROE: N/A')
    print(f'  負債比: {debt:.2f}%' if debt else '  負債比: N/A')
    print(f'  年營收: {revenue/1e8:.1f} 億元' if revenue else '  年營收: N/A')
    print(f'  年淨利: {net_income/1e8:.1f} 億元' if net_income else '  年淨利: N/A')
    
    # 抓取歷史損益
    hist = stock.history(period='1y')
    if len(hist) > 0:
        high_52w = info.get('fiftyTwoWeekHigh', 0)
        low_52w = info.get('fiftyTwoWeekLow', 0)
        print(f'  52週高: {high_52w:.2f} 元')
        print(f'  52週低: {low_52w:.2f} 元')
        
except Exception as e:
    print(f'  錯誤: {e}')

# 台泥國際（港股）
try:
    print('\n【台泥國際】8737.HK')
    print('-' * 50)
    stock = yf.Ticker('8737.HK')
    info = stock.info
    
    price = info.get('regularMarketPrice', 0)
    market_cap = info.get('marketCap', 0)
    pe = info.get('trailingPE', 0)
    pb = info.get('priceToBook', 0)
    
    print(f'  現價: {price:.2f} HKD' if price else '  現價: N/A')
    print(f'  市值: {market_cap/1e8:.1f} 億 HKD' if market_cap else '  市值: N/A')
    print(f'  PE: {pe:.2f}x' if pe else '  PE: N/A')
    print(f'  PB: {pb:.2f}x' if pb else '  PB: N/A')
    
    # 台泥持有約 40-45%，計算權益市值
    if market_cap:
        tcc_stake = market_cap * 0.42  # 約 42% 持股
        print(f'  台泥權益市值: {tcc_stake/1e8:.1f} 億 HKD (約 {tcc_stake*4/1e8:.1f} 億台幣)')
    
except Exception as e:
    print(f'  錯誤: {e}')

# 台灣水泥的主要轉投資架構
print('\n' + '=' * 70)
print('台泥集團轉投資架構')
print('=' * 70)

investments = [
    ('台泥國際（香港）', '8737.HK', '42%', '海外投資平台', '葡萄牙、土耳其、非洲'),
    ('Cimpor（葡萄牙）', '透過台泥國際', '40%', '歐洲水泥', '葡萄牙、非洲、土耳其'),
    ('Cimpor Türkiye', '透過 Cimpor', '40%', '土耳其水泥', '約 350 萬噸/年'),
    ('和平電力', '轉投資', '約 20%', '電力', '水泥廠餘熱發電'),
    ('台泥綠能', '子公司', '100%', '再生能源', '太陽能、儲能'),
]

print('\n{:<20} {:<12} {:<8} {:<12} {:<20}'.format('公司', '上市/架構', '持股', '產業', '主要市場'))
print('-' * 70)
for name, structure, stake, industry, market in investments:
    print(f'{name:<20} {structure:<12} {stake:<8} {industry:<12} {market:<20}')

# 財務摘要
print('\n' + '=' * 70)
print('台泥集團財務摘要（推估）')
print('=' * 70)

print("""
【2024 年推估財務數字】

台泥本體（1101.TW）：
- 營收：約 600-700 億元（主要來自中國水泥）
- 淨利：約 20-40 億元（中國需求下滑，獲利大幅縮水）
- ROE：約 2-4%（偏低）
- 負債比：約 60-70%（偏高）

台泥國際（8737.HK）：
- 營收：約 150-200 億港元（葡萄牙、土耳其、非洲）
- 淨利：約 10-20 億港元
- 台泥權益：約 42% → 貢獻淨利約 4-8 億港元

Cimpor（葡萄牙）：
- 產能：約 1,000 萬噸/年
- 市佔率：葡萄牙約 30-40%
- 獲利：穩定但成長有限

Cimpor Türkiye（土耳其）：
- 產能：約 350 萬噸/年
- 市佔率：土耳其約 4-5%
- 獲利：受通膨、匯率影響，波動大
""")

# 關鍵財務指標評估
print('=' * 70)
print('關鍵財務指標評估')
print('=' * 70)

metrics = [
    ('本益比（PE）', 'N/A（虧損或獲利極低）', '偏高', '❌'),
    ('股價淨值比（PB）', '約 0.5-0.8x', '偏低', '🟢'),
    ('ROE', '2-4%', '偏低', '❌'),
    ('負債比率', '60-70%', '偏高', '⚠️'),
    ('現金流', '勉強為正', '普通', '🟡'),
    ('海外獲利貢獻', '約 20-30%', '成長中', '🟢'),
]

print('\n{:<20} {:<20} {:<10} {:<6}'.format('指標', '數值', '評價', '狀態'))
print('-' * 70)
for metric, value, eval, status in metrics:
    print(f'{metric:<20} {value:<20} {eval:<10} {status:<6}')

print('\n' + '=' * 70)
print('分析完成')
print('=' * 70)
