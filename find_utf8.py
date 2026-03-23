import os
import glob

base = r"D:\AI_Scripts"
dirs = [d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d))]
for d in sorted(dirs):
    print(repr(d))
