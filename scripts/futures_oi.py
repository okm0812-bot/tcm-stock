# -*- coding: utf-8 -*-
"""
期貨未平倉口數 — TAIEX 官方 ✅
使用方法: uv run --with requests python scripts/futures_oi.py [YYYYMMDD]
"""
import requests
import warnings
warnings.filterwarnings('ignore')
import sys

def fetch_futures_oi(date='20260327'):
    url = 'https://www.taifex.com.tw/cht/3/futContractsDateDown'
    params = {
        'queryStartDate': f'{date[:4]}/{date[4:6]}/{date[6:8]}',
        'queryEndDate': f'{date[:4]}/{date[4:6]}/{date[6:8]}',
    }
    
    print(f"\n[TXF Futures OI] {date}\n")
    
    try:
        r = requests.get(url, params=params, verify=False, timeout=20)
        text = r.content.decode('ms950')
        lines = text.split('\n')
        
        # 解析
        oi_long = 0
        oi_short = 0
        
        for i, line in enumerate(lines):
            parts = line.split(',')
            if len(parts) > 5 and date[:4] in line:
                try:
                    oi_val = int(parts[5].replace(',',''))
                except:
                    oi_val = 0
                
                if i == 1:
                    oi_long = oi_val
                elif i == 2:
                    oi_short = oi_val
        
        print("Category     | OI")
        print("-" * 25)
        print(f"Long(Buy)   | {oi_long:>12,}")
        print(f"Short(Sell) | {oi_short:>12,}")
        print("-" * 25)
        
        net = oi_long - oi_short
        print(f"Net         | {net:>+12,}")
        
        print(f"\n[Result]")
        if net > 0:
            print(f"  +{net:,} => Bullish (Long positions dominate)")
        elif net < 0:
            print(f"  {net:,} => Bearish (Short positions dominate)")
        else:
            print(f"  0 => Neutral")
        
        print(f"\nData: Taiwan Futures Exchange (TAIFEX)\n")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else '20260327'
    fetch_futures_oi(d)
