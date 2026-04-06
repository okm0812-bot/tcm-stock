# -*- coding: utf-8 -*-
"""
TurboScribe 字幕抓取
"""
import asyncio
from playwright.async_api import async_playwright

async def get_turbo_transcript():
    url = "https://turboscribe.ai/zh-TW/transcript/share/5548434741017151039/3gS07JZ4z_Gu2tV2z8Y2e2AvMXKoqjJ7Yhp4fZOTVL8/wei2-he2-mei3-yi1-zhan4-zheng1-hui4-rang4-gu3-shi4-beng1-6000-dian3-tai2-gu3-bao4-bao4-bao4"
    
    print(f"\n[TurboScribe Transcript]\n")
    print("="*60)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(url, wait_until='networkidle', timeout=60000)
            await page.wait_for_timeout(10000)
            
            # 取得頁面內容
            text = await page.evaluate('document.body.innerText')
            
            print(f"頁面載入成功，長度: {len(text)} 字\n")
            
            # 找主要內容
            print("-"*60)
            print("內容 (前5000字):")
            print("-"*60)
            print(text[:5000])
            
            if len(text) > 5000:
                print(f"\n... 共 {len(text)} 字")
            
        except Exception as e:
            print(f"Error: {e}")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(get_turbo_transcript())
