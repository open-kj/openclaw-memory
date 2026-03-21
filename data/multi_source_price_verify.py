"""
multi_source_price_verify.py v2.0
新增：资金流异常告警 + API故障自动切换
"""
import requests
import sys
import os
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from config.settings import TAVILY_API_KEY, SESSION_STATE_FILE

sys.stdout.reconfigure(encoding='utf-8')

# API故障记录
_api_errors = {}
_API_PRIMARY = 'tencent'

def get_tencent(code):
    try:
        r = requests.get('https://qt.gtimg.cn/q=' + code, timeout=8)
        parts = r.text.split('~')
        if len(parts) > 32 and float(parts[3]) > 0:
            return {'source': '腾讯财经', 'price': float(parts[3]), 'chg': float(parts[32])}
    except:
        _record_error('腾讯财经')
    return None

def get_sina(code):
    try:
        headers = {'Referer': 'https://finance.sina.com.cn'}
        r = requests.get('https://hq.sinajs.cn/list=' + code, headers=headers, timeout=8)
        content = r.text.split('"')[1]
        parts = content.split(',')
        if len(parts) > 10 and float(parts[3]) > 0:
            return {'source': '新浪财经', 'price': float(parts[3]), 'chg': float(parts[32])}
    except:
        _record_error('新浪财经')
    return None

def get_akshare(code):
    try:
        import akshare as ak
        df = ak.stock_zh_a_spot_em()
        row = df[df['代码'] == code[2:]]
        if not row.empty:
            price = float(row['最新价'].values[0])
            chg = float(row['涨跌幅'].values[0])
            return {'source': 'akshare', 'price': price, 'chg': chg}
    except:
        _record_error('akshare')
    return None

def _record_error(source):
    now = time.time()
    if source not in _api_errors:
        _api_errors[source] = []
    _api_errors[source].append(now)
    # 只保留1小时内的记录
    _api_errors[source] = [t for t in _api_errors[source] if now - t < 3600]
    if len(_api_errors[source]) >= 3:
        _send_api_alert(source)

def _send_api_alert(source):
    msg = '⚠️ 【API故障】' + source + '连续3次失败，已暂停使用'
    print(msg)
    _write_alert(msg)

def _write_alert(msg):
    try:
        ts = datetime.now().strftime('%Y-%m-%d %H:%M')
        with open(SESSION_STATE_FILE, 'a', encoding='utf-8') as f:
            f.write('\n## ⚠️ ' + ts + '\n' + msg + '\n')
    except:
        pass

def _get_best_source(code):
    """按优先级获取数据，自动切换故障源"""
    sources = [
        ('腾讯财经', get_tencent),
        ('新浪财经', get_sina),
        ('akshare', get_akshare),
    ]
    for name, fn in sources:
        if name in _api_errors and len(_api_errors[name]) >= 3:
            continue  # 该源在熔断
        result = fn(code)
        if result:
            _api_errors[name] = []  # 成功则清除错误记录
            return result
    return None

def get_money_flow_check(code):
    """检查资金流异常：净流入/流出>5%"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://data.eastmoney.com'}
        market = 1 if code.startswith('sh') else 0
        secid = f'{market}.{code[2:]}'
        r = requests.get(
            'https://push2.eastmoney.com/api/qt/stock/get',
            params={'secid': secid, 'fields': 'f62,f184',
                    'ut': 'b2884a393a59ad64002292a3e90d46a5'},
            headers=headers, timeout=8
        )
        d = r.json().get('data', {})
        if d:
            rate = d.get('f184', 0) or 0
            net = d.get('f62', 0) or 0
            return {'main_rate': rate, 'main_net': net / 1e6, 'alert': abs(rate) > 5}
    except:
        pass
    return {'main_rate': 0, 'main_net': 0, 'alert': False}

def verify_with_alerts(code, name=''):
    """带告警的交叉验证"""
    prices = {}
    sources_used = []

    for src_name, fn in [('腾讯财经', get_tencent), ('新浪财经', get_sina), ('akshare', get_akshare)]:
        if src_name in _api_errors and len(_api_errors[src_name]) >= 3:
            continue
        result = fn(code)
        if result:
            prices[src_name] = result['price']
            sources_used.append(src_name)

    if len(prices) < 1:
        _write_alert('⚠️ 【数据源异常】' + code + ' 所有API均失效')
        return {'code': code, 'error': 'all_failed', 'sources_used': sources_used}

    avg = sum(prices.values()) / len(prices)
    diff = max(prices.values()) - min(prices.values())
    diff_ratio = diff / avg if avg > 0 else 0

    alerts = []

    # 价格差异告警
    if diff_ratio > 0.005:
        alerts.append('价格差异{:.2f}%'.format(diff_ratio * 100))
        _write_alert('⚠️ ' + code + ' ' + name + ' 多源价格差异{:.2f}%'.format(diff_ratio * 100))

    # 资金流告警
    mf = get_money_flow_check(code)
    if mf.get('alert'):
        direction = '净流入' if mf['main_rate'] > 0 else '净流出'
        alerts.append('资金流{}>5%'.format(direction))
        _write_alert('💰 ' + code + ' ' + name + ' 资金流{} {:.1f}%'.format(direction, mf['main_rate']))

    return {
        'code': code, 'name': name,
        'prices': prices,
        'average': avg,
        'diff_ratio': diff_ratio,
        'money_flow': mf,
        'alerts': alerts,
        'sources_used': sources_used,
        'status': 'WARN' if alerts else 'OK',
    }

def verify_all(codes_names):
    print('=== 多源价格验证 v2.0（含资金流+API切换）===')
    alerts_all = []
    for code, name in codes_names:
        v = verify_with_alerts(code, name)
        icon = '⚠️' if v['status'] == 'WARN' else '✅'
        print(icon + ' [' + code + '] ' + name)
        for src, price in v.get('prices', {}).items():
            print('    ' + src + ': ' + str(price))
        if v.get('alerts'):
            for a in v['alerts']:
                print('    ⚠️ ' + a)
            alerts_all.append(v)
        print()
    print('API故障记录: ' + str({k: len(v) for k, v in _api_errors.items()}))
    return alerts_all

if __name__ == '__main__':
    holdings = [
        ('sz300394', '天孚通信'),
        ('sz300223', '北京君正'),
        ('sz300548', '长芯博创'),
        ('sh688521', '芯原股份'),
    ]
    verify_all(holdings)
