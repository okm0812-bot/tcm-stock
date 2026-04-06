# -*- coding: utf-8 -*-
"""
技能協調器 - CEO 統一分析系統
自動路由請求到正確的技能，避免衝突
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ==================== 7大模組定義 ====================
MODULES = {
    "quantitative": {
        "name": "量化模組",
        "core_skill": "finance-pro",
        "sub_skills": ["stock-strategy-backtester", "backtest-strategy-framework"],
        "output": ["Sharpe比率", "VaR風險價值", "CAGR年化報酬", "MDD最大回撤", "回測報告"],
        "route_keywords": ["Sharpe", "VaR", "CAGR", "MDD", "回測", "風險調整"]
    },
    "value": {
        "name": "價值模組",
        "core_skill": "buffett-investment",
        "sub_skills": ["competitor-benchmark", "simplified-dcf-valuation"],
        "output": ["護城河分析", "DCF估值", "安全邊際", "同業對標"],
        "route_keywords": ["護城河", "安全邊際", "DCF", "內在價值", "巴菲特", "價值投資"]
    },
    "fundamental": {
        "name": "基本面模組",
        "core_skill": "stock-research-engine",
        "sub_skills": ["earnings-tracker", "cashflow-analysis", "financial-ratio-deepdive"],
        "output": ["財報分析", "現金流", "杜邦分析", "ROE分解"],
        "route_keywords": ["財報", "EPS", "營收", "毛利率", "ROE", "基本面", "盈餘"]
    },
    "technical": {
        "name": "技術模組",
        "core_skill": "stock-info-explorer",
        "sub_skills": ["advanced-technical-indicators", "technical-risk-analysis"],
        "output": ["RSI", "MACD", "布林帶", "KDJ", "OBV", "ADX", "進場訊號"],
        "route_keywords": ["技術", "RSI", "MACD", "KDJ", "布林帶", "技術面", "支撐", "壓力"]
    },
    "risk": {
        "name": "風險模組",
        "core_skill": "stock-evaluator",
        "sub_skills": ["stock-monitor-skill", "comprehensive-alert-system"],
        "output": ["買/持有/賣", "停損建議", "預警系統", "風險評級"],
        "route_keywords": ["停損", "風險", "預警", "買", "賣", "持有", "風控", "評估"]
    },
    "macro": {
        "name": "總經模組",
        "core_skill": "macro-monitor",
        "sub_skills": ["macroeconomic-comprehensive", "market-researcher"],
        "output": ["Fed利率", "CPI", "GDP", "PMI", "失業率", "市場趨勢"],
        "route_keywords": ["Fed", "CPI", "GDP", "PMI", "利率", "總經", "宏觀", "美國經濟", "失業"]
    },
    "market": {
        "name": "市場模組",
        "core_skill": "news-summary",
        "sub_skills": ["institutional-flow-analysis", "industry-analysis-deepdive"],
        "output": ["最新消息", "法人流向", "產業分析", "五力分析"],
        "route_keywords": ["新聞", "消息", "法人", "外資", "產業", "五力"]
    }
}

# ==================== 路由函數 ====================
def route_request(query: str) -> dict:
    """
    根據查詢關鍵詞自動路由到正確的模組
    """
    query_lower = query.lower()
    
    scores = {}
    for module_id, module in MODULES.items():
        score = 0
        for keyword in module["route_keywords"]:
            if keyword.lower() in query_lower:
                score += 1
        
        # 核心技能匹配加權
        if module["core_skill"].lower() in query_lower:
            score += 3
        
        scores[module_id] = score
    
    # 選擇最高分
    if max(scores.values()) > 0:
        best_module = max(scores, key=scores.get)
        return {
            "module": best_module,
            "name": MODULES[best_module]["name"],
            "core_skill": MODULES[best_module]["core_skill"],
            "sub_skills": MODULES[best_module]["sub_skills"],
            "output": MODULES[best_module]["output"],
            "confidence": scores[best_module]
        }
    
    return None

# ==================== 衝突解決 ====================
def resolve_conflict(skill1: str, skill2: str) -> dict:
    """
    解決兩個技能的衝突
    """
    conflicts = {
        ("stock-info-explorer", "advanced-technical-indicators"): {
            "resolution": "基礎技術由 stock-info-explorer 負責，進階由 advanced-technical-indicators 負責"
        },
        ("stock-info-explorer", "technical-risk-analysis"): {
            "resolution": "技術訊號由 stock-info-explorer 負責，風險量化由 technical-risk-analysis 負責"
        },
        ("stock-evaluator", "stock-monitor-skill"): {
            "resolution": "買賣建議由 stock-evaluator 負責，預警由 stock-monitor-skill 負責"
        },
        ("stock-monitor-skill", "comprehensive-alert-system"): {
            "resolution": "7大預警由 stock-monitor-skill 負責，8維度由 comprehensive-alert-system 負責"
        },
        ("macro-monitor", "macroeconomic-comprehensive"): {
            "resolution": "基礎宏觀由 macro-monitor 負責，深度分析由 macroeconomic-comprehensive 負責"
        },
        ("finance-pro", "stock-strategy-backtester"): {
            "resolution": "量化指標由 finance-pro 負責，回測由 stock-strategy-backtester 負責"
        },
    }
    
    key = tuple(sorted([skill1, skill2]))
    return conflicts.get(key, {"resolution": "由CEO裁決"})

# ==================== 測試 ====================
def main():
    print("=" * 70)
    print("技能協調器測試")
    print("=" * 70)
    
    # 測試路由
    test_queries = [
        "分析台泥的RSI和MACD",
        "計算0050的Sharpe比率",
        "評估友達的買賣建議",
        "分析Fed利率決策",
        "查看最新的消息",
        "評估佳世達的護城河",
        "追蹤友達的法人流向",
        "計算風險VaR",
        "分析台泥的財報",
        "給出總經環境報告"
    ]
    
    print("\n【路由測試】")
    print("-" * 70)
    
    for query in test_queries:
        result = route_request(query)
        if result:
            print(f"\n📌 查詢：{query}")
            print(f"   → 路由至：{result['name']}")
            print(f"   → 核心技能：{result['core_skill']}")
            print(f"   → 輸出：{', '.join(result['output'][:3])}")
        else:
            print(f"\n📌 查詢：{query}")
            print(f"   → 需要CEO裁決")
    
    print("\n" + "=" * 70)
    print("【衝突解決測試】")
    print("-" * 70)
    
    test_conflicts = [
        ("stock-info-explorer", "advanced-technical-indicators"),
        ("stock-evaluator", "stock-monitor-skill"),
        ("macro-monitor", "macroeconomic-comprehensive"),
        ("finance-pro", "stock-strategy-backtester"),
    ]
    
    for skill1, skill2 in test_conflicts:
        result = resolve_conflict(skill1, skill2)
        print(f"\n⚡ {skill1} vs {skill2}")
        print(f"   解決方案：{result['resolution']}")
    
    print("\n" + "=" * 70)
    print("【整合後的7大模組】")
    print("=" * 70)
    
    for module_id, module in MODULES.items():
        print(f"\n📦 {module['name']}")
        print(f"   核心：{module['core_skill']}")
        print(f"   衛星：{', '.join(module['sub_skills'])}")
        print(f"   輸出：{', '.join(module['output'][:3])}")
    
    print("\n" + "=" * 70)
    print("✅ 衝突優化完成！")
    print("=" * 70)

if __name__ == "__main__":
    main()
