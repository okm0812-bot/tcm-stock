# -*- coding: utf-8 -*-
"""
Enhanced Technical Indicators - scripts/ta_fetch.py
Extended with KDJ, OBV, ADX, Bollinger Band Width
"""
import sys, warnings
warnings.filterwarnings('ignore')
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import yfinance as yf
except ImportError:
    print("yfinance required: pip install yfinance")
    sys.exit(1)

try:
    import pandas as pd
    import numpy as np
except ImportError:
    print("pandas/numpy required: pip install pandas numpy")
    sys.exit(1)


def calc_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None
    deltas = np.diff(prices)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = gains[:period].mean()
    avg_loss = losses[:period].mean()
    for i in range(period, len(deltas)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(100 - 100 / (1 + rs), 2)


def calc_macd(prices, fast=12, slow=26, signal=9):
    if len(prices) < slow + signal:
        return None, None, None

    def ema(data, n):
        k = 2 / (n + 1)
        ema_val = np.mean(data[:n])
        result = [ema_val]
        for d in data[n:]:
            ema_val = d * k + ema_val * (1 - k)
            result.append(ema_val)
        return np.array(result)

    prices_arr = np.array(prices)
    ema_fast = ema(prices_arr, fast)
    ema_slow = ema(prices_arr, slow)
    macd_line = ema_fast[-len(ema_slow):] - ema_slow
    signal_line = ema(macd_line, signal)
    macd_val = macd_line[-1]
    signal_val = signal_line[-1]
    return round(float(macd_val), 4), round(float(signal_val), 4), round(float(macd_val - signal_val), 4)


def calc_bollinger(prices, period=20):
    if len(prices) < period:
        return None
    recent = prices[-period:]
    sma = np.mean(recent)
    std = np.std(recent, ddof=1)
    upper = sma + 2 * std
    lower = sma - 2 * std
    current = prices[-1]
    bandwidth = (upper - lower) / sma * 100 if sma != 0 else 0
    position = (current - lower) / (upper - lower) * 100 if upper != lower else 50
    return {
        "upper": round(float(upper), 2),
        "mid": round(float(sma), 2),
        "lower": round(float(lower), 2),
        "current": round(float(current), 2),
        "position_pct": round(float(position), 1),
        "bandwidth_pct": round(float(bandwidth), 2),
    }


def calc_kdj(high, low, close, period=9, m1=3, m2=3):
    """Calculate KDJ (Stochastic RSI variant)"""
    if len(close) < period:
        return None
    k_arr = []
    d_arr = []
    k = 50.0
    d = 50.0
    for i in range(period - 1, len(close)):
        window_high = max(high[i - period + 1:i + 1])
        window_low = min(low[i - period + 1:i + 1])
        if window_high == window_low:
            rsv = 50
        else:
            rsv = (close[i] - window_low) / (window_high - window_low) * 100
        k = (2/3) * k + (1/3) * rsv
        d = (2/3) * d + (1/3) * k
        k_arr.append(round(k, 2))
        d_arr.append(round(d, 2))
    j = 3 * k - 2 * d
    return {
        "K": round(k, 2),
        "D": round(d, 2),
        "J": round(j, 2),
        "K_arr": k_arr[-20:],
        "D_arr": d_arr[-20:],
    }


def calc_obv(closes, volumes):
    """On-Balance Volume - Energy indicator"""
    if len(closes) < 2 or len(volumes) < 2:
        return None
    obv = [0]
    for i in range(1, len(closes)):
        if closes[i] > closes[i-1]:
            obv.append(obv[-1] + volumes[i])
        elif closes[i] < closes[i-1]:
            obv.append(obv[-1] - volumes[i])
        else:
            obv.append(obv[-1])
    obv_arr = np.array(obv)
    # OBV trend: compare recent avg to earlier avg
    n = len(obv)
    recent_avg = np.mean(obv_arr[max(0, n-10):])
    earlier_avg = np.mean(obv_arr[max(0, n-20):n-10]) if n > 20 else np.mean(obv_arr[:max(1, n-10)])
    trend = "BULLISH (rising)" if recent_avg > earlier_avg else "BEARISH (falling)"
    return {
        "current": round(float(obv[-1]), 0),
        "recent_avg": round(float(recent_avg), 0),
        "earlier_avg": round(float(earlier_avg), 0),
        "trend": trend,
        "obv_array": obv_arr[-20:].tolist(),
    }


def calc_adx(high, low, close, period=14):
    """Average Directional Index - Trend strength"""
    if len(close) < period * 2:
        return None
    n = len(close)
    high_arr = np.array(high)
    low_arr = np.array(low)
    close_arr = np.array(close)

    # True Range
    tr = np.maximum(high_arr[1:] - low_arr[1:],
                    np.maximum(np.abs(high_arr[1:] - close_arr[:-1]),
                               np.abs(close_arr[:-1] - low_arr[1:])))

    # Directional Movement
    plus_dm = np.maximum(high_arr[1:] - high_arr[:-1], 0)
    minus_dm = np.maximum(low_arr[:-1] - low_arr[1:], 0)
    plus_dm = np.where((plus_dm > minus_dm) & (plus_dm > 0), plus_dm, 0)
    minus_dm = np.where((minus_dm > plus_dm) & (minus_dm > 0), minus_dm, 0)

    # Smooth with Wilder's EMA
    def wilder_smooth(data, n):
        result = [np.mean(data[:n])]
        for i in range(n, len(data)):
            result.append((result[-1] * (n - 1) + data[i]) / n)
        return np.array(result)

    if len(tr) < period:
        return None

    tr_s = wilder_smooth(tr, period)
    plus_dm_s = wilder_smooth(plus_dm, period)
    minus_dm_s = wilder_smooth(minus_dm, period)

    plus_di = np.where(tr_s != 0, plus_dm_s / tr_s * 100, 0)
    minus_di = np.where(tr_s != 0, minus_dm_s / tr_s * 100, 0)

    dx = np.where(plus_di + minus_di != 0,
                  np.abs(plus_di - minus_di) / (plus_di + minus_di) * 100, 0)

    adx = wilder_smooth(dx, period)
    if len(adx) < 1:
        return None

    adx_val = float(adx[-1])
    plus_di_val = float(plus_di[-1])
    minus_di_val = float(minus_di[-1])

    strength = "WEAK"
    if adx_val > 25:
        strength = "STRONG TREND"
    elif adx_val > 20:
        strength = "MODERATE"

    direction = "NEUTRAL"
    if plus_di_val > minus_di_val:
        direction = "BULLISH (+DI > -DI)"
    elif minus_di_val > plus_di_val:
        direction = "BEARISH (-DI > +DI)"

    return {
        "ADX": round(adx_val, 2),
        "plus_DI": round(plus_di_val, 2),
        "minus_DI": round(minus_di_val, 2),
        "strength": strength,
        "direction": direction,
    }


def analyze_full(symbol: str, period_days: int = 90) -> dict:
    """Full technical analysis with all indicators."""
    print(f"\nFetching {symbol} ({period_days}d)...")
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=f"{period_days + 30}d")

    if hist.empty:
        return {"error": "No data", "symbol": symbol}

    closes = hist["Close"].tolist()
    highs = hist["High"].tolist()
    lows = hist["Low"].tolist()
    volumes = hist["Volume"].tolist()

    results = {"symbol": symbol, "period_days": period_days}

    # Basic
    results["current_price"] = round(closes[-1], 2)
    results["volume"] = volumes[-1]

    # RSI
    rsi = calc_rsi(closes)
    results["RSI_14"] = rsi
    if rsi:
        if rsi > 70:
            results["RSI_signal"] = "OVERBOUGHT"
        elif rsi < 30:
            results["RSI_signal"] = "OVERSOLD"
        else:
            results["RSI_signal"] = "NEUTRAL"

    # MACD
    macd, signal, hist_val = calc_macd(closes)
    results["MACD"] = macd
    results["MACD_signal"] = signal
    results["MACD_histogram"] = hist_val
    if macd and signal:
        results["MACD_signal_text"] = "BULLISH" if macd > signal else "BEARISH"

    # Bollinger Bands
    bb = calc_bollinger(closes)
    results["BB"] = bb
    if bb:
        if closes[-1] > bb["upper"]:
            results["BB_signal"] = "UPPER BREAK - OVERBOUGHT"
        elif closes[-1] < bb["lower"]:
            results["BB_signal"] = "LOWER BREAK - OVERSOLD"
        else:
            results["BB_signal"] = "IN BAND"

    # KDJ
    kdj = calc_kdj(highs, lows, closes)
    results["KDJ"] = kdj
    if kdj:
        if kdj["K"] > 80 or kdj["J"] > 100:
            results["KDJ_signal"] = "OVERBOUGHT"
        elif kdj["K"] < 20 or kdj["J"] < 0:
            results["KDJ_signal"] = "OVERSOLD"
        else:
            results["KDJ_signal"] = "NEUTRAL"

    # OBV
    obv = calc_obv(closes, volumes)
    results["OBV"] = obv

    # ADX
    adx = calc_adx(highs, lows, closes)
    results["ADX"] = adx

    return results


def print_report(results: dict):
    print(f"\n{'='*60}")
    print(f"[{results['symbol']}] Technical Analysis Report")
    print(f"{'='*60}")
    print(f"  Price: {results['current_price']} | Vol: {results['volume']:,}")

    print(f"\n--- RSI ---")
    print(f"  RSI(14): {results['RSI_14']} => {results.get('RSI_signal', 'N/A')}")

    print(f"\n--- MACD ---")
    print(f"  MACD: {results['MACD']} | Signal: {results['MACD_signal']} | Hist: {results['MACD_histogram']}")
    print(f"  Signal: {results.get('MACD_signal_text', 'N/A')}")

    print(f"\n--- Bollinger Bands ---")
    bb = results.get("BB", {})
    if bb:
        print(f"  Upper: {bb['upper']} | Mid: {bb['mid']} | Lower: {bb['lower']}")
        print(f"  Position: {bb['position_pct']}% | Bandwidth: {bb['bandwidth_pct']}%")
        print(f"  Signal: {results.get('BB_signal', 'N/A')}")

    print(f"\n--- KDJ ---")
    kdj = results.get("KDJ", {})
    if kdj:
        print(f"  K: {kdj['K']} | D: {kdj['D']} | J: {kdj['J']}")
        print(f"  Signal: {results.get('KDJ_signal', 'N/A')}")

    print(f"\n--- OBV (Energy) ---")
    obv = results.get("OBV", {})
    if obv:
        print(f"  Current OBV: {obv['current']:,.0f}")
        print(f"  Trend: {obv['trend']}")

    print(f"\n--- ADX (Trend Strength) ---")
    adx = results.get("ADX", {})
    if adx:
        print(f"  ADX: {adx['ADX']} ({adx['strength']})")
        print(f"  +DI: {adx['plus_DI']} | -DI: {adx['minus_DI']}")
        print(f"  Direction: {adx['direction']}")

    print(f"\n{'='*60}")


if __name__ == "__main__":
    import sys
    symbol = sys.argv[1] if len(sys.argv) > 1 else "0050.TW"
    results = analyze_full(symbol)
    if results.get("error"):
        print(f"Error: {results['error']}")
    else:
        print_report(results)
