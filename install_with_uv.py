import subprocess, os, sys

# Set writable cache/tool dirs
os.makedirs(r"C:\Users\user\.qclaw\uv-cache", exist_ok=True)
os.makedirs(r"C:\Users\user\.qclaw\uv-tools", exist_ok=True)

env = os.environ.copy()
env["UV_CACHE_DIR"] = r"C:\Users\user\.qclaw\uv-cache"
env["UV_TOOL_DIR"] = r"C:\Users\user\.qclaw\uv-tools"
env["UV_PYTHON"] = sys.executable

# Try installing packages via uv pip
r = subprocess.run(
    ["uv", "pip", "install", "yfinance", "requests", "beautifulsoup4",
     "--python", sys.executable,
     "--cache-dir", r"C:\Users\user\.qclaw\uv-cache"],
    capture_output=True, text=True, env=env
)
print("STDOUT:", r.stdout[-2000:] if r.stdout else "")
print("STDERR:", r.stderr[-2000:] if r.stderr else "")
print("RC:", r.returncode)
