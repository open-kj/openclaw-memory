"""
market_data.py v2.0 - 大盘指数 + 北向/南向资金
"""
import requests
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def get_indices():
    r = requests.get('https://qt.gtimg.cn/q=sh000001,sz399001,sz399006', timeout=8)
    results = {}
    name_map = {'sh000001': '上证指数', 'sz399001': '深证成指', 'sz399006': '创业板指'}
    for line in r.text.strip().split('\n'):
        if '=' not in line:
            continue
        raw = line.split('=')[0].replace('var v_', '').strip()
        parts = line.split('~')
        if len(parts) > 32:
            code = raw.replace('v_', '')
            try:
                results[code] = {
                    'name': name_map.get(code, parts[1]),
                    'price': float(parts[3]),
                    'chg': float(parts[32]),
                }
            except:
                pass
    return results

def get_north_south_flow():
    """
    北向/南向资金实时数据
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://data.eastmoney.com'}
        # 东方财富沪股通+深股通数据
        r = requests.get(
            'https://push2.eastmoney.com/api/qt/kamt.rtmin/get',
            headers=headers, timeout=8
        )
        d = r.json().get('data', {})
        # 简化：使用hgt=沪股通净买入 sgt=深股通净买入
        hgt = d.get('hgt006', 0) or 0  # 沪股通（百万元）
        sgt = d.get('sgt007', 0) or 0  # 深股通（百万元）
        north = (hgt + sgt) / 1e8  # 转为亿元
        return {
            'hgt': hgt / 1e8,
            'sgt': sgt / 1e8,
            'north_total': north,
            'north_yi': round(north, 2),
            'direction': '净买入' if north > 0 else ('净卖出' if north < 0 else '持平'),
        }
    except:
        return None

def check_north_flow_alert():
    """
    北向资金>50亿触发大盘异动告警
    """
    d = get_north_south_flow()
    if d:
        threshold_yi = 50  # 50亿
        if abs(d['north_yi']) > threshold_yi:
            return {
                'alert': True,
                'direction': d['direction'],
                'amount_yi': d['north_yi'],
                'threshold_yi': threshold_yi,
            }
    return {'alert': False}

if __name__ == '__main__':
    indices = get_indices()
    print('=== 大盘指数 ===')
    for code, data in indices.items():
        icon = 'RED' if data['chg'] < 0 else 'GREEN'
        print('[{}] {}: {:.2f} ({:+.2f}%)'.format(icon, data['name'], data['price'], data['chg']))
    print()
    nf = get_north_south_flow()
    if nf:
        print('=== 北向资金 ===')
        print('沪股通: {:.2f}亿元'.format(nf['hgt']))
        print('深股通: {:.2f}亿元'.format(nf['sgt']))
        print('合计: {} {:.2f}亿元'.format(nf['direction'], abs(nf['north_yi'])))
        alert = check_north_flow_alert()
        if alert['alert']:
            print('⚠️ 北向资金{}亿，触发大盘异动告警！'.format(alert['amount_yi']))
        else:
            print('北向资金正常，无异动')
    else:
        print('北向资金数据获取失败')
