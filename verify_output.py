import os

out_dir = r'D:\AI_Scripts\2026-03-23_深户团购_E公司报价清单\03_Excel数据处理\output'
print("Output files:")
for f in sorted(os.listdir(out_dir)):
    size = os.path.getsize(os.path.join(out_dir, f))
    print(f"  {f} ({size:,} bytes)")
