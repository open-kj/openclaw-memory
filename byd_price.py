import urllib.request

url = 'https://qt.gtimg.cn/q=sz002594'
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=5) as resp:
        data = resp.read().decode('gbk')
        parts = data.split('~')
        if len(parts) > 10:
            price = parts[3]
            prev_close = parts[4]
            pct = parts[32] if len(parts) > 32 else '0'
            print(f"BUY sz002594 at {price}")
except Exception as e:
    print(f"FAIL: {e}")
