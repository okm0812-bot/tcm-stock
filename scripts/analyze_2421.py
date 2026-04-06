# -*- coding: utf-8 -*-
"""
CEO v6.0 - 建準 2421 完整分析
"""
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def safe_get(info, key, default=0):
    val = info.get(key, default)
    return val if val else default

def search_news(keyword, count=3):
    try:
        url = f"https://news.google.com/rss/search?q={keyword}&hl=zh-TW&num={count}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, 'xml')
        items = soup.find_all('item')[:count]
        return [item.title.text for item in items]
    except:
        return []

def get_twse_institutional(code):
    try:
        date = datetime.now()
        while date.weekday() >= 5:
            date -= timedelta(days=1)
        date_str = date.strftime('%Y%m%d')
        url = f"https://www.twse.com.tw/fund/T86?response=json&date={date_str}&selectType=ALL"
        r = requests.get(url, verify=False, timeout=15)
        data = r.json()
        if data.get('stat') == 'OK':
            for row in data.get('data', []):
                if row[0].replace(' ', '') == code:
                    return {
                        'foreign': int(row[2].replace(',', '')),
                        'trust': int(row[5].replace(',', '')),
                        'dealer': int(row[8].replace(',', '')),
                        'total': int(row[11].replace(',', ''))
                    }
    except:
        pass
    return None

lines = []
def add(text=''):
    lines.append(text)

# ==================== 抓取數據 ====================
ticker = yf.Ticker("2421.TW")
info = ticker.info
hist = ticker.history(period="3mo")

price = safe_get(info, 'regularMarketPrice')
prev_close = safe_get(info, 'regularMarketPreviousClose')
change = price - prev_close
change_pct = change / prev_close * 100 if prev_close else 0

pe = safe_get(info, 'trailingPE')
eps = safe_get(info, 'trailingEps')
roe = safe_get(info, 'returnOnEquity')
debt = safe_get(info, 'debtToEquity')
fcf = safe_get(info, 'freeCashflow')
div_yield = safe_get(info, 'dividendYield')
high_52 = safe_get(info, 'fiftyTwoWeekHigh')
low_52 = safe_get(info, 'fiftyTwoWeekLow')
volume = safe_get(info, 'regularMarketVolume')
avg_volume = safe_get(info, 'averageVolume')
market_cap = safe_get(info, 'marketCap')
gross_margin = safe_get(info, 'grossMargins')
op_margin = safe_get(info, 'operatingMargins')
revenue = safe_get(info, 'totalRevenue')
net_income = safe_get(info, 'netIncomeToCommon')

# 技術指標
ma5 = hist['Close'].tail(5).mean()
ma10 = hist['Close'].tail(10).mean()
ma20 = hist['Close'].tail(20).mean()
ma60 = hist['Close'].tail(60).mean() if len(hist) >= 60 else 0

delta = hist['Close'].diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
rs = gain / loss
rsi = (100 - 100 / (1 + rs)).iloc[-1]

vol_ratio = volume / avg_volume if avg_volume else 0

# ==================== 報告 ====================
add("="*70)
add("CEO ANALYSIS v6.0 - 建準電機 2421")
add("="*70)
add(f"分析時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

# 1. 即時數據
add("")
add("[1. 即時數據]")
add("-"*70)
add(f"  現價:       {price:.2f} 元")
add(f"  漲跌:       {change:+.2f} ({change_pct:+.2f}%)")
add(f"  52週高點:   {high_52:.2f} 元")
add(f"  52週低點:   {low_52:.2f} 元")
add(f"  距高點:     {(price-high_52)/high_52*100:.1f}%")
add(f"  距低點:     {(price-low_52)/low_52*100:+.1f}%")
add(f"  成交量:     {volume:,.0f}")
add(f"  量比:       {vol_ratio:.2f}x")
add(f"  市值:       {market_cap/1e8:.1f} 億元" if market_cap else "  市值:       N/A")

# 2. 基本面
add("")
add("[2. 基本面分析]")
add("-"*70)
add(f"  EPS:        {eps:.2f} 元" if eps else "  EPS:        N/A")
add(f"  本益比:     {pe:.2f}x" if pe else "  本益比:     N/A")
add(f"  ROE:        {roe*100:.2f}%" if roe else "  ROE:        N/A")
add(f"  毛利率:     {gross_margin*100:.2f}%" if gross_margin else "  毛利率:     N/A")
add(f"  營業利益率: {op_margin*100:.2f}%" if op_margin else "  營業利益率: N/A")
add(f"  負債比:     {debt:.2f}%" if debt else "  負債比:     N/A")
add(f"  自由現金流: {fcf/1e8:.2f} 億元" if fcf else "  自由現金流: N/A")
add(f"  殖利率:     {div_yield*100:.2f}%" if div_yield else "  殖利率:     N/A")

# 基本面評分
add("")
add("  基本面評分:")
score = 0
if pe and 0 < pe < 20: score += 1; add("    PE < 20: 估值合理 +1")
elif pe and pe >= 20: add(f"    PE {pe:.1f}x: 估值偏高")
if roe and roe > 0.15: score += 1; add("    ROE > 15%: 獲利能力佳 +1")
elif roe and roe > 0.10: score += 1; add("    ROE > 10%: 獲利能力可 +1")
elif roe: add(f"    ROE {roe*100:.1f}%: 獲利能力待觀察")
if debt and debt < 100: score += 1; add("    負債比 < 100%: 財務穩健 +1")
elif debt: add(f"    負債比 {debt:.0f}%: 偏高")
if fcf and fcf > 0: score += 1; add("    自由現金流為正 +1")
add(f"    總分: {score}/4")

# 3. 技術面
add("")
add("[3. 技術面分析]")
add("-"*70)
add(f"  現價:   {price:.2f}")
add(f"  5MA:    {ma5:.2f}  {'[上方]' if price > ma5 else '[下方]'}")
add(f"  10MA:   {ma10:.2f}  {'[上方]' if price > ma10 else '[下方]'}")
add(f"  20MA:   {ma20:.2f}  {'[上方]' if price > ma20 else '[下方]'}")
if ma60: add(f"  60MA:   {ma60:.2f}  {'[上方]' if price > ma60 else '[下方]'}")
add(f"  RSI:    {rsi:.2f}  {'[超買]' if rsi > 70 else '[超賣]' if rsi < 30 else '[中性]'}")
add(f"  量比:   {vol_ratio:.2f}x  {'[爆量]' if vol_ratio > 2 else '[縮量]' if vol_ratio < 0.7 else '[正常]'}")

if price > ma5 > ma10 > ma20:
    add("  趨勢:   多頭排列 [偏多]")
elif price < ma5 < ma10 < ma20:
    add("  趨勢:   空頭排列 [偏空]")
else:
    add("  趨勢:   盤整 [中性]")

# 4. 三大法人
add("")
add("[4. 三大法人]")
add("-"*70)
inst = get_twse_institutional("2421")
if inst:
    add(f"  外資:   {inst['foreign']:>+12,} 張")
    add(f"  投信:   {inst['trust']:>+12,} 張")
    add(f"  自營商: {inst['dealer']:>+12,} 張")
    add(f"  合計:   {inst['total']:>+12,} 張")
    if inst['total'] > 0:
        add("  判讀:   法人買超 [偏多]")
    else:
        add("  判讀:   法人賣超 [偏空]")
else:
    add("  無法取得法人資料")

# 5. 新聞
add("")
add("[5. 最新消息]")
add("-"*70)
news = search_news("建準 2421", 4)
if news:
    for i, n in enumerate(news[:4], 1):
        add(f"  {i}. {n[:60]}...")
else:
    add("  今日無重大新聞")

# 6. 巴菲特分析
add("")
add("[6. 巴菲特框架分析]")
add("-"*70)
add("  建準電機業務:")
add("  - 散熱風扇、馬達、電源供應器")
add("  - 主要客戶: 伺服器、PC、家電")
add("  - AI 伺服器散熱需求受惠")
add("")

buffett_score = 0
add("  護城河評估:")
if gross_margin and gross_margin > 0.20:
    buffett_score += 1
    add(f"    毛利率 {gross_margin*100:.1f}% > 20%: 有一定護城河 +1")
else:
    add(f"    毛利率偏低: 護城河薄弱")

if roe and roe > 0.15:
    buffett_score += 1
    add(f"    ROE {roe*100:.1f}% > 15%: 資本效率佳 +1")

if debt and debt < 50:
    buffett_score += 1
    add(f"    負債比 {debt:.0f}% < 50%: 財務保守 +1")

if fcf and fcf > 0:
    buffett_score += 1
    add(f"    自由現金流為正: 現金創造能力佳 +1")

add(f"  巴菲特評分: {buffett_score}/4")

# 7. DCF 估值
add("")
add("[7. 簡化 DCF 估值]")
add("-"*70)
if eps and eps > 0:
    pe_low = eps * 12
    pe_mid = eps * 18
    pe_high = eps * 25
    add(f"  EPS: {eps:.2f} 元")
    add(f"  悲觀估值 (PE 12x): {pe_low:.2f} 元")
    add(f"  中性估值 (PE 18x): {pe_mid:.2f} 元")
    add(f"  樂觀估值 (PE 25x): {pe_high:.2f} 元")
    add(f"  現價: {price:.2f} 元")
    if price < pe_low:
        add(f"  估值判斷: 低估 [買進訊號]")
    elif price < pe_mid:
        add(f"  估值判斷: 合理偏低 [可考慮買進]")
    elif price < pe_high:
        add(f"  估值判斷: 合理 [持有]")
    else:
        add(f"  估值判斷: 偏高 [謹慎]")
else:
    add("  EPS 資料不足，無法估值")

# 8. CEO 最終裁決
add("")
add("="*70)
add("[8. CEO 最終裁決]")
add("="*70)

total_score = score + buffett_score
max_score = 8

add(f"  綜合評分: {total_score}/{max_score}")
add("")

if total_score >= 6:
    verdict = "買進"
    reason = "基本面佳，值得投資"
elif total_score >= 4:
    verdict = "觀察"
    reason = "基本面中等，等待更好進場點"
else:
    verdict = "謹慎"
    reason = "基本面待改善，不建議現在買進"

add(f"  裁決: {verdict}")
add(f"  理由: {reason}")
add("")
add("  CEO 團隊意見:")
add(f"    技術長: {'偏多' if price > ma20 else '偏空'}")
add(f"    財務長: {'財務穩健' if debt and debt < 100 else '財務偏高風險'}")
add(f"    投資長: {'有護城河' if buffett_score >= 2 else '護城河薄弱'}")
add(f"    巴菲特: {'符合價值投資' if buffett_score >= 3 else '不完全符合'}")
add("")
add("  注意事項:")
add("  - 數據有 15 分鐘延遲")
add("  - 僅供參考，投資決策請自行判斷")
add("  - 系統限制：無法預測未來")
add("="*70)

# 寫入檔案
with open('analysis_2421.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("分析完成！報告已儲存: analysis_2421.txt")
print(f"現價: {price:.2f} 元")
print(f"裁決: {verdict}")