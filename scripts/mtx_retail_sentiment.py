import requests, sys, json
import datetime
from collections import defaultdict

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def fetch_mtx_retail_sentiment(days=20):
    """
    抓取小台期貨散戶多空比
    來源：FinMind API（台期所官方數據）
    邏輯：法人淨部位反向 = 散戶方向
    """
    today = datetime.date.today()
    start_date = (today - datetime.timedelta(days=days*2)).strftime('%Y-%m-%d')

    headers = {'User-Agent': 'Mozilla/5.0'}
    url = 'https://api.finmindtrade.com/api/v4/data'
    params = {
        'dataset': 'TaiwanFuturesInstitutionalInvestors',
        'data_id': 'MTX',
        'start_date': start_date,
        'token': '',
    }

    r = requests.get(url, params=params, headers=headers, timeout=15)
    data = r.json().get('data', [])

    # 整理法人數據
    institutional_by_date = defaultdict(dict)
    for row in data:
        d = row['date']
        inv = row['institutional_investors']
        institutional_by_date[d][inv] = {
            'long_oi': row['long_open_interest_balance_volume'],
            'short_oi': row['short_open_interest_balance_volume'],
        }

    results = []
    for d in sorted(institutional_by_date.keys())[-days:]:
        inv = institutional_by_date[d]
        total_long  = sum(v.get('long_oi', 0) for v in inv.values())
        total_short = sum(v.get('short_oi', 0) for v in inv.values())
        net = total_long - total_short

        # 法人淨空 → 散戶偏多（危險）；法人淨多 → 散戶偏空（底部訊號）
        if net < -8000:
            retail_signal = '散戶極度偏多'
            color = '🔴🔴'
            score = -2
        elif net < -3000:
            retail_signal = '散戶偏多'
            color = '🔴'
            score = -1
        elif net < -500:
            retail_signal = '散戶略偏多'
            color = '🟡'
            score = 0
        elif net < 500:
            retail_signal = '散戶中性'
            color = '🟡'
            score = 0
        elif net < 3000:
            retail_signal = '散戶略偏空'
            color = '🟢'
            score = 1
        elif net < 8000:
            retail_signal = '散戶偏空'
            color = '🟢🟢'
            score = 2
        else:
            retail_signal = '散戶極度偏空'
            color = '🟢🟢🟢'
            score = 3

        results.append({
            'date': d,
            'inst_long': total_long,
            'inst_short': total_short,
            'inst_net': net,
            'retail_signal': retail_signal,
            'color': color,
            'score': score,
        })

    return results


if __name__ == '__main__':
    print('=' * 70)
    print('小台期貨（MTX）散戶多空比分析')
    print('資料來源：FinMind API（台期所官方數據）')
    print('=' * 70)
    print()

    results = fetch_mtx_retail_sentiment(days=20)

    print(f'{"日期":<12} {"法人多":>7} {"法人空":>7} {"法人淨":>8}  {"散戶訊號":<12} {"信號"}')
    print('-' * 70)
    for r in results:
        print(f'{r["date"]:<12} {r["inst_long"]:>7,} {r["inst_short"]:>7,} {r["inst_net"]:>+8,}  {r["retail_signal"]:<12} {r["color"]}')

    print()
    print('=' * 70)
    print('今日解讀')
    print('=' * 70)

    latest = results[-1]
    print(f'日期：{latest["date"]}')
    print(f'法人淨部位：{latest["inst_net"]:+,} 口')
    print(f'散戶訊號：{latest["color"]} {latest["retail_signal"]}')
    print()

    score = latest['score']
    if score <= -2:
        print('⚠️  警告：散戶極度偏多，歷史上常是市場頭部！')
        print('   建議：不要追高，等待回調')
    elif score == -1:
        print('⚠️  注意：散戶偏多，市場樂觀情緒過高')
        print('   建議：謹慎，不宜大量買入')
    elif score == 0:
        print('🟡 中性：散戶情緒平衡，無明顯訊號')
        print('   建議：觀察，可少量試單')
    elif score == 1:
        print('🟢 偏正面：散戶略偏空，市場開始悲觀')
        print('   建議：可開始分批佈局')
    elif score >= 2:
        print('🟢🟢 強烈訊號：散戶偏空/極度偏空，歷史上常是底部！')
        print('   建議：積極分批買入，這是好的進場時機')

    print()
    print('近5日趨勢：')
    for r in results[-5:]:
        print(f'  {r["date"]}  {r["color"]} {r["retail_signal"]}')

    print()
    print('=' * 70)
    print('指標說明')
    print('=' * 70)
    print("""
散戶多空比是「反向指標」：
  散戶集體做多 → 市場通常快到頂（賣出訊號）
  散戶集體做空 → 市場通常快到底（買入訊號）

計算方式：
  法人（外資+投信+自營商）淨部位反向推算散戶方向
  法人淨空 → 散戶偏多（危險）
  法人淨多 → 散戶偏空（機會）
""")
