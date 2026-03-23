import urllib.request
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 52只候选池
POOL = [
    # 光模块/AI算力
    'sz300394', 'sz300308', 'sz300502', 'sh688027', 'sz300570',
    # 半导体/IP
    'sh688521', 'sh688256', 'sh688981', 'sz002371', 'sz002049', 'sh688396', 'sz300661', 'sh688008',
    # 新能源整车
    'sz002594', 'sh986633', 'sh986803', 'sh987033', 'sh601127',
    # 锂电/电池
    'sz300014', 'sz002812', 'sz300207', 'sh688005',
    # 智能驾驶
    'sz002920', 'sh688638', 'sz002536', 'sh688220', 'sz300496',
    # AI应用
    'sz002230', 'sh688111', 'sz300033', 'sh688318', 'sz300624',
    # 消费电子
    'sz002475', 'sz002241', 'sh601138', 'sz002600', 'sh603986',
    # 医药/医疗
    'sz300760', 'sh688278', 'sz002007', 'sh688180', 'sz300529',
    # 军工/航天
    'sz002025', 'sh600893', 'sz002013', 'sz300719', 'sz002049',
    # 食品饮料
    'sh600519', 'sz000858', 'sh603288', 'sz002714',
    # 游戏/传媒
    'sz002555', 'sh603444', 'sz300418',
]

NAME_MAP = {
    'sz300394': '天孚通信', 'sz300308': '中际旭创', 'sz300502': '新易盛',
    'sh688027': '德科立', 'sz300570': '太辰光',
    'sh688521': '芯原股份', 'sh688256': '寒武纪', 'sh688981': '中芯国际',
    'sz002371': '北方华创', 'sz002049': '紫光国微', 'sh688396': '华润微',
    'sz300661': '圣邦股份', 'sh688008': '澜起科技',
    'sz002594': '比亚迪', 'sh986633': '理想汽车', 'sh986803': '蔚来',
    'sh987033': '小鹏汽车', 'sh601127': '赛力斯',
    'sz300014': '亿纬锂能', 'sz002812': '恩捷股份', 'sz300207': '欣旺达',
    'sh688005': '容百科技',
    'sz002920': '德赛西威', 'sh688638': '威迈斯', 'sz002536': '飞龙股份',
    'sh688220': '翱捷科技', 'sz300496': '中科创达',
    'sz002230': '科大讯飞', 'sh688111': '金山办公', 'sz300033': '同花顺',
    'sh688318': '财富趋势', 'sz300624': '东方国信',
    'sz002475': '立讯精密', 'sz002241': '歌尔股份', 'sh601138': '工业富联',
    'sz002600': '领益智造', 'sh603986': '兆易创新',
    'sz300760': '迈瑞医疗', 'sh688278': '特宝生物', 'sz002007': '华兰生物',
    'sh688180': '君实生物', 'sz300529': '健帆生物',
    'sz002025': '航天电器', 'sh600893': '航发动力', 'sz002013': '中航机电',
    'sz300719': '安达维尔',
    'sh600519': '贵州茅台', 'sz000858': '五粮液', 'sh603288': '海天味业',
    'sz002714': '牧原股份',
    'sz002555': '三七互娱', 'sh603444': '吉比特', 'sz300418': '昆仑万维',
}

results = []
print(f"获取{len(POOL)}只股票数据...")
for code in POOL:
    url = f'https://qt.gtimg.cn/q={code}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = resp.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 10:
                price = float(parts[3])
                prev_close = float(parts[4]) if parts[4] else price
                pct = float(parts[32]) if parts[32] else 0
                high52 = float(parts[33]) if parts[33] else price
                low52 = float(parts[34]) if parts[34] else price
                vol = float(parts[36]) if parts[36] else 0
                name = NAME_MAP.get(code, code)
                
                # 计算距52周高低
                dist_low = (price - low52) / low52 * 100 if low52 else 999
                dist_high = (high52 - price) / price * 100 if price else 999
                
                results.append({
                    'code': code,
                    'name': name,
                    'price': price,
                    'pct': pct,
                    'dist_low': dist_low,
                    'dist_high': dist_high,
                    'vol': vol,
                    'valid': True
                })
    except Exception as e:
        name = NAME_MAP.get(code, code)
        print(f"  {name}({code}): 失败 {e}")

print(f"\n成功获取{sum(1 for r in results if r['valid'])}只")

# 筛选：今日跌幅<8%，距52周低<15%，成交量>10万
print("\n=== 筛选：今日跌幅<8% + 距52周低<15% + 成交量>10万 ===")
passed = []
for r in results:
    if not r['valid']:
        continue
    if r['pct'] < -8:
        continue
    if r['dist_low'] > 15:
        continue
    if r['vol'] < 100000:
        continue
    passed.append(r)

print(f"\n符合条件: {len(passed)}只")

# 按今日涨幅排序
passed.sort(key=lambda x: x['pct'], reverse=True)

print(f"\n{'名称':<10} {'代码':<12} {'现价':>8} {'今日涨幅':>8} {'距52周低':>10} {'距52周高':>10}")
print("-" * 60)
for r in passed[:20]:
    print(f"{r['name']:<10} {r['code']:<12} {r['price']:>8.2f} {r['pct']:>+7.2f}% {r['dist_low']:>+9.1f}% {r['dist_high']:>+9.1f}%")

# 不符合条件
print(f"\n=== 不符合条件({len(results)-len(passed)}只) ===")
for r in results:
    if not r['valid']:
        continue
    if r in passed:
        continue
    reasons = []
    if r['pct'] <= -8:
        reasons.append(f"跌幅超8%({r['pct']:.1f}%)")
    if r['dist_low'] > 15:
        reasons.append(f"距52周低超15%({r['dist_low']:.1f}%)")
    if r['vol'] < 100000:
        reasons.append("成交量不足")
    print(f"  {r['name']}: {', '.join(reasons)}")
