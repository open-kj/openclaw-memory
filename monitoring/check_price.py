import urllib.request
import json

stocks = ['sz300394', 'sh688521', 'sz002594']
stop_loss = {
    'sz300394': {'stop': 291.64, 'low_buy': 305.00, 'high_sell': 320.00, 'warn': 300.00},
    'sh688521': {'stop': 188.94, 'low_buy': 195.00, 'high_sell': 208.00, 'warn': 192.00},
    'sz002594': {'stop': 103.45, 'low_buy': 105.00, 'high_sell': 115.00}
}
results = {}

for s in stocks:
    try:
        url = f'https://qt.gtimg.cn/q={s}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = r.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 4:
                name = parts[1]
                price = float(parts[3])
                yesterday_close = float(parts[4])
                change_pct = round((price - yesterday_close) / yesterday_close * 100, 2)
                results[s] = {'name': name, 'price': price, 'change_pct': change_pct}
            else:
                results[s] = {'error': 'data format error'}
    except Exception as e:
        results[s] = {'error': str(e)}

print(json.dumps(results, ensure_ascii=False))

# Check triggers
alerts = []
for s, info in results.items():
    if 'error' in info or 'price' not in info:
        continue
    p = info['price']
    sl = stop_loss[s]
    if p <= sl['stop']:
        alerts.append(f"🚨 止损触发！{info['name']}现价{p}，低于止损线{sl['stop']}")
    elif 'warn' in sl and p <= sl['warn']:
        alerts.append(f"⚠️ 支撑位警示！{info['name']}现价{p}，跌至支撑位{sl['warn']}，暂停加仓")
    elif p <= sl['low_buy']:
        alerts.append(f"🟡 波段低吸预警！{info['name']}现价{p}，建议加仓2万（低吸线{sl['low_buy']}）")
    elif p >= sl['high_sell']:
        alerts.append(f"🟡 波段高抛预警！{info['name']}现价{p}，建议减仓（高抛线{sl['high_sell']}）")

if alerts:
    print("ALERTS:")
    for a in alerts:
        print(a)
else:
    print("ALERTS: none")
