# -*- coding: utf-8 -*-
"""
完整持股分析腳本 (portfolio_analysis.py)
整合所有功能：驗證、還原股價、爬蟲、圖表，輸出完整持股分析報告
作者：投資分析系統增強版
"""

import sys
import os

# 確保 UTF-8 輸出
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ==================== 依賴檢查 ====================
_required = []
try:
    import yfinance as yf
except ImportError:
    _required.append("yfinance")
try:
    import pandas as pd
except ImportError:
    _required.append("pandas")
try:
    import requests
except ImportError:
    _required.append("requests")
try:
    import matplotlib
except ImportError:
    _required.append("matplotlib")
try:
    import mplfinance
except ImportError:
    _required.append("mplfinance")
try:
    import numpy as np
except ImportError:
    _required.append("numpy")

if _required:
    print(f"⚠️ 缺少套件：{', '.join(_required)}，部分功能可能無法執行")
    print(f"   安裝指令：pip install {' '.join(_required)}")


# ==================== 嘗試匯入自訂模組 ====================
_script_dir = os.path.dirname(os.path.abspath(__file__))

def _import_module(name):
    """嘗試匯入本地模組"""
    try:
        import importlib.util
        path = os.path.join(_script_dir, f"{name}.py")
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location(name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
    except Exception as e:
        print(f"⚠️ 無法匯入 {name}：{e}")
    return None

calc_verifier = _import_module("calc_verifier")
adjusted_price = _import_module("adjusted_price")
twstock_scraper = _import_module("twstock_scraper")
chart_generator = _import_module("chart_generator")
data_cache = _import_module("data_cache")


# ==================== 持股資料（從 MEMORY.md 讀取）====================

def 讀取持股資料() -> list:
    """
    讀取持股資料（優先從MEMORY.md，若失敗則使用預設）
    """
    default = [
        {
            "代號": "1101",
            "名稱": "台泥",
            "張數": 19,
            "成本": 34.56,
            "現價": 22.55,  # 2026-03-30 快取資料
            "備註": "水泥股，長持"
        },
        {
            "代號": "2409",
            "名稱": "友達",
            "張數": 9,
            "成本": 16.2,
            "現價": 14.3,
            "備註": "面板股，波動大"
        },
        {
            "代號": "2352",
            "名稱": "佳世達",
            "張數": 11,
            "成本": 53.78,
            "現價": 23.1,
            "備註": "電子代工，持有中"
        },
    ]
    
    # 嘗試讀取快取
    if data_cache:
        try:
            cache = data_cache.建立快取(預設過期秒數=600)
            cached_data, expired = cache.取得("持股資料")
            if cached_data and not expired:
                print(f"📦 從快取載入持股資料")
                return cached_data
        except:
            pass
    
    return default


def 從網路更新現價(持股列表: list) -> list:
    """
    從Yahoo Finance更新持股現價
    """
    if not yf:
        print("⚠️ yfinance 未安裝，跳過現價更新")
        return 持股列表
    
    updated = []
    for 持股 in 持股列表:
        try:
            ticker = yf.Ticker(f"{持股['代號']}.TW")
            info = ticker.info
            現價 = info.get("currentPrice") or info.get("regularMarketPrice")
            if 現價:
                持股 = 持股.copy()
                持股["現價"] = round(現價, 2)
                持股["更新時間"] = pd.Timestamp.now().strftime("%Y-%m-%d")
        except Exception as e:
            pass
        updated.append(持股)
    
    return updated


# ==================== 持股分析核心 ====================

def 分析單一持股(持股: dict, 快取過期秒數: int = 300) -> dict:
    """
    分析單一持股
    
    參數：
        持股 (dict)：持股資料
        快取過期秒數 (int)：快取過期秒數
    
    回傳：
        dict：完整分析結果
    """
    代號 = 持股["代號"]
    名稱 = 持股["名稱"]
    Yahoo代號 = f"{代號}.TW"
    
    結果 = {
        "代號": 代號,
        "名稱": 名稱,
        "持股": 持股,
        "分析時間": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M"),
    }
    
    # ==================== 步驟1：數字驗證 ====================
    print(f"\n{'='*60}")
    print(f"📋 {名稱}({代號}) 分析")
    print(f"{'='*60}")
    
    if calc_verifier:
        # 驗證投資金額
        投資驗證 = calc_verifier.verify_investment(
            本金=持股["張數"] * 1000 * 持股["成本"],
            張數=持股["張數"],
            價格=持股["成本"]
        )
        結果["投資驗證"] = 投資驗證
        print(f"  【驗證】投資金額：{投資驗證['訊息']}")
        
        # 驗證虧損
        股數 = 持股["張數"] * 1000
        虧損驗證 = calc_verifier.verify_loss(
            成本=持股["成本"],
            現價=持股["現價"],
            股數=股數
        )
        結果["虧損驗證"] = 虧損驗證
        print(f"  【驗證】虧損：{虧損驗證['虧損金額']:,.0f}元 ({虧損驗證['虧損比例']})")
    else:
        結果["驗證"] = {"錯誤": "calc_verifier 模組不可用"}
    
    # ==================== 步驟2：還原股價與真實報酬 ====================
    print(f"  【還原股價】抓取中...", end=" ", flush=True)
    
    if adjusted_price and yf:
        try:
            import importlib
            # 重新匯入以確保模組可用
            adj_mod = _import_module("adjusted_price")
            
            還原結果 = adjusted_price.fetch_adjusted_prices(Yahoo代號, 天數=3650)
            
            if 還原結果.get("錯誤"):
                結果["還原股價"] = {"錯誤": 還原結果["錯誤"]}
                print(f"❌")
            else:
                結果["還原股價"] = 還原結果
                print(f"✅")
                print(f"     期間：{還原結果['起始日期']} ~ {還原結果['結束日期']}")
                print(f"     還原收盤：{還原結果['起始還原收盤']} → {還原結果['最新還原收盤']}")
                print(f"     期間報酬：{還原結果['期間累計報酬']}%")
                print(f"     年化報酬：{還原結果['年化報酬']}%")
        except Exception as e:
            結果["還原股價"] = {"錯誤": f"還原股價抓取失敗：{e}"}
            print(f"❌ {e}")
    else:
        結果["還原股價"] = {"錯誤": "此功能因缺少 yfinance 或 adjusted_price 無法執行"}
        print(f"❌")
    
    # ==================== 步驟3：基本面爬蟲 ====================
    print(f"  【基本面】爬取中...", end=" ", flush=True)
    
    if twstock_scraper:
        try:
            基本面 = twstock_scraper.full_scrape(代號, include_institutional=True)
            結果["基本面"] = 基本面
            print(f"✅ (品質：{基本面.get('資料品質', '?')}/3)")
            
            # 顯示關鍵指標
            y = 基本面.get("Yahoo", {})
            if y and not y.get("錯誤"):
                print(f"     PE={y.get('PE', '?')}, ROE={y.get('ROE', '?')}, "
                      f"殖利率={y.get('股息殖利率', '?')}")
        except Exception as e:
            結果["基本面"] = {"錯誤": f"基本面爬取失敗：{e}"}
            print(f"❌")
    else:
        結果["基本面"] = {"錯誤": "此功能因缺少 twstock_scraper 無法執行"}
        print(f"❌")
    
    # ==================== 步驟4：快取更新 ====================
    if data_cache:
        try:
            cache = data_cache.DataCache(預設過期秒數=快取過期秒數)
            cache.設定(f"持股_分析_{代號}", 結果)
            print(f"  【快取】已儲存分析結果")
        except:
            pass
    
    return 結果


# ==================== 生成文字報告 ====================

def 生成文字報告(分析結果列表: list, 持股列表: list) -> str:
    """
    生成完整的持股分析文字報告
    """
    lines = []
    lines.append("=" * 70)
    lines.append("📊 持股分析報告")
    lines.append(f"生成時間：{pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)
    
    # 總體摘要
    lines.append("\n【一、總體摘要】")
    
    總市值 = 0
    總成本 = 0
    總虧損 = 0
    
    for 持股 in 持股列表:
        成本 = 持股["張數"] * 1000 * 持股["成本"]
        市值 = 持股["張數"] * 1000 * 持股["現價"]
        虧損 = 市值 - 成本
        
        總市值 += 市值
        總成本 += 成本
        總虧損 += 虧損
        
        虧損比例 = 虧損 / 成本 * 100 if 成本 > 0 else 0
        
        lines.append(f"  {持股['代號']} {持股['名稱']}：")
        lines.append(f"    持股：{持股['張數']}張 / 成本均價：{持股['成本']}元")
        lines.append(f"    市值：${市值:,.0f} | 成本：${成本:,.0f} | "
                     f"{'虧損' if 虧損 < 0 else '獲利'}：${abs(虧損):,.0f} ({虧損比例:+.1f}%)")
    
    總虧損比例 = 總虧損 / 總成本 * 100 if 總成本 > 0 else 0
    lines.append(f"\n  總市值：${總市值:,.0f}")
    lines.append(f"  總成本：${總成本:,.0f}")
    lines.append(f"  總{'虧損' if 總虧損 < 0 else '獲利'}：${abs(總虧損):,.0f} ({總虧損比例:+.1f}%)")
    
    # 各股分析
    lines.append("\n【二、個別分析】")
    
    for 結果 in 分析結果列表:
        代號 = 結果["代號"]
        名稱 = 結果["名稱"]
        
        lines.append(f"\n── {代號} {名稱} ──")
        
        # 驗證結果
        if "投資驗證" in 結果:
            v = 結果["投資驗證"]
            lines.append(f"  驗證：{v['訊息']} | 預期=${v.get('預期金額', '?'):,}")
        
        # 虧損驗證
        if "虧損驗證" in 結果:
            l = 結果["虧損驗證"]
            lines.append(f"  虧損：${l.get('虧損金額', 0):,.0f} ({l.get('虧損比例', '?')})")
        
        # 還原股價
        adj = 結果.get("還原股價", {})
        if adj.get("錯誤"):
            lines.append(f"  還原股價：❌ {adj['錯誤']}")
        elif adj:
            lines.append(f"  還原股價：✅")
            lines.append(f"    期間：{adj.get('起始日期', '?')} ~ {adj.get('結束日期', '?')}")
            lines.append(f"    還原收盤：{adj.get('起始還原收盤', '?')} → {adj.get('最新還原收盤', '?')}")
            lines.append(f"    期間報酬：{adj.get('期間累計報酬', '?')}%")
            lines.append(f"    年化報酬：{adj.get('年化報酬', '?')}%")
            if adj.get("CSV路徑"):
                lines.append(f"    CSV：{adj['CSV路徑']}")
        
        # 基本面
        fin = 結果.get("基本面", {})
        y = fin.get("Yahoo", {})
        if y and not y.get("錯誤"):
            lines.append(f"  Yahoo Finance 基本面：")
            lines.append(f"    現價：{y.get('現價', '?')} | PE：{y.get('PE', '?')} | EPS：{y.get('EPS', '?')}")
            lines.append(f"    ROE：{y.get('ROE', '?')} | ROA：{y.get('ROA', '?')}")
            lines.append(f"    殖利率：{y.get('股息殖利率', '?')} | Beta：{y.get('beta', '?')}")
            lines.append(f"    52週區間：{y.get('52週低', '?')} ~ {y.get('52週高', '?')}")
            lines.append(f"    季線：{y.get('季線(MA50)', '?')} | 年線：{y.get('年線(MA200)', '?')}")
            if y.get("位於季線"):
                lines.append(f"    位置：季線{y.get('位於季線', '')} / 年線{y.get('位於年線', '')}")
        elif fin.get("錯誤"):
            lines.append(f"  基本面：❌ {fin.get('錯誤')}")
        else:
            lines.append(f"  基本面：❌ 資料不足")
    
    lines.append("\n" + "=" * 70)
    lines.append("✅ 報告結束")
    lines.append("=" * 70)
    
    return "\n".join(lines)


# ==================== 主程式 ====================

if __name__ == "__main__":
    print("=" * 70)
    print("📊 完整持股分析腳本")
    print("=" * 70)
    
    # 讀取持股資料
    print("\n📂 讀取持股資料...")
    持股列表 = 讀取持股資料()
    
    for 持股 in 持股列表:
        print(f"  • {持股['代號']} {持股['名稱']}：{持股['張數']}張 @ ${持股['成本']} → ${持股['現價']}")
    
    # 分析每一持股
    分析結果列表 = []
    
    for 持股 in 持股列表:
        try:
            結果 = 分析單一持股(持股, 快取過期秒數=300)
            分析結果列表.append(結果)
        except Exception as e:
            print(f"\n  ❌ 分析 {持股['代號']} {持股['名稱']} 時發生錯誤：{e}")
            分析結果列表.append({
                "代號": 持股["代號"],
                "名稱": 持股["名稱"],
                "錯誤": str(e)
            })
    
    # 生成文字報告
    print("\n" + "=" * 70)
    print("📝 生成文字報告...")
    print("=" * 70)
    
    報告 = 生成文字報告(分析結果列表, 持股列表)
    print(報告)
    
    # 儲存報告
    報告路徑 = os.path.join(os.path.dirname(_script_dir), "持股分析報告.md")
    with open(報告路徑, "w", encoding="utf-8") as f:
        f.write(報告)
    print(f"\n✅ 報告已儲存：{報告路徑}")
    
    # 生成圖表（若可用）
    print("\n" + "=" * 70)
    print("📈 生成圖表...")
    print("=" * 70)
    
    if chart_generator:
        # 生成圓餅圖
        print("\n  【圓餅圖】")
        配置_dict = {}
        for 持股 in 持股列表:
            市值 = 持股["張數"] * 1000 * 持股["現價"]
            配置_dict[f"{持股['代號']} {持股['名稱']}"] = 市值
        
        pie_result = chart_generator.plot_portfolio_allocation(
            配置_dict,
            標題="持股組合配置",
            output_dir=os.path.dirname(_script_dir)
        )
        if pie_result["成功"]:
            print(f"  ✅ {pie_result['圖表路徑']}")
        else:
            print(f"  ❌ {pie_result.get('錯誤', '未知錯誤')}")
        
        # 為每支股票生成K線圖
        for 持股 in 持股列表:
            print(f"\n  【K線圖】{持股['代號']} {持股['名稱']}")
            k_result = chart_generator.plot_price_history(
                f"{持股['代號']}.TW",
                天數=365,
                output_dir=os.path.dirname(_script_dir)
            )
            if k_result["成功"]:
                print(f"  ✅ {k_result['圖表路徑']}")
            else:
                print(f"  ❌ {k_result.get('錯誤', '未知錯誤')}")
    else:
        print("  ❌ chart_generator 模組不可用，跳過圖表生成")
    
    print("\n" + "=" * 70)
    print("✅ 持股分析完成")
    print("=" * 70)
