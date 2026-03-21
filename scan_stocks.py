import requests
import json

r = requests.get('https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple?page=1&num=50&sort=changepercent&asc=0&node=hs_a', timeout=10)
data = r.json()

print("=== 今日强势股（涨幅>5%，近期上市科技/IT/化工/军工类）===")
results = []
for item in data:
    try:
        chg = float(item.get('changepercent', 0))
        sym = str(item.get('symbol', ''))
        name = str(item.get('name', ''))
        price = str(item.get('trade', ''))
        is_new = sym.startswith('sh688') or sym.startswith('sz301') or sym.startswith('sz300827') or sym.startswith('sz301658')
        if chg > 5 and is_new:
            results.append({'name': name, 'symbol': sym, 'chg': chg, 'price': price})
    except:
        pass

results.sort(key=lambda x: x['chg'], reverse=True)
for i, s in enumerate(results[:15]):
    print(f"{i+1}. {s['name']} | {s['symbol']} | +{s['chg']:.2f}% | 现价:{s['price']}")

print()
print("=== 涨幅>8%的近期上市股票（全部）===")
for item in data:
    try:
        chg = float(item.get('changepercent', 0))
        sym = str(item.get('symbol', ''))
        name = str(item.get('name', ''))
        price = str(item.get('trade', ''))
        if chg > 8 and (sym.startswith('sh688') or sym.startswith('sz301') or sym.startswith('sz300827') or sym.startswith('sz301658')):
            print(f"  {sym} | {name} | +{chg:.2f}% | {price}")
    except:
        pass

print()
print("=== 所有688/301开头的近期强势股 ===")
for item in data:
    try:
        chg = float(item.get('changepercent', 0))
        sym = str(item.get('symbol', ''))
        name = str(item.get('name', ''))
        price = str(item.get('trade', ''))
        if (sym.startswith('sh688') or sym.startswith('sz301')) and chg > 2:
            print(f"  {sym} | {name} | +{chg:.2f}% | {price}")
    except:
        pass
