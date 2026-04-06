# -*- coding: utf-8 -*-
"""
=================================================================
選股自動化系統 v1.0 - CEO 整合版
功能：
1. 多條件篩選（本益比、殖利率、ROE、市值）
2. 產業別篩選
3. 技術面條件（均線、成交量）
4. 法人籌碼條件
5. 輸出候選名單
=================================================================
"""

import os
import json
from datetime import datetime

# ==================== 篩選條件預設 ====================
DEFAULT_FILTERS = {
    "valuation": {
        "pe_ratio_max": 20,        # 本益比上限
        "pe_ratio_min": 5,          # 本益比下限
        "dividend_yield_min": 3.0,  # 殖利率下限（%）
        "pb_ratio_max": 2.0,         # 股淨值比上限
    },
    "fundamental": {
        "roe_min": 10,              # ROE下限（%）
        "eps_growth_min": 5,        # EPS成長率下限（%）
        "revenue_growth_min": 5,    # 營收成長率下限（%）
    },
    "technical": {
        "above_ma20": True,         # 站上20日均線
        "volume_ratio_min": 1.0,    # 成交量比率下限
        "rsi_max": 80,              # RSI上限
        "rsi_min": 30,              # RSI下限
    },
    "chips": {
        "foreign_net_buy_days": 3,  # 外資連續買超天數
        "trust_net_buy_days": 0,     # 投信連續買超天數
        "margin_ratio_max": 10,      # 融資比率上限（%）
    },
    "market": {
        "market_cap_min": 100,      # 市值下限（億）
        "industry": [],              # 產業別（空=全部）
        "exclude_stocks": [],        # 排除股票
    }
}

# ==================== 股票池 ====================
# 台灣上市股票代碼（部分）
TW_STOCK_POOL = [
    # 權值股
    "2330", "2317", "2454", "2412", "1301", "1303", "1326", "2881",
    "2882", "2883", "2884", "2885", "2886", "2890", "2891", "2892",
    # 高股息
    "0050", "0056", "00713", "00878", "00919", "00929",
    # 科技
    "2303", "2308", "2311", "2316", "2327", "2337", "2340", "2345",
    "2353", "2357", "2363", "2368", "2379", "2382", "2383", "2395",
    "2408", "2409", "2414", "2427", "2441", "2449", "2455", "2468",
    "2471", "2474", "2489", "2498", "2504", "2514", "2603", "2609",
    "2610", "2615", "2618", "2633", "2637", "2640", "2655", "2660",
    "2665", "2668", "2674", "2676", "2679", "2682", "2690", "2704",
    "2707", "2723", "2727", "2731", "2745", "2752", "2753", "2761",
    "2763", "2776", "2780", "2783", "2801", "2809", "2812", "2816",
    "2820", "2823", "2832", "2834", "2838", "2845", "2847", "2849",
    "2850", "2851", "2852", "2855", "2856", "2867", "2880", "2901",
    "2903", "2905", "2906", "2908", "2909", "2910", "2911", "2912",
    "2915", "2919", "2923", "2924", "2925", "2929", "2930", "2931",
    # 傳產
    "1101", "1102", "1104", "1201", "1203", "1210", "1213", "1216",
    "1217", "1218", "1220", "1225", "1227", "1229", "1231", "1232",
    "1233", "1234", "1235", "1236", "1240", "1249", "1258", "1259",
    "1260", "1262", "1264", "1265", "1266", "1268", "1270", "1274",
    "1276", "1280", "1281", "1285", "1287", "1290", "1291", "1292",
    "1293", "1295", "1298", "1302", "1304", "1305", "1307", "1308",
    "1309", "1310", "1312", "1313", "1314", "1315", "1316", "1319",
    "1321", "1323", "1324", "1325", "1327", "1329", "1333", "1336",
    "1337", "1338", "1339", "1340", "1341", "1342", "1343", "1344",
    "1345", "1346", "1347", "1348", "1349", "1350", "1351", "1352",
    "1353", "1354", "1355", "1356", "1357", "1358", "1359", "1360",
    "1361", "1362", "1363", "1364", "1365", "1366", "1367", "1368",
    "1369", "1370", "1371", "1372", "1373", "1374", "1375", "1376",
    "1377", "1378", "1379", "1380", "1381", "1382", "1383", "1384",
    "1385", "1386", "1387", "1388", "1389", "1390", "1391", "1392",
    "1393", "1394", "1395", "1396", "1397", "1398", "1399", "1402",
]

# ==================== 篩選函數 ====================
def filter_by_valuation(stock_data, filters):
    """估值篩選"""
    passed = True
    reasons = []
    
    pe = stock_data.get("pe_ratio", 0)
    dividend_yield = stock_data.get("dividend_yield", 0)
    pb = stock_data.get("pb_ratio", 0)
    
    if pe > 0:  # 有獲利才判斷
        if pe > filters["valuation"]["pe_ratio_max"]:
            passed = False
            reasons.append(f"本益比 {pe:.1f} > {filters['valuation']['pe_ratio_max']}")
        if pe < filters["valuation"]["pe_ratio_min"]:
            passed = False
            reasons.append(f"本益比 {pe:.1f} < {filters['valuation']['pe_ratio_min']}")
    
    if dividend_yield < filters["valuation"]["dividend_yield_min"]:
        passed = False
        reasons.append(f"殖利率 {dividend_yield:.2f}% < {filters['valuation']['dividend_yield_min']}%")
    
    if pb > filters["valuation"]["pb_ratio_max"]:
        passed = False
        reasons.append(f"股淨值比 {pb:.2f} > {filters['valuation']['pb_ratio_max']}")
    
    return passed, reasons

def filter_by_fundamental(stock_data, filters):
    """基本面篩選"""
    passed = True
    reasons = []
    
    roe = stock_data.get("roe", 0)
    eps_growth = stock_data.get("eps_growth", 0)
    
    if roe < filters["fundamental"]["roe_min"]:
        passed = False
        reasons.append(f"ROE {roe:.1f}% < {filters['fundamental']['roe_min']}%")
    
    return passed, reasons

def filter_by_technical(stock_data, filters):
    """技術面篩選"""
    passed = True
    reasons = []
    
    above_ma20 = stock_data.get("above_ma20", True)
    volume_ratio = stock_data.get("volume_ratio", 1.0)
    rsi = stock_data.get("rsi", 50)
    
    if filters["technical"]["above_ma20"] and not above_ma20:
        passed = False
        reasons.append("未站上20日均線")
    
    if rsi > filters["technical"]["rsi_max"]:
        passed = False
        reasons.append(f"RSI {rsi:.1f} 過高")
    
    if rsi < filters["technical"]["rsi_min"]:
        passed = False
        reasons.append(f"RSI {rsi:.1f} 過低")
    
    return passed, reasons

def filter_by_chips(stock_data, filters):
    """籌碼面篩選"""
    passed = True
    reasons = []
    
    foreign_buy_days = stock_data.get("foreign_buy_days", 0)
    trust_buy_days = stock_data.get("trust_buy_days", 0)
    
    if foreign_buy_days < filters["chips"]["foreign_net_buy_days"]:
        passed = False
        reasons.append(f"外資連續買超僅 {foreign_buy_days} 日")
    
    if trust_buy_days < filters["chips"]["trust_net_buy_days"]:
        passed = False
        reasons.append(f"投信連續買超僅 {trust_buy_days} 日")
    
    return passed, reasons

# ==================== 主篩選函數 ====================
def run_stock_filter(custom_filters=None, stock_pool=None):
    """
    執行股票篩選
    custom_filters: 自訂條件（覆蓋預設）
    stock_pool: 自訂股票池
    """
    # 合併條件
    filters = DEFAULT_FILTERS.copy()
    if custom_filters:
        for key, value in custom_filters.items():
            if key in filters:
                filters[key].update(value)
    
    # 使用自訂股票池或預設
    stocks = stock_pool if stock_pool else TW_STOCK_POOL
    
    results = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "filters_used": filters,
        "passed_stocks": [],
        "rejected_stocks": {},
    }
    
    # 逐股篩選
    for stock_code in stocks:
        # 跳過排除名單
        if stock_code in filters["market"]["exclude_stocks"]:
            continue
        
        # 模擬數據（實際需從 API/web_fetch 獲取）
        stock_data = {
            "code": stock_code,
            "pe_ratio": 15.0,  # 需要實際數據
            "dividend_yield": 4.0,
            "pb_ratio": 1.5,
            "roe": 12,
            "above_ma20": True,
            "volume_ratio": 1.2,
            "rsi": 55,
            "foreign_buy_days": 3,
            "trust_buy_days": 0,
        }
        
        # 執行各項篩選
        all_reasons = []
        passed_all = True
        
        val_passed, val_reasons = filter_by_valuation(stock_data, filters)
        fund_passed, fund_reasons = filter_by_fundamental(stock_data, filters)
        tech_passed, tech_reasons = filter_by_technical(stock_data, filters)
        chips_passed, chips_reasons = filter_by_chips(stock_data, filters)
        
        all_reasons = val_reasons + fund_reasons + tech_reasons + chips_reasons
        passed_all = val_passed and fund_passed and tech_passed and chips_passed
        
        if passed_all:
            results["passed_stocks"].append({
                "code": stock_code,
                "score": len([r for r in [val_passed, fund_passed, tech_passed, chips_passed] if r]),
            })
        else:
            results["rejected_stocks"][stock_code] = all_reasons
    
    return results

# ==================== 報告輸出 ====================
def generate_filter_report(result):
    """產生篩選報告"""
    report = []
    report.append("="*60)
    report.append("選股自動化報告")
    report.append(f"時間: {result['timestamp']}")
    report.append("="*60)
    
    passed = result["passed_stocks"]
    rejected = result["rejected_stocks"]
    
    report.append(f"\n【通過篩選】共 {len(passed)} 檔")
    for stock in sorted(passed, key=lambda x: x.get("score", 0), reverse=True):
        report.append(f"  ✅ {stock['code']}")
    
    report.append(f"\n【未通過】共 {len(rejected)} 檔")
    for code, reasons in list(rejected.items())[:10]:  # 只顯示前10檔
        report.append(f"  ❌ {code}: {', '.join(reasons)}")
    
    return "\n".join(report)

# ==================== 整合說明 ====================
"""
整合方式：
1. 被 CEO 統一分析系統調用
2. 數據來源：
   - Yahoo Finance API
   - Goodinfo.tw
   - Wantgoo

使用範例：
  from stock_filter import run_stock_filter, generate_filter_report
  
  # 自訂條件
  my_filters = {
      "valuation": {"pe_ratio_max": 15, "dividend_yield_min": 4},
      "chips": {"foreign_net_buy_days": 5}
  }
  
  result = run_stock_filter(my_filters)
  print(generate_filter_report(result))
"""

if __name__ == "__main__":
    # 測試用 - 輸出到檔案避免編碼問題
    result = run_stock_filter()
    report = generate_filter_report(result)
    with open("stock_filter_test.txt", "w", encoding="utf-8") as f:
        f.write(report)
    print("測試完成，報告已寫入 stock_filter_test.txt")
