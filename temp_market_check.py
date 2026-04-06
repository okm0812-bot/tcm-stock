# -*- coding: utf-8 -*-
import urllib.request
import json
import re

def fetch_tw_stock(symbol, name):
    """Fetch Taiwan stock from TWSE (simplified)"""
    # Use Yahoo Finance TW suffix
    yahoo_symbol = f'{symbol}.TW'
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{yahoo_symbol}?interval=1d&range=5d'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=15).read().decode())
        result = data['chart']['result']
        if result:
            meta = result[0]['meta']
            price = meta.get('regularMarketPrice')
            prev = meta.get('previousClose')
            if price and prev:
                change = ((price - prev) / prev) * 100
                print(f'{name} ({symbol}): ${price:.2f} (前收: ${prev:.2f}, 漲跌: {change:+.2f}%)')
                return price, prev
        print(f'{name} ({symbol}): 無數據')
    except Exception as e:
        print(f'{name} ({symbol}): Error - {str(e)[:50]}')
    return None, None

def fetch_index(symbol, name):
    """Fetch index"""
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=5d'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        data = json.loads(urllib.request.urlopen(req, timeout=15).read().decode())
        result = data['chart']['result']
        if result:
            meta = result[0]['meta']
            price = meta.get('regularMarketPrice')
            prev = meta.get('previousClose')
            if price and prev:
                change = ((price - prev) / prev) * 100
                print(f'{name}: {price:.2f} (前收: {prev:.2f}, 漲跌: {change:+.2f}%)')
                return price, prev
        print(f'{name}: 無數據')
    except Exception as e:
        print(f'{name}: Error - {str(e)[:50]}')
    return None, None

print('=' * 60)
print('台股與國際市場數據 - 2026/03/27')
print('=' * 60)

# 台股加權指數
print('\n【大盤指數】')
fetch_index('%5ETWII', '台股加權指數')

# 美國10年期公債殖利率
fetch_index('%5ETNX', '美國10年期公債殖利率')

# 台積電ADR
fetch_index('TSM', '台積電ADR')

print('\n' + '=' * 60)
print('持倉個股報價')
print('=' * 60)

# 持倉個股
holdings = [
    ('1101', '台泥'),
    ('2352', '佳世達'),
    ('2409', '友達'),
    ('3311', '閎暉'),
    ('6919', '康霈'),
]

for symbol, name in holdings:
    fetch_tw_stock(symbol, name)

print('\n' + '=' * 60)
print('美債ETF報價')
print('=' * 60)

# 美債ETF - Yahoo Finance symbol
bond_etfs = [
    ('00687B.TW', '國泰20年美債'),
    ('00795B.TW', '中信美國公債20年'),
]

for symbol, name in bond_etfs:
    fetch_index(symbol, name)
