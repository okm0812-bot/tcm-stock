# -*- coding: utf-8 -*-
"""
期貨未平倉 — WantGoo 完整解析
"""
import requests
import warnings
warnings.filterwarnings('ignore')
import re
import json

def fetch_wantgoo_oi():
    url = 'https://www.wantgoo.com/futures/institutional-investors/net-open-interest'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }
    
    print(f"\n{'='*70}")
    print(f"[TXF Futures OI] WantGoo")
    print(f"{'='*70}\n")
    
    try:
        r = requests.get(url, headers=headers, verify=False, timeout=20)
        text = r.text
        
        # 直接搜索數字模式
        # 找 "多單", "空單", "淨額" 相關的數字
        
        # 找 JSON 數據
        json_pattern = r'data\s*:\s*(\[[^\]]+\])'
        matches = re.findall(json_pattern, text)
        
        if matches:
            print("Found data array")
            # 嘗試解析
            for m in matches[:3]:
                try:
                    data = json.loads(m)
                    print(f"Parsed: {data[:5] if len(data) > 5 else data}")
                except:
                    pass
        
        # 直接搜索數字
        # 格式可能是: 多單: 12345, 空單: 6789, 淨額: +5432
        
        # 找所有4-8位數字
        numbers = re.findall(r'(\d{4,8})', text)
        
        # 去重並排序
        unique_nums = sorted(set(numbers), key=lambda x: -int(x))[:30]
        
        print(f"\nLarge numbers found (possible OI values):")
        for n in unique_nums[:20]:
            print(f"  {int(n):,}")
        
        # 找包含 "口" 的文字
        kou_matches = re.findall(r'[^<>]{0,20}口[^<>]{0,20}', text)
        if kou_matches:
            print(f"\n'口' related text:")
            for m in kou_matches[:10]:
                # 清理
                clean = ''.join(x if x.isprintable() else ' ' for x in m)
                if len(clean.strip()) > 5:
                    print(f"  {clean.strip()[:50]}")
    
    except Exception as e:
        print(f"Error: {e}")
    
    print(f"{'='*70}\n")

if __name__ == '__main__':
    fetch_wantgoo_oi()
