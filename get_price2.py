import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

stocks = [
    ('sz300394', '天孚通信'),
    ('sh688521', '芯原股份'),
    ('sz002594', '比亚迪'),
    ('sh688981', '中芯国际')
]

results = []
for code, name in stocks:
    url = f'https://qt.gtimg.cn/q={code}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 10:
                price = float(parts[3])
                close = float(parts[4])
                results.append((name, code, price, close))
    except Exception as e:
        print(f'{name} ERROR: {e}')

# Check alerts
check = [
    ('天孚通信', 'sz300394', 298.49, 291.64, 300.00, 305.00, 320.00),
    ('芯原股份', 'sh688521', 190.50, 188.94, 192.00, 195.00, 198.00),
    ('比亚迪', 'sz002594', 107.63, 103.45, 103.45, 105.00, 115.00),
    ('中芯国际', 'sh688981', 98.04, 93.14, 93.14, 95.00, 103.00),
]

for name, code, close, stop, support, low_buy, high_sell in check:
    price = None
    for n, c, p, cl in results:
        if c == code:
            price = p
            break
    if price is None:
        continue

    change = (price - close) / close * 100
    alerts = []

    if price <= stop:
        alerts.append(f'STOP_TRIGGER: {price}<={stop}')
    elif price <= support:
        alerts.append(f'SUPPORT: {price}<={support}')
    if price <= low_buy:
        alerts.append(f'LOWBUY: {price}<={low_buy}')
    if price >= high_sell:
        alerts.append(f'HIGHSELL: {price}>={high_sell}')

    status = ' '.join(alerts) if alerts else 'OK'
    print(f'{name} {price} ({change:+.2f}%) {status}')
