import os

base = r"D:\AI_Scripts"
for item in os.listdir(base):
    full = os.path.join(base, item)
    if os.path.isdir(full):
        # Get short 8.3 name to identify
        import subprocess
        result = subprocess.run(['cmd', '/c', 'dir', '/x', base], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        for line in lines:
            if '~' in line:
                print(f"Short: {line.strip()}")
        
        # List subfolders
        subs = os.listdir(full)
        print(f"\nFolder: {repr(item)}")
        print(f"  Has 'output': {'output' in str(subs)}")
        for s in subs:
            print(f"  - {repr(s)}")
        break
