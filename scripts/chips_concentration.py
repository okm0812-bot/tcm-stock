import yfinance as yf
import numpy as np
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# 籌碼集中度：用大量買超/賣超天數 + 持股集中度代理
# 來源：Yahoo Finance 歷史成交量 + 法人買賣超

import requests
import datetime
from collections import defaultdict

def fetch_institutional_detail(stock_id, days=30):
    """抓取三大法人買賣超明細"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://api.finmindtrade.com/api/v4/data'
    start = (datetime.date.today() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')
    params = {
        'dataset': 'TaiwanStockInstitutionalInvestorsBuySell',
        'data_id': stock_id,
        'start_date': start,
        'token': '',
    }
    r = requests.get(url, params=params, headers=headers, timeout=15)
    return r.json().get('data', [])

def analyze_concentration(stock_id, name):
    print(f'\n{"="*65}')
    print(f'籌碼集中度分析：{name} ({stock_id})')
    print(f'{"="*65}')

    # 1. 法人連續買超/賣超
    data = fetch_institutional_detail(stock_id, days=30)
    if data:
        data = sorted(data, key=lambda x: x['date'])

        # 整理每日三大法人合計
        daily = defaultdict(int)
        for row in data:
            net = row.get('buy', 0) - row.get('sell', 0)
            daily[row['date']] += net

        dates = sorted(daily.keys())
        nets = [daily[d] for d in dates]

        # 連續買超/賣超天數
        streak = 0
        direction = None
        for n in reversed(nets):
            if direction is None:
                direction = 'buy' if n > 0 else 'sell'
            if direction == 'buy' and n > 0:
                streak += 1
            elif direction == 'sell' and n <= 0:
                streak += 1
            else:
                break

        total_net = sum(nets)
        recent5_net = sum(nets[-5:]) if len(nets) >= 5 else sum(nets)

        print(f'\n【三大法人籌碼】')
        print(f'  近30日合計淨買超: {total_net:+,} 張')
        print(f'  近5日合計淨買超:  {recent5_net:+,} 張')

        if direction == 'buy':
            print(f'  連續買超: {streak} 天 🟢')
        else:
            print(f'  連續賣超: {streak} 天 🔴')

        # 評估
        if total_net > 5000:
            print('  評估: 🟢🟢 法人大量買進，籌碼集中中')
        elif total_net > 1000:
            print('  評估: 🟢 法人小量買進')
        elif total_net > -1000:
            print('  評估: 🟡 法人中性')
        elif total_net > -5000:
            print('  評估: 🔴 法人小量賣出')
        else:
            print('  評估: 🔴🔴 法人大量賣出，籌碼鬆散')

        # 顯示近10日明細
        print(f'\n  近10日法人買賣超：')
        print(f'  {"日期":<12} {"淨買超":>10} {"訊號"}')
        print(f'  {"-"*35}')
        for d, n in zip(dates[-10:], nets[-10:]):
            sig = '🟢' if n > 0 else '🔴'
            print(f'  {d:<12} {n:>+10,} 張  {sig}')

    # 2. 股價與成交量分析（籌碼集中度代理）
    print(f'\n【成交量籌碼分析】')
    try:
        hist = yf.Ticker(f'{stock_id}.TW').history(period='3mo')
        if len(hist) > 20:
            avg_vol = hist['Volume'].mean()
            recent_vol = hist['Volume'].tail(5).mean()
            vol_ratio = recent_vol / avg_vol

            price_now = hist['Close'].iloc[-1]
            price_1m  = hist['Close'].iloc[-22] if len(hist) >= 22 else hist['Close'].iloc[0]
            price_chg = (price_now / price_1m - 1) * 100

            print(f'  平均日成交量: {avg_vol/1000:.0f} 千股')
            print(f'  近5日成交量:  {recent_vol/1000:.0f} 千股')
            print(f'  量比（近5日/均量）: {vol_ratio:.2f}x')

            # 量價關係判斷
            if vol_ratio > 1.5 and price_chg > 0:
                print('  量價判斷: 🟢🟢 價漲量增，主力積極買進')
            elif vol_ratio > 1.5 and price_chg < 0:
                print('  量價判斷: 🔴🔴 價跌量增，主力出貨中！')
            elif vol_ratio < 0.7 and price_chg > 0:
                print('  量價判斷: 🟡 價漲量縮，上漲動能不足')
            elif vol_ratio < 0.7 and price_chg < 0:
                print('  量價判斷: 🟡 價跌量縮，賣壓減輕')
            else:
                print('  量價判斷: 🟡 量價中性')

            # 籌碼集中度估算
            # 用近期成交量佔流通股比例估算換手率
            shares = hist['Volume'].tail(20).sum()
            total_shares_est = avg_vol * 252  # 估算流通股
            turnover = shares / total_shares_est * 100 if total_shares_est > 0 else 0

            print(f'  近20日換手率估算: {turnover:.1f}%')
            if turnover < 10:
                print('  籌碼評估: 🟢 換手率低，籌碼穩定集中')
            elif turnover < 30:
                print('  籌碼評估: 🟡 換手率中等')
            else:
                print('  籌碼評估: 🔴 換手率高，籌碼鬆散')

    except Exception as e:
        print(f'  無法取得數據: {e}')


if __name__ == '__main__':
    print('=' * 65)
    print('籌碼集中度分析系統')
    print('資料來源：FinMind API + Yahoo Finance')
    print('=' * 65)

    stocks = [
        ('1101', '台泥'),
        ('2352', '佳世達'),
        ('2409', '友達'),
        ('6919', '康霈'),
    ]

    for sid, name in stocks:
        analyze_concentration(sid, name)

    print()
    print('=' * 65)
    print('分析完成')
    print('=' * 65)
