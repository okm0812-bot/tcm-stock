# -*- coding: utf-8 -*-
"""
融資融券 — CSV 解析（修正版）
"""
import requests
import warnings
warnings.filterwarnings('ignore')
import csv
import io
import sys

def fetch_margin_oi():
    url = 'https://www.twse.com.tw/cht/3/marginDownload'
    
    params = {
        'queryStartDate': '2026/03/27',
        'queryEndDate': '2026/03/27',
    }
    
    print(f"\n{'='*60}")
    print(f"[Margin Trading] CSV Download")
    print(f"{'='*60}\n")
    
    try:
        r = requests.get(url, params=params, verify=False, timeout=20)
        
        print(f"Status: {r.status_code}")
        
        if r.status_code == 200 and len(r.content) > 100:
            # 嘗試各種解碼
            for enc in ['utf-8', 'ms950', 'big5', 'cp950', 'latin1']:
                try:
                    text = r.content.decode(enc)
                    print(f"Decoded with: {enc}")
                    
                    # 檢查是否正常
                    if '融資' in text or '融券' in text or 'Margin' in text:
                        print(f"\n[SUCCESS] Found margin data!\n")
                        
                        # 解析
                        lines = text.split('\n')
                        for i, line in enumerate(lines[:30]):
                            if line.strip():
                                print(f"  {line[:80]}")
                        
                        return
                    
                except Exception as e:
                    continue
            
            # 如果都失敗，用 binary
            print("Using binary mode...")
            text = r.content.decode('utf-8', errors='replace')
            print(text[:500])
    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    fetch_margin_oi()
