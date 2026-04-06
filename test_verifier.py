# -*- coding: utf-8 -*-
"""測試計算驗證機制"""
import sys
sys.path.insert(0, 'scripts')
from calc_verifier import *

print("=" * 60)
print("計算驗證機制測試")
print("=" * 60)

# 測試1：驗證0050張數計算
print("\n【測試1】30萬可以買多少0050？")
print("-" * 60)
result = verify_shares(金額=300000, 價格=72.35)
print(f"公式：股數 = 金額 ÷ 價格")
print(f"計算：300,000 ÷ 72.35 = {result['可買股數']:,} 股")
print(f"驗證：{result['可買股數']:,} × 72.35 = {result['實際花費']:,.2f} 元")
print(f"餘額：{result['餘額']:,.2f} 元")
print(f"結果：{result['訊息']}")

# 測試2：驗證比例配置
print("\n【測試2】ETF配置比例是否正確？")
print("-" * 60)
result = verify_percentage([50, 25, 20, 5])
print(f"配置：0050(50%) + VOO(25%) + 美債(20%) + 00878(5%)")
print(f"總和：{result['總和']}%")
print(f"結果：{result['訊息']}")

# 測試3：驗證虧損
print("\n【測試3】佳世達虧損驗證")
print("-" * 60)
result = verify_loss(成本=53.78, 現價=22.75, 股數=6000)
print(f"佳世達：成本 53.78 → 現價 22.75")
print(f"虧損：({53.78} - {22.75}) × 6,000 股 = {result['虧損金額']:,.0f} 元")
print(f"虧損率：{result['虧損比例']}")
print(f"結果：{result['訊息']}")

print("\n" + "=" * 60)
print("測試完成")
print("=" * 60)
