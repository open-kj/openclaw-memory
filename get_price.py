# -*- coding: utf-8 -*-
import urllib.request
import sys

stocks = ['sz300394', 'sh688521', 'sz002594', 'sh688981']
url = 'https://qt.gtimg.cn/q=' + ','.join(stocks)
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=10)
data = resp.read().decode('gbk')

lines = data.strip().split('\n')
results = []
for line in lines:
    if '=' not in line:
        continue
    parts = line.split('~')
    if len(parts) > 10:
        code = parts[0].split('_')[1] if '_' in parts[0] else parts[0]
        name = parts[1]
        price = float(parts[3])
        yesterday_close = float(parts[4])
        change = (price - yesterday_close) / yesterday_close * 100
        results.append(f'{code}|{name}|{price:.2f}|{yesterday_close:.2f}|{change:+.2f}%')

sys.stdout.reconfigure(encoding='utf-8')
for r in results:
    print(r)
