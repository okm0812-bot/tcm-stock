import yfinance as yf
import numpy as np
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print('=' * 70)
print('Monte Carlo 投資組合模擬 - 延長版（1年/3年/5年）')
print('=' * 70)

# 持倉
portfolio = {
    '1101.TW': {'name': '台泥',   'shares': 19000, 'cost': 34.56, 'weight': 0.15},
    '2352.TW': {'name': '佳世達', 'shares': 11000, 'cost': 53.78, 'weight': 0.09},
    '2409.TW': {'name': '友達',   'shares':  9000, 'cost': 16.20, 'weight': 0.05},
    '6919.TW': {'name': '康霈',   'shares':   300, 'cost': 102.36,'weight': 0.01},
    'BOND':    {'name': '美債ETF', 'value': 1986690,'weight': 0.70},
}

# 抓取歷史報酬
print('抓取歷史數據...')
ann_returns = []
ann_vols    = []
weights     = []

for ticker, info in portfolio.items():
    if ticker == 'BOND':
        ann_returns.append(0.03)
        ann_vols.append(0.08)
        weights.append(info['weight'])
        print(f"  美債ETF  年化報酬: +3.0%  波動: 8.0%")
        continue
    try:
        hist = yf.Ticker(ticker).history(period='3y')
        r = hist['Close'].pct_change().dropna()
        ar = r.mean() * 252
        av = r.std() * np.sqrt(252)
        ann_returns.append(ar)
        ann_vols.append(av)
        weights.append(info['weight'])
        print(f"  {info['name']:<8} 年化報酬: {ar*100:+.1f}%  波動: {av*100:.1f}%")
    except:
        ann_returns.append(0)
        ann_vols.append(0.3)
        weights.append(info['weight'])

weights = np.array(weights)
weights = weights / weights.sum()

port_return = np.dot(weights, ann_returns)
port_vol    = np.sqrt(np.dot(weights**2, np.array(ann_vols)**2))

print()
print(f'投資組合年化預期報酬: {port_return*100:.1f}%')
print(f'投資組合年化波動率:   {port_vol*100:.1f}%')
print()

# 初始價值
try:
    total_stock = 0
    for ticker, info in portfolio.items():
        if ticker == 'BOND':
            total_stock += info['value']
            continue
        price = yf.Ticker(ticker).info.get('regularMarketPrice', info['cost'])
        total_stock += price * info['shares']
    initial_value = total_stock
except:
    initial_value = 2830000

print(f'初始投資組合價值: {initial_value:,.0f} 元')
print()

np.random.seed(42)
n_sim = 10000

for years, label in [(1, '1年'), (3, '3年'), (5, '5年')]:
    n_days = years * 252
    daily_r = port_return / 252
    daily_v = port_vol / np.sqrt(252)

    rand = np.random.normal(daily_r, daily_v, (n_sim, n_days))
    cum  = np.cumprod(1 + rand, axis=1)
    final = initial_value * cum[:, -1]

    p5   = np.percentile(final, 5)
    p25  = np.percentile(final, 25)
    p50  = np.percentile(final, 50)
    p75  = np.percentile(final, 75)
    p95  = np.percentile(final, 95)
    mean = np.mean(final)

    profit_prob = np.mean(final > initial_value) * 100
    loss30_prob = np.mean(final < initial_value * 0.7) * 100

    print('=' * 70)
    print(f'【{label}後情境預測】（模擬 {n_sim:,} 次）')
    print('=' * 70)
    print(f'  5%  極度悲觀: {p5:>12,.0f} 元  ({(p5/initial_value-1)*100:+.1f}%)')
    print(f' 25%  悲觀:     {p25:>12,.0f} 元  ({(p25/initial_value-1)*100:+.1f}%)')
    print(f' 50%  中性:     {p50:>12,.0f} 元  ({(p50/initial_value-1)*100:+.1f}%)')
    print(f' 75%  樂觀:     {p75:>12,.0f} 元  ({(p75/initial_value-1)*100:+.1f}%)')
    print(f' 95%  極度樂觀: {p95:>12,.0f} 元  ({(p95/initial_value-1)*100:+.1f}%)')
    print(f'      平均值:   {mean:>12,.0f} 元  ({(mean/initial_value-1)*100:+.1f}%)')
    print()
    print(f'  獲利機率（不賠不賺以上）: {profit_prob:.1f}%')
    print(f'  重大虧損機率（虧損>30%）: {loss30_prob:.1f}%')
    print()

print('=' * 70)
print('換股後（假設換成 0050+00881）的對比模擬')
print('=' * 70)

# 換股後假設：年化報酬 12%，波動 22%
new_return = 0.12
new_vol    = 0.22

print(f'假設換股後: 年化報酬 {new_return*100:.0f}%，波動 {new_vol*100:.0f}%')
print()

for years, label in [(1, '1年'), (3, '3年'), (5, '5年')]:
    n_days = years * 252
    daily_r = new_return / 252
    daily_v = new_vol / np.sqrt(252)

    rand = np.random.normal(daily_r, daily_v, (n_sim, n_days))
    cum  = np.cumprod(1 + rand, axis=1)
    final = initial_value * cum[:, -1]

    p5   = np.percentile(final, 5)
    p50  = np.percentile(final, 50)
    p95  = np.percentile(final, 95)
    profit_prob = np.mean(final > initial_value) * 100

    print(f'【換股後 {label}】')
    print(f'  5%  悲觀:   {p5:>12,.0f} 元  ({(p5/initial_value-1)*100:+.1f}%)')
    print(f' 50%  中性:   {p50:>12,.0f} 元  ({(p50/initial_value-1)*100:+.1f}%)')
    print(f' 95%  樂觀:   {p95:>12,.0f} 元  ({(p95/initial_value-1)*100:+.1f}%)')
    print(f'  獲利機率: {profit_prob:.1f}%')
    print()
