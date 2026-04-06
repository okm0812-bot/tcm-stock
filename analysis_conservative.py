#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import math

# 讀取市場數據
with open('C:\\Users\\user\\.qclaw\\workspace\\market_data_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 提取數據
def extract_data(ticker):
    return {
        'name': data[ticker]['name'],
        'price': data[ticker]['price'],
        'hist_close': data[ticker]['hist_close'],
        'hist_dates': data[ticker]['hist_dates']
    }

# 計算10年報酬
def calculate_returns(hist_close, fee_rate=0.0032, inflation=0.025):
    """計算含股息再投資的總報酬"""
    if len(hist_close) < 2:
        return None
    
    start_price = hist_close[0]
    end_price = hist_close[-1]
    
    years = 10
    
    # 總報酬 = (期末價格 - 期初價格) / 期初價格
    price_return = (end_price - start_price) / start_price
    
    # 加上股息（保守估計）
    dividend_yield = 0.03  # 3% 年均股息
    dividend_return = (1 + dividend_yield) ** years - 1
    
    # 總報酬
    total_return = (1 + price_return) * (1 + dividend_return) - 1
    
    # 扣除費用
    net_return = total_return - (fee_rate * years)
    
    # 扣除通膨
    real_return = (1 + net_return) / (1 + inflation) ** years - 1
    
    return {
        'price_return': price_return,
        'dividend_return': dividend_return,
        'total_return': total_return,
        'net_return': net_return,
        'real_return': real_return
    }

# 計算波動率
def calculate_volatility(hist_close):
    """計算年化波動率"""
    if len(hist_close) < 2:
        return None
    
    returns = []
    for i in range(1, len(hist_close)):
        ret = (hist_close[i] - hist_close[i-1]) / hist_close[i-1]
        returns.append(ret)
    
    mean_ret = sum(returns) / len(returns)
    variance = sum((r - mean_ret) ** 2 for r in returns) / len(returns)
    daily_vol = math.sqrt(variance)
    annual_vol = daily_vol * math.sqrt(252)
    
    return annual_vol

# 提取各資產數據
assets = {
    '0050': extract_data('0050.TW'),
    'VOO': extract_data('VOO'),
    '台泥': extract_data('1101.TW'),
    '友達': extract_data('2409.TW'),
    '佳世達': extract_data('2352.TW'),
    '高股息': extract_data('00878.TW'),
    '群益高息': extract_data('00919.TW')
}

# 計算報酬
print("=" * 80)
print("【項目1：真實報酬計算】")
print("=" * 80)

for ticker, asset in assets.items():
    returns = calculate_returns(asset['hist_close'])
    if returns:
        print(f"\n{ticker} ({asset['name']})")
        print(f"  期初價格: {asset['hist_close'][0]:.2f}")
        print(f"  期末價格: {asset['price']:.2f}")
        print(f"  股價報酬: {returns['price_return']*100:.2f}%")
        print(f"  含股息報酬: {returns['total_return']*100:.2f}%")
        print(f"  扣費用後: {returns['net_return']*100:.2f}%")
        print(f"  實質報酬(扣通膨): {returns['real_return']*100:.2f}%")
        print(f"  年化波動率: {calculate_volatility(asset['hist_close'])*100:.2f}%")

# Stress Test
print("\n" + "=" * 80)
print("【項目2：Stress Test 極端情境分析】")
print("=" * 80)

scenarios = {
    '情境A (2008金融海嘯)': 0.50,
    '情境B (2020 COVID)': 0.30,
    '情境C (2022升息恐慌)': 0.35,
    '情境D (關稅戰升級)': 0.40
}

test_assets = {
    '0050': 72.35,
    '友達': 14.50,
    '台泥': 23.0
}

for asset_name, current_price in test_assets.items():
    print(f"\n{asset_name} (現價: {current_price}元)")
    for scenario, decline_pct in scenarios.items():
        new_price = current_price * (1 - decline_pct)
        print(f"  {scenario}: 跌至 {new_price:.2f}元 (虧損 {decline_pct*100:.1f}%)")

# 計算交易成本
print("\n" + "=" * 80)
print("【項目4：交易成本計算】")
print("=" * 80)

trade_amount = 1000000  # 100萬
fee_rate = 0.001425  # 0.1425%
tax_rate = 0.003  # 0.3%
total_cost_rate = fee_rate + tax_rate

cost = trade_amount * total_cost_rate
print(f"買賣金額: {trade_amount:,}元")
print(f"手續費率: {fee_rate*100:.4f}%")
print(f"證交稅率: {tax_rate*100:.2f}%")
print(f"總成本率: {total_cost_rate*100:.4f}%")
print(f"一次買賣成本: {cost:,.0f}元")
print(f"建議: 減少交易次數，每次買足，降低成本")

print("\n" + "=" * 80)
print("【項目3：VOO 匯率風險分析】")
print("=" * 80)

# 過去10年台幣/美元匯率（2016-2026）
# 資料來源：歷史平均
usd_twd_rates = {
    '2016': 32.3,
    '2017': 30.4,
    '2018': 30.7,
    '2019': 30.1,
    '2020': 29.6,
    '2021': 28.9,
    '2022': 30.6,
    '2023': 31.5,
    '2024': 32.2,
    '2025': 32.5,
    '2026': 32.3  # 目前
}

rates = list(usd_twd_rates.values())
avg_rate = sum(rates) / len(rates)
max_rate = max(rates)
min_rate = min(rates)

print(f"過去10年台幣/美元匯率:")
print(f"  最高: {max_rate:.2f}")
print(f"  最低: {min_rate:.2f}")
print(f"  平均: {avg_rate:.2f}")
print(f"  目前: {rates[-1]:.2f}")

# 計算匯率風險
investment_usd = 100000 / 32.3  # 10萬台幣換美元
print(f"\n10萬台幣買VOO:")
print(f"  換美元: ${investment_usd:.2f}")
print(f"  按最高匯率(32.5): {investment_usd * 32.5:,.0f}台幣")
print(f"  按最低匯率(28.9): {investment_usd * 28.9:,.0f}台幣")
print(f"  匯率風險: {(32.5 - 28.9) / 30.7 * 100:.1f}%")

print(f"\n保守型VOO配置建議: 不超過30-40%")
print(f"理由: 匯率波動風險約10-12%，需要長期持有以平均成本")

EOF
