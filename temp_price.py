# -*- coding: utf-8 -*-
import requests
import json
import sys

stocks = {
    'sz300394': '天孚通信',
    'sh688521': '芯原股份',
    'sz002594': '比亚迪',
    'sh688981': '中芯国际'
}

# 止损线和预警线
levels = {
    'sz300394': {'stop': 291.64, 'warn1': 300.00, 'buy': 305.00, 'sell': 320.00, 'prev': 298.49},
    'sh688521': {'stop': 188.94, 'warn1': 192.00, 'buy': 195.00, 'sell': 198.00, 'prev': 190.50, 'danger': True},
    'sz002594': {'stop': 103.45, 'buy': 105.00, 'sell': 115.00, 'prev': 107.63},
    'sh688981': {'stop': 93.14, 'warn1': 95.00, 'sell': 103.00, 'prev': 98.04, 'new': True}
}

codes = ','.join(stocks.keys())
url = f'https://qt.gtimg.cn/q={codes}'

try:
    resp = requests.get(url, timeout=5)
    resp.encoding = 'gbk'
    text = resp.text
    
    print('=== 持仓实时价格 ===')
    print('时间: 13:30')
    print()
    
    alerts = []
    
    for code, name in stocks.items():
        # 解析腾讯API数据
        search_str = f'"{code}='
        idx = text.find(search_str)
        if idx == -1:
            print(f'{name}({code}): 无法获取数据')
            continue
            
        start = text.find('="', idx) + 2
        end = text.find('";', start)
        data = text[start:end]
        parts = data.split('~')
        
        if len(parts) < 10:
            print(f'{name}({code}): 数据解析错误')
            continue
            
        price = float(parts[3])
        prev_close = float(parts[4])
        change = price - prev_close
        change_pct = (change / prev_close) * 100
        
        print(f'{name}({code}): 现价={price} 昨收={prev_close} 涨跌={change:+.2f}({change_pct:+.2f}%)')
        
        # 检查止损线
        lv = levels.get(code, {})
        stop = lv.get('stop', 0)
        if price <= stop:
            alerts.append(f"🚨 【止损预警】{name}({code}) 现价{price} <= 止损线{stop}！立即通知用户决策！")
        
        # 检查警示支撑位
        warn1 = lv.get('warn1', 0)
        if warn1 and price <= warn1:
            alerts.append(f"⚠️ {name}({code}) 现价{price} <= 警示支撑位{warn1}")
        
        # 检查波段低吸预警
        buy = lv.get('buy', 0)
        if buy and price <= buy and price > stop:
            alerts.append(f"📍 波段低吸预警: {name}({code}) 现价{price} <= 低吸线{buy}")
        
        # 检查波段高抛预警
        sell = lv.get('sell', 0)
        if sell and price >= sell:
            alerts.append(f"📍 波段高抛预警: {name}({code}) 现价{price} >= 高抛线{sell}")
    
    print()
    if alerts:
        print('=== 触发条件 ===')
        for a in alerts:
            print(a)
    else:
        print('=== 无触发条件 ===')
        print('所有持仓价格运行在安全区间')
    
except Exception as e:
    print(f'Error: {e}')
    sys.exit(1)
