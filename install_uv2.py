import subprocess, sys, os

os.environ["TMP"] = r"C:\Users\user\AppData\Local\Temp"
os.environ["TEMP"] = r"C:\Users\user\AppData\Local\Temp"

result = subprocess.run(
    [sys.executable, "-m", "pip", "install", "uv",
     "--user", "--no-warn-script-location"],
    env={**os.environ},
    capture_output=True, text=True
)
print("STDOUT:", result.stdout[-2000:] if result.stdout else "(empty)")
print("STDERR:", result.stderr[-2000:] if result.stderr else "(empty)")
print("RC:", result.returncode)
