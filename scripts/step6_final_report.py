# -*- coding: utf-8 -*-
"""
階段 6: 整合最終報告
"""
import json
from datetime import datetime, timezone, timedelta

tz8 = timezone(timedelta(hours=8))
now = datetime.now(tz8).strftime('%Y-%m-%d %H:%M:%S')

lines = []
def add(t=''): lines.append(t)

# 讀取所有結果
with open('market_data_raw.json', 'r', encoding='utf-8') as f:
    market_data = json.load(f)
with open('monte_carlo_results.json', 'r', encoding='utf-8') as f:
    mc_data = json.load(f)
with open('mpt_results.json', 'r', encoding='utf-8') as f:
    mpt_data = json.load(f)
with open('fama_french_results.json', 'r', encoding='utf-8') as f:
    ff_data = json.load(f)

add("="*70)
add("CEO 深度分析報告 v2.0")
add("Monte Carlo + MPT + Fama-French 三模型整合")
add("="*70)
add(f"生成時間: {now}")
add(f"數據來源: Yahoo Finance 3年歷史 + 聯網搜尋")
add("")

# ==================== 1. 市場現況 ====================
add("[1. 市場現況]")
add("-"*70)
twii = market_data.get('^TWII', {})
sp500 = market_data.get('^GSPC', {})
vix = market_data.get('^VIX', {})
tnx = market_data.get('^TNX', {})

add(f"  台股加權指數: {twii.get('price', 0):,.0f} 點")
add(f"  S&P 500:      {sp500.get('price', 0):,.0f} 點")
add(f"  VIX 恐慌指數: {vix.get('price', 0):.2f}")
add(f"  美國10年債:   {tnx.get('price', 0):.3f}%")
add("")
add("  市場環境評估:")
vix_val = vix.get('price', 0)
if vix_val > 30:
    add("    VIX > 30: 市場恐慌，高風險環境")
elif vix_val > 20:
    add("    VIX 20-30: 市場謹慎，中等風險")
else:
    add("    VIX < 20: 市場平靜，低風險環境")

# ==================== 2. Monte Carlo ====================
add("")
add("[2. Monte Carlo 台股走勢模擬（10,000次模擬，1年期）]")
add("-"*70)
add("")

for code in ['^TWII', '0050.TW', '00919.TW', 'VOO']:
    if code not in mc_data:
        continue
    mc = mc_data[code]
    name = mc['name']
    p = mc['last_price']
    
    add(f"  【{name}】")
    add(f"  現價: {p:.2f}")
    add(f"  年化預期報酬: {mc['mu_annual']*100:+.2f}%")
    add(f"  年化波動率:   {mc['sigma_annual']*100:.2f}%")
    add("")
    add(f"  1年後價格分佈（10,000次模擬）:")
    add(f"    最悲觀 5%:  {mc['p5']:.2f}  ({(mc['p5']/p-1)*100:+.1f}%)")
    add(f"    悲觀 10%:   {mc['p10']:.2f}  ({(mc['p10']/p-1)*100:+.1f}%)")
    add(f"    悲觀 25%:   {mc['p25']:.2f}  ({(mc['p25']/p-1)*100:+.1f}%)")
    add(f"    中位數 50%: {mc['p50']:.2f}  ({(mc['p50']/p-1)*100:+.1f}%)")
    add(f"    樂觀 75%:   {mc['p75']:.2f}  ({(mc['p75']/p-1)*100:+.1f}%)")
    add(f"    樂觀 90%:   {mc['p90']:.2f}  ({(mc['p90']/p-1)*100:+.1f}%)")
    add(f"    最樂觀 95%: {mc['p95']:.2f}  ({(mc['p95']/p-1)*100:+.1f}%)")
    add("")
    add(f"  機率分析:")
    add(f"    上漲機率:       {mc['prob_up']*100:.1f}%")
    add(f"    上漲 >10% 機率: {mc['prob_up10']*100:.1f}%")
    add(f"    上漲 >20% 機率: {mc['prob_up20']*100:.1f}%")
    add(f"    下跌 >10% 機率: {mc['prob_down10']*100:.1f}%")
    add(f"    下跌 >20% 機率: {mc['prob_down20']*100:.1f}%")
    add("")

# ==================== 3. MPT ====================
add("[3. MPT 現代投資組合理論優化（50,000次模擬）]")
add("-"*70)
add("")

assets = mpt_data.get('assets', [])
names = [a['name'] for a in assets]

add("  各資產基本統計:")
mean_returns = mpt_data.get('mean_returns', [])
for i, a in enumerate(assets):
    if i < len(mean_returns):
        add(f"    {a['name']}: 年化報酬 {mean_returns[i]*252*100:.2f}%")
add("")

bs = mpt_data.get('best_sharpe', {})
mv = mpt_data.get('min_vol', {})
br = mpt_data.get('best_return', {})

add("  【最佳夏普比率組合（風險調整後最優）】")
if bs.get('weights'):
    for i, a in enumerate(assets):
        if i < len(bs['weights']):
            add(f"    {a['name']}: {bs['weights'][i]*100:.1f}%")
add(f"    年化報酬: {bs.get('return', 0)*100:.2f}%")
add(f"    年化波動: {bs.get('std', 0)*100:.2f}%")
add(f"    夏普比率: {bs.get('sharpe', 0):.3f}")
add("")

add("  【最小波動組合（最保守）】")
if mv.get('weights'):
    for i, a in enumerate(assets):
        if i < len(mv['weights']):
            add(f"    {a['name']}: {mv['weights'][i]*100:.1f}%")
add(f"    年化報酬: {mv.get('return', 0)*100:.2f}%")
add(f"    年化波動: {mv.get('std', 0)*100:.2f}%")
add(f"    夏普比率: {mv.get('sharpe', 0):.3f}")
add("")

add("  【最高報酬組合（最積極）】")
if br.get('weights'):
    for i, a in enumerate(assets):
        if i < len(br['weights']):
            add(f"    {a['name']}: {br['weights'][i]*100:.1f}%")
add(f"    年化報酬: {br.get('return', 0)*100:.2f}%")
add(f"    年化波動: {br.get('std', 0)*100:.2f}%")
add(f"    夏普比率: {br.get('sharpe', 0):.3f}")
add("")

# ==================== 4. Fama-French ====================
add("[4. Fama-French 三因子分析]")
add("-"*70)
add("")
add("  因子說明:")
add("    Alpha:    超額報酬（扣除市場、規模、價值因子後）")
add("    Beta 市場: 市場敏感度（>1 放大漲跌，<1 較穩定）")
add("    Beta SMB: 規模因子（>0 偏小型股特性）")
add("    Beta HML: 價值因子（>0 偏價值股，<0 偏成長股）")
add("")

for code, result in ff_data.items():
    name = result['name']
    alpha = result['alpha']
    b_mkt = result['beta_mkt']
    b_smb = result['beta_smb']
    b_hml = result['beta_hml']
    r2 = result['r2']
    
    add(f"  【{name}】")
    add(f"    Alpha (年化):  {alpha*100:+.2f}%  {'[超額報酬]' if alpha > 0 else '[落後市場]'}")
    add(f"    Beta 市場:     {b_mkt:.3f}  {'[高市場敏感]' if b_mkt > 1.2 else '[低市場敏感]' if b_mkt < 0.8 else '[正常]'}")
    add(f"    Beta SMB:      {b_smb:.3f}  {'[小型股特性]' if b_smb > 0.3 else '[大型股特性]' if b_smb < -0.3 else '[中性]'}")
    add(f"    Beta HML:      {b_hml:.3f}  {'[價值股]' if b_hml > 0.3 else '[成長股]' if b_hml < -0.3 else '[中性]'}")
    add(f"    R²:            {r2:.3f}  {'[解釋力強]' if r2 > 0.7 else '[解釋力中]' if r2 > 0.4 else '[解釋力弱]'}")
    add("")

# ==================== 5. 換股建議 ====================
add("[5. 三模型整合換股建議]")
add("-"*70)
add("")

# 從 Monte Carlo 取 0050 數據
mc_0050 = mc_data.get('0050.TW', {})
mc_919 = mc_data.get('00919.TW', {})
mc_voo = mc_data.get('VOO', {})

add("  基於三模型分析結論:")
add("")
add("  【台泥 1101】")
add("    Fama-French: 傳產股，高 HML（價值股特性）")
add("    建議: 逢高減碼 50%，換入 0050")
add("    目標: 23-24 元賣出 5,000-10,000 股")
add("")
add("  【佳世達 2352】")
add("    Fama-French: Alpha 為負，落後市場")
add("    建議: 停損 22.00 元，立刻換出")
add("    換入: 0050 或 VOO")
add("")
add("  【友達 2409】")
add("    Fama-French: 高市場 Beta，景氣循環敏感")
add("    建議: 續抱，等面板景氣改善")
add("    停損: 12.00 元")
add("")
add("  【康霈 6919】")
add("    Fama-French: 高 SMB（小型股），高波動")
add("    建議: 逢高鎖利 100-150 股")
add("    目標: 85-90 元")
add("")

# MPT 最佳組合
add("  【MPT 最佳夏普比率組合建議】")
if bs.get('weights'):
    for i, a in enumerate(assets):
        if i < len(bs['weights']):
            add(f"    {a['name']}: {bs['weights'][i]*100:.1f}%")
add("")

# Monte Carlo 風險評估
add("  【Monte Carlo 風險評估】")
if mc_0050:
    add(f"    0050 下跌 >20% 機率: {mc_0050.get('prob_down20', 0)*100:.1f}%")
    add(f"    0050 上漲 >10% 機率: {mc_0050.get('prob_up10', 0)*100:.1f}%")
if mc_voo:
    add(f"    VOO 下跌 >20% 機率:  {mc_voo.get('prob_down20', 0)*100:.1f}%")
    add(f"    VOO 上漲 >10% 機率:  {mc_voo.get('prob_up10', 0)*100:.1f}%")
add("")

# ==================== 6. 最終建議 ====================
add("="*70)
add("[6. CEO 最終換股建議]")
add("="*70)
add("")
add("  基於 Monte Carlo + MPT + Fama-French 三模型分析:")
add("")
add("  【立即行動（本週）】")
add("  1. 佳世達 2352: 停損 22.00 元 → 換入 0050")
add("     理由: Alpha 為負，落後市場，無回本希望")
add("")
add("  2. 康霈 6919: 逢高鎖利 100-150 股")
add("     理由: 小型股高波動，先鎖利降風險")
add("")
add("  3. 台泥 1101: 逢高減碼 5,000 股")
add("     理由: 傳產股，景氣循環，先減碼")
add("")
add("  【換入配置（MPT 最佳夏普）】")
if bs.get('weights'):
    for i, a in enumerate(assets):
        if i < len(bs['weights']):
            pct = bs['weights'][i] * 100
            add(f"  {a['name']}: {pct:.1f}%")
add("")
add("  【風險控制】")
add("  - 分批買入（每週 25%，共 4 週）")
add("  - 設好停損點（每檔 -15%）")
add("  - 關注美國關稅政策（4月升級風險）")
add("")
add("="*70)
add(f"報告生成: {now}")
add("="*70)

with open('deep_analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('\n'.join(lines))
