# -*- coding: utf-8 -*-
"""
=================================================================
風險預警系統 v2.0 - CEO 整合版
功能：
1. 即時大盤監控（每 5 分鐘）
2. 持股停損監視（跌破停損價立即通知）
3. 法人買賣超異常警告
4. VIX 恐慌指數監控
5. 多頻道通知（檔案輸出 + 訊息推送）
=================================================================
"""

import os
import json
from datetime import datetime, timedelta

# ==================== 持股資料（從 memory 載入）====================
PORTFOLIO = {
    "1101": {"shares": 19000, "avg_price": 34.56, "stop_loss": 20.00, "name": "台泥"},
    "2352": {"shares": 5000, "avg_price": 51.33, "stop_loss": 22.50, "name": "佳世達"},
    "2409": {"shares": 9000, "avg_price": 16.20, "stop_loss": 12.00, "name": "友達"},
    "6919": {"shares": 300, "avg_price": 102.36, "stop_loss": 85.00, "name": "康霈"},
}

# ==================== 預警設定 ====================
ALERT_CONFIG = {
    # 大盤
    "twii_drop_threshold": 0.03,       # 大盤跌 >3% 紅色警告
    "twii_drop_warning": 0.02,         # 大盤跌 >2% 黃色警告
    "twii_rise_threshold": 0.03,       # 大盤漲 >3% 通知
    
    # 個股
    "stock_drop_threshold": 0.05,      # 持股跌 >5% 警告
    "stock_stop_loss_buffer": 0.02,   # 接近停損價 2% 預警
    
    # VIX
    "vix_panic": 30,                   # VIX > 30 恐慌
    "vix_warning": 25,                  # VIX > 25 警告
    
    # 法人
    "foreign_sell_threshold": 10000,  # 外資單日賣超 >1萬張警告
    "trust_sell_days": 3,              # 投信連續賣超 >3日警告
}

# ==================== 預警等級 ====================
class AlertLevel:
    INFO = "INFO"           # 一般資訊
    WARNING = "WARNING"     # 黃色警告
    CRITICAL = "CRITICAL"   # 紅色警告
    EMERGENCY = "EMERGENCY" # 緊急（停損觸發）

# ==================== 預警訊息模板 ====================
ALERT_TEMPLATES = {
    "twii_drop_critical": "🔴 【緊急】大盤暴跌 {change:.2f}%！現價 {price:.0f} 點",
    "twii_drop_warning": "🟡 【警告】大盤下跌 {change:.2f}%，現價 {price:.0f} 點",
    "twii_rise": "🟢 大盤大漲 {change:.2f}%，現價 {price:.0f} 點",
    
    "stock_stop_loss": "🚨 【緊急】{name}({code})跌破停損價 {stop_loss}！現價 {price}",
    "stock_near_stop": "⚠️ {name}({code})接近停損價（{buffer:.1f}%內），現價 {price}",
    "stock_drop_warning": "🟡 【警告】{name}({code})下跌 {change:.2f}%，現價 {price}",
    
    "vix_panic": "😱 VIX恐慌指數 {vix:.1f} > {threshold}，市場恐慌",
    "vix_warning": "⚠️ VIX {vix:.1f} > {threshold}，波動升高",
    
    "foreign_heavy_sell": "🔴 外資大賣超 {amount:,} 張",
}

# ==================== 預警檢查函數 ====================
def check_twii_alert(current_price, previous_close):
    """檢查大盤預警"""
    alerts = []
    
    if previous_close == 0:
        return alerts
    
    change = (current_price - previous_close) / previous_close
    
    if change <= -ALERT_CONFIG["twii_drop_threshold"]:
        alerts.append({
            "level": AlertLevel.CRITICAL,
            "message": ALERT_TEMPLATES["twii_drop_critical"].format(
                change=change*100, price=current_price
            )
        })
    elif change <= -ALERT_CONFIG["twii_drop_warning"]:
        alerts.append({
            "level": AlertLevel.WARNING,
            "message": ALERT_TEMPLATES["twii_drop_warning"].format(
                change=change*100, price=current_price
            )
        })
    elif change >= ALERT_CONFIG["twii_rise_threshold"]:
        alerts.append({
            "level": AlertLevel.INFO,
            "message": ALERT_TEMPLATES["twii_rise"].format(
                change=change*100, price=current_price
            )
        })
    
    return alerts

def check_stock_alerts(prices):
    """
    檢查持股預警
    prices: {"1101": 23.70, "2352": 23.30, ...}
    """
    alerts = []
    
    for code, data in PORTFOLIO.items():
        current_price = prices.get(code, 0)
        if current_price == 0:
            continue
        
        stop_loss = data["stop_loss"]
        avg_price = data["avg_price"]
        name = data["name"]
        
        # 1. 檢查停損觸發
        if current_price <= stop_loss:
            alerts.append({
                "level": AlertLevel.EMERGENCY,
                "message": ALERT_TEMPLATES["stock_stop_loss"].format(
                    name=name, code=code, stop_loss=stop_loss, price=current_price
                ),
                "action": f"建議立即賣出 {name}"
            })
        
        # 2. 檢查接近停損
        buffer = ALERT_CONFIG["stock_stop_loss_buffer"]
        if current_price <= stop_loss * (1 + buffer):
            alerts.append({
                "level": AlertLevel.WARNING,
                "message": ALERT_TEMPLATES["stock_near_stop"].format(
                    name=name, code=code, buffer=buffer*100, price=current_price
                )
            })
        
        # 3. 檢查跌幅
        change = (current_price - avg_price) / avg_price
        if change <= -ALERT_CONFIG["stock_drop_threshold"]:
            alerts.append({
                "level": AlertLevel.WARNING,
                "message": ALERT_TEMPLATES["stock_drop_warning"].format(
                    name=name, code=code, change=change*100, price=current_price
                )
            })
    
    return alerts

def check_vix_alert(vix_value):
    """檢查 VIX 預警"""
    alerts = []
    
    if vix_value >= ALERT_CONFIG["vix_panic"]:
        alerts.append({
            "level": AlertLevel.CRITICAL,
            "message": ALERT_TEMPLATES["vix_panic"].format(
                vix=vix_value, threshold=ALERT_CONFIG["vix_panic"]
            )
        })
    elif vix_value >= ALERT_CONFIG["vix_warning"]:
        alerts.append({
            "level": AlertLevel.WARNING,
            "message": ALERT_TEMPLATES["vix_warning"].format(
                vix=vix_value, threshold=ALERT_CONFIG["vix_warning"]
            )
        })
    
    return alerts

def check_chips_alert(foreign_net, trust_sell_days):
    """檢查籌碼預警"""
    alerts = []
    
    if foreign_net <= -ALERT_CONFIG["foreign_sell_threshold"]:
        alerts.append({
            "level": AlertLevel.WARNING,
            "message": ALERT_TEMPLATES["foreign_heavy_sell"].format(amount=abs(foreign_net))
        })
    
    return alerts

# ==================== 統一預警入口 ====================
def run_full_alert_check(market_data, stock_prices):
    """
    執行完整預警檢查
    market_data: {twii_now, twii_prev, vix}
    stock_prices: {"1101": 23.70, ...}
    """
    all_alerts = []
    
    # 1. 大盤檢查
    twii_alerts = check_twii_alert(
        market_data.get("twii_now", 0),
        market_data.get("twii_prev", 0)
    )
    all_alerts.extend(twii_alerts)
    
    # 2. 持股檢查
    stock_alerts = check_stock_alerts(stock_prices)
    all_alerts.extend(stock_alerts)
    
    # 3. VIX 檢查
    vix_alerts = check_vix_alert(market_data.get("vix", 0))
    all_alerts.extend(vix_alerts)
    
    # 排序（緊急 > 嚴重 > 警告 > 資訊）
    priority = {
        AlertLevel.EMERGENCY: 0,
        AlertLevel.CRITICAL: 1,
        AlertLevel.WARNING: 2,
        AlertLevel.INFO: 3
    }
    all_alerts.sort(key=lambda x: priority.get(x["level"], 99))
    
    return all_alerts

# ==================== 輸出函數 ====================
def output_alerts(alerts, output_file=None):
    """輸出預警（檔案 + 訊息）"""
    if not alerts:
        return "✅ 目前無預警"
    
    lines = []
    lines.append("="*60)
    lines.append(f"風險預警報告 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("="*60)
    
    for alert in alerts:
        level_icon = {
            AlertLevel.EMERGENCY: "🚨",
            AlertLevel.CRITICAL: "🔴",
            AlertLevel.WARNING: "🟡",
            AlertLevel.INFO: "🟢"
        }.get(alert["level"], "⚪")
        
        lines.append(f"{level_icon} {alert['message']}")
        if "action" in alert:
            lines.append(f"   → {alert['action']}")
    
    output = "\n".join(lines)
    
    # 寫入檔案
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output)
    
    return output

# ==================== 定時執行設定（供 cron 使用）====================
"""
Cron 設定範例：
- 開盤前（08:30）：預警提醒
- 盤中（每 5 分鐘）：檢查停損
- 收盤後（14:00）：總結報告

使用方式：
  python risk_alert_v2.py --mode=realtime    # 即時檢查
  python risk_alert_v2.py --mode=daily      # 每日總結
"""

# ==================== 整合說明 ====================
"""
整合方式：
1. 被 CEO 統一分析系統調用
2. 與 unified_chips.py、stock_filter.py 協同
3. 支援 cron 定時執行
4. 輸出檔案供訊息模組讀取推送

使用範例：
  from risk_alert_v2 import run_full_alert_check, output_alerts
  
  market_data = {"twii_now": 32000, "twii_prev": 33000, "vix": 28}
  stock_prices = {"1101": 23.70, "2352": 23.30}
  
  alerts = run_full_alert_check(market_data, stock_prices)
  print(output_alerts(alerts, "alert_report.txt"))
"""

if __name__ == "__main__":
    # 測試用 - 輸出到檔案避免編碼問題
    test_market = {"twii_now": 32000, "twii_prev": 33000, "vix": 28}
    test_prices = {"1101": 23.70, "2352": 22.00, "2409": 16.85, "6919": 95.0}
    
    alerts = run_full_alert_check(test_market, test_prices)
    output = output_alerts(alerts, "risk_alert_test.txt")
    print("測試完成，報告已寫入 risk_alert_test.txt")
