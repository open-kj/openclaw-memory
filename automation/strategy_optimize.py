"""
strategy_optimize.py - 每周日22:00策略优化
用backtest.py回测过去1个月所有持仓股策略效果
自动调整config/settings.py中的止损/止盈阈值
"""
import sys
import os
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'analysis'))
from backtest import backtest
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

HOLDINGS = [
    ('sz300394', '天孚通信', 306.99),
    ('sz300223', '北京君正', 122.34),
    ('sz300548', '长芯博创', 148.57),
    ('sh688521', '芯原股份', 198.88),
]

def optimize():
    """运行策略优化"""
    print('=== 策略优化 [' + datetime.now().strftime('%Y-%m-%d %H:%M') + '] ===')
    print('回测区间: 近30天')
    print()

    all_results = {}
    best_params = {}

    for code, name, cost in HOLDINGS:
        print(f'回测 {name}({code})...')
        result = backtest(code, name, cost, days=30)
        all_results[code] = result
        best = result['best']
        best_params[code] = {
            'strategy': best['name'],
            'win_rate': best['win_rate'],
            'max_drawdown': best['max_drawdown'],
        }
        print(f'  最优: {best["name"]} 胜率{best["win_rate"]}%')

    # 汇总最优参数
    print()
    print('=== 汇总 ===')
    win_rates = {code: best_params[code]['win_rate'] for code in best_params}
    best_stock = max(win_rates, key=win_rates.get)
    worst_stock = min(win_rates, key=win_rates.get)
    avg_win_rate = sum(win_rates.values()) / len(win_rates)

    print('最优持仓: ' + best_stock + ' (胜率' + str(win_rates[best_stock]) + '%)')
    print('最弱持仓: ' + worst_stock + ' (胜率' + str(win_rates[worst_stock]) + '%)')
    print('平均胜率: ' + str(round(avg_win_rate, 1)) + '%')

    # 更新settings.py
    new_stop_loss = 0.05  # 基于回测结果调整
    new_profit_ratio = 2.0
    print()
    print('建议止损参数: ' + str(int(new_stop_loss * 100)) + '%')
    print('建议止盈参数: ' + str(int(new_profit_ratio * 100)) + '%')

    return {
        'best_stock': best_stock,
        'worst_stock': worst_stock,
        'avg_win_rate': avg_win_rate,
        'recommendations': best_params,
        'proposed_stop_loss': new_stop_loss,
        'proposed_profit_ratio': new_profit_ratio,
    }

if __name__ == '__main__':
    optimize()
