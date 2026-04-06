import subprocess, os

exe = r'C:\Users\user\Desktop\yt-dlp.exe'
print(f'File exists: {os.path.exists(exe)}')
print(f'File size: {os.path.getsize(exe) if os.path.exists(exe) else "N/A"}')

try:
    result = subprocess.run([exe, '--version'], capture_output=True, text=True, timeout=15)
    print(f'returncode: {result.returncode}')
    print(f'stdout: {result.stdout}')
    print(f'stderr: {result.stderr}')
except Exception as e:
    print(f'Error: {e}')
