# -*- coding: utf-8 -*-
"""
期貨夜盤資料 — Playwright（優化版）
"""
import asyncio
from playwright.async_api import async_playwright

async def fetch_night_session():
    print(f"\n{'='*60}")
    print(f"[TXF Night Session Data - 台指期夜盤]")
    print(f"{'='*60}\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto('https://www.wantgoo.com/futures/wtxp', 
                         wait_until='domcontentloaded', timeout=60000)
            await page.wait_for_timeout(10000)
            
            # 用 JS 解析
            data = await page.evaluate('''
                () => {
                    const result = {};
                    
                    // 嘗試找報價
                    const priceEl = document.querySelector('.price') || 
                                   document.querySelector('[class*="price"]') ||
                                   document.querySelector('span[class*="num"]');
                    
                    if (priceEl) result.price = priceEl.innerText;
                    
                    // 找所有文字
                    const text = document.body.innerText;
                    
                    // 找數字模式
                    const numbers = text.match(/\\d{4,}/g);
                    if (numbers) result.numbers = numbers.slice(0, 20);
                    
                    // 直接返回 body text
                    result.text = text;
                    
                    return result;
                }
            ''')
            
            print("解析結果:")
            print(f"  Price: {data.get('price', 'N/A')}")
            print(f"  Numbers: {data.get('numbers', [])[:10]}")
            
            # 顯示部分文字
            text = data.get('text', '')
            lines = text.split('\n')
            
            print(f"\n找到 {len(lines)} 行")
            
            # 找關鍵行
            for line in lines:
                line = line.strip()
                if len(line) > 5 and any(c.isdigit() for c in line):
                    # 只顯示包含大數字的行
                    if any(len(n) >= 4 for n in line.split()):
                        print(f"  {line[:60]}")
            
            print(f"\n[Source: WantGoo 期貨夜盤]")
            
        except Exception as e:
            print(f"Error: {e}")
        
        await browser.close()
    
    print(f"{'='*60}\n")

if __name__ == '__main__':
    asyncio.run(fetch_night_session())
