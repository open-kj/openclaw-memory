import urllib.request
import json

stocks = {
    'sz300394': '天孚通信',
    'sh688521': '芯原股份', 
    'sz002594': '比亚迪',
    'sh688981': '中芯国际'
}

codes = ','.join(stocks.keys())
url = f'https://qt.gtimg.cn/q={codes}'

try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        data = response.read().decode('gbk')
    
    lines = data.strip().split('\n')
    for line in lines:
        if 'pv.gif' in line or not line.strip():
            continue
        parts = line.split('~')
        if len(parts) > 32:
            code = parts[0].replace('"', '').replace('v_', '')
            name = stocks.get(code, code)
            price = parts[3]
            yesterday_close = parts[4]
            open_price = parts[5]
            print(f'{name}({code}): price={price}, yesterday_close={yesterday_close}, open={open_price}')
except Exception as e:
    print(f'Error: {e}')
