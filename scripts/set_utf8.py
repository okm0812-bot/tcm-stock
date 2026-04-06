# -*- coding: utf-8 -*-
"""
設定 PowerShell UTF-8 編碼
"""
import subprocess
import sys

print("設定 PowerShell UTF-8 編碼...")

# 方法1: 設定控制台輸出為 UTF-8
import ctypes
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleOutputCP(65001)  # UTF-8

print("✓ 控制台輸出已設為 UTF-8")

# 測試中文
print("\n測試中文輸出:")
print("中文測試 - 繁體中文")
print("中文测试 - 简体中文") 
print("日本語テスト")
print("한국어 테스트")

print("\n如果上面都顯示正常，編碼設定成功！")