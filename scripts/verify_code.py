import requests, sys
sys.stdout.reconfigure(encoding='utf-8')
r = requests.get('https://hq.sinajs.cn/list=sh688521,sh688498', headers={'Referer':'https://finance.sina.com.cn'}, timeout=8)
for line in r.text.strip().split('\n'):
    code = line.split('=')[0].replace('var hq_str_', '')
    content = line.split('"')[1]
    name = content.split(',')[0]
    price = content.split(',')[3]
    chg = content.split(',')[32]
    print(f'{code}: {name} | 现价={price} | 涨跌幅={chg}%')
