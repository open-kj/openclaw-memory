"""
capital_flow.py - 资金流数据
集成东方财富API获取个股主力资金流入/流出、龙虎榜数据
"""
import requests
import sys
import os
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

def get_money_flow(code):
    """
    获取个股资金流向（东方财富API）
    返回：主力净流入、净流入率、买卖差额
    """
    try:
        # 东方财富资金流向API
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://data.eastmoney.com'
        }
        # code转换：sz->0, sh->1
        market = 1 if code.startswith('sh') else 0
        secid = f'{market}.{code[2:]}'
        url = f'https://push2.eastmoney.com/api/qt/stock/get'
        params = {
            'secid': secid,
            'fields': 'f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f64,f65,f70,f73,f76,f79,f82,f85,f88',
            'ut': 'b2884a393a59ad64002292a3e90d46a5'
        }
        r = requests.get(url, params=params, headers=headers, timeout=8)
        d = r.json().get('data', {})
        if not d:
            return None

        # f62=主力净流入额(元) f184=主力净流入率 f66=超大单净流入 f69=大单净流入
        # f72=中单净流入 f75=小单净流入
        main_net = d.get('f62', 0) or 0
        main_rate = d.get('f184', 0) or 0

        return {
            'main_net': main_net,       # 主力净流入（元）
            'main_net_m': main_net / 1e6,  # 主力净流入（万元）
            'main_rate': main_rate,     # 主力净流入率（%）
            'f66': d.get('f66', 0) or 0,  # 超大单
            'f69': d.get('f69', 0) or 0,  # 大单
            'f72': d.get('f72', 0) or 0,  # 中单
            'f75': d.get('f75', 0) or 0,  # 小单
        }
    except Exception as e:
        return {'error': str(e)}

def get_market_flow():
    """
    获取大盘资金整体流向
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://data.eastmoney.com'}
        url = 'https://push2.eastmoney.com/api/qt/stock/get'
        # 上证指数
        r1 = requests.get(url, params={
            'secid': '1.000001',
            'fields': 'f62,f184',
            'ut': 'b2884a393a59ad64002292a3e90d46a5'
        }, headers=headers, timeout=8)
        # 深证成指
        r2 = requests.get(url, params={
            'secid': '0.399001',
            'fields': 'f62,f184',
            'ut': 'b2884a393a59ad64002292a3e90d46a5'
        }, headers=headers, timeout=8)

        d1 = r1.json().get('data', {}) or {}
        d2 = r2.json().get('data', {}) or {}
        return {
            'sh_main_net': d1.get('f62', 0) or 0,
            'sh_main_rate': d1.get('f184', 0) or 0,
            'sz_main_net': d2.get('f62', 0) or 0,
            'sz_main_rate': d2.get('f184', 0) or 0,
        }
    except:
        return None

def check_money_flow_alert(code, name):
    """
    检查资金流异常：净流入/流出>5%触发告警
    """
    data = get_money_flow(code)
    if not data or 'error' in data:
        return None

    main_rate = abs(data['main_rate'])
    if main_rate > 5:
        direction = '净流入' if data['main_rate'] > 0 else '净流出'
        return {
            'code': code,
            'name': name,
            'direction': direction,
            'rate': data['main_rate'],
            'net_m': data['main_net_m'],
            'alert': True
        }
    return {'code': code, 'name': name, 'alert': False, 'rate': data['main_rate']}

def get_north_south_flow():
    """
    北向/南向资金（沪深港通）
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://data.eastmoney.com'}
        # 东方财富北向资金
        r = requests.get(
            'https://push2.eastmoney.com/api/qt/kamt.rtmin/get',
            headers=headers, timeout=8
        )
        d = r.json().get('data', {})
        north_net = d.get('hgt006', 0) or 0  # 沪股通净买入
        south_net = d.get('sgt007', 0) or 0  # 深股通净买入
        return {
            'north_buy': north_net,   # 北向（沪股通+深股通）净买入
            'north_buy_yi': north_net / 1e8,  # 亿元
        }
    except:
        return None

if __name__ == '__main__':
    print('=== 个股资金流 ===')
    stocks = [('sz300394','天孚通信'), ('sz300223','北京君正'),
              ('sz300548','长芯博创'), ('sh688521','芯原股份')]
    for code, name in stocks:
        d = get_money_flow(code)
        if d and 'error' not in d:
            print(f'{name}({code}): 主力净流入={d["main_net_m"]:.1f}万元 净流入率={d["main_rate"]:.2f}%')
        else:
            print(f'{name}: 获取失败 {d.get("error","")}')

    print()
    print('=== 北向资金 ===')
    ns = get_north_south_flow()
    if ns:
        print(f'北向净买入: {ns["north_buy_yi"]:.2f}亿元')
