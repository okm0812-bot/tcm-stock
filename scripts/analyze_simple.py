#!/usr/bin/env python3
"""Simple stock analysis using yfinance - fallback version"""
import yfinance as yf
import sys

if len(sys.argv) < 2:
    print("Usage: python analyze_simple.py TICKER")
    sys.exit(1)

ticker = sys.argv[1].upper()
stock = yf.Ticker(ticker)

info = stock.info
print(f"=== {ticker} Analysis ===")
print(f"Current Price: {info.get('currentPrice', 'N/A')}")
print(f"52W High: {info.get('fiftyTwoWeekHigh', 'N/A')}")
print(f"52W Low: {info.get('fiftyTwoWeekLow', 'N/A')}")
print(f"P/E: {info.get('trailingPE', 'N/A')}")
print(f"EPS: {info.get('trailingEps', 'N/A')}")
print(f"Market Cap: {info.get('marketCap', 'N/A')}")
print(f"Volume: {info.get('volume', 'N/A')}")
print(f"Avg Volume: {info.get('averageVolume', 'N/A')}")
