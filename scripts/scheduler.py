# Auto scheduler using schedule package
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
            cwd=r'C:\Users\user\.qclaw\workspace',
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
