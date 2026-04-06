# -*- coding: utf-8 -*-
"""
期貨夜盤資料 — 整合版
"""
import asyncio
from playwright.async_api import async_playwright
import re

async def get_night_data():
    """取得台指期貨夜盤資料"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # 嘗試多個期貨報價頁面
            urls = [
                'https://www.wantgoo.com/futures/wtxp',
                'https://www.wantgoo.com/futures/TXF',
                'https://www.wantgoo.com/futures/international/TXF'
            ]
            
            for url in urls:
                try:
                    await page.goto(url, wait_until='domcontentloaded', timeout=30000)
                    await page.wait_for_timeout(5000)
                    
                    text = await page.evaluate('document.body.innerText')
                    
                    # 找數字報價
                    if 'TXF' in text or '台指' in text or any(c.isdigit() for c in text[:500]):
                        # 解析報價
                        numbers = re.findall(r'(\d{3,5}\.?\d*)', text)
                        
                        # 過濾合理的價格
                        prices = [n for n in numbers if 15000 < float(n.replace(',','')) < 25000]
                        
                        if prices:
                            return {
                                'source': url.split('/')[-1],
                                'price': prices[0] if prices else 'N/A',
                                'all_prices': prices[:5]
                            }
                except:
                    continue
            
            return None
            
        except Exception as e:
            return None
        finally:
            await browser.close()

def fetch_futures_night():
    """主函數"""
    print(f"\n{'='*60}")
    print(f"[TXF Night Session - 期貨夜盤]")
    print(f"{'='*60}\n")
    
    result = asyncio.run(get_night_data())
    
    if result:
        print(f"Source: {result.get('source', 'N/A')}")
        print(f"Price: {result.get('price', 'N/A')}")
        print(f"Prices found: {result.get('all_prices', [])}")
    else:
        print("[INFO] Night session data currently unavailable")
        print("       (Needs real-time futures API)")
    
    print(f"\n{'='*60}\n")
    
    return result

if __name__ == '__main__':
    fetch_futures_night()
