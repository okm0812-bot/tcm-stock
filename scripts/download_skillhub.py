import urllib.request, os

url = 'https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/latest.tar.gz'
tmp = r'C:\Users\user\.qclaw\workspace\skillhub_latest.tar.gz'
print('Downloading...')
urllib.request.urlretrieve(url, tmp)
print(f'Downloaded: {os.path.getsize(tmp)} bytes')
print(f'Path: {tmp}')
