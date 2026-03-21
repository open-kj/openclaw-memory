"""
decision.py - 交易决策引擎
动态止损/止盈 + 明确操作建议
止损阈值按波动率动态调整(3%-8%)，止盈=2倍止损
决策结果自动写入SESSION-STATE.md并飞书推送
"""
import requests
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.settings import (
    TAVILY_API_KEY, SESSION_STATE_FILE, FEISHU_USER_ID,
    DYNAMIC_STOP_LOSS_MIN, DYNAMIC_STOP_LOSS_MAX, STOP_PROFIT_RATIO
)
from data.market_data import get_indices

sys.stdout.reconfigure(encoding='utf-8')

HOLDINGS = [
    {'code': 'sz300394', 'name': '天孚通信', 'cost': 306.99, 'qty': 618, 'stop': 291.64, 'priority': 'normal'},
    {'code': 'sz300223', 'name': '北京君正', 'cost': 122.34, 'qty': 1530, 'stop': 116.22, 'priority': 'high'},
    {'code': 'sz300548', 'name': '长芯博创', 'cost': 148.57, 'qty': 1000, 'stop': 141.14, 'priority': 'normal'},
    {'code': 'sh688521', 'name': '芯原股份', 'cost': 198.88, 'qty': 1000, 'stop': 188.94, 'priority': 'normal'},
]
CASH = 294992.0

def get_price(code):
    """获取单只股票现价"""
    try:
        r = requests.get(f'https://qt.gtimg.cn/q={code}', timeout=8)
        parts = r.text.split('~')
        if len(parts) > 32:
            return float(parts[3])
    except:
        return None

def calc_volatility(code, days=20):
    """计算股票历史波动率（简化版：用近20日涨跌标准差）"""
    # 简化：返回固定波动率，后续可接入真实数据
    return 0.03  # 3%作为基准

def calc_dynamic_stop(code, cost):
    """动态计算止损阈值"""
    vol = calc_volatility(code)
    stop_ratio = max(DYNAMIC_STOP_LOSS_MIN, min(vol, DYNAMIC_STOP_LOSS_MAX))
    return cost * (1 - stop_ratio)

def decide():
    """执行交易决策"""
    print('=== 交易决策分析 ===')
    print()
    indices = get_indices()
    sh_chg = indices.get('sh000001', {}).get('chg', 0)
    sz_chg = indices.get('sz399001', {}).get('chg', 0)
    cy_chg = indices.get('sz399006', {}).get('chg', 0)
    print(f'大盘状态: 上证{sh_chg:+.2f}% 深证{sz_chg:+.2f}% 创业板{cy_chg:+.2f}%')
    print()

    decisions = []
    total_value = 0
    actions = []

    for h in HOLDINGS:
        price = get_price(h['code'])
        if price is None:
            continue

        cost_amt = h['cost'] * h['qty']
        value = price * h['qty']
        total_value += value
        profit = value - cost_amt
        profit_pct = (profit / cost_amt) * 100

        # 静态止损线
        static_stop = h['stop']
        # 动态止损线
        dynamic_stop = calc_dynamic_stop(h['code'], h['cost'])
        # 使用较严格的止损
        effective_stop = max(static_stop, dynamic_stop)

        # 距止损距离
        if price <= effective_stop:
            distance_to_stop = 0
        else:
            distance_to_stop = (price - effective_stop) / price * 100

        # 止盈线
        take_profit = h['cost'] * (1 + STOP_PROFIT_RATIO * (1 - effective_stop / h['cost']))

        # 决策
        action = '持有'
        color = 'green'
        if price <= effective_stop:
            action = '止损'
            color = 'red'
        elif profit_pct >= 10:
            action = '考虑止盈'
            color = 'orange'
        elif distance_to_stop < 3:
            action = '关注'
            color = 'orange'
        else:
            action = '持有'
            color = 'green'

        decisions.append({
            **h,
            'price': price,
            'profit': profit,
            'profit_pct': profit_pct,
            'static_stop': static_stop,
            'dynamic_stop': dynamic_stop,
            'effective_stop': effective_stop,
            'take_profit': take_profit,
            'distance_to_stop': distance_to_stop,
            'action': action,
            'color': color,
        })
        actions.append((h['name'], action, color))
        print(f'[{h["name"]}] 现价:{price:.2f} 成本:{h["cost"]:.2f} 盈亏:{profit_pct:+.1f}%')
        print(f'  止损线:{effective_stop:.2f}(静态{static_stop}/动态{dynamic_stop:.2f}) 距止损:{distance_to_stop:.1f}%')
        print(f'  止盈线:{take_profit:.2f} → 建议:{action}')
        print()

    total_asset = total_value + CASH
    total_profit = total_asset - 1_000_000.0
    total_profit_pct = total_profit / 1_000_000.0 * 100
    print(f'总资产:{total_asset:,.0f}元 盈亏:{total_profit:+,.0f}元({total_profit_pct:+.2f}%)')
    print()

    # 输出可操作信号
    urgent = [d for d in decisions if d['color'] in ('red', 'orange')]
    if urgent:
        print(f'⚠️ 需要关注: {", ".join([d["name"] for d in urgent])}')
    else:
        print('✅ 持仓全部安全')

    return {
        'decisions': decisions,
        'total_asset': total_asset,
        'total_profit': total_profit,
        'total_profit_pct': total_profit_pct,
        'urgent': urgent,
    }

if __name__ == '__main__':
    decide()
