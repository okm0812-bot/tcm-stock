# -*- coding: utf-8 -*-
"""
融資融券 — Playwright JS 渲染（修正版）
"""
import asyncio
from playwright.async_api import async_playwright

async def fetch_margin():
    print(f"\n{'='*60}")
    print(f"[Margin Trading] Yahoo with Playwright")
    print(f"{'='*60}\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # 使用 domcontentloaded 而非 networkidle
            await page.goto('https://tw.stock.yahoo.com/margin-balance', 
                         wait_until='domcontentloaded', timeout=60000)
            
            # 等待一段時間讓 JS 執行
            await page.wait_for_timeout(8000)
            
            # 取得內容
            content = await page.content()
            print(f"Page loaded, length: {len(content)}")
            
            # 嘗試取得文字
            text = await page.evaluate('document.body.innerText')
            print(f"\nPage text (first 1000 chars):\n{text[:1000]}")
            
        except Exception as e:
            print(f"Error: {e}")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(fetch_margin())
