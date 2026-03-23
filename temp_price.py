import urllib.request
import json
import sys

stocks = ['sz300394', 'sz300223', 'sz300548', 'sh688521']
names = {'sz300394':'天孚通信','sz300223':'北京君正','sz300548':'博创科技','sh688521':'芯原股份'}
stop_loss = {'sz300394':291.64,'sz300223':116.22,'sz300548':141.14,'sh688521':188.94}
warnings = {
    'sz300394':{'low_warn':305,'high_warn':320,'support':300},
    'sz300223':{'warn':118,'stop':116.22},
    'sz300548':{'warn':143,'stop':141.14},
    'sh688521':{'low_warn':195,'high_warn':208,'support':192}
}

results = []
alerts = []

for s in stocks:
    url = f'https://qt.gtimg.cn/q={s}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = r.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 3:
                price = float(parts[3])
                pct = parts[32] if len(parts)>32 else '0'
                results.append({'code':s,'name':names[s],'price':price,'pct':pct,'stop':stop_loss[s],'warn':warnings[s]})
    except Exception as e:
        results.append({'code':s,'name':names[s],'error':str(e)})

for r in results:
    if 'error' in r:
        print(f"{r['name']} {r['code']}: ERROR - {r['error']}")
    else:
        print(f"{r['name']} {r['code']}: 现价={r['price']} 涨跌幅={r['pct']}%")
        stop_dist = (r['price']-r['stop'])/r['stop']*100
        print(f"  止损线={r['stop']} 现价距止损={stop_dist:.1f}%")
        w = r['warn']
        if 'low_warn' in w:
            if r['price'] <= w['low_warn']:
                msg = f"  *** 波段低吸预警! 现价<=低吸线{w['low_warn']}"
                print(msg)
                alerts.append(f"{r['name']}波段低吸预警: 现价{r['price']}<=低吸线{w['low_warn']}")
            if r['price'] >= w['high_warn']:
                msg = f"  *** 波段高抛预警! 现价>=高抛线{w['high_warn']}"
                print(msg)
                alerts.append(f"{r['name']}波段高抛预警: 现价{r['price']}>=高抛线{w['high_warn']}")
            if r['price'] <= w['support']:
                msg = f"  *** 支撑位警示! 现价<=支撑{w['support']}"
                print(msg)
                alerts.append(f"{r['name']}支撑位警示: 现价{r['price']}<=支撑{w['support']}")
        if 'warn' in w:
            if r['price'] <= w['warn']:
                msg = f"  *** 预警! 现价<=预警线{w['warn']}"
                print(msg)
                alerts.append(f"{r['name']}预警: 现价{r['price']}<=预警线{w['warn']}")
        if r['price'] <= r['stop']:
            msg = f"  ==== 止损触发! 现价<=止损线{r['stop']} ===="
            print(msg)
            alerts.append(f"{r['name']}止损触发! 现价{r['price']}<=止损线{r['stop']}")
        print()

if alerts:
    print("=== ALERTS ===")
    for a in alerts:
        print(a)
else:
    print("=== 无触发条件 ===")
