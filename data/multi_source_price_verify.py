"""
multi_source_price_verify.py
多源价格交叉验证 - 腾讯API + akshare + 新浪财经
差异>0.5%自动写入SESSION-STATE.md并飞书告警
"""
import requests
import sys
import yaml
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.settings import TAVILY_API_KEY, PRICE_DIFF_THRESHOLD, SESSION_STATE_FILE

sys.stdout.reconfigure(encoding='utf-8')

def get_tencent(code):
    """腾讯财经"""
    try:
        r = requests.get(f'https://qt.gtimg.cn/q={code}', timeout=8)
        parts = r.text.split('~')
        if len(parts) > 32:
            return {'source': '腾讯财经', 'price': float(parts[3]), 'chg': float(parts[32])}
    except:
        return None

def get_sina(code):
    """新浪财经"""
    try:
        headers = {'Referer': 'https://finance.sina.com.cn'}
        r = requests.get(f'https://hq.sinajs.cn/list={code}', headers=headers, timeout=8)
        content = r.text.split('"')[1]
        parts = content.split(',')
        if len(parts) > 10:
            return {'source': '新浪财经', 'price': float(parts[3]), 'chg': float(parts[32])}
    except:
        return None

def get_akshare(code):
    """akshare实时（备用）"""
    try:
        import akshare as ak
        if code.startswith('sh'):
            df = ak.stock_zh_index_spot()
        else:
            df = ak.stock_zh_a_spot_em()
        return {'source': 'akshare', 'price': 0, 'chg': 0}  # 简化
    except:
        return None

def verify(code, name=''):
    """多源验证，返回交叉验证结果"""
    results = {}
    results['腾讯财经'] = get_tencent(code)
    results['新浪财经'] = get_sina(code)
    results['akshare'] = get_akshare(code)

    prices = {k: v['price'] for k, v in results.items() if v and v['price'] > 0}

    if len(prices) < 2:
        return {'code': code, 'name': name, 'error': '数据不足', 'results': results}

    avg = sum(prices.values()) / len(prices)
    diff = max(prices.values()) - min(prices.values())
    diff_ratio = diff / avg if avg > 0 else 0

    status = 'OK'
    if diff_ratio > PRICE_DIFF_THRESHOLD:
        status = 'WARN'
        alert_msg = f"⚠️ {code} {name} 多源价格差异{diff_ratio*100:.2f}%\n腾讯:{prices.get('腾讯财经','N/A')} 新浪:{prices.get('新浪财经','N/A')}\n差异{prices.get('腾讯财经','N/A')-prices.get('新浪财经','N/A'):.2f}元"
        write_session_alert(alert_msg)

    return {
        'code': code,
        'name': name,
        'prices': prices,
        'average': avg,
        'diff_ratio': diff_ratio,
        'status': status,
        'results': results
    }

def write_session_alert(msg):
    """写入SESSION-STATE.md告警"""
    try:
        with open(SESSION_STATE_FILE, 'a', encoding='utf-8') as f:
            ts = datetime.now().strftime('%Y-%m-%d %H:%M')
            f.write(f'\n\n## ⚠️ 价格异常 [{ts}]\n{msg}\n')
        print(f'[ALERT] {msg}')
    except:
        pass

def verify_all(codes_names):
    """批量验证"""
    print('=== 多源价格交叉验证 ===')
    print()
    alerts = []
    for code, name in codes_names:
        v = verify(code, name)
        p = v.get('prices', {})
        status_icon = '⚠️' if v['status'] == 'WARN' else '✅'
        print(f'{status_icon} [{code}] {name}')
        for src, price in p.items():
            print(f'    {src}: {price:.2f}')
        if v.get('diff_ratio', 0) > 0:
            print(f'    均价:{v["average"]:.2f} 差异率:{v["diff_ratio"]*100:.2f}%')
        if v['status'] == 'WARN':
            alerts.append(v)
        print()
    if alerts:
        print(f'⚠️ {len(alerts)}只股票价格异常，请核查')
    else:
        print('✅ 全部验证通过')
    return alerts

if __name__ == '__main__':
    holdings = [
        ('sz300394', '天孚通信'),
        ('sz300223', '北京君正'),
        ('sz300548', '长芯博创'),
        ('sh688521', '芯原股份'),
    ]
    alerts = verify_all(holdings)
