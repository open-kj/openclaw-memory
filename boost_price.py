import pandas as pd
import numpy as np

f = r"C:\Users\Administrator\Desktop\ceshi\temp.xls"

# 读取，第一个sheet
df = pd.read_excel(f, sheet_name=0, header=None)
print(f"Shape: {df.shape}")

# 列5是单价，列6是总价
# 从第1行开始是数据（第0行是表头）
print("\n原始报价（列5=单价, 列6=总价）:")
for i in range(1, df.shape[0]):
    model = df.iloc[i, 1]
    unit_price = df.iloc[i, 5]
    total_price = df.iloc[i, 6]
    qty = df.iloc[i, 3]
    print(f"  {model}: 单价={unit_price}, 总价={total_price}, 数量={qty}")

# 提升15%
print("\n提升15%后:")
for i in range(1, df.shape[0]):
    old_unit = df.iloc[i, 5]
    old_total = df.iloc[i, 6]
    if pd.notna(old_unit) and isinstance(old_unit, (int, float)):
        new_unit = old_unit * 1.15
        new_total = old_total * 1.15
        df.iloc[i, 5] = new_unit
        df.iloc[i, 6] = new_total
        print(f"  {df.iloc[i, 1]}: {old_unit} -> {new_unit:.2f}")

# 保存
output_path = r"C:\Users\Administrator\Desktop\ceshi\深户团购报价清单_涨价15%.xlsx"
df.to_excel(output_path, index=False, header=False, sheet_name='Sheet1')
print(f"\n已保存到: {output_path}")
