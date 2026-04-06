# -*- coding: utf-8 -*-
"""
融資融券 — Yahoo 股市（最終版）
使用方法: uv run --with playwright python scripts/yahoo_margin.py
"""
import asyncio
from playwright.async_api import async_playwright

async def fetch_margin():
    print(f"\n{'='*60}")
    print(f"[Margin Trading - Yahoo Finance TW]")
    print(f"{'='*60}\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto('https://tw.stock.yahoo.com/margin-balance', 
                         wait_until='domcontentloaded', timeout=60000)
            await page.wait_for_timeout(8000)
            
            # 用 JS 解析數據
            data = await page.evaluate('''
                () => {
                    const text = document.body.innerText;
                    const lines = text.split('\\n');
                    const result = [];
                    
                    for (let i = 0; i < lines.length; i++) {
                        if (/202[56]\\/\\d{2}\\/\\d{2}/.test(lines[i])) {
                            let dataLine = lines[i];
                            for (let j = 1; j <= 6 && i+j < lines.length; j++) {
                                const nextLine = lines[i+j].trim();
                                if (nextLine && !nextLine.includes('20')) {
                                    dataLine += '|' + nextLine;
                                }
                            }
                            result.push(dataLine);
                        }
                    }
                    return result.slice(0, 5);
                }
            ''')
            
            # 解析並顯示
            print("Date        | 融資餘額   | 融券餘額   | 融資比率")
            print("-" * 55)
            
            for d in data:
                parts = d.replace('\\n', '|').split('|')
                if len(parts) >= 2:
                    date = parts[0][:10]
                    # 找到融資餘額和融券餘額
                    margin_bal = ""
                    short_bal = ""
                    ratio = ""
                    
                    for p in parts[1:]:
                        p = p.strip()
                        if ',' in p and 'M' not in p and len(p) > 3:
                            if not margin_bal:
                                margin_bal = p
                            elif not short_bal:
                                short_bal = p
                        if '%' in p:
                            ratio = p
                    
                    print(f"{date:12} | {margin_bal:>10} | {short_bal:>10} | {ratio:>6}")
            
            print(f"\n[Source: Yahoo Finance TW - Margin Trading]")
            
        except Exception as e:
            print(f"Error: {e}")
        
        await browser.close()
    
    print(f"{'='*60}\n")

if __name__ == '__main__':
    asyncio.run(fetch_margin())
