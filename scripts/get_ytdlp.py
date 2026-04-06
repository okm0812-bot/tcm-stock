import urllib.request, os

url = 'https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe'
out = r'C:\Users\user\.qclaw\workspace\scripts\yt-dlp.exe'
print('Downloading yt-dlp.exe...')
urllib.request.urlretrieve(url, out)
print(f'Done: {os.path.getsize(out)} bytes')
