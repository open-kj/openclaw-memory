"""
dashboard.py - 每日持仓可视化仪表盘
生成持仓报告（市值/盈亏/评分/仓位占比）
"""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.stdout.reconfigure(encoding='utf-8')

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except:
    HAS_MATPLOTLIB = False

HOLDINGS = [
    {'code': 'sz300394', 'name': '天孚通信', 'cost': 306.99, 'qty': 618},
    {'code': 'sz300223', 'name': '北京君正', 'cost': 122.34, 'qty': 1530},
    {'code': 'sz300548', 'name': '长芯博创', 'cost': 148.57, 'qty': 1000},
    {'code': 'sh688521', 'name': '芯原股份', 'cost': 198.88, 'qty': 1000},
]
CASH = 294992.0
INITIAL = 1_000_000.0

def get_prices():
    import requests
    codes = ','.join([h['code'] for h in HOLDINGS])
    r = requests.get('https://qt.gtimg.cn/q=' + codes, timeout=8)
    prices = {}
    for line in r.text.strip().split('\n'):
        if '=' not in line:
            continue
        code = line.split('=')[0].replace('var v_', '').strip()
        parts = line.split('~')
        if len(parts) > 32:
            try:
                prices[code] = {'price': float(parts[3]), 'chg': float(parts[32])}
            except:
                pass
    return prices

def generate_text_report():
    """生成文本格式仪表盘"""
    prices = get_prices()
    print('=' * 50)
    print('  📊 持仓仪表盘')
    print('=' * 50)

    total_cost = 0
    total_value = 0
    rows = []

    for h in HOLDINGS:
        p = prices.get(h['code'], {})
        price = p.get('price', h['cost'])
        chg = p.get('chg', 0)
        cost_amt = h['cost'] * h['qty']
        value = price * h['qty']
        profit = value - cost_amt
        profit_pct = profit / cost_amt * 100
        total_cost += cost_amt
        total_value += value
        pos_ratio = value / (total_value + CASH) * 100

        icon = '🟢' if profit >= 0 else '🔴'
        print()
        print('  {} {}'.format(icon, h['name']))
        print('    代码: {}'.format(h['code']))
        print('    现价: {:.2f} ({:+.2f}%)'.format(price, chg))
        print('    成本: {:.2f} | 盈亏: {:+.0f}元 ({:+.1f}%)'.format(h['cost'], profit, profit_pct))
        print('    市值: {:,.0f}元 | 占比: {:.1f}%'.format(value, pos_ratio))

    total_asset = total_value + CASH
    total_profit = total_asset - INITIAL
    total_profit_pct = total_profit / INITIAL * 100

    print()
    print('  💵 账户总览')
    print('    总资产: {:,.0f}元'.format(total_asset))
    print('    总盈亏: {:+,.0f}元 ({:+.2f}%)'.format(total_profit, total_profit_pct))
    print('    现金: {:,.0f}元 ({:.1f}%)'.format(CASH, CASH / total_asset * 100))
    print('    持仓: {:,.0f}元 ({:.1f}%)'.format(total_value, total_value / total_asset * 100))
    print('    总成本: {:,.0f}元'.format(total_cost))
    print()
    print('=' * 50)

def generate_image_report():
    """生成图片格式仪表盘"""
    if not HAS_MATPLOTLIB:
        print('matplotlib未安装，跳过图片生成')
        return

    import matplotlib.pyplot as plt
    import numpy as np

    prices = get_prices()
    names = [h['name'] for h in HOLDINGS]
    values = [prices.get(h['code'], {}).get('price', h['cost']) * h['qty'] for h in HOLDINGS]
    costs = [h['cost'] * h['qty'] for h in HOLDINGS]
    profits = [v - c for v, c in zip(values, costs)]
    total_value = sum(values)
    pos_ratios = [v / (total_value + CASH) * 100 for v in values]

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('AShare Dashboard', fontsize=14)

    # 1. 市值占比饼图
    labels = names + ['Cash']
    sizes = values + [CASH]
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#ffd700']
    axes[0, 0].pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors[:len(sizes)])
    axes[0, 0].set_title('Position Ratio')

    # 2. 盈亏柱状图
    colors2 = ['green' if p >= 0 else 'red' for p in profits]
    axes[0, 1].bar(names, profits, color=colors2)
    axes[0, 1].axhline(0, color='black', linewidth=0.5)
    axes[0, 1].set_title('Profit/Loss (Yuan)')
    axes[0, 1].tick_params(axis='x', rotation=15)

    # 3. 持仓占比
    axes[1, 0].bar(names, pos_ratios, color='#66b3ff')
    axes[1, 0].set_title('Position Ratio (%)')
    axes[1, 0].tick_params(axis='x', rotation=15)

    # 4. 成本vs市值
    x = np.arange(len(names))
    width = 0.35
    axes[1, 1].bar(x - width/2, costs, width, label='Cost', color='gray')
    axes[1, 1].bar(x + width/2, values, width, label='Market Value', color='steelblue')
    axes[1, 1].set_xticks(x)
    axes[1, 1].set_xticklabels(names, rotation=15)
    axes[1, 1].legend()
    axes[1, 1].set_title('Cost vs Market Value')

    plt.tight_layout()
    out_path = os.path.join(BASE, 'logs', 'dashboard.png')
    plt.savefig(out_path)
    print('图表已保存: ' + out_path)
    return out_path

if __name__ == '__main__':
    generate_text_report()
    generate_image_report()
