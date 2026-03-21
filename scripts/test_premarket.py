import requests, sys
sys.stdout.reconfigure(encoding='utf-8')
API = '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'

stocks = [
    ('sz300394', '天孚通信', 'sz300394 光模块'),
    ('sz300223', '炬芯科技', 'sz300223 电池管理芯片'),
    ('sz300548', '博创科技', 'sz300548 光模块'),
    ('sh688521', '源杰股份', 'sh688521 半导体激光器'),
]

print('=== 持仓股新闻搜索（主动预判） ===')
for code, name, q in stocks:
    r = requests.post('https://api.tavily.com/search', json={
        'api_key': API, 'query': q, 'search_depth': 'basic', 'max_results': 2
    }, timeout=15)
    d = r.json()
    print(f'[{code}] {name}:')
    for item in d.get('results', [])[:2]:
        t = item['title'][:55]
        u = item['url'][:65]
        print(f'  {t}')
        print(f'  {u}')
    print()
