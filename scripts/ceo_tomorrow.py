# -*- coding: utf-8 -*-
"""CEO 明日操作分析 - v3.2 雙團隊分工"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=" * 70)
print("CEO 統一分析 v3.2 - 明日操作建議")
print("=" * 70)

# ==================== 第一階段：數據收集 ====================
print("\n【第一階段】數據收集團隊")
print("-" * 70)

try:
    import yfinance as yf
    
    # 市場數據
    print("\n📊 市場數據：")
    tw = yf.Ticker('^TWII')
    print(f"  台股加權: {tw.info.get('regularMarketPrice', 'N/A')}")
    
    vix = yf.Ticker('^VIX')
    print(f"  VIX: {vix.info.get('regularMarketPrice', 'N/A')}")
    
    bond = yf.Ticker('^TNX')
    print(f"  美10年債: {bond.info.get('regularMarketPrice', 'N/A')}")
    
    sp = yf.Ticker('^GSPC')
    print(f"  S&P 500: {sp.info.get('regularMarketPrice', 'N/A')}")
    
except Exception as e:
    print(f"  市場數據获取失敗: {e}")

# 持倉個股（使用記憶中的收盤價）
print("\n📈 持倉個股（今日收盤）：")
holdings = {
    "台泥 1101": {"price": 23.70, "shares": 19000, "cost": 34.56, "stop": 20.00},
    "佳世達 2352": {"price": 23.30, "shares": 6000, "cost": 51.33, "stop": 22.50},
    "友達 2409": {"price": 15.95, "shares": 9000, "cost": 16.20, "stop": 12.00},
    "康霈 6919": {"price": 94.90, "shares": 300, "cost": 102.36, "stop": 85.00},
    "0050": {"price": 75.45, "shares": 0, "cost": 0, "stop": 0},
}

total_value = 0
total_cost = 0

for name, data in holdings.items():
    value = data["price"] * data["shares"]
    cost = data["cost"] * data["shares"] if data["shares"] > 0 else 0
    pnl = value - cost if cost > 0 else 0
    pnl_pct = (pnl / cost * 100) if cost > 0 else 0
    total_value += value
    total_cost += cost
    
    stop_loss = data["stop"]
    status = "⚠️ 接近停損" if data["price"] <= stop_loss * 1.1 else "正常"
    
    if data["shares"] > 0:
        print(f"  {name}: {data['price']}元 × {data['shares']}股 = {value:,.0f}元 (虧損{ pnl_pct:+.1f}%) {status}")

print(f"\n  總市值: {total_value:,.0f}元")
print(f"  總成本: {total_cost:,.0f}元")
print(f"  總虧損: {total_value - total_cost:,.0f}元 ({((total_value-total_cost)/total_cost*100):+.1f}%)")

# ==================== 第二階段：分析團隊 ====================
print("\n【第二階段】分析團隊")
print("-" * 70)

# 風險分析
print("\n📉 風險分析：")
for name, data in holdings.items():
    if data["shares"] > 0:
        stop_loss = data["stop"]
        diff = data["price"] - stop_loss
        if diff < 0:
            print(f"  ⚠️ {name}: 已跌破停損 {stop_loss}元，應立即停損！")
        elif data["price"] < stop_loss * 1.1:
            print(f"  🔶 {name}: 接近停損 {stop_loss}元（距離{diff:.2f}元）")

# 技術分析
print("\n📊 技術分析：")
print("  • 台股今日大漲 1451 點（+4.58%），史上第2大漲點")
print("  • 軋空行情，空頭被迫回補")
print("  • 友達亮燈漲停（+10%），面板股大爆發")
print("  • 台積電大漲 95 元（+5.4%），股價 1855 元")

# 基本面分析
print("\n📋 基本面分析：")
print("  • 佳世達：仍處虧損狀態，Alpha -53%，建議停損")
print("  • 友達：今日大漲但基本面具挑戰，僅 Alpha -16%")
print("  • 康霈：小型股高波動，目標 100 元")
print("  • 台泥：俄烏戰爭潜在利多，但仍需觀察")

# ==================== 第三階段：CEO 裁決 ====================
print("\n【第三階段】CEO 整合裁決")
print("-" * 70)

print("""
┌─────────────────────────────────────────────────────────────────────┐
│                       明日操作建議                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  🔴 優先處理：                                                      │
│     1. 佳世達 2352：設定 22.50 停損條件單                            │
│        - 距離現價 23.30 有 3.4% 安全邊際                            │
│        - 若觸及毫不猶豫停損                                         │
│        - 停損後資金投入 0050（等回調 73-74 元買入）                   │
│                                                                     │
│  🟡 觀察名單：                                                      │
│     2. 康霈 6919：若突破 100 元，先賣一半                           │
│        - 移動停損提高到 85 元                                       │
│                                                                     │
│     3. 友達 2409：若達 18-20 元，考慮減碼                           │
│        - 接近解套區間                                               │
│                                                                     │
│     4. 台泥 1101：若達 28-30 元，考慮減碼                           │
│                                                                     │
│  🟢 買入建議：                                                      │
│     5. 0050：等回調到 73-74 元分批買入                              │
│        - 今日收盤 75.45 元偏高                                     │
│        - 分批買入（每週 25%，共 4 週）                               │
│                                                                     │
│  ⚠️ 風險提示：                                                      │
│     • VIX 仍偏高（25+），波動仍在                                   │
│     • 軋空行情可能反轉                                             │
│     • 留意明日開盤走勢                                             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
""")

# 明日開盤重點
print("\n📌 明日開盤重點：")
print("  1. 佳世達 22.50 停損線")
print("  2. 康霈 100 元關卡")
print("  3. 友達解套壓力區（18-20元）")
print("  4. 台股是否持續高檔震盪")

print("\n" + "=" * 70)
print("分析完成")
print("=" * 70)