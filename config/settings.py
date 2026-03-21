"""
settings.py - 全局参数配置 v2.0
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

# ============ 仓位风控（v2.0新增）============
INITIAL_CAPITAL = 1_000_000.0
MAX_POSITION_PER_STOCK = 0.30    # 单只股票仓位≤30%
MAX_POSITION_INDUSTRY = 0.50     # 单一行业仓位≤50%
MAX_TOTAL_POSITION = 1.00         # 总仓位≤100%
MIN_CASH_RATIO = 0.10           # 最低现金保留10%
# ===========================================

# ============ 止损止盈 =============
DEFAULT_STOP_LOSS = 0.05   # 默认止损5%
DYNAMIC_STOP_LOSS_MIN = 0.03  # 动态止损下限3%
DYNAMIC_STOP_LOSS_MAX = 0.08  # 动态止损上限8%
STOP_PROFIT_RATIO = 2.0   # 止盈=2倍止损
# ===========================================

# ============ 价格验证 =============
PRICE_DIFF_THRESHOLD = 0.005  # 交叉验证差异>0.5%告警
# ===========================================

# ============ 资金流 =============
MONEY_FLOW_ALERT_THRESHOLD = 0.05  # 主力净流入/流出>5%触发告警
NORTH_SOUTH_FLOW_THRESHOLD = 50e8  # 北向资金单日>50亿触发大盘异动
# ===========================================

# ============ 调度优先级 =============
HIGH_PRIORITY_INTERVAL = 600   # 高优先级(北京君正)每10分钟
NORMAL_PRIORITY_INTERVAL = 1800  # 普通每30分钟
MARKET_CHANGE_THRESHOLD = 0.015  # 大盘涨跌>1.5%触发全量检查
# ===========================================

# ============ 舆情 =============
SENTIMENT_NEGATIVE_THRESHOLD = 0.60  # 舆情负面>60%触发风险提示
# ===========================================

# ============ 多因子评分 =============
FACTOR_SCORE_BUY = 8.0   # 评分≥8建议买入
FACTOR_SCORE_SELL = 3.0  # 评分≤3建议卖出
# ===========================================

# ============ 熔断 =============
CIRCUIT_BREAKER_ERRORS = 3       # 同一模块1小时内≥3次报错触发熔断
CIRCUIT_BREAKER_WINDOW = 3600   # 熔断时间窗口（秒）
# ===========================================

# ============ 健康度 =============
HEALTH_SCORE_WARNING = 80  # 健康度<80分触发告警
# ===========================================

# ============ 文件路径 =============
SESSION_STATE_FILE = os.path.join(BASE_DIR, 'SESSION-STATE.md')
MEMORY_FILE = os.path.join(BASE_DIR, 'MEMORY.md')
HOLDINGS_FILE = os.path.join(CONFIG_DIR, 'holdings.yaml')
# ===========================================

# ============ 日志 =============
LOG_FILE = os.path.join(LOGS_DIR, 'heartbeat.log')
WAL_LOG = os.path.join(LOGS_DIR, 'wal.log')
# ===========================================
