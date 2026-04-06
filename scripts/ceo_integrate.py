# -*- coding: utf-8 -*-
"""
=================================================================
CEO 整合調度系統 v1.0 - 統一調用三大模組
模組：
1. unified_chips.py - 法人籌碼整合
2. stock_filter.py - 選股自動化
3. risk_alert_v2.py - 風險預警

使用方式：
  python ceo_integrate.py --module=chips --stock=2317
  python ceo_integrate.py --module=filter --pe=15 --yield=4
  python ceo_integrate.py --module=alert
  python ceo_integrate.py --module=all
=================================================================
"""

import sys
import json
from datetime import datetime

# ==================== 模組導入 ====================
try:
    from unified_chips import analyze_stock_chips, generate_chips_report
    CHIPS_AVAILABLE = True
except ImportError:
    CHIPS_AVAILABLE = False

try:
    from stock_filter import run_stock_filter, generate_filter_report
    FILTER_AVAILABLE = True
except ImportError:
    FILTER_AVAILABLE = False

try:
    from risk_alert_v2 import run_full_alert_check, output_alerts
    ALERT_AVAILABLE = True
except ImportError:
    ALERT_AVAILABLE = False

# ==================== 健壯性包裝 ====================
def safe_run(func, *args, **kwargs):
    """安全執行函數，捕獲所有錯誤"""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        return {"error": str(e), "module": func.__name__}

# ==================== 統一調用介面（健壯版）====================
def run_chips_analysis(stock_code, days=5):
    """執行籌碼分析（健壯版）"""
    if not CHIPS_AVAILABLE:
        return {"error": "籌碼模組未載入", "module": "chips"}
    
    try:
        # 測試數據結構
        test_data = {
            "foreign": {"buy": 5000, "sell": 2000, "net": 3000},
            "investment_trust": {"net": 1000},
            "dealer": {"net": -500},
            "margin": {"margin_balance": 50000, "short_balance": 2000},
            "signals": ["[+] 外資連續買超 3 日"]
        }
        report = generate_chips_report(stock_code, test_data)
        
        return {
            "module": "chips",
            "stock_code": stock_code,
            "report": report,
            "status": "success",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {
            "module": "chips",
            "error": str(e),
            "status": "failed",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def run_stock_screening(custom_filters=None):
    """執行選股篩選"""
    if not FILTER_AVAILABLE:
        return {"error": "選股模組未載入"}
    
    result = run_stock_filter(custom_filters)
    report = generate_filter_report(result)
    
    return {
        "module": "filter",
        "passed_count": len(result["passed_stocks"]),
        "report": report,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def run_risk_check(market_data=None, stock_prices=None):
    """執行風險檢查"""
    if not ALERT_AVAILABLE:
        return {"error": "預警模組未載入"}
    
    # 預設測試數據（實際應從 API/web_fetch 獲取）
    if market_data is None:
        market_data = {
            "twii_now": 32000,
            "twii_prev": 32500,
            "vix": 25
        }
    
    if stock_prices is None:
        # 從持股資料讀取
        stock_prices = {
            "1101": 23.70,
            "2352": 23.30,
            "2409": 16.85,
            "6919": 95.0
        }
    
    alerts = run_full_alert_check(market_data, stock_prices)
    output = output_alerts(alerts, "risk_alert_now.txt")
    
    return {
        "module": "alert",
        "alert_count": len(alerts),
        "report": output,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def run_full_analysis(stock_code=None):
    """執行完整分析（三大模組整合）"""
    results = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "modules_run": []
    }
    
    # 1. 風險預警（最高優先）
    alert_result = run_risk_check()
    results["alert"] = alert_result
    results["modules_run"].append("alert")
    
    # 2. 籌碼分析
    if stock_code:
        chips_result = run_chips_analysis(stock_code)
        results["chips"] = chips_result
        results["modules_run"].append("chips")
    
    # 3. 選股篩選
    filter_result = run_stock_screening()
    results["filter"] = {
        "passed_count": filter_result.get("passed_count", 0),
        "top_10": filter_result.get("report", "").split("\n")[10:20] if filter_result.get("report") else []
    }
    results["modules_run"].append("filter")
    
    return results

# ==================== 報告輸出 ====================
def generate_integrated_report(results):
    """產生整合報告"""
    lines = []
    lines.append("="*70)
    lines.append("CEO 整合分析報告")
    lines.append(f"時間: {results['timestamp']}")
    lines.append("="*70)
    
    # 風險預警
    if "alert" in results:
        lines.append("\n【風險預警】")
        alert_report = results["alert"].get("report", "")
        lines.append(alert_report if alert_report else "無預警")
    
    # 籌碼分析
    if "chips" in results:
        lines.append("\n【籌碼分析】")
        chips_report = results["chips"].get("report", "")
        lines.append(chips_report if chips_report else "無資料")
    
    # 選股結果
    if "filter" in results:
        lines.append("\n【選股結果】")
        lines.append(f"通過篩選: {results['filter'].get('passed_count', 0)} 檔")
        if results['filter'].get('top_10'):
            lines.append("前10檔推薦:")
            for line in results['filter']['top_10']:
                lines.append(f"  {line}")
    
    return "\n".join(lines)

# ==================== CLI 介面 ====================
def main():
    """命令列介面"""
    args = sys.argv[1:]
    
    module = "all"
    stock_code = None
    custom_filters = {}
    
    # 解析參數
    for arg in args:
        if arg.startswith("--module="):
            module = arg.split("=")[1]
        elif arg.startswith("--stock="):
            stock_code = arg.split("=")[1]
        elif arg.startswith("--pe="):
            custom_filters["valuation"] = {"pe_ratio_max": int(arg.split("=")[1])}
        elif arg.startswith("--yield="):
            if "valuation" not in custom_filters:
                custom_filters["valuation"] = {}
            custom_filters["valuation"]["dividend_yield_min"] = float(arg.split("=")[1])
    
    # 執行對應模組
    if module == "chips":
        result = run_chips_analysis(stock_code or "2317")
    elif module == "filter":
        result = run_stock_screening(custom_filters if custom_filters else None)
    elif module == "alert":
        result = run_risk_check()
    else:
        result = run_full_analysis(stock_code)
    
    # 輸出報告
    report = generate_integrated_report(result)
    
    # 寫入檔案
    output_file = f"ceo_integrated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"分析完成，報告已寫入 {output_file}")
    return result

if __name__ == "__main__":
    main()
