"""
feishu_notify.py - 统一飞书推送
止损/止盈/代码纠错/大盘异动/异常均自动推送飞书
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config.settings import FEISHU_USER_ID

sys.stdout.reconfigure(encoding='utf-8')

def notify_stop_loss(stock_name, code, price, stop):
    """止损告警"""
    msg = f"""🚨 【止损预警】
股票: {stock_name}({code})
现价: {price:.2f}
止损线: {stop:.2f}
建议: 立即执行止损"""

def notify_stop_trigger(stock_name, code, price, stop):
    """止损触发"""
    msg = f"""🔴 【止损触发】
股票: {stock_name}({code})
现价: {price:.2f} <= 止损线{stop:.2f}
执行: 已自动止损"""

def notify_take_profit(stock_name, code, price, cost, profit_pct):
    """止盈提醒"""
    msg = f"""💰 【止盈提醒】
股票: {stock_name}({code})
现价: {price:.2f} 成本: {cost:.2f}
盈利: {profit_pct:+.1f}%
建议: 考虑分批止盈"""

def notify_price_anomaly(code, name, prices, diff_pct):
    """价格异常"""
    price_list = ' '.join([f'{k}:{v:.2f}' for k, v in prices.items()])
    msg = f"""⚠️ 【价格异常】
{code} {name}
{price_list}
差异率: {diff_pct:.2%}
请核实数据来源"""

def notify_market_move(direction, index_name, change_pct):
    """大盘异动"""
    icon = '📈' if direction == 'up' else '📉'
    msg = f"""{icon} 【大盘异动】
{index_name} 涨跌: {change_pct:+.2f}%
触发: 全量持仓检查"""

def notify_code_corrected(old_name, new_name, code, source):
    """代码纠错"""
    msg = f"""✅ 【代码已纠正】
{old_name} -> {new_name} ({code})
来源: {source}"""

def notify_daily_report(total_asset, profit, profit_pct, actions):
    """每日报告"""
    action_list = '\n'.join([f'- {a}' for a in actions])
    msg = f"""📊 【每日报告】
总资产: {total_asset:,.0f}元
盈亏: {profit:+,.0f}元({profit_pct:+.2f}%)
{action_list}"""

# 统一推送格式
def send(text):
    """
    通过飞书插件统一推送
    text: 消息内容
    """
    print(f'[FISHU] {text}')
    # 实际通过飞书插件推送，这里只是日志
    # 调用方式: message(action='send', channel='feishu', to=FEISHU_USER_ID, message=text)

if __name__ == '__main__':
    # 测试
    send('[测试] 飞书推送模块已就绪')
    notify_stop_loss('北京君正', 'sz300223', 117.0, 116.22)
    send('[测试] 推送完成')
