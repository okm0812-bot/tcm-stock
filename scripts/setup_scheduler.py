# -*- coding: utf-8 -*-
"""
自動排程設定 - Windows Task Scheduler
"""
from datetime import datetime

print("\n" + "="*70)
print("【自動排程設定指南】")
print("="*70)

print("""
目標：每日早上 9:00 自動執行投資報告

方法一：Windows 工作排程器 (推薦)
================================

步驟 1: 開啟工作排程器
- 按 Win + R，輸入 "taskschd.msc"
- 或搜尋 "工作排程器"

步驟 2: 建立基本工作
- 右鍵點 "工作排程器庫" → "建立基本工作"
- 名稱：CEO_Daily_Report
- 描述：每日自動執行投資報告

步驟 3: 設定觸發條件
- 選 "每天"
- 開始時間：09:00:00
- 每 1 天執行一次

步驟 4: 設定操作
- 選 "啟動程式"
- 程式：powershell.exe
- 引數：-NoProfile -Command "cd C:\Users\user\.qclaw\workspace; uv run --with yfinance --with requests --with beautifulsoup4 python scripts/daily_full_report_v2.py"

步驟 5: 完成設定
- 勾選 "開啟內容對話方塊"
- 點 "完成"

步驟 6: 進階設定
- 在 "一般" 頁籤，勾選 "無論使用者是否登入都要執行"
- 在 "條件" 頁籤，取消勾選 "只有在電腦使用交流電源時才啟動"
- 點 "確定"

方法二：Python schedule 套件 (替代方案)
========================================
""")

# 建立 schedule 腳本
schedule_script = '''# -*- coding: utf-8 -*-
"""
自動排程執行器 - 使用 schedule 套件
"""
import schedule
import time
import subprocess
from datetime import datetime

def run_daily_report():
    """執行每日報告"""
    print(f"[{datetime.now()}] 執行每日報告...")
    
    try:
        result = subprocess.run(
            ['uv', 'run', '--with', 'yfinance', '--with', 'requests', '--with', 'beautifulsoup4', 
             'python', 'scripts/daily_full_report_v2.py'],
            cwd='C:\\Users\\user\\.qclaw\\workspace',
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print(f"[{datetime.now()}] 報告執行成功！")
        else:
            print(f"[{datetime.now()}] 報告執行失敗：{result.stderr}")
            
    except Exception as e:
        print(f"[{datetime.now()}] 執行錯誤：{e}")

# 設定排程
schedule.every().day.at("09:00").do(run_daily_report)

print("自動排程已啟動！")
print("每日 09:00 自動執行投資報告")
print("按 Ctrl+C 停止")

# 持續執行
while True:
    schedule.run_pending()
    time.sleep(60)  # 每分鐘檢查一次
'''

with open('scripts/scheduler.py', 'w', encoding='utf-8') as f:
    f.write(schedule_script)

print("已建立 schedule 腳本: scripts/scheduler.py")
print("\n使用方法:")
print("  uv run --with schedule python scripts/scheduler.py")

print("\n" + "="*70)
print("建議")
print("="*70)
print("""
推薦使用「方法一：Windows 工作排程器」
- 不需要保持 Python 執行
- 系統層級排程，更穩定
- 開機自動啟動

設定完成後，系統會：
- 每日 9:00 自動執行報告
- 生成 daily_report.txt
- 你可以在 9:05 查看報告
""")

print("="*70)