# -*- coding: utf-8 -*-
"""
夜間分析 - 美股期貨 + 持股檢查
"""
import yfinance as yf
from datetime import datetime

lines = []
def add(text=''):
    lines.append(text)

# ==================== 美股期貨 ====================
add("="*60)
add("🌙 夜間市場追蹤")
add("="*60)
add(f"時間: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

add("\n【美股期貨】")
add("-"*60)

# S&P 500 期貨
sp = yf.Ticker("ES=F")
try:
    sp_info = sp.info
    sp_price = sp_info.get('regularMarketPrice', 0)
    sp_prev = sp_info.get('regularMarketPreviousClose', 0)
    sp_chg = sp_price - sp_prev if sp_prev else 0
    sp_pct = sp_chg / sp_prev * 100 if sp_prev else 0
    add(f"  S&P 500 期貨: {sp_price:,.2f} ({sp_chg:+,.2f}, {sp_pct:+.2f}%)")
except:
    add("  S&P 500 期貨: 無法取得")

# Nasdaq 期貨
nasdaq = yf.Ticker("NQ=F")
try:
    n_info = nasdaq.info
    n_price = n_info.get('regularMarketPrice', 0)
    n_prev = n_info.get('regularMarketPreviousClose', 0)
    n_chg = n_price - n_prev if n_prev else 0
    n_pct = n_chg / n_prev * 100 if n_prev else 0
    add(f"  Nasdaq 期貨:  {n_price:,.2f} ({n_chg:+,.2f}, {n_pct:+.2f}%)")
except:
    add("  Nasdaq 期貨: 無法取得")

# 台股期貨
tx = yf.Ticker("TX.F")
try:
    tx_info = tx.info
    tx_price = tx_info.get('regularMarketPrice', 0)
    tx_prev = tx_info.get('regularMarketPreviousClose', 0)
    tx_chg = tx_price - tx_prev if tx_prev else 0
    add(f"  台指期貨:     {tx_price:,.0f} ({tx_chg:+,.0f})")
except:
    add("  台指期貨:     資料有限")

# VIX
vix = yf.Ticker("^VIX")
try:
    v_info = vix.info
    v_price = v_info.get('regularMarketPrice', 0)
    add(f"  VIX 恐慌指數: {v_price:.2f}")
    if v_price > 25:
        add("    → [WARNING] 市場仍偏恐慌")
    elif v_price > 20:
        add("    → [CAUTION] 市場謹慎")
    else:
        add("    → [OK] 市場正常")
except:
    pass

# 美國10年債
tnx = yf.Ticker("^TNX")
try:
    t_info = tnx.info
    t_price = t_info.get('regularMarketPrice', 0)
    add(f"  美國10年債:   {t_price:.3f}%")
    if t_price > 4.5:
        add("    → [HIGH] 利率偏高，股市承壓")
    elif t_price < 4.0:
        add("    → [LOW] 利率偏低，股市有利")
    else:
        add("    → [NEUTRAL] 利率穩定")
except:
    pass

# ==================== 持股報價 ====================
add("\n【持股最新報價】")
add("-"*60)

stocks = [
    ("1101.TW", "台泥"),
    ("2352.TW", "佳世達"),
    ("2409.TW", "友達"),
    ("6919.TW", "康霈"),
]

for code, name in stocks:
    try:
        t = yf.Ticker(code)
        i = t.info
        price = i.get('regularMarketPrice', 0)
        prev = i.get('regularMarketPreviousClose', 0)
        chg = price - prev if prev else 0
        pct = chg / prev * 100 if prev else 0
        add(f"  {name:<8}: {price:>7.2f} ({chg:>+6.2f}, {pct:>+5.2f}%)")
    except:
        add(f"  {name:<8}: 無法取得")

# ==================== 明天開盤建議 ====================
add("\n" + "="*60)
add("📋 明天開盤操作建議")
add("="*60)

# 簡單判斷
add("\n根據夜間狀況分析:")
add("-"*60)

# 讀取今天報告
try:
    with open('CEO_MASTER_REPORT.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 抓關鍵數據
    import re
    matches = re.findall(r'(\d+\.\d+).*?(\+\d+,\d+|\-\d+,\d+)', content)
    add(f"\n持股狀況:")
    add(f"  台泥 1101: 續抱，等俄烏利多")
    add(f"  佳世達 2352: 停損設 22.00")
    add(f"  友達 2409: 續抱")
    add(f"  康霈 6919: 續抱")
    
except:
    pass

add(f"\n操作策略:")
add("-"*60)
add("  1. 台泥 1101:")
add("     → 續抱，殖利率 4%+ 可接受")
add("     → 關注俄烏戰爭進展")
add("")
add("  2. 佳世達 2352:")
add("     → 停損價 22.00 元")
add("     → 跌破果斷停損，不要猶豫")
add("")
add("  3. 友達 2409:")
add("     → 面板景氣觀望")
add("     → 續抱，等反彈")
add("")
add("  4. 康霈 6919:")
add("     → 生技股波動大，設 65 元停損")
add("     → 長期持有心態")
add("")
add("  5. 6147 頎邦:")
add("     → 等回調到 70-73 元再考慮")
add("     → 今晚先觀望")

add("\n" + "="*60)
add("🌙 夜間報告結束")
add("="*60)

# 寫入
with open('night_report.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print("夜間報告完成!")
print(f"VIX: {vix.info.get('regularMarketPrice', 'N/A')}")
print(f"美10年債: {tnx.info.get('regularMarketPrice', 'N/A')}%")