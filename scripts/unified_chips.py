# -*- coding: utf-8 -*-
"""
=================================================================
法人籌碼統一介面 v1.0 - CEO 整合版
功能：
1. 三大法人買賣超（外資、投信、自營商）
2. 外資期貨未平倉
3. 投信庫存變化
4. 主力進出（融資融券）
5. 籌碼集中度分析
=================================================================
"""

import os
import json
from datetime import datetime, timedelta

# ==================== 資料結構 ====================
CHIPS_DATA = {
    "timestamp": "",
    "stock_code": "",
    "foreign": {
        "buy": 0,
        "sell": 0,
        "net": 0,
        "oi_change": 0,  # 未平倉變化
        "oi_total": 0,   # 未平倉總量
    },
    "investment_trust": {
        "buy": 0,
        "sell": 0,
        "net": 0,
        "holding_days": 0,  # 連續持有天數
    },
    "dealer": {
        "buy": 0,
        "sell": 0,
        "net": 0,
        "self_buy": 0,     # 自營商自行買賣
        "hedge_buy": 0,    # 避險買賣
    },
    "margin": {
        "margin_buy": 0,   # 融資買進
        "margin_sell": 0,  # 融資賣出
        "margin_balance": 0,  # 融資餘額
        "short_buy": 0,    # 融券買進
        "short_sell": 0,   # 融券賣出
        "short_balance": 0,  # 融券餘額
    },
    "concentration": {
        "top15_ratio": 0,  # 集中度（前15大券商）
        "diffusion": 0,    # 籌碼發散程度
    },
}

# ==================== 輔助函數 ====================
def get_date_str(days_ago=0):
    """取得日期字串"""
    date = datetime.now() - timedelta(days=days_ago)
    return date.strftime("%Y%m%d")

def format_number(num):
    """格式化數字（張/億）"""
    if abs(num) >= 100000:
        return f"{num/100000:.2f}億"
    elif abs(num) >= 1000:
        return f"{num/1000:.2f}千張"
    else:
        return f"{num}張"

# ==================== 籌碼分析函數 ====================
def analyze_chips_trend(data_list):
    """
    分析籌碼趨勢
    data_list: 近N日籌碼資料列表
    """
    if not data_list or len(data_list) < 2:
        return "資料不足"
    
    # 外資連續買/賣天數
    foreign_net_list = [d["foreign"]["net"] for d in data_list]
    
    foreign_streak = 0
    for net in foreign_net_list:
        if foreign_streak == 0:
            foreign_streak = 1 if net > 0 else -1 if net < 0 else 0
        elif foreign_streak > 0 and net > 0:
            foreign_streak += 1
        elif foreign_streak < 0 and net < 0:
            foreign_streak -= 1
        else:
            break
    
    # 投信連續買/賣天數
    trust_net_list = [d["investment_trust"]["net"] for d in data_list]
    trust_streak = 0
    for net in trust_net_list:
        if trust_streak == 0:
            trust_streak = 1 if net > 0 else -1 if net < 0 else 0
        elif trust_streak > 0 and net > 0:
            trust_streak += 1
        elif trust_streak < 0 and net < 0:
            trust_streak -= 1
        else:
            break
    
    return {
        "foreign_streak": foreign_streak,
        "trust_streak": trust_streak,
        "total_foreign": sum(foreign_net_list),
        "total_trust": sum(trust_net_list),
    }

def get_chips_signal(trend_data):
    """
    產生籌碼訊號
    """
    signals = []
    
    foreign_streak = trend_data.get("foreign_streak", 0)
    trust_streak = trend_data.get("trust_streak", 0)
    
    # 外資訊號
    if foreign_streak >= 3:
        signals.append("🟢 外資連續買超 {} 日".format(foreign_streak))
    elif foreign_streak <= -3:
        signals.append("🔴 外資連續賣超 {} 日".format(abs(foreign_streak)))
    
    # 投信訊號
    if trust_streak >= 5:
        signals.append("🟢 投信連續買超 {} 日（強勢）".format(trust_streak))
    elif trust_streak <= -5:
        signals.append("🔴 投信連續賣超 {} 日".format(abs(trust_streak)))
    
    # 法人同步訊號
    if foreign_streak > 0 and trust_streak > 0:
        signals.append("✅ 外資投信同步買超")
    elif foreign_streak < 0 and trust_streak < 0:
        signals.append("⚠️ 外資投信同步賣超")
    
    return signals

# ==================== 主分析函數 ====================
def analyze_stock_chips(stock_code, days=5):
    """
    分析個股籌碼（整合進 CEO 系統）
    """
    result = {
        "stock_code": stock_code,
        "analyze_date": datetime.now().strftime("%Y-%m-%d"),
        "data_days": days,
        "chips_summary": {},
        "trend": {},
        "signals": [],
    }
    
    # 這裡需要實際 API 或 web_fetch 獲取數據
    # 目前先返回結構框架
    
    return result

# ==================== 報告輸出 ====================
def generate_chips_report(stock_code, data):
    """
    產生籌碼報告（供 CEO 整合）
    """
    report = []
    report.append("="*60)
    report.append(f"法人籌碼分析 - {stock_code}")
    report.append("="*60)
    
    # 外資
    report.append("\n【外資】")
    report.append(f"  買超: {data['foreign']['buy']:,} 張")
    report.append(f"  賣超: {data['foreign']['sell']:,} 張")
    report.append(f"  淨買賣: {data['foreign']['net']:,} 張")
    
    # 投信
    report.append("\n【投信】")
    report.append(f"  淨買賣: {data['investment_trust']['net']:,} 張")
    
    # 自營商
    report.append("\n【自營商】")
    report.append(f"  淨買賣: {data['dealer']['net']:,} 張")
    
    # 融資融券
    report.append("\n【融資融券】")
    report.append(f"  融資餘額: {data['margin']['margin_balance']:,} 張")
    report.append(f"  融券餘額: {data['margin']['short_balance']:,} 張")
    
    # 訊號
    report.append("\n【籌碼訊號】")
    signals = data.get("signals", [])
    if signals:
        for s in signals:
            report.append(f"  {s}")
    else:
        report.append("  無明顯訊號")
    
    return "\n".join(report)

# ==================== 整合說明 ====================
"""
整合方式：
1. 被 CEO 統一分析系統調用
2. 數據來源：
   - institutional_fetch.py（三大法人）
   - yahoo_margin.py（融資融券）
   - wantgoo_oi.py（期貨未平倉）

使用範例：
  from unified_chips import analyze_stock_chips, generate_chips_report
  result = analyze_stock_chips("2317", days=5)
  report = generate_chips_report("2317", result)
"""

if __name__ == "__main__":
    # 測試用 - 輸出到檔案避免編碼問題
    test_data = {
        "foreign": {"buy": 5000, "sell": 2000, "net": 3000},
        "investment_trust": {"net": 1000},
        "dealer": {"net": -500},
        "margin": {"margin_balance": 50000, "short_balance": 2000},
        "signals": ["[+] 外資連續買超 3 日", "[OK] 外資投信同步買超"]
    }
    report = generate_chips_report("2317", test_data)
    with open("unified_chips_test.txt", "w", encoding="utf-8") as f:
        f.write(report)
    print("測試完成，報告已寫入 unified_chips_test.txt")
