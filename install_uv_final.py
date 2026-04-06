import subprocess, os, sys

base = r"C:\Users\user\.qclaw\workspace"
cache_dir = os.path.join(base, "uv-cache")
tool_dir = os.path.join(base, "uv-tools")
os.makedirs(cache_dir, exist_ok=True)
os.makedirs(tool_dir, exist_ok=True)

env = os.environ.copy()
env["UV_CACHE_DIR"] = cache_dir
env["UV_TOOL_DIR"] = tool_dir

# Install packages
r = subprocess.run(
    ["uv", "pip", "install",
     "--python", sys.executable,
     "--cache-dir", cache_dir,
     "--target", os.path.join(base, "python-libs"),
     "yfinance", "requests", "beautifulsoup4"],
    capture_output=True, text=True, env=env
)
print("STDOUT:", r.stdout[-2000:] if r.stdout else "")
print("STDERR:", r.stderr[-2000:] if r.stderr else "")
print("RC:", r.returncode)
