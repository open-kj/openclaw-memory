import urllib.request
import json

stocks = [
    ('sz300394', '天孚通信'),
    ('sh688521', '芯原股份'),
    ('sz002594', '比亚迪'),
    ('sh688981', '中芯国际')
]

for code, name in stocks:
    try:
        url = f'https://qt.gtimg.cn/q={code}'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = resp.read().decode('gbk')
            parts = data.split('~')
            if len(parts) > 3:
                price = parts[3]
                yestclose = parts[4] if len(parts) > 4 else ''
                change_pct = parts[32] if len(parts) > 32 else ''
                print(f'{name} {code} 现价:{price} 昨收:{yestclose} 涨跌%:{change_pct}')
            else:
                print(f'{name} {code} 数据解析失败')
    except Exception as e:
        print(f'{name} {code} 获取失败:{e}')
