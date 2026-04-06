import subprocess, os, sys

os.environ["UV_CACHE_DIR"] = r"C:\Temp\uv-cache"
os.environ["TEMP"] = r"C:\Temp"
os.environ["TMP"] = r"C:\Temp"
os.environ["PYTHONIOENCODING"] = "utf-8"

result = subprocess.run(
    ["uv", "run",
     r"C:\Users\user\.qclaw\workspace\skills\stock-analysis\scripts\analyze_stock.py",
     "2330.TW", "--output", "text"],
    capture_output=True, text=True, encoding="utf-8", errors="ignore", env=os.environ
)
print("RC:", result.returncode)
print("OUT:", result.stdout[-3000:] if result.stdout else "")
print("ERR:", result.stderr[-3000:] if result.stderr else "")
