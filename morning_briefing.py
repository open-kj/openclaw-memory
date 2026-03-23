"""
明日盘前分析生成器
每日08:00前自动推送
自动完成：候选池扫描 -> 强势板块 -> 重点关注 -> 操作计划
"""
import urllib.request
import sys
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

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

POSITIONS = {
    'sz300394': {'qty': 618, 'cost': 306.99, 'stop': 291.64},
    'sh688521': {'qty': 1000, 'cost': 198.88, 'stop': 188.94},
    'sz002594': {'qty': 3200, 'cost': 108.89, 'stop': 103.45},
}

def fetch(code):
    url = f'https://qt.gtimg.cn/q={code}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 34:
                price = float(parts[3])
                pct = float(parts[32]) if parts[32] else 0
                high52 = float(parts[33]) if parts[33] else price
                low52 = float(parts[34]) if parts[34] else price
                vol = float(parts[36]) if parts[36] else 0
                return {'price': price, 'pct': pct, 'high52': high52, 'low52': low52, 'vol': vol}
    except:
        pass
    return None

def get_account_status():
    total_value = 0
    total_cost = 0
    position_details = []
    for code, cfg in POSITIONS.items():
        r = fetch(code)
        if r:
            value = r['price'] * cfg['qty']
            cost_total = cfg['cost'] * cfg['qty']
            pnl = value - cost_total
            total_value += value
            total_cost += cost_total
            position_details.append({
                'name': NAME.get(code, code),
                'code': code,
                'price': r['price'],
                'cost': cfg['cost'],
                'qty': cfg['qty'],
                'value': value,
                'pnl': pnl,
                'stop': cfg['stop'],
                'dist_stop': (r['price'] - cfg['stop']) / cfg['stop'] * 100,
            })
    cash = 260995
    total = total_value + cash
    start = 1000000
    return {
        'total_value': total_value,
        'cash': cash,
        'total': total,
        'pnl': total - start,
        'pnl_pct': (total - start) / start * 100,
        'positions': position_details,
    }

def scan_candidates():
    results = {}
    for code in CODES:
        r = fetch(code)
        if r:
            results[code] = r
    sector_stats = {}
    for code, r in results.items():
        s = SECTOR.get(code, '其他')
        if s not in sector_stats:
            sector_stats[s] = {'total': 0, 'count': 0}
        sector_stats[s]['total'] += r['pct']
        sector_stats[s]['count'] += 1
    for s in sector_stats:
        cnt = sector_stats[s]['count']
        sector_stats[s]['avg'] = sector_stats[s]['total'] / cnt if cnt > 0 else 0
    candidates = []
    for code, r in results.items():
        if r['pct'] <= -8 or r['pct'] == 0:
            continue
        if r['low52'] > 0:
            dist_low = (r['price'] - r['low52']) / r['low52'] * 100
            if dist_low > 15:
                continue
        sector = SECTOR.get(code, '其他')
        sd = sector_stats.get(sector, {'avg': 0, 'count': 0})
        score = 0
        if r['pct'] > 3: score += 40
        elif r['pct'] > 1: score += 30
        elif r['pct'] > 0: score += 20
        elif r['pct'] > -2: score += 5
        else: score -= 20
        if sd['count'] >= 3 and sd['avg'] > 0: score += 30
        elif sd['count'] >= 3 and sd['avg'] > -2: score += 15
        if r['low52'] > 0:
            dist_low = (r['price'] - r['low52']) / r['low52'] * 100
            if dist_low < 5: score += 20
            elif dist_low < 10: score += 10
        candidates.append({
            'code': code,
            'name': NAME.get(code, code),
            'sector': sector,
            'price': r['price'],
            'pct': r['pct'],
            'score': score,
            'dist_low': (r['price'] - r['low52']) / r['low52'] * 100 if r['low52'] > 0 else 999,
        })
    candidates.sort(key=lambda x: x['score'], reverse=True)
    return candidates, sector_stats

def generate_report():
    today = datetime.now().strftime('%Y-%m-%d')
    account = get_account_status()
    candidates, sector_stats = scan_candidates()
    
    lines = []
    lines.append("=" * 55)
    lines.append(f"【盘前分析报告】{today}")
    lines.append("=" * 55)
    lines.append("")
    lines.append("一、账户状态")
    lines.append(f"  总资产: {account['total']:,.0f}元")
    lines.append(f"  持仓市值: {account['total_value']:,.0f}元")
    lines.append(f"  现金: {account['cash']:,.0f}元")
    lines.append(f"  累计盈亏: {account['pnl']:+,.0f}元 ({account['pnl_pct']:+.2f}%)")
    lines.append("")
    lines.append("二、持仓状态")
    for p in account['positions']:
        lines.append(f"")
        lines.append(f"  {p['name']} ({p['code']})")
        lines.append(f"    现价: {p['price']:.2f} | 成本: {p['cost']:.2f}")
        lines.append(f"    止损: {p['stop']:.2f} | 距止损: {p['dist_stop']:+.1f}%")
        lines.append(f"    盈亏: {p['pnl']:+.0f}元")
    lines.append("")
    lines.append("三、强势板块排序（今日）")
    sorted_sectors = sorted(sector_stats.items(), key=lambda x: x[1]['avg'], reverse=True)
    for s, d in sorted_sectors[:5]:
        lines.append(f"  {s}: {d['avg']:+.2f}% ({d['count']}只)")
    lines.append("")
    lines.append("四、明日重点关注 TOP 5")
    for i, c in enumerate(candidates[:5], 1):
        tag = ">>>" if i <= 3 else ""
        lines.append(f"")
        lines.append(f"{i}. {c['name']} ({c['code']}) {tag}")
        lines.append(f"   板块: {c['sector']} | 今日: {c['pct']:+.2f}% | 距52周低: {c['dist_low']:+.1f}%")
        lines.append(f"   评分: {c['score']}分")
    lines.append("")
    lines.append("五、操作计划")
    lines.append(f"")
    lines.append(f"  当前仓位: {account['total_value']/account['total']*100:.1f}%")
    lines.append(f"  可用现金: {account['cash']:,.0f}元")
    lines.append(f"")
    lines.append(f"  建议操作:")
    lines.append(f"  - 持仓止损线已设定，触发即执行，不犹豫")
    lines.append(f"  - 若有新增标的:")
    lines.append(f"    * 只选评分>=50分的标的")
    lines.append(f"    * 单只仓位<=20%")
    lines.append(f"    * 等待大盘回调后再买")
    lines.append(f"  - 不追高，不接飞刀")
    lines.append("")
    lines.append("=" * 55)
    return "\n".join(lines)

if __name__ == '__main__':
    print(generate_report())
