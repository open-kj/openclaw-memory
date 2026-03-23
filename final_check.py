import urllib.request
import sys
sys.stdout.reconfigure(encoding='utf-8')

stocks = ['sz300394', 'sh688521', 'sz002594']
names = {'sz300394': '天孚通信', 'sh688521': '芯原股份', 'sz002594': '比亚迪'}
stops = {'sz300394': 291.64, 'sh688521': 188.94, 'sz002594': 103.45}
costs = {'sz300394': 306.99, 'sh688521': 198.88, 'sz002594': 108.89}
qtys = {'sz300394': 618, 'sh688521': 1000, 'sz002594': 3200}

print("=== 持仓市值计算 ===")
total_value = 0
total_cost = 0
total_pnl = 0
for code in stocks:
    url = f'https://qt.gtimg.cn/q={code}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 10:
                price = float(parts[3])
                qty = qtys[code]
                cost = costs[code]
                value = price * qty
                cost_total = cost * qty
                pnl = value - cost_total
                total_value += value
                total_cost += cost_total
                total_pnl += pnl
                print(f"{names[code]}: 数量={qty}, 成本={cost}, 现价={price}, 市值={value:.0f}, 盈亏={pnl:.0f}")
    except Exception as e:
        print(f"{code}: 获取失败 {e}")

cash = 260995  # 买入比亚迪后剩余现金
total = total_value + cash
start = 1000000

print(f"\n=== 账户总览 ===")
print(f"持仓总市值: {total_value:.0f}")
print(f"现金: {cash:.0f}")
print(f"总资产: {total:.0f}")
print(f"起始资金: {start:.0f}")
print(f"累计盈亏: {total-start:.0f} ({((total-start)/start)*100:+.2f}%)")
