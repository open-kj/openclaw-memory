"""
主动预判引擎 - 盘前分析
"""
import requests
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')
API_KEY = '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'

HOLDINGS = [
    {'code': 'sz300394', 'name': '天孚通信', 'cost': 306.99, 'qty': 618, 'stop': 291.64},
    {'code': 'sz300223', 'name': '炬芯科技', 'cost': 122.34, 'qty': 1530, 'stop': 116.22},
    {'code': 'sz300548', 'name': '博创科技', 'cost': 148.57, 'qty': 1000, 'stop': 141.14},
    {'code': 'sh688521', 'name': '源杰股份', 'cost': 198.88, 'qty': 1000, 'stop': 188.94},
]
CASH = 294992.0

def get_prices(codes):
    url = 'https://qt.gtimg.cn/q=' + ','.join(codes)
    r = requests.get(url, timeout=8)
    results = {}
    for line in r.text.strip().split('\n'):
        if '=' not in line:
            continue
        code_part = line.split('=')[0].replace('var v_', '').strip()
        parts = line.split('"')[1].split('~')
        if len(parts) > 32:
            try:
                price = float(parts[3])
                chg_pct = float(parts[32])
                name = parts[1]
                results[code_part] = {'name': name, 'price': price, 'chg_pct': chg_pct}
            except:
                pass
    return results

def search_news(query, max_results=2):
    r = requests.post('https://api.tavily.com/search', json={
        'api_key': API_KEY,
        'query': query,
        'search_depth': 'basic',
        'max_results': max_results
    }, timeout=15)
    d = r.json()
    return d.get('results', [])[:max_results]

def calc_margin(price, stop):
    if price <= 0 or stop <= 0:
        return None
    return ((price - stop) / price) * 100

def run():
    print('=' * 55)
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    print(f'  A股盘前主动分析 - {now}')
    print('=' * 55)
    print()

    codes = [h['code'] for h in HOLDINGS]
    prices = get_prices(codes)

    print('[一、持仓状况]')
    print('  现金: {:,.0f}元'.format(CASH))
    total_value = 0
    total_cost = 0
    risk_stocks = []

    for h in HOLDINGS:
        p = prices.get(h['code'], {})
        price = p.get('price', h['cost'])
        chg = p.get('chg_pct', 0)
        cost_amt = h['cost'] * h['qty']
        value = price * h['qty']
        margin = calc_margin(price, h['stop'])
        profit = value - cost_amt
        profit_pct = (profit / cost_amt) * 100
        total_value += value
        total_cost += cost_amt

        if margin is not None and margin < 3:
            flag = ' [COLOR=red]!!![/COLOR]'
            risk_stocks.append(h['name'])
        elif margin is not None and margin < 5:
            flag = ' [COLOR=orange]?[/COLOR]'
        else:
            flag = ' [COLOR=green]OK[/COLOR]'

        margin_str = '{:.1f}%'.format(margin) if margin is not None else 'N/A'
        print('  {} ({})'.format(h['name'], h['code']))
        print('    现价: {:.2f} ({:+.2f}%) | 成本: {:.2f} | 盈亏: {:+.0f}元 ({:+.1f}%)'.format(
            price, chg, h['cost'], profit, profit_pct))
        print('    止损: {} | 距止损: {} {}'.format(h['stop'], margin_str, flag))
        print()

    total_asset = total_value + CASH
    total_profit = total_asset - 1000000.0
    total_profit_pct = (total_asset / 1000000.0 - 1) * 100
    print('  总资产: {:,.0f}元'.format(total_asset))
    print('  总盈亏: {:+,.0f}元 ({:+.2f}%)'.format(total_profit, total_profit_pct))
    print()

    print('[二、持仓新闻摘要]')
    count = 0
    for h in HOLDINGS:
        q = h['code'] + ' ' + h['name'] + ' 最新 2026'
        results = search_news(q, 1)
        for item in results:
            t = item['title'][:55]
            print('  {}: {}'.format(h['name'], t))
            count += 1
        if count >= 4:
            break
    print()

    print('[三、大盘今日预期]')
    mresults = search_news('A股 今日大盘 行情分析 2026年3月', 2)
    for item in mresults:
        print('  {}'.format(item['title'][:60]))
    print()

    print('[四、操作建议]')
    if risk_stocks:
        print('  [COLOR=red]重点关注: {}[/COLOR]'.format(', '.join(risk_stocks)))
        print('  若继续下跌触发止损线则自动执行')
    else:
        print('  持仓距止损均安全')
    print()

    if CASH < 100000:
        print('  [COLOR=orange]现金不足10万，暂停开新仓[/COLOR]')
    elif CASH >= 100000:
        print('  [COLOR=green]可用现金{:,.0f}元，等待回调[/COLOR]'.format(CASH))
    print()
    print('=' * 55)
    return {
        'total_asset': total_asset,
        'profit': total_profit,
        'profit_pct': total_profit_pct,
        'risk_stocks': risk_stocks,
    }

if __name__ == '__main__':
    run()
