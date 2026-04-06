# -*- coding: utf-8 -*-
"""
YouTube 字幕 — Playwright 瀏覽器方法
"""
import asyncio
from playwright.async_api import async_playwright

async def get_youtube_subtitles():
    video_id = "EaN5QwdWgLw"
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    print(f"\n[YouTube Subtitles] {url}\n")
    print("="*60)
    
    async with async_playwright() as p:
        # 使用有頭模式，這樣更像真實用戶
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # 直接導航
            await page.goto(url, wait_until='networkidle', timeout=120000)
            await page.wait_for_timeout(15000)  # 等待頁面完全載入
            
            # 取得標題
            title = await page.title()
            print(f"標題: {title}\n")
            
            # 方法1: 嘗試點擊字幕按鈕
            # 找字幕相關的按鈕 (CC button)
            cc_buttons = await page.query_selector_all('button[aria-label*="CC"]')
            
            if cc_buttons:
                print("找到 CC 按鈕，嘗試點擊...")
                await cc_buttons[0].click()
                await page.wait_for_timeout(3000)
            
            # 方法2: 取得頁面文字
            print("取得頁面文字...")
            text_content = await page.evaluate('''
                () => {
                    // 嘗試取得影片標題
                    let title = document.querySelector('h1.ytd-video-primary-info-renderer')?.innerText;
                    
                    // 嘗試取得描述
                    let description = document.querySelector('#description')?.innerText;
                    
                    // 嘗試取得所有文字
                    let bodyText = document.body.innerText;
                    
                    return {
                        title: title,
                        description: description?.substring(0, 2000),
                        bodyText: bodyText?.substring(0, 5000)
                    };
                }
            ''')
            
            print("\n--- 標題 ---")
            print(text_content.get('title', 'N/A')[:200])
            
            print("\n--- 描述前500字 ---")
            desc = text_content.get('description', '')
            if desc:
                print(desc[:500])
            else:
                print("無描述")
            
            print("\n--- 頁面關鍵字 ---")
            body = text_content.get('bodyText', '')
            keywords = ['投資', '股票', '理財', '分析', '教學', '建議', '預測', '市場', '經濟', '賺錢', '錢', '獲利', '退休金', 'ETF', '基金']
            for kw in keywords:
                if kw in body:
                    print(f"  發現: {kw}")
            
            # 方法3: 嘗試找 transcript 元素
            print("\n--- 嘗試找字幕元素 ---")
            transcript_panel = await page.query_selector('ytd-transcript-renderer')
            if transcript_panel:
                print("找到字幕面板！")
                # 點擊它
                try:
                    await transcript_panel.click()
                    await page.wait_for_timeout(3000)
                    
                    # 取得字幕文字
                    transcript_text = await page.evaluate('''
                        () => {
                            let container = document.querySelector('ytd-transcript-body');
                            return container ? container.innerText : '';
                        }
                    ''')
                    
                    if transcript_text:
                        print(f"\n字幕內容 (前2000字):\n{transcript_text[:2000]}")
                except Exception as e:
                    print(f"點擊字幕失敗: {e}")
            
            print("\n" + "="*60)
            print("注意: YouTube 字幕需要登入或允許才能顯示")
            print("="*60)
            
        except Exception as e:
            print(f"Error: {e}")
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(get_youtube_subtitles())
