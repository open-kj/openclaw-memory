"""
选股扫描器 - 必涨筛选 v2
"""
import urllib.request
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 52只候选池
CODES = [
    'sz300394', 'sz300308', 'sz300502', 'sh688027', 'sz300570',
    'sh688521', 'sh688256', 'sh688981', 'sz002371', 'sz002049', 'sh688396', 'sz300661', 'sh688008',
    'sz002594', 'sh986633', 'sh986803', 'sh987033', 'sh601127',
    'sz300014', 'sz002812', 'sz300207', 'sh688005',
    'sz002920', 'sh688638', 'sz002536', 'sh688220', 'sz300496',
    'sz002230', 'sh688111', 'sz300033', 'sh688318', 'sz300624',
    'sz002475', 'sz002241', 'sh601138', 'sz002600', 'sh603986',
    'sz300760', 'sh688278', 'sz002007', 'sh688180', 'sz300529',
    'sz002025', 'sh600893', 'sz002013', 'sz300719',
    'sh600519', 'sz000858', 'sh603288', 'sz002714',
    'sz002555', 'sh603444', 'sz300418',
]

NAME = {
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

SECTOR = {
    'sz300394': '光模块', 'sz300308': '光模块', 'sz300502': '光模块', 'sh688027': '光模块', 'sz300570': '光模块',
    'sh688521': '半导体', 'sh688256': 'AI芯片', 'sh688981': '半导体', 'sz002371': '半导体设备', 'sz002049': '半导体', 'sh688396': '半导体', 'sz300661': '模拟芯片', 'sh688008': '半导体',
    'sz002594': '新能源整车', 'sh986633': '新能源整车', 'sh986803': '新能源整车', 'sh987033': '新能源整车', 'sh601127': '新能源整车',
    'sz300014': '锂电', 'sz002812': '锂电', 'sz300207': '锂电', 'sh688005': '锂电正极',
    'sz002920': '智能驾驶', 'sh688638': '智能驾驶', 'sz002536': '汽车零部件', 'sh688220': 'AI芯片', 'sz300496': 'AI软件',
    'sz002230': 'AI软件', 'sh688111': 'AI软件', 'sz300033': '金融科技', 'sh688318': '金融科技', 'sz300624': 'AI软件',
    'sz002475': '消费电子', 'sz002241': '消费电子', 'sh601138': '消费电子', 'sz002600': '消费电子', 'sh603986': '半导体',
    'sz300760': '医疗器械', 'sh688278': '生物医药', 'sz002007': '生物医药', 'sh688180': '生物医药', 'sz300529': '医疗器械',
    'sz002025': '军工', 'sh600893': '军工', 'sz002013': '军工', 'sz300719': '军工',
    'sh600519': '白酒', 'sz000858': '白酒', 'sh603288': '食品', 'sz002714': '农业',
    'sz002555': '游戏', 'sh603444': '游戏', 'sz300418': 'AI应用',
}

def fetch(code):
    url = f'https://qt.gtimg.cn/q={code}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 34:
                return {
                    'price': float(parts[3]),
                    'pct': float(parts[32]),
                    'high': float(parts[33]),
                    'low': float(parts[34]),
                    'vol': float(parts[36]),
                }
    except:
        pass
    return None

def score(r, sector, sector_data):
    if not r:
        return -999
    score = 0
    # 今日涨幅
    if r['pct'] > 3: score += 40
    elif r['pct'] > 1: score += 30
    elif r['pct'] > 0: score += 20
    elif r['pct'] > -2: score += 5
    else: score -= 20
    # 板块效应
    if sector_data['count'] >= 3 and sector_data['avg'] > 0:
        score += 30
    elif sector_data['count'] >= 3 and sector_data['avg'] > -2:
        score += 15
    # 距低点近（安全边际）
    if r['low'] > 0:
        dist_low = (r['price'] - r['low']) / r['low'] * 100
        if dist_low < 5: score += 20
        elif dist_low < 10: score += 10
    return score

results = {}
for code in CODES:
    r = fetch(code)
    if r:
        results[code] = r

# 板块统计
sector_stats = {}
for code, r in results.items():
    s = SECTOR.get(code, '其他')
    if s not in sector_stats:
        sector_stats[s] = {'total': 0, 'count': 0}
    sector_stats[s]['total'] += r['pct']
    sector_stats[s]['count'] += 1

for s in sector_stats:
    cnt = sector_stats[s]['count']
    if cnt > 0:
        sector_stats[s]['avg'] = sector_stats[s]['total'] / cnt

print("=" * 55)
print("选股扫描器 - 必涨筛选 v2")
print("=" * 55)
print(f"\n成功获取: {len(results)}/{len(CODES)} 只\n")

print("板块今日平均涨幅:")
for s, d in sorted(sector_stats.items(), key=lambda x: x[1]['avg'], reverse=True):
    print(f"  {s}: {d['avg']:+.2f}% ({d['count']}只)")

# 评分
candidates = []
for code, r in results.items():
    if r['pct'] <= -8:
        continue
    sector = SECTOR.get(code, '其他')
    sd = sector_stats.get(sector, {'count': 0, 'avg': 0})
    sc = score(r, sector, sd)
    candidates.append({
        'code': code,
        'name': NAME.get(code, code),
        'sector': sector,
        'price': r['price'],
        'pct': r['pct'],
        'score': sc,
    })

candidates.sort(key=lambda x: x['score'], reverse=True)

print("\n" + "=" * 55)
print("【明日重点关注 TOP 5】")
print("=" * 55)

for i, c in enumerate(candidates[:5], 1):
    tag = ">>>" if i <= 3 else ""
    print(f"\n{i}. {c['name']} ({c['code']}) {tag}")
    print(f"   板块: {c['sector']}")
    print(f"   现价: {c['price']:.2f}")
    print(f"   今日: {c['pct']:+.2f}%")
    print(f"   评分: {c['score']}分")

print("\n" + "=" * 55)
print("【操作计划】")
print("=" * 55)
print("明日开盘买入前三只，每只仓位15-20%，总仓位不超过60%")
print("止损：跌破买入价-5%立即止损")
print("不幻想，不抗单，到止损线就卖")
