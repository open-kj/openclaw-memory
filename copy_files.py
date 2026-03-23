import os
import shutil

dst = r"C:\Users\Administrator\Desktop\ceshi"

src = r"C:\Users\Administrator\.openclaw\workspace"

print("=== 目标目录文件 ===")
for f in sorted(os.listdir(dst)):
    size = os.path.getsize(os.path.join(dst, f))
    print(f"  {f} ({size:,} bytes)")
