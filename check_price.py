import urllib.request
import json

stocks = ['sz300394', 'sh688521', 'sz002594']
results = {}
for s in stocks:
    url = f'https://qt.gtimg.cn/q={s}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = r.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 3:
                price = parts[3]
                name = parts[1]
                results[s] = {'name': name, 'price': float(price)}
                print(f'{name} {s}: {price}')
    except Exception as e:
        print(f'Error {s}: {e}')

# Check conditions
print('\n--- 监控结果 ---')
stop_loss = {'sz300394': 291.64, 'sh688521': 188.94, 'sz002594': 103.45}
buy_zone = {'sz300394': 305.00, 'sh688521': 195.00, 'sz002594': 105.00}
sell_zone = {'sz300394': 320.00, 'sh688521': 208.00, 'sz002594': 115.00}
warn_zone = {'sz300394': 300.00, 'sh688521': 192.00}

for code, info in results.items():
    p = info['price']
    name = info['name']
    print(f'{name}({code}): {p}')
    if p <= stop_loss[code]:
        print(f'  >>> 止损触发!')
    if p <= buy_zone[code]:
        print(f'  >>> 波段低吸预警!')
    if p >= sell_zone[code]:
        print(f'  >>> 波段高抛预警!')
    if code in warn_zone and p <= warn_zone[code]:
        print(f'  >>> 警示支撑位!')
