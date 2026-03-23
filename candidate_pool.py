# 候选股票池 - 扩大版（50只）
# 最后更新: 2026-03-23
# 板块覆盖：光模块/半导体/新能源/AI/消费/医药/军工

# === 1. 光模块/AI算力（5只）===
OPTICAL = {
    'sz300394': {'name': '天孚通信', 'pe_max': 150},
    'sz300308': {'name': '中际旭创', 'pe_max': 150},
    'sz300502': {'name': '新易盛', 'pe_max': 150},
    'sh688027': {'name': '德科立', 'pe_max': 150},
    'sz300570': {'name': '太辰光', 'pe_max': 150},
}

# === 2. 半导体/IP/AI芯片（8只）===
CHIP = {
    'sh688521': {'name': '芯原股份', 'pe_max': 180},
    'sh688256': {'name': '寒武纪', 'pe_max': 200},
    'sh688981': {'name': '中芯国际', 'pe_max': 100},
    'sz002371': {'name': '北方华创', 'pe_max': 150},
    'sz002049': {'name': '紫光国微', 'pe_max': 100},
    'sh688396': {'name': '华润微', 'pe_max': 80},
    'sz300661': {'name': '圣邦股份', 'pe_max': 150},
    'sh688008': {'name': '澜起科技', 'pe_max': 120},
}

# === 3. 新能源整车（5只）===
EV = {
    'sz002594': {'name': '比亚迪', 'pe_max': 50},
    'sz300750': {'name': '宁德时代', 'pe_max': 60},
    'sh986633': {'name': '理想汽车', 'pe_max': 80},
    'sh986803': {'name': '蔚来', 'pe_max': 80},
    'sh987033': {'name': '小鹏汽车', 'pe_max': 80},
}

# === 4. 锂电/电池/储能（4只，去重）===
BATTERY = {
    'sz300014': {'name': '亿纬锂能', 'pe_max': 60},
    'sz002812': {'name': '恩捷股份', 'pe_max': 80},
    'sz300207': {'name': '欣旺达', 'pe_max': 60},
    'sh688005': {'name': '容百科技', 'pe_max': 80},
}

# === 5. 智能驾驶/传感器（5只）===
AUTO = {
    'sz002920': {'name': '德赛西威', 'pe_max': 80},
    'sh688638': {'name': '威迈斯', 'pe_max': 60},
    'sz002536': {'name': '飞龙股份', 'pe_max': 60},
    'sh688220': {'name': '翱捷科技', 'pe_max': 100},
    'sz300496': {'name': '中科创达', 'pe_max': 100},
}

# === 6. AI应用/软件（5只）===
AI_APP = {
    'sz300496': {'name': '中科创达', 'pe_max': 100},
    'sz002230': {'name': '科大讯飞', 'pe_max': 150},
    'sh688111': {'name': '金山办公', 'pe_max': 150},
    'sz300033': {'name': '同花顺', 'pe_max': 100},
    'sh688318': {'name': '财富趋势', 'pe_max': 100},
}

# === 7. 消费电子/苹果链（5只）===
ELECTRONICS = {
    'sz002475': {'name': '立讯精密', 'pe_max': 60},
    'sz002241': {'name': '歌尔股份', 'pe_max': 60},
    'sh601138': {'name': '工业富联', 'pe_max': 50},
    'sz002600': {'name': '领益智造', 'pe_max': 60},
    'sh603986': {'name': '兆易创新', 'pe_max': 100},
}

# === 8. 医药/医疗（5只）===
MEDICAL = {
    'sz300760': {'name': '迈瑞医疗', 'pe_max': 80},
    'sh688278': {'name': '特宝生物', 'pe_max': 100},
    'sz002007': {'name': '华兰生物', 'pe_max': 60},
    'sh688180': {'name': '君实生物', 'pe_max': 200},
    'sz300529': {'name': '健帆生物', 'pe_max': 80},
}

# === 9. 军工/航天（5只）===
MILITARY = {
    'sz002025': {'name': '航天电器', 'pe_max': 80},
    'sh600893': {'name': '航发动力', 'pe_max': 150},
    'sz002013': {'name': '中航机电', 'pe_max': 80},
    'sh688185': {'name': '康希通信', 'pe_max': 100},
    'sz300719': {'name': '安达维尔', 'pe_max': 80},
}

# === 10. 食品饮料/白酒（4只）===
FOOD = {
    'sh600519': {'name': '贵州茅台', 'pe_max': 50},
    'sz000858': {'name': '五粮液', 'pe_max': 40},
    'sh603288': {'name': '海天味业', 'pe_max': 60},
    'sz002714': {'name': '牧原股份', 'pe_max': 50},
}

# === 11. 游戏/传媒（3只）===
GAME = {
    'sz002555': {'name': '三七互娱', 'pe_max': 30},
    'sh603444': {'name': '吉比特', 'pe_max': 30},
    'sz300418': {'name': '昆仑万维', 'pe_max': 60},
}

# === 全部合并 ===
ALL = {}
for pool in [OPTICAL, CHIP, EV, BATTERY, AUTO, AI_APP, ELECTRONICS, MEDICAL, MILITARY, FOOD, GAME]:
    ALL.update(pool)

# === 筛选条件 ===
FILTER_RULES = {
    'max_loss_52w': 15,       # 距52周低点不超过15%
    'max_today_loss': 8,      # 今日跌幅不超过8%
    'min_vol': 100000,        # 最小成交量（万元）
    'pe_max': 200,            # PE上限
}

# 输出统计
print(f"候选池总计: {len(ALL)} 只股票")
print(f"\n板块分布:")
pools = {
    '光模块/AI算力': OPTICAL,
    '半导体/IP': CHIP,
    '新能源整车': EV,
    '锂电/电池': BATTERY,
    '智能驾驶': AUTO,
    'AI应用': AI_APP,
    '消费电子': ELECTRONICS,
    '医药/医疗': MEDICAL,
    '军工/航天': MILITARY,
    '食品饮料': FOOD,
    '游戏/传媒': GAME,
}
for name, pool in pools.items():
    print(f"  {name}: {len(pool)}只")
