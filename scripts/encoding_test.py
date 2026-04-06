# -*- coding: utf-8 -*-
"""
編碼測試腳本
"""
import sys

print("Python 版本:", sys.version)
print("默認編碼:", sys.getdefaultencoding())
print()

# 測試中文輸出
test_strings = [
    "中文測試",
    "台灣股票",
    "投資分析",
    "⚠️ 警告符號",
    "✅ 打勾符號",
    "📊 圖表符號"
]

print("測試各種字符:")
for s in test_strings:
    try:
        print(f"  OK: {s}")
    except Exception as e:
        print(f"  FAIL: {e}")

print()
print("如果上面都顯示正常，編碼就沒問題了！")