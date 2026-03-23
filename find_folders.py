import os
import glob

# Try to read with different encodings
base = r"D:\AI_Scripts"
for item in sorted(os.listdir(base)):
    full = os.path.join(base, item)
    if os.path.isdir(full):
        # List with cp437 (DOS encoding)
        try:
            sub_items = os.listdir(full)
            print(f"DIR: {item}")
            for s in sub_items:
                print(f"  - {s}")
        except:
            print(f"DIR (error): {item}")
