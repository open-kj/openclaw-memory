"""
decision.py - 交易决策引擎 v2.0
@exception_handler 已应用
动态止损/止盈 + 明确操作建议
决策结果自动写入SESSION-STATE.md并飞书推送
"""
import requests
import os
from datetime import datetime
from utils.exception_handler import exception_handler

sys_path_fix = os.path.dirname(os.path.dirname(__file__))
import sys
sys.path.insert(0, sys_path_fix)
from config.settings import TAVILY_API_KEY

sys.stdout.reconfigure(encoding='utf-8')

HOLDINGS = [
    {'code': 'sz300394', 'name': '天孚通信',   'cost': 306.99, 'qty': 618,  'stop': 291.64, 'priority': 'normal'},
    {'code': 'sz300223', 'name': '北京君正',  'cost': 122.34, 'qty': 1530, 'stop': 116.22, 'priority': 'high'},
    {'code': 'sz300548', 'name': '长芯博创',  'cost': 148.57, 'qty': 1000, 'stop': 141.14, 'priority': 'normal'},
    {'code': 'sh688521', 'name': '芯原股份',  'cost': 198.88, 'qty': 1000, 'stop': 188.94, 'priority': 'normal'},
]
CASH = 294992.0

def get_price(code):
    try:
        r = requests.get('https://qt.gtimg.cn/q=' + code, timeout=8)
        parts = r.text.split('~')
        if len(parts) > 32:
            return float(parts[3])
    except:
        return None

def calc_dynamic_stop(cost):
    vol = 0.03
    stop_ratio = max(0.03, min(vol, 0.08))
    return cost * (1 - stop_ratio)

@exception_handler
def decide_and_record():
    """主决策函数：执行决策并写入SESSION-STATE.md"""
    lines = []
    lines.append('\n## 决策记录 [{}]'.format(datetime.now().strftime('%Y-%m-%d %H:%M')))
    lines.append('')

    decisions = []
    total_value = 0

    for h in HOLDINGS:
        price = get_price(h['code'])
        if price is None:
            continue
        value = price * h['qty']
        total_value += value
        profit = value - h['cost'] * h['qty']
        profit_pct = profit / (h['cost'] * h['qty']) * 100
        static_stop = h['stop']
        dyn_stop = calc_dynamic_stop(h['cost'])
        eff_stop = max(static_stop, dyn_stop)
        margin = (price - eff_stop) / price * 100 if price > eff_stop else 0

        if price <= eff_stop:
            action, color = '止损', 'red'
        elif profit_pct >= 10:
            action, color = '考虑止盈', 'orange'
        elif margin < 3:
            action, color = '关注', 'orange'
        else:
            action, color = '持有', 'green'

        decisions.append({**h, 'price': price, 'profit_pct': profit_pct,
                          'margin': margin, 'action': action, 'color': color})
        lines.append('- {}: 现价={:.2f} 盈亏={:+.1f}% 距止损={:.1f}% → [{}]'.format(
            h['name'], price, profit_pct, margin, action))

    total_asset = total_value + CASH
    total_profit = total_asset - 1000000.0
    lines.append('')
    lines.append('总资产: {:,.0f}元 盈亏: {:+,.0f}元'.format(total_asset, total_profit))

    # 写入SESSION-STATE.md
    session_file = os.path.join(sys_path_fix, 'SESSION-STATE.md')
    with open(session_file, 'a', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    urgent = [d for d in decisions if d['color'] in ('red', 'orange')]
    return {'decisions': decisions, 'total_asset': total_asset,
             'total_profit': total_profit, 'urgent': urgent}

@exception_handler
def decide():
    """决策入口"""
    return decide_and_record()

if __name__ == '__main__':
    result = decide()
    print('=== 决策结果 ===')
    for d in result.get('decisions', []):
        print('{}: {} {}% {}'.format(d['name'], d['price'], d['profit_pct'], d['action']))
    print('总资产:', result['total_asset'])
    print('需关注:', [d['name'] for d in result['urgent']])
