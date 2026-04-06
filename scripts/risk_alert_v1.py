# -*- coding: utf-8 -*-
"""
=================================================================
CEO 風險預警系統 v1.0 - 整合版
功能：
1. 大盤監控（漲跌 >3% 警告）
2. 持股監控（跌 >5% 警告）
3. 停損線監視
4. 自動發送通知
=================================================================
"""

import os
import json
import requests
from datetime import datetime
import time

# ==================== 持股資料 ====================
# 從 memory 或外部載入
PORTFOLIO = {
    "1101": {"shares": 19000, "avg_price": 34.56, "stop_loss": 20.00, "name": "台泥"},
    "2352": {"shares": 5000, "avg_price": 51.33, "stop_loss": 22.50, "name": "佳世達"},
    "2409": {"shares": 9000, "avg_price": 16.20, "stop_loss": 12.00, "name": "友達"},
    "6919": {"shares": 300, "avg_price": 102.36, "stop_loss": 85.00, "name": "康霈"},
}

# ==================== 設定 ====================
ALERT_CONFIG = {
    "twii_drop_threshold": 0.03,      # 大盤跌 >3% 警告
    "twii_rise_threshold": 0.03,       # 大盤漲 >3% 警告
    "stock_drop_threshold": 0.05,     # 持股跌 >5% 警告
    "stock_rise_threshold": 0.10,      # 持股漲 >10% 通知
}

# ==================== API 函數 ====================
def get_twii_price():
    """取得加權指數"""
    try:
        url = "https://tw.stock.yahoo.com/quote/%5ETWII"
        # 這裡需要用 web_fetch 或 requests
        return None
    except:
        return None

def get_stock_price(symbol):
    """取得個股價格"""
    try:
        url = f"https://tw.stock.yahoo.com/quote/{symbol}.TW"
        # 這裡需要用 web_fetch 或 requests
        return None
    except:
        return None

# ==================== 預警邏輯 ====================
def check_market_alert(twii_change):
    """檢查大盤預警"""
    alerts = []
    
    if twii_change <= -ALERT_CONFIG["twii_drop_threshold"]:
        alerts.append(f"⚠️ 大盤暴跌 {abs(twii_change)*100:.2f}%！")
    elif twii_change >= ALERT_CONFIG["twii_rise_threshold"]:
        alerts.append(f"🚀 大盤大漲 {twii_change*100:.2f}%")
    
    return alerts

def check_stock_alerts():
    """檢查持股預警"""
    alerts = []
    
    for symbol, data in PORTFOLIO.items():
        # 這裡用 webhook 或 API 獲取即時價格
        # 價格需要從外部傳入或即時抓取
        pass
    
    return alerts

def check_stop_loss():
    """檢查停損觸發"""
    triggers = []
    # 價格比對停損價
    return triggers

# ==================== 主程式 ====================
def run_risk_check(twii_now, stock_prices):
    """
    執行風險檢查
    twii_now: 現在的加權指數
    stock_prices: {"1101": 23.70, ...}
    """
    results = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "market_alerts": [],
        "stock_alerts": [],
        "stop_loss_triggers": [],
    }
    
    # 1. 大盤檢查
    # 需要昨天的收盤價來計算漲跌
    results["market_alerts"] = check_market_alert(0)  # 傳入漲跌比例
    
    # 2. 持股檢查
    results["stock_alerts"] = check_stock_alerts()
    
    # 3. 停損檢查
    results["stop_loss_triggers"] = check_stop_loss()
    
    return results

# ==================== 整合說明 ====================
"""
使用方式：
1. 透過 cron 每日定時執行
2. 價格資料從 web_fetch 獲取
3. 輸出結果到檔案或訊息

需要整合的功能：
- [x] institutional_fetch.py (法人資料)
- [x] 現有股價爬蟲腳本
- [x] daily_alert.py (現有警報)
- [ ] 需要一個統一調用介面
"""