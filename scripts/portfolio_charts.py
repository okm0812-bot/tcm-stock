# -*- coding: utf-8 -*-
"""
投資組合視覺化圖表
生成: K線圖、損益曲線、資產配置圖
"""
import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import json
import os
import numpy as np

# 設定中文字體
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'Arial Unicode MS', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 快取和歷史檔案
CACHE_FILE = "stock_cache.json"
HISTORY_FILE = "portfolio_history.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}

def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def get_stock_data(code, cache):
    now = datetime.now().timestamp()
    if code in cache:
        cached_time = cache[code].get('timestamp', 0)
        if now - cached_time < 300:
            return cache[code]['data']
    return None

def plot_portfolio_pie():
    """資產配置圓餅圖"""
    cache = load_cache()
    
    holdings = [
        {"code": "1101.TW", "name": "台泥", "shares": 19000},
        {"code": "2352.TW", "name": "佳世達", "shares": 6000},
        {"code": "2409.TW", "name": "友達", "shares": 9000},
        {"code": "6919.TW", "name": "康霈", "shares": 300},
    ]
    
    labels = []
    sizes = []
    values = []
    
    for h in holdings:
        data = get_stock_data(h['code'], cache)
        if data:
            value = data['price'] * h['shares']
            labels.append(h['name'])
            sizes.append(value)
            values.append(value)
    
    if not sizes:
        print("無法生成圖表：缺少數據")
        return
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99']
    explode = (0.05, 0.05, 0.05, 0.05) if len(sizes) == 4 else tuple([0.05] * len(sizes))
    
    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors[:len(sizes)],
                                       autopct=lambda pct: f'{pct:.1f}%\n(${int(pct/100*sum(sizes)):,})',
                                       shadow=True, startangle=90)
    
    ax.set_title(f'投資組合資產配置\n總市值: ${sum(sizes):,.0f}', fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('portfolio_allocation.png', dpi=150, bbox_inches='tight')
    print(f"資產配置圖已儲存: portfolio_allocation.png")
    plt.close()

def plot_pnl_chart():
    """損益柱狀圖"""
    cache = load_cache()
    
    holdings = [
        {"code": "1101.TW", "name": "台泥", "shares": 19000, "cost": 34.56},
        {"code": "2352.TW", "name": "佳世達", "shares": 6000, "cost": 53.78},
        {"code": "2409.TW", "name": "友達", "shares": 9000, "cost": 16.20},
        {"code": "6919.TW", "name": "康霈", "shares": 300, "cost": 102.36},
    ]
    
    names = []
    pnls = []
    pnl_pcts = []
    
    for h in holdings:
        data = get_stock_data(h['code'], cache)
        if data:
            price = data['price']
            cost = h['cost']
            pnl = (price - cost) * h['shares']
            pnl_pct = (price - cost) / cost * 100
            
            names.append(h['name'])
            pnls.append(pnl)
            pnl_pcts.append(pnl_pct)
    
    if not names:
        print("無法生成圖表：缺少數據")
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # 損益金額
    colors = ['green' if x > 0 else 'red' for x in pnls]
    ax1.bar(names, pnls, color=colors, alpha=0.7, edgecolor='black')
    ax1.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax1.set_title('各股損益金額', fontsize=14, fontweight='bold')
    ax1.set_ylabel('損益 (元)')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/10000:.0f}萬'))
    
    for i, v in enumerate(pnls):
        ax1.text(i, v + (max(pnls)-min(pnls))*0.02, f'{v/10000:.1f}萬', ha='center', fontsize=10)
    
    # 損益百分比
    colors2 = ['green' if x > 0 else 'red' for x in pnl_pcts]
    ax2.bar(names, pnl_pcts, color=colors2, alpha=0.7, edgecolor='black')
    ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax2.set_title('各股損益百分比', fontsize=14, fontweight='bold')
    ax2.set_ylabel('報酬率 (%)')
    
    for i, v in enumerate(pnl_pcts):
        ax2.text(i, v + (max(pnl_pcts)-min(pnl_pcts))*0.02, f'{v:.1f}%', ha='center', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('portfolio_pnl.png', dpi=150, bbox_inches='tight')
    print(f"損益圖已儲存: portfolio_pnl.png")
    plt.close()

def plot_history_trend():
    """歷史資產變化曲線"""
    history = load_history()
    
    if len(history) < 2:
        print("歷史數據不足，無法生成趨勢圖（至少需要 2 天數據）")
        return
    
    dates = []
    values = []
    
    for record in history:
        dates.append(datetime.strptime(record['date'], '%Y-%m-%d'))
        values.append(record['total_value'])
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    ax.plot(dates, values, marker='o', linewidth=2, markersize=6, color='blue', label='總市值')
    ax.fill_between(dates, values, alpha=0.3, color='blue')
    
    # 標註最新值
    ax.annotate(f'${values[-1]:,.0f}', 
                xy=(dates[-1], values[-1]),
                xytext=(10, 10), textcoords='offset points',
                fontsize=12, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
    
    ax.set_title('資產價值變化趨勢', fontsize=16, fontweight='bold')
    ax.set_xlabel('日期')
    ax.set_ylabel('總市值 (元)')
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/10000:.0f}萬'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('portfolio_trend.png', dpi=150, bbox_inches='tight')
    print(f"趨勢圖已儲存: portfolio_trend.png")
    plt.close()

def generate_all_charts():
    """生成所有圖表"""
    print("="*70)
    print("投資組合視覺化圖表生成")
    print("="*70)
    
    print("\n正在生成圖表...")
    print("-"*70)
    
    # 1. 資產配置圓餅圖
    try:
        plot_portfolio_pie()
    except Exception as e:
        print(f"資產配置圖生成失敗: {e}")
    
    # 2. 損益柱狀圖
    try:
        plot_pnl_chart()
    except Exception as e:
        print(f"損益圖生成失敗: {e}")
    
    # 3. 歷史趨勢圖
    try:
        plot_history_trend()
    except Exception as e:
        print(f"趨勢圖生成失敗: {e}")
    
    print("\n" + "="*70)
    print("圖表生成完成！")
    print("="*70)
    print("""
生成的檔案:
  - portfolio_allocation.png  (資產配置圓餅圖)
  - portfolio_pnl.png         (損益柱狀圖)
  - portfolio_trend.png       (歷史趨勢圖)

查看方式:
  - 直接點擊圖片檔案
  - 或在報告中查看
""")

if __name__ == "__main__":
    generate_all_charts()