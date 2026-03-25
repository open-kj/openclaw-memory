# -*- coding: utf-8 -*-
import urllib.request
import json

stocks = [('sz300394','天孚通信'),('sh688521','芯原股份'),('sz002594','比亚迪'),('sh688981','中芯国际')]
results = []
for code, name in stocks:
    try:
        url = 'https://qt.gtimg.cn/q=' + code
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 3:
                price = float(parts[3])
                results.append({"name": name, "code": code, "price": price})
                print(f"{name}|{code}|{price:.2f}")
            else:
                results.append({"name": name, "code": code, "price": None, "error": "parse_error"})
                print(f"{name}|{code}|PARSE_ERROR")
    except Exception as e:
        results.append({"name": name, "code": code, "price": None, "error": str(e)})
        print(f"{name}|{code}|ERROR|{e}")
