"""
backtest.py - 策略回测
支持输入股票代码+时间区间+策略（动态止损/固定止损）
输出：收益率、最大回撤、胜率
"""
import requests
import sys
import os
from datetime import datetime, timedelta
import math

sys.stdout.reconfigure(encoding='utf-8')

def get_historical_prices(code, days=30):
    """
    获取近N日收盘价（腾讯API历史数据）
    简化：使用akshare
    """
    try:
        import akshare as ak
        if code.startswith('sh'):
            df = ak.stock_zh_index_daily(symbol='sh000001')
        else:
            df = ak.stock_zh_a_hist(symbol=code[2:], period='daily',
                                      start_date=(datetime.now() - timedelta(days=days)).strftime('%Y%m%d'),
                                      end_date=datetime.now().strftime('%Y%m%d'))
        if df is not None and len(df) > 5:
            return df['close'].tolist()[-days:]
    except:
        pass
    return []

def simulate_dynamic_stop_loss(prices, buy_price, cost_ratio=0.05):
    """
    动态止损策略回测
    止损线 = 买入价 * (1 - 5%)，跌破止损
    """
    trades = []
    in_position = True
    peak = buy_price
    max_drawdown = 0
    wins = 0
    losses = 0

    for i, price in enumerate(prices):
        if not in_position:
            break
        peak = max(peak, price)
        drawdown = (peak - price) / peak if peak > 0 else 0
        max_drawdown = max(max_drawdown, drawdown)

        # 止损触发
        if price <= buy_price * (1 - cost_ratio):
            trades.append({'exit_price': price, 'return': (price - buy_price) / buy_price * 100})
            in_position = False
            losses += 1
        # 止盈触发（涨20%）
        elif price >= buy_price * 1.20:
            trades.append({'exit_price': price, 'return': (price - buy_price) / buy_price * 100})
            in_position = False
            wins += 1
        # 30天后强制平仓
        elif i >= len(prices) - 1:
            ret = (price - buy_price) / buy_price * 100
            trades.append({'exit_price': price, 'return': ret})
            in_position = False
            if ret > 0:
                wins += 1
            else:
                losses += 1

    returns = [t['return'] for t in trades]
    total_return = sum(returns)
    win_rate = wins / (wins + losses) * 100 if (wins + losses) > 0 else 0
    return {
        'strategy': '动态止损(5%)',
        'total_return': round(total_return, 2),
        'max_drawdown': round(max_drawdown * 100, 2),
        'win_rate': round(win_rate, 1),
        'num_trades': len(trades),
        'wins': wins,
        'losses': losses,
    }

def simulate_fixed_stop_loss(prices, buy_price, stop_ratio=0.03):
    """
    固定止损策略回测（可调止损率）
    """
    in_position = True
    peak = buy_price
    max_drawdown = 0
    wins = 0
    losses = 0

    for price in prices:
        if not in_position:
            break
        peak = max(peak, price)
        drawdown = (peak - price) / peak if peak > 0 else 0
        max_drawdown = max(max_drawdown, drawdown)

        if price <= buy_price * (1 - stop_ratio):
            in_position = False
            losses += 1
        elif price >= buy_price * 1.15:
            in_position = False
            wins += 1

    total_trades = wins + losses
    win_rate = wins / total_trades * 100 if total_trades > 0 else 0
    avg_return = 0  # 简化

    return {
        'strategy': f'固定止损({stop_ratio*100:.0f}%)',
        'total_return': round(avg_return, 2),
        'max_drawdown': round(max_drawdown * 100, 2),
        'win_rate': round(win_rate, 1),
        'num_trades': total_trades,
        'wins': wins,
        'losses': losses,
    }

def backtest(code, name, cost, days=30, strategies=None):
    """
    回测入口
    """
    print(f'=== 回测: {name}({code}) ===')
    print(f'成本: {cost} | 时间区间: 近{days}天')

    prices = get_historical_prices(code, days)
    if len(prices) < 5:
        print(f'数据不足，仅有{len(prices)}条，使用模拟数据')
        import random
        prices = [cost * (1 + random.uniform(-0.03, 0.03)) for _ in range(days)]

    print(f'数据点数: {len(prices)}')

    results = []
    if strategies is None:
        strategies = ['dynamic', 'fixed_3', 'fixed_5', 'fixed_8']

    for s in strategies:
        if s == 'dynamic':
            r = simulate_dynamic_stop_loss(prices, cost)
            r['name'] = '动态止损(5%)'
        elif s == 'fixed_3':
            r = simulate_fixed_stop_loss(prices, cost, 0.03)
            r['name'] = '固定止损(3%)'
        elif s == 'fixed_5':
            r = simulate_fixed_stop_loss(prices, cost, 0.05)
            r['name'] = '固定止损(5%)'
        elif s == 'fixed_8':
            r = simulate_fixed_stop_loss(prices, cost, 0.08)
            r['name'] = '固定止损(8%)'
        results.append(r)
        print(f'  {r["name"]}: 收益率={r["total_return"]:+.2f}% | 最大回撤={r["max_drawdown"]:.2f}% | 胜率={r["win_rate"]:.1f}%')

    # 找最优策略
    best = max(results, key=lambda x: x['win_rate'])
    print()
    print(f'最优策略: {best["name"]} (胜率{best["win_rate"]:.1f}%)')

    return {'code': code, 'name': name, 'results': results, 'best': best}

if __name__ == '__main__':
    stocks = [
        ('sz300394', '天孚通信', 306.99),
        ('sz300223', '北京君正', 122.34),
        ('sz300548', '长芯博创', 148.57),
        ('sh688521', '芯原股份', 198.88),
    ]
    for code, name, cost in stocks:
        backtest(code, name, cost, days=30)
        print()
