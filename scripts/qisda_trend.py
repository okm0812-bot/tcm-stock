# -*- coding: utf-8 -*-
"""
佳世達 2352 近期盤勢分析
"""
import yfinance as yf
from datetime import datetime, timedelta

print("\n" + "="*70)
print(f"【佳世達 2352 近期盤勢分析】{datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("="*70)

try:
    stock = yf.Ticker("2352.TW")
    
    # 取得最近1個月資料
    hist = stock.history(period="1mo")
    
    print("\n【近30日股價走勢】")
    print("-"*70)
    print(f"{'日期':<12} {'開盤':>8} {'最高':>8} {'最低':>8} {'收盤':>8} {'成交量':>12}")
    print("-"*70)
    
    for idx, row in hist.tail(15).iterrows():
        date_str = idx.strftime('%Y-%m-%d')
        print(f"{date_str:<12} {row['Open']:>8.2f} {row['High']:>8.2f} {row['Low']:>8.2f} {row['Close']:>8.2f} {int(row['Volume']):>12,}")
    
    # 技術分析
    latest = hist.iloc[-1]
    prev = hist.iloc[-2]
    
    print("\n【技術面分析】")
    print("-"*70)
    
    # 計算5日、10日均線
    ma5 = hist['Close'].tail(5).mean()
    ma10 = hist['Close'].tail(10).mean()
    ma20 = hist['Close'].tail(20).mean()
    
    print(f"5日均線: {ma5:.2f} 元")
    print(f"10日均線: {ma10:.2f} 元")
    print(f"20日均線: {ma20:.2f} 元")
    print(f"現價: {latest['Close']:.2f} 元")
    
    # 判斷趨勢
    if latest['Close'] > ma5 > ma10:
        print("\n趨勢: 短期偏多（股價 > 5MA > 10MA）")
    elif latest['Close'] < ma5 < ma10:
        print("\n趨勢: 短期偏空（股價 < 5MA < 10MA）")
    else:
        print("\n趨勢: 盤整（均線糾結）")
    
    # 支撐壓力
    recent_low = hist['Low'].tail(20).min()
    recent_high = hist['High'].tail(20).max()
    
    print(f"\n近20日低點（支撐）: {recent_low:.2f} 元")
    print(f"近20日高點（壓力）: {recent_high:.2f} 元")
    print(f"距離支撐: {((latest['Close'] - recent_low) / recent_low * 100):.2f}%")
    print(f"距離壓力: {((recent_high - latest['Close']) / latest['Close'] * 100):.2f}%")
    
    # RSI
    delta = hist['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    latest_rsi = rsi.iloc[-1]
    
    print(f"\nRSI(14): {latest_rsi:.2f}")
    if latest_rsi < 30:
        print("  狀態: 超賣區（<30），可能反彈")
    elif latest_rsi > 70:
        print("  狀態: 超買區（>70），可能回檔")
    else:
        print("  狀態: 中性區間")
    
    # 成交量分析
    avg_volume = hist['Volume'].tail(20).mean()
    latest_volume = latest['Volume']
    
    print(f"\n成交量分析:")
    print(f"  今日成交量: {int(latest_volume):,}")
    print(f"  20日均量: {int(avg_volume):,}")
    print(f"  量比: {latest_volume / avg_volume:.2f}x")
    
    if latest_volume > avg_volume * 1.5:
        print("  狀態: 放量（>1.5倍），有買盤")
    elif latest_volume < avg_volume * 0.5:
        print("  狀態: 縮量（<0.5倍），觀望氣氛濃")
    else:
        print("  狀態: 量能正常")
    
    # 綜合判斷
    print("\n" + "="*70)
    print("【反彈可能性評估】")
    print("="*70)
    
    signals = []
    
    if latest_rsi < 30:
        signals.append(("RSI超賣", True, "技術性反彈機會高"))
    else:
        signals.append(("RSI中性", False, "尚未超賣"))
    
    if latest['Close'] <= recent_low * 1.05:
        signals.append(("接近支撐", True, "可能獲得支撐"))
    else:
        signals.append(("距離支撐遠", False, "仍有下跌空間"))
    
    if latest_volume > avg_volume:
        signals.append(("放量", True, "有買盤進場"))
    else:
        signals.append(("縮量", False, "買盤不足"))
    
    if latest['Close'] > ma5:
        signals.append(("站上5MA", True, "短線轉強"))
    else:
        signals.append(("跌破5MA", False, "短線偏弱"))
    
    print(f"\n{'指標':<15} {'狀態':<10} {'解讀'}")
    print("-"*70)
    for name, positive, reason in signals:
        status = "有利" if positive else "不利"
        print(f"{name:<15} {status:<10} {reason}")
    
    positive_count = sum(1 for _, p, _ in signals if p)
    
    print("\n" + "="*70)
    if positive_count >= 3:
        print("結論: 反彈機會較高，可等反彈再賣")
    elif positive_count >= 2:
        print("結論: 反彈機會中等，可觀察1-2天")
    else:
        print("結論: 反彈機會較低，建議儘快停損")
    print("="*70)
    
    # 你的持股
    print(f"\n【你的持股狀況】")
    print(f"  成本: 53.78 元")
    print(f"  現價: {latest['Close']:.2f} 元")
    print(f"  虧損: {((latest['Close'] - 53.78) / 53.78 * 100):.2f}%")
    print(f"  距離 52週低點: {((latest['Close'] - 22.55) / 22.55 * 100):.2f}%")
    
    # 最終建議
    print("\n" + "="*70)
    print("【最終建議】")
    print("="*70)
    if positive_count >= 3:
        print("\n可等反彈至 5日均線附近（約 {:.2f} 元）再賣出".format(ma5))
        print("但嚴設停損：若跌破近期低點 {:.2f} 元，立即出場".format(recent_low))
    else:
        print("\n不建議等待反彈")
        print("理由: 技術面偏弱、成交量縮減、基本面差")
        print("建議: 今日趁有量能時停損出場")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
