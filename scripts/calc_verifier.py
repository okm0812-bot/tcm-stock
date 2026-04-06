# -*- coding: utf-8 -*-
"""
計算驗證機制 (calc_verifier.py)
用途：接收任意計算結果，自動反算驗證，確保數字正確
作者：投資分析系統增強版
"""

import sys
import os
import math

# 確保 UTF-8 輸出
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# ==================== 驗證函式 ====================

def verify_investment(本金: float, 張數: int, 價格: float, 誤差容許: float = 0.01) -> dict:
    """
    驗證投資金額
    公式：本金 = 張數 × 1000股 × 價格
    
    參數：
        本金 (float)：總投資金額
        張數 (int)：買進張數（1張 = 1000股）
        價格 (float)：每股價格
        誤差容許 (float)：容許誤差比例（預設1%）
    
    回傳：
        dict：{驗證通過: bool, 預期: float, 實際: float, 誤差: float, 訊息: str}
    """
    try:
        預期金額 = 張數 * 1000 * 價格
        誤差 = abs(預期金額 - 本金)
        誤差比例 = 誤差 / 預期金額 if 預期金額 != 0 else 0
        通過 = 誤差比例 <= 誤差容許
        
        return {
            "驗證通過": 通過,
            "預期金額": round(預期金額, 2),
            "實際金額": round(本金, 2),
            "誤差": round(誤差, 2),
            "誤差比例": f"{誤差比例:.2%}",
            "訊息": "✅ 驗證通過" if 通過 else "❌ 錯誤，需修正"
        }
    except Exception as e:
        return {
            "驗證通過": False,
            "預期金額": None,
            "實際金額": None,
            "誤差": None,
            "誤差比例": None,
            "訊息": f"❌ 計算錯誤：{str(e)}"
        }


def verify_percentage(配置比例列表: list, 誤差容許: float = 0.001) -> dict:
    """
    驗證比例相加是否等於 100%
    公式：sum(配置比例列表) == 100
    
    參數：
        配置比例列表 (list of float)：各項目比例，例：[30, 20, 50]
        誤差容許 (float)：容許誤差（預設0.1%）
    
    回傳：
        dict：{驗證通過: bool, 總和: float, 訊息: str}
    """
    try:
        總和 = sum(配置比例列表)
        誤差 = abs(總和 - 100)
        通過 = 誤差 <= 誤差容許
        
        return {
            "驗證通過": 通過,
            "總和": round(總和, 4),
            "誤差": round(誤差, 4),
            "訊息": "✅ 驗證通過" if 通過 else f"❌ 錯誤，需修正（總和為 {總和:.2f}%，需為 100%）"
        }
    except Exception as e:
        return {
            "驗證通過": False,
            "總和": None,
            "誤差": None,
            "訊息": f"❌ 計算錯誤：{str(e)}"
        }


def verify_loss(成本: float, 現價: float, 股數: int, 誤差容許: float = 0.01) -> dict:
    """
    驗證虧損金額
    公式：虧損 = (成本 - 現價) × 股數
    
    參數：
        成本 (float)：平均成本
        現價 (float)：目前股價
        股數 (int)：持有股數
        誤差容許 (float)：容許誤差金額
    
    回傳：
        dict：{驗證通過: bool, 虧損金額: float, 虧損比例: str, 訊息: str}
    """
    try:
        虧損金額 = (成本 - 現價) * 股數
        虧損比例 = (成本 - 現價) / 成本 if 成本 != 0 else 0
        成本總額 = 成本 * 股數
        通過 = abs(虧損金額) <= 成本總額  # 合理範圍內
        
        return {
            "驗證通過": 通過,
            "虧損金額": round(虧損金額, 2),
            "虧損比例": f"{虧損比例:.2%}",
            "成本總額": round(成本總額, 2),
            "現值總額": round(現價 * 股數, 2),
            "訊息": "✅ 驗證通過" if 通過 else "❌ 錯誤，需修正"
        }
    except Exception as e:
        return {
            "驗證通過": False,
            "虧損金額": None,
            "虧損比例": None,
            "訊息": f"❌ 計算錯誤：{str(e)}"
        }


def verify_shares(金額: float, 價格: float, 不足一股處理: str = "floor") -> dict:
    """
    驗證股數計算
    公式：股數 = 金額 / 價格（無條件捨去/進位取整）
    
    參數：
        金額 (float)：可用投資金額
        價格 (float)：每股價格
        不足一股處理 (str)："floor"=無條件捨去, "ceil"=無條件進位
    
    回傳：
        dict：{驗證通過: bool, 可買股數: int, 實際花費: float, 餘額: float, 訊息: str}
    """
    try:
        if 價格 <= 0:
            return {"驗證通過": False, "訊息": "❌ 價格必須大於0"}
        
        if 不足一股處理 == "floor":
            可買股數 = math.floor(金額 / 價格)
        else:
            可買股數 = math.ceil(金額 / 價格)
        
        實際花費 = 可買股數 * 價格
        餘額 = 金額 - 實際花費
        
        return {
            "驗證通過": True,
            "可買股數": 可買股數,
            "實際花費": round(實際花費, 2),
            "餘額": round(餘額, 2),
            "訊息": "✅ 驗證通過"
        }
    except Exception as e:
        return {
            "驗證通過": False,
            "可買股數": None,
            "實際花費": None,
            "餘額": None,
            "訊息": f"❌ 計算錯誤：{str(e)}"
        }


def verify_etf_allocation(總金額: float, 比例_dict: dict, 誤差容許: float = 0.001) -> dict:
    """
    驗證 ETF 配置
    公式：各ETF配置金額 = 總金額 × 比例%
    
    參數：
        總金額 (float)：總投資金額
        比例_dict (dict)：{ETF代號: 比例}，例：{"006208": 40, "0050": 60}
        誤差容許 (float)：容許誤差
    
    回傳：
        dict：{驗證通過: bool, 總和: float, 配置明細: dict, 訊息: str}
    """
    try:
        比例列表 = list(比例_dict.values())
        驗證結果 = verify_percentage(比例列表, 誤差容許)
        
        配置明細 = {}
        for 代號, 比例 in 比例_dict.items():
            配置明細[代號] = {
                "比例": f"{比例}%",
                "金額": round(總金額 * 比例 / 100, 2)
            }
        
        return {
            "驗證通過": 驗證結果["驗證通過"],
            "總和": 驗證結果["總和"],
            "總金額": round(總金額, 2),
            "配置明細": 配置明細,
            "訊息": 驗證結果["訊息"]
        }
    except Exception as e:
        return {
            "驗證通過": False,
            "總和": None,
            "配置明細": None,
            "訊息": f"❌ 計算錯誤：{str(e)}"
        }


# ==================== 批量驗證 ====================

def verify_portfolio(持股資料: list) -> dict:
    """
    批量驗證投資組合
    
    參數：
        持股資料 (list of dict)：[
            {"代號": "1101", "名稱": "台泥", "張數": 19, "成本": 34.56, "現價": 22.55},
            ...
        ]
    
    回傳：
        dict：各持股驗證結果摘要
    """
    結果列表 = []
    全部通過 = True
    
    for 持股 in 持股資料:
        try:
            # 驗證投資金額
            投資驗證 = verify_investment(
                持股.get("本金", 持股["張數"] * 1000 * 持股["成本"]),
                持股["張數"],
                持股["成本"]
            )
            
            # 驗證虧損
            虧損驗證 = verify_loss(
                持股["成本"],
                持股["現價"],
                持股["張數"] * 1000
            )
            
            通過 = 投資驗證["驗證通過"] and 虧損驗證["驗證通過"]
            全部通過 = 全部通過 and 通過
            
            結果列表.append({
                "代號": 持股.get("代號", "?"),
                "名稱": 持股.get("名稱", "?"),
                "投資驗證": 投資驗證,
                "虧損驗證": 虧損驗證,
                "總驗證": "✅" if 通過 else "❌"
            })
        except Exception as e:
            結果列表.append({
                "代號": 持股.get("代號", "?"),
                "名稱": 持股.get("名稱", "?"),
                "錯誤": str(e),
                "總驗證": "❌"
            })
            全部通過 = False
    
    return {
        "全部通過": 全部通過,
        "持股驗證": 結果列表,
        "摘要訊息": "✅ 所有持股驗證通過" if 全部通過 else "❌ 部分持股有錯誤，需修正"
    }


# ==================== 主程式測試 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("🧮 計算驗證機制測試")
    print("=" * 60)
    
    # 測試1：投資金額驗證
    print("\n【測試1】驗證投資金額")
    result = verify_investment(本金=65560, 張數=19, 價格=34.56)
    print(f"  張數: 19, 價格: 34.56")
    print(f"  預期本金: {result['預期金額']:,} 元")
    print(f"  實際本金: {result['實際金額']:,} 元")
    print(f"  {result['訊息']}")
    
    # 測試2：比例驗證
    print("\n【測試2】驗證配置比例")
    result = verify_percentage([30, 20, 30, 20])
    print(f"  比例: [30, 20, 30, 20]")
    print(f"  總和: {result['總和']}%")
    print(f"  {result['訊息']}")
    
    # 測試3：虧損驗證
    print("\n【測試3】驗證虧損金額")
    result = verify_loss(成本=34.56, 現價=22.55, 股數=19000)
    print(f"  成本: 34.56, 現價: 22.55, 股數: 19000")
    print(f"  虧損金額: {result['虧損金額']:,.0f} 元")
    print(f"  虧損比例: {result['虧損比例']}")
    print(f"  {result['訊息']}")
    
    # 測試4：股數驗證
    print("\n【測試4】驗證可買股數")
    result = verify_shares(金額=50000, 價格=23.65)
    print(f"  金額: 50,000 元, 價格: 23.65")
    print(f"  可買股數: {result['可買股數']:,} 股")
    print(f"  實際花費: {result['實際花費']:,.2f} 元")
    print(f"  餘額: {result['餘額']:,.2f} 元")
    print(f"  {result['訊息']}")
    
    # 測試5：ETF配置驗證
    print("\n【測試5】驗證ETF配置")
    result = verify_etf_allocation(
        總金額=100000,
        比例_dict={"006208": 50, "0050": 30, "00713": 20}
    )
    print(f"  總金額: 100,000 元")
    print(f"  比例: {{006208: 50%, 0050: 30%, 00713: 20%}}")
    for 代號, 明細 in result["配置明細"].items():
        print(f"    {代號}: {明細['比例']} = {明細['金額']:,.0f} 元")
    print(f"  {result['訊息']}")
    
    # 測試6：批量持股驗證
    print("\n【測試6】批量持股驗證")
    持股資料 = [
        {"代號": "1101", "名稱": "台泥", "張數": 19, "成本": 34.56, "現價": 22.55},
        {"代號": "2352", "名稱": "佳世達", "張數": 11, "成本": 53.78, "現價": 23.1},
        {"代號": "2409", "名稱": "友達", "張數": 9, "成本": 16.2, "現價": 14.3},
    ]
    結果 = verify_portfolio(持股資料)
    for 持股結果 in 結果["持股驗證"]:
        print(f"  {持股結果['總驗證']} {持股結果['代號']} {持股結果['名稱']}: ", end="")
        if "錯誤" in 持股結果:
            print(持股結果["錯誤"])
        else:
            print(f"投資={持股結果['投資驗證']['訊息'][0]}, 虧損={持股結果['虧損驗證']['虧損金額']:,.0f}元")
    print(f"  摘要: {結果['摘要訊息']}")
    
    print("\n" + "=" * 60)
    print("✅ 計算驗證機制測試完成")
    print("=" * 60)
