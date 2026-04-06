import urllib.request, os, sys

url = 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe'
# 嘗試寫到 Python Scripts 目錄
out = r'C:\Python314\Scripts\yt-dlp.exe'
print(f'Downloading to {out}...')
try:
    urllib.request.urlretrieve(url, out)
    print(f'Done: {os.path.getsize(out)} bytes')
except Exception as e:
    print(f'Failed: {e}')
    # 嘗試寫到 Python 根目錄
    out2 = r'C:\Python314\yt-dlp.exe'
    print(f'Trying {out2}...')
    urllib.request.urlretrieve(url, out2)
    print(f'Done: {os.path.getsize(out2)} bytes')
