# -*- coding: utf-8 -*-
"""
K線型態辨識 — 頭肩底、三重底、雙底等
資料來源：Yahoo Finance
指令：uv run --with yfinance python scripts/candlestick_patterns.py [stock_code]
"""
import sys
import warnings
warnings.filterwarnings('ignore')

def fetch_and_analyze(stock_code='2409'):
    """抓取並分析 K 線型態"""
    
    try:
        import yfinance as yf
    except:
        print("Installing yfinance...")
        import subprocess
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'yfinance'], check=True)
        import yfinance as yf
    
    symbol = f"{stock_code}.TW"
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period='6mo')
    
    if hist.empty:
        print(f"[ERROR] No data for {stock_code}")
        return
    
    closes = hist['Close'].tolist()
    highs = hist['High'].tolist()
    lows = hist['Low'].tolist()
    
    print(f"\n{'='*70}")
    print(f"[Candlestick Pattern Analysis] {stock_code} (6 months)")
    print(f"{'='*70}\n")
    
    # 簡單型態辨識
    patterns = []
    
    # 1. 雙底 (Double Bottom)
    if len(closes) >= 20:
        recent = closes[-20:]
        min_idx = recent.index(min(recent))
        if min_idx > 5 and min_idx < 15:
            left_min = min(recent[:min_idx])
            right_min = min(recent[min_idx:])
            if abs(left_min - right_min) / left_min < 0.05:  # 5% 容差
                patterns.append("Double Bottom (雙底) - BULLISH")
    
    # 2. 頭肩底 (Head and Shoulders Bottom)
    if len(closes) >= 30:
        recent = closes[-30:]
        # 簡化版：找三個低點
        lows_list = sorted(enumerate(recent), key=lambda x: x[1])[:3]
        if len(lows_list) == 3:
            idx1, val1 = lows_list[0]
            idx2, val2 = lows_list[1]
            idx3, val3 = lows_list[2]
            if idx1 < idx2 < idx3 and val2 < val1 and val2 < val3:
                patterns.append("Head and Shoulders Bottom (頭肩底) - BULLISH")
    
    # 3. 三重底 (Triple Bottom)
    if len(closes) >= 40:
        recent = closes[-40:]
        lows_list = sorted(enumerate(recent), key=lambda x: x[1])[:3]
        if len(lows_list) == 3:
            vals = [v for _, v in lows_list]
            if max(vals) - min(vals) < min(vals) * 0.03:  # 3% 容差
                patterns.append("Triple Bottom (三重底) - BULLISH")
    
    # 4. 上升趨勢 (Uptrend)
    if len(closes) >= 10:
        recent = closes[-10:]
        if recent[-1] > recent[0] and recent[-1] > max(recent[:-1]):
            patterns.append("Uptrend (上升趨勢) - BULLISH")
    
    # 5. 下降趨勢 (Downtrend)
    if len(closes) >= 10:
        recent = closes[-10:]
        if recent[-1] < recent[0] and recent[-1] < min(recent[:-1]):
            patterns.append("Downtrend (下降趨勢) - BEARISH")
    
    # 6. 整理區間 (Consolidation)
    if len(closes) >= 20:
        recent = closes[-20:]
        high = max(recent)
        low = min(recent)
        if (high - low) / low < 0.05:  # 5% 以內
            patterns.append("Consolidation (整理區間) - NEUTRAL")
    
    # 輸出
    print(f"Current Price: {closes[-1]:.2f}")
    print(f"52-week High: {max(closes):.2f}")
    print(f"52-week Low: {min(closes):.2f}")
    print(f"\nDetected Patterns:")
    
    if patterns:
        for p in patterns:
            print(f"  [+] {p}")
    else:
        print(f"  (No clear patterns detected)")
    
    print(f"\n{'='*70}\n")

if __name__ == '__main__':
    code = sys.argv[1] if len(sys.argv) > 1 else '2409'
    fetch_and_analyze(code)
