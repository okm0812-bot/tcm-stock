# scenario_dcf.py
# 情境 DCF 估值系統 - 三種情景分析
# 樂觀 / 中性 / 悲觀 三種情境下的內在價值

import yfinance as yf
import numpy as np
import sys
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def simple_dcf_scenario(fcf, growth_rate, discount_rate=0.10, terminal_growth=0.03, years=5, shares_outstanding=1e9):
    """
    簡化版 DCF 估值 - 三種情境
    
    返回: (樂觀價值, 中性價值, 悲觀價值)
    """
    results = {}
    
    for scenario_name, scenario_growth in [("樂觀", growth_rate * 1.5), ("中性", growth_rate), ("悲觀", growth_rate * 0.5)]:
        # 預測未來5年 FCF
        fcf_forecast = [fcf * (1 + scenario_growth) ** i for i in range(1, years + 1)]
        
        # 折現
        pv_fcf = sum([fcf_forecast[i] / (1 + discount_rate) ** (i + 1) for i in range(years)])
        
        # 終值
        terminal_fcf = fcf_forecast[-1] * (1 + terminal_growth)
        terminal_value = terminal_fcf / (discount_rate - terminal_growth)
        pv_terminal = terminal_value / (1 + discount_rate) ** years
        
        # 企業價值
        enterprise_value = pv_fcf + pv_terminal
        per_share = enterprise_value / shares_outstanding
        
        results[scenario_name] = {
            'fcf_forecast': fcf_forecast,
            'pv_fcf': pv_fcf,
            'terminal_value': terminal_value,
            'enterprise_value': enterprise_value,
            'per_share': per_share
        }
    
    return results

def analyze_with_dcf(ticker, name, current_price=None, buy_price=None, shares=0):
    """用 DCF 分析股票"""
    print()
    print("=" * 60)
    print(f"  [DCF估值] {name} ({ticker})")
    print("=" * 60)
    
    try:
        # 抓取數據
        data = yf.Ticker(ticker)
        info = data.info
        
        current_price = current_price or info.get('regularMarketPrice', 0)
        shares_out = info.get('sharesOutstanding', 1e9)
        fcf = info.get('freeCashflow', 0) or 0
        
        # 取得 EPS 成長率估算
        eps = info.get('trailingEps', 0) or 0
        pe = info.get('trailingPE', 0) or 15
        
        print()
        print(f"  【基本數據】")
        print(f"    目前股價: {current_price:.2f} 元")
        print(f"    EPS: {eps:.2f} 元" if eps else "    EPS: N/A")
        print(f"    PE: {pe:.2f}x" if pe else "    PE: N/A")
        print(f"    流通股數: {shares_out/1e9:.2f} 億股")
        print(f"    自由現金流: {fcf/1e8:.2f} 億元" if fcf else "    自由現金流: N/A")
        print()
        
        if not fcf or fcf <= 0:
            print(f"  【警告】自由現金流為負或N/A，無法使用DCF")
            print(f"    建議改用其他估值方法")
            return None
        
        # 根據產業估算成長率
        industry = info.get('industry', '')
        if 'AI' in industry or '電子' in industry or '科技' in industry:
            base_growth = 0.15
        elif '水泥' in industry or '傳產' in industry:
            base_growth = 0.05
        elif '面板' in industry or '電子元件' in industry:
            base_growth = 0.08
        elif '生技' in industry or '製藥' in industry:
            base_growth = 0.10
        else:
            base_growth = 0.10
        
        print(f"  【成長率設定】")
        print(f"    產業: {industry}")
        print(f"    基礎成長率: {base_growth*100:.0f}%/年")
        print()
        
        # 三種情境
        scenarios = {
            "樂觀": base_growth * 1.5,
            "中性": base_growth,
            "悲觀": base_growth * 0.5
        }
        
        print(f"  【DCF 三情境估值】")
        print(f"  {'情境':<8} {'FCF成長率':<12} {'企業價值':<15} {'每股內在價值':<15} {'安全邊際':<10}")
        print(f"  {'-'*60}")
        
        dcf_results = {}
        for scenario_name, growth in scenarios.items():
            result = simple_dcf_scenario(
                fcf=fcf,
                growth_rate=growth,
                discount_rate=0.10,
                terminal_growth=0.03,
                years=5,
                shares_outstanding=shares_out
            )[scenario_name]
            
            intrinsic = result['per_share']
            safety_margin = (intrinsic - current_price) / intrinsic * 100
            
            dcf_results[scenario_name] = {
                'intrinsic': intrinsic,
                'safety_margin': safety_margin,
                'growth': growth
            }
            
            margin_emoji = "🟢" if safety_margin > 20 else "🟡" if safety_margin > 0 else "🔴"
            print(f"  {scenario_name:<8} {growth*100:>8.1f}%    {result['enterprise_value']/1e8:>12.1f}億  {intrinsic:>12.2f}元  {margin_emoji}{safety_margin:>+7.1f}%")
        
        # 總結
        print()
        print(f"  【估值總結】")
        
        # 取中性情境作為主要參考
        neutral = dcf_results['中性']['intrinsic']
        optimistic = dcf_results['樂觀']['intrinsic']
        pessimistic = dcf_results['悲觀']['intrinsic']
        
        print(f"    合理價值區間: {pessimistic:.0f} ~ {optimistic:.0f} 元")
        print(f"    中性價值: {neutral:.0f} 元")
        print(f"    目前股價: {current_price:.0f} 元")
        
        avg_intrinsic = (optimistic + neutral + pessimistic) / 3
        avg_safety = (avg_intrinsic - current_price) / avg_intrinsic * 100
        
        print()
        print(f"    三年平均內在價值: {avg_intrinsic:.0f} 元")
        
        if avg_safety > 30:
            print(f"    安全邊際: 🟢 {avg_safety:.1f}% (大幅低估，建議買入)")
        elif avg_safety > 0:
            print(f"    安全邊際: 🟡 {avg_safety:.1f}% (輕微低估，觀望)")
        else:
            print(f"    安全邊際: 🔴 {avg_safety:.1f}% (高估，建議觀望)")
        
        # 持有分析
        if buy_price and shares > 0:
            print()
            print(f"  【持有分析】")
            cost = buy_price * shares
            current_value = current_price * shares
            unrealized = current_value - cost
            return_pct = unrealized / cost * 100
            
            print(f"    股數: {shares:,} 股")
            print(f"    成本均價: {buy_price:.2f} 元")
            print(f"    總成本: {cost:,.0f} 元")
            print(f"    目前市值: {current_value:,.0f} 元")
            print(f"    未實現損益: {unrealized:+,.0f} 元 ({return_pct:+.2f}%)")
            
            # 是否低於內在價值
            if current_price < avg_intrinsic * 0.8:
                print(f"    評估: 🟢 低於內在價值 20% 以上，持有價值浮現")
            elif current_price < avg_intrinsic:
                print(f"    評估: 🟡 低於內在價值，但幅度有限")
            else:
                print(f"    評估: 🔴 高於內在價值，建議觀望")
        
        return dcf_results
        
    except Exception as e:
        print(f"  錯誤: {e}")
        return None

# ============================================================
# 主程式
# ============================================================
print("=" * 60)
print("  [系統] 情境 DCF 估值分析")
print("=" * 60)
print(f"  分析時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 分析鴻海（你有興趣的）
portfolio = [
    {"name": "鴻海", "ticker": "2317.TW", "buy_price": 200.5, "shares": 0},
    {"name": "台泥", "ticker": "1101.TW", "buy_price": 34.56, "shares": 19000},
    {"name": "佳世達", "ticker": "2352.TW", "buy_price": 53.78, "shares": 11000},
    {"name": "友達", "ticker": "2409.TW", "buy_price": 16.20, "shares": 9000},
]

for stock in portfolio:
    analyze_with_dcf(stock["ticker"], stock["name"], 
                    buy_price=stock["buy_price"], shares=stock["shares"])

print()
print("=" * 60)
print("  [系統] 分析完成")
print("=" * 60)
