"""
nlp_interaction.py - 自然语言指令解析
支持自然语言指令，自动解析为对应函数调用
"""
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
sys.path_insert = sys.path.insert

sys.stdout.reconfigure(encoding='utf-8')

# 指令映射表
COMMANDS = {
    '分析': 'analyze_stock',
    '查看': 'check_data',
    '回测': 'run_backtest',
    '持仓': 'show_holdings',
    '止损': 'check_stop_loss',
    '资金': 'show_money_flow',
    '北向': 'show_north_flow',
    '大盘': 'show_market',
    '新闻': 'show_news',
    '评分': 'ai_factor_score',
}

def parse_command(text):
    """解析自然语言指令"""
    text = text.strip()

    # 匹配置信令词
    for kw, fn in COMMANDS.items():
        if kw in text:
            return fn, text

    # 默认返回帮助
    return 'help', text

def execute(cmd, text):
    """执行指令"""
    if cmd == 'analyze_stock':
        # 提取股票名称或代码
        code = extract_code(text)
        if code:
            return run_analysis(code)
        return '未识别股票代码，请明确说出股票名称或代码'

    elif cmd == 'run_backtest':
        code = extract_code(text)
        days = extract_days(text)
        if code:
            return run_backtest_cmd(code, days)
        return '未识别股票代码'

    elif cmd == 'show_holdings':
        return show_holdings_cmd()

    elif cmd == 'check_stop_loss':
        code = extract_code(text)
        if code:
            return check_stop_loss_cmd(code)
        return '未识别股票代码'

    elif cmd == 'show_money_flow':
        code = extract_code(text)
        if code:
            return show_money_flow_cmd(code)
        return show_all_money_flow_cmd()

    elif cmd == 'show_north_flow':
        return show_north_flow_cmd()

    elif cmd == 'show_market':
        return show_market_cmd()

    elif cmd == 'show_news':
        cat = 'all'
        if '财经' in text or 'A股' in text:
            cat = 'finance'
        elif '科技' in text:
            cat = 'tech'
        elif '军事' in text or '军工' in text:
            cat = 'military'
        return show_news_cmd(cat)

    elif cmd == 'ai_factor_score':
        code = extract_code(text)
        if code:
            return run_ai_factor_cmd(code)
        return '未识别股票代码'

    return '未知指令，请使用：分析/查看/回测/持仓/止损/资金/北向/大盘/新闻/评分'

def extract_code(text):
    """从文本提取股票代码"""
    # 6位数字代码
    m = re.search(r'\b(\d{6})\b', text)
    if m:
        num = m.group(1)
        return ('sh' if num.startswith(('6', '5')) else 'sz') + num

    # 名称映射
    name_map = {
        '天孚': 'sz300394', '北京君正': 'sz300223',
        '长芯博创': 'sz300548', '芯原': 'sh688521',
        '炬芯': 'sh688049',
    }
    for name, code in name_map.items():
        if name in text:
            return code
    return None

def extract_days(text):
    m = re.search(r'(\d+)天', text)
    return int(m.group(1)) if m else 30

def run_analysis(code):
    try:
        from analysis.ai_factor_analysis import calc_score
        names = {'sz300394': '天孚通信', 'sz300223': '北京君正',
                 'sz300548': '长芯博创', 'sh688521': '芯原股份', 'sh688049': '炬芯科技'}
        name = names.get(code, code)
        result = calc_score(code, name, 0)
        return '{}: {}/10 → {}\n因子: {}\n原因: {}'.format(
            name, result['score'], result['advice'],
            result['factors'], ', '.join(result['reasons']))
    except Exception as e:
        return '分析失败: ' + str(e)

def run_backtest_cmd(code, days):
    try:
        from analysis.backtest import backtest
        names = {'sz300394': ('天孚通信', 306.99), 'sz300223': ('北京君正', 122.34),
                  'sz300548': ('长芯博创', 148.57), 'sh688521': ('芯原股份', 198.88)}
        name, cost = names.get(code, (code, 100))
        result = backtest(code, name, cost, days=days)
        best = result['best']
        return '{}回测({}天): 最优策略={} 胜率={}% 最大回撤={}%'.format(
            name, days, best['name'], best['win_rate'], best['max_drawdown'])
    except Exception as e:
        return '回测失败: ' + str(e)

def show_holdings_cmd():
    return ('持仓:\n- 天孚通信 sz300394 成本306.99\n- 北京君正 sz300223 成本122.34\n'
            '- 长芯博创 sz300548 成本148.57\n- 芯原股份 sh688521 成本198.88\n现金: 294,992元')

def check_stop_loss_cmd(code):
    stops = {'sz300394': 291.64, 'sz300223': 116.22, 'sz300548': 141.14, 'sh688521': 188.94}
    stop = stops.get(code, 'N/A')
    return '止损线: ' + str(stop)

def show_money_flow_cmd(code):
    try:
        from data.capital_flow import get_money_flow
        d = get_money_flow(code)
        if d and 'error' not in d:
            return '主力净流入: {:.1f}万元 净流入率: {:.2f}%'.format(d['main_net_m'], d['main_rate'])
    except:
        pass
    return '获取资金流失败'

def show_all_money_flow_cmd():
    from data.capital_flow import get_money_flow
    stocks = [('sz300394','天孚'),('sz300223','北京君正'),('sz300548','长芯博创'),('sh688521','芯原')]
    lines = ['资金流:']
    for code, name in stocks:
        d = get_money_flow(code)
        if d and 'error' not in d:
            lines.append('  {}: {:.1f}万元({:.2f}%)'.format(name, d['main_net_m'], d['main_rate']))
    return '\n'.join(lines)

def show_north_flow_cmd():
    try:
        from data.capital_flow import get_north_south_flow
        d = get_north_south_flow()
        if d:
            return '北向资金净买入: {:.2f}亿元'.format(d['north_buy_yi'])
    except:
        return '获取北向资金数据失败'

def show_market_cmd():
    try:
        from data.market_data import get_indices
        idx = get_indices()
        lines = ['大盘:']
        for code, data in idx.items():
            lines.append('  {}: {:.2f}({:+.2f}%)'.format(data['name'], data['price'], data['chg']))
        return '\n'.join(lines)
    except:
        return '获取大盘数据失败'

def show_news_cmd(category):
    try:
        from utils.news_aggregator import run
        import io
        old = sys.stdout
        sys.stdout = io.StringIO()
        run(category)
        output = sys.stdout.getvalue()
        sys.stdout = old
        return output[:800]
    except:
        return '获取新闻失败'

def run_ai_factor_cmd(code):
    return run_analysis(code)

if __name__ == '__main__':
    tests = [
        '分析北京君正',
        '查看北向资金',
        '回测天孚通信近1个月',
        '显示大盘情况',
        '新闻 财经',
        '评分 芯原股份',
    ]
    for t in tests:
        cmd, _ = parse_command(t)
        print('>>> ' + t)
        print(execute(cmd, t))
        print()
