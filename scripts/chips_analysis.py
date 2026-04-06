import requests, sys
import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def fetch_foreign_holding(stock_id, days=60):
    """抓取外資持股比例"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://api.finmindtrade.com/api/v4/data'
    start = (datetime.date.today() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')

    params = {
        'dataset': 'TaiwanStockShareholding',
        'data_id': stock_id,
        'start_date': start,
        'token': '',
    }
    r = requests.get(url, params=params, headers=headers, timeout=15)
    return r.json().get('data', [])

def fetch_director_holding(stock_id):
    """抓取董監持股"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://api.finmindtrade.com/api/v4/data'
    start = (datetime.date.today() - datetime.timedelta(days=120)).strftime('%Y-%m-%d')

    params = {
        'dataset': 'TaiwanStockDirectorShareholding',
        'data_id': stock_id,
        'start_date': start,
        'token': '',
    }
    r = requests.get(url, params=params, headers=headers, timeout=15)
    return r.json().get('data', [])

def fetch_margin_balance(stock_id, days=30):
    """抓取融資融券"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://api.finmindtrade.com/api/v4/data'
    start = (datetime.date.today() - datetime.timedelta(days=days)).strftime('%Y-%m-%d')

    params = {
        'dataset': 'TaiwanStockMarginPurchaseShortSale',
        'data_id': stock_id,
        'start_date': start,
        'token': '',
    }
    r = requests.get(url, params=params, headers=headers, timeout=15)
    return r.json().get('data', [])

def analyze_chips(stock_id, name):
    print(f'\n{"="*65}')
    print(f'籌碼分析：{name} ({stock_id})')
    print(f'{"="*65}')

    # 1. 外資持股比例
    print('\n【外資持股比例】')
    fh_data = fetch_foreign_holding(stock_id, days=90)
    if fh_data:
        fh_data = sorted(fh_data, key=lambda x: x['date'])
        latest = fh_data[-1]
        oldest = fh_data[0]

        foreign_pct = latest.get('ForeignInvestmentSharesRatio', 0)
        foreign_pct_old = oldest.get('ForeignInvestmentSharesRatio', 0)
        change = foreign_pct - foreign_pct_old

        print(f'  目前外資持股比例: {foreign_pct:.2f}%')
        print(f'  近3個月變化: {change:+.2f}%')

        if foreign_pct > 50:
            print('  評估: 🟢 外資高度持有，護盤意願強')
        elif foreign_pct > 30:
            print('  評估: 🟢 外資持有比例高，相對穩定')
        elif foreign_pct > 15:
            print('  評估: 🟡 外資持有中等')
        else:
            print('  評估: 🔴 外資持有比例低，波動風險高')

        if change > 2:
            print(f'  趨勢: 🟢 外資近期持續買進 (+{change:.1f}%)')
        elif change < -2:
            print(f'  趨勢: 🔴 外資近期持續賣出 ({change:.1f}%)')
        else:
            print(f'  趨勢: 🟡 外資持股變化不大')
    else:
        print('  無法取得外資持股數據')

    # 2. 融資融券
    print('\n【融資融券餘額】')
    mg_data = fetch_margin_balance(stock_id, days=30)
    if mg_data:
        mg_data = sorted(mg_data, key=lambda x: x['date'])
        latest_mg = mg_data[-1]
        oldest_mg = mg_data[0]

        margin_buy = latest_mg.get('MarginPurchaseTodayBalance', 0)
        short_sell = latest_mg.get('ShortSaleTodayBalance', 0)
        margin_buy_old = oldest_mg.get('MarginPurchaseTodayBalance', 0)
        short_sell_old = oldest_mg.get('ShortSaleTodayBalance', 0)

        margin_chg = (margin_buy - margin_buy_old) / margin_buy_old * 100 if margin_buy_old > 0 else 0
        short_chg  = (short_sell - short_sell_old) / short_sell_old * 100 if short_sell_old > 0 else 0

        print(f'  融資餘額: {margin_buy:,} 張  (近月變化: {margin_chg:+.1f}%)')
        print(f'  融券餘額: {short_sell:,} 張  (近月變化: {short_chg:+.1f}%)')

        # 融資使用率
        if margin_buy > 0 and short_sell > 0:
            ratio = short_sell / margin_buy * 100
            print(f'  券資比: {ratio:.1f}%')
            if ratio > 15:
                print('  評估: 🟢 券資比高，空頭多，可能有軋空行情')
            elif ratio < 5:
                print('  評估: 🟡 券資比低，空頭少')

        if margin_chg > 10:
            print(f'  融資警示: 🔴 融資大幅增加 (+{margin_chg:.1f}%)，散戶借錢追高，風險上升')
        elif margin_chg < -10:
            print(f'  融資趨勢: 🟢 融資減少 ({margin_chg:.1f}%)，去槓桿中，較健康')
    else:
        print('  無法取得融資融券數據')

    # 3. 董監持股
    print('\n【董監持股】')
    dir_data = fetch_director_holding(stock_id)
    if dir_data:
        dir_data = sorted(dir_data, key=lambda x: x['date'])
        if len(dir_data) >= 2:
            latest_dir = dir_data[-1]
            oldest_dir = dir_data[0]
            dir_pct = latest_dir.get('DirectorShareholdingRatio', 0)
            dir_pct_old = oldest_dir.get('DirectorShareholdingRatio', 0)
            dir_chg = dir_pct - dir_pct_old

            print(f'  董監持股比例: {dir_pct:.2f}%')
            print(f'  近期變化: {dir_chg:+.2f}%')

            if dir_pct > 30:
                print('  評估: 🟢 董監高度持股，與股東利益一致')
            elif dir_pct > 15:
                print('  評估: 🟡 董監持股中等')
            else:
                print('  評估: 🔴 董監持股偏低，需注意')

            if dir_chg < -2:
                print(f'  警示: 🔴 董監近期大量減持 ({dir_chg:.1f}%)，內部人出逃！')
            elif dir_chg > 1:
                print(f'  訊號: 🟢 董監近期增持 (+{dir_chg:.1f}%)，內部人看好')
    else:
        print('  無法取得董監持股數據')


if __name__ == '__main__':
    print('=' * 65)
    print('籌碼分析系統（外資持股 + 融資融券 + 董監持股）')
    print('資料來源：FinMind API（台灣證交所官方數據）')
    print('=' * 65)

    stocks = [
        ('1101', '台泥'),
        ('2352', '佳世達'),
        ('2409', '友達'),
        ('6919', '康霈'),
    ]

    for sid, name in stocks:
        analyze_chips(sid, name)

    print()
    print('=' * 65)
    print('分析完成')
    print('=' * 65)
