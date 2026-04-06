# -*- coding: utf-8 -*-
"""
CEO v6.0 - 6147 完整分析
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

# 嘗試不同代碼格式
codes_to_try = ["6147.TWO", "6147.TW", "6147"]
ticker_data = None
real_code = None

for code in codes_to_try:
    try:
        ticker = yf.Ticker(code)
        info = ticker.info
        if info and info.get('regularMarketPrice'):
            ticker_data = ticker
            real_code = code
            info = ticker.info
            break
    except:
        continue

if not ticker_data:
    # 嘗試抓取資訊
    for code in codes_to_try:
        try:
            ticker = yf.Ticker(code)
            info = ticker.info
            if info:
                ticker_data = ticker
                real_code = code
                break
        except:
            continue

if not ticker_data:
    print("無法取得股票資料，請確認代碼是否正確")
    exit()

hist = ticker_data.history(period="3mo")

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
shares = safe_get(info, 'sharesOutstanding')

# 技術指標
ma5 = hist['Close'].tail(5).mean()
ma10 = hist['Close'].tail(10).mean()
ma20 = hist['Close'].tail(20).mean()
ma60 = hist['Close'].tail(60).mean() if len(hist) >= 60 else 0

delta = hist['Close'].diff()
gain = delta.where(delta > 0, 0).rolling(14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
rs = gain / loss
rsi_val = (100 - 100 / (1 + rs)).iloc[-1]

vol_ratio = volume / avg_volume if avg_volume else 0

# ==================== 報告 ====================
add("="*70)
add("CEO ANALYSIS v6.0 - 6147")
add("="*70)
add(f"分析時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
add(f"股票代碼: {real_code}")

# 1. 即時數據
add("")
add("[1. 即時數據]")
add("-"*70)
add(f"  現價:       {price:.2f} 元" if price else "  現價:       N/A")
add(f"  昨收:       {prev_close:.2f} 元" if prev_close else "")
add(f"  漲跌:       {change:+.2f} ({change_pct:+.2f}%)" if price and prev_close else "")
add(f"  52週高點:   {high_52:.2f} 元" if high_52 else "  52週高點:   N/A")
add(f"  52週低點:   {low_52:.2f} 元" if low_52 else "  52週低點:   N/A")
if price and high_52:
    add(f"  距高點:     {(price-high_52)/high_52*100:.1f}%")
if price and low_52:
    add(f"  距低點:     {(price-low_52)/low_52*100:+.1f}%")
add(f"  成交量:     {volume:,.0f}" if volume else "  成交量:     N/A")
add(f"  量比:       {vol_ratio:.2f}x" if vol_ratio else "")
add(f"  市值:       {market_cap/1e8:.1f} 億元" if market_cap else "  市值:       N/A")

# 2. 基本面
add("")
add("[2. 基本面分析]")
add("-"*70)
add(f"  EPS:        {eps:.2f} 元" if eps else "  EPS:        N/A")
add(f"  本益比:     {pe:.2f}x" if pe and pe > 0 else "  本益比:     N/A")
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
if eps:
    add(f"    EPS {eps:.2f}: +1")
    score += 1
if pe and 0 < pe < 25:
    add(f"    PE {pe:.1f}x 合理: +1")
    score += 1
if roe and roe > 0.10:
    add(f"    ROE {roe*100:.1f}%: +1")
    score += 1
if debt and debt < 100:
    add(f"    負債比 {debt:.0f}%: +1")
    score += 1
if fcf and fcf > 0:
    add(f"    FCF 正: +1")
    score += 1
add(f"    總分: {score}/5")

# 3. 技術面
add("")
add("[3. 技術面分析]")
add("-"*70)
add(f"  現價:   {price:.2f}" if price else "  現價:   N/A")
add(f"  5MA:    {ma5:.2f}" if ma5 else "")
add(f"  10MA:   {ma10:.2f}" if ma10 else "")
add(f"  20MA:   {ma20:.2f}" if ma20 else "")
if ma60: add(f"  60MA:   {ma60:.2f}")
add(f"  RSI:    {rsi_val:.2f}" if rsi_val else "")

if price and ma5 and ma10 and ma20:
    if price > ma5 > ma10 > ma20:
        trend = "多頭排列 [偏多]"
    elif price < ma5 < ma10 < ma20:
        trend = "空頭排列 [偏空]"
    else:
        trend = "盤整 [中性]"
    add(f"  趨勢:   {trend}")

# 4. 三大法人
add("")
add("[4. 三大法人]")
add("-"*70)
inst = get_twse_institutional("6147")
if inst:
    add(f"  外資:   {inst['foreign']:>+12,} 張")
    add(f"  投信:   {inst['trust']:>+12,} 張")
    add(f"  自營商: {inst['dealer']:>+12,} 張")
    add(f"  合計:   {inst['total']:>+12,} 張")
else:
    add("  無法取得法人資料（可能為上櫃/興櫃）")

# 5. 新聞
add("")
add("[5. 最新消息]")
add("-"*70)
news = search_news("6147", 4)
if news:
    for i, n in enumerate(news[:4], 1):
        add(f"  {i}. {n[:60]}...")
else:
    add("  今日無重大新聞")

# 6. 巴菲特分析
add("")
add("[6. 巴菲特框架分析]")
add("-"*70)

buffett_score = 0
if gross_margin:
    if gross_margin > 0.30:
        add(f"  毛利率 {gross_margin*100:.1f}% > 30%: 強護城河 +2")
        buffett_score += 2
    elif gross_margin > 0.20:
        add(f"  毛利率 {gross_margin*100:.1f}% > 20%: 有護城河 +1")
        buffett_score += 1
    elif gross_margin > 0.10:
        add(f"  毛利率 {gross_margin*100:.1f}%: 普通 +0")
    else:
        add(f"  毛利率 {gross_margin*100:.1f}%: 低護城河")

if roe:
    if roe > 0.20:
        add(f"  ROE {roe*100:.1f}% > 20%: 優秀 +2")
        buffett_score += 2
    elif roe > 0.15:
        add(f"  ROE {roe*100:.1f}% > 15%: 佳 +1")
        buffett_score += 1
    elif roe > 0.10:
        add(f"  ROE {roe*100:.1f}% > 10%: 可接受 +0")
    else:
        add(f"  ROE {roe*100:.1f}%: 偏低")

if debt:
    if debt < 50:
        add(f"  負債比 {debt:.0f}% < 50%: 保守 +2")
        buffett_score += 2
    elif debt < 100:
        add(f"  負債比 {debt:.0f}% < 100%: 正常 +1")
        buffett_score += 1

if fcf:
    if fcf > 0:
        add(f"  FCF 為正: +1")
        buffett_score += 1

add(f"  巴菲特評分: {buffett_score}/7")

# 7. DCF 估值
add("")
add("[7. 簡化 DCF 估值]")
add("-"*70)
if eps and eps > 0:
    pe_low = eps * 10
    pe_mid = eps * 15
    pe_high = eps * 22
    add(f"  EPS: {eps:.2f} 元")
    add(f"  悲觀 (PE 10x): {pe_low:.2f} 元")
    add(f"  中性 (PE 15x): {pe_mid:.2f} 元")
    add(f"  樂觀 (PE 22x): {pe_high:.2f} 元")
    add(f"  現價: {price:.2f} 元")
    if price < pe_low * 0.9:
        add(f"  估值: 明显低估 [強烈買進]")
    elif price < pe_low:
        add(f"  估值: 低估 [買進]")
    elif price < pe_mid:
        add(f"  估值: 合理偏低 [可考慮]")
    elif price < pe_high:
        add(f"  估值: 合理 [持有]")
    else:
        add(f"  估值: 偏高 [謹慎]")
else:
    add("  EPS 不足，無法估值")

# 8. CEO 裁決
add("")
add("="*70)
add("[8. CEO 最終裁決]")
add("="*70)

total_score = score + buffett_score
max_score = 12

add(f"  綜合評分: {total_score}/{max_score}")

if total_score >= 9:
    verdict = "分數佳"
    reason = "基本面良好，可考慮投資"
elif total_score >= 6:
    verdict = "中性"
    reason = "基本面中等，需進一步研究"
else:
    verdict = "待觀察"
    reason = "資料不足或基本面偏弱"

add(f"  裁決: {verdict}")
add(f"  理由: {reason}")
add("")
add("  CEO 團隊:")
add(f"    基本面: {score}/5")
add(f"    巴菲特: {buffett_score}/7")
add("")
add("  風險提示:")
add("  - 數據有 15 分鐘延遲")
add("  - 上櫃/興櫃股票流動性較低")
add("  - 請自行判斷投資決策")
add("="*70)

# 寫入
with open('analysis_6147.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"分析完成！")
print(f"代碼: {real_code}")
print(f"現價: {price}")
print(f"裁決: {verdict}")
print(f"總分: {total_score}/{max_score}")