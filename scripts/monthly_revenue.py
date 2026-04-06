import requests, sys
import datetime

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def fetch_monthly_revenue(stock_id, months=18):
    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://api.finmindtrade.com/api/v4/data'
    start = (datetime.date.today() - datetime.timedelta(days=months*35)).strftime('%Y-%m-%d')
    params = {
        'dataset': 'TaiwanStockMonthRevenue',
        'data_id': stock_id,
        'start_date': start,
        'token': '',
    }
    r = requests.get(url, params=params, headers=headers, timeout=15)
    return r.json().get('data', [])

def analyze_revenue(stock_id, name):
    data = fetch_monthly_revenue(stock_id, months=26)
    if not data:
        print(f'{name} ({stock_id}): 無法取得月營收數據')
        return None

    data = sorted(data, key=lambda x: (x['revenue_year'], x['revenue_month']))

    # 建立 {(year, month): revenue} 字典
    rev_dict = {}
    for row in data:
        key = (row['revenue_year'], row['revenue_month'])
        rev_dict[key] = row['revenue']

    print(f'\n{"="*65}')
    print(f'月營收分析：{name} ({stock_id})')
    print(f'{"="*65}')
    print(f'{"月份":<10} {"月營收(億)":>10} {"月增率":>9} {"年增率":>9} {"訊號"}')
    print('-' * 65)

    # 只顯示最近12個月
    recent = sorted(rev_dict.keys())[-12:]
    yoy_list = []
    prev_rev = None

    for key in recent:
        y, m = key
        rev = rev_dict[key]
        rev_b = rev / 1e8  # 億元

        # 月增率
        if prev_rev and prev_rev > 0:
            mom = (rev - prev_rev) / prev_rev * 100
        else:
            mom = 0

        # 年增率（同期去年）
        prev_year_key = (y - 1, m)
        if prev_year_key in rev_dict and rev_dict[prev_year_key] > 0:
            yoy = (rev - rev_dict[prev_year_key]) / rev_dict[prev_year_key] * 100
        else:
            yoy = None

        if yoy is not None:
            yoy_list.append(yoy)
            if yoy > 20:
                sig = '🟢🟢 強勁成長'
            elif yoy > 5:
                sig = '🟢 成長'
            elif yoy > -5:
                sig = '🟡 持平'
            elif yoy > -20:
                sig = '🔴 衰退'
            else:
                sig = '🔴🔴 嚴重衰退'
            yoy_str = f'{yoy:>+8.1f}%'
        else:
            sig = '🟡 無去年數據'
            yoy_str = f'{"N/A":>9}'

        mom_str = f'{mom:>+8.1f}%' if prev_rev else f'{"N/A":>9}'
        print(f'{y}-{m:02d}       {rev_b:>10.2f} {mom_str} {yoy_str}  {sig}')
        prev_rev = rev

    # 趨勢分析
    print()
    if yoy_list:
        avg3 = sum(yoy_list[-3:]) / len(yoy_list[-3:]) if len(yoy_list) >= 3 else sum(yoy_list) / len(yoy_list)
        avg6 = sum(yoy_list[-6:]) / len(yoy_list[-6:]) if len(yoy_list) >= 6 else sum(yoy_list) / len(yoy_list)
        print(f'近3個月平均年增率: {avg3:+.1f}%')
        print(f'近6個月平均年增率: {avg6:+.1f}%')

        # 連續成長/衰退
        streak = 0
        direction = None
        for s in reversed(yoy_list):
            if direction is None:
                direction = 'up' if s > 0 else 'down'
            if direction == 'up' and s > 0:
                streak += 1
            elif direction == 'down' and s <= 0:
                streak += 1
            else:
                break

        if direction == 'up':
            print(f'連續年增率正成長: {streak} 個月 🟢')
        else:
            print(f'連續年增率衰退: {streak} 個月 🔴')

        print()
        if avg3 > 15 and avg6 < 0:
            print('⚡ 轉機訊號：近3月大幅改善，業績可能反轉！')
        elif avg3 > 10:
            print('✅ 業績強勁成長中')
        elif avg3 > 0:
            print('🟢 業績溫和成長')
        elif avg3 > -10:
            print('🟡 業績持平或小幅衰退')
        else:
            print('🔴 業績持續衰退，基本面不佳')

        return {'avg3': avg3, 'avg6': avg6, 'streak': streak, 'direction': direction}
    return None


if __name__ == '__main__':
    print('=' * 65)
    print('月營收分析系統（自動計算 YoY/MoM）')
    print('資料來源：FinMind API（台灣證交所官方數據）')
    print('=' * 65)

    stocks = [
        ('1101', '台泥'),
        ('2352', '佳世達'),
        ('2409', '友達'),
        ('6919', '康霈'),
    ]

    results = {}
    for sid, name in stocks:
        result = analyze_revenue(sid, name)
        if result:
            results[name] = result

    if results:
        print()
        print('=' * 65)
        print('月營收綜合評比')
        print('=' * 65)
        print(f'{"股票":<10} {"近3月YoY":>10} {"近6月YoY":>10} {"趨勢":<18} {"評級"}')
        print('-' * 65)
        for name, r in results.items():
            trend = f'連續{"成長" if r["direction"]=="up" else "衰退"}{r["streak"]}月'
            if r['avg3'] > 10:
                grade = 'A 強勁'
            elif r['avg3'] > 0:
                grade = 'B 成長'
            elif r['avg3'] > -10:
                grade = 'C 持平'
            else:
                grade = 'D 衰退'
            print(f'{name:<10} {r["avg3"]:>+9.1f}% {r["avg6"]:>+9.1f}%  {trend:<18} {grade}')
