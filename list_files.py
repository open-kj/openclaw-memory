import os

folder = r"C:\Users\Administrator\Desktop\ceshi"
files = os.listdir(folder)
for f in files:
    full = os.path.join(folder, f)
    print(f"Name: {repr(f)}")
    print(f"Full path: {repr(full)}")
    print(f"Size: {os.path.getsize(full)}")
    print()
