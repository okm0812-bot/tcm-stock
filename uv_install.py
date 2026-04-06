import subprocess, os, sys

base = r"C:\Users\user\AppData\Local\Temp\uv-work"
cache_dir = r"C:\Users\user\AppData\Local\Temp\uv-cache"
os.makedirs(cache_dir, exist_ok=True)
os.makedirs(base, exist_ok=True)

env = os.environ.copy()
env["UV_CACHE_DIR"] = cache_dir
env["UV_TOOL_DIR"] = base

r = subprocess.run(
    ["uv", "pip", "install",
     "--python", sys.executable,
     "--cache-dir", cache_dir,
     "yfinance", "requests", "beautifulsoup4"],
    capture_output=True, text=True, env=env
)
print("RC:", r.returncode)
print("OUT:", r.stdout[-2000:] if r.stdout else "")
print("ERR:", r.stderr[-2000:] if r.stderr else "")
