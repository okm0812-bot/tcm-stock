# -*- coding: utf-8 -*-
"""
圖表繪製腳本 (chart_generator.py)
用途：生成專業投資分析圖表（K線圖、配置圖、模擬圖、壓力測試圖）
作者：投資分析系統增強版
"""

import sys
import os

# 確保 UTF-8 輸出
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ==================== 安裝必要套件 ====================
_required_packages = {
    "matplotlib": "pip install matplotlib",
    "mplfinance": "pip install mplfinance",
    "yfinance": "pip install yfinance",
    "pandas": "pip install pandas",
}

_missing = []
for pkg, cmd in _required_packages.items():
    try:
        __import__(pkg.replace("-", "_"))
    except ImportError:
        _missing.append((pkg, cmd))

if _missing:
    print("❌ 缺少必要套件，請先安裝：")
    for pkg, cmd in _missing:
        print(f"   {cmd}")
    print("\n建議一次性安裝：")
    print("   pip install matplotlib mplfinance yfinance pandas pillow")
    # 不退出，繼續執行（可能已有部分套件）


# ==================== 設定中文字體 ====================
import matplotlib
matplotlib.use("Agg")  # 非互動式後端
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import warnings
warnings.filterwarnings("ignore")

# 嘗試設定中文字體
_FONT_SET = False
_CHINESE_FONTS = [
    "Microsoft JhengHei",
    "Microsoft YaHei",
    "PingFang TC",
    "SimHei",
    "Noto Sans CJK TC",
    "Noto Sans CJK SC",
]

for font in _CHINESE_FONTS:
    try:
        fm.fontManager.addfont(
            fm.findfont(fm.FontProperties(family=font), fail_on_missing=False) 
            if font in fm.fontManager.ttfweights else ""
        )
        plt.rcParams["font.sans-serif"] = [font] + plt.rcParams["font.sans-serif"]
        plt.rcParams["axes.unicode_minus"] = False
        _FONT_SET = True
        break
    except:
        continue

if not _FONT_SET:
    # 使用系統可用字體
    try:
        available = [f.name for f in fm.fontManager.ttflist]
        for f in ["Microsoft JhengHei", "Microsoft YaHei", "SimHei"]:
            if f in available:
                plt.rcParams["font.sans-serif"] = [f]
                plt.rcParams["axes.unicode_minus"] = False
                _FONT_SET = True
                break
    except:
        pass

if not _FONT_SET:
    print("⚠️  無法設定中文字體，圖表中文可能顯示為方塊")
    _CHINESE_FONTS = ["sans-serif"]


# ==================== 依賴 import ====================
try:
    import yfinance as yf
    _HAS_YF = True
except ImportError:
    _HAS_YF = False

try:
    import pandas as pd
    _HAS_PD = True
except ImportError:
    _HAS_PD = False

try:
    import mplfinance as mpf
    _HAS_MPF = True
except ImportError:
    _HAS_MPF = False

try:
    import numpy as np
    _HAS_NP = True
except ImportError:
    _HAS_NP = False

try:
    from datetime import datetime, timedelta
    _HAS_DT = True
except ImportError:
    _HAS_DT = False


# ==================== 工具函式 ====================

def _savefig(fig, 代號: str, 圖表名: str, output_dir: str = None) -> str:
    """儲存圖表為PNG，回傳路徑"""
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"{代號}_{圖表名}_{datetime.now().strftime('%Y%m%d')}.png"
    path = os.path.join(output_dir, filename)
    
    fig.savefig(
        path, 
        dpi=150, 
        bbox_inches="tight", 
        facecolor="white",
        edgecolor="none"
    )
    plt.close(fig)
    return path


# ==================== 圖表1：股價K線圖 ====================

def plot_price_history(代號: str, 天數: int = 365, output_dir: str = None) -> dict:
    """
    繪製股價K線圖（含MA均線）
    
    參數：
        代號 (str)：Yahoo Finance 代號，例："0050.TW"
        天數 (int)：歷史天數
        output_dir (str)：輸出目錄
    
    回傳：
        dict：{成功: bool, 圖表路徑: str, 錯誤: str}
    """
    if not _HAS_YF or not _HAS_PD or not _HAS_MPF:
        return {
            "成功": False,
            "圖表路徑": None,
            "錯誤": "❌ 此功能因缺少 yfinance/mplfinance 套件無法執行"
        }
    
    if not _HAS_DT:
        return {
            "成功": False,
            "圖表路徑": None,
            "錯誤": "❌ 此功能因缺少 datetime 模組無法執行"
        }
    
    try:
        # 抓取數據
        ticker = yf.Ticker(代號)
        end = datetime.now()
        start = end - timedelta(days=天數)
        
        df = ticker.history(start=start, end=end, auto_adjust=False)
        
        if df.empty:
            return {
                "成功": False,
                "圖表路徑": None,
                "錯誤": "❌ 資料不足：無法取得歷史數據"
            }
        
        # 計算均線
        df["MA20"] = df["Close"].rolling(20).mean()
        df["MA60"] = df["Close"].rolling(60).mean()
        df["MA120"] = df["Close"].rolling(120).mean()
        
        # K線圖配色
        mc = mpf.make_marketcolors(
            up="#FF4136", down="#2ECC40",
            edge="inherit",
            wick="inherit",
            volume="inherit",
        )
        style = mpf.make_mpf_style(
            marketcolors=mc,
            gridstyle="-",
            gridcolor="#DDDDDD",
            y_on_right=True,
        )
        
        # 添加均線
        add_plots = [
            mpf.make_addplot(df["MA20"], color="#FF6B00", width=1, linestyle="--"),
            mpf.make_addplot(df["MA60"], color="#0074D9", width=1.2),
            mpf.make_addplot(df["MA120"], color="#B10DC9", width=1.5),
        ]
        
        # 繪製圖表
        fig, axes = mpf.plot(
            df,
            type="candle",
            style=style,
            title=f"\n{代號} 股價K線圖（近{天數}天）",
            ylabel="價格",
            volume=True,
            addplot=add_plots,
            figsize=(14, 8),
            returnfig=True,
            tight_layout=True,
        )
        
        # 加入圖例
        axes[0].legend(["MA20", "MA60", "MA120"], loc="upper left", fontsize=8)
        
        path = _savefig(fig, 代號.replace(".", "_"), "K線圖", output_dir)
        
        return {
            "成功": True,
            "圖表路徑": path,
            "錯誤": None,
            "資料筆數": len(df),
            "起始日期": df.index[0].strftime("%Y-%m-%d"),
            "結束日期": df.index[-1].strftime("%Y-%m-%d"),
            "起始收盤": round(df["Close"].iloc[0], 2),
            "最新收盤": round(df["Close"].iloc[-1], 2),
        }
        
    except Exception as e:
        return {
            "成功": False,
            "圖表路徑": None,
            "錯誤": f"❌ 繪圖錯誤：{str(e)}"
        }


# ==================== 圖表2：圓餅圖（投資組合配置）====================

def plot_portfolio_allocation(配置_dict: dict, 標題: str = "投資組合配置", 
                                output_dir: str = None) -> dict:
    """
    繪製投資組合配置圓餅圖
    
    參數：
        配置_dict (dict)：{名稱: 金額} 或 {名稱: (金額, 顏色)}
        標題 (str)：圖表標題
        output_dir (str)：輸出目錄
    
    回傳：
        dict：{成功: bool, 圖表路徑: str, 錯誤: str}
    """
    try:
        if not 配置_dict:
            return {
                "成功": False,
                "圖表路徑": None,
                "錯誤": "❌ 配置字典為空"
            }
        
        # 解析數據
        名稱列表 = []
        金額列表 = []
        顏色列表 = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", "#98D8C8",
            "#DDA0DD", "#F7DC6F", "#BB8FCE", "#85C1E9", "#F8B500"
        ]
        
        for i, (key, val) in enumerate(配置_dict.items()):
            if isinstance(val, tuple):
                金額 = val[0]
                顏色 = val[1] if len(val) > 1 else 顏色列表[i % len(顏色列表)]
            else:
                金額 = val
                顏色 = 顏色列表[i % len(顏色列表)]
            
            名稱列表.append(str(key))
            金額列表.append(float(金額))
        
        總金額 = sum(金額列表)
        比例列表 = [v / 總金額 * 100 for v in 金額列表]
        
        # 繪圖
        fig, ax = plt.subplots(figsize=(10, 8))
        
        wedges, texts, autotexts = ax.pie(
            金額列表,
            labels=None,
            autopct=lambda pct: f"{pct:.1f}%\n${pct/100*總金額:,.0f}",
            colors=顏色列表[:len(名稱列表)],
            startangle=90,
            explode=[0.02] * len(名稱列表),
            shadow=False,
            textprops={"fontsize": 10}
        )
        
        # 設定百分比文字顏色
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontweight("bold")
        
        # 加入圖例
        ax.legend(
            wedges,
            [f"{n} (${v:,.0f})" for n, v in zip(名稱列表, 金額列表)],
            title="標的",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=9
        )
        
        ax.set_title(標題, fontsize=16, fontweight="bold", pad=20)
        
        # 加入總金額標註
        fig.text(0.5, 0.02, f"總金額：${總金額:,.0f}", 
                 ha="center", fontsize=12, style="italic")
        
        plt.tight_layout()
        path = _savefig(fig, "portfolio", "配置圖", output_dir)
        
        return {
            "成功": True,
            "圖表路徑": path,
            "錯誤": None,
            "總金額": 總金額,
            "配置項目": len(名稱列表),
        }
        
    except Exception as e:
        return {
            "成功": False,
            "圖表路徑": None,
            "錯誤": f"❌ 繪圖錯誤：{str(e)}"
        }


# ==================== 圖表3：Monte Carlo 模擬結果直方圖 ====================

def plot_monte_carlo(模擬結果: dict, 標題: str = "Monte Carlo 模擬結果",
                     output_dir: str = None) -> dict:
    """
    繪製Monte Carlo模擬結果直方圖
    
    參數：
        模擬結果 (dict)：{
            "最終價值列表": [list of float],  # 各路徑最終價值
            "機率列表": [list of float],       # 各路徑發生機率（可選）
        }
        標題 (str)：圖表標題
        output_dir (str)：輸出目錄
    
    回傳：
        dict：{成功: bool, 圖表路徑: str, 統計摘要: dict, 錯誤: str}
    """
    if not _HAS_NP:
        return {
            "成功": False,
            "圖表路徑": None,
            "錯誤": "❌ 此功能因缺少 numpy 套件無法執行"
        }
    
    try:
        最終價值 = 模擬結果.get("最終價值列表", [])
        
        if not 最終價值:
            return {
                "成功": False,
                "圖表路徑": None,
                "錯誤": "❌ 模擬結果為空"
            }
        
        values = np.array(最終價值)
        
        # 統計
        mean_val = np.mean(values)
        median_val = np.median(values)
        std_val = np.std(values)
        min_val = np.min(values)
        max_val = np.max(values)
        pct_5 = np.percentile(values, 5)
        pct_25 = np.percentile(values, 25)
        pct_75 = np.percentile(values, 75)
        pct_95 = np.percentile(values, 95)
        
        # 繪圖
        fig, ax = plt.subplots(figsize=(12, 6))
        
        n, bins, patches = ax.hist(
            values, bins=50, color="#4ECDC4", edgecolor="white",
            alpha=0.8, density=True
        )
        
        # 著色（根據價值高低）
        for i, patch in enumerate(patches):
            bin_center = (bins[i] + bins[i+1]) / 2
            if bin_center < pct_25:
                patch.set_facecolor("#FF6B6B")
            elif bin_center > pct_75:
                patch.set_facecolor("#2ECC40")
        
        # 標記線
        ax.axvline(mean_val, color="#FF6B00", linestyle="--", linewidth=2,
                   label=f"平均值 ${mean_val:,.0f}")
        ax.axvline(median_val, color="#0074D9", linestyle="-.", linewidth=1.5,
                   label=f"中位數 ${median_val:,.0f}")
        ax.axvline(pct_5, color="#B10DC9", linestyle=":", linewidth=1.5,
                   label=f"5%分位 ${pct_5:,.0f}")
        ax.axvline(pct_95, color="#B10DC9", linestyle=":", linewidth=1.5,
                   label=f"95%分位 ${pct_95:,.0f}")
        
        # 文字標註
        ax.text(0.02, 0.95,
                f"平均: ${mean_val:,.0f}\n"
                f"標準差: ${std_val:,.0f}\n"
                f"5%~95%: ${pct_5:,.0f} ~ ${pct_95:,.0f}\n"
                f"最小~最大: ${min_val:,.0f} ~ ${max_val:,.0f}",
                transform=ax.transAxes,
                fontsize=9,
                verticalalignment="top",
                bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8)
        )
        
        ax.set_xlabel("最終投資價值", fontsize=11)
        ax.set_ylabel("機率密度", fontsize=11)
        ax.set_title(標題, fontsize=14, fontweight="bold")
        ax.legend(loc="upper right", fontsize=9)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        path = _savefig(fig, "mc", "模擬結果", output_dir)
        
        return {
            "成功": True,
            "圖表路徑": path,
            "錯誤": None,
            "統計摘要": {
                "模擬路徑數": len(values),
                "平均值": round(mean_val, 0),
                "中位數": round(median_val, 0),
                "標準差": round(std_val, 0),
                "5%分位": round(pct_5, 0),
                "25%分位": round(pct_25, 0),
                "75%分位": round(pct_75, 0),
                "95%分位": round(pct_95, 0),
                "最小值": round(min_val, 0),
                "最大值": round(max_val, 0),
            }
        }
        
    except Exception as e:
        return {
            "成功": False,
            "圖表路徑": None,
            "錯誤": f"❌ 繪圖錯誤：{str(e)}"
        }


# ==================== 圖表4：壓力測試情境柱狀圖 ====================

def plot_stress_test(情境_dict: dict, 標題: str = "壓力測試情境分析",
                     output_dir: str = None) -> dict:
    """
    繪製極端情境柱狀圖
    
    參數：
        情境_dict (dict)：{
            "情境名稱": 虧損金額或報酬率,
            ...
        }
        標題 (str)：圖表標題
        output_dir (str)：輸出目錄
    
    回傳：
        dict：{成功: bool, 圖表路徑: str, 錯誤: str}
    """
    try:
        if not 情境_dict:
            return {
                "成功": False,
                "圖表路徑": None,
                "錯誤": "❌ 情境字典為空"
            }
        
        名稱列表 = list(情境_dict.keys())
        數值列表 = [float(v) for v in 情境_dict.values()]
        
        # 著色：正值=綠色，負值=紅色
        顏色列表 = []
        for v in 數值列表:
            if v > 0:
                顏色列表.append("#2ECC40")
            elif v < 0:
                顏色列表.append("#FF4136")
            else:
                顏色列表.append("#AAAAAA")
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.bar(名稱列表, 數值列表, color=顏色列表, edgecolor="white", linewidth=1)
        
        # 加入數值標籤
        for bar, val in zip(bars, 數值列表):
            height = bar.get_height()
            if height >= 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + max(數值列表)*0.02,
                        f"${val:,.0f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
            else:
                ax.text(bar.get_x() + bar.get_width()/2., height - max(abs(v) for v in 數值列表)*0.05,
                        f"${val:,.0f}", ha="center", va="top", fontsize=9, fontweight="bold",
                        color="#FF4136")
        
        # 基準線
        ax.axhline(0, color="black", linewidth=0.8)
        
        ax.set_xlabel("情境", fontsize=11)
        ax.set_ylabel("虧損金額（元）", fontsize=11)
        ax.set_title(標題, fontsize=14, fontweight="bold")
        ax.grid(True, axis="y", alpha=0.3)
        
        # 調整y軸範圍
        max_abs = max(abs(v) for v in 數值列表)
        ax.set_ylim(-max_abs * 1.2, max_abs * 1.2)
        
        plt.xticks(rotation=15, ha="right")
        plt.tight_layout()
        
        path = _savefig(fig, "stress", "壓力測試", output_dir)
        
        return {
            "成功": True,
            "圖表路徑": path,
            "錯誤": None,
            "情境數": len(名稱列表),
        }
        
    except Exception as e:
        return {
            "成功": False,
            "圖表路徑": None,
            "錯誤": f"❌ 繪圖錯誤：{str(e)}"
        }


# ==================== 主程式測試 ====================

if __name__ == "__main__":
    print("=" * 65)
    print("📊 圖表繪製腳本")
    print("=" * 65)
    
    # 測試1：0050 K線圖
    print("\n【測試1】0050.TW 股價K線圖")
    result = plot_price_history("0050.TW", 天數=365)
    if result["成功"]:
        print(f"  ✅ 已儲存：{result['圖表路徑']}")
        print(f"     資料筆數：{result.get('資料筆數', '?')}")
    else:
        print(f"  {result['錯誤']}")
    
    # 測試2：圓餅圖
    print("\n【測試2】投資組合配置圓餅圖")
    配置 = {
        "元大台灣50(0050)": 300000,
        "元大AAA至A公司債(00751B)": 50000,
        "國泰20年美債(00687B)": 100000,
        "中信高股息ETF(00717)": 80000,
        "兆豐藍籌30 ETF": 70000,
    }
    result = plot_portfolio_allocation(配置, 標題="投資組合配置")
    if result["成功"]:
        print(f"  ✅ 已儲存：{result['圖表路徑']}")
        print(f"     總金額：${result['總金額']:,.0f}")
    else:
        print(f"  {result['錯誤']}")
    
    # 測試3：Monte Carlo 直方圖（若numpy可用）
    print("\n【測試3】Monte Carlo 模擬直方圖")
    if _HAS_NP:
        np.random.seed(42)
        模擬值 = np.random.normal(loc=500000, scale=100000, size=1000)
        result = plot_monte_carlo({"最終價值列表": 模擬值.tolist()})
        if result["成功"]:
            print(f"  ✅ 已儲存：{result['圖表路徑']}")
            s = result["統計摘要"]
            print(f"     平均: ${s['平均值']:,.0f}, 標準差: ${s['標準差']:,.0f}")
        else:
            print(f"  {result['錯誤']}")
    else:
        print("  ❌ 此功能因缺少 numpy 套件無法執行")
    
    # 測試4：壓力測試柱狀圖
    print("\n【測試4】壓力測試情境柱狀圖")
    情境 = {
        "正常情境(0%)": 0,
        "下跌10%": -30000,
        "下跌20%": -60000,
        "下跌30%": -90000,
        "黑天鵝-50%": -150000,
        "大幅反彈+15%": 45000,
    }
    result = plot_stress_test(情境)
    if result["成功"]:
        print(f"  ✅ 已儲存：{result['圖表路徑']}")
    else:
        print(f"  {result['錯誤']}")
    
    print(f"\n{'='*65}")
    print("✅ 圖表繪製完成")
    print("=" * 65)
