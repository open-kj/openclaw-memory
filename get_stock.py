# -*- coding: gbk -*-
import urllib.request
import sys

url = 'https://qt.gtimg.cn/q=sz300394,sz300223,sz300548,sh688521'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req, timeout=10)
data = resp.read().decode('gbk')
print(data)
