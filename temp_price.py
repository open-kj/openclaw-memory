import urllib.request

stocks = ['sz300394', 'sh688521']
prices = {}
for s in stocks:
    url = f'https://qt.gtimg.cn/q={s}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = r.read().decode('gbk')
            parts = data.split('=')
            if len(parts) > 1:
                quoted = parts[1].strip().strip('"')
                fields = quoted.split('~')
                name = fields[1]
                price = fields[3]
                change_pct = fields[32]
                prices[s] = {'name': name, 'price': float(price), 'change_pct': float(change_pct)}
    except Exception as e:
        prices[s] = {'error': str(e)}

# 止损线
stop_loss = {'sz300394': 291.64, 'sh688521': 188.94}
bands = {
    'sz300394': {'low_buy': 305.00, 'high_sell': 320.00, 'support': 300.00},
    'sh688521': {'low_buy': 195.00, 'high_sell': 208.00, 'support': 192.00}
}

alerts = []
for s, d in prices.items():
    if 'error' in d:
        continue
    p = d['price']
    sl = stop_loss[s]
    b = bands[s]
    name = d['name']
    
    if p <= sl:
        alerts.append(f"!!STOP_LOSS!! {name}({s}) 现价{p} <= 止损线{sl}")
    elif p <= b['support']:
        alerts.append(f"!!SUPPORT!! {name}({s}) 现价{p} <= 支撑位{b['support']}，暂停加仓")
    elif p <= b['low_buy']:
        alerts.append(f"!!LOW_BUY!! {name}({s}) 现价{p} <= 波段低吸{b['low_buy']}，建议加仓2万")
    elif p >= b['high_sell']:
        alerts.append(f"!!HIGH_SELL!! {name}({s}) 现价{p} >= 波段高抛{b['high_sell']}，建议减仓")
    else:
        margin = p - sl
        pct = (p - sl) / sl * 100
        alerts.append(f"OK {name}({s}) 现价{p} 距止损{margin:.2f}({pct:.1f}%) 安全")

for a in alerts:
    print(a)
