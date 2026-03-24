# -*- coding: utf-8 -*-
import csv
import os

# === 完整交易流水账 ===
# Day 1-5 (2026-03-19 至 2026-03-24)

entries = [
    # 日期, 时间, 操作类型, 股票/事件, 方向, 金额, 现金余额, 备注
    ("2026-03-19", "Day 1", "起始资金", "-", "投入", 1000000, 1000000, "模拟账户开始"),
    ("2026-03-20", "09:33", "止损卖出", "珈伟新能", "卖出", 11111, None, "成本15123，亏损-4012"),
    ("2026-03-20", "09:37", "止盈卖出", "源杰科技", "卖出", 22974, None, "成本177280，盈利+22974"),
    ("2026-03-20", "09:37", "止损卖出", "协创数据", "卖出", 16000, None, "成本21119，亏损-5119"),
    ("2026-03-20", "09:54", "买入（5只）", "5只股票", "买入", -945380, None, "总买入金额"),
    ("2026-03-20", "13:42", "卖出", "网达软件", "卖出", 187136, None, "部分仓位止盈"),
    ("2026-03-20", "13:42", "买入", "北京君正", "买入", -187180, None, "买入1530股"),
    ("2026-03-21", "盘中", "卖出", "炬芯科技", "卖出", 48000, None, "估算止盈"),
    ("2026-03-22", "盘中", "卖出", "长电科技", "卖出", 22416, None, "估算止盈"),
    ("2026-03-23", "09:49", "止损卖出", "北京君正", "卖出", 175491, None, "成本187180，亏损-11689"),
    ("2026-03-23", "09:49", "止损卖出", "博创科技", "卖出", 138960, None, "成本148570，亏损-9610"),
    ("2026-03-23", "12:41", "买入", "比亚迪", "买入", -348448, None, "买入3200股（模拟仓）"),
    ("2026-03-24", "08:46", "买入", "中芯国际", "买入", -199904, None, "买入2039股（模拟仓）"),
]

# 计算现金余额
cash = 1000000
for e in entries:
    date, time_, op, stock, direction, amount, balance, note = e
    if amount is not None:
        cash += amount
    entries[entries.index(e)] = (date, time_, op, stock, direction, amount, cash, note)

# 今日持仓市值
today_close = {
    "天孚通信": 298.71 * 618,
    "芯原股份": 205.88 * 1000,
    "比亚迪": 106.64 * 3200,
    "中芯国际": 99.25 * 2039,
}
total_value = sum(today_close.values())
final_assets = total_value + cash

# 输出CSV
output_path = os.path.join(os.path.expanduser("~"), "Desktop", "交易流水账_2026-03-24.csv")
with open(output_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["日期", "时间", "操作", "标的", "方向", "金额", "现金余额", "备注"])
    for e in entries:
        writer.writerow(e)
    writer.writerow([])
    writer.writerow(["=== 持仓明细（今日收盘2026-03-24）==="])
    for name, value in today_close.items():
        writer.writerow(["持仓", name, "", "", "", "", "", f"市值 {value:.0f}元"])
    writer.writerow(["持仓合计", "", "", "", "", "", total_value, "元"])
    writer.writerow(["现金", "", "", "", "", "", cash, "元"])
    writer.writerow(["总资产", "", "", "", "", "", final_assets, "元"])
    writer.writerow(["累计盈亏", "", "", "", "", "", final_assets - 1000000, f"元 ({((final_assets-1000000)/1000000*100):+.2f}%)"])

print(f"流水账已生成: {output_path}")
print(f"最终现金: {cash}")
print(f"持仓市值: {total_value:.0f}")
print(f"总资产: {final_assets:.0f}")
print(f"累计盈亏: {final_assets-1000000:+.0f} ({((final_assets-1000000)/1000000*100):+.2f}%)")
