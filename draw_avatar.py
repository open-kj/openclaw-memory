import urllib.request
import json
import os

# Doubao API endpoint (火山引擎)
# Note: This would require API credentials

prompt = "亚洲中国女性，精致五官，肤若凝脂，眼神妩媚，黑色长发，时尚露肩装，完美身材，明星范，性感迷人，超写实，高清照片"

print("尝试调用豆包API...")
print(f"提示词: {prompt}")

# Check if there's a doubao CLI or API we can use
# For now, let's try to use the doubao web API via curl

# Try to find doubao CLI
possible_paths = [
    r"C:\Users\Administrator\AppData\Local\Programs\doubao\doubao.exe",
    r"C:\Program Files\doubao\doubao.exe",
    os.path.expanduser(r"~\AppData\Local\Programs\doubao\doubao.exe"),
]

found = None
for p in possible_paths:
    if os.path.exists(p):
        found = p
        print(f"Found doubao at: {p}")
        break

if not found:
    print("Doubao not found in standard locations")
    # List AppData programs
    appdata = os.path.expanduser(r"~\AppData\Local\Programs")
    if os.path.exists(appdata):
        print(f"\nPrograms in {appdata}:")
        try:
            for item in os.listdir(appdata):
                print(f"  {item}")
        except:
            pass
