"""
market_data.py - 大盘实时数据获取
"""
import requests
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def get_indices():
    """获取三大指数实时数据"""
    r = requests.get('https://qt.gtimg.cn/q=sh000001,sz399001,sz399006', timeout=8)
    results = {}
    name_map = {
        'sh000001': '上证指数',
        'sz399001': '深证成指',
        'sz399006': '创业板指',
    }
    for line in r.text.strip().split('\n'):
        if '=' not in line:
            continue
        raw_code = line.split('=')[0].replace('var v_', '').strip()
        # raw_code = 'v_sh000001'
        parts = line.split('~')
        if len(parts) > 32:
            code = raw_code.replace('v_', '')  # 'sh000001'
            try:
                results[code] = {
                    'name': name_map.get(code, parts[1]),
                    'price': float(parts[3]),
                    'chg': float(parts[32]),
                }
            except:
                pass
    return results

if __name__ == '__main__':
    indices = get_indices()
    print('=== 大盘指数 ===')
    for code, data in indices.items():
        icon = 'RED' if data['chg'] < 0 else 'GREEN'
        print(f'[{icon}] {data["name"]}: {data["price"]:.2f} ({data["chg"]:+.2f}%)')
