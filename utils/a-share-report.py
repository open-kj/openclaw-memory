"""
用法: python a-share-report.py [YYYY-MM-DD]
"""
import requests
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding='utf-8')

HOLDINGS = {
    'sz300394': {'name': '天孚通信', 'cost': 306.99, 'qty': 618, 'stop': 291.64},
    'sz300223': {'name': '炬芯科技', 'cost': 122.34, 'qty': 1530, 'stop': 116.22},
    'sz300548': {'name': '博创科技', 'cost': 148.57, 'qty': 1000, 'stop': 141.14},
    'sh688521': {'name': '源杰股份', 'cost': 198.88, 'qty': 1000, 'stop': 188.94},
}
CASH = 294992.0
INITIAL_CAPITAL = 1000000.0

def get_index():
    try:
        r = requests.get('https://qt.gtimg.cn/q=sh000001,sz399001,sz399006', timeout=8)
        result = {}
        for line in r.text.strip().split('\n'):
            parts = line.split('~')
            if len(parts) > 35:
                code = parts[2]
                result[code] = {'name': parts[1], 'price': float(parts[3]), 'chg_pct': float(parts[32])}
        return result
    except:
        return {}

def get_holdings_price():
    codes = ','.join(HOLDINGS.keys())
    try:
        r = requests.get(f'https://qt.gtimg.cn/q={codes}', timeout=8)
        result = {}
        for line in r.text.strip().split('\n'):
            parts = line.split('~')
            if len(parts) > 35:
                raw = parts[2]
                if raw.startswith('1') or raw.startswith('3'):
                    code = 'sz' + raw
                elif raw.startswith('6'):
                    code = 'sh' + raw
                else:
                    code = raw
                result[code] = {'name': parts[1], 'price': float(parts[3]), 'chg_pct': float(parts[32]), 'prev_close': float(parts[4])}
        return result
    except:
        return {}

def get_top_gainers():
    try:
        r = requests.get('https://money.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeDataSimple?page=1&num=20&sort=changepercent&asc=0&node=hs_a', timeout=8)
        data = r.json()
        result = []
        for d in data[:20]:
            try:
                chg = float(d.get('changepercent', 0))
                if chg > 3:
                    result.append({'name': d['name'], 'symbol': d['symbol'], 'chg_pct': chg, 'price': float(d.get('trade', 0))})
            except:
                pass
        return result
    except:
        return []

def get_ipo_calendar():
    try:
        import akshare as ak, warnings
        warnings.filterwarnings('ignore')
        df = ak.stock_new_ipo_cninfo()
        df['申购日期'] = df['申购日期'].astype(str)
        today = datetime.now().strftime('%Y-%m-%d')[:10]
        upcoming = df[df['申购日期'] >= today].head(6)
        result = []
        for _, r in upcoming.iterrows():
            try:
                price = float(r.iloc[4]) if str(r.iloc[4]) not in ('nan','') else None
                price_str = f'{price:.2f}元' if price else '待定'
            except:
                price_str = '待定'
            result.append({'code': str(r.iloc[0]), 'name': str(r.iloc[1]), 'apply_date': r['申购日期'], 'price': price_str})
        return result
    except:
        return []

def generate_report(date=None):
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    index = get_index()
    holdings = get_holdings_price()
    gainers = get_top_gainers()
    ipo = get_ipo_calendar()

    hold_mv = 0
    hold_lines = []
    for code, cfg in HOLDINGS.items():
        if code in holdings:
            d = holdings[code]
            mv = d['price'] * cfg['qty']
            pnl = mv - cfg['cost'] * cfg['qty']
            pnl_pct = (d['price'] - cfg['cost']) / cfg['cost'] * 100
            stop_margin = (d['price'] - cfg['stop']) / cfg['stop'] * 100
            arrow = '▲' if pnl >= 0 else '▼'
            icon = '⚠️' if stop_margin < 5 else '✅'
            hold_lines.append({'code': code, 'name': cfg['name'], 'price': d['price'], 'chg_pct': d['chg_pct'], 'mv': mv, 'pnl': pnl, 'pnl_pct': pnl_pct, 'stop': cfg['stop'], 'stop_margin': stop_margin, 'arrow': arrow, 'icon': icon})
            hold_mv += mv
        else:
            hold_lines.append({'code': code, 'name': cfg['name'], 'price': 0, 'chg_pct': 0, 'mv': 0, 'pnl': 0, 'pnl_pct': 0, 'stop': cfg['stop'], 'stop_margin': -999, 'arrow': '?', 'icon': '❌'})

    total_assets = hold_mv + CASH
    total_pnl = total_assets - INITIAL_CAPITAL
    pnl_pct = total_pnl / INITIAL_CAPITAL * 100
    total_cost = sum(cfg['cost'] * cfg['qty'] for cfg in HOLDINGS.values())

    report = f"""# A股每日分析报告
**日期**: {date}
**生成时间**: {datetime.now().strftime('%H:%M')}

---

## 一，大盘指数

| 指数 | 代码 | 收盘价 | 涨跌幅 |
|------|------|--------|--------|
"""
    for code, d in index.items():
        arrow = '▲' if d['chg_pct'] > 0 else '▼'
        cp = f'+{d["chg_pct"]:.2f}%' if d['chg_pct'] > 0 else f'{d["chg_pct"]:.2f}%'
        report += f"| {d['name']} | {code} | {d['price']:.2f} | {arrow}{cp} |\n"

    report += "\n---\n\n## 二，持仓分析\n\n"
    for h in hold_lines:
        if h['price'] > 0:
            stop_str = f"止损{abs(h['stop_margin']):.1f}%" if h['stop_margin'] > 0 else '跌破止损!'
            chg_str = f"{h['arrow']}{abs(h['pnl_pct']):.2f}%"
            report += f"""### {h['name']} ({h['code']})
- **现价**: {h['price']:.2f} ({h['chg_pct']:+.2f}%)
- **持仓市值**: {h['mv']:,.0f}元
- **盈亏**: {h['pnl']:+,.0f}元 ({chg_str})
- **止损线**: {h['stop']:.2f} | {h['icon']} {stop_str}

"""
        else:
            report += f"### {h['name']} ({h['code']})\n- **状态**: 数据获取失败\n\n"

    asset_pnl_str = f"{'+' if total_pnl >= 0 else ''}{total_pnl:,.0f}元"
    report += f"""
| 项目 | 金额 |
|------|------|
| 持仓总市值 | {hold_mv:,.0f}元 |
| 持仓总成本 | {total_cost:,.0f}元 |
| 现金 | {CASH:,.0f}元 |
| **总资产** | **{total_assets:,.0f}元** |
| **总盈亏** | **{asset_pnl_str} ({'+' if pnl_pct >= 0 else ''}{pnl_pct:.2f}%)** |

---

## 三，今日强势板块

"""
    if gainers:
        report += '| 股票 | 代码 | 涨幅 | 现价 |\n|------|------|------|------|\n'
        for g in gainers[:10]:
            report += f"| {g['name']} | {g['symbol']} | +{g['chg_pct']:.2f}% | {g['price']:.2f} |\n"
    else:
        report += "暂无数据\n"

    report += "\n---\n\n## 四，新股日历\n\n"
    if ipo:
        for item in ipo:
            report += f"- **{item['name']}** ({item['code']}) | 申购: {item['apply_date']} | {item['price']}\n"
    else:
        report += "暂无新股数据\n"

    warns = [h for h in hold_lines if 0 < h['stop_margin'] < 5]
    report += "\n---\n\n## 五，明日操作建议\n\n"
    if warns:
        for h in sorted(warns, key=lambda x: x['stop_margin']):
            report += f"⚠️ **{h['name']}** 安全边际仅{h['stop_margin']:.1f}%，明日重点关注\n"
    else:
        report += "✅ 所有持仓安全边际充足，正常持有\n"

    report += """
---

*本报告由AI自动生成 | 数据来源：腾讯财经、akshare、新浪财经 | 仅供参考，不构成投资建议*
"""
    return report

if __name__ == '__main__':
    date = sys.argv[1] if len(sys.argv) > 1 else None
    report = generate_report(date)
    print(report)
