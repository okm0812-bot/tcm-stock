# -*- coding: utf-8 -*-
"""
台股爬蟲腳本 (twstock_scraper.py)
用途：從Goodinfo與Yahoo Finance爬取台股基本面資料
作者：投資分析系統增強版
"""

import sys
import os
import json
import time
import random
from datetime import datetime

# 確保 UTF-8 輸出
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ==================== 安裝必要套件 ====================
_required = []
try:
    import requests
except ImportError:
    _required.append("requests")
try:
    import yfinance as yf
except ImportError:
    _required.append("yfinance")
try:
    import pandas as pd
except ImportError:
    _required.append("pandas")

if _required:
    print(f"❌ 缺少套件：{', '.join(_required)}")
    print(f"   請先執行：pip install {' '.join(_required)}")
    sys.exit(1)


# ==================== Goodinfo 爬蟲函式 ====================

def scrape_goodinfo_financial(股票代號: str) -> dict:
    """
    從Goodinfo爬取基本面資料
    try/except防呆，若爬不到回傳「資料不足」
    
    參數：
        股票代號 (str)：台股代號（不含.TW）
    
    回傳：
        dict：基本面資料
    """
    try:
        # Goodinfo 基本面 URL
        url = f"https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID={股票代號}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.8",
            "Referer": "https://goodinfo.tw/"
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.encoding = "utf-8"
        html = response.text
        
        # 解析各項基本面（使用關鍵字定位）
        def extract_value(html, keywords, patterns=None):
            """通用解析函式"""
            for kw in keywords:
                if kw in html:
                    try:
                        # 嘗試找到數值
                        idx = html.index(kw)
                        snippet = html[idx:idx+300]
                        # 提取數字（可能帶有%或,）
                        import re
                        nums = re.findall(r'[-+]?\d+\.?\d*', snippet)
                        if nums:
                            return float(nums[0].replace(',', ''))
                    except:
                        continue
            return None
        
        result = {
            "代號": 股票代號,
            "資料來源": "Goodinfo",
            "更新時間": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "錯誤": None
        }
        
        # 嘗試解析營收年月（最新一期）
        營收 = extract_value(html, ["月營收", "營收", "營業收入"])
        result["最新營收"] = 營收
        result["營收狀態"] = "✅ 已取得" if 營收 else "❌ 資料不足"
        
        # 毛利率
        毛利率 = extract_value(html, ["毛利率", "Gross Margin"])
        result["毛利率"] = 毛利率
        result["毛利率狀態"] = "✅ 已取得" if 毛利率 else "❌ 資料不足"
        
        # 營益率
        營益率 = extract_value(html, ["營益率", "Operating Margin"])
        result["營益率"] = 營益率
        result["營益率狀態"] = "✅ 已取得" if 營益率 else "❌ 資料不足"
        
        # 淨利率
        淨利率 = extract_value(html, ["淨利率", "Net Margin", "純益率"])
        result["淨利率"] = 淨利率
        result["淨利率狀態"] = "✅ 已取得" if 淨利率 else "❌ 資料不足"
        
        # EPS
        eps = extract_value(html, ["EPS", "每股盈餘"])
        result["EPS"] = eps
        result["EPS狀態"] = "✅ 已取得" if eps else "❌ 資料不足"
        
        # ROE
        roe = extract_value(html, ["ROE", "股東權益報酬率"])
        result["ROE"] = roe
        result["ROE狀態"] = "✅ 已取得" if roe else "❌ 資料不足"
        
        # ROA
        roa = extract_value(html, ["ROA", "資產報酬率"])
        result["ROA"] = roa
        result["ROA狀態"] = "✅ 已取得" if roa else "❌ 資料不足"
        
        # 檢查是否真的取得任何資料
        關鍵欄位 = ["毛利率", "營益率", "淨利率", "EPS", "ROE", "ROA"]
        有效欄位 = [k for k in 關鍵欄位 if result.get(k) is not None]
        
        if len(有效欄位) < 3:
            result["錯誤"] = "❌ 資料不足：Goodinfo 無法取得足夠基本面資料"
        else:
            result["錯誤"] = None
        
        return result
        
    except requests.exceptions.Timeout:
        return {
            "代號": 股票代號,
            "錯誤": "❌ 資料不足：Goodinfo 連線逾時"
        }
    except requests.exceptions.RequestException as e:
        return {
            "代號": 股票代號,
            "錯誤": f"❌ 資料不足：網路錯誤 - {str(e)}"
        }
    except Exception as e:
        return {
            "代號": 股票代號,
            "錯誤": f"❌ 資料不足：解析錯誤 - {str(e)}"
        }


# ==================== Yahoo Finance 爬蟲函式 ====================

def scrape_yahoo_financial(股票代號: str) -> dict:
    """
    從Yahoo Finance爬取技術面與市場資料
    try/except防呆，若爬不到回傳「資料不足」
    
    參數：
        股票代號 (str)：Yahoo Finance 代號，例："1101.TW"
    
    回傳：
        dict：技術面與市場資料
    """
    try:
        ticker = yf.Ticker(股票代號)
        info = ticker.info
        
        result = {
            "代號": 股票代號,
            "資料來源": "Yahoo Finance",
            "更新時間": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "錯誤": None
        }
        
        # 52週高低
        week52_high = info.get("fiftyTwoWeekHigh")
        week52_low = info.get("fiftyTwoWeekLow")
        result["52週高"] = week52_high
        result["52週低"] = week52_low
        result["52週高低狀態"] = "✅ 已取得" if (week52_high and week52_low) else "❌ 資料不足"
        
        # 目前價格與均線關係
        current_price = info.get("currentPrice") or info.get("regularMarketPrice")
        ma50 = info.get("fiftyDayAverage")
        ma200 = info.get("twoHundredDayAverage")
        result["現價"] = current_price
        result["季線(MA50)"] = ma50
        result["年線(MA200)"] = ma200
        result["均線狀態"] = "✅ 已取得" if (current_price and ma50 and ma200) else "❌ 資料不足"
        
        # 位置判斷
        if current_price and ma50 and ma200:
            if current_price > ma50:
                result["位於季線"] = "✅ 上方"
            else:
                result["位於季線"] = "❌ 下方"
            
            if current_price > ma200:
                result["位於年線"] = "✅ 上方"
            else:
                result["位於年線"] = "❌ 下方"
        
        # 基本面
        result["PE"] = info.get("trailingPE")
        result["EPS"] = info.get("trailingEps")
        result["ROE"] = info.get("returnOnEquity")
        result["ROA"] = info.get("returnOnAssets")
        result["股息殖利率"] = info.get("dividendYield")
        result["beta"] = info.get("beta")
        result["市值"] = info.get("marketCap")
        
        # 成交量
        result["成交量"] = info.get("regularMarketVolume")
        
        return result
        
    except Exception as e:
        return {
            "代號": 股票代號,
            "錯誤": f"❌ 資料不足：Yahoo Finance 錯誤 - {str(e)}"
        }


# ==================== TWSE 法人買賣超 ====================

def scrape_institutional_flow(股票代號: str, 日期: str = None) -> dict:
    """
    從TWSE API抓取法人買賣超資料
    
    參數：
        股票代號 (str)：台股代號（不含.TW）
        日期 (str)：查詢日期，格式 YYYYMMDD，預設為最近交易日
    
    回傳：
        dict：法人買賣超資料
    """
    try:
        if 日期 is None:
            日期 = datetime.now().strftime("%Y%m%d")
        
        # TWSE API
        url = f"https://www.twse.com.tw/rwd/zh/fund/T86"
        params = {
            "date": 日期,
            "stockNo": 股票代號,
            "response": "json"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        
        if data.get("stat") != "OK" or not data.get("data"):
            return {
                "代號": 股票代號,
                "日期": 日期,
                "錯誤": "❌ 資料不足：TWSE 無法取得法人資料（非交易日或股票代號錯誤）"
            }
        
        # 解析法人資料（取最新一筆）
        rows = data["data"]
        latest = rows[-1]  # 最新一筆
        
        result = {
            "代號": 股票代號,
            "日期": latest[0] if latest else 日期,
            "資料來源": "TWSE",
            "更新時間": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "錯誤": None
        }
        
        # 法人欄位依序（依TWSE格式）
        # 外資, 投信, 自營商
        try:
            外資 = latest[4] if len(latest) > 4 else None  # 買賣差額
            投信 = latest[7] if len(latest) > 7 else None
            自營商 = latest[10] if len(latest) > 10 else None
            
            result["外資買賣超"] = 外資
            result["投信買賣超"] = 投信
            result["自營商買賣超"] = 自營商
            result["狀態"] = "✅ 已取得"
        except Exception as e:
            result["錯誤"] = f"❌ 資料不足：法人資料解析錯誤"
        
        return result
        
    except Exception as e:
        return {
            "代號": 股票代號,
            "日期": 日期,
            "錯誤": f"❌ 資料不足：TWSE API 錯誤 - {str(e)}"
        }


# ==================== 整合爬蟲 ====================

def full_scrape(股票代號: str, include_institutional: bool = True) -> dict:
    """
    完整爬取（Goodinfo + Yahoo Finance + TWSE）
    
    參數：
        股票代號 (str)：台股代號（不含.TW）
        include_institutional (bool)：是否爬取法人資料
    
    回傳：
        dict：完整基本面報告
    """
    print(f"\n🔍 完整爬取 {股票代號}...")
    
    result = {
        "代號": 股票代號,
        "爬取時間": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # 1. Yahoo Finance（優先，成功率高）
    print(f"  📡 Yahoo Finance...", end=" ")
    yahoo = scrape_yahoo_financial(f"{股票代號}.TW")
    if yahoo.get("錯誤"):
        print(f"❌")
        result["Yahoo"] = yahoo
    else:
        print(f"✅")
        result["Yahoo"] = yahoo
    
    # 隨機延遲避免被阻擋
    time.sleep(random.uniform(0.3, 0.8))
    
    # 2. Goodinfo（次要，成功率較低）
    print(f"  📡 Goodinfo...", end=" ")
    goodinfo = scrape_goodinfo_financial(股票代號)
    if goodinfo.get("錯誤"):
        print(f"❌")
        result["Goodinfo"] = {"錯誤": goodinfo.get("錯誤")}
    else:
        print(f"✅")
        result["Goodinfo"] = goodinfo
    
    # 3. TWSE 法人（最後）
    if include_institutional:
        print(f"  📡 TWSE 法人...", end=" ")
        inst = scrape_institutional_flow(股票代號)
        if inst.get("錯誤"):
            print(f"❌")
            result["TWSE法人"] = {"錯誤": inst.get("錯誤")}
        else:
            print(f"✅")
            result["TWSE法人"] = inst
    
    # 摘要
    已取得 = []
    if not result.get("Yahoo", {}).get("錯誤"):
        已取得.append("Yahoo")
    if not result.get("Goodinfo", {}).get("錯誤"):
        已取得.append("Goodinfo")
    if include_institutional and not result.get("TWSE法人", {}).get("錯誤"):
        已取得.append("TWSE")
    
    result["資料品質"] = f"{len(已取得)}/3"
    
    return result


# ==================== 主程式測試 ====================

if __name__ == "__main__":
    print("=" * 65)
    print("🌐 台股爬蟲腳本")
    print("=" * 65)
    
    # 測試標的
    測試標的 = [
        ("0050", "元大台灣50"),
        ("1101", "台泥"),
        ("2409", "友達"),
    ]
    
    for 代號, 名稱 in 測試標的:
        print(f"\n{'='*65}")
        print(f"🔍 {名稱} ({代號})")
        print(f"{'='*65}")
        
        結果 = full_scrape(代號, include_institutional=True)
        
        # 顯示Yahoo資料
        if 結果.get("Yahoo") and not 結果["Yahoo"].get("錯誤"):
            y = 結果["Yahoo"]
            print(f"\n  📊 Yahoo Finance 資料：")
            print(f"     52週區間：{y.get('52週低', '?')} ~ {y.get('52週高', '?')}")
            print(f"     現價：{y.get('現價', '?')}")
            print(f"     季線：{y.get('季線(MA50)', '?')}")
            print(f"     年線：{y.get('年線(MA200)', '?')}")
            print(f"     PE：{y.get('PE', '?')}")
            print(f"     EPS：{y.get('EPS', '?')}")
            print(f"     ROE：{y.get('ROE', '?')}")
        else:
            print(f"\n  ❌ Yahoo：{結果.get('Yahoo', {}).get('錯誤', '未知錯誤')}")
        
        # 顯示Goodinfo資料
        if 結果.get("Goodinfo") and not 結果["Goodinfo"].get("錯誤"):
            g = 結果["Goodinfo"]
            print(f"\n  📊 Goodinfo 資料：")
            for k in ["毛利率", "營益率", "淨利率", "EPS", "ROE", "ROA"]:
                v = g.get(k)
                s = g.get(f"{k}狀態", "")
                print(f"     {k}：{v} {s}")
        else:
            print(f"\n  ❌ Goodinfo：{結果.get('Goodinfo', {}).get('錯誤', '未知錯誤')}")
        
        # 顯示TWSE資料
        if 結果.get("TWSE法人") and not 結果["TWSE法人"].get("錯誤"):
            t = 結果["TWSE法人"]
            print(f"\n  📊 TWSE 法人資料：")
            print(f"     日期：{t.get('日期', '?')}")
            print(f"     外資買賣超：{t.get('外資買賣超', '?')}")
            print(f"     投信買賣超：{t.get('投信買賣超', '?')}")
            print(f"     自營商買賣超：{t.get('自營商買賣超', '?')}")
        else:
            print(f"\n  ❌ TWSE法人：{結果.get('TWSE法人', {}).get('錯誤', '未知錯誤')}")
        
        print(f"\n  資料品質：{結果.get('資料品質', '?')}/3")
        
        # 避免請求過快
        time.sleep(random.uniform(1, 2))
    
    print(f"\n{'='*65}")
    print("✅ 台股爬蟲完成")
    print("=" * 65)
