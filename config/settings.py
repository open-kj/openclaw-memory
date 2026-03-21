"""
settings.py - 全局参数配置
"""
import os

BASE_DIR = r'C:\Users\Administrator\.openclaw\workspace'
DATA_DIR = os.path.join(BASE_DIR, 'data')
ANALYSIS_DIR = os.path.join(BASE_DIR, 'analysis')
AUTOMATION_DIR = os.path.join(BASE_DIR, 'automation')
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')
UTILS_DIR = os.path.join(BASE_DIR, 'utils')

# API Keys
TAVILY_API_KEY = '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'

# Feishu
FEISHU_USER_ID = 'ou_7f6d33164c200178d4c1563469f9343d'

# 交易参数
INITIAL_CAPITAL = 1_000_000.0
MAX_POSITION_RATIO = 0.20  # 单只仓位上限20%
MAX_TOTAL_POSITION = 0.90  # 总仓位上限90%
MIN_CASH_RATIO = 0.10     # 最低现金保留10%

# 止损止盈
DEFAULT_STOP_LOSS = 0.05   # 默认止损5%
DYNAMIC_STOP_LOSS_MIN = 0.03  # 动态止损下限3%
DYNAMIC_STOP_LOSS_MAX = 0.08  # 动态止损上限8%
STOP_PROFIT_RATIO = 2.0   # 止盈=2倍止损

# 价格验证
PRICE_DIFF_THRESHOLD = 0.005  # 交叉验证差异>0.5%告警

# 调度优先级
HIGH_PRIORITY_INTERVAL = 600   # 高优先级(炬芯)每10分钟
NORMAL_PRIORITY_INTERVAL = 1800  # 普通每30分钟
MARKET_CHANGE_THRESHOLD = 0.015  # 大盘涨跌>1.5%触发全量检查

# 文件
SESSION_STATE_FILE = os.path.join(BASE_DIR, 'SESSION-STATE.md')
MEMORY_FILE = os.path.join(BASE_DIR, 'MEMORY.md')
HOLDINGS_FILE = os.path.join(CONFIG_DIR, 'holdings.yaml')

# 日志
LOG_FILE = os.path.join(LOGS_DIR, 'heartbeat.log')
