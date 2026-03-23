import requests
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

codes = ['sz300394', 'sz300223', 'sz300548', 'sh688521']
url = 'https://qt.gtimg.cn/q=' + ','.join(codes)
try:
    resp = requests.get(url, timeout=5)
    resp.encoding = 'gbk'
    lines = resp.text.strip().split('\n')
    results = []
    for line in lines:
        parts = line.split('~')
        if len(parts) > 32:
            code = parts[0].split('_')[1] if '_' in parts[0] else parts[0]
            name = parts[1]
            price = parts[3]
            yesterday_close = parts[4]
            change_pct = parts[32]
            results.append(f'{name}({code}): 现价={price}, 昨收={yesterday_close}, 涨跌幅={change_pct}%')
    for r in results:
        print(r)
except Exception as e:
    print(f'Error: {e}')
