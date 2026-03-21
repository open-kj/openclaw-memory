"""
scheduler.py - 智能调度器
按股票优先级动态调整检查频率
高优先级(如炬芯/北京君正)每10分钟，普通每30分钟
大盘涨跌>1.5%时自动触发全量持仓检查
"""
import sys
import os
import time
import requests
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.settings import (
    HIGH_PRIORITY_INTERVAL, NORMAL_PRIORITY_INTERVAL,
    MARKET_CHANGE_THRESHOLD, TAVILY_API_KEY
)
from data.market_data import get_indices

sys.stdout.reconfigure(encoding='utf-8')

# 持仓配置
HOLDINGS = [
    {'code': 'sz300394', 'name': '天孚通信', 'priority': 'normal'},
    {'code': 'sz300223', 'name': '北京君正', 'priority': 'high'},  # sz300223=北京君正
    {'code': 'sz300548', 'name': '长芯博创', 'priority': 'normal'},
    {'code': 'sh688521', 'name': '芯原股份', 'priority': 'normal'},
]
PREV_INDICES = {'sh000001': None, 'sz399001': None, 'sz399006': None}

def get_price(code):
    try:
        r = requests.get(f'https://qt.gtimg.cn/q={code}', timeout=8)
        parts = r.text.split('~')
        if len(parts) > 32:
            return float(parts[3])
    except:
        return None

def check_stop_loss(h):
    """检查止损，返回告警信息"""
    price = get_price(h['code'])
    if price is None:
        return None
    stops = {
        'sz300394': 291.64,
        'sz300223': 116.22,
        'sz300548': 141.14,
        'sh688521': 188.94,
    }
    stop = stops.get(h['code'])
    if stop and price <= stop:
        return {
            'name': h['name'],
            'code': h['code'],
            'price': price,
            'stop': stop,
            'level': 'TRIGGER',
        }
    elif stop and price <= stop * 1.015:  # 距止损1.5%以内
        margin = (price - stop) / price * 100
        return {
            'name': h['name'],
            'code': h['code'],
            'price': price,
            'stop': stop,
            'margin': margin,
            'level': 'WARNING',
        }
    return None

def check_market_change():
    """检查大盘异动，>1.5%触发全量检查"""
    global PREV_INDICES
    indices = get_indices()
    alerts = []
    for code, data in indices.items():
        prev = PREV_INDICES.get(code)
        if prev is not None:
            change = abs(data['chg'] - prev)
            if change > MARKET_CHANGE_THRESHOLD * 100:
                alerts.append(f"大盘异动: {data['name']} {data['chg']:+.2f}%")
        PREV_INDICES[code] = data['chg']
    return alerts

def run_scheduler_cycle():
    """执行一轮调度"""
    print(f'[{datetime.now().strftime("%H:%M:%S")}] === 调度检查 ===')

    # 1. 大盘异动检查
    market_alerts = check_market_change()
    if market_alerts:
        print(f'⚠️ 大盘异动: {", ".join(market_alerts)}')

    # 2. 按优先级检查持仓
    urgent = []
    for h in HOLDINGS:
        alert = check_stop_loss(h)
        if alert:
            urgent.append(alert)
            if alert['level'] == 'TRIGGER':
                print(f'🚨 止损触发: {h["name"]}({h["code"]}) 现价{alert["price"]} <= 止损{alert["stop"]}')
            elif alert['level'] == 'WARNING':
                print(f'⚠️ 止损预警: {h["name"]} 距止损{alert["margin"]:.1f}%')

    if not urgent:
        print('✅ 持仓安全')

    return {
        'market_alerts': market_alerts,
        'stop_alerts': urgent,
        'timestamp': datetime.now().isoformat(),
    }

def run_continuous(hours=1):
    """连续运行（用于测试）"""
    print(f'启动调度器，连续运行{hours}小时')
    start = time.time()
    cycle = 0
    while time.time() - start < hours * 3600:
        cycle += 1
        try:
            result = run_scheduler_cycle()
            print(f'  周期{cycle}完成')
        except Exception as e:
            print(f'  周期{cycle}异常: {e}')
        time.sleep(60)  # 每分钟检查一次

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        run_continuous(hours=1)
    else:
        run_scheduler_cycle()
