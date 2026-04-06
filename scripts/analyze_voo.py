# -*- coding: utf-8 -*-
"""
VOO Analysis Script - scripts/analyze_voo.py
Full analysis: Yahoo Finance data, P/E valuation, currency impact, dividend yield
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

from datetime import datetime, timedelta


def get_usd_twd_rate() -> float:
    """Fetch current USD/TWD exchange rate via Yahoo Finance."""
    try:
        rate = yf.Ticker("USDTWD=X").history(period="5d")
        if not rate.empty:
            return round(float(rate["Close"].iloc[-1]), 2)
    except Exception:
        pass
    # Fallback approximate rate
    return 32.5


def analyze_voo() -> str:
    """Run full VOO analysis and return report text."""
    ticker = yf.Ticker("VOO")
    info = ticker.info

    # Current data
    current_price = info.get("currentPrice") or info.get("regularMarketPrice")
    nav = info.get("navPrice")
    pe_ratio = info.get("trailingPE")
    forward_pe = info.get("forwardPE")
    dividend_yield = info.get("dividendYield")
    if dividend_yield:
        dividend_yield = dividend_yield * 100
    expense_ratio = info.get("expenseRatio")
    aum = info.get("totalAssets")
    week_52_high = info.get("fiftyTwoWeekHigh")
    week_52_low = info.get("fiftyTwoWeekLow")
    beta = info.get("beta")

    # Historical P/E for percentile
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365 * 5)

    hist = ticker.history(start=start_date, end=end_date, auto_adjust=False)
    if hist.empty:
        return "ERROR: Could not fetch VOO data"

    adj_close = hist["Adj Close"]
    price_now = adj_close.iloc[-1]
    price_year_ago = adj_close.iloc[-252] if len(adj_close) > 252 else adj_close.iloc[0]

    # Annual return
    annual_return = round((price_now / price_year_ago - 1) * 100, 2)

    # Fetch S&P 500 earnings data for P/E context
    sp500_pe = None
    try:
        sp500_ticker = yf.Ticker("^SPX")
        sp500_info = sp500_ticker.info
        sp500_pe = sp500_info.get("trailingPE")
    except Exception:
        pass

    # Currency impact
    usd_twd = get_usd_twd_rate()
    price_twd = round(price_now * usd_twd, 2)

    # Historical returns simulation
    returns_1y = []
    for i in range(252, len(adj_close)):
        r = (adj_close.iloc[i] / adj_close.iloc[i - 252] - 1) * 100
        returns_1y.append(r)

    pct_10 = round(np.percentile(returns_1y, 10), 2) if returns_1y else None
    pct_50 = round(np.percentile(returns_1y, 50), 2) if returns_1y else None
    pct_90 = round(np.percentile(returns_1y, 90), 2) if returns_1y else None

    # Valuation assessment
    if pe_ratio:
        if pe_ratio < 15:
            val_signal = "UNDERVALUED"
        elif pe_ratio < 20:
            val_signal = "FAIR VALUE"
        elif pe_ratio < 25:
            val_signal = "SLIGHTLY OVERVALUED"
        else:
            val_signal = "EXPENSIVE"
    else:
        val_signal = "N/A"

    # Dividend analysis
    div_history = ticker.dividends
    if not div_history.empty:
        last_div = float(div_history.iloc[-1])
        # Filter using string comparison to avoid timezone issues
        cutoff_str = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        divs_12m = div_history[div_history.index.strftime("%Y-%m-%d") >= cutoff_str]
        div_12m_total = float(divs_12m.sum())
    else:
        last_div = 0
        div_12m_total = 0

    div_yield_actual = round(div_12m_total / price_now * 100, 2) if price_now else 0

    # Build report
    report = []
    report.append("=" * 70)
    report.append(f"VOO ANALYSIS REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append("=" * 70)
    report.append("")
    report.append("--- BASIC INFO ---")
    report.append(f"  Current Price (USD): ${round(price_now, 2)}")
    report.append(f"  Price in TWD:        NT${price_twd:,.2f} (USD/TWD: {usd_twd})")
    report.append(f"  NAV:                  ${round(nav, 2) if nav else 'N/A'}")
    report.append(f"  52W High:             ${round(week_52_high, 2) if week_52_high else 'N/A'}")
    report.append(f"  52W Low:              ${round(week_52_low, 2) if week_52_low else 'N/A'}")
    report.append(f"  Distance from 52W High: {round((price_now/week_52_high-1)*100,2) if week_52_high else 'N/A'}%")
    report.append(f"  Beta vs Market:       {round(beta, 2) if beta else 'N/A'}")
    report.append(f"  AUM:                  ${round(aum/1e9, 2) if aum else 'N/A'}B")
    report.append(f"  Expense Ratio:        {round(expense_ratio*100, 2) if expense_ratio else 'N/A'}%")
    report.append("")
    report.append("--- VALUATION (P/E) ---")
    report.append(f"  Trailing P/E:         {round(pe_ratio, 2) if pe_ratio else 'N/A'}x")
    report.append(f"  Forward P/E:          {round(forward_pe, 2) if forward_pe else 'N/A'}x")
    report.append(f"  S&P 500 P/E:          {round(sp500_pe, 2) if sp500_pe else 'N/A'}x")
    report.append(f"  Valuation Signal:     {val_signal}")
    if pe_ratio and sp500_pe:
        diff = round(pe_ratio - sp500_pe, 2)
        report.append(f"  VOO vs SPX P/E diff: {diff:+g}x")
    report.append("")
    report.append("--- DIVIDEND YIELD ---")
    report.append(f"  12M Dividend Total:   ${round(div_12m_total, 4)}")
    report.append(f"  Dividend Yield:       {div_yield_actual}%")
    report.append(f"  Last Quarterly Div:   ${round(last_div, 4)}")
    report.append(f"  Yield in TWD:         {round(div_yield_actual, 2)}% (USD) | ~{round(div_yield_actual/usd_twd*100, 2) if usd_twd else 0}% equivalent")
    report.append("")
    report.append("--- CURRENCY IMPACT ---")
    report.append(f"  USD/TWD Rate:         {usd_twd}")
    report.append(f"  TWD depreciation risk: Historical avg ~1-2%/yr vs USD")
    report.append(f"  Hedged equivalent:    NT${round(price_twd, 2)} (includes currency risk)")
    report.append(f"  Annual currency cost: ~{round((1 - (usd_twd/32.0)) * 100, 1) if usd_twd else 0}% vs 32 TWD/USD baseline")
    report.append("")
    report.append("--- PERFORMANCE ---")
    report.append(f"  1-Year Return (USD):  {annual_return}%")
    report.append(f"  Historical 1Y Returns (5Y backtest):")
    report.append(f"    10th percentile:    {pct_10}%")
    report.append(f"    50th percentile:    {pct_50}%")
    report.append(f"    90th percentile:    {pct_90}%")
    report.append("")
    report.append("--- INVESTMENT VERDICT ---")
    if pe_ratio and pe_ratio < 20:
        verdict = "FAVORABLE - P/E below historical average"
    elif pe_ratio and pe_ratio > 25:
        verdict = "CAUTION - Elevated P/E, reduced margin of safety"
    else:
        verdict = "NEUTRAL - P/E at fair value"
    report.append(f"  {verdict}")
    report.append(f"  Currency note: Consider ETF currency-hedged variant if TWD volatility is a concern")
    report.append(f"  Dividend note: VOO dividends taxed 30% for Taiwan residents (WHT)")
    report.append("")
    report.append("=" * 70)

    return "\n".join(report)


if __name__ == "__main__":
    report = analyze_voo()
    print(report)

    # Save to file
    output_path = "C:/Users/user/.qclaw/workspace/analysis_VOO.txt"
    with open(output_path, "w", encoding="utf-8-sig") as f:
        f.write(report)
    print(f"\n[SAVED] {output_path}")
