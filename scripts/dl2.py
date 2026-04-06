import urllib.request, os

url = 'https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/install/latest.tar.gz'
out = r'C:\Users\user\.qclaw\workspace\skillhub_test.txt'
try:
    urllib.request.urlretrieve(url, out)
    print('Done:', os.path.getsize(out))
except Exception as e:
    print('Error:', e)
    # Try alternative: use request with headers
    req = urllib.request.Request(url, headers={'User-Agent': 'curl/8.0'})
    with urllib.request.urlopen(req) as resp, open(out, 'wb') as f:
        shutil.copyfileobj(resp, f)
    print('Done via alt method:', os.path.getsize(out))
