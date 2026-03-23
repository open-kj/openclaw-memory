# 候选股票池 - 扩大版
# 最后更新: 2026-03-23

# === 板块分类 ===

# 1. 光模块/AI算力（核心赛道）
OPTICAL = {
    'sz300394': {'name': '天孚通信', 'exchange': 'SZ', 'pe_max': 150},
    'sz300308': {'name': '中际旭创', 'exchange': 'SZ', 'pe_max': 150},
    'sz300502': {'name': '新易盛', 'exchange': 'SZ', 'pe_max': 150},
}

# 2. 半导体/IP（RISC-V/AI芯片）
CHIP = {
    'sh688521': {'name': '芯原股份', 'exchange': 'SH', 'pe_max': 180},
    'sh688256': {'name': '寒武纪', 'exchange': 'SH', 'pe_max': 180},
    'sh688981': {'name': '中芯国际', 'exchange': 'SH', 'pe_max': 100},
    'sz002371': {'name': '北方华创', 'exchange': 'SZ', 'pe_max': 150},
}

# 3. 新能源整车（扩展赛道）
EV = {
    'sz002594': {'name': '比亚迪', 'exchange': 'SZ', 'pe_max': 50},
    'sz300750': {'name': '宁德时代', 'exchange': 'SZ', 'pe_max': 60},
    'sh986633': {'name': '理想汽车', 'exchange': 'SH', 'pe_max': 80},
    'sh986803': {'name': '蔚来', 'exchange': 'SH', 'pe_max': 80},
    'sh987033': {'name': '小鹏汽车', 'exchange': 'SH', 'pe_max': 80},
}

# 4. 智能驾驶/传感器
AUTO = {
    'sz002920': {'name': '德赛西威', 'exchange': 'SZ', 'pe_max': 80},
    'sh688638': {'name': '威迈斯', 'exchange': 'SH', 'pe_max': 60},
}

# 5. 模拟芯片（稀缺标的）
ANALOG = {
    'sz300661': {'name': '圣邦股份', 'exchange': 'SZ', 'pe_max': 150},
    'sz002049': {'name': '紫光国微', 'exchange': 'SZ', 'pe_max': 100},
}

# 6. GPU/AI服务器
GPU = {
    'sz000977': {'name': '浪潮信息', 'exchange': 'SZ', 'pe_max': 80},
    'sh688039': {'name': '当虹科技', 'exchange': 'SH', 'pe_max': 100},
}

# === 全部合并 ===
ALL = {}
for pool in [OPTICAL, CHIP, EV, AUTO, ANALOG, GPU]:
    ALL.update(pool)

# === 筛选条件 ===
FILTER_RULES = {
    'max_loss_52w': 15,       # 距52周低点不超过15%（禁止接飞刀）
    'max_today_loss': 8,      # 今日跌幅不超过8%（不接暴跌股）
    'min_vol': 100000,       # 最小成交量（万元）
}

print(f"候选池总计: {len(ALL)} 只股票")
for name, code in sorted([(v['name'], k) for k, v in ALL.items()]):
    print(f"  {name} ({code})")
