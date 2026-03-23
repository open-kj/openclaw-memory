import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

candidates = {
    'sz300308': '中际旭创',
    'sz300502': '新易盛', 
    'sh688981': '中芯国际',
    'sz002049': '紫光国微',
    'sz300661': '圣邦股份',
    'sh688256': '寒武纪',
    'sz300474': '景嘉微',
    'sz002371': '北方华创',
    'sz300223': '北京君正',
    'sz300548': '博创科技',
}

results = {}
for code, name in candidates.items():
    url = f'https://qt.gtimg.cn/q={code}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 10:
                price = parts[3]
                prev_close = parts[4]
                pct = parts[32] if len(parts) > 32 else '0'
                high52 = parts[33] if len(parts) > 33 else '0'
                low52 = parts[34] if len(parts) > 34 else '0'
                vol = parts[36] if len(parts) > 36 else '0'
                results[code] = {
                    'name': name,
                    'price': float(price),
                    'prev_close': float(prev_close) if prev_close else 0,
                    'pct': float(pct),
                    'high52': float(high52) if high52 else 0,
                    'low52': float(low52) if low52 else 0,
                    'vol': vol,
                }
    except Exception as e:
        print(f"{name}({code}): FAIL {e}")

print("=== 候选标的筛选 ===")
print(f"{'名称':<10} {'代码':<12} {'现价':>8} {'今日涨幅':>8} {'距52周低':>10} {'距52周高':>10}")
print("-" * 60)

filtered = []
for code, r in results.items():
    if r['pct'] == 0 or r['low52'] == 0 or r['high52'] == 0:
        continue
    dist_low = (r['price'] - r['low52']) / r['low52'] * 100
    dist_high = (r['high52'] - r['price']) / r['price'] * 100
    r['dist_low'] = dist_low
    r['dist_high'] = dist_high
    # Filter: not fallen too much today, close to 52w low
    if r['pct'] > -8 and dist_low < 15:
        filtered.append(r)
    print(f"{r['name']:<10} {code:<12} {r['price']:>8.2f} {r['pct']:>+7.2f}% {dist_low:>+9.1f}% {dist_high:>+9.1f}%")

print(f"\n=== 符合建仓条件标的（今日跌幅<8% 且 距52周低点<15%）===")
for r in filtered:
    print(f"OK {r['name']}({r['price']:.2f}) 今日{r['pct']:+.2f}% 距52周低{r['dist_low']:+.1f}%")
