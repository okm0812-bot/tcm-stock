# -*- coding: utf-8 -*-
"""
Adjusted Price Calculator - fetch historical adjusted prices from Yahoo Finance
"""
import sys, os
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import yfinance as yf
except ImportError:
    print("yfinance not installed. Run: pip install yfinance")
    sys.exit(1)

try:
    import pandas as pd
except ImportError:
    print("pandas not installed. Run: pip install pandas")
    sys.exit(1)


def fetch_adjusted_prices(symbol: str, days: int = 3650, output_path: str = None) -> dict:
    """
    Fetch adjusted prices and compute total return.
    symbol: Yahoo Finance symbol (e.g. "0050.TW")
    days: history days (default 3650 = 10 years)
    output_path: CSV output path; None = save next to script
    """
    try:
        print(f"\n[FETCH] {symbol} ({days} days)...")
        ticker = yf.Ticker(symbol)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        df = ticker.history(start=start_date, end=end_date, auto_adjust=False)
        if df.empty:
            return {"symbol": symbol, "error": "No data returned"}

        df["raw_close"] = df["Close"]
        df["adj_close"] = df["Adj Close"]
        df["daily_return"] = df["adj_close"].pct_change()
        initial = df["adj_close"].iloc[0]
        df["cum_return"] = (df["adj_close"] / initial - 1) * 100

        last_row = df.iloc[-1]
        print(f"  Rows: {len(df)} | Period: {df.index[0].strftime('%Y-%m-%d')} ~ {df.index[-1].strftime('%Y-%m-%d')}")
        print(f"  Adj Close: {last_row['adj_close']:.2f} | Cum Return: {last_row['cum_return']:.2f}%")

        if output_path is None:
            safe_symbol = symbol.replace(".", "_")
            output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"adjusted_{safe_symbol}.csv")

        out = df[["raw_close", "adj_close", "daily_return", "cum_return"]].copy()
        out.index = out.index.strftime("%Y-%m-%d")
        out.columns = ["Raw_Close", "Adj_Close", "Daily_Return_Pct", "Cum_Return_Pct"]
        out["Raw_Close"] = out["Raw_Close"].round(2)
        out["Adj_Close"] = out["Adj_Close"].round(2)
        out["Daily_Return_Pct"] = (out["Daily_Return_Pct"] * 100).round(4)
        out["Cum_Return_Pct"] = out["Cum_Return_Pct"].round(2)

        out.to_csv(output_path, encoding="utf-8-sig", index_label="Date")
        print(f"  [SAVE] {output_path}")

        annual = round((last_row["adj_close"] / initial) ** (365 / days) - 1, 4) * 100
        return {
            "symbol": symbol,
            "start_date": df.index[0].strftime("%Y-%m-%d"),
            "end_date": df.index[-1].strftime("%Y-%m-%d"),
            "rows": len(df),
            "start_adj": round(initial, 2),
            "end_adj": round(last_row["adj_close"], 2),
            "cum_return": round(last_row["cum_return"], 2),
            "annual_return": round(annual, 2),
            "csv_path": output_path,
            "error": None
        }
    except Exception as e:
        return {"symbol": symbol, "error": str(e)}


def fetch_dividends(symbol: str, days: int = 3650) -> dict:
    """Fetch dividend history."""
    try:
        ticker = yf.Ticker(symbol)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        divs = ticker.dividends
        # Filter by string comparison to avoid timezone comparison issues
        start_str = start_date.strftime("%Y-%m-%d")
        divs = divs[divs.index.strftime("%Y-%m-%d") >= start_str]
        if divs.empty:
            return {"symbol": symbol, "count": 0, "msg": "No dividends"}
        total = divs.sum()
        count = len(divs)
        return {
            "symbol": symbol,
            "count": count,
            "total": round(float(total), 4),
            "avg": round(float(total) / count, 4),
            "last": round(float(divs.iloc[-1]), 4),
            "last_date": divs.index[-1].strftime("%Y-%m-%d"),
            "msg": f"OK: {count} dividends, total {total:.2f}",
            "error": None
        }
    except Exception as e:
        return {"symbol": symbol, "error": str(e)}


if __name__ == "__main__":
    print("=" * 60)
    print("Adjusted Price Calculator")
    print("=" * 60)

    stocks = [
        ("0050.TW", 3650, "Yuan Da Taiwan 50"),
        ("1101.TW", 3650, "Taiwan Cement"),
        ("2409.TW", 3650, "AU Optronics"),
    ]

    results = []
    for sym, days, name in stocks:
        print(f"\n{'='*60}")
        print(f"[{sym}] {name}")
        print("=" * 60)

        res = fetch_adjusted_prices(sym, days)
        if res.get("error"):
            print(f"  ERROR: {res['error']}")
        else:
            results.append(res)
            print(f"\n  Summary:")
            print(f"    Period: {res['start_date']} ~ {res['end_date']}")
            print(f"    Adj Close: {res['start_adj']} -> {res['end_adj']}")
            print(f"    Cum Return: {res['cum_return']}%")
            print(f"    Annual: {res['annual_return']}%")
            print(f"    CSV: {res['csv_path']}")

        div = fetch_dividends(sym, days)
        if div.get("error"):
            print(f"  Dividend ERROR: {div['error']}")
        else:
            print(f"  Dividend: {div['msg']}")

    print(f"\n{'='*60}")
    print("ALL RESULTS")
    print("=" * 60)
    for r in results:
        print(f"  {r['symbol']}: {r['cum_return']}% / Annual {r['annual_return']}%")

    print(f"\nDONE")
    print("=" * 60)
