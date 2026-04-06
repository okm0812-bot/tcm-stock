import urllib.request, os
url = 'https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/latest.tar.gz'
out = r'C:\Users\user\Downloads\skillhub_latest.tar.gz'
urllib.request.urlretrieve(url, out)
print('Done:', os.path.getsize(out))
