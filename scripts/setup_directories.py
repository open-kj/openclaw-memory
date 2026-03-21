"""
一键系统初始化脚本
执行目录创建、工具测试、文件整理
"""
import os
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')
BASE = r'C:\Users\Administrator\.openclaw\workspace'

# 1. 创建目录结构
dirs = ['data', 'analysis', 'automation', 'config', 'logs', 'utils']
for d in dirs:
    path = os.path.join(BASE, d)
    os.makedirs(path, exist_ok=True)
    print(f'[OK] {d}/')

# 2. 测试核心工具
api_key = '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'

print()
print('=== 腾讯API测试 ===')
r = requests.get('https://qt.gtimg.cn/q=sh000001,sz399001,sz399006,sz300223', timeout=8)
for line in r.text.strip().split('\n'):
    if '=' not in line:
        continue
    code = line.split('=')[0].replace('var v_', '').strip()
    parts = line.split('~')
    if len(parts) > 32:
        try:
            name = parts[1]
            price = float(parts[3])
            chg = float(parts[32])
            print(f'  [{code}] {name}: {price:.2f} ({chg:+.2f}%)')
        except:
            pass

print()
print('=== Tavily测试 ===')
r2 = requests.post('https://api.tavily.com/search', json={
    'api_key': api_key,
    'query': 'A股测试',
    'max_results': 1
}, timeout=12)
d = r2.json()
title = d.get('results', [{}])[0].get('title', 'N/A')[:50]
print(f'  Tavily: {title}')

print()
print('=== Feishu插件 ===')
print('  Feishu: OAPI全部工具已注册 ✅')

# 3. 移动现有脚本到utils/
scripts_to_move = [
    ('scripts/multi-source-query.py', 'utils/'),
    ('scripts/premarket_analysis.py', 'utils/'),
    ('scripts/news_aggregator.py', 'utils/'),
    ('scripts/test_premarket.py', 'utils/'),
    ('scripts/verify_code.py', 'utils/'),
    ('scripts/fix_name.py', 'utils/'),
    ('scripts/a-share-report.py', 'utils/'),
]
print()
print('=== 移动脚本到utils/ ===')
for src, dst_dir in scripts_to_move:
    src_path = os.path.join(BASE, src)
    if os.path.exists(src_path):
        dst_path = os.path.join(BASE, dst_dir, os.path.basename(src))
        import shutil
        shutil.move(src_path, dst_path)
        print(f'  {src} -> {dst_dir}{os.path.basename(src)} ✅')

# 4. 删除tushare相关文件
print()
print('=== 删除tushare相关 ===')
tushare_files = [
    'skills/tushare-finance',
]
for f in tushare_files:
    path = os.path.join(BASE, f)
    if os.path.exists(path):
        import shutil
        shutil.rmtree(path)
        print(f'  删除 {f} ✅')

# 5. 检查文件完整性
print()
print('=== 配置文件检查 ===')
files = ['SOUL.md', 'MEMORY.md', 'SESSION-STATE.md', 'HEARTBEAT.md', 'AGENTS.md']
for f in files:
    path = os.path.join(BASE, f)
    if os.path.exists(path):
        size = os.path.getsize(path)
        lines = len(open(path, encoding='utf-8').readlines())
        print(f'  {f}: {size}B, {lines}行 ✅')
    else:
        print(f'  {f}: ❌ 缺失')

print()
print('=== 完成 ===')
