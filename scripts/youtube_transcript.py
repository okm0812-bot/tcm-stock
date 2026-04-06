# -*- coding: utf-8 -*-
"""
YouTube 字幕抓取 — Playwright
"""
import asyncio
from playwright.async_api import async_playwright

async def get_youtube_transcript():
    video_id = "Ea5QwdWgLw"
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    print(f"\n[YouTube Transcript] {url}\n")
    print("="*60)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # 打開影片
            await page.goto(url, wait_until='domcontentloaded', timeout=60000)
            await page.wait_for_timeout(10000)  # 等待 JS 載入
            
            # 取得標題
            title = await page.title()
            print(f"標題: {title}\n")
            
            # 嘗試找字幕按鈕
            # YouTube 字幕按鈕通常是 "CC" 按鈕
            
            # 方法1: 嘗試點擊字幕按鈕
            cc_buttons = await page.query_selector_all('button[aria-label*="字幕"]')
            
            # 方法2: 取得影片描述
            description = await page.evaluate('''
                () => {
                    const elem = document.querySelector('#description');
                    return elem ? elem.innerText : "";
                }
            ''')
            
            if description:
                print(f"描述 (前500字):\n{description[:500]}\n")
            
            # 方法3: 取得頁面文字
            page_text = await page.evaluate('document.body.innerText')
            
            # 找關鍵字
            keywords = ['摘要', '投資', '股票', '分析', '教學', '理財', '經濟']
            for kw in keywords:
                if kw in page_text:
                    print(f"發現關鍵字: {kw}")
            
            print(f"\n[注意] YouTube 字幕需要用 official API 或特定工具才能抓取")
            print(f"建議: 1. 用 YouTube 官方字幕功能")
            print(f"      2. 複製影片描述給我分析")
            
        except Exception as e:
            print(f"Error: {e}")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(get_youtube_transcript())
