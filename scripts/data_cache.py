# -*- coding: utf-8 -*-
"""
快取+更新機制 (data_cache.py)
用途：設定過期時間的資料快取，避免重複請求API
作者：投資分析系統增強版
"""

import sys
import os
import json
import time
from datetime import datetime, timedelta
from pathlib import Path

# 確保 UTF-8 輸出
sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# ==================== DataCache 類別 ====================

class DataCache:
    """
    資料快取類別
    
    功能：
    1. 設定過期時間（預設5分鐘）
    2. 快取讀取/寫入JSON
    3. 自動判斷是否需要更新
    4. 避免重複請求API
    """
    
    def __init__(self, 快取檔案路徑: str = None, 預設過期秒數: int = 300):
        """
        初始化 DataCache
        
        參數：
            快取檔案路徑 (str)：快取JSON檔案路徑，預設為工作目錄/stock_cache.json
            預設過期秒數 (int)：預設過期時間（秒），預設300=5分鐘
        """
        if 快取檔案路徑 is None:
            # 預設路徑：工作目錄/stock_cache.json
            work_dir = os.path.dirname(os.path.abspath(__file__))
            快取檔案路徑 = os.path.join(work_dir, "..", "stock_cache.json")
        
        self.快取檔案路徑 = os.path.abspath(快取檔案路徑)
        self.預設過期秒數 = 預設過期秒數
        
        # 確保目錄存在
        os.makedirs(os.path.dirname(self.快取檔案路徑), exist_ok=True)
        
        # 初始化快取結構
        self._快取: dict = self._讀取快取檔案()
    
    # ==================== 私有方法 ====================
    
    def _讀取快取檔案(self) -> dict:
        """讀取快取檔案（若不存在則回傳空dict）"""
        try:
            if os.path.exists(self.快取檔案路徑):
                with open(self.快取檔案路徑, "r", encoding="utf-8") as f:
                    return json.load(f)
            return {}
        except Exception as e:
            print(f"⚠️ 讀取快取檔案失敗：{e}，將建立新快取")
            return {}
    
    def _寫入快取檔案(self) -> None:
        """寫入快取檔案"""
        try:
            with open(self.快取檔案路徑, "w", encoding="utf-8") as f:
                json.dump(self._快取, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ 寫入快取檔案失敗：{e}")
    
    def _取得時間戳(self) -> float:
        """取得目前時間戳"""
        return time.time()
    
    # ==================== 公開方法 ====================
    
    def 取得(self, 金鑰: str, 過期秒數: int = None) -> tuple:
        """
        取得快取資料
        
        參數：
            金鑰 (str)：資料金鑰
            過期秒數 (int)：自訂過期時間，None則使用預設
        
        回傳：
            tuple: (資料, 是否過期/不存在)
            - 若有快取且未過期：回傳 (資料, False)
            - 若有快取但已過期：回傳 (資料, True)
            - 若無快取：回傳 (None, True)
        """
        if 過期秒數 is None:
            過期秒數 = self.預設過期秒數
        
        if 金鑰 not in self._快取:
            return (None, True)
        
        項目 = self._快取[金鑰]
        
        # 檢查時間戳
        時間戳 = 項目.get("timestamp", 0)
        現在時間 = self._取得時間戳()
        
        已過期 = (現在時間 - 時間戳) > 過期秒數
        
        return (項目.get("data"), 已過期)
    
    def 設定(self, 金鑰: str, 資料, 過期秒數: int = None) -> None:
        """
        設定快取資料
        
        參數：
            金鑰 (str)：資料金鑰
            資料：要快取的資料（需為JSON可序列化）
            過期秒數 (int)：自訂過期時間，None則使用預設
        """
        if 過期秒數 is None:
            過期秒數 = self.預設過期秒數
        
        self._快取[金鑰] = {
            "timestamp": self._取得時間戳(),
            "expires_in": 過期秒數,
            "data": 資料
        }
        
        self._寫入快取檔案()
    
    def 刪除(self, 金鑰: str) -> bool:
        """
        刪除快取項目
        
        參數：
            金鑰 (str)：資料金鑰
        
        回傳：
            bool：是否成功刪除
        """
        if 金鑰 in self._快取:
            del self._快取[金鑰]
            self._寫入快取檔案()
            return True
        return False
    
    def 清除全部(self) -> None:
        """清除所有快取"""
        self._快取 = {}
        self._寫入快取檔案()
    
    def 查詢狀態(self, 金鑰: str) -> dict:
        """
        查詢快取項目狀態
        
        參數：
            金鑰 (str)：資料金鑰
        
        回傳：
            dict：狀態資訊
        """
        if 金鑰 not in self._快取:
            return {"存在": False, "金鑰": 金鑰}
        
        項目 = self._快取[金鑰]
        時間戳 = 項目.get("timestamp", 0)
        過期秒數 = 項目.get("expires_in", self.預設過期秒數)
        現在時間 = self._取得時間戳()
        已過期 = (現在時間 - 時間戳) > 過期秒數
        
        剩餘秒數 = max(0, 過期秒數 - (現在時間 - 時間戳))
        
        return {
            "存在": True,
            "金鑰": 金鑰,
            "已過期": 已過期,
            "快取時間": datetime.fromtimestamp(時間戳).strftime("%Y-%m-%d %H:%M:%S"),
            "剩餘秒數": round(剩餘秒數, 0),
            "總有效秒數": 過期秒數
        }
    
    def 列出所有金鑰(self) -> list:
        """列出所有快取金鑰"""
        return list(self._快取.keys())
    
    def 需要更新(self, 金鑰: str, 過期秒數: int = None) -> bool:
        """
        判斷是否需要更新（快速檢查）
        
        參數：
            金鑰 (str)：資料金鑰
            過期秒數 (int)：自訂過期時間
        
        回傳：
            bool：True=需要更新，False=有快取且未過期
        """
        if 金鑰 not in self._快取:
            return True
        
        項目 = self._快取[金鑰]
        時間戳 = 項目.get("timestamp", 0)
        
        if 過期秒數 is None:
            過期秒數 = 項目.get("expires_in", self.預設過期秒數)
        
        現在時間 = self._取得時間戳()
        已過期 = (現在時間 - 時間戳) > 過期秒數
        
        return 已過期
    
    def 批量取得(self, 金鑰列表: list, 過期秒數: int = None) -> dict:
        """
        批量取得多個快取資料
        
        參數：
            金鑰列表 (list of str)：多個資料金鑰
            過期秒數 (int)：預設過期時間
        
        回傳：
            dict：{金鑰: (資料, 是否過期/不存在), ...}
        """
        結果 = {}
        for 金鑰 in 金鑰列表:
            結果[金鑰] = self.取得(金鑰, 過期秒數)
        return 結果
    
    def 批量設定(self, 資料_dict: dict, 過期秒數: int = None) -> None:
        """
        批量設定多個快取資料
        
        參數：
            資料_dict (dict)：{金鑰: 資料, ...}
            過期秒數 (int)：預設過期時間
        """
        for 金鑰, 資料 in 資料_dict.items():
            self.設定(金鑰, 資料, 過期秒數)


# ==================== 快捷工廠函式 ====================

def 建立快取(預設過期秒數: int = 300) -> DataCache:
    """
    建立快取實例（讀取現有stock_cache.json），
    若有舊資料且未過期則直接使用
    
    參數：
        預設過期秒數 (int)：預設過期時間（秒）
    
    回傳：
        DataCache：快取實例
    """
    # 嘗試讀取現有 stock_cache.json
    possible_paths = [
        os.path.join(os.getcwd(), "stock_cache.json"),
        os.path.join(os.path.dirname(__file__), "..", "stock_cache.json"),
    ]
    
    cache_path = None
    for path in possible_paths:
        if os.path.exists(path):
            cache_path = path
            break
    
    cache = DataCache(cache_path, 預設過期秒數)
    
    existing_keys = cache.列出所有金鑰()
    if existing_keys:
        print(f"📦 載入現有快取：金鑰 {len(existing_keys)} 個")
        for key in existing_keys:
            狀態 = cache.查詢狀態(key)
            print(f"   - {key}: {'🔴 已過期' if 狀態['已過期'] else '🟢 有效'} "
                  f"({狀態.get('剩餘秒數', '?')}秒)")
    else:
        print("📦 建立新快取")
    
    return cache


# ==================== 主程式測試 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("💾 快取+更新機制測試")
    print("=" * 60)
    
    # 建立快取（使用測試檔案）
    測試快取檔案 = os.path.join(os.path.dirname(__file__), "..", "test_cache.json")
    cache = DataCache(測試快取檔案, 預設過期秒數=10)  # 測試用10秒過期
    
    # 測試1：設定快取
    print("\n【測試1】設定快取")
    cache.設定("0050.TW", {"price": 185.5, "name": "元大台灣50"}, 過期秒數=10)
    cache.設定("1101.TW", {"price": 22.8, "name": "台泥"}, 過期秒數=10)
    cache.設定("2409.TW", {"price": 14.4, "name": "友達"}, 過期秒數=10)
    print(f"  ✅ 已設定 3 個快取項目")
    print(f"  📁 快取檔案：{cache.快取檔案路徑}")
    
    # 測試2：讀取快取
    print("\n【測試2】讀取快取")
    data, expired = cache.取得("0050.TW")
    print(f"  0050.TW: {data} (已過期={expired})")
    
    data, expired = cache.取得("nonexistent")
    print(f"  nonexistent: {data} (已過期={expired})")
    
    # 測試3：查詢狀態
    print("\n【測試3】查詢狀態")
    for key in cache.列出所有金鑰():
        狀態 = cache.查詢狀態(key)
        print(f"  {key}: {'🔴' if 狀態['已過期'] else '🟢'} "
              f"快取時間={狀態['快取時間']}, 剩餘={狀態['剩餘秒數']}秒")
    
    # 測試4：需要更新檢查
    print("\n【測試4】需要更新檢查")
    print(f"  0050.TW 需要更新？ {cache.需要更新('0050.TW')}")
    print(f"  nonexistent 需要更新？ {cache.需要更新('nonexistent')}")
    
    # 測試5：刪除快取
    print("\n【測試5】刪除快取")
    cache.刪除("2409.TW")
    print(f"  ✅ 已刪除 2409.TW")
    print(f"  剩餘金鑰：{cache.列出所有金鑰()}")
    
    # 測試6：批量操作
    print("\n【測試6】批量操作")
    results = cache.批量取得(["0050.TW", "1101.TW"])
    for key, (data, expired) in results.items():
        print(f"  {key}: 已過期={expired}, data={data}")
    
    print("\n" + "=" * 60)
    print("✅ 快取+更新機制測試完成")
    print("=" * 60)
    
    # 清理測試檔案
    if os.path.exists(測試快取檔案):
        os.remove(測試快取檔案)
        print(f"\n🗑️ 已清理測試快取檔案")
