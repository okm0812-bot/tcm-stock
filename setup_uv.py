import subprocess, os, sys

os.environ["UV_CACHE_DIR"] = r"C:\Users\user\.qclaw\uv-cache"
os.environ["UV_TOOL_DIR"] = r"C:\Users\user\.qclaw\uv-tools"

result = subprocess.run(
    [sys.executable, "-m", "pip", "install",
     "yfinance", "requests", "beautifulsoup4"],
    capture_output=True, text=True
)
print("pip install:", result.returncode)
print(result.stdout[-500:] if result.stdout else "")
print(result.stderr[-500:] if result.stderr else "")

result2 = subprocess.run(
    ["uv", "pip", "install",
     "--target", r"C:\Users\user\.qclaw\workspace\python-libs",
     "yfinance", "requests"],
    capture_output=True, text=True,
    env={**os.environ}
)
print("uv pip install:", result2.returncode)
print(result2.stdout[-1000:] if result2.stdout else "")
print(result2.stderr[-1000:] if result2.stderr else "")
