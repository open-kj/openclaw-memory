import urllib.request
import json

stocks = {
    'sz300394': '天孚通信',
    'sh688521': '芯原股份',
    'sz002594': '比亚迪',
    'sh688981': '中芯国际'
}

results = []
for code, name in stocks.items():
    url = f'https://qt.gtimg.cn/q={code}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 3:
                price = float(parts[3])
                change_pct = parts[32] if len(parts) > 32 else 'N/A'
                results.append(f"{name} {code}: {price} ({change_pct}%)")
            else:
                results.append(f"{name} {code}: PARSE_ERROR")
    except Exception as e:
        results.append(f"{name} {code}: ERROR {e}")

for r in results:
    print(r)
