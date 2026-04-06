# -*- coding: utf-8 -*-
"""
自動排程設定 - Windows Task Scheduler
"""
from datetime import datetime

output = []

def add(text):
    output.append(text)

add("="*70)
add("AUTO SCHEDULER SETUP GUIDE")
add("="*70)

add("\nGOAL: Auto-run daily report at 9:00 AM")

add("\nMethod 1: Windows Task Scheduler (Recommended)")
add("="*70)
add("Step 1: Open Task Scheduler")
add("  - Press Win + R, type: taskschd.msc")
add("  - Or search: Task Scheduler")

add("\nStep 2: Create Basic Task")
add("  - Right click 'Task Scheduler Library'")
add("  - Select 'Create Basic Task'")
add("  - Name: CEO_Daily_Report")
add("  - Description: Auto-run investment report daily")

add("\nStep 3: Set Trigger")
add("  - Select 'Daily'")
add("  - Start time: 09:00:00")
add("  - Recur every: 1 days")

add("\nStep 4: Set Action")
add("  - Select 'Start a program'")
add("  - Program: powershell.exe")
add("  - Arguments: -NoProfile -Command \"cd C:\\Users\\user\\.qclaw\\workspace; uv run --with yfinance --with requests --with beautifulsoup4 python scripts/daily_full_report_v2.py\"")

add("\nStep 5: Finish")
add("  - Check 'Open the Properties dialog'")
add("  - Click 'Finish'")

add("\nStep 6: Advanced Settings")
add("  - In 'General' tab, check 'Run whether user is logged on or not'")
add("  - In 'Conditions' tab, uncheck 'Start the task only if the computer is on AC power'")
add("  - Click 'OK'")

add("\n" + "="*70)
add("Method 2: Python Schedule (Alternative)")
add("="*70)

# Create scheduler script
scheduler_code = '''# Auto scheduler using schedule package
import schedule
import time
import subprocess
from datetime import datetime

def run_report():
    print(f"[{datetime.now()}] Running daily report...")
    try:
        result = subprocess.run(
            ['uv', 'run', '--with', 'yfinance', '--with', 'requests', '--with', 'beautifulsoup4', 
             'python', 'scripts/daily_full_report_v2.py'],
            cwd=r'C:\\Users\\user\\.qclaw\\workspace',
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            print(f"[{datetime.now()}] Success!")
        else:
            print(f"[{datetime.now()}] Failed: {result.stderr}")
    except Exception as e:
        print(f"[{datetime.now()}] Error: {e}")

schedule.every().day.at("09:00").do(run_report)

print("Scheduler started! Daily at 09:00")
print("Press Ctrl+C to stop")

while True:
    schedule.run_pending()
    time.sleep(60)
'''

with open('scripts/scheduler.py', 'w', encoding='utf-8') as f:
    f.write(scheduler_code)

add("\nCreated: scripts/scheduler.py")
add("Usage: uv run --with schedule python scripts/scheduler.py")

add("\n" + "="*70)
add("RECOMMENDATION")
add("="*70)
add("Use Method 1 (Windows Task Scheduler)")
add("- More stable, system-level scheduling")
add("- No need to keep Python running")
add("- Auto-start on boot")

add("\nAfter setup:")
add("- Report runs daily at 9:00 AM")
add("- Check daily_report.txt at 9:05 AM")
add("="*70)

# Write to file
with open('scheduler_setup_guide.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print('\n'.join(output))
print(f"\nGuide saved to: scheduler_setup_guide.txt")