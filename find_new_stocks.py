import requests
import json

print("=== 1. 新浪财经 - 今日涨幅榜（前30）===")
r = requests.get('https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple?page=1&num=30&sort=changepercent&asc=0&node=hs_a', timeout=10)
data = r.json()
strong = []
for item in data:
    try:
        chg = float(item.get('changepercent', 0))
        if chg > 5:
            strong.append({'name': item.get('name'), 'symbol': item.get('symbol'), 'chg': chg, 'price': item.get('trade')})
    except:
        pass
print(f"涨幅>5%的股票共{len(strong)}只:")
for s in sorted(strong, key=lambda x: x['chg'], reverse=True)[:15]:
    print(f"  {s['name']} | {s['symbol']} | +{s['chg']:.2f}% | 现价:{s['price']}")

print("\n=== 2. 东方财富 - 新股/次新股板块 ===")
# 东方财富次新股板块
r2 = requests.get('https://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=20&po=1&np=1&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:1+t:2,m:1+t:23&fields=f2,f3,f12,f14,f15,f16,f17', timeout=10)
if r2.status_code == 200:
    try:
        j = r2.json()
        items = j.get('data', {}).get('diff', [])
        print(f"热门板块股票共{len(items)}只:")
        for item in items[:15]:
            print(f"  {item.get('f14')} | {item.get('f12')} | {item.get('f3')}%")
    except Exception as e:
        print(f"解析失败: {e}, raw: {r2.text[:200]}")
else:
    print(f"请求失败: {r2.status_code}")

print("\n=== 3. 腾讯财经 - 获取涨幅榜 ===")
r3 = requests.get('https://qt.gtimg.cn/q=sh000001,sz399001,sz399006', timeout=10)
print("大盘指数:", r3.text[:200])
