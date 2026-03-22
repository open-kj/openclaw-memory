# -*- coding: utf-8 -*-
import urllib.request, ssl, json, sys

ssl._create_default_https_context = ssl._create_unverified_context

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

print("=" * 60)
print("多源数据交叉验证报告")
print("时间: 2026-03-22 13:42 (数据截止: 03-20收盘)")
print("=" * 60)

# ========== 腾讯财经 (主力) ==========
print("\n[数据源1: 腾讯财经 qt.gtimg.cn]")
print("-" * 50)
codes_tx = {
    'sz300223': '北京君正',
    'sz300394': '天孚通信',
    'sz300548': '长芯博创',
    'sh688521': '芯原股份',
    'sh000001': '上证指数',
    'sz399006': '创业板'
}
tx_results = {}
for code, name in codes_tx.items():
    try:
        url = 'https://qt.gtimg.cn/q=' + code
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as r:
            raw = r.read().decode('gbk', errors='replace')
            parts = raw.split('~')
            if len(parts) > 40:
                price = parts[3]
                prev = parts[4]
                openp = parts[5]
                high = parts[33]
                low = parts[34]
                chg = parts[31]
                pct = parts[32]
                vol = parts[36]
                amount = parts[37]
                pe = parts[39] if len(parts) > 39 else 'N/A'
                tx_results[name] = {
                    'price': price, 'prev': prev, 'open': openp,
                    'high': high, 'low': low, 'chg': chg,
                    'pct': pct, 'vol': vol, 'amount': amount, 'pe': pe
                }
                try:
                    pct_f = float(pct)
                    chg_f = float(chg)
                    sign = '+' if chg_f >= 0 else ''
                    print(f"  [{name}] price={price} chg={sign}{chg_f:.2f}({sign}{pct_f:.2f}%) PE={pe}")
                except:
                    print(f"  [{name}] price={price} chg={chg}({pct}%)")
    except Exception as e:
        print(f"  [{name}] ERROR: {str(e)[:50]}")

# ========== 东方财富 (备用) ==========
print("\n[数据源2: 东方财富 push2his.eastmoney.com]")
print("-" * 50)
codes_em_kline = {
    '0.300223': '北京君正',
    '0.300394': '天孚通信',
    '0.300548': '长芯博创',
    '1.688521': '芯原股份',
    '1.000001': '上证指数'
}
em_results = {}
for secid, name in codes_em_kline.items():
    try:
        url = 'https://push2his.eastmoney.com/api/qt/stock/kline/get?secid=' + secid + '&fields1=f1,f2,f3,f4,f5,f6&fields2=f51,f52,f53,f54,f55,f56,f57,f58&kltn=101&fqt=0&beg=20260320&end=20260320'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0', 'Referer': 'https://finance.eastmoney.com'})
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read())
            klines = data.get('data', {}).get('klines', [])
            if klines:
                k = klines[0].split(',')
                date, openp, close, high, low, vol, amount, chg_pct = k[0], k[1], k[2], k[3], k[4], k[5], k[6], k[8]
                em_results[name] = {'date': date, 'open': openp, 'close': close, 'high': high, 'low': low, 'pct': chg_pct}
                print(f"  [{name}] date={date} close={close} open={openp} high={high} low={low} chg={chg_pct}%")
            else:
                print(f"  [{name}] No kline data returned")
    except Exception as e:
        print(f"  [{name}] ERROR: {str(e)[:60]}")

# ========== 持仓汇总 ==========
print("\n" + "=" * 60)
print("持仓数据汇总")
print("=" * 60)
print(f"{'股票':<10} {'现价':>8} {'昨收':>8} {'涨跌幅':>10} {'PE':>8} {'距止损':>8}")
print("-" * 60)

# 持仓数据
holdings = {
    '天孚通信': {'price': '312.00', 'cost': 306.99, 'stop': 291.64, 'pe': '132.37'},
    '北京君正': {'price': '119.80', 'cost': 122.34, 'stop': 116.22, 'pe': '182.06'},
    '长芯博创': {'price': '146.13', 'cost': 148.57, 'stop': 141.14, 'pe': '149.74'},
    '芯原股份': {'price': '199.50', 'cost': 198.88, 'stop': 188.94, 'pe': '亏损'},
}

for name, d in holdings.items():
    if name in tx_results:
        tx = tx_results[name]
        price = tx['price']
        prev = tx['prev']
        pct = tx['pct']
        try:
            dist = (float(price) - d['stop']) / d['stop'] * 100
            dist_str = f"+{dist:.1f}%"
        except:
            dist_str = "N/A"
        print(f"{name:<10} {price:>8} {prev:>8} {pct:>9}% {d['pe']:>8} {dist_str:>8}")

print("-" * 60)
print("数据来源: 腾讯财经(qt.gtimg.cn) 03-20收盘")
print("=" * 60)
