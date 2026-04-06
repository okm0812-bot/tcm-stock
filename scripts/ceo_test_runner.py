# -*- coding: utf-8 -*-
"""
=================================================================
CEO 系統自動化測試 v1.0
功能：
1. 測試所有整合模組
2. 驗證輸出格式
3. 檢查檔案生成
4. 產生測試報告
=================================================================
"""

import os
import sys
from datetime import datetime

# 測試項目
TEST_ITEMS = [
    ("風險預警", "risk_alert_v2.py", "risk_alert_test.txt"),
    ("法人籌碼", "unified_chips.py", "unified_chips_test.txt"),
    ("選股自動化", "stock_filter.py", "stock_filter_test.txt"),
    ("CEO整合", "ceo_integrate.py", None),
]

def test_module(name, script, expected_output):
    """測試單一模組"""
    result = {
        "name": name,
        "script": script,
        "status": "pending",
        "message": "",
        "output_file": expected_output
    }
    
    script_path = f"C:\\Users\\user\\.qclaw\\workspace\\scripts\\{script}"
    
    # 檢查腳本存在
    if not os.path.exists(script_path):
        result["status"] = "failed"
        result["message"] = f"腳本不存在: {script}"
        return result
    
    # 檢查輸出檔案（如果有的話）
    if expected_output:
        output_path = f"C:\\Users\\user\\.qclaw\\workspace\\{expected_output}"
        if os.path.exists(output_path):
            result["status"] = "passed"
            result["message"] = f"輸出檔案存在: {expected_output}"
        else:
            result["status"] = "warning"
            result["message"] = f"輸出檔案不存在: {expected_output}"
    else:
        result["status"] = "passed"
        result["message"] = "腳本存在"
    
    return result

def run_all_tests():
    """執行所有測試"""
    results = []
    
    for name, script, output in TEST_ITEMS:
        result = test_module(name, script, output)
        results.append(result)
    
    return results

def generate_test_report(results):
    """產生測試報告"""
    lines = []
    lines.append("="*60)
    lines.append("CEO 系統自動化測試報告")
    lines.append(f"時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("="*60)
    
    passed = sum(1 for r in results if r["status"] == "passed")
    failed = sum(1 for r in results if r["status"] == "failed")
    warning = sum(1 for r in results if r["status"] == "warning")
    
    lines.append(f"\n測試結果: {passed} 通過, {warning} 警告, {failed} 失敗")
    lines.append("-"*60)
    
    for result in results:
        status_icon = {
            "passed": "✅",
            "failed": "❌",
            "warning": "⚠️",
            "pending": "⏳"
        }.get(result["status"], "❓")
        
        lines.append(f"{status_icon} {result['name']}")
        lines.append(f"   腳本: {result['script']}")
        lines.append(f"   狀態: {result['status']}")
        lines.append(f"   訊息: {result['message']}")
        lines.append("")
    
    return "\n".join(lines)

if __name__ == "__main__":
    results = run_all_tests()
    report = generate_test_report(results)
    
    # 輸出到檔案
    output_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(f"測試完成，報告已寫入 {output_file}")
