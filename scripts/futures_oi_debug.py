# -*- coding: utf-8 -*-
"""
期貨未平倉 - Debug 版
"""
import requests
import warnings
warnings.filterwarnings('ignore')
import csv
import sys

def fetch_futures_oi(date='20260327'):
    url = 'https://www.taifex.com.tw/cht/3/futContractsDateDown'
    
    params = {
        'queryStartDate': f'{date[:4]}/{date[4:6]}/{date[6:8]}',
        'queryEndDate': f'{date[:4]}/{date[4:6]}/{date[6:8]}',
    }
    
    print(f"\n{'='*70}")
    print(f"DEBUG: TXF Futures OI - {date}")
    print(f"{'='*70}\n")
    
    try:
        r = requests.get(url, params=params, verify=False, timeout=20)
        text = r.content.decode('ms950')
        lines = text.split('\n')
        reader = csv.reader(lines)
        
        # 顯示前10行原始資料
        for i, row in enumerate(reader):
            if not row:
                continue
            
            # 顯示每一行的結構
            print(f"Row {i}: ", end="")
            for j, cell in enumerate(row[:8]):
                try:
                    print(f"[{j}={cell[:20]}] ", end="")
                except:
                    print(f"[{j}=ERR] ", end="")
            print()
            
            if i > 8:
                break
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    d = sys.argv[1] if len(sys.argv) > 1 else '20260327'
    fetch_futures_oi(d)
