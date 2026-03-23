import urllib.request

stocks = {
    'sz300394': '天孚通信',
    'sh688521': '芯原股份'
}

results = {}
for code, name in stocks.items():
    url = f'https://qt.gtimg.cn/q={code}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 10:
                price = parts[3]
                pct = parts[32] if len(parts) > 32 else '0'
                results[code] = {'name': name, 'price': price, 'pct': pct}
                print(f'{name} {code}: 现价={price}, 涨跌幅={pct}%')
    except Exception as e:
        print(f'{name} {code}: 获取失败 {e}')

positions = {
    'sz300394': {'qty': 618, 'cost': 306.99, 'stop': 291.64},
    'sh688521': {'qty': 1000, 'cost': 198.88, 'stop': 188.94}
}

print('\n=== 持仓明细 ===')
total_value = 0
total_cost = 0
for code, pos in positions.items():
    if code in results:
        price = float(results[code]['price'])
        cost = pos['cost']
        qty = pos['qty']
        stop = pos['stop']
        value = price * qty
        cost_total = cost * qty
        pnl = value - cost_total
        pct = (price - cost) / cost * 100
        dist = (price - stop) / stop * 100
        total_value += value
        total_cost += cost_total
        print(f"{results[code]['name']}: 数量={qty}, 成本={cost}, 现价={price}, 市值={value:.0f}, 盈亏={pnl:.0f}({pct:+.2f}%), 止损={stop}, 距止损={dist:+.1f}%")

print(f'\n持仓总市值: {total_value:.0f}')
print(f'持仓总成本: {total_cost:.0f}')
print(f'持仓总盈亏: {total_value-total_cost:.0f}')
print(f'现金: ~609,443')
print(f'总资产: ~{total_value+609443:.0f}')
print(f'起始资金: 1,000,000')
print(f'累计盈亏: ~{total_value+609443-1000000:.0f}')
