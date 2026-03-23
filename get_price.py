import urllib.request
import sys
sys.stdout.reconfigure(encoding='utf-8')

stocks = ['sz300394', 'sh688521', 'sz002594']
names = {'sz300394': '天孚通信', 'sh688521': '芯原股份', 'sz002594': '比亚迪'}
stops = {'sz300394': 291.64, 'sh688521': 188.94, 'sz002594': 103.45}
costs = {'sz300394': 306.99, 'sh688521': 198.88, 'sz002594': 108.89}
qtys = {'sz300394': 618, 'sh688521': 1000, 'sz002594': 3200}

print("=== 持仓实时 ===")
for code in stocks:
    url = f'https://qt.gtimg.cn/q={code}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 10:
                price = float(parts[3])
                pct = float(parts[32]) if parts[32] else 0
                stop = stops[code]
                dist = (price - stop) / stop * 100
                print(f"{names[code]}: {price} ({pct:+.2f}%) 距止损{dist:+.1f}%")
    except:
        pass
